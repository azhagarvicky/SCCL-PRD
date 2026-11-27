"""LMS page (DISC-327) – opened by the “LMS” CTA on the home page.

The modules follow the left menu of the LMS (uatlms.shriramcredit.in): Dashboard, Products, Loans (Active, Inactive, Draft,
Submitted, Closed, Rejected), Collaterals, Clients, Approvals, Disbursement Management, Reports, Settings.
Each module opens its own section (CSS :target, no script). Content for each module is added here as the owner shares it.
"""
import html as _h

LMS_MODULES = [   # (id, name, sub-modules, description)
    ("dashboard", "Dashboard", [], ""),
    ("products", "Products", [], ""),
    ("loans", "Loans", [("active", "Active"), ("inactive", "Inactive"), ("draft", "Draft"), ("submitted", "Submitted"),
                        ("closed", "Closed"), ("rejected", "Rejected")], ""),
    ("collaterals", "Collaterals", [], ""),
    ("clients", "Clients", [], ""),
    ("approvals", "Approvals", [], ""),
    ("disbursement", "Disbursement Management", [], ""),
    ("reports", "Reports", [], ""),
    ("settings", "Settings", [], ""),
]

TBA = '<p class="lms-tba">Screens and requirements for this module will be added here.</p>'

# ---- Loans list views (DISC-328) – columns, filters and status badges as in the live LMS (lms.shriramcredit.in/loans/<status>).
# Rows are SAMPLE data only (made-up names, PANs and LANs) – no real customer data.
BASE_COLS = ["LAN", "Product Id", "Client Name", "Status", "PAN", "Sanction Amount", "Rate of Interest", "Start Date", "End Date",
             "Generated", "Source"]
ACTIVE_COLS = BASE_COLS[:2] + ["Risk Level"] + BASE_COLS[2:]
REJECTED_COLS = ["LAN", "Product Id", "Client Name", "PAN", "Sanction Amount", "Rate of Interest", "Generated", "Source"]
_NAMES = ["Sample Customer A", "Sample Customer B", "Sample Customer C", "Sample Customer D", "Sample Customer E",
          "Sample Customer F", "Sample Customer G", "Sample Customer H", "Sample Customer I", "Sample Customer J"]
_SRC = ["SCCL LOS", "Quicklend", "Liquify", "SCCL LOS", "Quicklend", "Forward wealth", "SCCL LOS", "Liquify", "Quicklend", "SCCL LOS"]
_PROD = ["LAMF20261114", "LAMF20261113", "LAMF20261117", "LAMF20261114", "LAMF2026106", "LAMF20261113", "LAMF20261114",
         "LAMF20261117", "LAMF2026106", "LAMF20261113"]
_AMT = ["₹1,25,000", "₹59,300", "₹19,300", "₹1,06,000", "₹32,500", "₹10,600", "₹22,400", "₹19,000", "₹18,700", "₹18,200"]
_ROI = ["10.49%", "11%", "10.49%", "10.49%", "11%", "11%", "10.49%", "10.49%", "10.49%", "10.49%"]


START = {"active": 99, "inactive": 89, "draft": 79, "submitted": 69, "closed": 59, "rejected": 49}   # unique sample LANs per list


def _rows(view):
    n = {"active": 10, "inactive": 10, "draft": 10, "submitted": 5, "closed": 2, "rejected": 2}[view]
    status = {"active": "Active", "inactive": "Inactive", "draft": "Draft", "submitted": "Submitted", "closed": "Foreclosed"}.get(view)
    out = []
    for k in range(n):
        d = 17 - k // 2
        r = {"LAN": f"SCCLMF202611000{START[view] - k:02d}", "Product Id": _PROD[k], "Client Name": _NAMES[k], "Status": status,
             "PAN": f"ABCPX{1000 + k * 7}A", "Generated": f"{d:02d}/11/2026", "Source": _SRC[k],
             "Risk Level": ["No Risk", "No Risk", "No Risk", "L1", "L1", "L1", "L1", "L1", "No Risk", "No Risk"][k]}
        has_amt = view in ("active", "closed", "rejected") or k % 3 == 0
        r["Sanction Amount"] = _AMT[k] if has_amt else "-"
        r["Rate of Interest"] = _ROI[k] if (has_amt or k % 2 == 0) else "-"
        if view in ("active", "closed"):
            r["Start Date"] = f"{d - 1:02d}/11/2026"
            r["End Date"] = f"{d - 2:02d}/11/2029" if view == "active" else f"{d + 3:02d}/11/2026"
        else:
            r["Start Date"] = r["End Date"] = "-"
        out.append(r)
    return out


NUM = {"Sanction Amount", "Rate of Interest"}


def loan_view(view):
    cols = ACTIVE_COLS if view == "active" else REJECTED_COLS if view == "rejected" else BASE_COLS
    rows = _rows(view)
    def cell(c, r):
        v = r[c]
        if c == "Status":
            return f'<td><span class="lms-st st-{v.lower()}">{_h.escape(v)}</span></td>'
        if c == "LAN":
            return f'<td><a class="lms-lan" href="#lan-{view}-{v}">{_h.escape(v)}</a></td>'
        return f'<td class="{"num" if c in NUM else ""}">{_h.escape(v)}</td>'
    chips = ('<span class="lms-chip on">All</span><span class="lms-chip">Shortfall</span><span class="lms-chip">In Default</span>'
             if view == "active" else "")
    note = ('<p class="lms-note">Columns assumed to be the same as Draft – share a Submitted screenshot to confirm.</p>'
            if view == "submitted" else "")
    return (f'<div class="lms-filters"><span class="lms-select">Select a value <i>⌄</i></span>{chips}</div>{note}'
            '<div class="lms-tablewrap"><table class="lms-table"><thead><tr>'
            + "".join(f'<th class="{"num" if c in NUM else ""}">{c}</th>' for c in cols) + '</tr></thead><tbody>'
            + "".join("<tr>" + "".join(cell(c, r) for c in cols) + "</tr>" for r in rows) + '</tbody></table></div>'
            f'<div class="lms-pager"><span>Showing 1 - {len(rows)} items</span><span class="lms-pp"><span class="lms-select">10 <i>⌄</i></span>'
            ' rows/page <span class="lms-pg">‹</span><span class="lms-pg">›</span></span></div>'
            '<p class="lms-sample">Sample data for the prototype – not real customers.</p>')


# ---- LAN detail (DISC-329) – opened by clicking a LAN in any loan list; layout as in the LMS loan page (Overview tab).
TABS = ["Overview", "Approvals", "Disbursement &amp; Repayments", "Collateral", "Transactions &amp; Reports", "KYC", "Documents",
        "Audit", "Notes"]


def _num(v):
    return int(v.replace("₹", "").replace(",", "")) if v not in ("-", None) else None


def _rs(n, dec=False):
    if n is None:
        return "-"
    s = f"{n:,.2f}" if dec else f"{int(n):,}"
    whole, _, frac = s.partition(".")
    whole = whole.replace(",", "")
    head, tail = whole[:-3], whole[-3:]
    head = ",".join([head[max(0, i - 2):i] for i in range(len(head), 0, -2)][::-1]) if head else ""
    return "₹" + (head + "," if head else "") + tail + ("." + frac if frac else "")


# ---- Approvals tab for a DRAFT loan (DISC-337) – new, as per the Waiver BRD 3.1 / 3.2 (not in the live LMS yet).
# Charges depend on how far the customer went (Waiver BRD scenarios 2 – 4); amounts include 18% GST.
# DISC-354: Lien Marking, Lien Removal and Stamp Duty are included in the Processing Fee – one charge only (sample ₹1,499 + GST – sanctioned amount below ₹1.5 lakh, DISC-355)
# DISC-356: scenario 2 (pledged, no Sanction Letter yet) – Lien Marking + Lien Removal; from the Sanction Letter – Processing Fee* only
# DISC-400: in LMS the Processing Fee* is shown split – Processing Fee (₹1,499 − ₹750 = ₹749 + GST) + Lien Marking + Lien Removal + Stamp Duty
_SPLIT = [("Processing Fee", 883.82), ("Lien Marking Charges", 531), ("Lien Removal Charges", 118), ("Stamp Duty Charges", 236)]
DRAFT_CHARGES = {2: [("Lien Marking Charges", 531), ("Lien Removal Charges", 118)], 3: _SPLIT, 4: _SPLIT}
FX = ' data-fixed="1"'
FIXED = {"Lien Marking Charges", "Lien Removal Charges", "Stamp Duty Charges", "Pledge", "Stamp duty", "Collateral release"}   # DISC-400: full waive-off only


