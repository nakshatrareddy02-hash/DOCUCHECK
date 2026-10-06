"""SQLite persistence for history and generated reports (documents themselves are never stored)."""
from __future__ import annotations
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "docucheck.db"
REPORT_DIR = ROOT / "data" / "reports"


def _conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.executescript("""
    CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT, document TEXT, doc_type TEXT, action TEXT,
        status TEXT, score REAL, created TEXT, payload TEXT);
    CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT UNIQUE, document TEXT,
        report_type TEXT, status TEXT, created TEXT, path TEXT);""")
    return c


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def add_history(document, doc_type, action, status, score=None, payload=None):
    with _conn() as c:
        c.execute("INSERT INTO history(document,doc_type,action,status,score,created,payload) VALUES(?,?,?,?,?,?,?)",
                  (document, doc_type, action, status, score, now(), json.dumps(payload or {}, default=str)))


def list_history(limit=500):
    with _conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM history ORDER BY id DESC LIMIT ?", (limit,))]


def delete_history(hid=None):
    with _conn() as c:
        c.execute("DELETE FROM history WHERE id=?", (hid,)) if hid else c.execute("DELETE FROM history")


def save_report(filename, document, report_type, status, data: bytes):
    path = REPORT_DIR / filename
    path.write_bytes(data)
    with _conn() as c:
        c.execute("DELETE FROM reports WHERE filename=?", (filename,))
        c.execute("INSERT INTO reports(filename,document,report_type,status,created,path) VALUES(?,?,?,?,?,?)",
                  (filename, document, report_type, status, now(), str(path)))


def list_reports():
    with _conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM reports ORDER BY id DESC")]


def read_report(path) -> bytes | None:
    try:
        return Path(path).read_bytes()
    except OSError:
        return None


def clear_all():
    with _conn() as c:
        c.execute("DELETE FROM history")
        c.execute("DELETE FROM reports")
    for f in REPORT_DIR.glob("*.pdf"):
        try:
            f.unlink()
        except OSError:
            pass


def stats() -> dict:
    h = list_history(10000)
    docs = {r["document"] for r in h if r["action"] != "Comparison" and r["action"] != "Multi-Document"} or {r["document"] for r in h}
    latest = {}
    for r in reversed(h):  # oldest -> newest, so the newest verification per document wins
        if r["action"] == "Verification":
            latest[r["document"]] = r
    ver = list(latest.values())
    scores = [r["score"] for r in ver if r["score"] is not None]
    types = {}
    for r in h:
        if r["action"] in ("Analysis", "Verification"):
            types.setdefault(r["document"], r["doc_type"])
    from collections import Counter
    return {"processed": len({r["document"] for r in h}), "verified": sum(1 for r in ver if r["status"] == "Verified"),
            "compared": sum(1 for r in h if r["action"] == "Comparison"),
            "avg": round(sum(scores) / len(scores)) if scores else None,
            "types": Counter(types.values()),
            "results": Counter(r["status"] for r in ver), "recent": h[:5], "total": len(h)}
