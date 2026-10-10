#!/usr/bin/env python3
"""Build one branded brand-system PDF per project into public/docs/.

Usage: python3 scripts/build-brand-docs.py
See scripts/BRAND-DOCS.md for where the source documents live.
"""
import os
import re
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

HOME = os.path.expanduser("~")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "public", "docs")

INK = HexColor("#1B1A17")
ACCENT = HexColor("#4338CA")
DEEP = HexColor("#1E1B4B")
SOFT = HexColor("#55524B")
LINE = HexColor("#E4DED2")
PAPER = HexColor("#FAF7F2")

FONT_CANDIDATES = [
    ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "ArialUni", "ArialUni"),
    ("/Library/Fonts/Arial Unicode.ttf", "ArialUni", "ArialUni"),
]

PROJECTS = [
    {
        "slug": "mj-health-brand-system",
        "title": "MJ Health Nutrition & Fitness",
        "subtitle": "Brand system: voice guidelines, positioning and customer profiles",
        "source": os.path.join(ROOT, "scripts", "brand-docs", "mj-health.md"),
    },
    {
        "slug": "panther-fit-brand-system",
        "title": "Panther Fit",
        "subtitle": "Brand system: context, voice guidelines and customer profile",
        "source": os.path.join(ROOT, "scripts", "brand-docs", "panther-fit.md"),
    },
]


def register_font():
    for path, regular, bold in FONT_CANDIDATES:
        if os.path.isfile(path):
            pdfmetrics.registerFont(TTFont(regular, path))
            return regular, bold
    return "Helvetica", "Helvetica-Bold"


BODY_FONT, BOLD_FONT = register_font()


def styles():
    base = dict(fontName=BODY_FONT)
    return {
        "h1": ParagraphStyle("h1", **base, fontSize=17, leading=22, spaceBefore=16,
                             spaceAfter=8, textColor=DEEP),
        "h2": ParagraphStyle("h2", **base, fontSize=13, leading=17, spaceBefore=14,
                             spaceAfter=6, textColor=ACCENT),
        "h3": ParagraphStyle("h3", **base, fontSize=11, leading=15, spaceBefore=10,
                             spaceAfter=4, textColor=INK),
        "body": ParagraphStyle("body", **base, fontSize=9.5, leading=14.5,
                               spaceAfter=6, textColor=SOFT),
        "bullet": ParagraphStyle("bullet", **base, fontSize=9.5, leading=14.5,
                                 leftIndent=10, bulletIndent=1, spaceAfter=3,
                                 textColor=SOFT),
        "cell": ParagraphStyle("cell", **base, fontSize=8.5, leading=12, textColor=SOFT),
        "cellhead": ParagraphStyle("cellhead", **base, fontSize=8.5, leading=12,
                                   textColor=white),
    }


ST = styles()


def inline(text):
    """Markdown inline to reportlab markup."""
    text = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", text)
    # No em or en dashes in output, per house style.
    return text.replace("—", ", ").replace("–", " to ")


def table_from(rows):
    head, body = rows[0], rows[1:]
    data = [[Paragraph(inline(c), ST["cellhead"]) for c in head]]
    data += [[Paragraph(inline(c), ST["cell"]) for c in r] for r in body]
    cols = (A4[0] - 36 * mm) / max(len(head), 1)
    t = Table(data, colWidths=[cols] * len(head), hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DEEP),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, PAPER]),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def md_to_flowables(md):
    flow, pending, i = [], [], 0
    lines = md.split("\n")

    def flush_table():
        if pending:
            flow.append(table_from(pending))
            flow.append(Spacer(1, 8))
            pending.clear()

    while i < len(lines):
        raw = lines[i].rstrip()
        line = raw.strip()
        i += 1

        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            pending.append(cells)
            continue
        flush_table()

        if not line or set(line) <= set("-*_") and len(line) >= 3:
            continue
        if line.startswith("### "):
            flow.append(Paragraph(inline(line[4:]), ST["h3"]))
        elif line.startswith("## "):
            flow.append(Paragraph(inline(line[3:]), ST["h2"]))
        elif line.startswith("# "):
            flow.append(Paragraph(inline(line[2:]), ST["h1"]))
        elif re.match(r"^[-*] ", line):
            flow.append(Paragraph(inline(line[2:]), ST["bullet"], bulletText="•"))
        elif re.match(r"^\d+\. ", line):
            n, rest = line.split(". ", 1)
            flow.append(Paragraph(inline(rest), ST["bullet"], bulletText=f"{n}."))
        elif line.startswith("> "):
            flow.append(Paragraph(inline(line[2:]), ST["bullet"]))
        else:
            flow.append(Paragraph(inline(line), ST["body"]))

    flush_table()
    return flow


def build(project):
    src = project["source"]
    if not os.path.isfile(src):
        print(f"  missing source, skipped: {src}")
        return None
    chunks = [open(src, encoding="utf-8").read()]

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, project["slug"] + ".pdf")
    title = project["title"]
    subtitle = project["subtitle"]

    def decorate(canv, doc):
        canv.saveState()
        canv.setFillColor(DEEP)
        canv.rect(0, A4[1] - 16 * mm, A4[0], 16 * mm, fill=1, stroke=0)
        canv.setFillColor(white)
        canv.setFont(BOLD_FONT, 8.5)
        canv.drawString(18 * mm, A4[1] - 10.5 * mm, title)
        canv.setFillColor(HexColor("#A5A0F5"))
        canv.drawRightString(A4[0] - 18 * mm, A4[1] - 10.5 * mm, "Prepared by Tony Quang")
        canv.setStrokeColor(LINE)
        canv.setLineWidth(0.5)
        canv.line(18 * mm, 14 * mm, A4[0] - 18 * mm, 14 * mm)
        canv.setFillColor(SOFT)
        canv.setFont(BODY_FONT, 7.5)
        canv.drawString(18 * mm, 10 * mm, subtitle)
        canv.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {doc.page}")
        canv.restoreState()

    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=18 * mm,
                          rightMargin=18 * mm, topMargin=24 * mm, bottomMargin=20 * mm,
                          title=f"{title} brand system", author="Tony Quang")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=decorate)])

    story = []
    for n, chunk in enumerate(chunks):
        if n:
            story.append(Spacer(1, 14))
        story.extend(md_to_flowables(chunk))
    doc.build(story)
    return out_path


if __name__ == "__main__":
    wrote = []
    for proj in PROJECTS:
        print(f"building {proj['slug']}")
        path = build(proj)
        if path:
            wrote.append(path)
            print(f"  wrote {path} ({os.path.getsize(path) // 1024} KB)")
    if not wrote:
        sys.exit("No PDFs written.")
