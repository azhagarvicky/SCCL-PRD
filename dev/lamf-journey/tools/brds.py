"""BRD documents (DISC-269) – listed on brd.html (home CTA “Open BRD document”); each BRD opens brd-<slug>.html.

Add a BRD here: slug (file name), title, status, last updated (DD-MM-YYYY), one-line summary and the body (HTML;
empty = “content to be added”).
"""

TBD = '<span class="brd-tbd">To be defined</span>'
PROP = '<span class="brd-prop">Proposed</span>'

# Waiver of Charges and Processing Fee (DISC-270): the 7 drop-off scenarios after lien marking.
# (No, drop-off stage, how the case ends, charges incurred) – scenario list proposed by Claude, to be confirmed by the owner.
WAIVER_SCENARIOS = [
    (1, "After lien marking – Sanction Letter not generated (Loan Application Status: DRAFT)",
     "OPS rejects the DRAFT LAN in LMS (Approvals tab) with full, partial or no waive-off of the charges", "Lien marking (₹531), Lien removal (₹118)"),
    (2, "After the Sanction Letter – before the Loan Agreement e-Sign",
     "No action for 30 days → application expires → lien removal", "Lien marking, Lien removal"),
    (3, "After the Loan Agreement e-Sign – before / failed E-Mandate",
     "E-Mandate not completed in 30 days → application expires → lien removal", "Lien marking, Lien removal"),
    (4, "Customer asks to cancel the application after lien marking",
     "Cancelled on the customer's request → lien removal", "Lien marking, Lien removal"),
    (5, "Application submitted – Loan Account Opening rejected by OPS",
     "OPS rejects in LMS (Rejected with Charges / Rejected without Charges) → lien removal", "Lien marking, Lien removal, Processing fee (if levied)"),
    (6, "Account opened – Loan Lodgement rejected by OPS",
     "OPS rejects in LMS (Rejected with Charges / Rejected without Charges) → lien removal", "Lien marking, Lien removal, Processing fee"),
    (7, "Loan account active – no withdrawal, customer asks to close",
     "Closure on request without any disbursement → lien removal", "Lien marking, Lien removal, Processing fee"),
]

