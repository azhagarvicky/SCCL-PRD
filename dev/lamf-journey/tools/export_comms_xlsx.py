# Writes exports/LAMF_Customer_Communications.xlsx from COMMS in build_pages.py (DISC-197).
# Run after changing COMMS:  python3 lamf-journey/tools/export_comms_xlsx.py   (needs openpyxl)
import os, re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://azhagarvicky.github.io/SCCL-PRD/dev/lamf-journey/'
REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(HERE, 'build_pages.py')).read()
import html
ns = {'os': os, 're': re, 'html': html, 'ROOT': os.path.dirname(HERE)}   # what the COMMS block uses
exec(src[src.index('COMMS = ['):src.index('CONTACT = (')], ns)      # only the COMMS / COMMS_COLS data
COMMS, COLS = ns['COMMS'], ns['COMMS_COLS']

wb = Workbook()
thin = Side(style='thin', color='000000'); bd = Border(left=thin, right=thin, top=thin, bottom=thin)

def sheet(ws, COMMS, COLS, widths):
  ws.append(COLS)
  for c in ws[1]:
      c.font = Font(name='Calibri', size=11, bold=True); c.fill = PatternFill('solid', fgColor='B4C6E7')
      c.border = bd; c.alignment = Alignment(vertical='center', wrap_text=True)
  for k, r in enumerate(COMMS, 1):
      ws.append([k] + [re.sub(r'\s*\[\[view:[^\]]+\]\]', '\nView mail', re.sub(r'</?u>', '', v)) for v in r])
      for col, v in enumerate(r, 2):                     # “View mail” opens the mail template on the dev site (DISC-207)
          m = re.search(r'\[\[view:([^\]]+)\]\]', v)
          if m:
              cell = ws.cell(ws.max_row, col); cell.hyperlink = SITE + m.group(1)
      av = COLS.index('SMS Available' if 'SMS Available' in COLS else 'Available')   # column number (S.No is column 1)
      na = r[av - 1].startswith('No')
      st = COLS.index('SMS Status') if 'SMS Status' in COLS else None   # column number of SMS Status
      nr = st is not None and r[st - 1] == 'Not Required'       # DISC-201: kept, shown greyed
      for c in ws[ws.max_row]:
          is_av, is_st = c.column == av, c.column == st or COLS[c.column - 1] == 'Mail Status'
          color = ('B42318' if (is_av and na) or (c.column == st and nr) else '12753B' if is_st and c.value else '8A8A8A' if nr else '000000')
          c.font = Font(name='Calibri', size=11, bold=(is_av and na) or is_st, color=color)
          c.border = bd; c.alignment = Alignment(vertical='top', wrap_text=True, horizontal='center' if c.column == 1 else None)
          if nr: c.fill = PatternFill('solid', fgColor='EDEDED')
          elif na: c.fill = PatternFill('solid', fgColor='FFF2CC')
  for i, w in enumerate(widths, 1):
      ws.column_dimensions[chr(64 + i)].width = w
  ws.freeze_panes = 'C2'; ws.auto_filter.ref = f'A1:{chr(64 + len(COLS))}{ws.max_row}'
  n = ws.max_row + 2
  ws.cell(n, 1, 'Notes:').font = Font(name='Calibri', bold=True)
  for j, t in enumerate(['Summary – ' + ' · '.join(f'{k}: {v}' + (f' ({d})' if d else '') for k, v, d in ns['COMMS_SUMMARY']),

          'Rows highlighted in yellow (Available = "No – to be created") are templates drafted for approval; they still have to be created and registered.',
          'Rows with SMS Status = "Not Required" are in the separate "Not Required" sheet – kept for reference only; they will not be sent.',
          'Actual Content shows a sample with the variables filled in (sample customer AZHAGARSAMY, loan account SCCLMF20261000102).',
          'Source: LAMF – Customer Communications page (https://azhagarvicky.github.io/SCCL-PRD/dev/lamf-journey/communications.html).',
          'Created by Azhagarsamy Subburaj. For any observation or clarification, please reach out to azhagarsamy.s@shriramcredit.in'], 1):
      ws.cell(n + j, 1, t).font = Font(name='Calibri', size=10, italic=True)
  ws.page_setup.orientation = 'landscape'; ws.sheet_properties.pageSetUpPr.fitToPage = True
  ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0

ws = wb.active; ws.title = 'SMS and Mail'      # single sheet; the Mail sheet was removed (DISC-240)
W = [6, 28, 45, 12, 9, 14, 55, 55, 12, 18, 14, 40, 40, 70, 70, 14, 12, 45]
sheet(ws, COMMS, COLS, W)
sheet(wb.create_sheet('Not Required'), ns['COMMS_NR'], COLS, W)          # DISC-243
out = os.path.join(REPO, 'exports', 'LAMF_Customer_Communications.xlsx')
os.makedirs(os.path.dirname(out), exist_ok=True); wb.save(out)
print(len(COMMS), 'communications +', len(ns['COMMS_NR']), 'not required written to', out)
