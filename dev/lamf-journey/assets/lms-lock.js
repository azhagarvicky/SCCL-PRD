/* LMS lock (DISC-489, DISC-490): the LMS pages open only after the mail ID and the secret code are entered on lms-access.html (no hints shown).
   The code is not stored here – only a PBKDF2-SHA256 hash (300,000 rounds) of "mail:code". Client-side only: a front door, not real security.
   Protected pages load this script in <head> (assets/lms-lock.js); lms-access.html calls LMS_LOCK.check(mail, code). */
(function () {
  var SALT = '91b28d0e3c2628585d5b9e79ec1fec24', HASH = 'd3398603ad732271e823d0acc9fb687acf99b5eea68d222b6a740a6e24488b56', ROUNDS = 300000;
  var KEY = 'lms-unlock', TRIES = 'lms-unlock-tries', HOURS = 12;   // stays unlocked for 12 hours on this browser
  var me = document.currentScript, base = me ? me.src.replace(/assets\/lms-lock\.js.*$/, '') : '';
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch (e) {} }
  function open_() { var t = +get(KEY) || 0; return t > Date.now(); }
  function hex(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ('0' + b.toString(16)).slice(-2); }).join(''); }
  window.LMS_LOCK = {
    isOpen: open_,
    lock: function () { put(KEY, null); },
    blockedFor: function () { var t = JSON.parse(get(TRIES) || '{"n":0,"until":0}'); return Math.max(0, t.until - Date.now()); },
    check: function (mail, code) {
      var t = JSON.parse(get(TRIES) || '{"n":0,"until":0}');
      if (t.until > Date.now()) return Promise.resolve({ ok: false, blocked: t.until - Date.now() });
      var enc = new TextEncoder();
      return crypto.subtle.importKey('raw', enc.encode(String(mail).trim().toLowerCase() + ':' + String(code).trim()), 'PBKDF2', false, ['deriveBits'])
        .then(function (k) { return crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt: enc.encode(SALT), iterations: ROUNDS }, k, 256); })
        .then(function (bits) {
          if (hex(bits) === HASH) { put(KEY, String(Date.now() + HOURS * 3600e3)); put(TRIES, null); return { ok: true }; }
          t.n += 1; if (t.n >= 5) { t.until = Date.now() + 5 * 60e3; t.n = 0; }   // 5 wrong tries → wait 5 minutes
          put(TRIES, JSON.stringify(t));
          return { ok: false, left: t.until > Date.now() ? 0 : 5 - t.n, blocked: t.until > Date.now() ? t.until - Date.now() : 0 };
        });
    }
  };
  if (me && me.getAttribute('data-gate') === 'off') return;   // the lock page itself
  if (!open_()) {
    document.documentElement.style.visibility = 'hidden';
    location.replace(base + 'lms-access.html?next=' + encodeURIComponent(location.href));
  }
})();