# Scenario detail given by the owner (DISC-271)
SCENARIO_DETAIL = {1: """
<h4>LMS – Approvals tab for a DRAFT LAN</h4>
<ul>
<li>In LMS, the LAN details have the tabs Overview, Approvals, Disbursement &amp; Repayments, Collateral, Transactions &amp; Reports, KYC,
Documents, Audit, Notes. <b>Approvals is not available for a DRAFT LAN today – it has to be added</b> for the DRAFT loan section.</li>
<li>Under Approvals, a charges table (below) and the <b>Reject</b> CTA at the bottom of the same page.</li>
</ul>
<table class="brd-table"><thead><tr><th>Column</th><th>Behaviour</th></tr></thead><tbody>
<tr><th>Checkbox</th><td>Select all (header) or select each charge individually. Only a selected charge can be waived.</td></tr>
<tr><th>Charges Name</th><td>The charges incurred for the LAN: Lien Marking Charges, Lien Removal Charges, and a Total row.</td></tr>
<tr><th>Amount of Charges</th><td>Lien Marking ₹531, Lien Removal ₹118, Total ₹649 (read only).</td></tr>
<tr><th>Amount to be waived off</th><td>Entered by the OPS user for a selected charge – from 0 up to the Amount of Charges (full or partial waive-off,
e.g. ₹500 of ₹531). Default 0.</td></tr>
<tr><th>Payable Charges</th><td>Amount of Charges − Amount to be waived off, per charge and in total (Total highlighted).</td></tr>
</tbody></table>
<figure class="brd-fig"><img src="assets/img/brd/waiver-charges-table.png" alt="Charges table – Checkbox, Charges Name, Amount of Charges, Amount to be waived off, Payable Charges">
<figcaption>Charges table (reference shared by the owner)</figcaption></figure>
<h4>Reject and confirmation</h4>
<p>The OPS user clicks <b>Reject</b> → confirmation pop-up “This action is irreversible. Are you sure you want to proceed?” with
<b>No</b> (closes the pop-up) and <b>Yes</b> (confirms the rejection) and a close ×.</p>
<figure class="brd-fig sm"><img src="assets/img/brd/waiver-confirm-popup.png" alt="Confirmation pop-up – This action is irreversible. Are you sure you want to proceed? No / Yes">
<figcaption>Confirmation pop-up (reference shared by the owner)</figcaption></figure>
<h4>Flow after Yes</h4>
<table class="brd-table"><thead><tr><th></th><th>Total Payable Charges = 0 (full waive-off)</th><th>Total Payable Charges &gt; 0 (partial or no waive-off)</th></tr></thead><tbody>
<tr><th>Approval</th><td>No second approval – rejected directly.</td>
<td>Goes for approval: shown in the same LAN’s <b>Approvals</b> tab and in the separate <b>Approvals</b> section of the hamburger menu,
approval type <b>Partial Waive-off Rejection</b>. Another OPS user can <b>Accept Rejection</b> or <b>Cancel Rejection</b>.</td></tr>
<tr><th>LMS – LAN status</th><td>DRAFT → <b>REJECTED</b>; the LAN moves to the <b>Rejected</b> section.</td>
<td>Accept Rejection: DRAFT → <b>REJECTED</b>, LAN moves to the Rejected section. Cancel Rejection: {TBD} (LAN stays DRAFT?).</td></tr>
<tr><th>Charges</th><td>Borne by SCCL (fully waived).</td><td>The customer pays the Total Payable Charges through the payment link; the waived part is borne by SCCL.</td></tr>
<tr><th>Lien</th><td>{TBD} (lien removal triggered on rejection?)</td><td>The units stay lien-marked until the customer pays; lien removal after the payment.</td></tr>
<tr><th>Customer communication (SMS and mail – to be created)</th>
<td>“Dear AZHAGARSAMY, We regret that your Loan Against Mutual Fund application could not be approved. For assistance, please contact our support team - Shriram Credit”</td>
<td>On Accept Rejection: “Dear AZHAGARSAMY, We regret that your Loan Against Mutual Fund application rejected. Your Mutual Fund units remain lien-marked.
Please pay the applicable charges (processing fee, lien marking and lien removal) of Rs. 92,313 using this link: https://lamf.shriramcredit.in/ to Lien removal - Shriram Credit”</td></tr>
<tr><th>LOS</th><td>{TBD}</td><td>{TBD}</td></tr>
<tr><th>UNO</th><td>{TBD}</td><td>{TBD}</td></tr>
</tbody></table>
"""}
SCENARIO_DETAIL = {k: v.replace("{TBD}", TBD) for k, v in SCENARIO_DETAIL.items()}

