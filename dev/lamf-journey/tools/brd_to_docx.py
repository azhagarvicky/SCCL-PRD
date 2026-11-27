# Waiver BRD (web page) → Word, in the owner's BRD.docx format (their file used as the style template) – DISC-384
# Run ONLY when the owner asks for the Word file (DISC-297):
#   python3 lamf-journey/tools/brd_to_docx.py lamf-journey/brd-waive-off-scenarios.html exports/BRD_Charges_Waiver_Scenario-wise.docx
# Needs python-docx and beautifulsoup4, and the owner's BRD.docx as the template (TEMPLATE below).
import sys, re
import docx
from bs4 import BeautifulSoup, NavigableString, Tag
from docx.shared import Inches, Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SP = '/tmp/claude-0/-home-user-SCCL-PRD/ff2cc2d7-1750-5a78-8028-c60a6ead4a92/scratchpad/'
ROOT = '/home/user/SCCL-PRD/lamf-journey/'
SITE = 'https://azhagarvicky.github.io/SCCL-PRD/dev/lamf-journey/'
SRC, OUT = sys.argv[1], sys.argv[2]

TEMPLATE = __import__('os').path.join(__import__('os').path.dirname(__file__), 'brd_template.docx')
d = docx.Document(TEMPLATE)
body = d.element.body
numid = None
for p in d.paragraphs:
    np_ = p._p.find('.//' + qn('w:numPr'))
    if p.style.name == 'List Paragraph' and np_ is not None:
        numid = np_.find(qn('w:numId')).get(qn('w:val')); break
for el in list(body):
    if el.tag != qn('w:sectPr'):
        body.remove(el)
FONT = 'Calibri'
BODY = 12   # DISC-474: Normal and List Paragraph in Calibri 12; headings Calibri, sized below; tables 10, captions 9


def _style(name, size, bold=None):
    st = d.styles[name]; st.font.name = FONT; st.font.size = Pt(size)
    if bold is not None: st.font.bold = bold
    rf = st.element.get_or_add_rPr().find(qn('w:rFonts'))
    if rf is None: rf = OxmlElement('w:rFonts'); st.element.get_or_add_rPr().append(rf)
    for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'): rf.set(qn(k), FONT)
    for k in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        if rf.get(qn(k)) is not None: del rf.attrib[qn(k)]


for _n, _sz in (('Normal', BODY), ('List Paragraph', BODY), ('Heading 1', 20), ('Heading 2', 16), ('Heading 3', 14), ('Heading 4', 13), ('Heading 5', 12)):
    _style(_n, _sz, True if _n.startswith('Heading') else None)   # DISC-475: every heading bold
for sec in d.sections:
    sec.left_margin = sec.right_margin = Inches(0.75)


def add_run(p, text, bold=False, italic=False, size=BODY):
    if not text: return
    r = p.add_run(text); r.bold = bold or None; r.italic = italic or None; r.font.name = FONT; r.font.size = Pt(size)


def add_link(p, url, text, size=BODY):
    r_id = p.part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), r_id)
    r = OxmlElement('w:r'); rp = OxmlElement('w:rPr')
    for tag, val in (('w:color', '0563C1'), ('w:u', 'single')):
        e = OxmlElement(tag); e.set(qn('w:val'), val); rp.append(e)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(size * 2)); rp.append(sz)
    r.append(rp); t = OxmlElement('w:t'); t.text = text; t.set(qn('xml:space'), 'preserve'); r.append(t); h.append(r)
    p._p.append(h)


def norm(t):
    return re.sub(r'\s+', ' ', t)


