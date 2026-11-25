# -*- coding: utf-8 -*-
"""ATS-safe CV generator: single column, no tables/text boxes, base-14 font,
standard headings, text-selectable, contact details in the body."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, KeepTogether, Flowable)
import content as C

INK, SOFT, RULE = HexColor("#000000"), HexColor("#333333"), HexColor("#000000")
SCALE = float(os.environ.get("CV_SCALE", "0.99"))
BASE, LEAD = 9.5 * SCALE, 11.5 * SCALE

def S(**kw):
    d = dict(fontName="Helvetica", fontSize=BASE, leading=LEAD, textColor=INK,
             spaceBefore=0, spaceAfter=0)
    d.update(kw)
    return ParagraphStyle("s%d" % id(kw), **d)

st_name  = S(fontName="Helvetica-Bold", fontSize=21*SCALE, leading=24*SCALE, alignment=TA_CENTER)
st_head  = S(fontSize=10.2*SCALE, leading=13*SCALE, alignment=TA_CENTER, textColor=SOFT)
st_meta  = S(fontSize=9.3*SCALE, leading=11.6*SCALE, alignment=TA_CENTER, textColor=SOFT)
st_sec   = S(fontName="Helvetica-Bold", fontSize=9.8*SCALE, leading=11.5*SCALE)
st_body  = S()
st_org   = S(fontSize=9.3*SCALE, leading=11.3*SCALE, textColor=SOFT)
st_stack = S(fontName="Helvetica-Oblique", fontSize=9.2*SCALE, leading=11.2*SCALE, textColor=SOFT)
st_bul   = S(fontSize=9.4*SCALE, leading=11.3*SCALE, leftIndent=11, bulletIndent=1,
             bulletFontName="Symbol", bulletFontSize=9.0*SCALE, spaceAfter=0.9)
st_skill = S(fontSize=9.4*SCALE, leading=11.4*SCALE, spaceAfter=1.2)

class Rule(Flowable):
    """Hairline under a section heading. Vector only - carries no text."""
    def __init__(self, thickness=0.7, sb=1.1*SCALE, sa=2.4*SCALE):
        Flowable.__init__(self); self.t, self.sb, self.sa = thickness, sb, sa
    def wrap(self, aw, ah):
        self.width, self.height = aw, self.t + self.sb + self.sa
        return (self.width, self.height)
    def draw(self):
        self.canv.setStrokeColor(RULE); self.canv.setLineWidth(self.t)
        y = self.sa + self.t / 2.0
        self.canv.line(0, y, self.width, y)

class LineWithDate(Flowable):
    """Left title + right-aligned date on one baseline, emitted in reading order."""
    def __init__(self, left, right, lf="Helvetica-Bold", ls=10.1*SCALE,
                 rf="Helvetica", rs=9.2*SCALE, leading=12.2*SCALE):
        Flowable.__init__(self)
        self.left, self.right = left, right
        self.lf, self.ls, self.rf, self.rs, self.leading = lf, ls, rf, rs, leading
    def wrap(self, aw, ah):
        self.width, self.height = aw, self.leading
        return (aw, self.height)
    def draw(self):
        c = self.canv; y = self.leading - self.ls - 0.5
        c.setFont(self.lf, self.ls); c.setFillColor(INK); c.drawString(0, y, self.left)
        if self.right:
            c.setFont(self.rf, self.rs); c.setFillColor(SOFT)
            c.drawRightString(self.width, y + (self.ls - self.rs) * 0.35, self.right)

def section(title):
    return [Spacer(1, 4.0*SCALE), Paragraph(title, st_sec), Rule()]

def bullet(t):
    return Paragraph(t, st_bul, bulletText="•")

def build(path):
    doc = BaseDocTemplate(
        path, pagesize=LETTER,
        leftMargin=0.50*inch, rightMargin=0.50*inch,
        topMargin=0.36*inch, bottomMargin=0.30*inch,
        title="Miraj Bhattarai - Resume", author="Miraj Bhattarai",
        subject="Resume / Curriculum Vitae",
        keywords=("Machine Learning, Python, Scikit-learn, TensorFlow, PyTorch, FastAPI, Flask, React, "
                  "Full-Stack Developer, Freelance, Data Science, Nepal"),
        creator="Miraj Bhattarai")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="body")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame])])

    f = []
    f.append(Paragraph(C.NAME, st_name)); f.append(Spacer(1, 2.5))
    f.append(Paragraph(C.HEADLINE, st_head)); f.append(Spacer(1, 3.5))

    def linkify(line):
        out = line
        for text, href in C.LINKS.items():
            if text in out:
                out = out.replace(text, '<a href="%s" color="#000000">%s</a>' % (href, text))
        return out
    f.append(Paragraph(linkify(C.CONTACT_LINE_1), st_meta))
    f.append(Paragraph(linkify(C.CONTACT_LINE_2), st_meta))

    f += section("PROFESSIONAL SUMMARY")[1:]
    f.insert(len(f) - 2, Spacer(1, 2.0))
    f.append(Paragraph(C.SUMMARY, st_body))

    f += section("TECHNICAL SKILLS")
    for label, items in C.SKILLS:
        f.append(Paragraph("<b>%s:</b> %s" % (label, items), st_skill))

    f += section("EXPERIENCE")
    for i, job in enumerate(C.EXPERIENCE):
        blk = []
        if i: blk.append(Spacer(1, 4.0*SCALE))
        blk += [LineWithDate(job["role"], job["dates"]),
                Paragraph(job["org"], st_org)]
        if job.get("note"):
            blk.append(Paragraph(job["note"], st_stack))
        blk.append(Spacer(1, 1.8))
        blk += [bullet(b) for b in job["bullets"]]
        f.append(KeepTogether(blk))

    f += section("PROJECTS")
    for i, p in enumerate(C.PROJECTS):
        blk = []
        if i: blk.append(Spacer(1, 3.4*SCALE))
        blk.append(LineWithDate(p["title"], "", ls=9.9*SCALE, leading=11.9*SCALE))
        blk.append(Paragraph(p["meta"], st_org))
        if p.get("stack"): blk.append(Paragraph(p["stack"], st_stack))
        blk.append(Spacer(1, 1.4))
        blk += [bullet(b) for b in p["bullets"]]
        f.append(KeepTogether(blk))

    f += section("EDUCATION")
    for i, e in enumerate(C.EDUCATION):
        if i: f.append(Spacer(1, 2.8*SCALE))
        f.append(LineWithDate(e["degree"], e["dates"], ls=9.9*SCALE, leading=11.9*SCALE))
        f.append(Paragraph(e["org"], st_org))
        if e.get("detail"): f.append(Paragraph(e["detail"], st_skill))

    f += section("ACHIEVEMENTS AND LEADERSHIP")
    for a in C.ACHIEVEMENTS:
        f.append(bullet(a))

    doc.build(f)
    return path

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "Miraj_Bhattarai_CV.pdf")
    print("built")
