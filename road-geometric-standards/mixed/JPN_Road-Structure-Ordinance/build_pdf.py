# -*- coding: utf-8 -*-
"""
Build a readable PDF of 道路構造令 (Road Structure Ordinance) from the official
e-Gov Law Search XML (API v1 lawdata, lawid 345CO0000000320).

Source XML: https://laws.e-gov.go.jp/api/1/lawdata/345CO0000000320
The e-Gov system serves the law only as HTML/XML (no native PDF export),
so this renders the authoritative XML into a faithful PDF.
"""
import xml.etree.ElementTree as ET
from fpdf import FPDF

SRC = "egov_api_v1.xml"
OUT = "JPN_Road-Structure-Ordinance_egov.pdf"
FONT_REGULAR = r"C:\Windows\Fonts\YuGothR.ttc"
FONT_BOLD = r"C:\Windows\Fonts\YuGothB.ttc"

tree = ET.parse(SRC)
root = tree.getroot()


def txt(el):
    """Collect all text under an element in document order, dropping Ruby Rt
    (reading aids) but keeping the base RubyText so we don't lose kanji."""
    parts = []

    def walk(e):
        if e.tag == "Rt":
            return  # skip phonetic reading
        if e.text:
            parts.append(e.text)
        for c in list(e):
            walk(c)
            if c.tail:
                parts.append(c.tail)

    walk(el)
    return "".join(parts).strip()


# ---- gather metadata ----
law = root.find(".//Law")
law_title = txt(root.find(".//LawTitle")) if root.find(".//LawTitle") is not None else "道路構造令"
law_num = txt(root.find(".//LawNum")) if root.find(".//LawNum") is not None else ""

pdf = FPDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_font("Yu", "", FONT_REGULAR)
pdf.add_font("Yu", "B", FONT_BOLD)
pdf.add_page()
pdf.set_margins(18, 18, 18)

EPW = pdf.w - 2 * 18  # effective page width


def line(s, size=10, style="", gap=1.5, indent=0):
    if not s:
        return
    pdf.set_font("Yu", style, size)
    x0 = 18 + indent
    pdf.set_x(x0)
    pdf.multi_cell(EPW - indent, size * 0.55 + 2.2, s, align="L")
    pdf.ln(gap)


# ---- title block ----
line(law_title, size=18, style="B", gap=2)
if law_num:
    line(law_num, size=11, gap=1)
line("出典: e-Gov法令検索（デジタル庁／総務省）公式XMLより生成  "
     "Source: e-Gov Law Search (official XML), lawid 345CO0000000320",
     size=8, gap=1)
line("URL: https://laws.e-gov.go.jp/document?lawid=345CO0000000320_20201125_502CO0000000329",
     size=8, gap=3)

enact = root.find(".//EnactStatement")
if enact is not None:
    line(txt(enact), size=9, gap=3)


def render_table(tbl):
    for row in tbl.findall(".//TableRow"):
        cells = []
        for col in row.findall("TableColumn"):
            cells.append(txt(col))
        rowtext = " ｜ ".join(c for c in cells if c)
        if rowtext:
            line("  " + rowtext, size=8.5, gap=0.6, indent=6)


def render_sentences(parent, size=10, indent=0):
    s = " ".join(txt(se) for se in parent.findall("Sentence") if txt(se))
    if s:
        line(s, size=size, gap=1, indent=indent)


def render_paragraph(p):
    num_el = p.find("ParagraphNum")
    num = txt(num_el) if num_el is not None else ""
    cap = p.find("ParagraphCaption")
    if cap is not None and txt(cap):
        line(txt(cap), size=9.5, style="B", gap=0.5)
    ps = p.find("ParagraphSentence")
    body = ""
    if ps is not None:
        body = " ".join(txt(se) for se in ps.findall("Sentence") if txt(se))
    prefix = (num + " ") if num else ""
    line(prefix + body, size=10, gap=1, indent=4)
    # items
    for item in p.findall("Item"):
        it = item.find("ItemTitle")
        itt = txt(it) if it is not None else ""
        isent = item.find("ItemSentence")
        ib = ""
        if isent is not None:
            ib = " ".join(txt(se) for se in isent.findall("Sentence") if txt(se))
            for col in isent.findall("Column"):
                ib += " " + txt(col)
        line((itt + " " + ib).strip(), size=9.5, gap=0.6, indent=10)
    # tables inside paragraph
    for tbl in p.findall(".//TableStruct"):
        ttl = tbl.find("TableStructTitle")
        if ttl is not None and txt(ttl):
            line(txt(ttl), size=9, style="B", gap=0.4, indent=4)
        render_table(tbl)


def render_article(art):
    pdf.ln(1)
    cap = art.find("ArticleCaption")
    if cap is not None and txt(cap):
        line(txt(cap), size=10, style="B", gap=0.4)
    title = art.find("ArticleTitle")
    t = txt(title) if title is not None else ""
    if t:
        line(t, size=11, style="B", gap=0.6)
    for p in art.findall("Paragraph"):
        render_paragraph(p)


# ---- main provision ----
main = root.find(".//MainProvision")
if main is not None:
    for art in main.findall("Article"):
        render_article(art)
    # paragraphs/tables directly under main (rare)
    for p in main.findall("Paragraph"):
        render_paragraph(p)

# ---- supplementary provisions ----
for sp in root.findall(".//SupplProvision"):
    pdf.ln(2)
    lbl = sp.find("SupplProvisionLabel")
    if lbl is not None and txt(lbl):
        line(txt(lbl), size=12, style="B", gap=1)
    for art in sp.findall("Article"):
        render_article(art)
    for p in sp.findall("Paragraph"):
        render_paragraph(p)
    for tbl in sp.findall(".//TableStruct"):
        ttl = tbl.find("TableStructTitle")
        if ttl is not None and txt(ttl):
            line(txt(ttl), size=9, style="B", gap=0.4)
        render_table(tbl)

pdf.output(OUT)
print("WROTE", OUT)