FOOT = ("Lien Marking, Lien Removal and Stamp Duty can only be waived in full – select or unselect. Other charges: enter any amount. "
        "The customer sees one Processing Fee* (inclusive of Lien Marking, Lien Removal and Stamp Duty).")   # DISC-400


def _amt(v):
    return f"{v:,.2f}".rstrip("0").rstrip(".") if v % 1 else f"{int(v):,}"


def draft_approvals(r, tid):
    """Draft loan Approvals tab. DISC-361: waive-off and rejection are ONE request – OPS enters the amounts to waive and the reason
    and clicks Reject; the request goes to Treasury, who approves (waive-off and rejection applied together) or declines (request
    cancelled, LAN stays DRAFT). No separate Waive-off button."""
    k = START["draft"] - int(r["LAN"][-2:])
    sc = 2 if k < 4 else 3 if k < 7 else 4
    # DISC-362: maker → checker → Treasury by the sanctioned amount (a draft with no sanctioned amount yet is taken as below ₹5 lakh)
    mk, ck, tr = "OPS L1", "OPS L2 / OPS L3", "Treasury L1 / L2 / L3"   # DISC-400: same for any sanctioned amount
    # DISC-345: “Waived off Charges” column – what is already waived; Amount of Charges stays the original charge
    rows = "".join(f'<tr data-name="{n}" data-chg="{a}" data-done="0"{FX if n in FIXED else ""}><td><input type="checkbox" class="wv-chk" aria-label="Select {n}"></td><td>{n}</td>'
                   f'<td class="num wv-chg">₹{_amt(a)}</td><td class="num wv-done-amt">₹0</td>'
                   f'<td><input class="wv-amt" type="number" min="0" step="0.01" value="0" data-max="{a}" disabled></td>'
                   f'<td class="num wv-pay">₹{_amt(a)}</td></tr>' for n, a in DRAFT_CHARGES[sc])
    total = sum(a for _, a in DRAFT_CHARGES[sc])
    pop = lambda cls, body: f'<div class="wv-pop {cls}" hidden><div class="wv-box"><button type="button" class="wv-x" aria-label="Close">×</button>{body}</div></div>'
    return (f'<div class="wv" data-tid="{tid}" data-orig="{total}" data-mk="{mk}" data-ck="{ck}" data-tr="{tr}"><p class="lms-new">New – as per the Waiver BRD (Waiver BRD scenario {sc}). '
            'Not in the live LMS yet.</p>'
            '<div class="wv-head"><h3>Waive-off charges</h3></div>'
            '<table class="lms-table wv-table"><thead><tr><th><input type="checkbox" class="wv-all" aria-label="Select all"></th>'
            '<th>Charges Name</th><th class="num">Amount of Charges</th><th class="num">Waived off Charges</th><th>Amount to be waived off</th><th class="num">Payable Charges</th></tr></thead>'
            f'<tbody>{rows}</tbody><tfoot><tr><td></td><td><b>Total</b></td><td class="num"><b class="wv-ctot">₹{_amt(total)}</b></td>'
            f'<td class="num"><b class="wv-dtot">₹0</b></td><td><b class="wv-wtot">₹0</b></td><td class="num"><b class="wv-ptot">₹{_amt(total)}</b></td></tr></tfoot></table>'
            + f'<p class="wv-hint">{FOOT}</p>' +
            '<p class="wv-allgone" hidden>All charges have been waived off – nothing is payable.</p>'
            '<p class="wv-type">Type of waive-off: <b>No waive-off</b></p>'
            f'<p class="wv-role">Maker: <b>{mk}</b> → Checker: <b>{ck}</b> → <b>{tr}</b> (any sanctioned amount)</p>'
            '<label class="wv-lbl">Add a note <span>(required – rejection reason, recorded in the Audit)</span></label>'
            '<textarea class="wv-note" rows="2" placeholder="Add a note"></textarea>'
            '<label class="wv-lbl">Upload a file <span>(required)</span></label>'
            '<label class="wv-drop">Drop files here or <u>click</u><input type="file" class="wv-file" hidden></label><p class="wv-fname"></p>'
            '<p class="wv-hint">PDF, PNG or JPG. Max 5MB</p><p class="wv-err"></p>'
            f'<div class="wv-ctas"><button type="button" class="wv-reject">Reject</button></div>'
            # DISC-362: OPS checker – can change the amounts; a change needs the note and a file
            f'<div class="wv-ck" hidden><h3>Waive-off &amp; Rejection – pending {ck} (Checker) approval</h3><p class="wv-ck-st"></p>'
            '<p class="wv-hint">The checker can change the amounts to be waived off in the table above. If anything is changed, the note and a '
            'file are required; otherwise only the note.</p>'
            '<label class="wv-lbl">Checker note <span>(required)</span></label>'
            '<textarea class="wv-cnote" rows="2" placeholder="Add a note"></textarea>'
            '<label class="wv-lbl">Upload a file <span>(required if changed)</span></label>'
            '<label class="wv-drop">Drop files here or <u>click</u><input type="file" class="wv-cfile" hidden></label><p class="wv-fname"></p>'
            '<p class="wv-cerr"></p><div class="wv-appr-ctas"><button type="button" class="wv-ck-dec">Decline Rejection</button>'
            f'<button type="button" class="wv-ck-app">Accept Rejection</button></div><p class="wv-hint">{ck} only.</p></div>'
            # DISC-361 / 362: Treasury – approve or decline only, no change to the amounts
            f'<div class="wv-appr" hidden><h3>Waive-off &amp; Rejection – pending {tr} approval</h3><p class="wv-appr-st"></p>'
            '<label class="wv-lbl">Treasury note <span>(required)</span></label>'
            '<textarea class="wv-tnote" rows="2" placeholder="Add a note"></textarea><p class="wv-terr"></p>'
            '<div class="wv-appr-ctas"><button type="button" class="wv-decline">Decline Rejection</button><button type="button" class="wv-approve">Accept Rejection</button></div>'   # DISC-465
            f'<p class="wv-hint">{tr} only – Treasury can only approve or decline; the amounts cannot be changed.</p></div>'
            '<div class="wv-done" hidden></div>'
            # DISC-351: after the rejection – customer payment (from the LOS), Treasury confirmation, then de-pledge
            '<div class="wv-pay-box" hidden><h3>Charges payment</h3><p class="wv-pay-st"></p>'
            '<div class="wv-pay-ctas"><button type="button" class="wv-sim">Simulate customer payment (prototype)</button>'
            '<button type="button" class="wv-resend">Resend Payment Link</button>'   # DISC-463: OPS resends the link on the customer's request
            '<button type="button" class="wv-depledge" disabled>Initiate De-pledge</button></div>'
            # DISC-453: Treasury confirms the payment – Approve (received) or Reject (not received); LMS enables the de-pledge when the balance payable is ₹0
            '<div class="wv-tc" hidden><h4>Treasury – payment confirmation</h4>'
            '<p class="wv-hint">Cross-check that the payment is received, then approve or reject.</p>'
            '<div class="wv-appr-ctas"><button type="button" class="wv-tc-rej">Reject – payment not received</button>'
            '<button type="button" class="wv-confirm">Approve – payment received</button></div></div>'
            '<p class="wv-hint wv-dp-hint">De-pledge is enabled once Treasury approves the payment (the balance payable is then ₹0).</p></div>'
            + pop('wv-pr', '<h3>Are you sure you want to reject the application with the selected waive-off?</h3>' '<p class="wv-ptype"></p>'
                  f'<p class="wv-ps-txt">The request will be sent to {ck} (Checker) for approval.</p>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No</button><button type="button" class="wv-yes-r">Yes, submit</button></div>')
            + pop('wv-pk', '<h3>Are you sure you want to accept the rejection with the selected waive-off?</h3>' '<p class="wv-ptype"></p>'
                  f'<p class="wv-ps-txt">The request will be sent to {tr} for approval.</p>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No</button><button type="button" class="wv-yes-k">Yes, accept</button></div>')
            + pop('wv-pa', '<h3>This action is irreversible. Are you sure you want to proceed?</h3>' '<p class="wv-ptype"></p>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No</button><button type="button" class="wv-yes-a">Yes</button></div>')
            + pop('wv-pd', '<h3>Are you sure you want to decline the rejection? The waive-off and rejection request will be cancelled.</h3>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No</button><button type="button" class="wv-yes-d">Yes, decline</button></div>')
            + pop('wv-prs', '<h3>Are you sure you want to send the payment link to the customer again?</h3>'
                  '<p class="wv-ps-txt">The customer gets the payment reminder SMS and mail with the same payment link.</p>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No</button><button type="button" class="wv-yes-rs">Yes, send</button></div>')
            + pop('wv-pn', '<h3>Are you sure the payment is not received? The payment will be rejected.</h3>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No</button><button type="button" class="wv-yes-n">Yes, reject</button></div>')
            + pop('wv-pc', '<h3>Are you sure you want to confirm the payment received from the customer?</h3>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No</button><button type="button" class="wv-yes-c">Yes, confirm</button></div>')
            + '</div>')


