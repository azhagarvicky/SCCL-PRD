/**
 * LAMF site – access control (Google Apps Script, DISC-477).
 * SCCL mail ID → OTP by mail → admin approval. Used by assets/gate.js (login on the protected pages) and admin.html (admin portal).
 *
 * Setup (one time):
 *   1. Create a Google Sheet named "LAMF Site Access" (any tab name – the script creates Users, Sessions and Log).
 *   2. Extensions → Apps Script, replace everything with this file, Save.
 *   3. Run the function "setup" once (▶ Run) and allow the permissions (Sheets, send mail).
 *   4. Deploy → New deployment → type "Web app":  Execute as: Me  ·  Who has access: Anyone  → Deploy.
 *   5. Copy the Web app URL (ends in /exec) and give it to Claude.
 * After changing this script: Deploy → Manage deployments → edit → Version: New version (the URL stays the same).
 *
 * The OTP is never stored – only a SHA-256 hash with a secret salt, in the script cache for 10 minutes.
 * A login key (token) is given after the OTP is verified; only its hash is stored in Sessions, valid for 30 days.
 */
const ADMIN = 'azhagarsamy.s@shriramcredit.in';
const DOMAIN = '@shriramcredit.in';
const DAYS = 30;                 // login valid for 30 days
const OTP_MIN = 10;              // OTP valid for 10 minutes
const OTP_TRIES = 3;             // wrong attempts per OTP
const OTP_PER_HOUR = 5;          // OTPs per mail ID per hour
const SITE = 'https://azhagarvicky.github.io/SCCL-PRD/dev/lamf-journey/';
const USERS = ['Mail ID', 'Name', 'Requested on', 'Status', 'Approved by', 'Approved on', 'Last login'];
const SESS = ['Token hash', 'Mail ID', 'Created on', 'Expires on'];
const LOG = ['Date & time', 'Mail ID', 'Event', 'Detail'];

function setup() {
  tab_('Users', USERS); tab_('Sessions', SESS); tab_('Log', LOG); salt_();
  const u = tab_('Users', USERS);
  if (!find_(u, ADMIN)) u.appendRow([ADMIN, 'Admin', now_(), 'Approved', 'Setup', now_(), '']);
}

// ---- helpers ------------------------------------------------------------------------------------------------------------
function tab_(name, head) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  if (sh.getLastRow() === 0) {
    sh.appendRow(head); sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, head.length).setFontWeight('bold').setBackground('#FFCB08');
  }
  return sh;
}
function now_() { return Utilities.formatDate(new Date(), 'Asia/Kolkata', 'dd-MM-yyyy HH:mm'); }
function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function salt_() {
  const p = PropertiesService.getScriptProperties();
  let s = p.getProperty('SALT');
  if (!s) { s = Utilities.getUuid() + Utilities.getUuid(); p.setProperty('SALT', s); }
  return s;
}
function hash_(v) {
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, salt_() + '|' + v)
    .map(function (b) { return ('0' + (b & 255).toString(16)).slice(-2); }).join('');
}
function clean_(v, max) {   // plain text only – a leading = + - @ is escaped so nothing runs as a formula
  const s = String(v == null ? '' : v).slice(0, max).trim();
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}
function mail_(v) { return String(v || '').trim().toLowerCase(); }
function valid_(m) { return /^[a-z0-9._%+-]+@shriramcredit\.in$/.test(m); }
function find_(sh, m) {     // row number (1-based) of a mail ID in column A, or 0
  const v = sh.getRange(1, 1, sh.getLastRow(), 1).getValues();
  for (let i = 1; i < v.length; i++) if (String(v[i][0]).toLowerCase() === m) return i + 1;
  return 0;
}
function log_(m, ev, d) { tab_('Log', LOG).appendRow([now_(), m, ev, clean_(d, 300)]); }
function user_(m) {
  const sh = tab_('Users', USERS), r = find_(sh, m);
  if (!r) return null;
  const v = sh.getRange(r, 1, 1, USERS.length).getValues()[0];
  return { row: r, mail: m, name: v[1], status: m === ADMIN ? 'Approved' : String(v[3] || 'Pending') };
}
function session_(token) {   // → mail ID of a valid login key, or ''
  if (!token || String(token).length < 30) return '';
  const sh = tab_('Sessions', SESS), h = hash_('t:' + token), last = sh.getLastRow();
  if (last < 2) return '';
  const v = sh.getRange(2, 1, last - 1, 4).getValues();
  for (let i = 0; i < v.length; i++) {
    if (v[i][0] === h) return (Number(v[i][3]) > Date.now()) ? String(v[i][1]) : '';
  }
  return '';
}

