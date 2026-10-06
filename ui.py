"""Reusable UI building blocks (cards, badges, icons, tables, charts)."""
from __future__ import annotations
from html import escape
import streamlit as st
import plotly.graph_objects as go

ICONS = {
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    "upload": '<polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "bar": '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>',
    "compare": '<rect x="3" y="3" width="7" height="18" rx="1"/><rect x="14" y="3" width="7" height="18" rx="1"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "info": '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
}


def svg(name: str, size: int = 20, color: str = "#4F46E5", sw: float = 1.8) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def md(html: str):
    st.markdown(html, unsafe_allow_html=True)


def header(title: str, subtitle: str = ""):
    md(f'<div class="dc-title">{escape(title)}</div>' + (f'<div class="dc-sub">{escape(subtitle)}</div>' if subtitle else ""))


def card(key: str):
    return st.container(border=True, key=f"card_{key}")


def h3(text: str):
    md(f'<div class="dc-h3">{escape(text)}</div>')


def badge(text: str, kind: str | None = None) -> str:
    kinds = {"Found": "green", "Verified": "green", "Complete": "green", "Completed": "green", "Partial": "orange", "Needs Attention": "orange",
             "Attention": "orange", "Missing": "red", "Failed": "red", "Incomplete": "red", "Changed": "orange", "Unchanged": "green",
             "Only in A": "blue", "Only in B": "blue"}
    return f'<span class="dc-badge b-{kind or kinds.get(text, "gray")}">{escape(str(text))}</span>'


def pills(items) -> str:
    return "".join(f'<span class="dc-pill">{escape(str(i))}</span>' for i in items) or '<span class="dc-muted">None detected</span>'


def html_table(headers, rows, raw_cols=()):
    """rows: list of lists. Columns listed in raw_cols are inserted as HTML, others are escaped."""
    th = "".join(f"<th>{escape(h)}</th>" for h in headers)
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f"<td>{c if i in raw_cols else escape(str(c))}</td>" for i, c in enumerate(r)) + "</tr>"
    md(f'<div class="dc-wrap"><table class="dc-table"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')


def icon_class(ext: str) -> tuple[str, str]:
    e = ext.upper()
    if e == "DOCX":
        return "docx", "#2563EB"
    if e == "TXT":
        return "txt", "#475569"
    if e in ("JPG", "JPEG", "PNG"):
        return "img", "#16A34A"
    return "", "#DC2626"


def doc_html(doc: dict) -> str:
    cls, col = icon_class(doc["ext"])
    pages = f" • {doc['pages']} page{'s' if doc['pages'] != 1 else ''}"
    return (f'<div class="dc-doc"><div class="ico {cls}">{svg("file", 22, col)}</div><div><div class="nm">{escape(doc["name"])}</div>'
            f'<div class="meta">{escape(doc["ext"])} • {doc["size_label"]}{pages}</div></div></div>')


def metric(icon: str, value, label: str, bg: str, color: str) -> str:
    return (f'<div class="dc-metric" style="background:{bg}"><div class="ic">{svg(icon, 20, color)}</div>'
            f'<div><div class="v" style="color:{color}">{value}</div><div class="l">{escape(label)}</div></div></div>')


def empty_state(title: str, text: str, icon: str = "file"):
    md(f'<div class="dc-empty">{svg(icon, 34, "#818CF8")}<b>{escape(title)}</b>{escape(text)}</div>')


def ring(score: int, label: str) -> str:
    col = "#10B981" if score >= 85 else "#F59E0B" if score >= 60 else "#EF4444"
    r, c = 54, 2 * 3.14159 * 54
    return (f'<div style="text-align:center"><svg width="150" height="150" viewBox="0 0 140 140"><circle cx="70" cy="70" r="{r}" fill="none" stroke="#E2E8F0" stroke-width="12"/>'
            f'<circle cx="70" cy="70" r="{r}" fill="none" stroke="{col}" stroke-width="12" stroke-linecap="round" stroke-dasharray="{c * score / 100:.1f} {c:.1f}" transform="rotate(-90 70 70)"/>'
            f'<text x="70" y="70" text-anchor="middle" font-size="28" font-weight="800" fill="#172554" font-family="Inter,sans-serif">{score}%</text>'
            f'<text x="70" y="92" text-anchor="middle" font-size="12" fill="#64748B" font-family="Inter,sans-serif">{escape(label)}</text></svg></div>')


FONT = "Inter, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
PALETTE = ["#4F46E5", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4"]


def donut(labels, values, center: str, height=240, colors=None):
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.68, sort=False, marker=dict(colors=colors or PALETTE, line=dict(color="#fff", width=2)),
                           textinfo="none", hovertemplate="%{label}: %{value}<extra></extra>"))
    fig.update_layout(height=height, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", showlegend=True, font=dict(family=FONT),
                      legend=dict(font=dict(size=12, color="#475569"), orientation="v", y=0.5),
                      annotations=[dict(text=center, x=0.5 if True else 0, y=0.5, showarrow=False, font=dict(size=15, color="#172554", family=FONT))])
    fig.update_traces(domain=dict(x=[0, 0.62]))
    fig.layout.annotations[0].x = 0.31
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def bars(labels, values, colors, height=240):
    fig = go.Figure(go.Bar(x=labels, y=values, marker_color=colors, text=values, textposition="outside", width=0.45))
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      yaxis=dict(gridcolor="#EEF2F6", dtick=1, rangemode="tozero"), xaxis=dict(showgrid=False), font=dict(family=FONT, color="#475569", size=12))
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