AUDIT_NAME = {"Processing Fee*": "Processing fee charge", "Processing Fee": "Processing fee charge", "Lien Marking Charges": "Pledge charge",
              "Lien Removal Charges": "Collateral release charge", "Stamp Duty Charges": "Stamp duty charge"}


def _aud(ts, msg, approved="-", init="System", at=None, note="-"):
    """One Audit entry in the LMS style: “date, time ▸ message”, opens to Approved by / Initiated by (DISC-340)."""
    at = at or ts
    return (f'<details class="aud"><summary><span class="aud-t">{ts}</span><span class="aud-m">{msg}</span></summary>'
            f'<p>→ Approved by {approved}</p><p>→ Initiated by “{init}” at “{at}” - “{note}”</p></details>')


def draft_documents(r):
    """Draft LAN Documents tab (DISC-351): the charges payment receipt is added here when the customer pays (LOS)."""
    return ('<p class="lms-new">The charges payment receipt is new (Waiver BRD) – not in the live LMS yet.</p>'
            '<table class="lms-table doc-table"><thead><tr><th>Document</th><th>Reference</th><th>Uploaded on</th><th>Uploaded by</th><th></th></tr></thead>'
            '<tbody><tr class="doc-none"><td colspan="5">No documents yet.</td></tr></tbody></table>')


def draft_audit(r):
    k = START["draft"] - int(r["LAN"][-2:])
    sc = 2 if k < 4 else 3 if k < 7 else 4
    d = r["Generated"]
    items = [_aud(f"{d}, 11:{20 - i:02d}:{10 + i * 7:02d}", f"{AUDIT_NAME[n]} of ₹{a:,.2f} has been incurred")
             for i, (n, a) in enumerate(reversed(DRAFT_CHARGES[sc]))]
    items.append(_aud(f"{d}, 11:05:42", "Application created in DRAFT"))
    return ('<p class="lms-new">Waive-off and rejection entries are new (Waiver BRD) – not in the live LMS yet.</p>'
            f'<div class="aud-list">{"".join(items)}</div>'
            '<div class="lms-pager"><span></span><span class="lms-pp"><span class="lms-select">10 <i>⌄</i></span> rows/page '
            '<span class="lms-pg">‹</span><span class="lms-pg">›</span></span></div>')


