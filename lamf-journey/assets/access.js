/* LAMF site – module-wise access (DISC-528). Source file.
   Every module page loads this file with its module: <script src="assets/access.js" data-m="prd"></script>.
   The user signs in once on access.html with their mail ID + secret code; the Apps Script web app checks the Google Sheet
   "LAMF Site Access" → tab "Module Access" (one row per user, Y / N per module) and returns the modules that user may open.
   The answer is kept for this browser tab only (sessionStorage) and checked again with the sheet every 5 minutes, so a change in
   the sheet (module removed, Active = N) takes effect at once. Secret codes stay in the private sheet – never in this site.
   Note: this hides the pages from people who are not on the list; it is not a replacement for real server security. */
(function () {
  var ON = true;   // DISC-528/529: on – the owner deployed the new Apps Script version on 28-11-2026
  var ENDPOINT = 'https://script.google.com/macros/s/AKfycbxrag9tuAwoD111KNMX07yNhgxjkJriKNlGw_2TeBkGLzdIxQ3K_z_2X9QxwBQKBIYG/exec';
  var KEY = 'lamf-access', RECHECK = 5 * 60 * 1000;
  var NAMES = { prd: 'PRD document', brd: 'BRD documents', journey: 'LOS', comms: 'Communications', calc: 'Calculator', lms: 'LMS' };
  var me = document.currentScript, mod = me && me.getAttribute('data-m');
  var base = me ? me.src.replace(/assets\/access\.js.*$/, '') : '';   // site folder (…/lamf-journey/), works from sub-folders too
  function get() { try { var s = JSON.parse(sessionStorage.getItem(KEY)); return s && s.exp > Date.now() ? s : null; } catch (e) { return null; } }
  function put(s) { try { sessionStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }
  function clear() { try { sessionStorage.removeItem(KEY); } catch (e) {} }
  function call(body) {   // text/plain avoids the CORS pre-flight that Apps Script cannot answer
    return fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json(); });
  }
  function allowed(m, s) { s = s || get(); return !ON || !m || !!(s && s.mods && s.mods.indexOf(m) >= 0); }
  function go(m) { location.replace(base + 'access.html?m=' + encodeURIComponent(m) + '&next=' + encodeURIComponent(location.href)); }
  window.LAMF_ACCESS = {
    on: ON, names: NAMES, base: base, get: get, allowed: allowed, clear: clear,
    login: function (mail, code) {
      return call({ action: 'mlogin', mail: mail, code: code }).then(function (r) {
        if (r.ok) put({ token: r.token, mail: r.mail, name: r.name, mods: r.mods, exp: r.expires, t: Date.now() });
        return r;
      });
    },
    logout: function () { var s = get(); clear(); if (s) call({ action: 'logout', token: s.token }).catch(function () {}); },
    guard: function (m) { if (!allowed(m)) { go(m); return false; } return true; }   // for pages that change module without reloading (cloud.html)
  };
  if (!ON || !mod) return;
  var s = get();
  if (!allowed(mod, s)) { document.documentElement.style.visibility = 'hidden'; go(mod); return; }
  if (Date.now() - (s.t || 0) > RECHECK) {   // recheck with the sheet in the background
    call({ action: 'mcheck', token: s.token }).then(function (r) {
      if (!r.ok) { clear(); go(mod); return; }
      s.mods = r.mods; s.name = r.name; s.t = Date.now(); put(s);
      if (s.mods.indexOf(mod) < 0) go(mod);
    }).catch(function () {});
  }
})();
