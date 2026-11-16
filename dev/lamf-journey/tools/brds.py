"""BRD documents (DISC-269) – listed on brd.html (home CTA “Open BRD document”); each BRD opens brd-<slug>.html.

Add a BRD here: slug (file name), title, status, last updated (DD-MM-YYYY), one-line summary and the body (HTML;
empty = “content to be added”).
"""

TBD = '<span class="brd-tbd">To be defined</span>'

# ---------------------------------------------------------------------------------------------------------------------------
# BRD – Waiver of Charges and Processing Fee (DISC-270 … DISC-274)
# Scenarios, charges, product construct and treasury remarks from the owner's LAMF_Charges_Waiver_V1.xlsx; the waiver rules
# (full / partial / none, one confirmation) from the owner's Scenario 1 notes (DISC-271, DISC-273). Business logic only – no
# screen detail (DISC-272).
# ---------------------------------------------------------------------------------------------------------------------------
CHARGES = [   # (charge, amount incl. 18% GST, when it is incurred)
    ("Lien Marking Charge", "₹531 (₹450 + ₹81 GST)", "When the mutual fund units are pledged (lien marked)"),
    ("Lien Removal Charge", "₹118 (₹100 + ₹18 GST)", "When the lien is removed (units de-pledged)"),
    ("Processing Fee Charge", TBD, "From the Sanction Letter generation"),
    ("Stamp Duty Charge", TBD, "From the Loan Agreement e-Sign"),
    ("Bounce Charge", TBD, "Active loan – when an EMI bounces"),
    ("Penal Charge", TBD, "Active loan – on a delay or default"),
    ("Loan Renewal Charge", TBD, "Active loan – on renewal"),
    ("Bank Swap Charge", TBD, "Active loan – when the repayment bank account is changed"),
]
LM, LR, PF, SD = "Lien Marking Charge", "Lien Removal Charge", "Processing Fee Charge", "Stamp Duty Charge"
ACTIVE_CH = [LM, LR, PF, SD, "Bounce Charge", "Penal Charge", "Loan Renewal Charge", "Bank Swap Charge"]

_REJECT_DRAFT = "LMS requires a feature to reject applications in DRAFT status – not available today."
_NOTIFY_DRAFT = ("SCCL notifies the customer that the mutual fund units remain lien-marked; to de-pledge them the customer must pay "
                 "the applicable charges through the payment link in the communication.")
_TIMING_DRAFT = ("Initial communication: sent along with the marketing communication (drop-off reminders). "
                 "Payment link: sent with the rejection SMS / mail.")
_ACC_PAID = "Accounting entries for the applicable charges are triggered once SCCL successfully receives the payment."
_ACC_WAIVED = "The waived-off charges do not flow into UNO books."
_ACC_NONE = "No accounting entries are applicable at this stage."


def _draft_options(n):
    """Draft drop-offs (scenarios 2 – 4): without / partial / full waive-off."""
    return [
        (f"{n}.1", "Without waive-off", "OPS rejects the DRAFT application without any waiver – the customer pays all the charges.",
         ["OPS rejects the DRAFT application in LMS and confirms (final).", "LAN status DRAFT → REJECTED.",
          "Customer is informed of the rejection with the payable charges and the payment link.",
          "Customer pays → accounting entries are posted → the units are de-pledged."],
         [("LMS", f"{_REJECT_DRAFT} Once rejected, the mutual fund units can be de-pledged – after the customer pays."),
          ("Customer communication", f"{_NOTIFY_DRAFT}<br><b>Timing:</b> {_TIMING_DRAFT}"),
          ("UNO (Treasury)", _ACC_PAID)]),
        (f"{n}.2", "With waive-off (Partial)", "OPS waives a part of the charges – the customer pays the balance.",
         ["OPS enters the amount waived for each charge, rejects and confirms (final).", "LAN status DRAFT → REJECTED.",
          "Payable charges = the charges minus the amount waived.",
          "Customer is informed of the rejection with the payable charges and the payment link.",
          "Customer pays the balance → accounting entries for the amount received → the units are de-pledged."],
         [("LMS", f"{_REJECT_DRAFT} The units can be de-pledged after the customer pays the balance."),
          ("Customer communication", f"{_NOTIFY_DRAFT} (payable charges after the waiver)<br><b>Timing:</b> {_TIMING_DRAFT}"),
          ("UNO (Treasury)", f"{_ACC_PAID} {_ACC_WAIVED}")]),
        (f"{n}.3", "With waive-off (Full)", "OPS waives all the charges – nothing is payable; SCCL bears the charges.",
         ["OPS waives all the charges, rejects and confirms (final).", "LAN status DRAFT → REJECTED.",
          "Customer is informed of the rejection – no payment link.", "The units are de-pledged."],
         [("LMS", f"{_REJECT_DRAFT} Once rejected, the mutual fund units can be de-pledged."),
          ("Customer communication", "Rejection only – no payment link."),
          ("UNO (Treasury)", _ACC_WAIVED)]),
    ]