WAIVER_JS = """<script>
/* Draft loan Approvals tab (DISC-361, DISC-362 – maker → checker → Treasury). Waive-off and rejection are one request: tick a charge → amount to waive (≤ the charge) →
   reason (note) → Reject → confirm → pending Treasury approval. Treasury Approve (irreversible pop-up) → the waive-off is applied
   (Waived off Charges), LAN → REJECTED, customer communication, charges payment. Treasury Decline (remark) → request cancelled,
   LAN stays DRAFT, OPS can submit a new request. Every step is written to the Audit tab. */
(function () {
  var r2 = function (v) { return Math.round(v * 100) / 100; };
  var f = function (v) { return '₹' + r2(v).toLocaleString('en-IN', { maximumFractionDigits: 2 }); };
  var f2 = function (v) { return '₹' + r2(v).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  var now = function () { var d = new Date(), p = function (x) { return String(x).padStart(2, '0'); };
    return p(d.getDate()) + '-' + p(d.getMonth() + 1) + '-' + d.getFullYear() + ' ' + p(d.getHours()) + ':' + p(d.getMinutes()); };
  function calc(w) {
    var tw = 0, bal = 0, pend = 0, chg = 0, done = 0;
    w.querySelectorAll('tbody tr').forEach(function (tr) {
      var a = tr.querySelector('.wv-amt'), max = +a.dataset.max, v = +a.value || 0;
      if (v > max) { a.value = max; v = max; } if (v < 0) { a.value = 0; v = 0; }
      tw += v; bal += max; chg += +tr.dataset.chg; done += +tr.dataset.done; tr.querySelector('.wv-pay').textContent = f(max - v);
      if (tr.querySelector('.wv-chk').checked && v > 0) pend++;
    });
    var after = bal - tw, orig = +w.dataset.orig;
    w.querySelector('.wv-ctot').textContent = f(chg); w.querySelector('.wv-dtot').textContent = f(done); w.querySelector('.wv-wtot').textContent = f(tw); w.querySelector('.wv-ptot').textContent = f(after);
    var t = after <= 0 ? 'Full waive-off' : after < orig ? 'Partial waive-off' : 'No waive-off';
    w.querySelector('.wv-type b').textContent = t;
    w.querySelector('.wv-allgone').hidden = bal > 0;          // DISC-346: fully waived charges stay in the table
    return { tw: tw, tp: after, type: t };
  }
  function stamp() { var d = new Date(), p = function (x) { return String(x).padStart(2, '0'); };
    return p(d.getDate()) + '/' + p(d.getMonth() + 1) + '/' + d.getFullYear() + ', ' + p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds()); }
  var AN = { 'Processing Fee*': 'Processing fee charge', 'Processing Fee': 'Processing fee charge', 'Lien Marking Charges': 'Pledge charge',
             'Lien Removal Charges': 'Collateral release charge', 'Stamp Duty Charges': 'Stamp duty charge' };
  function audit(w, msg, note, by, appr) {   /* LMS-style Audit entry: “date, time ▸ message” → Approved by / Initiated by (DISC-340) */
    var list = w.closest('.lms-lanpage').querySelector('.aud-list'); if (!list) return;
    var ts = stamp(), el = document.createElement('details'); el.className = 'aud new';
    el.innerHTML = '<summary><span class="aud-t"></span><span class="aud-m"></span></summary><p class="aud-a"></p><p class="aud-i"></p>';
    el.querySelector('.aud-a').textContent = '→ Approved by ' + (appr || '-');
    el.querySelector('.aud-t').textContent = ts; el.querySelector('.aud-m').textContent = msg;
    el.querySelector('.aud-i').textContent = '→ Initiated by “' + (by || 'OPS user') + '” at “' + ts + '” - “' + (note || '-') + '”';
    list.prepend(el);
  }
  var show = function (w, c, on) { var pp = w.querySelector(c); pp.hidden = !on;
    var ty = pp.querySelector('.wv-ptype');            /* DISC-363: the reconfirmation shows the type of waive-off */
    if (on && ty) { var q = calc(w); ty.innerHTML = 'Type of waive-off: <b>' + q.type + '</b><br>Amount to be waived off: <b>' + f(q.tw) +
      '</b> · Payable charges: <b>' + f(q.tp) + '</b>'; } };
  var amts = function (w) { return Array.prototype.map.call(w.querySelectorAll('tbody .wv-amt'), function (x) { return (+x.value || 0).toFixed(2); }).join('|'); };
  var setSt = function (w, t) { w.closest('.lms-lanpage').querySelector('.lms-lanhead .lms-st').textContent = t; };
  document.addEventListener('change', function (e) {
    var w = e.target.closest('.wv'); if (!w) return;
    if (e.target.classList.contains('wv-all'))
      w.querySelectorAll('tbody .wv-chk:not(:disabled)').forEach(function (c) { c.checked = e.target.checked; c.dispatchEvent(new Event('change', { bubbles: true })); });
    if (e.target.classList.contains('wv-chk')) { var a = e.target.closest('tr').querySelector('.wv-amt'); a.disabled = !e.target.checked; if (!e.target.checked) a.value = 0;
      if (e.target.closest('tr').dataset.fixed) { a.disabled = true; a.value = e.target.checked ? a.dataset.max : 0; } }   /* DISC-400: full waive-off only */
    calc(w);
  });
  document.addEventListener('change', function (e) {     /* show the chosen file name under the upload box */
    if (e.target.classList.contains('wv-file') || e.target.classList.contains('wv-cfile')) {
      var fn = e.target.closest('.wv-drop').nextElementSibling; fn.textContent = e.target.files.length ? '📎 ' + e.target.files[0].name : '';
      var w0 = e.target.closest('.wv'); if (w0) w0.querySelector(e.target.classList.contains('wv-file') ? '.wv-err' : '.wv-cerr').textContent = ''; }
  });
  document.addEventListener('input', function (e) { var w = e.target.closest('.wv'); if (w && e.target.classList.contains('wv-amt')) calc(w); });
  document.addEventListener('click', function (e) {
    var w = e.target.closest('.wv'), c = e.target.classList; if (!w) return;
    if (c.contains('wv-x') || c.contains('wv-no') || c.contains('wv-ok')) e.target.closest('.wv-pop').hidden = true;
    if (c.contains('wv-reject')) {          /* maker – note and file required */
      var err = w.querySelector('.wv-err'), m = [];
      if (!w.querySelector('.wv-note').value.trim()) m.push('add the note');
      if (!w.querySelector('.wv-file').files.length) m.push('upload a file');
      if (m.length) { err.textContent = 'Please ' + m.join(' and ') + '.'; return; }
      err.textContent = ''; show(w, '.wv-pr', true);
    }
    if (c.contains('wv-yes-r')) {          /* maker submits → checker */
      show(w, '.wv-pr', false); var q = calc(w), note = w.querySelector('.wv-note').value.trim(), ts = stamp();
      w.dataset.mkAmts = amts(w);
      w.querySelectorAll('.wv-note, .wv-file, .wv-reject').forEach(function (x) { x.disabled = true; });
      var ck = w.querySelector('.wv-ck'); ck.hidden = false; w.querySelector('.wv-cerr').textContent = '';
      ck.querySelector('.wv-ck-st').innerHTML = 'Submitted by <b>' + w.dataset.mk + ' (Maker)</b> on ' + ts + '. Type of waive-off: <b>' + q.type +
        '</b>. Amount to be waived off: <b>' + f(q.tw) + '</b>. Payable charges: <b>' + f(q.tp) + '</b>.<br>Rejection reason: <span class="wv-rsn"></span>' +
        '<br>Mail sent to ' + w.dataset.ck + ': <i>Checker Approval Required – Waive-off &amp; Rejection</i>.';
      ck.querySelector('.wv-rsn').textContent = note;
      setSt(w, 'Draft – Pending ' + w.dataset.ck + ' approval');
      audit(w, 'Waive-off and rejection submitted by ' + w.dataset.mk + ' (Maker) for ' + w.dataset.ck + ' (Checker) approval (' + q.type.toLowerCase() +
            '; amount to be waived off ' + f2(q.tw) + '; charges payable ' + f2(q.tp) + ')', note, w.dataset.mk + ' user', '-');
    }
    if (c.contains('wv-ck-app')) {          /* checker – a change needs the note and a file */
      var ce = w.querySelector('.wv-cerr'), changed = amts(w) !== w.dataset.mkAmts, m2 = [];
      if (!w.querySelector('.wv-cnote').value.trim()) m2.push('add the note');          /* DISC-365: the checker note is always mandatory */
      if (changed && !w.querySelector('.wv-cfile').files.length) m2.push('upload a file');
      if (m2.length) { ce.textContent = (changed ? 'The amounts were changed – please ' : 'Please ') + m2.join(' and ') + '.'; return; }
      ce.textContent = ''; w.dataset.changed = changed ? '1' : ''; show(w, '.wv-pk', true);
    }
    if (c.contains('wv-yes-k')) {          /* checker approves → Treasury */
      show(w, '.wv-pk', false); var q = calc(w), cn = w.querySelector('.wv-cnote').value.trim(), ts2 = stamp(), chg = !!w.dataset.changed;
      w.querySelectorAll('.wv-table input, .wv-cnote, .wv-cfile, .wv-ck-app, .wv-ck-dec').forEach(function (x) { x.disabled = true; });
      show(w, '.wv-ck', false);
      var ap = w.querySelector('.wv-appr'); ap.hidden = false; w.querySelector('.wv-terr').textContent = '';
      ap.querySelector('.wv-appr-st').innerHTML = 'Maker: <b>' + w.dataset.mk + '</b>. Approved by <b>' + w.dataset.ck + ' (Checker)</b> on ' + ts2 +
        (chg ? ' – <b>amounts changed by the checker</b>' : '') + '. Type of waive-off: <b>' + q.type + '</b>. Amount to be waived off: <b>' + f(q.tw) +
        '</b>. Payable charges: <b>' + f(q.tp) + '</b>.<br>Rejection reason: <span class="wv-rsn"></span>' +
        (cn ? '<br>Checker note: <span class="wv-cn"></span>' : '') + '<br>Mail sent to ' + w.dataset.tr + ': <i>Approval Required – Waive-off &amp; Rejection</i>.';
      ap.querySelector('.wv-rsn').textContent = w.querySelector('.wv-note').value.trim(); if (cn) ap.querySelector('.wv-cn').textContent = cn;
      setSt(w, 'Draft – Pending ' + w.dataset.tr + ' approval');
      audit(w, 'Waive-off and rejection approved by ' + w.dataset.ck + ' (Checker)' + (chg ? ' with changes' : '') + ' and sent for ' + w.dataset.tr +
            ' approval (' + q.type.toLowerCase() + '; amount to be waived off ' + f2(q.tw) + '; charges payable ' + f2(q.tp) + ')', cn, w.dataset.ck + ' user', w.dataset.ck + ' user');
    }
    if (c.contains('wv-ck-dec')) {
      var ce2 = w.querySelector('.wv-cerr');
      if (!w.querySelector('.wv-cnote').value.trim()) { ce2.textContent = 'Please add the note to decline.'; return; }
      ce2.textContent = ''; w.dataset.dec = 'ck'; show(w, '.wv-pd', true);
    }
    if (c.contains('wv-decline')) {
      var te = w.querySelector('.wv-terr');
      if (!w.querySelector('.wv-tnote').value.trim()) { te.textContent = 'Please add the note to decline.'; return; }
      te.textContent = ''; w.dataset.dec = 'tr'; show(w, '.wv-pd', true);
    }
    if (c.contains('wv-yes-d')) {          /* checker or Treasury declines – the request is cancelled, the LAN stays DRAFT */
      show(w, '.wv-pd', false); var who = w.dataset.dec === 'ck' ? w.dataset.ck + ' (Checker)' : w.dataset.tr,
        rm = w.querySelector(w.dataset.dec === 'ck' ? '.wv-cnote' : '.wv-tnote').value.trim();
      audit(w, 'Waive-off and rejection request declined by ' + who + ' – request cancelled; LAN stays in DRAFT', rm,
            (w.dataset.dec === 'ck' ? w.dataset.ck : w.dataset.tr) + ' user', '-');
      w.querySelectorAll('tbody tr').forEach(function (tr) { var ck = tr.querySelector('.wv-chk'), am = tr.querySelector('.wv-amt');
        ck.checked = false; ck.disabled = false; am.value = 0; am.disabled = true; });
      w.querySelector('.wv-all').checked = false; w.querySelector('.wv-all').disabled = false;
      w.querySelectorAll('.wv-note, .wv-file, .wv-reject, .wv-cnote, .wv-cfile, .wv-ck-app, .wv-ck-dec').forEach(function (x) { x.disabled = false; });
      w.querySelectorAll('.wv-note, .wv-cnote, .wv-tnote, .wv-file, .wv-cfile').forEach(function (x) { x.value = ''; });
      w.querySelectorAll('.wv-fname').forEach(function (x) { x.textContent = ''; });
      show(w, '.wv-ck', false); show(w, '.wv-appr', false); calc(w); setSt(w, 'Draft');
      var d0 = w.querySelector('.wv-done'); d0.hidden = false; d0.className = 'wv-done wv-cancel';
      d0.innerHTML = '<b>Request declined by ' + who + ' – cancelled.</b> LAN status stays DRAFT; nothing is waived. Mail sent to the maker: <i>Waive-off Request Declined</i>. The maker can submit a new request.';
    }
    if (c.contains('wv-approve')) {          /* DISC-373: the Treasury note is mandatory to approve too */
      if (!w.querySelector('.wv-tnote').value.trim()) { w.querySelector('.wv-terr').textContent = 'Please add the note.'; return; }
      show(w, '.wv-pa', true); }
    if (c.contains('wv-yes-a')) {          /* Treasury approves – waive-off and rejection applied together */
      show(w, '.wv-pa', false); var note2 = w.querySelector('.wv-note').value.trim();
      w.querySelectorAll('tbody tr').forEach(function (tr) {
        var a = tr.querySelector('.wv-amt'), max = +a.dataset.max, v = Math.min(+a.value || 0, max);
        if (v <= 0) return;
        var left = r2(max - v);
        audit(w, (AN[tr.dataset.name] || tr.dataset.name) + ' of ' + f2(v) + ' has been waived off (' + (left > 0 ? 'partial' : 'full') +
                 ' waive-off); balance ' + f2(left), note2, w.dataset.mk + ' user', w.dataset.ck + ' user, ' + w.dataset.tr + ' user');
        a.dataset.max = left; a.value = 0; tr.dataset.done = r2(+tr.dataset.done + v);
        tr.querySelector('.wv-done-amt').textContent = f(+tr.dataset.done);
      });
      var q = calc(w); w.classList.add('closed'); show(w, '.wv-appr', false);
      w.querySelectorAll('input, textarea, .wv-reject').forEach(function (x) { x.disabled = true; });
      audit(w, 'Application rejected – LAN status changed from DRAFT to REJECTED (' + q.type.toLowerCase() + '; charges payable ' + f2(q.tp) + ')',
            note2, w.dataset.mk + ' user', w.dataset.ck + ' user, ' + w.dataset.tr + ' user');
      var d = w.querySelector('.wv-done'); d.hidden = false; d.className = 'wv-done';
      d.innerHTML = '<b>Rejection accepted by ' + w.dataset.ck + ' (Checker) and ' + w.dataset.tr + ' – application rejected.</b> LAN status: REJECTED. Type of waive-off: <b>' + q.type + '</b>. ' +
        'Mail sent to OPS and Treasury: <i>Waive-off &amp; Rejection Approved</i>. ' +
        (q.tp > 0 ? 'Payable charges ' + f(q.tp) + ' – rejection SMS and mail with the payment link sent to the customer; de-pledge after payment and Treasury confirmation.'
                  : 'Nothing payable – rejection SMS and mail sent without a payment link; the units can be de-pledged now.');
      var st = w.closest('.lms-lanpage').querySelector('.lms-lanhead .lms-st'); st.textContent = 'Rejected'; st.className = 'lms-st st-rejected';
      /* DISC-351: charges payment block – payable: wait for the customer's payment; nothing payable: de-pledge now */
      var pb = w.querySelector('.wv-pay-box'); pb.hidden = false; w.dataset.due = q.tp;
      pb.querySelectorAll('button').forEach(function (x) { x.disabled = false; });
      if (q.tp > 0) {
        pb.querySelector('.wv-pay-st').innerHTML = 'Awaiting the customer’s payment of <b>' + f(q.tp) + '</b> – payment link sent (SMS and mail). Full payment only.';
        pb.querySelector('.wv-depledge').disabled = true;
      } else {
        pb.querySelector('.wv-pay-st').innerHTML = 'Nothing payable (full waive-off) – the units can be de-pledged now.';
        pb.querySelector('.wv-sim').hidden = true; pb.querySelector('.wv-dp-hint').hidden = true; pb.querySelector('.wv-resend').hidden = true;
      }
    }
    if (c.contains('wv-sim')) {          /* the customer pays in the LOS – LMS gets the payment, receipt and UNO entries */
      var pb2 = w.querySelector('.wv-pay-box'), amt = f2(+w.dataset.due), ts = stamp();
      pb2.querySelector('.wv-pay-st').innerHTML = '<b>Payment received:</b> ' + amt + ' on ' + ts + ' · Transaction ID pay_SCCL7Q2X9K4M1B · ' +
        'Receipt RCPT/LAMF/2026/11/0149 (Documents tab) · UNO entries posted.<br>Mail sent to Treasury, Cc OPS: <i>Charges Payment Received</i> – ' +
        'please confirm the payment. <b>Pending Treasury confirmation.</b>';
      e.target.hidden = true; pb2.querySelector('.wv-tc').hidden = false; pb2.querySelector('.wv-resend').disabled = true;
      audit(w, 'Charges payment of ' + amt + ' received from the customer (pay_SCCL7Q2X9K4M1B); receipt RCPT/LAMF/2026/11/0149 generated', '-', 'System', '-');
      var docs = w.closest('.lms-lanpage').querySelector('.doc-table tbody');
      if (docs) { var nd = docs.querySelector('.doc-none'); if (nd) nd.remove();
        var tr = document.createElement('tr'); tr.className = 'doc-new';
        tr.innerHTML = '<td>Charges Payment Receipt</td><td>RCPT/LAMF/2026/11/0149</td><td></td><td>System</td>' +
          '<td><a href="charges-receipt.html" target="_blank" rel="noopener">View</a></td>';
        tr.children[2].textContent = ts; docs.prepend(tr); }
    }
    if (c.contains('wv-resend')) show(w, '.wv-prs', true);
    if (c.contains('wv-yes-rs')) {         /* DISC-463: OPS resends the payment link (same link, reminder SMS and mail) */
      show(w, '.wv-prs', false);
      w.querySelector('.wv-pay-st').insertAdjacentHTML('beforeend', '<br><b>Payment link sent again</b> on ' + stamp() +
        ' – reminder SMS and mail with the same link sent to the customer.');
      audit(w, 'Payment link for ' + f2(+w.dataset.due) + ' resent to the customer (reminder SMS and mail)', '-', w.dataset.mk + ' user', '-');
    }
    if (c.contains('wv-confirm')) show(w, '.wv-pc', true);
    if (c.contains('wv-yes-c')) {          /* Treasury approves – payment received; LMS enables the de-pledge when the balance payable is ₹0 (DISC-453) */
      show(w, '.wv-pc', false); var pb3 = w.querySelector('.wv-pay-box'), bal = 0, en = bal <= 0;   /* the full amount is paid in one payment */
      pb3.querySelector('.wv-pay-st').innerHTML = pb3.querySelector('.wv-pay-st').innerHTML.replace('<b>Pending Treasury confirmation.</b>', '');
      pb3.querySelector('.wv-pay-st').insertAdjacentHTML('beforeend', '<br><b>Payment approved by Treasury</b> (received) on ' + stamp() + '. ' +
        (en ? 'Balance payable ₹0 – De-pledge enabled. Mail sent to OPS, Cc Treasury: <i>Charges Received – Initiate De-pledge</i>.'
            : 'An amount is still payable – De-pledge not enabled.'));
      pb3.querySelector('.wv-tc').hidden = true; pb3.querySelector('.wv-depledge').disabled = !en; pb3.querySelector('.wv-dp-hint').hidden = en; pb3.querySelector('.wv-resend').hidden = true;
      audit(w, 'Charges payment of ' + f2(+w.dataset.due) + ' approved by Treasury (received)' + (en ? '; de-pledge enabled' : '; de-pledge not enabled'), '-', 'Treasury user', 'Treasury user');
    }
    if (c.contains('wv-tc-rej')) show(w, '.wv-pn', true);
    if (c.contains('wv-yes-n')) {          /* Treasury rejects – payment not received; the customer can pay again (DISC-452) */
      show(w, '.wv-pn', false); var pb5 = w.querySelector('.wv-pay-box');
      pb5.querySelector('.wv-pay-st').innerHTML = pb5.querySelector('.wv-pay-st').innerHTML.replace('<b>Pending Treasury confirmation.</b>', '');
      pb5.querySelector('.wv-pay-st').insertAdjacentHTML('beforeend', '<br><b>Payment rejected by Treasury</b> (not received) on ' + stamp() +
        '. De-pledge stays disabled; the amount is still payable. Mail sent to OPS, Cc Treasury.');
      pb5.querySelector('.wv-tc').hidden = true; pb5.querySelector('.wv-depledge').disabled = true; pb5.querySelector('.wv-sim').hidden = false; pb5.querySelector('.wv-resend').disabled = false;
      audit(w, 'Charges payment of ' + f2(+w.dataset.due) + ' rejected by Treasury (not received)', '-', 'Treasury user', 'Treasury user');
    }
    if (c.contains('wv-depledge')) {
      var pb4 = w.querySelector('.wv-pay-box'); e.target.disabled = true; e.target.textContent = 'De-pledge initiated';
      pb4.querySelector('.wv-pay-st').insertAdjacentHTML('beforeend', '<br><b>De-pledge initiated</b> on ' + stamp() + '.');
      audit(w, 'De-pledge of the pledged Mutual Fund units initiated', '-');
    }
  });
})();
</script>"""


