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

# ---------------------------------------------------------------------------------------------------------------------------
# BRD – Part Payment & Preclosure (DISC-281): from the owner's Part_Payment__Preclosure_BRD.docx and process flow diagram.
# Marked Completed by the owner.
# ---------------------------------------------------------------------------------------------------------------------------
PART_PAYMENT_PRECLOSURE = """
<h2>1. Overview</h2>
<p>The customer can pay towards the loan in LOS in two ways: a part payment or a preclosure. This BRD covers the changes in LOS,
the apportioning and accounting, the email notification, and the preclosure process in LMS.</p>
<h2>2. Process flow</h2>
<figure class="brd-fig wide"><img src="assets/img/brd/part-payment-preclosure-flow.jpg" alt="Part payment and preclosure process flow in LOS and LMS">
<figcaption>Part payment and preclosure – process flow in LOS and LMS</figcaption></figure>
<h2>3. Changes in LOS</h2>
<ul>
<li>A new field called Payment type is given to the customer with two options to choose from: Part payment and Preclosure.</li>
<li><b>Part payment:</b> the customer enters the amount to pay. The amount cannot be more than the sum of the overdue interest,
overdue charges, due interest, due charges and O/S principal.</li>
<li><b>Preclosure:</b> the amount to pay is prefilled and cannot be edited. It is the sum of the overdue interest, overdue charges,
due interest, due charges, O/S principal and accrued interest.</li>
</ul>
<table class="brd-table"><thead><tr><th>Amount made up of</th><th>Part payment (editable, up to the total)</th><th>Preclosure (prefilled, not editable)</th></tr></thead><tbody>
<tr><td>Overdue interest</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>Overdue charges</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>Due interest</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>Due charges</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>O/S principal</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>Accrued interest</td><td class="c">–</td><td class="c">✓</td></tr>
</tbody></table>
<h2>4. Apportioning logic and accounting</h2>
<ul>
<li>The apportioning logic stays the same and is applied on the payment made.</li>
<li><b>Part payment:</b> the accrued interest is not included in the amount the customer pays. It is posted separately on the 1st of the month.</li>
<li><b>Preclosure:</b> the accrued interest collected is settled directly to the Interest Income GL code, as this amount is not yet
posted to the customer’s account.</li>
<li>Any excess payment is settled to the Preclosure Liability GL code and is refunded to the customer. Normally this does not happen,
as both payment types restrict the amount.</li>
</ul>
<h2>5. Email notification</h2>
<ul><li>An email goes to the Ops and Accounts teams whenever the customer makes a part payment or a preclosure.</li></ul>
<h2>6. After a part payment</h2>
<ul><li>The loan account stays ACTIVE.</li></ul>
<h2>7. Preclosure process in LMS</h2>
<ol class="brd-flow">
<li>Ops L1 starts the preclosure process after receiving the email about the preclosure payment, and only when the pending dues are 0.</li>
<li>If the pending dues are more than 0, the customer has to pay the remaining amount before the closure can go ahead.</li>
<li>If the pending dues are less than 0 (excess payment), the Accounts team is told about the excess payment so that it can be refunded.
Once Accounts refunds it, the refund is updated in LMS with the UTR number to clear the excess payment.</li>
<li>The preclosure request started by Ops L1 goes to the Accounts team (L1, L2 and L3) for review and approval.</li>
<li>After the Accounts approval, the final approval goes to Ops L2 and L3. The revocation (de-pledge) of the units is started at the same time.</li>
<li>After the final approval, the loan closure email and the NOC are sent to the customer.</li>
</ol>
<h2>8. System impact</h2>
<table class="brd-table"><tbody>
<tr><th>LOS</th><td>Payment type field (Part payment / Preclosure); editable amount up to the total for a part payment; prefilled, non-editable amount for a preclosure.</td></tr>
<tr><th>LMS</th><td>Apportioning of the payment; Ops L1 preclosure start when dues are 0; Accounts L1 / L2 / L3 review and approval; Ops L2 / L3 final
approval; revocation in parallel; refund update with the UTR number for an excess payment.</td></tr>
<tr><th>Accounting</th><td>Accrued interest on preclosure to the Interest Income GL; excess payment to the Preclosure Liability GL and refunded.</td></tr>
<tr><th>Communication</th><td>Email to Ops and Accounts on every part payment and preclosure; loan closure email and NOC to the customer after the final approval.</td></tr>
</tbody></table>
"""

