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
TXN, RCPT, PAID_ON = "pay_SCCL7Q2X9K4M1B", "RCPT/LAMF/2026/11/0149", "23-11-2026 11:42 AM"


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


_ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen",
         "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
_TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]


def _w2(n):
    return _ONES[n] if n < 20 else _TENS[n // 10] + ("-" + _ONES[n % 10] if n % 10 else "")


def _w3(n):
    return (_ONES[n // 100] + " Hundred" + (" " + _w2(n % 100) if n % 100 else "")) if n >= 100 else _w2(n)


def in_words(v):
    """Indian numbering – Rupees … and Paise … Only."""
    r, p = int(v), round((v - int(v)) * 100)
    parts = []
    for div, name in ((10000000, "Crore"), (100000, "Lakh"), (1000, "Thousand")):
        if r >= div:
            parts.append(_w3(r // div) + " " + name); r %= div
    if r:
        parts.append(_w3(r))
    return "Rupees " + (" ".join(parts) or "Zero") + (f" and Paise {_w2(p)}" if p else "") + " Only"


def receipt():
    """Payment receipt sent to the customer (DISC-425): company details, receipt and payment details, the amount paid with the GST
    breakup (customer view – no waived amount, DISC-352), amount in words and the disclaimer. Printable / Save as PDF."""
    taxable = round(PAYABLE / 1.18, 2)
    gst = round(PAYABLE - taxable, 2)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Payment Receipt – {RCPT}</title>
<style>
body{{margin:0;background:#efeeec;font-family:Arial,Helvetica,sans-serif;color:#1a1a1a}}
.bar{{width:760px;max-width:calc(100% - 24px);margin:18px auto 0;display:flex;justify-content:flex-end}}
.bar button{{background:#1a1a1a;color:#fff;border:0;border-radius:6px;padding:9px 16px;font-size:13px;cursor:pointer}}
.r{{width:760px;max-width:calc(100% - 24px);margin:12px auto 28px;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
.h{{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;padding:24px 32px;border-bottom:5px solid #FFC20E}} .h img{{width:170px}}
.h p{{margin:0;font-size:11.5px;line-height:17px;color:#555;text-align:right}} .h p b{{color:#1a1a1a;font-size:13px}}
.t{{display:flex;justify-content:space-between;align-items:center;background:#1a1a1a;color:#FFC20E;font-weight:bold;font-size:18px;padding:12px 32px}}
.t span{{background:#1e7d32;color:#fff;font-size:12px;border-radius:12px;padding:3px 10px}}
.b{{padding:22px 32px}} h3{{font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:#666;margin:0 0 10px}}
.kv{{display:grid;grid-template-columns:1fr 1fr;gap:10px 24px;font-size:14px;margin-bottom:22px}}
.kv span{{color:#666;display:block;font-size:12px;margin-bottom:2px}}
table{{width:100%;border-collapse:collapse;font-size:14px}} th,td{{border:1px solid #e2e2e2;padding:8px 10px;text-align:right}}
th:first-child,td:first-child{{text-align:left}} th{{background:#FAFAF8}} tfoot td{{font-weight:bold;background:#FFF8E1}}
.w{{margin:12px 0 0;font-size:14px}} .incl{{margin:6px 0 0;font-size:12px;color:#666}}
.msg{{margin:18px 0 0;padding:12px 14px;background:#F1F8F2;border-left:4px solid #1e7d32;font-size:13px;line-height:19px}}
.d{{margin:22px 0 0;padding:14px 16px;border:1px solid #e2e2e2;border-radius:6px;background:#FAFAF8}}
.d h3{{margin-bottom:8px}} .d ol{{margin:0;padding-left:18px;font-size:12px;line-height:18px;color:#444}} .d li{{margin:3px 0}}
.f{{background:#FFC20E;padding:12px 32px;font-size:11.5px;line-height:17px}}
.note{{width:760px;max-width:calc(100% - 24px);margin:0 auto 24px;font-size:12px;color:#666}}
@media (max-width:600px){{.kv{{grid-template-columns:1fr}} .h{{flex-direction:column}} .h p{{text-align:left}}}}
@page{{size:A4;margin:8mm}}
@media print{{body{{background:#fff}} .bar,.note{{display:none}} .r{{box-shadow:none;margin:0 auto;width:100%;max-width:none;zoom:.82}}
  .h,.t,.f,tfoot td,.msg,.d{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}}}
</style></head><body>
<div class="bar"><button type="button" onclick="window.print()">Download / Print receipt</button></div>
<div class="r">
<div class="h"><img src="assets/img/shriram-logo.png" alt="Shriram Credit">
<p><b>Shriram Credit Company Limited</b><br>Registered Office: Shriram House, No. 4, Burkit Road, T. Nagar, Chennai 600017<br>
CIN: U65993TN1980PLC008215 · RBI Registration No.: B-07.00709<br>GSTIN: {{{{SCCL GSTIN}}}}</p></div>
<div class="t">Payment Receipt <span>Payment Successful</span></div>
<div class="b">
<h3>Receipt details</h3>
<div class="kv">
<div><span>Receipt No.</span><b>{RCPT}</b></div><div><span>Receipt Date &amp; Time</span>{PAID_ON}</div>
<div><span>Customer Name</span>AZHAGARSAMY</div><div><span>Loan Application No. (LAN)</span>{LAN}</div>
<div><span>Registered Mobile No.</span>XXXXXX7890</div><div><span>Product</span>Loan Against Mutual Funds (LAMF)</div>
</div>
<h3>Payment details</h3>
<div class="kv">
<div><span>Payment Mode</span>Online – payment gateway (UPI / Net Banking / Debit Card)</div><div><span>Transaction ID</span>{TXN}</div>
<div><span>Payment Status</span>Successful</div><div><span>Amount Received</span><b>{rs(PAYABLE)}</b></div>
<div style="grid-column:1/-1"><span>Purpose of Payment</span>Charges payable on the rejection of the Loan Against Mutual Funds application</div>
</div>
<table><thead><tr><th>Charges</th><th>Taxable Value</th><th>IGST @ 18%</th><th>Amount Paid</th></tr></thead>
<tbody><tr><td>Processing Fee*</td><td>{rs(taxable)}</td><td>{rs(gst)}</td><td>{rs(PAYABLE)}</td></tr></tbody>
<tfoot><tr><td>Total</td><td>{rs(taxable)}</td><td>{rs(gst)}</td><td>{rs(PAYABLE)}</td></tr></tfoot></table>
<p class="incl">{INCL}</p>
<p class="w">Amount received in words: <b>{in_words(PAYABLE)}</b></p>
<p class="msg">Thank you. We have received your payment. The removal of the lien on your Mutual Fund units will be initiated after the
payment is confirmed, and you will receive a separate confirmation from CAMS / KFintech once the units are released.</p>
<div class="d"><h3>Disclaimer</h3><ol>
<li>This is a computer-generated receipt and does not require a signature.</li>
<li>This receipt is issued towards the charges for the above loan application only. It is not a payment towards any loan account.</li>
<li>The charges include GST at the applicable rate. The Processing Fee* is inclusive of the Lien Marking, Lien Removal and Stamp Duty charges.</li>
<li>The amount paid is not refundable, except in case of a duplicate or excess payment, which will be refunded to the source account after
verification.</li>
<li>This receipt is subject to the realisation of the payment. If the transaction is reversed by the bank or the payment gateway, this receipt
stands cancelled.</li>
<li>Please check the details in this receipt. In case of any discrepancy, write to lassupport@shriramcredit.in within 7 days of the receipt
date, quoting the Receipt No. and the LAN.</li>
<li>For grievances, write to grievanceredressal@shriramcredit.in. Please keep this receipt for your records.</li>
</ol></div>
</div>
<div class="f">Shriram Credit Company Limited · Shriram House, No. 4, Burkit Road, T. Nagar, Chennai 600017 · lassupport@shriramcredit.in</div>
</div>
<p class="note">Prototype (Waiver BRD) – the receipt is generated on payment, saved in the LMS Documents tab and sent to the customer with the
Charges Payment Received mail. Receipt No. format: RCPT/LAMF/{{{{Payment Year}}}}/{{{{Payment Month}}}}/{{{{Number of receipts as 4 digits}}}}.
GSTIN to be added.</p>
</body></html>
"""