def lan_detail(view, r):
    amt = _num(r["Sanction Amount"])
    live = view in ("active", "closed")
    disb = round(amt * 0.48 / 100) * 100 if (amt and live) else None
    dp = amt * 1.0003 if amt else None
    fields = [
        ("LSP", r["Source"]), ("Sanctioned Amount", _rs(amt)), ("Drawing Power", _rs(dp, True) if dp else "-"),
        ("Disbursed Amount", _rs(disb) if live else "-"),
        ("Repaid Amount", "₹0" if live else "-"), ("Principal Outstanding", _rs(disb) if live else "-"),
        ("Available for Disbursement", _rs(amt - disb) if (live and amt) else "-"),
        ("Utilized Drawing Power", f'<span class="ok">{disb / dp * 100:.2f}% ▲</span>' if (live and amt) else "-"),
        ("Repayments", '<span class="ok">On time</span>' if view == "active" else "-"), ("Deduction Date", "5th, Monthly"),
        ("Repayment Type", "Interest Only"), ("Disbursement Type", "Revolving"),
        ("Rate of Interest", r["Rate of Interest"]), ("Processing Fee", _rs(amt * 0.0187, True) if amt else "-"),
        ("Tenure", "36 months"), ("Product Name", f'<span class="lnk">{r["Product Id"]}</span>'),
        ("Application Start Date", r["Generated"]), ("Application Submitted Date", r["Generated"] if view not in ("draft", "inactive") else "-"),
        ("Loan Start Date", r["Start Date"]), ("Loan End Date", r["End Date"]),
    ]
    if view == "draft":   # as in the LMS draft loan page (DISC-330): nothing sanctioned yet
        D = dict(fields)
        for k in ("Sanctioned Amount", "Drawing Power", "Disbursed Amount", "Repaid Amount", "Principal Outstanding",
                  "Available for Disbursement", "Utilized Drawing Power", "Repayments", "Processing Fee",
                  "Application Submitted Date", "Loan Start Date", "Loan End Date"):
            D[k] = "-"
        D["Disbursement Type"], D["Tenure"] = "Multiple", "12 months"
        fields = list(D.items())
    fields = [(k, v + ' <i class="lms-i" title="Breakup">ⓘ</i>' if k == "Processing Fee" else v) for k, v in fields]
    grid = "".join(f'<div><span>{k}</span><b>{v}</b></div>' for k, v in fields)
    coll = "".join(f'<div><span>{k}</span><b>Collected: {c}<br>Due: ₹0<br>Overdue: ₹0</b></div>'
                   for k, c in [("Interest", "₹0"), ("Principal", "₹0"), ("Charges", _rs(amt * 0.0187, True) if (live and amt) else "₹0")])
    status = r.get("Status") or "Rejected"
    risk = f'<span class="lms-risk">{r["Risk Level"]}</span>' if view == "active" else ""
    tid = f'{view}-{r["LAN"]}'
    tab_list = TABS   # Draft: Approvals tab after Overview, as per the Waiver BRD (DISC-337, replaces DISC-330)
    tabs = "".join(f'<input type="radio" name="t-{tid}" id="t-{tid}-{k}"{" checked" if k == 0 else ""}>'
                   f'<label for="t-{tid}-{k}">{t}</label>' for k, t in enumerate(tab_list))
    panes = ('<div class="lms-pane p0"><div class="lms-card2"><h3>Loan Details</h3><div class="lms-grid">' + grid + '</div></div>'
             '<div class="lms-card2"><h3>Collection Details</h3><div class="lms-grid g3">' + coll + '</div></div></div>'
             + "".join(f'<div class="lms-pane p{k}">{draft_approvals(r, tid) if (view == "draft" and k == 1) else active_approvals(r) if (view == "active" and k == 1) else draft_audit(r) if (view == "draft" and tab_list[k] == "Audit") else draft_documents(r) if (view == "draft" and tab_list[k] == "Documents") else TBA}</div>'
                       for k in range(1, len(tab_list))))
    return (f'<section id="lan-{tid}" class="lms-sec lms-lanpage"><div class="lms-lanhead"><a class="lms-back" href="#m-loans-{view}" '
            f'title="Back to the list">←</a><h2>LAN Number: {r["LAN"]}</h2><span class="lms-st st-{status.lower()}">{status}</span>{risk}'
            f'<span class="lms-vs">View status</span>{active_menu(r) if view == "active" else ""}</div><div class="lms-tabs">{tabs}{panes}</div>'
            '<p class="lms-sample">Sample data for the prototype – not real customers.</p></section>')


