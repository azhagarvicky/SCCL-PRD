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
     "OPS rejects the DRAFT LAN in LMS – 1.1 without waive-off, 1.2 partial waive-off, 1.3 full waive-off", "Lien marking ₹531, Lien removal ₹118 (incl. 18% GST)"),
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
SCENARIO_DETAIL = {1: """<h4>Pre-conditions</h4>
<ul><li>The customer has pledged the mutual fund units (lien marked).</li>
<li>The Sanction Letter is not generated.</li>
<li>Loan Application Status: <b>DRAFT</b>.</li></ul>
<h4>Rules for Scenario 1</h4>
<ul>
<li>OPS can reject a <b>DRAFT</b> LAN in LMS and decide the charges at the same time (rejecting a DRAFT LAN is a new capability – not available today).</li>
<li>Charges (including 18% GST): Lien Marking Charge ₹531 (₹450 + ₹81 GST) and Lien Removal Charge ₹118 (₹100 + ₹18 GST) – total ₹649.</li>
<li>For each charge, OPS can waive the full amount, a part of it, or nothing. The amount waived cannot be more than the charge.</li>
<li>Payable charges = the charges minus the amount waived. SCCL bears the amount waived; the customer pays the payable charges.</li>
<li>Rejection needs one confirmation from the OPS user; once confirmed it is <b>final</b> – no second approval, and it cannot be undone.</li>
<li>On rejection the LAN status changes from DRAFT to <b>REJECTED</b> and the customer is informed by SMS and mail (templates to be created).</li>
</ul>
<h4>1.1 Without waive-off</h4><p><b>When:</b> OPS waives nothing – the customer pays all the charges (₹649).</p><ol class="brd-flow"><li>OPS rejects the DRAFT LAN without any waiver and confirms.</li><li>LAN status DRAFT → REJECTED.</li><li>Customer is informed of the rejection with the payable amount (₹649) and a payment link.</li><li>Customer pays ₹649 → lien removal.</li></ol><table class="brd-table"><tbody><tr><th>Borne by SCCL</th><td>₹0</td></tr><tr><th>Paid by customer</th><td>₹649</td></tr><tr><th>Lien</th><td>Stays marked until the customer pays; removed after the payment</td></tr><tr><th>Customer communication</th><td>Rejection with the payable amount and the payment link</td></tr></tbody></table><h4>1.2 With waive-off (Partial)</h4><p><b>When:</b> OPS waives a part of the charges – e.g. ₹500 of the Lien Marking Charge (₹531).</p><ol class="brd-flow"><li>OPS enters the amount waived for each charge and rejects, and confirms.</li><li>LAN status DRAFT → REJECTED.</li><li>Payable charges = ₹649 − ₹500 = ₹149 (₹31 Lien Marking + ₹118 Lien Removal).</li><li>Customer is informed of the rejection with the payable amount (₹149) and a payment link.</li><li>Customer pays ₹149 → lien removal.</li></ol><table class="brd-table"><tbody><tr><th>Borne by SCCL</th><td>The amount waived (₹500)</td></tr><tr><th>Paid by customer</th><td>The balance (₹149)</td></tr><tr><th>Lien</th><td>Stays marked until the customer pays; removed after the payment</td></tr><tr><th>Customer communication</th><td>Rejection with the payable amount and the payment link</td></tr></tbody></table><h4>1.3 With waive-off (Full)</h4><p><b>When:</b> OPS waives all the charges – payable charges ₹0.</p><ol class="brd-flow"><li>OPS waives both charges in full and rejects, and confirms.</li><li>LAN status DRAFT → REJECTED.</li><li>SCCL bears all the charges (₹649).</li><li>Customer is informed of the rejection – no payment link.</li><li>Lien removal {TBD}.</li></ol><table class="brd-table"><tbody><tr><th>Borne by SCCL</th><td>₹649</td></tr><tr><th>Paid by customer</th><td>₹0</td></tr><tr><th>Lien</th><td>{TBD} (removed at once on rejection?)</td></tr><tr><th>Customer communication</th><td>Rejection only – no payment link</td></tr></tbody></table>
<h4>System impact</h4>
<table class="brd-table"><tbody>
<tr><th>LMS</th><td>Rejection of a DRAFT LAN with the waiver for each charge; status DRAFT → REJECTED; payable charges collected by payment link; lien removal after the payment (on a full waive-off – to be defined).</td></tr>
<tr><th>LOS</th><td>{TBD}</td></tr>
<tr><th>UNO</th><td>{TBD} (booking of the charges, the amount waived and the amount received)</td></tr>
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
<tr><td>Lien marking charge</td><td>When the units are pledged (lien marked)</td><td>₹531</td><td>Included – ₹450 + ₹81 (18%)</td></tr>
<tr><td>Lien removal charge</td><td>When the lien is removed after a drop-off, rejection or closure</td><td>₹118</td><td>Included – ₹100 + ₹18 (18%)</td></tr>
<tr><td>Processing fee</td><td>{TBD}</td><td>{TBD}</td><td>{TBD}</td></tr></tbody></table>
<h2>5. Scenarios {PROP}</h2>
<p class="brd-note">The {len(WAIVER_SCENARIOS)} scenarios below are proposed from the current LOS journey – to be confirmed.</p>
<table class="brd-table"><thead><tr><th>#</th><th>Drop-off stage</th><th>How the case ends</th><th>Charges incurred</th></tr></thead>
<tbody>{rows}</tbody></table>
<h2>6. Scenario-wise flow and impact</h2>
{scen}
<h2>7. Open points</h2>
<ul><li>Confirm the {len(WAIVER_SCENARIOS)} scenarios and the charges in each.</li>
<li>Amount and GST of the processing fee, and whether it is levied before the loan account is opened.</li>
<li>Accounting entries in UNO for the waived charges and the recovered charges.</li>
<li>Scenario 1: whether the lien is removed at once on a full waive-off (1.3); the impact in LOS and UNO.</li>
<li>What happens if the customer does not pay the payable charges (time limit, follow-up, lien retained)?</li>
</ul>
"""

BRDS = [
    {"slug": "waive-off", "title": "Waiver of Charges and Processing Fee", "status": "Draft", "updated": "16-11-2026",
     "summary": "Charges incurred when the customer drops off after the lien marking – with and without waive-off, "
                "and the impact on LOS, LMS and UNO.",
     "body": _waiver_body()},
]
