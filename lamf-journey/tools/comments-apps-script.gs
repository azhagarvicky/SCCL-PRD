/**
 * LAMF prototype – review comments receiver (Google Apps Script, DISC-028).
 *
 * Paste this into the comments Google Sheet: Extensions → Apps Script, replace everything,
 * Save, then Deploy → New deployment → type "Web app":
 *   Execute as: Me    ·    Who has access: Anyone
 * Copy the Web app URL (ends in /exec) and give it to Claude.
 *
 * The prototype pages send new comments here (POST) and read the list back (GET).
 * Open / Closed status is maintained by Claude in comment-status.json in the GitHub repo;
 * this script copies it into the Status / Closed on / What was done columns.
 */
const SHEET = 'Comments';
const STATUS_URL = 'https://raw.githubusercontent.com/azhagarvicky/SCCL-PRD/dev/comment-status.json';
const HEAD = ['ID', 'Created on', 'Site', 'Page', 'Selected text', 'Comment', 'Name', 'Status', 'Closed on', 'What was done', 'Page link'];
const LIMIT = { page: 200, quote: 1000, comment: 3000, name: 80, site: 20, link: 500 };

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET);
  if (!sh) { sh = ss.getSheets()[0]; sh.setName(SHEET); }   // first tab becomes "Comments"
  if (sh.getLastRow() === 0) sh.appendRow(HEAD);
  if (sh.getFrozenRows() !== 1) {
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, HEAD.length).setFontWeight('bold').setBackground('#FFCB08');
  }
  return sh;
}

// Text is stored as plain text: a leading = + - @ is escaped so nothing runs as a formula.
function clean_(v, max) {
  const s = String(v == null ? '' : v).slice(0, max).trim();
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function now_() {
  return Utilities.formatDate(new Date(), 'Asia/Kolkata', 'dd-MM-yyyy HH:mm');
}

function doPost(e) {
  let d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return out_({ ok: false, error: 'Bad request' }); }
  if (d.website) return out_({ ok: true });                 // spam trap: real users never fill this
  const comment = clean_(d.comment, LIMIT.comment), name = clean_(d.name, LIMIT.name);
  if (!comment || !name) return out_({ ok: false, error: 'Name and comment are required' });
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sh = sheet_();
    const id = 'C-' + String(sh.getLastRow()).padStart(4, '0');   // row 2 → C-0001
    sh.appendRow([id, now_(), clean_(d.site, LIMIT.site), clean_(d.page, LIMIT.page), clean_(d.quote, LIMIT.quote),
                  comment, name, 'Open', '', '', clean_(d.link, LIMIT.link)]);
    return out_({ ok: true, id: id });
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  const sh = sheet_();
  syncStatus_(sh);
  const values = sh.getDataRange().getDisplayValues();
  const rows = values.slice(1).filter((r) => r[0]).map((r) => ({
    id: r[0], created: r[1], site: r[2], page: r[3], quote: r[4], comment: r[5], name: r[6],
    status: r[7] || 'Open', closed: r[8], note: r[9],
  }));
  return out_({ ok: true, rows: rows });
}

// Copy Claude's Open / Closed updates from the repository into the sheet (checked at most once a minute).
function syncStatus_(sh) {
  const cache = CacheService.getScriptCache();
  if (cache.get('synced')) return;
  cache.put('synced', '1', 60);
  let status;
  try {
    const res = UrlFetchApp.fetch(STATUS_URL + '?t=' + Date.now(), { muteHttpExceptions: true });
    if (res.getResponseCode() !== 200) return;
    status = JSON.parse(res.getContentText());
  } catch (err) { return; }
  const n = sh.getLastRow() - 1;
  if (n < 1) return;
  const ids = sh.getRange(2, 1, n, 1).getValues();
  const cur = sh.getRange(2, 8, n, 3).getValues();           // Status, Closed on, What was done
  let changed = false;
  ids.forEach((r, i) => {
    const s = status[r[0]];
    if (!s) return;
    const next = [s.status || 'Open', s.closed || '', s.note || ''];
    if (next.join('|') !== cur[i].join('|')) { cur[i] = next; changed = true; }
  });
  if (changed) sh.getRange(2, 8, n, 3).setValues(cur);
}