def inline(p, node, bold=False, italic=False, size=BODY):
    """write the inline content of node into paragraph p (bold, italic, links, line breaks)."""
    for ch in node.children:
        if isinstance(ch, NavigableString):
            add_run(p, norm(str(ch)), bold, italic, size)
        elif isinstance(ch, Tag):
            if ch.name in ('ul', 'ol', 'table', 'figure', 'div'):
                continue                                    # block content handled by the caller
            if ch.name in ('b', 'strong'):
                inline(p, ch, True, italic, size)
            elif ch.name in ('i', 'em'):
                inline(p, ch, bold, True, size)
            elif ch.name == 'small':
                inline(p, ch, bold, italic, size - 1)
            elif ch.name == 'span' and set(ch.get('class') or []) & {'brd-ph', 'brd-tbc', 'm', 'c'}:
                k = [c for c in ch.get('class') if c in ('brd-ph', 'brd-tbc', 'm', 'c')][0]
                r = p.add_run(norm(ch.get_text())); r.bold = True; r.font.name = FONT; r.font.size = Pt(size)
                r.font.color.rgb = {'m': RGBColor(0x37, 0x30, 0xA3), 'c': RGBColor(0x06, 0x5F, 0x46)}.get(k, RGBColor(0xB4, 0x53, 0x09))
            elif ch.name == 'br':
                p.add_run().add_break()
            elif ch.name == 'a':
                href = ch.get('href', '')
                url = href if href.startswith('http') else SITE + href
                add_link(p, url, norm(ch.get_text()), size)
            else:
                inline(p, ch, bold, italic, size)


def bullet(li, level):
    p = d.add_paragraph(style='List Paragraph')
    if numid:
        pPr = p._p.get_or_add_pPr(); numPr = OxmlElement('w:numPr')
        il = OxmlElement('w:ilvl'); il.set(qn('w:val'), str(level)); ni = OxmlElement('w:numId'); ni.set(qn('w:val'), numid)
        numPr.append(il); numPr.append(ni); pPr.append(numPr)
    inline(p, li)
    for sub in li.find_all(['ul', 'ol'], recursive=False):
        for li2 in sub.find_all('li', recursive=False):
            bullet(li2, level + 1)
    for t in li.find_all('table', recursive=False):
        table(t)


def borders(tbl):
    tblPr = tbl._tbl.tblPr; b = OxmlElement('w:tblBorders')
    for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        x = OxmlElement('w:' + e); x.set(qn('w:val'), 'single'); x.set(qn('w:sz'), '4'); x.set(qn('w:color'), '999999'); b.append(x)
    tblPr.append(b)


def table(t):
    """HTML table (with rowspan / colspan) → Word table."""
    rows = t.find_all('tr')
    grid, ncol = [], 0
    spans = {}
    for r_i, tr in enumerate(rows):
        row, c = [], 0
        cells = tr.find_all(['th', 'td'], recursive=False)
        k = 0
        while k < len(cells) or (r_i, c) in spans:
            if (r_i, c) in spans:
                row.append(spans[(r_i, c)]); c += 1; continue
            cell = cells[k]; k += 1
            rs, cs = int(cell.get('rowspan', 1)), int(cell.get('colspan', 1))
            ref = {'cell': cell, 'id': id(cell), 'head': cell.name == 'th'}
            for j in range(cs):
                row.append(ref)
                for i in range(1, rs):
                    spans[(r_i + i, c + j)] = ref
            c += cs
        grid.append(row); ncol = max(ncol, len(row))
    wt = d.add_table(rows=len(grid), cols=ncol); borders(wt)
    done = {}
    for r_i, row in enumerate(grid):
        for c_i in range(ncol):
            ref = row[c_i] if c_i < len(row) else None
            if ref is None: continue
            wc = wt.cell(r_i, c_i)
            if ref['id'] in done:
                done[ref['id']] = done[ref['id']].merge(wc)
                continue
            done[ref['id']] = wc
            wc.text = ''
            inline(wc.paragraphs[0], ref['cell'], bold=ref['head'], size=10)
            if ref['head']:
                sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), 'D9E2F3'); wc._tc.get_or_add_tcPr().append(sh)
    # column widths (inches): fixed for the summary table, else by the longest text in each column
    usable = 7.0
    if 'brd-sum' in (t.get('class') or []) and ncol == 8:
        widths = [0.35, 0.8, 0.95, 0.95, 0.6, 1.5, 0.85, 1.0]
    else:
        lens = [1] * ncol
        for row in grid:
            for c_i, ref in enumerate(row):
                if ref is not None:
                    lens[c_i] = max(lens[c_i], min(len(norm(ref['cell'].get_text())), 60))
        tot = sum(lens); widths = [max(0.5, usable * l / tot) for l in lens]
        k = usable / sum(widths); widths = [w * k for w in widths]
    wt.autofit = False
    for i, gc in enumerate(wt._tbl.tblGrid.findall(qn('w:gridCol'))):
        gc.set(qn('w:w'), str(int(widths[i] * 1440)))
    for row in wt.rows:
        for i, c in enumerate(row.cells):
            if i < len(widths): c.width = Inches(widths[i])
    d.add_paragraph()