DYNAMIC_PRICING = """
<h2>1. Business requirement</h2>
<p>The rate of interest (ROI) for a customer is worked out with this formula:</p>
<p><b>Final ROI = Base interest rate + Bureau incremental rate + Equity % of portfolio incremental rate</b></p>
<p>The system works out each part on its own, using the rules below, and shows the calculation to the customer in a simple,
easy-to-understand way.</p>
<h2>2. Parts of the ROI</h2>
<h3>2.1 Base interest rate</h3>
<p>The base interest rate depends on the sanctioned loan amount.</p>
<table class="brd-table"><thead><tr><th>Loan amount</th><th>Base interest rate</th></tr></thead><tbody>
<tr><td>Below ₹10 lakh</td><td class="c">10.50%</td></tr>
<tr><td>₹10 lakh to below ₹50 lakh</td><td class="c">10.30%</td></tr>
<tr><td>₹50 lakh to below ₹1 crore</td><td class="c">10.00%</td></tr>
<tr><td>₹1 crore to below ₹2 crore</td><td class="c">9.75%</td></tr>
<tr><td>₹2 crore to below ₹100 crore</td><td class="c">9.60%</td></tr>
<tr><td>₹100 crore and above</td><td class="c">9.50%</td></tr>
</tbody></table>
<h3>2.2 Bureau incremental rate</h3>
<p>An extra rate is added based on the customer’s bureau score.</p>
<table class="brd-table"><thead><tr><th>Bureau score</th><th>Incremental rate</th></tr></thead><tbody>
<tr><td>650 to 900</td><td class="c">0.00%</td></tr>
<tr><td>550 to 649</td><td class="c">0.30%</td></tr>
<tr><td>300 to 549</td><td class="c">0.40%</td></tr>
<tr><td>Below 300</td><td class="c">0.25%</td></tr>
<tr><td>NA (score not available)</td><td class="c">0.25%</td></tr>
<tr><td>NH (no history / new to credit)</td><td class="c">0.25%</td></tr>
</tbody></table>
<p>Rules:</p>
<ul>
<li>The system picks up the bureau score available for the customer.</li>
<li>The score is matched to its bucket in the table above.</li>
<li>For NA or NH customers, the incremental rate is 0.25%.</li>
<li>The customer is shown the bureau score (or the NA / NH status), the bucket and the incremental rate.</li>
</ul>
<h3>2.3 Equity % of portfolio incremental rate</h3>
<p>The equity % of the portfolio is worked out from the collateral value of the pledged mutual funds:</p>
<p><b>Equity % of portfolio = (Collateral value of the equity mutual funds ÷ Collateral value of all the mutual funds) × 100</b></p>
<ul>
<li>Top part: the total collateral value of the equity mutual funds.</li>
<li>Bottom part: the total collateral value of all the eligible pledged mutual funds, that is equity, hybrid and debt funds.</li>
</ul>
<p>The percentage is then matched to this grid:</p>
<table class="brd-table"><thead><tr><th>Equity % of portfolio</th><th>Incremental rate</th></tr></thead><tbody>
<tr><td>0% to below 70%</td><td class="c">0.00%</td></tr>
<tr><td>70% to below 85%</td><td class="c">0.10%</td></tr>
<tr><td>85% to 100%</td><td class="c">0.20%</td></tr>
</tbody></table>
<h2>3. Approved Securities master</h2>
<ul>
<li>The Approved Securities list holds the type of each approved mutual fund.</li>
<li>A new column, <b>Type of mutual fund</b>, is added in the Collateral section. The same column is added to the download template
and to the upload.</li>
<li>The column takes one of three values: Equity, Hybrid or Debt.</li>
</ul>
<table class="brd-table"><thead><tr><th>Fund</th><th>Type of mutual fund</th></tr></thead><tbody>
<tr><td>Fund A</td><td>Equity</td></tr>
<tr><td>Fund B</td><td>Hybrid</td></tr>
<tr><td>Fund C</td><td>Debt</td></tr>
</tbody></table>
<h2>4. Example</h2>
<p>Customer details:</p>
<table class="brd-table"><tbody>
<tr><th>Sanctioned loan amount</th><td>₹75 lakh</td></tr>
<tr><th>Bureau score</th><td>620</td></tr>
<tr><th>Total collateral value</th><td>₹1 crore</td></tr>
<tr><th>Equity funds collateral value</th><td>₹60 lakh</td></tr>
<tr><th>Hybrid funds collateral value</th><td>₹10 lakh</td></tr>
<tr><th>Debt funds collateral value</th><td>₹30 lakh</td></tr>
</tbody></table>
<table class="brd-table"><thead><tr><th>Step</th><th>Working</th><th>Rate</th></tr></thead><tbody>
<tr><td>1. Base interest rate</td><td>₹75 lakh falls in the ₹50 lakh to below ₹1 crore bucket.</td><td class="c">10.00%</td></tr>
<tr><td>2. Bureau incremental rate</td><td>Score 620 falls in the 550 to 649 bucket.</td><td class="c">0.30%</td></tr>
<tr><td>3. Equity % of portfolio</td><td>Equity + hybrid = ₹60 lakh + ₹10 lakh = ₹70 lakh. ₹70 lakh ÷ ₹1 crore × 100 = 70%,
which falls in the 70% to below 85% bucket.</td><td class="c">0.10%</td></tr>
<tr><td><b>4. Final ROI</b></td><td>10.00% + 0.30% + 0.10%</td><td class="c"><b>10.40%</b></td></tr>
</tbody></table>
<h2>5. When the BRE is called</h2>
<p>The Business Rule Engine (BRE) is called two times in the customer journey to work out the eligibility and the ROI.</p>
<h3>5.1 First call – after the CAMS fetch</h3>
<ul>
<li><b>When:</b> after the mutual fund holdings are fetched from CAMS.</li>
<li><b>Input:</b> the mutual fund data from CAMS and the other values needed for the calculation.</li>
<li><b>What the BRE does:</b> processes the holdings from CAMS, works out the eligible loan amount using the LTV, works out the ROI
from the inputs available, and returns the offer and eligibility details.</li>
<li><b>Result:</b> the output fills the Curated Offers screen / dashboard. The customer continues through the CTA “Basis the CAMS
Output” (or the CTA set up for this step).</li>
</ul>
<h3>5.2 Second call – on the Funds Selection page</h3>
<ul>
<li><b>When:</b> on the Funds Selection page, after the customer selects the mutual funds for the loan.</li>
<li><b>Why:</b> the funds the customer selects can be different from the holdings received from CAMS, so the eligibility and the ROI
have to be worked out again for the final selection.</li>
<li><b>Input:</b> the final list of selected funds and the other values needed.</li>
<li><b>What the BRE works out again:</b> the eligible loan amount, the equity % of portfolio, the base interest rate (when the loan
amount changes), the bureau incremental rate (as applicable) and the final ROI.</li>
<li><b>Result:</b> the new ROI replaces the ROI from the first call wherever the inputs have changed.</li>
</ul>
<h2>6. Change in fund selection</h2>
<ul><li>Any change the customer makes on the Funds Selection page that changes the mix of pledged mutual funds calls the BRE again.</li></ul>
<h2>7. Where the ROI is used</h2>
<p>The ROI is shown on these screens:</p>
<ul>
<li>Curated Offers screen</li>
<li>Loan Application Summary screen</li>
<li>Withdrawal screen</li>
<li>Loan Details tab on the dashboard</li>
<li>Key Facts Statement (KFS)</li>
</ul>
<p>The same ROI is used for:</p>
<ul>
<li>The repayment schedule</li>
<li>The repayment worked out for each disbursement</li>
<li>Any other repayment figure shown to the customer that needs the ROI</li>
</ul>
<p>The ROI shown on all these screens and the ROI used in the repayment calculations must always be the same.</p>
<h2>8. System impact</h2>
<table class="brd-table"><tbody>
<tr><th>BRE</th><td>ROI worked out as base rate + bureau rate + equity % rate; called after the CAMS fetch, on the Funds Selection page,
and again on any change in the selected funds.</td></tr>
<tr><th>LOS</th><td>ROI and its breakup shown on Curated Offers, Loan Application Summary, Withdrawal and the Loan Details tab;
the ROI from the second call replaces the first one where the inputs changed.</td></tr>
<tr><th>LMS</th><td>New column “Type of mutual fund” (Equity / Hybrid / Debt) in the Collateral section of the Approved Securities
master, and in its download template and upload.</td></tr>
<tr><th>Documents and repayment</th><td>The same ROI in the KFS, the repayment schedule and each disbursement’s repayment.</td></tr>
</tbody></table>
"""

