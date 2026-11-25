# -*- coding: utf-8 -*-
"""Editable ATS-safe DOCX twin of the PDF. Single column, no tables, no text boxes."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import content as C

BLACK, GREY, FONT = RGBColor(0,0,0), RGBColor(0x33,0x33,0x33), "Calibri"

def set_font(run, size, bold=False, italic=False, color=BLACK):
    run.font.name = FONT; run.font.size = Pt(size)
    run.bold = bold; run.italic = italic; run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None: rf = OxmlElement('w:rFonts'); rpr.append(rf)
    for a in ('w:ascii','w:hAnsi','w:cs'): rf.set(qn(a), FONT)

def para(doc, sb=0, sa=0, line=1.0, align=None):
    p = doc.add_paragraph(); pf = p.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(sb), Pt(sa), line
    if align is not None: p.alignment = align
    return p

def bottom_border(p):
    pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement('w:pBdr'); b = OxmlElement('w:bottom')
    b.set(qn('w:val'),'single'); b.set(qn('w:sz'),'6'); b.set(qn('w:space'),'1'); b.set(qn('w:color'),'000000')
    pbdr.append(b); pPr.append(pbdr)

def section(doc, title):
    p = para(doc, sb=8, sa=3); set_font(p.add_run(title.upper()), 10.5, bold=True); bottom_border(p)

def bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet"); pf = p.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(0), Pt(1.5), 1.0
    pf.left_indent, pf.first_line_indent = Inches(0.22), Inches(-0.14)
    set_font(p.add_run(text), 10)

def right_tab(p, w=7.5):
    p.paragraph_format.tab_stops.add_tab_stop(Inches(w), WD_TAB_ALIGNMENT.RIGHT)

def build(path):
    doc = Document(); s = doc.sections[0]
    s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Inches(0.5)
    usable = 7.5
    n = doc.styles['Normal']; n.font.name = FONT; n.font.size = Pt(10)

    p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, sa=1); set_font(p.add_run(C.NAME), 21, bold=True)
    p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, sa=2); set_font(p.add_run(C.HEADLINE), 10.5, color=GREY)
    for line in (C.CONTACT_LINE_1, C.CONTACT_LINE_2):
        p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, sa=0); set_font(p.add_run(line), 9.5, color=GREY)

    section(doc, "Professional Summary")
    p = para(doc, sa=0); set_font(p.add_run(C.SUMMARY), 10)

    section(doc, "Technical Skills")
    for label, items in C.SKILLS:
        p = para(doc, sa=1.5); set_font(p.add_run(label + ": "), 10, bold=True); set_font(p.add_run(items), 10)

    section(doc, "Experience")
    for i, job in enumerate(C.EXPERIENCE):
        p = para(doc, sb=(5 if i else 0), sa=0); right_tab(p, usable)
        set_font(p.add_run(job["role"]), 10.5, bold=True)
        set_font(p.add_run("\t" + job["dates"]), 9.5, color=GREY)
        p = para(doc, sa=(0 if job.get("note") else 2)); set_font(p.add_run(job["org"]), 9.5, color=GREY)
        if job.get("note"):
            p = para(doc, sa=2); set_font(p.add_run(job["note"]), 9.5, italic=True, color=GREY)
        for b in job["bullets"]: bullet(doc, b)

    section(doc, "Projects")
    for i, pr in enumerate(C.PROJECTS):
        p = para(doc, sb=(5 if i else 0), sa=0); set_font(p.add_run(pr["title"]), 10.5, bold=True)
        p = para(doc, sa=(0 if pr.get("stack") else 2)); set_font(p.add_run(pr["meta"]), 9.5, color=GREY)
        if pr.get("stack"):
            p = para(doc, sa=2); set_font(p.add_run(pr["stack"]), 9.5, italic=True, color=GREY)
        for b in pr["bullets"]: bullet(doc, b)

    section(doc, "Education")
    for i, e in enumerate(C.EDUCATION):
        p = para(doc, sb=(4 if i else 0), sa=0); right_tab(p, usable)
        set_font(p.add_run(e["degree"]), 10.5, bold=True)
        set_font(p.add_run("\t" + e["dates"]), 9.5, color=GREY)
        p = para(doc, sa=0); set_font(p.add_run(e["org"]), 9.5, color=GREY)
        if e.get("detail"):
            p = para(doc, sa=0); set_font(p.add_run(e["detail"]), 10)

    section(doc, "Achievements and Leadership")
    for a in C.ACHIEVEMENTS: bullet(doc, a)

    cp = doc.core_properties
    cp.title, cp.author = "Miraj Bhattarai - Resume", "Miraj Bhattarai"
    cp.subject = "Resume / Curriculum Vitae"
    cp.keywords = ("Machine Learning, Python, Scikit-learn, TensorFlow, PyTorch, FastAPI, Flask, React, "
                   "Full-Stack Developer, Freelance, Data Science, Nepal")
    doc.save(path); return path

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "Miraj_Bhattarai_CV.docx"); print("built docx")
