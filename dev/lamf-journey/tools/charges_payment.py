"""LOS – charges payment after a DRAFT LAN rejection (DISC-351, Waiver BRD section 9). New – not in the live LOS yet.

charges-payment.html: a clickable mock-up of the customer's steps – payment link (SMS / mail) → OTP verification → Pay Charges page
(total charges with the breakup, one Pay CTA, no partial payment) → payment gateway (simulated) → success (lien removal will be
initiated soon, receipt) or failure (nothing changes – back to the Pay Charges page).
charges-receipt.html: the payment receipt – generated on payment, stored in the LMS Documents tab and sent to the customer.
Sample values are the same as the LMS prototype (DRAFT LAN SCCLMF20261100073: Processing Fee ₹1,768.82 with ₹500 waived) – the
Processing Fee includes the Lien Marking, Lien Removal and Stamp Duty charges and GST (DISC-354).
"""

LAN = "SCCLMF20261100073"
CHARGES = [("Processing Fee*", 1768.82, 500)]   # (charge, amount, waived off) – one charge only (DISC-354)
INCL = "*Inclusive of Lien Marking, Lien Removal and Stamp Duty"   # DISC-356
TOTAL = sum(a for _, a, _ in CHARGES)
WAIVED = sum(w for _, _, w in CHARGES)
PAYABLE = round(TOTAL - WAIVED, 2)
TXN, RCPT, PAID_ON = "pay_SCCL7Q2X9K4M1B", "RCPT/LAMF/2026/000149", "23-11-2026 11:42 AM"


def rs(v):
    v = round(v, 2)
    return f"₹{v:,.2f}" if v % 1 else f"₹{int(v):,}"


def _table(cls="cp-tbl"):   # customer view (DISC-352): only what the customer pays for each charge – no waived off / payable columns
    rows = "".join(f"<tr><td>{n}</td><td>{rs(a - w)}</td></tr>" for n, a, w in CHARGES if round(a - w, 2) > 0)
    return (f'<table class="{cls}"><thead><tr><th>Charges</th><th>Amount</th></tr></thead>'
            f'<tbody>{rows}</tbody><tfoot><tr><td>Total</td><td>{rs(PAYABLE)}</td></tr></tfoot></table><p class="cp-incl">{INCL}</p>')


HDR = ('<header class="hdr cp-hdr"><a class="logo" href="index.html" title="Home"><img src="assets/img/shriram-logo.png" alt="Shriram Credit"></a>'
       '{right}</header>')