// ---- web app ------------------------------------------------------------------------------------------------------------
function doGet() { return out_({ ok: true, service: 'LAMF site access' }); }

function doPost(e) {
  const lock = LockService.getScriptLock(); lock.waitLock(20000);
  try {
    const q = JSON.parse(e.postData.contents || '{}');
    const a = q.action;
    if (a === 'send') return out_(send_(q));
    if (a === 'verify') return out_(verify_(q));
    if (a === 'check') return out_(check_(q));
    if (a === 'logout') return out_(logout_(q));
    if (a === 'list') return out_(list_(q));
    if (a === 'set') return out_(set_(q));
    return out_({ ok: false, error: 'Unknown action' });
  } catch (err) {
    return out_({ ok: false, error: 'Something went wrong. Please try again.' });
  } finally { lock.releaseLock(); }
}

function send_(q) {
  const m = mail_(q.mail);
  if (!valid_(m)) return { ok: false, error: 'Only SCCL mail IDs (@shriramcredit.in) are allowed.' };
  const c = CacheService.getScriptCache(), rk = 'rate:' + m, n = Number(c.get(rk) || 0);
  if (n >= OTP_PER_HOUR) return { ok: false, error: 'Too many OTP requests. Please try again after an hour.' };
  c.put(rk, String(n + 1), 3600);
  const otp = String(Math.floor(100000 + Math.random() * 900000));
  c.put('otp:' + m, JSON.stringify({ h: hash_('o:' + m + ':' + otp), tries: 0, name: clean_(q.name, 80) }), OTP_MIN * 60);
  MailApp.sendEmail({
    to: m, name: 'LAMF Prototype',
    subject: 'Your LAMF site OTP – ' + otp,
    htmlBody: '<p>Dear User,</p><p>Your OTP to open the LAMF prototype site is <b style="font-size:18px">' + otp + '</b>.</p>' +
      '<p>It is valid for ' + OTP_MIN + ' minutes. Do not share it with anyone.</p><p>If you did not ask for it, please ignore this mail.</p>' +
      '<p>Regards,<br>LAMF Prototype</p>'
  });
  log_(m, 'OTP sent', '');
  return { ok: true, minutes: OTP_MIN };
}

function verify_(q) {
  const m = mail_(q.mail), otp = String(q.otp || '').replace(/\D/g, '');
  const c = CacheService.getScriptCache(), k = 'otp:' + m, raw = c.get(k);
  if (!valid_(m) || !raw) return { ok: false, error: 'The OTP has expired. Please click Resend OTP.' };
  const s = JSON.parse(raw);
  if (s.h !== hash_('o:' + m + ':' + otp)) {
    s.tries += 1;
    log_(m, 'OTP failed', 'attempt ' + s.tries);
    if (s.tries >= OTP_TRIES) { c.remove(k); return { ok: false, error: 'Incorrect OTP entered 3 times. Please click Resend OTP.' }; }
    c.put(k, JSON.stringify(s), OTP_MIN * 60);
    return { ok: false, error: 'Incorrect OTP. ' + (OTP_TRIES - s.tries) + ' attempt(s) left.' };
  }
  c.remove(k);
  const us = tab_('Users', USERS);
  let u = user_(m);
  if (!u) {      // first verification – a new request, Pending until the admin approves
    us.appendRow([m, s.name || '', now_(), 'Pending', '', '', '']);
    u = user_(m);
    MailApp.sendEmail({
      to: ADMIN, name: 'LAMF Prototype', subject: 'New access request – ' + m,
      htmlBody: '<p>New request to open the LAMF prototype site.</p><p><b>Name:</b> ' + (s.name || '-') + '<br><b>Mail ID:</b> ' + m +
        '<br><b>Requested on:</b> ' + now_() + '</p><p><a href="' + SITE + 'admin.html">Open the admin portal</a> to approve or reject.</p>'
    });
    log_(m, 'Access requested', s.name || '');
  } else if (u.status === 'Removed') {   // a removed user can ask again – back to Pending
    us.getRange(u.row, 4, 1, 3).setValues([['Pending', '', '']]); u.status = 'Pending';
    MailApp.sendEmail({ to: ADMIN, name: 'LAMF Prototype', subject: 'Access requested again – ' + m,
      htmlBody: '<p>' + m + ' asked again to open the LAMF prototype site.</p><p><a href="' + SITE + 'admin.html">Open the admin portal</a>.</p>' });
    log_(m, 'Access requested again', '');
  }
  const token = Utilities.getUuid() + Utilities.getUuid();
  const exp = Date.now() + DAYS * 864e5;
  tab_('Sessions', SESS).appendRow([hash_('t:' + token), m, now_(), exp]);
  log_(m, 'OTP verified', u.status);
  return { ok: true, token: token, expires: exp, status: u.status, mail: m, admin: m === ADMIN };
}