_REJ_LINK = ("SCCL notifies the customer that the application has been rejected and the mutual fund units remain lien-marked; to "
             "de-pledge them the customer must pay the applicable charges through the payment link.<br><b>Timing:</b> immediately after the rejection in LMS.")
_REJ_NOLINK = "SCCL notifies the customer that the application has been rejected – no payment link.<br><b>Timing:</b> immediately after the rejection in LMS."


def _reject_options(n, status, first):
    """Rejection by OPS of a SUBMITTED / ACCOUNT OPENED application – with or without a payment link."""
    return [
        (f"{n}.{first}", "Rejected – with payment link (without waive-off / partial waive-off)",
         "OPS rejects with charges – the customer pays all the charges, or the balance after a partial waiver.",
         ["OPS rejects the application in LMS (Rejected with Charges) and confirms (final).", f"LAN status {status} → REJECTED.",
          "Customer is informed at once with the payable charges and the payment link.",
          "Customer pays → accounting entries are posted → the units are de-pledged."],
         [("LMS", "Rejection with charges; the units stay lien-marked until the customer pays."),
          ("Customer communication", _REJ_LINK), ("UNO (Treasury)", _ACC_PAID)]),
        (f"{n}.{first + 1}", "Rejected – without payment link (with waive-off)",
         "OPS rejects without charges – all the charges are waived; SCCL bears them.",
         ["OPS rejects the application in LMS (Rejected without Charges) and confirms (final).", f"LAN status {status} → REJECTED.",
          "Customer is informed at once – no payment link.", "LMS gives the option to de-pledge the units."],
         [("LMS", "Following the rejection, LMS provides an option to de-pledge the mutual fund units."),
          ("Customer communication", _REJ_NOLINK), ("UNO (Treasury)", _ACC_WAIVED)]),
    ]