def body():
    steps = ["Payment link", "OTP verification", "Pay Charges", "Payment gateway", "Payment result"]
    bar = "".join(f'<button type="button" class="cp-step" data-go="{k}">{k + 1}. {s}</button>' for k, s in enumerate(steps))
    sms = (f"Dear AZHAGARSAMY, Your LAMF application has been rejected. To unpledge your MF units, please pay the charges of "
           f"Rs. {PAYABLE:,.2f} here: <a class='cp-link' data-go='1'>https://lamf.shriramcredit.in/user/loans/</a> - Shriram Credit")
    s0 = (f'<section class="cp-s" data-s="0"><div class="cp-phone"><p class="cp-ph-h">SGRCDT-T</p><div class="cp-bubble">{sms}</div>'
          '<p class="cp-ph-n">The same link is in the rejection mail (Pay Charges button). Tap the link.</p></div></section>')
    s1 = (f'<section class="cp-s" data-s="1" hidden>{HDR.format(right="")}<main class="cp-main"><div class="card cp-card cp-otp">'
          '<h3>Verify your mobile number</h3><p class="cp-sub">A 6-digit OTP has been sent by Shriram Credit to <b>+9195XXXX1623</b></p>'
          '<div class="otp">' + '<input maxlength="1" inputmode="numeric" autocomplete="off">' * 6 + '</div>'
          '<p class="otp-hint">Please use OTP <b>123456</b> to proceed</p><p class="cp-resend">Didn’t Receive OTP? <a>Resend OTP</a></p>'
          '<p class="field-err cp-err"></p><button type="button" class="btn btn-disabled btn-block cp-submit" disabled>Submit OTP</button>'
          '</div></main></section>')
    s2 = (f'<section class="cp-s" data-s="2" hidden>{HDR.format(right="<span class=cp-out>Logout</span>")}<main class="cp-main">'
          '<div class="card cp-card cp-pay"><h3>Pay Charges</h3>'
          f'<div class="cp-banner">Your Loan Against Mutual Fund application (<b>{LAN}</b>) has been rejected. Please pay the charges '
          'below to unpledge your Mutual Fund units.</div>'
          f'{_table()}<div class="cp-total"><span>Total Payable</span><b>{rs(PAYABLE)}</b></div>'
          '<p class="cp-note">The full amount has to be paid in one payment – partial payment is not available.</p>'
          f'<button type="button" class="btn btn-primary bold btn-block cp-paybtn" data-go="3">Pay {rs(PAYABLE)}</button>'
          '<p class="cp-sec">Payments are processed securely through the payment gateway.</p></div></main></section>')
    s3 = (f'<section class="cp-s" data-s="3" hidden><div class="cp-pg"><p class="cp-pg-h">Payment gateway (simulation)</p>'
          f'<p class="cp-pg-a">Shriram Credit Company Limited<br><b>{rs(PAYABLE)}</b></p><p class="cp-pg-n">UPI, cards and net banking as '
          'offered by the payment gateway.</p><div class="cp-pg-b"><button type="button" class="btn btn-primary bold" data-go="4">Payment successful</button>'
          '<button type="button" class="btn btn-outline cp-fail" data-go="2">Payment failed</button></div>'
          '<p class="cp-pg-n">Payment failed → nothing changes: the customer is back on the Pay Charges page and can pay again.</p></div></section>')
    s4 = (f'<section class="cp-s" data-s="4" hidden>{HDR.format(right="<span class=cp-out>Logout</span>")}<main class="cp-main">'
          '<div class="card cp-card cp-done"><div class="cp-tick">✓</div><h3>Payment successful</h3>'
          f'<p class="cp-sub">We have received your payment of <b>{rs(PAYABLE)}</b>. Your lien removal will be initiated soon.</p>'
          f'<div class="cp-kv"><span>Loan Application ID</span><b>{LAN}</b><span>Amount Paid</span><b>{rs(PAYABLE)}</b>'
          f'<span>Transaction ID</span><b>{TXN}</b><span>Paid on</span><b>{PAID_ON}</b><span>Receipt No.</span><b>{RCPT}</b></div>'
          '<a class="btn btn-outline btn-block" href="charges-receipt.html" target="_blank" rel="noopener">Download Receipt</a>'
          '<p class="cp-sec">The receipt is also sent to your registered email ID. You will be informed once the lien on your Mutual '
          'Fund units is removed.</p></div></main></section>')
    return ('<div class="cp"><div class="cp-top"><a href="index.html">← Home</a><b>LOS – Charges payment (after rejection)</b>'
            '<span class="lms-new">New – as per the Waiver BRD (section 9). Not in the live LOS yet.</span></div>'
            f'<nav class="cp-bar">{bar}</nav>{s0}{s1}{s2}{s3}{s4}</div>' + JS)


JS = """<script>
(function () {
  var S = document.querySelectorAll('.cp-s'), B = document.querySelectorAll('.cp-step');
  function go(n) { S.forEach(function (s) { s.hidden = s.dataset.s != n; }); B.forEach(function (b) { b.classList.toggle('on', b.dataset.go == n); });
    if (n == 1) { var i = document.querySelectorAll('.cp-otp .otp input'); i.forEach(function (x) { x.value = ''; }); chk(); i[0].focus(); }
    window.scrollTo(0, 0); }
  document.addEventListener('click', function (e) { var g = e.target.closest('[data-go]'); if (g) go(g.dataset.go); });
  var ins = document.querySelectorAll('.cp-otp .otp input'), sub = document.querySelector('.cp-submit'), err = document.querySelector('.cp-err');
  function val() { return Array.prototype.map.call(ins, function (x) { return x.value; }).join(''); }
  function chk() { var ok = /^\\d{6}$/.test(val()); sub.disabled = !ok; sub.className = 'btn btn-block cp-submit ' + (ok ? 'btn-primary bold' : 'btn-disabled'); err.textContent = ''; }
  ins.forEach(function (x, k) {
    x.addEventListener('input', function () { x.value = x.value.replace(/\\D/g, '').slice(0, 1); if (x.value && ins[k + 1]) ins[k + 1].focus(); chk(); });
    x.addEventListener('keydown', function (e) { if (e.key === 'Backspace' && !x.value && ins[k - 1]) ins[k - 1].focus(); });
  });
  sub.addEventListener('click', function () { if (val() === '123456') go(2); else err.textContent = 'Invalid OTP. Please try again.'; });
  go(0);
})();
</script>"""


