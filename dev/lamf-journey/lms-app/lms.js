/* LMS prototype (DISC-484, DISC-494) – page logic. Source file. */
(function () {
  // ---- Login: only an SCCL mail ID (@shriramcredit.in) is accepted
  var f = document.getElementById('lg-form');
  if (f) {
    var mail = document.getElementById('lg-mail'), err = document.getElementById('lg-err'), next = document.getElementById('lg-next');
    var MSG = {   // wording to be confirmed against the live LMS
      empty: 'Please enter your email ID.',
      bad: 'Please enter a valid Shriram Credit email ID (@shriramcredit.in).'
    };
    var show = function (m) { err.textContent = m || ''; mail.classList.toggle('bad', !!m); };
    mail.addEventListener('input', function () { if (err.textContent) show(''); next.hidden = true; });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = mail.value.trim().toLowerCase();
      if (!v) return show(MSG.empty);
      if (!/^[a-z0-9._%+-]+@shriramcredit\.in$/.test(v)) return show(MSG.bad);
      show('');
      location.href = 'otp.html?mail=' + encodeURIComponent(v);   // DISC-494: OTP step
    });
  }

  // ---- Login – OTP step (DISC-494): 6 boxes, 30-second resend timer, Submit
  var of = document.getElementById('ot-form');
  if (of) {
    var m = (new URLSearchParams(location.search).get('mail') || '').toLowerCase();
    if (!/^[a-z0-9._%+-]+@shriramcredit\.in$/.test(m)) { location.replace('login.html'); return; }
    document.getElementById('ot-mail').textContent = m;
    var wrap = document.getElementById('ot-boxes'), boxes = [].slice.call(wrap.querySelectorAll('input'));
    var oerr = document.getElementById('ot-err'), onext = document.getElementById('ot-next');
    var timer = document.getElementById('ot-timer'), again = document.getElementById('ot-again');
    var OTP_OK = '000000';   // DISC-496: the sample correct OTP of the prototype (also shown in the OTP mail)
    var OMSG = { short: 'Please enter the 6-digit OTP.', wrong: 'Please enter the correct OTP.' };   // wrong OTP: UAT shows “Bad credentials” – owner's wording
    var bad = function (msg) { oerr.textContent = msg || ''; wrap.classList.toggle('bad', !!msg); };
    boxes.forEach(function (b, i) {
      b.addEventListener('input', function () {
        var d = b.value.replace(/\D/g, '');
        if (d.length > 1) { fill(d, i); return; }
        b.value = d; bad(''); onext.hidden = true;
        if (d && boxes[i + 1]) boxes[i + 1].focus();
      });
      b.addEventListener('keydown', function (e) {
        if (e.key === 'Backspace' && !b.value && boxes[i - 1]) { boxes[i - 1].focus(); boxes[i - 1].value = ''; e.preventDefault(); }
        if (e.key === 'ArrowLeft' && boxes[i - 1]) boxes[i - 1].focus();
        if (e.key === 'ArrowRight' && boxes[i + 1]) boxes[i + 1].focus();
      });
      b.addEventListener('paste', function (e) {
        var d = ((e.clipboardData || window.clipboardData).getData('text') || '').replace(/\D/g, '');
        if (d) { e.preventDefault(); fill(d, i); }
      });
    });
    function fill(d, from) {
      for (var k = 0; k < d.length && from + k < boxes.length; k++) boxes[from + k].value = d[k];
      boxes[Math.min(from + d.length, boxes.length - 1)].focus(); bad('');
    }
    boxes[0].focus();
    var left;
    function start() {
      left = 30; again.hidden = true; timer.hidden = false;
      var tick = function () { timer.textContent = '0:' + ('0' + left).slice(-2); };
      tick();
      var t = setInterval(function () { left--; if (left <= 0) { clearInterval(t); timer.hidden = true; again.hidden = false; } else tick(); }, 1000);
    }
    start();
    again.addEventListener('click', function () { boxes.forEach(function (b) { b.value = ''; }); boxes[0].focus(); bad(''); start(); });
    of.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = boxes.map(function (b) { return b.value; }).join('');
      if (v.length < 6) return bad(OMSG.short);
      if (v !== OTP_OK) return bad(OMSG.wrong);
      bad(''); onext.hidden = false;
      onext.textContent = 'OTP submitted. The screen after login comes next – please share its UAT screenshot.';
    });
  }
})();
