"""BRD documents (DISC-269) – listed on brd.html (home CTA “Open BRD document”); each BRD opens brd-<slug>.html.

Add a BRD here: slug (file name), title, status, last updated (DD-MM-YYYY), one-line summary and the body (HTML;
empty = “content to be added”).
"""

TBD = '<span class="brd-tbd">To be defined</span>'

# ---------------------------------------------------------------------------------------------------------------------------
# BRD – Waiver of Charges and Processing Fee (DISC-270 … DISC-280)
# Scenarios, charges, product construct and treasury remarks from the owner's LAMF_Charges_Waiver_V1.xlsx; the waiver rules
# (full / partial / none, one confirmation) from the owner's Scenario 1 notes (DISC-271, DISC-273). Business logic only – no
# screen detail (DISC-272).
# ---------------------------------------------------------------------------------------------------------------------------
CHARGES = [   # (charge, amount incl. 18% GST, when it is incurred)
    ("Lien Marking Charge", "₹531 (₹450 + ₹81 GST)", "When the mutual fund units are pledged (lien marked)"),
    ("Lien Removal Charge", "₹118 (₹100 + ₹18 GST)", "When the lien is removed (units de-pledged)"),
    ("Processing Fee Charge", TBD, "From the Sanction Letter generation"),
    ("Stamp Duty Charge", TBD, "From the Loan Agreement e-Sign"),
    ("Bounce Charge", TBD, "Active loan, when an EMI bounces"),
    ("Penal Charge", TBD, "Active loan, on a delay or default"),
    ("Loan Renewal Charge", TBD, "Active loan, on renewal"),
    ("Bank Swap Charge", TBD, "Active loan, when the repayment bank account is changed"),
]
LM, LR, PF, SD = "Lien Marking Charge", "Lien Removal Charge", "Processing Fee Charge", "Stamp Duty Charge"
ACTIVE_CH = [LM, LR, PF, SD, "Bounce Charge", "Penal Charge", "Loan Renewal Charge", "Bank Swap Charge"]

# The 7 scenarios from the owner's LAMF_Charges_Waiver_V1.xlsx (DISC-274). The waive-off process in section 5 is common to all of
# them (DISC-280); this table only says what applies in each one.
# (No, LMS LAN status, scenario, charges applicable, what OPS can do, notes)
WAIVER_SCENARIOS = [
    (1, "DRAFT", "Customer drops off before pledging the mutual funds", [],
     "Nothing. No charges apply.",
     "If the units are not pledged within 30 days from the LAN generated date, the LAN moves from DRAFT to INACTIVE automatically. "
     "No accounting entries."),
    (2, "DRAFT", "Customer drops off after pledging the mutual funds", [LM, LR],
     "Reject the application, with no, partial or full waive-off.",
     "Rejecting a DRAFT LAN is a new feature in LMS (see the BRD DRAFT LAN Rejection)."),
    (3, "DRAFT", "Customer drops off after the Sanction Letter is generated (mutual funds already pledged)", [PF, LM, LR],
     "Reject the application, with no, partial or full waive-off.",
     "Rejecting a DRAFT LAN is a new feature in LMS (see the BRD DRAFT LAN Rejection)."),
    (4, "DRAFT", "Customer drops off after the Loan Agreement e-Sign (mutual funds pledged, Sanction Letter generated and submitted)",
     [PF, LM, LR, SD], "Reject the application, with no, partial or full waive-off.",
     "Rejecting a DRAFT LAN is a new feature in LMS (see the BRD DRAFT LAN Rejection)."),
    (5, "SUBMITTED", "Customer drops off after the E-Mandate (mutual funds pledged, Sanction Letter generated, Loan Agreement e-Signed)",
     [PF, LM, LR, SD], "Approve the Loan Account Opening, or reject it with no, partial or full waive-off.",
     "On approval the LAN moves to ACCOUNT OPENED and no charges are collected at this stage."),
    (6, "ACCOUNT OPENED", "Customer drops off after the Loan Account Opening", [PF, LM, LR, SD],
     "Approve the Loan Lodgement (with or without waive-off), or reject it with no, partial or full waive-off.",
     "On approval the application goes to the loan lodgement and no charges are collected at this stage. Waived charges do not go into UNO books."),
    (7, "ACTIVE", "Customer drops off after the Loan Lodgement (loan account active)", ACTIVE_CH,
     "Waive charges on the active loan account (no, partial or full). There is no rejection at this stage.",
     "Without waive-off, all charges are collected before the loan account is closed (existing accounting process). With waive-off, "
     "the charges are already posted in the Statement of Account (SOA), so the SOA must be updated with the waiver narration. "
     "Waived charges do not go into UNO books."),
]