function check_(q) {
  const m = session_(q.token);
  if (!m) return { ok: false, status: 'LoggedOut' };
  const u = user_(m);
  if (!u) return { ok: false, status: 'LoggedOut' };
  if (u.status === 'Approved') {
    const sh = tab_('Users', USERS), cell = sh.getRange(u.row, 7), t = now_();
    if (String(cell.getDisplayValue()).slice(0, 10) !== t.slice(0, 10)) cell.setValue(t);   // last login, once a day
  }
  return { ok: true, status: u.status, mail: m, name: u.name, admin: m === ADMIN };
}

function logout_(q) {
  const sh = tab_('Sessions', SESS), h = hash_('t:' + q.token), last = sh.getLastRow();
  if (last >= 2) {
    const v = sh.getRange(2, 1, last - 1, 1).getValues();
    for (let i = v.length - 1; i >= 0; i--) if (v[i][0] === h) sh.deleteRow(i + 2);
  }
  return { ok: true };
}

function list_(q) {
  if (session_(q.token) !== ADMIN) return { ok: false, error: 'Not an admin.' };
  const sh = tab_('Users', USERS), last = sh.getLastRow();
  const rows = last < 2 ? [] : sh.getRange(2, 1, last - 1, USERS.length).getDisplayValues().map(function (v) {
    return { mail: v[0], name: v[1], requested: v[2], status: v[3], by: v[4], on: v[5], last: v[6] };
  });
  return { ok: true, users: rows };
}

function set_(q) {
  if (session_(q.token) !== ADMIN) return { ok: false, error: 'Not an admin.' };
  const m = mail_(q.mail), st = String(q.status);
  if (['Approved', 'Rejected', 'Removed'].indexOf(st) < 0 || m === ADMIN) return { ok: false, error: 'Not allowed.' };
  const u = user_(m);
  if (!u) return { ok: false, error: 'User not found.' };
  const sh = tab_('Users', USERS);
  sh.getRange(u.row, 4, 1, 3).setValues([[st, ADMIN, now_()]]);
  if (st !== 'Approved') {   // take access back at once – end every login of this user
    const ss = tab_('Sessions', SESS), last = ss.getLastRow();
    if (last >= 2) {
      const v = ss.getRange(2, 2, last - 1, 1).getValues();
      for (let i = v.length - 1; i >= 0; i--) if (String(v[i][0]).toLowerCase() === m) ss.deleteRow(i + 2);
    }
  }
  if (st !== 'Removed') {
    MailApp.sendEmail({
      to: m, name: 'LAMF Prototype',
      subject: st === 'Approved' ? 'Access approved – LAMF prototype site' : 'Access request – LAMF prototype site',
      htmlBody: st === 'Approved'
        ? '<p>Dear User,</p><p>Your access to the LAMF prototype site is approved. <a href="' + SITE + 'brd.html">Open the site</a>.</p><p>Regards,<br>LAMF Prototype</p>'
        : '<p>Dear User,</p><p>Your request to open the LAMF prototype site is not approved.</p><p>Regards,<br>LAMF Prototype</p>'
    });
  }
  log_(m, 'Status ' + st, 'by ' + ADMIN);
  return { ok: true };
}
