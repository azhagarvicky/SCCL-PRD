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
     "OPS rejects the DRAFT LAN in LMS with full, partial or no waive-off of the charges", "Lien marking (₹531), Lien removal (₹118)"),
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

# Scenario detail given by the owner (DISC-271) – written as business logic, rules and conditions, not screen detail (DISC-272)
SCENARIO_DETAIL = {1: """
<h4>Pre-conditions</h4>
<ul><li>The customer has pledged the mutual fund units (lien marked).</li>
<li>The Sanction Letter is not generated.</li>
<li>Loan Application Status: <b>DRAFT</b>.</li></ul>
<h4>Business rules</h4>
<table class="brd-table"><tbody>
<tr><th>BR-1.1</th><td>OPS must be able to reject a <b>DRAFT</b> LAN in LMS and decide the charges at the same time (approval for a DRAFT LAN is a new capability – not available today).</td></tr>
<tr><th>BR-1.2</th><td>Charges applicable: Lien Marking Charge (₹531) and Lien Removal Charge (₹118) – total ₹649.</td></tr>
<tr><th>BR-1.3</th><td>Each charge can be waived <b>fully, partially or not at all</b>. Waiver amount per charge: 0 ≤ waiver ≤ charge amount.</td></tr>
<tr><th>BR-1.4</th><td>Payable charges = Σ (charge amount − waiver amount). SCCL bears the waived amount; the customer pays the payable charges.</td></tr>
<tr><th>BR-1.5</th><td>A rejection is irreversible and needs the OPS user’s confirmation.</td></tr>
<tr><th>BR-1.6</th><td><b>Payable = 0</b> (full waive-off): single-level – the LAN is rejected at once (DRAFT → REJECTED).</td></tr>
<tr><th>BR-1.7</th><td><b>Payable &gt; 0</b> (partial or no waive-off): maker-checker – the rejection needs the approval of a <b>second OPS user</b>
(approval type <b>Partial Waive-off Rejection</b>), who can approve or cancel it. The LAN becomes REJECTED only on approval.</td></tr>
<tr><th>BR-1.8</th><td>When payable &gt; 0, the units stay lien-marked until the customer pays; the lien is removed after the payment.</td></tr>
<tr><th>BR-1.9</th><td>The customer is informed by SMS and mail on rejection – without a payment link when payable = 0, with the payable amount and a payment link when payable &gt; 0 (templates to be created).</td></tr>
</tbody></table>
<h4>Flow</h4>
<ol class="brd-flow">
<li>OPS selects the DRAFT LAN for rejection and reviews the charges (₹531 + ₹118).</li>
<li>OPS decides the waiver for each charge (full / partial / none) → payable charges are worked out.</li>
<li>OPS rejects and confirms.</li>
<li><b>If payable = 0</b> → LAN DRAFT → REJECTED → SCCL bears all charges → customer informed (no payment link) → lien removal {TBD}.</li>
<li><b>If payable &gt; 0</b> → rejection goes for approval (Partial Waive-off Rejection) → a second OPS user:
  <ul><li><b>Approves</b> → LAN DRAFT → REJECTED → customer informed with the payable amount and payment link → customer pays → lien removal.
  SCCL bears the waived part.</li>
  <li><b>Cancels</b> → {TBD} (LAN stays DRAFT; waiver discarded?).</li></ul></li>
</ol>
<h4>Outcome by condition</h4>
<table class="brd-table"><thead><tr><th>Condition</th><th>Approval</th><th>LAN status</th><th>Borne by SCCL</th><th>Paid by customer</th><th>Lien</th><th>Customer communication</th></tr></thead><tbody>
<tr><td>Full waive-off (payable = 0)</td><td>Single level</td><td>DRAFT → REJECTED</td><td>₹649</td><td>₹0</td><td>{TBD}</td><td>Rejection, no payment link</td></tr>
<tr><td>Partial waive-off (e.g. ₹500 of ₹531)</td><td>Maker-checker</td><td>DRAFT → REJECTED on approval</td><td>Waived amount (₹500)</td><td>Balance (₹149)</td><td>Removed after payment</td><td>Rejection with payable amount and payment link</td></tr>
<tr><td>No waive-off (payable = ₹649)</td><td>Maker-checker</td><td>DRAFT → REJECTED on approval</td><td>₹0</td><td>₹649</td><td>Removed after payment</td><td>Rejection with payable amount and payment link</td></tr>
<tr><td>Rejection cancelled by the second OPS user</td><td>–</td><td>{TBD}</td><td>–</td><td>–</td><td>Stays lien-marked</td><td>{TBD}</td></tr>
</tbody></table>
<h4>System impact</h4>
<table class="brd-table"><tbody>
<tr><th>LMS</th><td>Rejection of a DRAFT LAN with waiver per charge; maker-checker approval when payable &gt; 0; status DRAFT → REJECTED; payment link and lien removal after payment.</td></tr>
<tr><th>LOS</th><td>{TBD}</td></tr>
<tr><th>UNO</th><td>{TBD} (booking of the charges, the waived amount and the amount received)</td></tr>
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
<li>Scenario 1: what happens when the second OPS user cancels the rejection; whether the lien is removed at once on a full waive-off;
the impact in LOS and UNO; the payment-link communication has to state only the charges that apply (₹649 or less, no processing fee).</li>
<li>What happens if the customer does not pay the payable charges (time limit, follow-up, lien retained)?</li>
<li>Are ₹531 and ₹118 inclusive of 18% GST (₹450 and ₹100 + GST)?</li></ul>
"""

BRDS = [
    {"slug": "waive-off", "title": "Waiver of Charges and Processing Fee", "status": "Draft", "updated": "16-11-2026",
     "summary": "Charges incurred when the customer drops off after the lien marking – with and without waive-off, "
                "and the impact on LOS, LMS and UNO.",
     "body": _waiver_body()},
]
