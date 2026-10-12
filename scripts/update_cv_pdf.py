#!/usr/bin/env python3
"""Update the supplied CV, preserving its original sections and older presentations.

Requires PyMuPDF. Run with the Python environment that provides `fitz`.
The immutable original PDF and editorial.json are the sources.
"""
from pathlib import Path
from html import escape, unescape
import json
import re
import fitz

ROOT = Path(__file__).resolve().parents[1]
VERSION = "October 12, 2026"
OUTPUT = ROOT.parent / "output/pdf/Tomohide_R_Sato.pdf"


def lines(markup):
    text = re.sub(r"<br\s*/?>", "\n", markup, flags=re.I)
    text = unescape(re.sub(r"<[^>]*>", "", text))
    return [x.strip() for x in text.splitlines() if x.strip()]


def conference_section(locale, title):
    return next(s for s in locale["cv"] if s["title"] == title)["entries"]


def put_html(page, rect, html, css):
    spare, scale = page.insert_htmlbox(rect, html, css=css, scale_low=1)
    if spare < 0 or scale != 1:
        raise ValueError("Conference text does not fit at the intended font size")


def main():
    data = json.loads((ROOT / "content/editorial.json").read_text())
    en = conference_section(data["locales"]["en"], "Academic conferences")
    ja = conference_section(data["locales"]["ja"], "学会発表")
    doc = fitz.open(ROOT / "content/cv-original.pdf")
    original = doc[0].get_text("text", clip=fitz.Rect(20, 504, 590, 739))
    original = re.sub(r"(?<=\w)-\s*\n(?=\w)", "-", original)
    earlier = []
    for item in re.split(r"(?m)(?=^202\d [A-Z][a-z]{2}\s)", original):
        item = " ".join(item.split())
        match = re.match(r"^(202\d [A-Z][a-z]{2})\s+(.+)$", item)
        if match:
            earlier.append((match[1], match[2]))
    if len(earlier) != 7:
        raise ValueError("Could not recover all seven original presentations")
    latest_old = max(
        (int(date[:4]), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(date[5:8]))
        for date, _ in earlier
    )
    recent = []
    for english, japanese in zip(en, ja, strict=True):
        date = re.match(r"^(202\d) ([A-Z][a-z]{2})", english["date"])
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(date[2])
        if (int(date[1]), month) > latest_old:
            e, j = lines(english["html"]), lines(japanese["html"])
            recent.append(f'<div class="entry"><p><b>{escape(english["date"])}</b> &nbsp; {escape(e[0])}</p><p class="detail">{escape(e[1])}</p><p class="detail japanese">Japanese title: {escape(j[1])}</p></div>')
    if len(recent) != 3:
        raise ValueError("Expected the December presentation and two September presentations")
    first = doc[0]
    first.add_redact_annot(fitz.Rect(42, 485, 580, 739), fill=(1, 1, 1))
    for rect in first.search_for("Date of this version: June 3, 2026"):
        first.add_redact_annot(rect + (-2, -1, 2, 2), fill=(1, 1, 1))
    first.apply_redactions(images=0, graphics=0)
    put_html(first, fitz.Rect(170, 88, 442, 105), f"Date of this version: {VERSION}",
             "body {font-family: serif; font-size: 9pt; line-height: 1.2; margin: 0; text-align: center;}")
    css = """body {font-family: serif; font-size: 9.3pt; line-height: 1.28; margin: 0;}
      h2 {font-size: 12.5pt; color: #365f91; margin: 0 0 7pt;}
      p {margin: 0;} .entry {margin-bottom: 8pt;} .detail {margin-left: 11pt;}
      .japanese {font-size: 8.6pt;} .continued {font-size: 8.5pt; margin-top: 5pt; color: #555;}"""
    put_html(first, fitz.Rect(46.775, 486.5, 568, 738),
             "<h2>Academic Conference Presentations</h2>" + "".join(recent) +
             '<p class="continued">Earlier presentations continue on the following page.</p>', css)
    continuation = doc.new_page(pno=1, width=612, height=792)
    put_html(continuation, fitz.Rect(46.775, 41, 568, 65), "<b>Tomohide R. Sato, M.D.</b>",
             "body {font-family: serif; font-size: 12pt; line-height: 1.2; margin: 0;}")
    historical = "".join(f'<div class="entry"><p><b>{escape(date)}</b> &nbsp; {escape(text)}</p></div>' for date, text in earlier)
    put_html(continuation, fitz.Rect(46.775, 73, 568, 733),
             "<h2>Academic Conference Presentations (continued)</h2>" + historical,
             "body {font-family: serif; font-size: 10.5pt; line-height: 1.5; margin: 0;} h2 {font-size: 14pt; color: #365f91; margin: 0 0 18pt;} p {margin: 0;} .entry {margin-bottom: 16pt;}")
    for index, page in enumerate(doc):
        for rect in page.search_for("Tomohide R. Sato, M.D. — Curriculum Vitae — June 3, 2026"):
            page.add_redact_annot(rect + (-2, -1, 2, 2), fill=(1, 1, 1))
        page.apply_redactions(images=0, graphics=0)
        put_html(page, fitz.Rect(90, 745.8, 522, 765),
                 f"Tomohide R. Sato, M.D. - Curriculum Vitae - {VERSION} - {index + 1}/{len(doc)}",
                 "body {font-family: serif; font-size: 8pt; line-height: 1.2; margin: 0; text-align: center;}")
    metadata = doc.metadata
    metadata.update({"title": "Curriculum Vitae - Tomohide R. Sato", "subject": "CV updated with September presentations and scheduled December 2026 presentation", "modDate": "D:20261012000000+09'00'"})
    doc.set_metadata(metadata)
    doc.subset_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT, garbage=4, deflate=True)
    doc.close()
    print(f"Updated CV: {OUTPUT}")


if __name__ == "__main__":
    main()
