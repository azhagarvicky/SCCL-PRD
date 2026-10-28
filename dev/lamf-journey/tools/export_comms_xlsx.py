# Writes exports/LAMF_Customer_Communications.xlsx from COMMS in build_pages.py (DISC-197).
# Run after changing COMMS:  python3 lamf-journey/tools/export_comms_xlsx.py   (needs openpyxl)
import os, re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(HERE, 'build_pages.py')).read()
ns = {}
exec(src[src.index('COMMS = ['):src.index('CONTACT = (')], ns)      # only the COMMS / COMMS_COLS data
COMMS, COLS = ns['COMMS'], ns['COMMS_COLS']
MAILS, MAIL_COLS = ns['MAILS'], ns['MAIL_COLS']        # Mail sheet (DISC-199)

wb = Workbook()
thin = Side(style='thin', color='000000'); bd = Border(left=thin, right=thin, top=thin, bottom=thin)

def sheet(ws, COMMS, COLS, widths):
  ws.append(COLS)
  for c in ws[1]:
      c.font = Font(name='Calibri', size=11, bold=True); c.fill = PatternFill('solid', fgColor='B4C6E7')
      c.border = bd; c.alignment = Alignment(vertical='center', wrap_text=True)
  for k, r in enumerate(COMMS, 1):
      ws.append([k] + [re.sub(r'</?u>', '', v) for v in r])
      av = COLS.index('Available')                      # column number of Available (S.No is column 1)
      na = r[av - 1].startswith('No')
      st = COLS.index('Status') if 'Status' in COLS else None   # column number of Status
      nr = st is not None and r[st - 1] == 'Not Required'       # DISC-201: kept, shown greyed
      for c in ws[ws.max_row]:
          is_av, is_st = c.column == av, c.column == st
          color = ('B42318' if (is_av and na) or (is_st and nr) else '12753B' if is_st else '8A8A8A' if nr else '000000')
          c.font = Font(name='Calibri', size=11, bold=(is_av and na) or is_st, color=color)
          c.border = bd; c.alignment = Alignment(vertical='top', wrap_text=True, horizontal='center' if c.column == 1 else None)
          if nr: c.fill = PatternFill('solid', fgColor='EDEDED')
          elif na: c.fill = PatternFill('solid', fgColor='FFF2CC')
  for i, w in enumerate(widths, 1):
      ws.column_dimensions[chr(64 + i)].width = w
  ws.freeze_panes = 'C2'; ws.auto_filter.ref = f'A1:{chr(64 + len(COLS))}{ws.max_row}'
  n = ws.max_row + 2
  ws.cell(n, 1, 'Notes:').font = Font(name='Calibri', bold=True)
  for j, t in enumerate([
          'Rows highlighted in yellow (Available = "No – to be created") are templates drafted for approval; they still have to be created and registered.',
          'Rows in grey (Status = "Not Required") are kept for reference only; they will not be sent.',
          'Actual Content shows a sample with the variables filled in (sample customer AZHAGARSAMY, loan account SCCLMF20261000102).',
          'Source: LAMF – Customer Communications page (https://azhagarvicky.github.io/SCCL-PRD/dev/lamf-journey/communications.html).',
          'Created by Azhagarsamy Subburaj. For any observation or clarification, please reach out to azhagarsamy.s@shriramcredit.in'], 1):
      ws.cell(n + j, 1, t).font = Font(name='Calibri', size=10, italic=True)
  ws.page_setup.orientation = 'landscape'; ws.sheet_properties.pageSetUpPr.fitToPage = True
  ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0

ws = wb.active; ws.title = 'SMS'
sheet(ws, COMMS, COLS, [6, 28, 45, 12, 14, 9, 55, 55, 12, 12, 18, 14, 16, 40, 80])
sheet(wb.create_sheet('Mail'), MAILS, MAIL_COLS, [6, 28, 40, 12, 14, 9, 80, 80, 40, 10, 12])
out = os.path.join(REPO, 'exports', 'LAMF_Customer_Communications.xlsx')
os.makedirs(os.path.dirname(out), exist_ok=True); wb.save(out)
print(len(COMMS), 'SMS and', len(MAILS), 'mails written to', out)