def receipt():
    rows = "".join(f"<tr><td>{n}</td><td>{rs(a)}</td><td>{rs(w)}</td><td>{rs(a - w)}</td></tr>" for n, a, w in CHARGES)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Payment Receipt – {RCPT}</title>
<style>
body{{margin:0;background:#efeeec;font-family:Arial,Helvetica,sans-serif;color:#1a1a1a}}
.r{{width:680px;max-width:calc(100% - 24px);margin:28px auto;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
.h{{display:flex;justify-content:space-between;align-items:center;padding:24px 32px;border-bottom:5px solid #FFC20E}} .h img{{width:170px}}
.h p{{margin:0;font-size:12px;line-height:18px;color:#555;text-align:right}}
.t{{background:#1a1a1a;color:#FFC20E;text-align:center;font-weight:bold;font-size:18px;padding:14px}}
.b{{padding:24px 32px}} .kv{{display:grid;grid-template-columns:1fr 1fr;gap:10px 24px;font-size:14px;margin-bottom:20px}}
.kv span{{color:#666;display:block;font-size:12px}} table{{width:100%;border-collapse:collapse;font-size:14px}}
th,td{{border:1px solid #e2e2e2;padding:8px 10px;text-align:right}} th:first-child,td:first-child{{text-align:left}} th{{background:#FAFAF8}}
tfoot td{{font-weight:bold}} .w{{margin:14px 0 0;font-size:14px}} .n{{margin:18px 0 0;font-size:12px;color:#666;line-height:18px}}
.f{{background:#FFC20E;padding:12px 32px;font-size:12px}}
</style></head><body><div class="r">
<div class="h"><img src="assets/img/shriram-logo.png" alt="Shriram Credit"><p><b>Shriram Credit Company Limited</b><br>Payment Receipt</p></div>
<div class="t">Payment Receipt</div>
<div class="b"><div class="kv">
<div><span>Receipt No.</span>{RCPT}</div><div><span>Receipt Date</span>{PAID_ON}</div>
<div><span>Customer Name</span>AZHAGARSAMY SUBBURAJ</div><div><span>Loan Application ID (LAN)</span>{LAN}</div>
<div><span>Payment Mode</span>Online – payment gateway</div><div><span>Transaction ID</span>{TXN}</div>
<div><span>Purpose</span>Charges on rejection of the Loan Against Mutual Fund application</div><div><span>Amount Received</span><b>{rs(PAYABLE)}</b></div>
</div>
<table><thead><tr><th>Charges</th><th>Amount of Charges</th><th>Waived off</th><th>Amount Paid</th></tr></thead><tbody>{rows}</tbody>
<tfoot><tr><td>Total</td><td>{rs(TOTAL)}</td><td>{rs(WAIVED)}</td><td>{rs(PAYABLE)}</td></tr></tfoot></table>
<p class="w">Amount received in words: <b>Rupees One Thousand Two Hundred Sixty-Eight and Paise Eighty-Two Only</b></p>
<p class="n">{INCL}. This is a system-generated receipt and does not need a signature. The lien on your Mutual Fund
units will be removed after the payment is confirmed.</p></div>
<div class="f">Sample receipt for the prototype (Waiver BRD) – generated on payment, stored in the LMS Documents tab and sent to the customer.</div>
</div></body></html>
"""
