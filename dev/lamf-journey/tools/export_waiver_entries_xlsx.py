# Waiver BRD accounting entries (UNO) → Excel (DISC-397). Reads the generated brd-waive-off.html so the sheet always matches the BRD.
# Run after build_pages.py:  python3 lamf-journey/tools/export_waiver_entries_xlsx.py
import os, re
from bs4 import BeautifulSoup, Tag
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(ROOT, 'brd-waive-off.html')
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
COLS = ['DocType', 'A/c Nature', 'A/c code', 'Description', 'Doc. Dt', 'Debit', 'Credit', 'Subdoctype', 'Subaccd']

wb = Workbook()
# ---- Sheet 1: entries for each scenario
ws = wb.active; ws.title = 'Scenario entries'
ws['A1'] = 'Charges Waiver & Post-Pledge Drop-off – Accounting entries in UNO (sample amounts)'; ws['A1'].font = Font(bold=True, size=13)
ws['A2'] = ('Posted when the customer pays the charges. Only the amount actually paid is posted; a waived amount is never posted. '
            'Approve (S 5.1 – S 5.3, S 6.1 – S 6.3): no entry at approval – the charges are deducted from the first disbursement and posted then.')
ws['A2'].alignment = Alignment(wrap_text=True); ws.merge_cells('A2:I2'); ws.row_dimensions[2].height = 32
r = 4; scen = None
sec = body.find('h3', string=re.compile(r'Scenario details'))
for el in sec.find_all_next(['h4', 'p', 'table']):
    if el.name == 'h3' or (el.name == 'h4' and not txt(el).startswith('S ')):
        break
    if el.name == 'h4':
        scen = txt(el); ws.cell(r, 1, scen).font = BOLD
        for c in range(1, 10): ws.cell(r, c).fill = SCEN
        r += 1
    elif el.name == 'p' and el.find('b') and re.match(r'S \d\.\d', txt(el.find('b'))):
        title = txt(el)
        ws.cell(r, 1, title).font = BOLD
        for c in range(1, 10): ws.cell(r, c).fill = NONE if 'no accounting entry' in title else SUB
        r += 1
        if 'no accounting entry' in title:
            r += 1
    elif el.name == 'table' and [txt(th) for th in el.find_all('th')] == COLS:
        header(ws, r, COLS); r += 1; first = r
        for tr in el.find('tbody').find_all('tr'):
            for c, td in enumerate(tr.find_all('td'), 1):
                v = txt(td); n = num(v) if c in (3, 6, 7) else None
                x = ws.cell(r, c, n if n is not None else (v or None)); x.border = BOX
                if c in (6, 7): x.number_format = '#,##0.00'
            r += 1
        ws.cell(r, 5, 'Total').font = BOLD
        for c in (6, 7):
            L = get_column_letter(c); x = ws.cell(r, c, f'=SUM({L}{first}:{L}{r - 1})'); x.font = BOLD; x.number_format = '#,##0.00'
        ws.cell(r, 8, f'=IF(ROUND(F{r}-G{r},2)=0,"Balanced","Check")').font = BOLD
        for c in range(5, 10): ws.cell(r, c).fill = TOT; ws.cell(r, c).border = BOX
        r += 2
widths(ws, [10, 14, 10, 40, 13, 12, 12, 12, 20]); ws.freeze_panes = 'A4'

# ---- Sheet 2: the owner's reference format and Sheet 3: account codes (section 4.3)
s43 = body.find('h3', string=re.compile(r'Accounting entries'))
tables = []
for el in s43.find_all_next(['h3', 'table']):
    if el.name == 'h3':
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
        w.cell(rr, 5, 'Total').font = BOLD
        for c in (6, 7):
            L = get_column_letter(c); w.cell(rr, c, f'=SUM({L}2:{L}{rr - 1})').font = BOLD
        w.cell(rr, 8, f'=IF(ROUND(F{rr}-G{rr},2)=0,"Balanced","Check")').font = BOLD
        widths(w, [10, 14, 10, 40, 13, 12, 12, 12, 20])
    else:
        widths(w, [12, 42, 26])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print('saved', os.path.normpath(OUT))
