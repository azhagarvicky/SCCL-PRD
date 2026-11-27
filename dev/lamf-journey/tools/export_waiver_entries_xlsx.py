# Waiver BRD accounting entries (UNO) → Excel (DISC-397). Reads the generated brd-waive-off-scenarios.html so the sheet always matches the BRD.
# Run after build_pages.py:  python3 lamf-journey/tools/export_waiver_entries_xlsx.py
import os, re
from bs4 import BeautifulSoup, Tag
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(ROOT, 'brd-waive-off-scenarios.html')   # DISC-464: the only Waiver BRD
OUT = os.path.join(ROOT, '..', 'exports', 'Waiver_BRD_Accounting_Entries.xlsx')

HEAD = PatternFill('solid', fgColor='1F3864'); SCEN = PatternFill('solid', fgColor='D9E2F3'); SUB = PatternFill('solid', fgColor='F2F2F2')
TOT = PatternFill('solid', fgColor='FFF2CC'); NONE = PatternFill('solid', fgColor='FCE4D6')
thin = Side(style='thin', color='999999'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WHITE = Font(bold=True, color='FFFFFF'); BOLD = Font(bold=True)
txt = lambda el: re.sub(r'\s+', ' ', el.get_text(' ')).strip()


def num(v):
    v = v.replace(',', '').strip()
    return float(v) if re.fullmatch(r'-?\d+(\.\d+)?', v) else None


def header(ws, r, cols):
    for c, h in enumerate(cols, 1):
        x = ws.cell(r, c, h); x.font = WHITE; x.fill = HEAD; x.border = BOX; x.alignment = Alignment(wrap_text=True, vertical='center')


def widths(ws, w):
    for i, v in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(i)].width = v


soup = BeautifulSoup(open(SRC, encoding='utf-8').read(), 'html.parser')
body = soup.find(class_='brd-body')
COLS = ['DocType', 'A/c Nature', 'A/c code', 'Description', 'Debit', 'Credit', 'Subdoctype', 'Subaccd']

wb = Workbook()
# ---- Sheet 1: entries for each scenario (section 3 of the scenario-wise BRD)
ws = wb.active; ws.title = 'Scenario entries'
ws['A1'] = 'Charges Waiver & Post-Pledge Drop-off – Accounting entries in UNO (fixed charges; Processing Fee for a sanction amount of ₹1,00,000)'; ws['A1'].font = Font(bold=True, size=13)
ws['A2'] = ('Posted when the customer pays the charges. Only the amount actually paid is posted; a waived amount is never posted. '
            'Approve (S 5.1 – S 5.3, S 6.1 – S 6.3): no entry at approval – LMS shows the charges (reduced by any waive-off); they are posted in UNO at the first withdrawal or repayment.')
ws['A2'].alignment = Alignment(wrap_text=True); ws.merge_cells('A2:H2'); ws.row_dimensions[2].height = 32
r = 4
sec = body.find('h2', string=re.compile(r'^3\. Scenarios'))
for el in sec.find_all_next(['h2', 'h3', 'h4', 'p', 'table']):
    if el.name == 'h2':
        break
    if el.name == 'h3':
        ws.cell(r, 1, txt(el)).font = BOLD
        for c in range(1, 9): ws.cell(r, c).fill = SCEN
        r += 1
    elif el.name == 'h4':
        ws.cell(r, 1, txt(el)).font = BOLD
        for c in range(1, 9): ws.cell(r, c).fill = SUB
        r += 1
    elif el.name == 'p' and txt(el).startswith('UNO entry: none'):
        ws.cell(r, 1, 'No accounting entry – nothing is received.').fill = NONE; r += 2
    elif el.name == 'table' and [txt(th) for th in el.find_all('th')] == COLS:
        header(ws, r, COLS); r += 1
        for tr in el.find('tbody').find_all('tr'):
            for c, td in enumerate(tr.find_all('td'), 1):
                v = txt(td); n = num(v) if c in (3, 5, 6) else None
                x = ws.cell(r, c, n if n is not None else (v or None)); x.border = BOX
                if c in (5, 6): x.number_format = '#,##0.00'
            r += 1
        r += 1   # DISC-460: no Total line under the entries
widths(ws, [12, 14, 10, 40, 12, 12, 12, 20]); ws.freeze_panes = 'A4'

# ---- Sheet 2: the owner's reference format and Sheet 3: account codes (section 4.3)
s43 = body.find('h2', string=re.compile(r'Accounting Entry'))   # section 5 (DISC-464)
tables = []
for el in s43.find_all_next(['h2', 'table']):
    if el.name == 'h2':
        break
    tables.append(el)
for name, t in (('Reference format', tables[0]), ('Account codes', tables[1])):
    w = wb.create_sheet(name)
    cols = [txt(th) for th in t.find_all('th')]
    header(w, 1, cols); rr = 2
    for tr in t.find('tbody').find_all('tr'):
        for c, td in enumerate(tr.find_all('td'), 1):
            v = txt(td); n = num(v) if cols[c - 1] in ('A/c code', 'Debit', 'Credit') else None
            x = w.cell(rr, c, n if n is not None else (v or None)); x.border = BOX
        rr += 1
    if name == 'Reference format':
        widths(w, [10, 14, 10, 40, 13, 12, 12, 12, 20])
    else:
        widths(w, [12, 42, 26])

# ---- Sheet 4: SOA example for an ACTIVE loan waiver (DISC-437) – from the S 7.3 tables
w = wb.create_sheet('SOA (ACTIVE)'); rr = 1
for t in body.find_all('table', class_='brd-soa'):
    w.cell(rr, 1, txt(t.find_previous('p'))).font = BOLD; rr += 1
    cols = [txt(th) for th in t.find_all('th')]; header(w, rr, cols); rr += 1
    for tr in t.find('tbody').find_all('tr'):
        for c, td in enumerate(tr.find_all('td'), 1):
            v = txt(td); n = num(v) if cols[c - 1] in ('Debit', 'Credit', 'Balance') else None
            x = w.cell(rr, c, n if n is not None else (v or None)); x.border = BOX
            if n is not None: x.number_format = '#,##0.00'
        rr += 1
    rr += 1
widths(w, [12, 46, 12, 12, 12, 8])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print('saved', os.path.normpath(OUT))