# (No, LMS LAN status, scenario, charges applicable, [(code, type, when, flow, [(system, impact)])])
WAIVER_SCENARIOS = [
    (1, "DRAFT", "Customer drops off before pledging the mutual funds", [],
     [("1.1", "No charges", "The customer leaves before the lien marking.",
       ["No charge is incurred; the application stays in DRAFT (expires as per the existing rule)."],
       [("LMS", "No charges apply at this stage."), ("UNO (Treasury)", _ACC_NONE)])]),
    (2, "DRAFT", "Customer drops off after pledging the mutual funds", [LM, LR], _draft_options(2)),
    (3, "DRAFT", "Customer drops off after the Sanction Letter generation (mutual funds already pledged)", [PF, LM, LR], _draft_options(3)),
    (4, "DRAFT", "Customer drops off after the Loan Agreement e-Sign (mutual funds pledged, Sanction Letter generated and submitted)",
     [PF, LM, LR, SD], _draft_options(4)),
    (5, "SUBMITTED", "Customer drops off after the E-Mandate (mutual funds pledged, Sanction Letter generated, Loan Agreement e-Signed) – "
                     "OPS decides on the Loan Account Opening", [PF, LM, LR, SD],
     [("5.1", "Approved", "OPS approves the Loan Account Opening.",
       ["OPS approves.", "LAN status SUBMITTED → ACCOUNT OPENED.", "No charges are collected at this stage."],
       [("LMS", "The application moves to ACCOUNT OPENED status. No charges are collected at this stage."),
        ("UNO (Treasury)", _ACC_NONE)])] + _reject_options(5, "SUBMITTED", 2)),
    (6, "ACCOUNT OPENED", "Customer drops off after the Loan Account Opening – OPS decides on the Loan Lodgement", [PF, LM, LR, SD],
     [("6.1", "Approved (without waive-off)", "OPS approves the Loan Lodgement; the charges stay applicable.",
       ["OPS approves.", "The application proceeds to the loan lodgement (ACCOUNT OPENED → ACTIVE).", "No charges are collected at this stage."],
       [("LMS", "The application proceeds to the loan lodgement. No charges are collected at this stage."),
        ("UNO (Treasury)", _ACC_NONE)]),
      ("6.2", "Approved (with waive-off)", "OPS approves the Loan Lodgement and waives the charges.",
       ["OPS waives the charges and approves.", "The application proceeds to the loan lodgement.", "The waived charges are not collected."],
       [("LMS", "No charges apply at this stage (waived)."), ("UNO (Treasury)", _ACC_WAIVED)])] + _reject_options(6, "ACCOUNT OPENED", 3)),
    (7, "ACTIVE", "Customer drops off after the Loan Lodgement (loan account active)", ACTIVE_CH,
     [("7.1", "Without waive-off", "The charges stay payable.",
       ["All applicable charges are collected before the loan account is closed."],
       [("LMS", "All applicable charges are collected before the loan account is closed."),
        ("UNO (Treasury)", "The existing accounting process applies.")]),
      ("7.2", "With waive-off", "OPS waives charges already posted to the loan account.",
       ["OPS waives the charge in LMS.", "The Statement of Account (SOA) is updated with the waiver narration."],
       [("LMS", "LMS requires an option to waive charges. As the charges are already posted in the Statement of Account (SOA), the SOA "
                "must be updated with the corresponding waiver narration."),
        ("UNO (Treasury)", _ACC_WAIVED)])]),
]