# ---- Active loan: ≡ menu at the top right of the LAN page → Waive-off page (DISC-366) – as in the LMS UAT screens
MENU = ["Disbursal", "Repayment", "Soft Freeze", "Hard Freeze", "Unfreeze", "De-Pledge Assets", "Liquidate Assets", "Change ROI",
        "Foreclose", "Waive-off", "Add Credit Note"]


def active_menu(r):
    items = "".join(f'<a class="lms-mi" href="#waive-active-{r["LAN"]}">{m}</a>' if m == "Waive-off"
                    else f'<span class="lms-mi{" off" if m == "Unfreeze" else ""}">{m}</span>' for m in MENU)
    return ('<span class="lms-sim">Go to Simulator</span><details class="lms-menu"><summary title="Menu">☰</summary>'
            f'<div class="lms-menu-list">{items}</div></details>')


def active_waive(r):
    """Active LAN Waive-off page (DISC-366 / DISC-421 / DISC-422 / DISC-431): opened from the ≡ menu; the waive-off table (same as the
    Approvals tab), Add a note and Upload a file (both mandatory for the maker) and the Waive-off button. Full or partial waive-off only;
    nothing selected = no waive-off (no request). On “Yes, Waive Off” the standalone request goes to the Approvals tab of the LAN, where the checker and Treasury approve or decline."""
    mk, ck, tr = "OPS L1", "OPS L2 / OPS L3", "Treasury L1 / L2 / L3"
    rows = _SPLIT + [("Bounce Charges", 118), ("Annual Maintenance Charges (AMC)", 1178.82)]
    body = "".join(f'<tr data-name="{n}" data-chg="{a}" data-done="0"{FX if n in FIXED else ""}><td><input type="checkbox" class="wa-chk" aria-label="Select {n}"></td><td>{n}</td>'
                   f'<td class="num">₹{_amt(a)}</td><td class="num wa-dn">₹0</td><td><input class="wa-amt" type="number" min="0" step="0.01" value="0" '
                   f'data-max="{a}" disabled></td><td class="num wa-bal">₹{_amt(a)}</td></tr>' for n, a in rows)
    tot = sum(a for _, a in rows)
    pop = lambda cls, b: f'<div class="wv-pop {cls}" hidden><div class="wv-box"><button type="button" class="wv-x" aria-label="Close">×</button>{b}</div></div>'
    return (f'<section id="waive-active-{r["LAN"]}" class="lms-sec lms-lanpage"><div class="lms-lanhead"><a class="lms-back" '
            f'href="#lan-active-{r["LAN"]}" title="Back to the LAN">←</a><h2>Waive-off</h2></div>'
            f'<div class="wa" data-lan="{r["LAN"]}" data-mk="{mk}" data-ck="{ck}" data-tr="{tr}"><p class="lms-new">Waive-off (Waiver BRD) – '
            'not in the live LMS yet. The request is approved in the Approvals tab of the LAN.</p>'
            '<div class="wv-head"><span></span><button type="button" class="wv-waive wa-btn" disabled>Waive-off</button></div>'
            '<table class="lms-table wv-table wa-table"><thead><tr><th><input type="checkbox" class="wa-all" aria-label="Select all"></th><th>Charges Name</th>'
            '<th class="num">Amount of Charges</th><th class="num">Waived off Charges</th><th>Amount to be waived off</th><th class="num">Payable Charges</th></tr></thead>'
            f'<tbody>{body}</tbody><tfoot><tr><td></td><td><b>Total</b></td><td class="num"><b>₹{_amt(tot)}</b></td><td class="num"><b class="wa-dtot">₹0</b></td>'
            f'<td><b class="wa-wtot">₹0</b></td><td class="num"><b class="wa-ptot">₹{_amt(tot)}</b></td></tr></tfoot></table>'
            f'<p class="wv-hint">{FOOT} Only full or partial waive-off – if nothing is selected, there is no waive-off and no request.</p>'
            '<label class="wv-lbl">Add a note <span>(required – reason for the waive-off)</span></label>'
            '<textarea class="wv-note wa-note" rows="2" placeholder="Add a note"></textarea>'
            '<label class="wv-lbl">Upload a file <span>(required)</span></label>'
            '<label class="wv-drop">Drop files here or <u>click</u><input type="file" class="wa-file" hidden></label><p class="wv-fname"></p>'
            '<p class="wv-hint">PDF, PNG or JPG. Max 5MB</p><p class="wv-err wa-err"></p>'
            '<p class="wa-msg" hidden></p>'
            + pop('wa-pw', '<h3>Are you sure you want to waive off the selected charges?</h3><p class="wv-ptype"></p>'
                  f'<p class="wv-ps-txt">The request will go to the Approvals tab for {ck} (Checker) and {tr} approval.</p>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No, Don’t Waive Off</button><button type="button" class="wa-yes">Yes, Waive Off</button></div>')
            + '</div><p class="lms-sample">Sample data for the prototype – not real customers. Same table as the Approvals tab.</p></section>')