def _waiver_body():
    rows = "".join(f"<tr><td class='c'>{n}</td><td>{st}</td><td>{end}</td><td>{ch}</td></tr>" for n, st, end, ch in WAIVER_SCENARIOS)
    impact = lambda n: (
        "<table class='brd-table'><thead><tr><th>System</th><th>With waive-off (SCCL bears the charges)</th>"
        "<th>Without waive-off (customer pays the charges)</th></tr></thead><tbody>"
        f"<tr><th>LOS</th><td>{TBD}</td><td>{TBD}</td></tr>"
        f"<tr><th>LMS</th><td>{TBD}</td><td>{TBD}</td></tr>"
        f"<tr><th>UNO</th><td>{TBD}</td><td>{TBD}</td></tr>"
        f"<tr><th>Customer communication</th><td>{TBD}</td><td>{TBD}</td></tr></tbody></table>")
    scen = "".join(f"<h3>Scenario {n} – {st}</h3><p><b>How the case ends:</b> {end}<br><b>Charges incurred:</b> {ch}</p>"
                   + (SCENARIO_DETAIL[n] if n in SCENARIO_DETAIL else impact(n)) for n, st, end, ch in WAIVER_SCENARIOS)
    return f"""
<h2>1. Background</h2>
<p>In the LAMF LOS journey the customer pledges the mutual fund units (lien marking) before the loan account is opened.
When the customer drops off after the lien marking, charges are incurred for the lien marking and the lien removal.
Who pays these charges is not decided yet, so today <b>SCCL bears them</b>.</p>
<h2>2. Objective</h2>
<p>Define, for every drop-off scenario after the lien marking, the charges that are incurred and two options –
<b>with waive-off</b> (SCCL bears the charges) and <b>without waive-off</b> (the charges are recovered from the customer) –
and how each option works in <b>LOS</b>, <b>LMS</b> and <b>UNO</b>.</p>
<h2>3. Scope</h2>
<ul><li>In scope: drop-offs after the lien marking (pledge) – {len(WAIVER_SCENARIOS)} scenarios below; the lien marking charge,
the lien removal charge and the processing fee; the waive-off / recovery flow in LOS, LMS and UNO; customer communication.</li>
<li>Out of scope: drop-offs before the lien marking (no charge is incurred).</li></ul>
<h2>4. Charges</h2>
<table class="brd-table"><thead><tr><th>Charge</th><th>When it is incurred</th><th>Amount</th><th>GST</th></tr></thead><tbody>
<tr><td>Lien marking charge</td><td>When the units are pledged (lien marked)</td><td>₹531</td><td>Included? (₹450 + 18% = ₹531) – to be confirmed</td></tr>
<tr><td>Lien removal charge</td><td>When the lien is removed after a drop-off, rejection or closure</td><td>₹118</td><td>Included? (₹100 + 18% = ₹118) – to be confirmed</td></tr>
<tr><td>Processing fee</td><td>{TBD}</td><td>{TBD}</td><td>{TBD}</td></tr></tbody></table>
<h2>5. Scenarios {PROP}</h2>
<p class="brd-note">The {len(WAIVER_SCENARIOS)} scenarios below are proposed from the current LOS journey – to be confirmed.</p>
<table class="brd-table"><thead><tr><th>#</th><th>Drop-off stage</th><th>How the case ends</th><th>Charges incurred</th></tr></thead>
<tbody>{rows}</tbody></table>
<h2>6. Scenario-wise flow and impact</h2>
{scen}
<h2>7. Open points</h2>
<ul><li>Confirm the {len(WAIVER_SCENARIOS)} scenarios and the charges in each.</li>
<li>Amount and GST of each charge; whether the processing fee is levied before the loan account is opened.</li>
<li>Who decides waive-off or recovery (per case or by rule), and where it is recorded (LOS / LMS).</li>
<li>How the charges are recovered when not waived (payment link, before the lien removal or after) and what happens if the customer does not pay.</li>
<li>Accounting entries in UNO for the waived charges and the recovered charges.</li>
<li>Scenario 1: what happens on Cancel Rejection; whether the lien removal starts on a full waive-off rejection; the impact in LOS
(status shown to the customer); the payment-link SMS lists “processing fee” and Rs. 92,313 – for Scenario 1 only lien marking and
lien removal apply (₹649 or less), so the SMS text / amount to be confirmed.</li>
<li>Are ₹531 and ₹118 inclusive of 18% GST (₹450 and ₹100 + GST)?</li></ul>
"""

BRDS = [
    {"slug": "waive-off", "title": "Waiver of Charges and Processing Fee", "status": "Draft", "updated": "16-11-2026",
     "summary": "Charges incurred when the customer drops off after the lien marking – with and without waive-off, "
                "and the impact on LOS, LMS and UNO.",
     "body": _waiver_body()},
]
