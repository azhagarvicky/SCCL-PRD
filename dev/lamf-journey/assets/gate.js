/* LAMF site – access gate (DISC-477): SCCL mail ID → OTP → admin approval. Backend: tools/access-apps-script.gs (Google Apps Script).
   Load it in <head> of a protected page: <script src="assets/gate.js"></script>. The page stays hidden until the login key is checked.
   admin.html loads it with data-admin="1" and gets window.LAMF_GATE.onAdmin(token) after an admin login. */
(function () {
  var ENDPOINT = 'https://script.google.com/macros/s/AKfycbxrag9tuAwoD111KNMX07yNhgxjkJriKNlGw_2TeBkGLzdIxQ3K_z_2X9QxwBQKBIYG/exec';   // Google Apps Script web app URL (…/exec). Empty = not connected yet: the page is not blocked.
  var me = document.currentScript, isAdmin = me && me.getAttribute('data-admin') === '1';
  var KEY = isAdmin ? 'lamf-gate-admin' : 'lamf-gate-token', OK = 'lamf-gate-ok', RECHECK = 10 * 60 * 1000;   // admin login kept apart; re-check every 10 minutes
  var api = window.LAMF_GATE = { endpoint: ENDPOINT, call: call, token: get, logout: logout };
  if (!ENDPOINT) { if (isAdmin) document.addEventListener('DOMContentLoaded', function () { notReady(); }); return; }

  function get() { try { return localStorage.getItem(KEY) || ''; } catch (e) { return ''; } }
  function put(t) { try { t ? localStorage.setItem(KEY, t) : localStorage.removeItem(KEY); } catch (e) {} }
  function okAt(v) { try { if (v === undefined) return +sessionStorage.getItem(OK) || 0; v ? sessionStorage.setItem(OK, String(v)) : sessionStorage.removeItem(OK); } catch (e) { return 0; } }
  function call(body) {   // text/plain POST – no pre-flight, works with the Apps Script web app
    return fetch(ENDPOINT, { method: 'POST', body: JSON.stringify(body), redirect: 'follow' }).then(function (r) { return r.json(); });
  }
  function logout() { var t = get(); put(''); okAt(0); if (t) call({ action: 'logout', token: t }).catch(function () {}); location.reload(); }

  // hide the page until the check is done
  var css = document.createElement('style');
  css.textContent =
    'html.gate-lock body>*:not(#lamf-gate){display:none!important}' +
    '#lamf-gate{position:fixed;inset:0;z-index:2147483000;background:#f4f4f2;display:flex;align-items:center;justify-content:center;padding:16px;font-family:"Segoe UI",Arial,Helvetica,sans-serif;color:#1a1a1a}' +
    '#lamf-gate .g-box{width:400px;max-width:100%;background:#fff;border-radius:12px;box-shadow:0 4px 24px rgba(0,0,0,.12);overflow:hidden}' +
    '#lamf-gate .g-head{background:#1a1a1a;color:#FFC20E;padding:18px 24px;font-weight:700;font-size:18px}' +
    '#lamf-gate .g-head small{display:block;color:#ddd;font-weight:400;font-size:13px;margin-top:4px}' +
    '#lamf-gate .g-body{padding:22px 24px 24px}' +
    '#lamf-gate label{display:block;font-size:13px;font-weight:600;margin:12px 0 6px}' +
    '#lamf-gate input{width:100%;box-sizing:border-box;font:inherit;font-size:15px;padding:10px 12px;border:1px solid #bbb;border-radius:8px}' +
    '#lamf-gate input:focus{outline:2px solid #FFC20E;border-color:#1a1a1a}' +
    '#lamf-gate button{font:inherit;font-weight:600;font-size:15px;border:0;border-radius:8px;padding:11px 16px;cursor:pointer;background:#FFC20E;color:#1a1a1a;width:100%;margin-top:16px}' +
    '#lamf-gate button[disabled]{opacity:.55;cursor:default}' +
    '#lamf-gate .g-link{background:none;color:#1a1a1a;text-decoration:underline;width:auto;padding:0;margin-top:12px;font-weight:400;font-size:13px}' +
    '#lamf-gate .g-err{color:#b91c1c;font-size:13px;margin:8px 0 0;min-height:18px}' +
    '#lamf-gate .g-msg{font-size:14px;line-height:21px;margin:0}' +
    '#lamf-gate .g-row{display:flex;justify-content:space-between;align-items:center}';
  document.head.appendChild(css);
  document.documentElement.classList.add('gate-lock');

  var box, t = get();
  if (t && Date.now() - okAt() < RECHECK && !isAdmin) { unlock(); return; }   // checked a moment ago on this tab
  ready(function () {
    if (!t) return show('mail');
    view('<p class="g-msg">Checking your access…</p>');
    call({ action: 'check', token: t }).then(function (r) {
      if (r.ok && r.status === 'Approved') return done(r);
      if (r.ok && r.status === 'Pending') return show('pending', r);
      if (r.ok) return show('denied', r);
      put(''); show('mail');
    }).catch(function () { view('<p class="g-msg">Could not check your access. Please check your connection and try again.</p><button type="button" onclick="location.reload()">Try again</button>'); });
  });

  function ready(fn) { document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', fn) : fn(); }
  function unlock() { document.documentElement.classList.remove('gate-lock'); var g = document.getElementById('lamf-gate'); if (g) g.remove(); }
  function done(r) {
    okAt(Date.now());
    if (isAdmin) { if (!r.admin) return show('denied', { status: 'NotAdmin' }); unlock(); return api.onAdmin && api.onAdmin(get(), r); }
    unlock();
  }
  function view(html) {
    if (!box) {
      box = document.createElement('div'); box.id = 'lamf-gate';
      box.innerHTML = '<div class="g-box"><div class="g-head">LAMF Prototype' + (isAdmin ? ' – Admin' : '') +
        '<small>Only for approved SCCL users</small></div><div class="g-body"></div></div>';
      document.body.appendChild(box);
    }
    box.querySelector('.g-body').innerHTML = html;
  }
  function esc(s) { return String(s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var mail = '', name = '';

  function show(step, r) {
    if (step === 'mail') {
      view('<p class="g-msg">Enter your SCCL mail ID. We will send you an OTP to verify it.</p>' +
        (isAdmin ? '' : '<label for="g-name">Your name</label><input id="g-name" autocomplete="name" maxlength="80">') +
        '<label for="g-mail">SCCL mail ID</label><input id="g-mail" type="email" autocomplete="email" placeholder="name@shriramcredit.in" maxlength="120">' +
        '<p class="g-err"></p><button type="button" id="g-send">Send OTP</button>');
      var b = box.querySelector('#g-send'), mi = box.querySelector('#g-mail'), ni = box.querySelector('#g-name');
      mi.value = mail; if (ni) ni.value = name; (ni && !name ? ni : mi).focus();
      mi.addEventListener('keydown', function (e) { if (e.key === 'Enter') b.click(); });
      b.onclick = function () {
        mail = mi.value.trim().toLowerCase(); name = ni ? ni.value.trim() : 'Admin';
        var err = box.querySelector('.g-err');
        if (ni && !name) return (err.textContent = 'Please enter your name.');
        if (!/^[a-z0-9._%+-]+@shriramcredit\.in$/.test(mail)) return (err.textContent = 'Only SCCL mail IDs (@shriramcredit.in) are allowed.');
        send(b, err);
      };
    } else if (step === 'otp') {
      view('<p class="g-msg">We have sent a 6-digit OTP to <b>' + esc(mail) + '</b>. It is valid for 10 minutes.</p>' +
        '<label for="g-otp">Enter OTP</label><input id="g-otp" inputmode="numeric" autocomplete="one-time-code" maxlength="6">' +
        '<p class="g-err"></p><button type="button" id="g-ver" disabled>Verify OTP</button>' +
        '<div class="g-row"><button type="button" class="g-link" id="g-back">Change mail ID</button>' +
        '<button type="button" class="g-link" id="g-re" disabled>Resend OTP in <span>30</span>s</button></div>');
      var o = box.querySelector('#g-otp'), v = box.querySelector('#g-ver'), re = box.querySelector('#g-re'), er = box.querySelector('.g-err');
      o.focus();
      o.addEventListener('input', function () { o.value = o.value.replace(/\D/g, '').slice(0, 6); v.disabled = o.value.length !== 6; });
      o.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !v.disabled) v.click(); });
      var n = 30, tm = setInterval(function () { n--; if (n <= 0) { clearInterval(tm); re.disabled = false; re.textContent = 'Resend OTP'; } else re.querySelector('span').textContent = n; }, 1000);
      re.onclick = function () { clearInterval(tm); send(re, er); };
      box.querySelector('#g-back').onclick = function () { clearInterval(tm); show('mail'); };
      v.onclick = function () {
        v.disabled = true; er.textContent = '';
        call({ action: 'verify', mail: mail, otp: o.value }).then(function (r) {
          if (!r.ok) { er.textContent = r.error; v.disabled = false; if (/Resend/.test(r.error)) { o.value = ''; v.disabled = true; } return; }
          clearInterval(tm); put(r.token);
          if (r.status === 'Approved') return done(r);
          show(r.status === 'Pending' ? 'pending' : 'denied', r);
        }).catch(function () { er.textContent = 'Could not verify. Please try again.'; v.disabled = false; });
      };
    } else if (step === 'pending') {
      view('<p class="g-msg"><b>Waiting for approval.</b><br>Your mail ID <b>' + esc(r.mail || mail) + '</b> is verified. The admin has been ' +
        'informed; you will get a mail once access is approved. Then open this page again.</p>' +
        '<button type="button" id="g-chk">Check again</button><button type="button" class="g-link" id="g-out">Use another mail ID</button>');
      box.querySelector('#g-chk').onclick = function () { okAt(0); location.reload(); };
      box.querySelector('#g-out').onclick = logout;
    } else {
      view('<p class="g-msg"><b>' + (r && r.status === 'NotAdmin' ? 'This page is only for the admin.' : 'You do not have access to this site.') +
        '</b><br>Please contact the LAMF project team.</p><button type="button" class="g-link" id="g-out">Use another mail ID</button>');
      box.querySelector('#g-out').onclick = logout;
    }
  }
  function send(btn, err) {
    btn.disabled = true; err.textContent = '';
    call({ action: 'send', mail: mail, name: name }).then(function (r) {
      if (!r.ok) { err.textContent = r.error; btn.disabled = false; return; }
      show('otp');
    }).catch(function () { err.textContent = 'Could not send the OTP. Please try again.'; btn.disabled = false; });
  }
  function notReady() {   // shown on admin.html until the Apps Script web app URL is added above
    var m = document.querySelector('#adm-main'); if (!m) return;
    m.innerHTML = '<div style="background:#fff;border-radius:10px;padding:18px 22px;box-shadow:0 1px 3px rgba(0,0,0,.08);line-height:1.6">' +
      '<h2 style="margin:0 0 8px;font-size:18px">Not switched on yet</h2>' +
      '<p style="margin:0 0 10px">The portal is ready. It starts working once the Google Sheet and its Apps Script are set up:</p><ol style="margin:0 0 10px;padding-left:20px">' +
      '<li>Create a Google Sheet named <b>LAMF Site Access</b>.</li>' +
      '<li><b>Extensions → Apps Script</b> – paste the script <code>lamf-journey/tools/access-apps-script.gs</code> – <b>Save</b>.</li>' +
      '<li>Select <b>setup</b> at the top and click <b>▶ Run</b>; allow the permissions.</li>' +
      '<li><b>Deploy → New deployment → Web app</b> – Execute as: <b>Me</b>, Who has access: <b>Anyone</b> – <b>Deploy</b>.</li>' +
      '<li>Send the <b>Web app URL</b> (ends in /exec) to Claude to connect it.</li></ol>' +
      '<p style="margin:0;color:#555">After that, this page asks for the admin mail ID and an OTP, then lists the access requests.</p></div>';
  }
})();