def active_approvals(r):
    """Approvals tab of an ACTIVE LAN (DISC-422): the standalone waive-off request raised on the Waive-off page – the checker and Treasury
    approve or decline it here, each with a note."""
    ck, tr = "OPS L2 / OPS L3", "Treasury L1 / L2 / L3"
    pop = lambda cls, b: f'<div class="wv-pop {cls}" hidden><div class="wv-box"><button type="button" class="wv-x" aria-label="Close">×</button>{b}</div></div>'
    return (f'<div class="wa-ap" data-lan="{r["LAN"]}"><p class="lms-new">Waive-off approval (Waiver BRD) – not in the live LMS yet.</p>'
            '<h3>Waive-off request</h3><p class="wa-none">No waive-off request pending. OPS maker raises it from ≡ → Waive-off.</p>'
            '<div class="wa-req" hidden><p class="wa-req-st"></p><table class="lms-table wa-req-t"><thead><tr><th>Charges Name</th>'
            '<th class="num">Amount of Charges</th><th class="num">Amount to be waived off</th><th class="num">Payable Charges</th></tr></thead><tbody></tbody></table></div>'
            f'<div class="wv-ck wa-ck" hidden><h3>Pending {ck} (Checker) approval</h3>'
            '<label class="wv-lbl">Checker note <span>(required)</span></label><textarea class="wv-cnote wa-cnote" rows="2" placeholder="Add a note"></textarea>'
            '<p class="wv-cerr wa-cerr"></p><div class="wv-appr-ctas"><button type="button" class="wv-ck-dec wa-ck-dec">Decline</button>'
            f'<button type="button" class="wv-ck-app wa-ck-app">Approve</button></div><p class="wv-hint">{ck} only.</p></div>'
            f'<div class="wv-appr wa-tr" hidden><h3>Pending {tr} approval</h3>'
            '<label class="wv-lbl">Treasury note <span>(required)</span></label><textarea class="wv-tnote wa-tnote" rows="2" placeholder="Add a note"></textarea>'
            '<p class="wv-terr wa-terr"></p><div class="wv-appr-ctas"><button type="button" class="wv-decline wa-dec">Decline</button>'
            f'<button type="button" class="wv-approve wa-app">Approve</button></div><p class="wv-hint">{tr} only.</p></div>'
            '<div class="wv-done wa-done" hidden></div>'
            + pop('wa-pa', '<h3>This action is irreversible. Are you sure you want to proceed?</h3>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No</button><button type="button" class="wv-yes-a wa-yes-a">Yes</button></div>')
            + pop('wa-pd', '<h3>Are you sure you want to decline? The waive-off request will be cancelled.</h3>'
                  '<div class="wv-pbtns"><button type="button" class="wv-no">No</button><button type="button" class="wv-yes-d wa-yes-d">Yes, decline</button></div>')
            + '</div>')


