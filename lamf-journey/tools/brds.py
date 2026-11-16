"""BRD documents (DISC-269) – listed on brd.html (home CTA “Open BRD document”); each BRD opens brd-<slug>.html.

Add a BRD here: slug (file name), title, status, last updated (DD-MM-YYYY), one-line summary and the body (HTML;
empty = “content to be added”).
"""

TBD = '<span class="brd-tbd">To be defined</span>'
PROP = '<span class="brd-prop">Proposed</span>'

# Waiver of Charges and Processing Fee (DISC-270): the 7 drop-off scenarios after lien marking.
# (No, drop-off stage, how the case ends, charges incurred) – scenario list proposed by Claude, to be confirmed by the owner.
WAIVER_SCENARIOS = [
    (1, "After lien marking – before the Sanction Letter (Agreement and E-Mandate page)",
     "No action for 30 days → application expires (Day 31) → lien removal", "Lien marking, Lien removal"),
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

def _waiver_body():
    rows = "".join(f"<tr><td class='c'>{n}</td><td>{st}</td><td>{end}</td><td>{ch}</td></tr>" for n, st, end, ch in WAIVER_SCENARIOS)
    impact = lambda n: (
        "<table class='brd-table'><thead><tr><th>System</th><th>With waive-off (SCCL bears the charges)</th>"
        "<th>Without waive-off (customer pays the charges)</th></tr></thead><tbody>"
        f"<tr><th>LOS</th><td>{TBD}</td><td>{TBD}</td></tr>"
        f"<tr><th>LMS</th><td>{TBD}</td><td>{TBD}</td></tr>"
        f"<tr><th>UNO</th><td>{TBD}</td><td>{TBD}</td></tr>"
        f"<tr><th>Customer communication</th><td>{TBD}</td><td>{TBD}</td></tr></tbody></table>")
    scen = "".join(f"<h3>Scenario {n} – {st}</h3><p><b>How the case ends:</b> {end}<br><b>Charges incurred:</b> {ch}</p>{impact(n)}"
                   for n, st, end, ch in WAIVER_SCENARIOS)
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
<tr><td>Lien marking charge</td><td>When the units are pledged (lien marked)</td><td>{TBD}</td><td>{TBD}</td></tr>
<tr><td>Lien removal charge</td><td>When the lien is removed after a drop-off, rejection or closure</td><td>{TBD}</td><td>{TBD}</td></tr>
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
<li>Accounting entries in UNO for the waived charges and the recovered charges.</li></ul>
"""

BRDS = [
    {"slug": "waive-off", "title": "Waiver of Charges and Processing Fee", "status": "Draft", "updated": "16-11-2026",
     "summary": "Charges incurred when the customer drops off after the lien marking – with and without waive-off, "
                "and the impact on LOS, LMS and UNO.",
     "body": _waiver_body()},
]