def _waiver_body():
    tick = lambda c, chs: "✓" if c in chs else ""
    matrix = ("<table class='brd-table brd-mx'><thead><tr><th>Charge</th><th>Amount (incl. 18% GST)</th>"
              + "".join(f"<th>Sc. {n}</th>" for n, *_ in WAIVER_SCENARIOS) + "</tr></thead><tbody>"
              + "".join(f"<tr><td>{c}</td><td>{amt}</td>" + "".join(f"<td class='c'>{tick(c, s[3])}</td>" for s in WAIVER_SCENARIOS) + "</tr>"
                        for c, amt, _ in CHARGES) + "</tbody></table>")
    charges = ("<table class='brd-table'><thead><tr><th>Charge</th><th>Amount (incl. 18% GST)</th><th>When it is incurred</th></tr></thead><tbody>"
               + "".join(f"<tr><td>{c}</td><td>{a}</td><td>{w}</td></tr>" for c, a, w in CHARGES) + "</tbody></table>")
    scen = ("<table class='brd-table'><thead><tr><th>#</th><th>LMS LAN status</th><th>Scenario</th><th>Charges applicable</th>"
            "<th>What OPS can do</th><th>Notes</th></tr></thead><tbody>"
            + "".join(f"<tr><td class='c'>{n}</td><td>{st}</td><td>{sc}</td><td>{'<br>'.join(ch) or 'None'}</td><td>{do}</td><td>{note}</td></tr>"
                      for n, st, sc, ch, do, note in WAIVER_SCENARIOS) + "</tbody></table>")
    return f"""
<h2>1. Background</h2>
<p>In the LAMF journey the customer pledges the mutual fund units (lien marking) before the loan account is opened. If the customer
drops off after that, some charges are already incurred: lien marking and lien removal, and at later stages the processing fee and
the stamp duty. Today it is not decided who pays these charges, so SCCL bears them.</p>
<h2>2. Objective</h2>
<p>Give OPS one common way, for all the scenarios, to waive these charges fully, partially or not at all, and to collect the
balance from the customer before the units are de-pledged.</p>
<h2>3. Scope</h2>
<ul><li>The 7 scenarios in section 6 (DRAFT, SUBMITTED, ACCOUNT OPENED and ACTIVE).</li>
<li>The waive-off decision, the rejection, the customer communication, the payment by the customer, the Treasury confirmation,
the receipt and the de-pledge.</li>
<li>Rejecting a DRAFT LAN itself (who can reject, status rules) is in the BRD DRAFT LAN Rejection. This BRD covers the charges.</li></ul>
<h2>4. Charges</h2>
{charges}
<p><b>Charges applicable in each scenario</b></p>
{matrix}
<h2>5. Waive-off process (common for all scenarios)</h2>
<h3>5.1 Approvals tab in LMS</h3>
<p>In LMS, the Approvals tab under the LAN details shows the charges that apply to the LAN. For each charge, the OPS user can enter
the amount to waive off. The payable charge is the amount of the charge minus the amount waived off. The amount waived off cannot be
more than the charge.</p>
<h3>5.2 Type of waive-off</h3>
<p>The system decides the type of waive-off only when the OPS user rejects the application. The OPS user does not choose it.</p>
<table class="brd-table"><thead><tr><th>Payable charges compared with the amount of charges</th><th>Type of waive-off</th></tr></thead><tbody>
<tr><td>Payable charges are the same as the amount of charges</td><td>No waive-off</td></tr>
<tr><td>Payable charges are less than the amount of charges, but not 0</td><td>Partial waive-off</td></tr>
<tr><td>Payable charges are 0</td><td>Full waive-off</td></tr>
</tbody></table>
<h3>5.3 Rejection</h3>
<ul><li>The OPS user rejects the application from the Approvals tab and enters a rejection reason.</li>
<li>The existing pop-up asks the OPS user to confirm. Once confirmed, the rejection is final and cannot be revoked. The LAN status
becomes REJECTED.</li>
<li>Who can reject: if the loan amount is below ₹5 lakh, OPS L1 only. If it is ₹5 lakh or more, OPS L2 or L3 only.</li></ul>
<h3>5.4 Customer communication</h3>
<ul><li>The customer is told only after the application is rejected. Nothing is sent before that.</li>
<li>Full waive-off: the SMS and mail say that the application is rejected. There is no payment link.</li>
<li>Partial or no waive-off: the SMS and mail say that the application is rejected and give the payable charges with a payment link.</li></ul>
<h3>5.5 Payment by the customer</h3>
<ul><li>The customer can pay in two ways: from the payment link in the SMS or mail, or by logging in to LOS.</li>
<li>The payment link needs OTP verification before the customer can pay.</li>
<li>After the rejection, when the customer logs in to LOS, the only option is to pay the charges. A new LOS page is needed for this.
It shows the total charges with the breakup of each charge, and a Pay button.</li></ul>
<h3>5.6 After the payment</h3>
<ul><li>As soon as the customer pays, the accounting entry is posted in UNO.</li>
<li>At the same time an internal mail goes to the Treasury team (Natarajan K) with the LAN, the amount paid and the breakup of the charges.</li></ul>
<h3>5.7 Treasury confirmation</h3>
<ul><li>The Treasury team confirms the payment in LMS.</li>
<li>Until Treasury confirms, the de-pledge option stays disabled in LMS.</li></ul>
<h3>5.8 Receipt</h3>
<ul><li>After Treasury confirms, the system generates a receipt.</li>
<li>The receipt is stored in the Documents tab of the LAN in LMS.</li>
<li>The receipt is sent to the customer with an SMS and mail saying that the payment has been received.</li></ul>
<h3>5.9 De-pledge</h3>
<ul><li>Full waive-off: nothing is payable, so OPS can de-pledge the units after the rejection.</li>
<li>Partial or no waive-off: OPS can de-pledge only after the customer has paid and Treasury has confirmed the payment. Until then
LMS shows the pending charges and does not allow OPS to de-pledge.</li>
<li>De-pledge is allowed only for a REJECTED or a CLOSED LAN.</li></ul>
<h3>5.10 UNO</h3>
<ul><li>The accounting entry is posted only when the customer pays.</li>
<li>Waived charges do not go into UNO books.</li></ul>
<h2>6. End to end flow</h2>
<ol class="brd-flow">
<li>The OPS user opens the LAN in LMS and goes to the Approvals tab.</li>
<li>The OPS user enters the amount to waive off for each charge, if any.</li>
<li>The OPS user rejects the application, enters the reason and confirms. The LAN status becomes REJECTED.</li>
<li>The system decides the type of waive-off: no, partial or full.</li>
<li>Full waive-off: the customer gets the rejection SMS and mail without a payment link. OPS can de-pledge the units.</li>
<li>Partial or no waive-off: the customer gets the rejection SMS and mail with the payable charges and a payment link.</li>
<li>The customer pays through the payment link (after OTP verification) or from the new LOS payment page.</li>
<li>The accounting entry is posted in UNO and an internal mail goes to the Treasury team (Natarajan K) with the amount and the breakup.</li>
<li>The Treasury team confirms the payment in LMS.</li>
<li>The system generates the receipt, stores it in the Documents tab and sends it to the customer with a payment received SMS and mail.</li>
<li>The de-pledge option is enabled and OPS de-pledges the units.</li>
</ol>
<h2>7. Scenarios</h2>
<p>The process in section 5 applies to every scenario below. The table only shows what is different in each one.</p>
{scen}
<h2>8. System impact</h2>
<table class="brd-table"><tbody>
<tr><th>LMS</th><td>Approvals tab with the charges and the amount to waive off for each charge; the system decides the type of waive-off on
rejection; Treasury confirmation of the payment; de-pledge only after the confirmation when something was payable; receipt stored in
the Documents tab.</td></tr>
<tr><th>LOS</th><td>New page shown after the rejection: total charges with the breakup and a Pay button. This is the only option for the customer.</td></tr>
<tr><th>Payment link</th><td>Sent with the rejection SMS and mail for partial or no waive-off; OTP verification before the payment.</td></tr>
<tr><th>UNO</th><td>Accounting entry posted as soon as the customer pays. Waived charges do not go into UNO books.</td></tr>
<tr><th>Communication</th><td>Customer: rejection (with or without the payment link) and payment received with the receipt. Internal: payment
details to the Treasury team (Natarajan K).</td></tr>
</tbody></table>
<h2>9. Open points</h2>
<ul><li>Amount of the processing fee, the stamp duty and the active loan charges (bounce, penal, loan renewal, bank swap).</li>
<li>What happens if the customer does not pay the payable charges (time limit, reminders). The units stay lien-marked.</li>
<li>Scenario 7: who can waive charges on an active loan, and any limit on the amount.</li>
<li>Templates for the rejection SMS and mail, the payment received SMS and mail, and the internal mail to Treasury.</li></ul>
"""