RISK_STAGE = """
<h2>1. Requirement</h2>
<p>The system puts every active loan into a risk stage. The stage depends on how the loan outstanding compares with the collateral
value at each of the three LTV levels (L1, L2 and L3).</p>
<ul><li>Hybrid funds are treated as equity for this classification.</li></ul>
<h2>2. LTV levels</h2>
<p>As per the revised regulatory directions (revision of 22-09-2026), the LTV grid is as below. The equity values have changed;
the debt values stay the same.</p>
<table class="brd-table"><thead><tr><th>LTV level</th><th>Equity (incl. hybrid) – revised</th><th>Equity – earlier</th><th>Debt</th></tr></thead><tbody>
<tr><td>L1</td><td class="c"><mark>45%</mark></td><td class="c">65%</td><td class="c">75%</td></tr>
<tr><td>L2</td><td class="c"><mark>48%</mark></td><td class="c">68%</td><td class="c">78%</td></tr>
<tr><td>L3</td><td class="c"><mark>49%</mark></td><td class="c">73%</td><td class="c">83%</td></tr>
</tbody></table>
<h2>3. Collateral value at each level</h2>
<p>For each active loan, the system works out the current collateral value at each LTV level:</p>
<table class="brd-table"><tbody>
<tr><th>A1</th><td>Current collateral value at L1</td></tr>
<tr><th>A2</th><td>Current collateral value at L2</td></tr>
<tr><th>A3</th><td>Current collateral value at L3</td></tr>
</tbody></table>
<ul>
<li>Collateral value = Loan outstanding ÷ LTV of that level.</li>
<li>When a loan has more than one fund type, the equity or debt LTV is applied to each fund as per the approved collateral
classification and LTV logic.</li>
</ul>
<h2>4. Risk stage</h2>
<p>The loan outstanding is compared with A1, A2 and A3:</p>
<table class="brd-table"><thead><tr><th>Loan outstanding</th><th>Risk stage</th></tr></thead><tbody>
<tr><td>Less than A1</td><td>No Risk</td></tr>
<tr><td>A1 or more, but less than A2</td><td>Stage 1</td></tr>
<tr><td>A2 or more, but less than A3</td><td>Stage 2</td></tr>
<tr><td>A3 or more</td><td>Stage 3</td></tr>
</tbody></table>
<h2>5. Stage column in LMS</h2>
<ul>
<li>A new column, <b>Stage</b>, is added on the Active Loans page and the Shortfall page.</li>
<li>The stage is worked out every time from the latest loan outstanding and the current collateral value (NAV), so it always shows
the current position.</li>
</ul>
<h2>6. Shortfall and customer notification</h2>
<ul>
<li>Shortfall amount = Current outstanding – Collateral value at L1.</li>
<li>When a loan is in Stage 2, the customer gets an email and an SMS every day asking them to pledge more units or pay part of the principal.</li>
</ul>
<h2>7. System impact</h2>
<table class="brd-table"><tbody>
<tr><th>LMS</th><td>LTV grid L1 / L2 / L3 for equity (incl. hybrid) and debt; A1, A2 and A3 worked out for each active loan;
new Stage column on the Active Loans and Shortfall pages; shortfall amount against L1.</td></tr>
<tr><th>Communication</th><td>Daily email and SMS to the customer while the loan is in Stage 2.</td></tr>
</tbody></table>
<h2>8. Open points</h2>
<ol class="brd-flow">
<li>Formula: as written, Collateral value = Loan outstanding ÷ LTV, and then the loan outstanding is compared with that value.
Should A1, A2 and A3 instead be the loan amount allowed at each level (Current collateral value × LTV of that level), so that the
loan outstanding can be compared with them?</li>
<li>Communication for Stage 1 and Stage 3: is anything sent to the customer, or to Ops, at these stages?</li>
<li>Daily Stage 2 email and SMS: the content, the time of sending, and when it stops (for example, once the loan moves back to No Risk or Stage 1).</li>
</ol>
"""