WAIVE_ACTIVE_JS = """<script>
/* ACTIVE loan waive-off (DISC-422 / DISC-431): Waive-off page = table + maker note and file (mandatory) + Waive-off button; the request goes to the Approvals tab
   of the LAN, where the checker (note) and Treasury (note, irreversible pop-up) approve or decline it. Full or partial only. */
(function () {
  var r2 = function (v) { return Math.round(v * 100) / 100; };
  var f = function (v) { return '₹' + r2(v).toLocaleString('en-IN', { maximumFractionDigits: 2 }); };
  var Q = function (w, c) { return w.querySelector(c); };
  var W = function (lan) { return document.querySelector('.wa[data-lan="' + lan + '"]'); };
  var A = function (lan) { return document.querySelector('.wa-ap[data-lan="' + lan + '"]'); };
  function calc(w) { var tw = 0, n = 0, bal = 0, dn = 0;
    w.querySelectorAll('tbody tr').forEach(function (tr) { var a = tr.querySelector('.wa-amt'), mx = +a.dataset.max, v = +a.value || 0;
      if (v > mx) { a.value = mx; v = mx; } if (v < 0) { a.value = 0; v = 0; } bal += mx; dn += +tr.dataset.done || 0;
      if (tr.querySelector('.wa-chk').checked && v > 0) { tw += v; n++; } tr.querySelector('.wa-bal').textContent = f(mx - v); });
    Q(w, '.wa-dtot').textContent = f(dn); Q(w, '.wa-wtot').textContent = f(tw); Q(w, '.wa-ptot').textContent = f(bal - tw);
    Q(w, '.wa-btn').disabled = !n || w.dataset.stage === 'pending';
    return { tw: tw, n: n, type: tw >= bal ? 'Full waive-off' : 'Partial waive-off' }; }
  function lock(w, on) { w.querySelectorAll('.wa-table input').forEach(function (x) {
      if (on) x.disabled = true; else if (x.classList.contains('wa-chk') || x.classList.contains('wa-all')) x.disabled = x.classList.contains('wa-chk') && +x.closest('tr').querySelector('.wa-amt').dataset.max <= 0; }); }
  function finish(w, ap, msg, cls) {
    w.querySelectorAll('tbody tr').forEach(function (tr) { tr.querySelector('.wa-chk').checked = false; tr.querySelector('.wa-amt').value = 0; tr.querySelector('.wa-amt').disabled = true; });
    Q(w, '.wa-all').checked = false; w.dataset.stage = ''; lock(w, false); calc(w);
    var nt = Q(w, '.wa-note'), fl = Q(w, '.wa-file'); nt.disabled = false; nt.value = ''; fl.disabled = false; fl.value = '';
    w.querySelectorAll('.wv-fname').forEach(function (x) { x.textContent = ''; });
    Q(ap, '.wa-ck').hidden = true; Q(ap, '.wa-tr').hidden = true; Q(ap, '.wa-req').hidden = true; Q(ap, '.wa-none').hidden = false;
    ap.querySelectorAll('textarea').forEach(function (x) { x.value = ''; });
    var d = Q(ap, '.wa-done'); d.hidden = false; d.className = 'wv-done wa-done' + (cls ? ' ' + cls : ''); d.innerHTML = msg;
    var m = Q(w, '.wa-msg'); m.hidden = false; m.innerHTML = msg; }
  document.addEventListener('change', function (e) { var w = e.target.closest('.wa'); if (!w) return;
    if (e.target.classList.contains('wa-file')) { e.target.closest('.wv-drop').nextElementSibling.textContent = e.target.files.length ? '📎 ' + e.target.files[0].name : '';
      Q(w, '.wa-err').textContent = ''; return; }
    var fx = function (c) { var tr = c.closest('tr'), a = tr.querySelector('.wa-amt'); a.disabled = !c.checked; if (!c.checked) a.value = 0;
      if (tr.dataset.fixed) { a.disabled = true; a.value = c.checked ? a.dataset.max : 0; } };
    if (e.target.classList.contains('wa-all')) w.querySelectorAll('tbody .wa-chk:not(:disabled)').forEach(function (c) { c.checked = e.target.checked; fx(c); });
    if (e.target.classList.contains('wa-chk')) fx(e.target);
    calc(w); });
  document.addEventListener('input', function (e) { var w = e.target.closest('.wa'); if (w && e.target.classList.contains('wa-amt')) calc(w);
    if (w && e.target.classList.contains('wa-note')) Q(w, '.wa-err').textContent = '';
    var ap = e.target.closest('.wa-ap'); if (ap) { if (e.target.classList.contains('wa-cnote')) Q(ap, '.wa-cerr').textContent = '';
      if (e.target.classList.contains('wa-tnote')) Q(ap, '.wa-terr').textContent = ''; } });
  document.addEventListener('click', function (e) { var c = e.target.classList, w = e.target.closest('.wa'), ap = e.target.closest('.wa-ap');
    if ((w || ap) && (c.contains('wv-x') || c.contains('wv-no'))) { e.target.closest('.wv-pop').hidden = true; return; }
    if (w && c.contains('wa-btn')) { var m0 = [];               /* DISC-431: the maker's note and file are mandatory */
      if (!Q(w, '.wa-note').value.trim()) m0.push('add the note'); if (!Q(w, '.wa-file').files.length) m0.push('upload a file');
      if (m0.length) { Q(w, '.wa-err').textContent = 'Please ' + m0.join(' and ') + '.'; return; }
      Q(w, '.wa-err').textContent = ''; var q = calc(w), p = Q(w, '.wa-pw');
      p.querySelector('.wv-ptype').innerHTML = 'Type of waive-off: <b>' + q.type + '</b><br>' + q.n + ' charge(s) – amount to be waived off: <b>' + f(q.tw) + '</b>';
      p.hidden = false; }
    if (w && c.contains('wa-yes')) { Q(w, '.wa-pw').hidden = true; var q1 = calc(w), a1 = A(w.dataset.lan);
      w.dataset.stage = 'pending'; lock(w, true); Q(w, '.wa-btn').disabled = true;
      Q(w, '.wa-note').disabled = true; Q(w, '.wa-file').disabled = true;
      var rows = ''; w.querySelectorAll('tbody tr').forEach(function (tr) { var a = tr.querySelector('.wa-amt'), v = +a.value || 0;
        if (tr.querySelector('.wa-chk').checked && v > 0) rows += '<tr><td>' + tr.dataset.name + '</td><td class="num">' + f(+a.dataset.max) +
          '</td><td class="num">' + f(v) + '</td><td class="num">' + f(+a.dataset.max - v) + '</td></tr>'; });
      Q(a1, '.wa-req-t tbody').innerHTML = rows; Q(a1, '.wa-none').hidden = true; Q(a1, '.wa-done').hidden = true; Q(a1, '.wa-req').hidden = false;
      Q(a1, '.wa-req-st').innerHTML = 'Raised by <b>' + w.dataset.mk + ' (Maker)</b> from the Waive-off page. Type of waive-off: <b>' + q1.type +
        '</b>. Amount to be waived off: <b>' + f(q1.tw) + '</b>.<br>Maker note: <span class="wa-mn"></span><br>File: <span class="wa-mf"></span>' +
        '<br>Mail sent to ' + w.dataset.ck + ': <i>Checker Approval Required – Waive-off</i>.';
      Q(a1, '.wa-mn').textContent = Q(w, '.wa-note').value.trim(); Q(a1, '.wa-mf').textContent = Q(w, '.wa-file').files[0].name;
      Q(a1, '.wa-ck').hidden = false;
      var m = Q(w, '.wa-msg'); m.hidden = false; m.innerHTML = 'Waive-off request raised – pending approval in the <a href="#lan-active-' + w.dataset.lan + '">Approvals tab</a>.'; }
    if (!ap) return; var w2 = W(ap.dataset.lan);
    if (c.contains('wa-ck-app')) { if (!Q(ap, '.wa-cnote').value.trim()) { Q(ap, '.wa-cerr').textContent = 'Please add the note.'; return; }
      Q(ap, '.wa-ck').hidden = true; Q(ap, '.wa-tr').hidden = false;
      Q(ap, '.wa-req-st').innerHTML += '<br>Approved by <b>' + w2.dataset.ck + ' (Checker)</b>. Mail sent to ' + w2.dataset.tr + ': <i>Approval Required – Waive-off</i>.'; }
    if (c.contains('wa-ck-dec')) { if (!Q(ap, '.wa-cnote').value.trim()) { Q(ap, '.wa-cerr').textContent = 'Please add the note to decline.'; return; }
      ap.dataset.dec = w2.dataset.ck + ' (Checker)'; Q(ap, '.wa-pd').hidden = false; }
    if (c.contains('wa-dec')) { if (!Q(ap, '.wa-tnote').value.trim()) { Q(ap, '.wa-terr').textContent = 'Please add the note to decline.'; return; }
      ap.dataset.dec = w2.dataset.tr; Q(ap, '.wa-pd').hidden = false; }
    if (c.contains('wa-yes-d')) { Q(ap, '.wa-pd').hidden = true;
      finish(w2, ap, '<b>Waive-off request declined by ' + ap.dataset.dec + ' – cancelled.</b> Nothing is waived. Mail sent to the maker: <i>Waive-off Request Declined</i>.', 'wv-cancel'); }
    if (c.contains('wa-app')) { if (!Q(ap, '.wa-tnote').value.trim()) { Q(ap, '.wa-terr').textContent = 'Please add the note.'; return; } Q(ap, '.wa-pa').hidden = false; }
    if (c.contains('wa-yes-a')) { Q(ap, '.wa-pa').hidden = true; var q3 = calc(w2);
      w2.querySelectorAll('tbody tr').forEach(function (tr) { var ck = tr.querySelector('.wa-chk'), a = tr.querySelector('.wa-amt'), v = +a.value || 0;
        if (!ck.checked || v <= 0) return; var left = r2(+a.dataset.max - v); a.dataset.max = left;
        tr.dataset.done = r2((+tr.dataset.done || 0) + v); tr.querySelector('.wa-dn').textContent = f(tr.dataset.done); });
      finish(w2, ap, '<b>Approved by ' + w2.dataset.ck + ' (Checker) and ' + w2.dataset.tr + ' – ' + f(q3.tw) + ' waived off (' + q3.type.toLowerCase() + ').</b> ' +
        'The waiver is posted in the Statement of Account with a waiver narration; the Waived off and Payable columns are updated. Mail sent: <i>Waive-off Approved</i>.'); }
  });
})();
</script>"""


def lms_body(logo, home):
    nav, secs = [], []
    for mid, name, subs, desc in LMS_MODULES:
        nav.append(f'<a class="lms-nav-m" href="#m-{mid}">{_h.escape(name)}</a>')
        nav += [f'<a class="lms-nav-s" href="#m-{mid}-{sid}">{_h.escape(s)}</a>' for sid, s in subs]
        subs_html = ("<ul class='lms-subs'>" + "".join(f'<li><a href="#m-{mid}-{sid}">{_h.escape(s)}</a></li>' for sid, s in subs)
                     + "</ul>") if subs else ""
        secs.append(f'<section id="m-{mid}" class="lms-sec"><h2>{_h.escape(name)}</h2>{desc or TBA}{subs_html}</section>')
        secs += [f'<section id="m-{mid}-{sid}" class="lms-sec lms-list"><p class="lms-crumb">{_h.escape(name)} › {_h.escape(s)}</p>'
                 + (loan_view(sid) if mid == "loans" else f'<h2>{_h.escape(name)} – {_h.escape(s)}</h2>{TBA}') + '</section>' for sid, s in subs]
    # one detail section per sample LAN in every list (DISC-329)
    for v in ("active", "inactive", "draft", "submitted", "closed", "rejected"):
        secs += [lan_detail(v, r) for r in _rows(v)]
    secs += [active_waive(r) for r in _rows("active")]   # Active loan Waive-off pages (DISC-366)
    intro = ('<section class="lms-intro"><h2>LMS – Loan Management System</h2>'
             '<p>The modules of the LMS, as in the left menu of the LMS. Choose a module to open it.</p>'
             '<div class="lms-cards">' + "".join(f'<a class="lms-card" href="#m-{mid}"><b>{_h.escape(n)}</b>'
                                                 + (f'<small>{", ".join(s for _, s in subs)}</small>' if subs else '') + '</a>'
                                                 for mid, n, subs, _ in LMS_MODULES) + '</div></section>')
    return (f'<div class="lms"><aside class="lms-side"><div class="lms-logo">{logo}</div>'
            f'<a class="lms-home" href="{home}">← Home</a><nav>{"".join(nav)}</nav></aside>'
            f'<main class="lms-main">{intro}{"".join(secs)}</main></div>' + WAIVER_JS + WAIVE_ACTIVE_JS)