def figure(f):
    img = f.find('img'); cap = f.find('figcaption')
    if not img: return
    w = 3.6 if 'sm' in (f.get('class') or []) else 6.8
    p = d.add_paragraph(); p.add_run().add_picture(ROOT + img['src'], width=Inches(w))
    if cap:
        c = d.add_paragraph(); r = c.add_run(norm(cap.get_text())); r.italic = True; r.font.size = Pt(9); r.font.name = FONT
        r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)


COL = {'m': RGBColor(0x37, 0x30, 0xA3), 'c': RGBColor(0x06, 0x5F, 0x46), 'brd-ph': RGBColor(0xB4, 0x53, 0x09)}


def flow(f):
    """process flow (DISC-393): bold sub-scenario title, then the steps joined by arrows; mails in colour."""
    p = d.add_paragraph(); add_run(p, norm(f.find('b').get_text()).strip() if f.find('b') else 'Flow', bold=True, size=BODY)
    p.paragraph_format.space_after = Pt(0); p.paragraph_format.keep_with_next = True
    q = d.add_paragraph()
    for i, sp in enumerate(f.select('.fl > span')):
        if i: add_run(q, '  →  ', size=10)
        cls = [c for c in (sp.get('class') or []) if c in COL]
        r = q.add_run(norm(sp.get_text())); r.font.name = FONT; r.font.size = Pt(10)
        if cls: r.font.color.rgb = COL[cls[0]]; r.bold = True


def block(el):
    for ch in el.children:
        if not isinstance(ch, Tag):
            continue
        n = ch.name
        if n == 'h2':
            d.add_paragraph(norm(ch.get_text()).strip(), style='Heading 2')
        elif n == 'h3':
            d.add_paragraph(norm(ch.get_text()).strip(), style='Heading 3')
        elif n == 'h4':
            d.add_paragraph(norm(ch.get_text()).strip(), style='Heading 4')
        elif n == 'h5':
            d.add_paragraph(norm(ch.get_text()).strip(), style='Heading 5')
        elif n == 'p':
            p = d.add_paragraph(); inline(p, ch)
        elif n == 'ol':   # numbered steps (DISC-398)
            for i, li in enumerate(ch.find_all('li', recursive=False), 1):
                q = d.add_paragraph(style='List Paragraph'); q.paragraph_format.left_indent = Inches(0.35)
                q.paragraph_format.first_line_indent = Inches(-0.25); add_run(q, f'{i}.\t'); inline(q, li)
        elif n == 'ul':
            for li in ch.find_all('li', recursive=False):
                bullet(li, 0)
        elif n == 'table':
            table(ch)
        elif n == 'figure':
            figure(ch)
        elif n == 'div' and 'brd-flow' in (ch.get('class') or []):
            flow(ch)
        elif n == 'div':
            block(ch)


soup = BeautifulSoup(open(SRC, encoding='utf-8').read(), 'html.parser')
title = soup.find('h1').get_text(strip=True)
d.add_paragraph(title, style='Heading 1')
meta = soup.find(class_='brd-meta')
p = d.add_paragraph(); add_run(p, norm(meta.get_text(' ')).strip() if meta else '', size=10)
add_run(p, ' | Web: ', size=10); add_link(p, SITE + __import__('os').path.basename(SRC), 'Web page', 10)
block(soup.find(class_='brd-body'))
d.save(OUT)
print('saved', OUT)