ADDITIONAL_FUND_FETCH = """
<h2>1. Overview</h2>
<p>At onboarding, the customer’s mutual funds are fetched from MF Central using the mobile number and PAN given. A customer may
hold more funds under the same PAN that are registered with another mobile number or an email ID. This BRD covers the
<b>additional fund fetch</b>, where the customer gives a secondary mobile number or an email ID to fetch those funds too, and how it
flows into KYC, pledging and the loan.</p>
<h2>2. Process flow</h2>
<figure class="brd-fig wide"><a href="assets/img/brd/additional-fund-fetch-flow.jpg" target="_blank" rel="noopener"><img src="assets/img/brd/additional-fund-fetch-flow.jpg" alt="Additional fund fetch through a secondary mobile number or email ID – process flow"></a>
<figcaption>Additional fund fetch through a secondary mobile number or email ID – process flow for two profiles on the same mobile number (click to open full size)</figcaption></figure>
<h2>3. Same mobile number with two PANs</h2>
<ul>
<li>One validated mobile number (M1) can be used with two different PANs (P1 and P2).</li>
<li>Each mobile number + PAN pair is a separate profile: M1P1 and M1P2.</li>
<li>Each profile goes through its own fund fetch, additional fund fetch, KYC, pledging and loan, and gets its own LAN
(LAN 1 for M1P1, LAN 2 for M1P2).</li>
<li>The funds of one profile are never mixed with the funds of the other.</li>
</ul>
<h2>4. First fund fetch</h2>
<ul>
<li>The customer onboards with the mobile number (M1) and the PAN (P1).</li>
<li>The funds are fetched from MF Central for M1 + P1 and the eligibility is worked out. Example: Funds A, B and C.</li>
</ul>
<h2>5. Additional fund fetch</h2>
<p>The customer can then ask for an additional fund fetch by giving another mobile number or an email ID. The funds are fetched only
when the contact is linked with the same PAN. The outcomes are:</p>
<table class="brd-table"><thead><tr><th>Contact given</th><th>Linked with the PAN?</th><th>What happens</th><th>Example (profile M1P1)</th></tr></thead><tbody>
<tr><td>Same mobile number (M1)</td><td>Yes</td><td>Nothing new is fetched; the funds are already fetched.</td><td>Funds A, B, C (no change)</td></tr>
<tr><td>Secondary mobile number (M2)</td><td>Yes</td><td>The funds linked with M2 + P1 are fetched and the eligibility is worked out again.</td><td>Funds A, D, E</td></tr>
<tr><td>Email ID (E1)</td><td>Yes</td><td>The funds linked with E1 + P1 are fetched and the eligibility is worked out again. Funds already fetched are not added again.</td><td>Funds A, B, C, D, E</td></tr>
<tr><td>Mobile number (M3) or email ID (E2)</td><td>No</td><td>No funds are available for this contact and PAN. The customer continues with the funds already fetched.</td><td>No new funds</td></tr>
</tbody></table>
<ul>
<li>A fund that comes back in more than one fetch (for example, Fund A) is shown only once.</li>
<li>After every additional fund fetch, the eligibility is worked out again on the full list of funds.</li>
<li>For profile M1P2 the same rules apply to its own funds. Example: first fetch X, Y, Z; M2 gives X, U, V; E1 gives X, Y, Z, U, V.</li>
</ul>
<h2>6. Dedupe check</h2>
<table class="brd-table"><thead><tr><th>Journey</th><th>When the dedupe check runs</th></tr></thead><tbody>
<tr><td>Organic</td><td>After onboarding, before the MF Central fund fetch.</td></tr>
<tr><td>LSP</td><td>After the fund fetch and the additional fund fetch, before KYC.</td></tr>
</tbody></table>
<h2>7. KYC</h2>
<ul>
<li>If an email ID was used in the additional fund fetch, it is auto-filled in KYC and cannot be edited.</li>
<li>If more than one email ID was used in the additional fund fetch, the customer is shown radio buttons to choose one.</li>
</ul>
<h2>8. Pledging and loan</h2>
<ul>
<li>The funds are pledged giving priority to the contact that covers the most funds (the mutually inclusive contact). In the
example, this is the email ID E1, as it covers Funds A, B, C, D and E.</li>
<li>The customer then completes the sanction letter, the e-Agreement and the mandate, and the LAN is submitted
(LAN 1 for M1P1, LAN 2 for M1P2).</li>
</ul>
<h2>9. End to end flow</h2>
<ol class="brd-flow">
<li>The customer validates the mobile number (M1) and gives the PAN (P1 or P2).</li>
<li>Organic journey: dedupe check.</li>
<li>Funds are fetched from MF Central and the eligibility is worked out.</li>
<li>The customer can do an additional fund fetch with a secondary mobile number or an email ID linked with the same PAN; the eligibility is worked out again.</li>
<li>LSP journey: dedupe check.</li>
<li>KYC, with the email ID from the additional fund fetch auto-filled (or chosen, if more than one).</li>
<li>Pledging of the funds, giving priority to the mutually inclusive contact.</li>
<li>Sanction letter, e-Agreement and mandate; the LAN is submitted.</li>
</ol>
<h2>10. System impact</h2>
<table class="brd-table"><tbody>
<tr><th>LOS</th><td>Option for an additional fund fetch with a secondary mobile number or email ID; combined fund list without duplicates;
eligibility worked out again; email auto-filled and locked in KYC, or a radio button when there is more than one; two profiles on
one mobile number, each with its own LAN.</td></tr>
<tr><th>MF Central / BRE</th><td>Fund fetch for each contact + PAN; eligibility worked out again after every fetch.</td></tr>
<tr><th>Pledging</th><td>Pledge through the mutually inclusive contact first.</td></tr>
<tr><th>Dedupe</th><td>Before the fund fetch for Organic; before KYC for LSP.</td></tr>
</tbody></table>
<h2>11. Open points</h2>
<ol class="brd-flow">
<li>Is an OTP sent to the secondary mobile number or email ID before its funds are fetched?</li>
<li>How many additional fund fetches can the customer do in one application?</li>
<li>Pledging: when no single contact covers all the selected funds, are the remaining funds pledged through the other contacts?</li>
<li>In the diagram, the “No funds available” box of profile M1P2 reads “M3/E2 &amp; P1”; it should read “M3/E2 &amp; P2”.</li>
</ol>
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
    {"slug": "part-payment-preclosure", "title": "Part Payment & Preclosure", "status": "Completed", "updated": "16-11-2026",
     "summary": "Part payment and preclosure from LOS: payment type, amount rules, apportioning and accounting, notifications and "
                "the preclosure approval process in LMS.",
     "body": PART_PAYMENT_PRECLOSURE},
    {"slug": "dynamic-pricing", "title": "Dynamic Pricing", "status": "Completed", "updated": "16-11-2026",
     "summary": "Rate of interest worked out as base rate (by loan amount) + bureau rate (by score) + equity % of portfolio rate, "
                "calculated by the BRE after the CAMS fetch and again on fund selection, and kept the same across LOS, KFS and repayment.",
     "body": DYNAMIC_PRICING},
    {"slug": "loan-risk-stage", "title": "Loan Risk Stage Classification", "status": "Draft", "updated": "17-11-2026",
     "summary": "Every active loan is put into No Risk or Stage 1, 2 or 3 by comparing the loan outstanding with the collateral value "
                "at the L1, L2 and L3 LTV levels (revised grid of 22-09-2026), with a Stage column in LMS and daily alerts in Stage 2.",
     "body": RISK_STAGE},
    {"slug": "additional-fund-fetch", "title": "Additional Fund Fetch through Secondary Mobile Number", "status": "Draft", "updated": "17-11-2026",
     "summary": "Fetch more mutual funds under the same PAN using a secondary mobile number or email ID, re-work the eligibility, "
                "carry the email into KYC and pledge through the mutually inclusive contact; one mobile number can hold two PAN profiles.",
     "body": ADDITIONAL_FUND_FETCH},
]