# ---------------------------------------------------------------------------------------------------------------------------
# BRD – DRAFT LAN Rejection (DISC-275)
# ---------------------------------------------------------------------------------------------------------------------------
DRAFT_REJECTION = f"""
<h2>1. Background</h2>
<p>Today the OPS team can reject a loan application in LMS only after it is <b>SUBMITTED</b>. A loan application in <b>DRAFT</b>
status cannot be rejected. When the customer drops off after the mutual fund units are lien-marked (pledged) but before the
application is submitted, the LAN stays in DRAFT and the units stay lien-marked: the lien can be removed (de-pledged) only for a
<b>REJECTED</b> or a <b>CLOSED</b> LAN, and a DRAFT LAN can be neither.</p>
<h2>2. Objective</h2>
<p>Allow the OPS team to <b>reject a DRAFT loan application in LMS</b> when the customer has pledged the mutual fund units, so that
the LAN status becomes <b>REJECTED</b> and the units can be de-pledged.</p>
<h2>3. Scope</h2>
<ul><li><b>In scope:</b> DRAFT LANs where the lien marking (pledge) is successful.</li>
<li><b>Out of scope:</b> DRAFT LANs that are not pledged – they move from DRAFT to <b>INACTIVE</b> automatically (rule below);
SUBMITTED and later statuses – the existing rejection applies; the charges on rejection – covered by the BRD “Waiver of Charges
and Processing Fee”.</li></ul>
<h2>4. LAN status rules</h2>
<ul>
<li><b>REJECTED</b> – the application is rejected by OPS (new: also from DRAFT).</li>
<li><b>CLOSED</b> – only an <b>ACTIVE</b> loan account is closed (foreclosure, tenure completion or invocation): ACTIVE → CLOSED. A LAN is
<b>never</b> closed from DRAFT.</li>
<li><b>De-pledge (lien removal)</b> is allowed only for a REJECTED or a CLOSED LAN. So for a pledged DRAFT LAN, rejection is the only
way to remove the lien.</li>
<li><b>INACTIVE</b> – a DRAFT LAN that is not pledged within 30 days from the LAN generated date (automatic).</li>
</ul>
<h2>5. Eligibility</h2>
<table class="brd-table"><thead><tr><th>LAN status</th><th>Pledged (lien marked)?</th><th>Can OPS reject?</th><th>What happens</th></tr></thead><tbody>
<tr><td>DRAFT</td><td>No</td><td>No</td><td>Moves from DRAFT to <b>INACTIVE</b> automatically when the units are not pledged within <b>30 days</b> from the LAN generated date.</td></tr>
<tr><td>DRAFT</td><td>Yes</td><td><b>Yes – new</b></td><td>Does <b>not</b> expire automatically (the lien is marked) – stays DRAFT until OPS rejects it: DRAFT → <b>REJECTED</b>.</td></tr>
<tr><td>SUBMITTED and later</td><td>Yes</td><td>Yes – existing</td><td>No change.</td></tr>
</tbody></table>
<h2>6. Business rules</h2>
<ul>
<li>LMS must give an <b>Approvals</b> section in the LAN details for a DRAFT LAN (today it is not available for DRAFT loans), with a
<b>Reject</b> action.</li>
<li>The Reject action is available <b>only for a DRAFT LAN whose units are pledged</b>. For a DRAFT LAN that is not pledged, Reject is not offered.</li>
<li>A pledged DRAFT LAN is <b>not expired automatically</b>. OPS rejects it manually:
  <ul><li>after 30 days from the LAN generated date, when the customer has not submitted the application; or</li>
  <li>at any time before that, when the customer asks for the lien removal.</li></ul></li>
<li>Who can reject depends on the loan amount: <b>below ₹5 lakh – OPS L1 only</b>; <b>₹5 lakh and above – OPS L2 or L3 only</b>.</li>
<li>A <b>rejection reason</b> must be captured – <b>free text</b> for now (a fixed list of reasons later) – and the rejection (reason, user, date and time) is recorded in the <b>Audit</b>.</li>
<li>Rejection needs one confirmation from the OPS user (the existing pop-up confirmation); once confirmed it is <b>final</b> and cannot be revoked.</li>
<li>On confirmation the LAN status changes from DRAFT to <b>REJECTED</b> and the LAN is listed with the rejected applications; the
units can then be de-pledged.</li>
<li>A DRAFT LAN that is not pledged within 30 days from the LAN generated date moves to <b>INACTIVE</b> automatically – no OPS action.</li>
<li>The charges applicable on the rejection (lien marking, lien removal, and processing fee / stamp duty where incurred), their
waive-off, the payment link and the de-pledging follow the BRD “Waiver of Charges and Processing Fee” (scenarios 2 – 4).</li>
<li><b>Customer communication</b> on rejection: the customer is told that the loan application has been rejected and the units are
still lien-marked (with the payable charges and payment link where applicable, as per the Waiver BRD).</li>
<li><b>LOS:</b> when the customer logs in after the rejection, the Curated Offers page shows <b>a fresh</b> product card (start a
new application) instead of continuing the rejected one.</li>
</ul>
<h2>7. Flow</h2>
<ol class="brd-flow">
<li>The customer generates the LAN in LOS → LAN status DRAFT.</li>
<li><b>If the units are not pledged within 30 days</b> from the LAN generated date → the system moves the LAN from DRAFT to INACTIVE.</li>
<li><b>If the units are pledged</b> and the customer drops off before submitting → the LAN stays DRAFT (no automatic expiry).</li>
<li>OPS (L1 below ₹5 lakh; L2 / L3 for ₹5 lakh and above) opens the DRAFT LAN in LMS → Approvals → Reject – after 30 days, or earlier on the customer’s request for lien removal.</li>
<li>OPS enters the rejection reason and confirms (final).</li>
<li>LAN status DRAFT → REJECTED; the rejection is recorded in the Audit.</li>
<li>Customer is informed: application rejected, units still lien-marked (charges and payment link as per the Waiver BRD).</li>
<li>De-pledge of the units: at once when the charges are fully waived; otherwise after the customer pays and the Treasury team confirms the payment in LMS (Waiver BRD).</li>
<li>Next login in LOS → the Curated Offers page shows a fresh product card.</li>
</ol>
<h2>8. Status changes</h2>
<table class="brd-table"><thead><tr><th>From</th><th>To</th><th>When</th><th>By</th></tr></thead><tbody>
<tr><td>DRAFT (not pledged)</td><td>INACTIVE</td><td>30 days from the LAN generated date without a pledge</td><td>System (automatic)</td></tr>
<tr><td>DRAFT (pledged)</td><td>REJECTED</td><td>OPS rejects (after 30 days, or earlier on the customer’s request)</td><td>OPS L1 (below ₹5 lakh) / L2 or L3 (₹5 lakh and above) – new</td></tr>
<tr><td>SUBMITTED</td><td>REJECTED</td><td>OPS rejects the Loan Account Opening</td><td>OPS user – existing</td></tr>
<tr><td>ACTIVE</td><td>CLOSED</td><td>Foreclosure, tenure completion or invocation</td><td>Existing</td></tr>
</tbody></table>
<h2>9. System impact</h2>
<table class="brd-table"><tbody>
<tr><th>LMS</th><td>Approvals section with Reject for a pledged DRAFT LAN (OPS L1 below ₹5 lakh, L2 / L3 for ₹5 lakh and above); rejection reason captured and recorded in the
Audit; status DRAFT → REJECTED; de-pledge allowed for the REJECTED LAN; no automatic expiry for a pledged DRAFT LAN; the automatic
DRAFT → INACTIVE move for an unpledged LAN after 30 days.</td></tr>
<tr><th>LOS</th><td>After the rejection, the Curated Offers page shows a fresh product card on the next login (no “Continue” of the rejected application).</td></tr>
<tr><th>UNO</th><td>No accounting entry for the rejection itself. When the customer pays the charges, the entry is posted as per the Waiver BRD.</td></tr>
<tr><th>Customer communication</th><td>On rejection: loan application rejected, units still lien-marked (template to be created).</td></tr>
</tbody></table>
<h2>10. Open points</h2>
<ul>
<li>Customer communication when an unpledged DRAFT LAN moves to INACTIVE – to be decided later.</li>
<li>The existing “Application Expired – Lien Marked” communication (Day 31) – on hold (a pledged DRAFT LAN no longer expires automatically).</li>
<li>Rejection reasons: free text now; a fixed list of reasons in a later phase.</li>
</ul>
"""

BRDS = [
    {"slug": "waive-off", "title": "Waiver of Charges and Processing Fee", "status": "Draft", "updated": "16-11-2026",
     "summary": "One common process to waive the charges fully, partially or not at all, collect the balance from the customer "
                "and allow the de-pledge only after Treasury confirms the payment.",
     "body": _waiver_body()},
    {"slug": "draft-lan-rejection", "title": "DRAFT LAN Rejection", "status": "Draft", "updated": "16-11-2026",
     "summary": "Reject a loan application in DRAFT status in LMS when the mutual fund units are pledged (DRAFT → REJECTED, "
                "then de-pledge); unpledged DRAFT LANs move to INACTIVE after 30 days.",
     "body": DRAFT_REJECTION},
]