def _waiver_body():
    tick = lambda c, chs: "✓" if c in chs else ""
    matrix = ("<table class='brd-table brd-mx'><thead><tr><th>Charge</th><th>Amount (incl. 18% GST)</th>"
              + "".join(f"<th>Sc. {n}</th>" for n, *_ in WAIVER_SCENARIOS) + "</tr></thead><tbody>"
              + "".join(f"<tr><td>{c}</td><td>{amt}</td>" + "".join(f"<td class='c'>{tick(c, s[3])}</td>" for s in WAIVER_SCENARIOS) + "</tr>"
                        for c, amt, _ in CHARGES) + "</tbody></table>")
    charges = ("<table class='brd-table'><thead><tr><th>Charge</th><th>Amount (incl. 18% GST)</th><th>When it is incurred</th></tr></thead><tbody>"
               + "".join(f"<tr><td>{c}</td><td>{a}</td><td>{w}</td></tr>" for c, a, w in CHARGES) + "</tbody></table>")
    summary = ("<table class='brd-table'><thead><tr><th>#</th><th>LMS LAN status</th><th>Scenario</th><th>Charges applicable</th><th>Options</th></tr></thead><tbody>"
               + "".join(f"<tr><td class='c'>{n}</td><td>{st}</td><td>{sc}</td><td>{'<br>'.join(ch) or 'NA'}</td>"
                         f"<td>{'<br>'.join(o[0] + ' ' + o[1] for o in opts)}</td></tr>" for n, st, sc, ch, opts in WAIVER_SCENARIOS)
               + "</tbody></table>")

    def opt(o):
        code, typ, when, flow, rows = o
        return (f"<h4>{code} {typ}</h4><p><b>When:</b> {when}</p><ol class='brd-flow'>" + "".join(f"<li>{x}</li>" for x in flow) + "</ol>"
                "<table class='brd-table'><tbody>" + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows) + "</tbody></table>")
    detail = "".join(f"<h3>Scenario {n} – {sc}</h3><p><b>LMS LAN status:</b> {st}<br><b>Charges applicable:</b> {', '.join(ch) or 'None'}</p>"
                     + "".join(opt(o) for o in opts) for n, st, sc, ch, opts in WAIVER_SCENARIOS)
    return f"""
<h2>1. Background</h2>
<p>In the LAMF journey the customer pledges the mutual fund units (lien marking) before the loan account is opened. When the
customer drops off at a later stage, charges have already been incurred – lien marking and lien removal, and from later stages
the processing fee and the stamp duty. Who pays these charges is not decided today, so <b>SCCL bears them</b>.</p>
<h2>2. Objective</h2>
<p>For every stage at which the customer can drop off, define the charges that apply and how the case is closed <b>with
waive-off</b> (SCCL bears the charges) and <b>without waive-off</b> (the customer pays) – in LMS, in the customer communication and
in UNO (Treasury).</p>
<h2>3. Scope</h2>
<ul><li>{len(WAIVER_SCENARIOS)} scenarios by LMS LAN status – DRAFT (before pledging, after pledging, after the Sanction Letter, after the
Loan Agreement e-Sign), SUBMITTED, ACCOUNT OPENED and ACTIVE.</li>
<li>The charges below; the waive-off decision; the rejection of the application; the de-pledging of the units; the customer
communication; the accounting in UNO.</li></ul>
<h2>4. Charges</h2>
{charges}
<p><b>Charges applicable by scenario</b></p>
{matrix}
<h2>5. Common rules</h2>
<ul>
<li>OPS decides the waive-off for each charge: the full amount, a part of it, or nothing. The amount waived cannot be more than the charge.</li>
<li>Payable charges = the charges minus the amount waived. SCCL bears the amount waived; the customer pays the payable charges.</li>
<li>A rejection needs one confirmation from the OPS user; once confirmed it is <b>final</b> – no second approval, and it cannot be undone.</li>
<li>Nothing payable (full waive-off): the customer is informed without a payment link and the units can be de-pledged at once.</li>
<li>Something payable: the customer is informed with the payable charges and a payment link; the units stay lien-marked until the
customer pays, then they are de-pledged.</li>
<li>UNO: accounting entries are posted only when SCCL receives the payment; waived charges never flow into UNO books.</li>
<li>Communication timing – DRAFT stages: the first notice goes with the marketing communication, the payment link with the
rejection SMS / mail. SUBMITTED / ACCOUNT OPENED: immediately after the rejection in LMS.</li>
</ul>
<h2>6. Scenarios</h2>
{summary}
<h2>7. Scenario-wise flow and impact</h2>
{detail}
<h2>8. Open points</h2>
<ul><li>Amount of the processing fee, the stamp duty and the active-loan charges (bounce, penal, loan renewal, bank swap).</li>
<li>LOS: what the customer sees in the LOS journey after a rejection (DRAFT, SUBMITTED, ACCOUNT OPENED).</li>
<li>What happens if the customer does not pay the payable charges (time limit, follow-up; the units stay lien-marked).</li>
<li>Scenario 6.2: which charges can be waived at the loan lodgement approval and how the waiver is recorded.</li>
<li>Scenario 7.2: who can waive charges on an active loan, and any limit on the amount.</li></ul>
"""


BRDS = [
    {"slug": "waive-off", "title": "Waiver of Charges and Processing Fee", "status": "Draft", "updated": "16-11-2026",
     "summary": "Charges at each drop-off stage of the LAMF journey – with and without waive-off – and the handling in LMS, "
                "the customer communication and UNO.",
     "body": _waiver_body()},
]
