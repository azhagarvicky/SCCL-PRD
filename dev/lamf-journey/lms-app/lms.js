/* LMS prototype (DISC-484) – page logic. Source file. */
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
      next.hidden = false;
      next.innerHTML = 'OTP sent to <b>' + v.replace(/[<>&"]/g, '') + '</b>.<br>The OTP screen comes next – please share its UAT screenshot.';
    });
  }
})();
