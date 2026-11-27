# Make every letter of a Word file black (DISC-476): all run colours, hyperlinks and style colours (headings use theme colours).
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def black(d):
    for root in (d.element, d.styles.element):
        for rpr in root.iter(qn('w:rPr')):
            c = rpr.find(qn('w:color'))
            if c is None:
                c = OxmlElement('w:color'); rpr.append(c)
            for k in list(c.attrib):
                if k != qn('w:val'): del c.attrib[k]
            c.set(qn('w:val'), '000000')
    for name in ('Heading 1', 'Heading 2', 'Heading 3', 'Heading 4', 'Heading 5', 'Title', 'Normal', 'List Paragraph', 'Hyperlink'):
        try:
            st = d.styles[name]
        except KeyError:
            continue
        rpr = st.element.get_or_add_rPr(); c = rpr.find(qn('w:color'))
        if c is None:
            c = OxmlElement('w:color'); rpr.append(c)
        for k in list(c.attrib):
            if k != qn('w:val'): del c.attrib[k]
        c.set(qn('w:val'), '000000')
