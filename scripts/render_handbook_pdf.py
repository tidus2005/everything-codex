from __future__ import annotations

import html
import re
import textwrap
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from PIL import Image as PILImage


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "Everything-CodeX.md"
OUT = ROOT / "docs" / "Everything-CodeX.pdf"


pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
FONT = "STSong-Light"


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCN",
            parent=base["Title"],
            fontName=FONT,
            fontSize=31,
            leading=38,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=20,
            wordWrap="CJK",
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCN",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=11.5,
            leading=17,
            textColor=colors.HexColor("#334155"),
            alignment=TA_CENTER,
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "H2CN",
            parent=base["Heading2"],
            fontName=FONT,
            fontSize=17,
            leading=23,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=15,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "h3": ParagraphStyle(
            "H3CN",
            parent=base["Heading3"],
            fontName=FONT,
            fontSize=12.5,
            leading=18,
            textColor=colors.HexColor("#1e293b"),
            spaceBefore=10,
            spaceAfter=5,
            wordWrap="CJK",
        ),
        "body": ParagraphStyle(
            "BodyCN",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=9.6,
            leading=14.4,
            textColor=colors.HexColor("#111827"),
            spaceAfter=5.5,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "small": ParagraphStyle(
            "SmallCN",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=8.1,
            leading=11.5,
            textColor=colors.HexColor("#1f2937"),
            wordWrap="CJK",
        ),
        "bullet": ParagraphStyle(
            "BulletCN",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=9.3,
            leading=13.8,
            leftIndent=13,
            firstLineIndent=-9,
            spaceAfter=3.5,
            textColor=colors.HexColor("#111827"),
            wordWrap="CJK",
        ),
        "quote": ParagraphStyle(
            "QuoteCN",
            parent=base["BodyText"],
            fontName=FONT,
            fontSize=9.5,
            leading=14.8,
            leftIndent=12,
            rightIndent=8,
            borderColor=colors.HexColor("#93c5fd"),
            borderWidth=1,
            borderPadding=8,
            backColor=colors.HexColor("#eff6ff"),
            textColor=colors.HexColor("#1e3a8a"),
            spaceBefore=4,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "code": ParagraphStyle(
            "CodeCN",
            fontName=FONT,
            fontSize=7.2,
            leading=9.4,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#f8fafc"),
            borderColor=colors.HexColor("#cbd5e1"),
            borderWidth=0.6,
            borderPadding=6,
            spaceBefore=4,
            spaceAfter=8,
        ),
    }


STYLES = styles()


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    return text


def para(text: str, style: str = "body") -> Paragraph:
    return Paragraph(inline(text), STYLES[style])


def code_block(text: str) -> Preformatted:
    out: list[str] = []
    for line in text.rstrip("\n").splitlines():
        if len(line) <= 92:
            out.append(line)
        else:
            out.extend(textwrap.wrap(line, width=92, replace_whitespace=False, drop_whitespace=False))
    return Preformatted("\n".join(out), STYLES["code"])


def image_flowable(rel_path: str):
    path = (SRC.parent / rel_path).resolve()
    if not path.exists():
        return para(f"[missing image: {rel_path}]", "quote")
    max_w = A4[0] - 3.2 * cm
    with PILImage.open(path) as im:
        w, h = im.size
    scale = min(max_w / w, 8.0 * cm / h)
    return Image(str(path), width=w * scale, height=h * scale, hAlign="CENTER")


def table_from(lines: list[str]):
    rows = []
    for line in lines:
        stripped = line.strip()
        if re.fullmatch(r"\|?[\s:|-]+\|?", stripped):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        rows.append([Paragraph(inline(c), STYLES["small"]) for c in cells])
    if not rows:
        return []
    col_count = max(len(r) for r in rows)
    for row in rows:
        while len(row) < col_count:
            row.append(Paragraph("", STYLES["small"]))
    available = A4[0] - 3.2 * cm
    widths = [available / col_count] * col_count
    table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ]
        )
    )
    return [table, Spacer(1, 7)]


def parse(text: str):
    lines = text.splitlines()
    story = []
    i = 0
    in_code = False
    code_lines: list[str] = []
    first_title = True

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        if stripped.startswith("```"):
            if in_code:
                story.append(code_block("\n".join(code_lines)))
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(raw)
            i += 1
            continue

        if not stripped:
            story.append(Spacer(1, 3))
            i += 1
            continue

        if stripped == "---":
            story.append(Spacer(1, 9))
            i += 1
            continue

        img_match = re.match(r"!\[[^\]]*\]\(([^)]+)\)", stripped)
        if img_match:
            image_path = img_match.group(1)
            story.append(Spacer(1, 5))
            story.append(image_flowable(image_path))
            story.append(Spacer(1, 9))
            if "codex-operating-system" in image_path:
                story.append(PageBreak())
            i += 1
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            story.extend(table_from(tbl))
            continue

        if stripped.startswith("# "):
            title = stripped[2:].strip()
            if first_title:
                story.append(Spacer(1, 2.0 * cm))
                story.append(para(title, "title"))
                first_title = False
            else:
                story.append(PageBreak())
                story.append(para(title, "h2"))
            i += 1
            continue

        if stripped.startswith("## "):
            if not stripped.startswith("## 阅读地图") and not stripped.startswith("## 0."):
                story.append(Spacer(1, 4))
            story.append(para(stripped[3:].strip(), "h2"))
            i += 1
            continue

        if stripped.startswith("### "):
            story.append(para(stripped[4:].strip(), "h3"))
            i += 1
            continue

        if stripped.startswith(">"):
            story.append(para(stripped.lstrip("> ").strip(), "quote"))
            i += 1
            continue

        if re.match(r"^[-*] ", stripped):
            story.append(para("- " + stripped[2:].strip(), "bullet"))
            i += 1
            continue

        if re.match(r"^\d+\. ", stripped):
            story.append(para(stripped, "bullet"))
            i += 1
            continue

        parts = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt == "---"
                or nxt.startswith("#")
                or nxt.startswith("```")
                or nxt.startswith("|")
                or nxt.startswith("> ")
                or nxt.startswith("![")
                or re.match(r"^[-*] ", nxt)
                or re.match(r"^\d+\. ", nxt)
            ):
                break
            parts.append(nxt)
            i += 1
        if parts[0].startswith("副标题:") or parts[0].startswith("版本:") or parts[0].startswith("适用对象:"):
            story.append(para(" ".join(parts), "subtitle"))
        else:
            story.append(para(" ".join(parts), "body"))
    return story


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.line(1.6 * cm, 1.35 * cm, A4[0] - 1.6 * cm, 1.35 * cm)
    canvas.drawString(1.6 * cm, 1.0 * cm, "Everything CodeX v2 draft")
    canvas.drawRightString(A4[0] - 1.6 * cm, 1.0 * cm, str(doc.page))
    canvas.restoreState()


def main():
    story = parse(SRC.read_text(encoding="utf-8"))
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.55 * cm,
        bottomMargin=1.75 * cm,
        title="Everything CodeX v2",
        author="tidus2005",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT)


if __name__ == "__main__":
    main()
