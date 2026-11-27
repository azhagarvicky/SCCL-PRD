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
CHARGES = [   # (charge, amount, when it is incurred) – amounts confirmed by the owner (DISC-289); GST at 18%
    # DISC-354 / DISC-356: from the Sanction Letter, Lien Marking, Lien Removal and Stamp Duty are included in the Processing Fee*;
    # before it (scenario 2 – pledged only) the Lien Marking and Lien Removal charges apply on their own
    ("Lien Marking Charge", "₹450 + GST (₹531)", "When the units are pledged (S 2 onwards). Full waive-off only."),
    ("Lien Removal Charge", "₹100 + GST (₹118)", "When the units are pledged (S 2 onwards). Full waive-off only."),
    ("Stamp Duty Charge", "₹200 + GST (₹236)", "From the Sanction Letter (S 3 onwards). Full waive-off only."),
    ("Processing Fee Charge", "Processing Fee* from the fee structure less ₹750 (Lien Marking ₹450 + Lien Removal ₹100 + Stamp Duty ₹200), + GST "
     "(sample ₹1,499 − ₹750 = ₹749 + GST = ₹883.82)", "From the Sanction Letter (S 3 onwards). Any amount can be waived."),
    ("Bounce Charge", "₹100 + GST (₹118) per instance", "Active loan, when an EMI bounces"),
    ("Penal Charge", "36% a year on the unpaid interest / EMI – no GST", "Active loan, on a delay or default"),
    ("Loan Renewal Charge", "₹999 + GST (₹1,178.82)", "Active loan, on renewal"),
    ("Annual Maintenance Charge (AMC)", "₹999 + GST (₹1,178.82)", "Active loan, every year"),
    ("Bank Swap Charge", "₹250 + GST (₹295)", "Active loan, when the repayment bank account is changed"),
]
LM, LR, PF, SD = "Lien Marking Charge", "Lien Removal Charge", "Processing Fee Charge", "Stamp Duty Charge"   # DISC-400
ACTIVE_CH = [PF, "Bounce Charge", "Penal Charge", "Loan Renewal Charge", "Annual Maintenance Charge (AMC)", "Bank Swap Charge"]

# The 7 scenarios from the owner's LAMF_Charges_Waiver_V1.xlsx (DISC-274) – outcomes, Product Construct and Treasury Remarks
# (accounting) per scenario. Layout on the owner's request (DISC-290): Purpose → Summary of scenarios → Common changes →
# each scenario with its accounting entries.
_PAY = "After payment and Treasury confirmation"
# Simple English, only the logic (DISC-380)
REJ_OUTCOMES = [   # (outcome, what happens, customer communication, de-pledge, accounting – UNO)
    ("Rejected – no waive-off", "Loan rejected without any waive-off. LAN → REJECTED.", "SMS and mail with the payment link.", _PAY,
     "Paid amount posted in UNO when received."),
    ("Rejected – partial waive-off", "Loan rejected and part of the charges waived. LAN → REJECTED.", "SMS and mail with the payment link for the balance.",
     _PAY, "Paid amount posted in UNO when received. Waived amount is not posted."),
    ("Rejected – full waive-off", "Loan rejected and all the charges waived. LAN → REJECTED.", "SMS and mail. No payment link.",
     "Right after the rejection", "No entry."),
]
def _approve(to):
    cm = "No communication." if to == "ACCOUNT OPENED" else "SMS and mail – loan lodgement approved."   # DISC-416
    return [("Approved – no waive-off", f"Loan approved without any waive-off. LAN → {to}. LMS shows the full charges; posted in UNO at the first withdrawal or repayment.", cm,
             "Not applicable – loan continues.", "Charges posted in UNO at the first withdrawal or repayment."),
            ("Approved – partial waive-off", f"Loan approved and part of the charges waived. LAN → {to}. LMS shows the reduced charges; posted in UNO at the first withdrawal or repayment.", cm,
             "Not applicable – loan continues.", "Waived amount is not posted."),
            ("Approved – full waive-off", f"Loan approved and all the charges waived. LAN → {to}. Nothing payable – no UNO entry.", cm,
             "Not applicable – loan continues.", "Waived amount is not posted.")]
def _approve_only(to):   # S 5.1 – Approve only, no waive-off with the approval (DISC-399)
    return [("Approved", f"Loan approved (Loan Account Opening), no waive-off. LAN → {to}. LMS shows the full charges; posted in UNO at the first withdrawal or repayment.",
             "No communication.", "Not applicable – loan continues.", "Charges posted in UNO at the first withdrawal or repayment.")]
WAIVER_SCENARIOS = [   # (No, LAN status, customer dropped off, charges, what OPS can do, outcomes)
    (1, "DRAFT", "Before pledging the mutual funds", [], "No action. The LAN moves to INACTIVE automatically on day 31.", []),
    (2, "DRAFT", "After pledging the mutual funds", [LM, LR], "Reject the loan, with or without waive-off.", REJ_OUTCOMES),
    (3, "DRAFT", "After the Sanction Letter is generated (units pledged)", [PF, LM, LR, SD], "Reject the loan, with or without waive-off.", REJ_OUTCOMES),
    (4, "DRAFT", "After the Loan Agreement e-Sign (units pledged, Sanction Letter generated and submitted)", [PF, LM, LR, SD], "Reject the loan, with or without waive-off.", REJ_OUTCOMES),
    (5, "SUBMITTED", "After the E-Mandate (units pledged, Sanction Letter submitted, Loan Agreement e-Signed)", [PF, LM, LR, SD],
     "Approve or reject the loan, with or without waive-off.", _approve("ACCOUNT OPENED") + REJ_OUTCOMES),   # S 5.1 – 5.3 approve again (DISC-412)
    (6, "ACCOUNT OPENED", "After the Loan Account Opening", [PF, LM, LR, SD], "Approve or reject the loan, with or without waive-off.", _approve("ACTIVE") + REJ_OUTCOMES),
    (7, "ACTIVE", "After the Loan Lodgement (loan account active)", ACTIVE_CH, "Waive-off only, from the ≡ menu. The loan can't be rejected at this stage.",
     [("Without waive-off", "Nothing waived. The charges stay in the SOA and are collected before the loan is closed.", "No communication.",
       "At loan closure.", "Charges posted in UNO when collected."),
      ("With full waive-off", "Full charge waived. The SOA is updated with a waiver narration.", "No communication.", "At loan closure.",
       "Waived amount is not posted."),
      ("With partial waive-off", "Part of the charge waived. The SOA is updated with a waiver narration. The balance is collected before the loan is closed.",
       "No communication.", "At loan closure.", "Waived amount is not posted.")]),
]


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
SUBMITTED and later statuses – the existing rejection applies; the charges on rejection – covered by the BRD “Charges Waiver &
Post-Pledge Drop-off”.</li></ul>
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
waive-off, the payment link and the de-pledging follow the BRD “Charges Waiver &amp; Post-Pledge Drop-off” (scenarios 2 – 4).</li>
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

SHORTFALL_EMI_DEFAULT = """
<h2>1. Overview</h2>
<p>This BRD covers what happens when a customer misses an EMI (EMI default) and when the value of the pledged funds falls below
what the loan needs (shortfall, also called LTV breach). It covers the charges, the re-presentation of the EMI, the customer
notifications, the withdrawal freeze, the invocation (sale) of the pledged units and the loan closure.</p>
<h2>2. EMI default</h2>
<ol class="brd-flow">
<li>The EMI is presented on the 5th of every month. If it bounces, it is presented again on the 10th of the same month.</li>
<li>A bounce charge of ₹100 + GST is levied for every bounce. Penal charges of 36% a year are levied on the unpaid interest / EMI
from the first day of default until the dues are paid.</li>
<li>The next EMI is presented as usual on its due date. The penal and bounce charges of the earlier default are posted to the
customer’s ledger and, if the customer does not pay them, are collected at the time of loan closure.</li>
<li>If the next EMI also bounces on its due date, it is presented again 5 days later (T+5).</li>
<li>If the T+5 re-presentation also bounces, the customer has missed the EMI for two months in a row. The funds are then sold
(invoked), the outstanding is settled, the loan is closed, and any amount left over after the sale is refunded to the customer.</li>
<li>For a loan closed through invocation, the pending interest, the charges, the outstanding principal and the lien removal
charges are recovered.</li>
<li>The invocation is done manually by the team, not triggered automatically by the system.</li>
<li>The customer gets an SMS and an email at every stage above.</li>
</ol>
<h2>3. Shortfall (LTV breach)</h2>
<p><b>LTV % = (Qualified loan amount ÷ Total loan outstanding) × 100</b></p>
<p>Qualified loan amount = sum of (latest collateral value of each fund × LTV of that fund type), where the LTV depends on whether
the fund is debt or equity.</p>
<table class="brd-table"><thead><tr><th>LTV %</th><th>What happens</th></tr></thead><tbody>
<tr><td>Reaches 90%</td><td>The customer gets an SMS and an email every day asking them to pay the shortfall amount or to pledge
more funds to cover it.</td></tr>
<tr><td>Between 90% and 75%</td><td>No invocation. The loan stays as it is even if the customer does not pay, unless there is an
internal decision to sell the units.</td></tr>
<tr><td>Reaches 75%</td><td>The funds are sold to recover the shortfall amount and the lien removal charges for every invocation.
The loan stays ACTIVE, because only the shortfall and its charges are recovered.</td></tr>
</tbody></table>
<ul>
<li>To cover the shortfall by payment, the customer pays the exact shortfall amount.</li>
<li>To cover the shortfall by pledging, the customer pledges funds worth 2 times the shortfall amount.</li>
<li>The invocation is done manually by the team, not triggered automatically by the system.</li>
</ul>
<h2>4. Withdrawal rules</h2>
<h3>4.1 During an LTV breach</h3>
<ul><li>The Withdraw option is disabled in LOS, as the drawing power is less than the outstanding amount.</li></ul>
<h3>4.2 During an EMI default</h3>
<ul>
<li>If the EMI bounces at the first presentation of any month, the account is frozen for withdrawal.</li>
<li>If the payment is received at the re-presentation, the freeze is released and the customer can withdraw again.</li>
<li>If the re-presentation also bounces, the customer cannot withdraw until they pay the dues.</li>
<li>Until the overdue interest / EMI is paid, the withdrawal stays frozen, even when the defaults are not in consecutive months.</li>
</ul>
<table class="brd-table"><thead><tr><th>Example (July)</th><th>Withdrawal</th></tr></thead><tbody>
<tr><td>EMI bounces on 5 July</td><td>Frozen</td></tr>
<tr><td>Payment received at the re-presentation on 10 July</td><td>Allowed again from 11 July</td></tr>
<tr><td>Re-presentation on 10 July also bounces</td><td>Stays frozen until the customer pays the dues</td></tr>
</tbody></table>
<h2>5. Invocation and revocation approval</h2>
<p>Every invocation and revocation goes through a maker and a checker, with OTP validation.</p>
<table class="brd-table"><thead><tr><th>Exposure</th><th>Role</th><th>Name</th><th>Email ID</th></tr></thead><tbody>
<tr><td rowspan="2">Any amount</td><td>Maker</td><td>Richa</td><td>richajayswal@shriramcredit.in</td></tr>
<tr><td>Checker / Approver</td><td>Satya</td><td>satyaparida@shriramcredit.in</td></tr>
</tbody></table>
<h2>6. Invocation reasons in LMS</h2>
<p>On the Invoke (Sell) page in LMS, the team chooses an invocation reason. The amount to be invoked depends on the reason.</p>
<table class="brd-table"><thead><tr><th>Invocation reason</th><th>Used when</th><th>Amount recovered</th><th>Loan after invocation</th></tr></thead><tbody>
<tr><td>Shortfall (already available)</td><td>LTV breach reaches 75%</td><td>Shortfall amount + lien removal charges</td><td>Stays ACTIVE</td></tr>
<tr><td>Loan Closure</td><td>Two EMIs missed in a row; or a bullet (balloon) loan where the customer cannot pay the principal at the end of the tenure</td>
<td>Total outstanding: principal, pending interest, charges and arrears, plus lien removal charges</td><td>CLOSED after settlement</td></tr>
<tr><td>Defaulted EMIs</td><td>An EMI default that is not in consecutive months</td><td>Interest, charges and arrears of the default</td><td>Stays ACTIVE</td></tr>
</tbody></table>
<h2>7. Loan closure through invocation</h2>
<ol class="brd-flow">
<li>The units are sold (redeemed) to recover the total outstanding amount.</li>
<li>The amount left over after recovery is refunded to the customer. It is recorded under Refund even when it is zero.</li>
<li>New fields under the Refund category, against the redemption details: UTR number, refund date and amount refunded.</li>
<li>The refund (points 2 and 3) is also posted in the customer ledger.</li>
<li>Once the total outstanding is recovered and the excess is refunded, the loan account is updated to CLOSED.</li>
<li>A loan can come into the revocation (de-pledge) window only when the total loan outstanding is 0, or is in credit because of an
excess payment.</li>
</ol>
<h2>8. System impact</h2>
<table class="brd-table"><tbody>
<tr><th>LMS</th><td>Presentation on the 5th and re-presentation on the 10th / T+5; bounce charge and penal charges posted to the ledger;
LTV % worked out daily; invocation reasons Shortfall, Loan Closure and Defaulted EMIs with the right amount for each; maker and
checker with OTP for invocation and revocation; Refund fields (UTR number, date, amount) and ledger entries; loan closed after
settlement; revocation only when the outstanding is 0 or in credit.</td></tr>
<tr><th>LOS</th><td>Withdraw disabled during an LTV breach; withdrawal frozen during an EMI default until the dues are paid.</td></tr>
<tr><th>Communication</th><td>SMS and email at every EMI default stage; daily SMS and email from 90% LTV until the shortfall is covered.</td></tr>
</tbody></table>
"""

SANCTION_AGREEMENT = """
<h2>1. Overview</h2>
<p>Two documents are generated for the customer from fixed formats (templates), with the customer and loan details filled in by
the system:</p>
<table class="brd-table"><thead><tr><th>Document</th><th>What it is</th><th>Format version</th></tr></thead><tbody>
<tr><td>In-principle e-Sanction Letter</td><td>The sanction letter with the Key Fact Statement (KFS), the APR working and the illustrative repayment schedule.</td><td>v1, 11-11-2026</td></tr>
<tr><td>Loan cum Pledge Agreement</td><td>The loan agreement between the customer and SCCL, with the schedule of charges, the risk disclosure and the loan application form.</td><td>v1, 11-11-2026</td></tr>
</tbody></table>
<p>This BRD lists what each document contains, the fields the system fills in, and the fixed values in the formats.</p>
<h2>2. Sanction letter</h2>
<h3>2.1 Letter</h3>
<ul>
<li>Date, customer name, correspondence address (three lines) and customer ID.</li>
<li>Subject: request for financial assistance of the sanctioned amount.</li>
<li>Body: in-principle e-sanction of a loan against mutual funds for the stated purpose, as per the KFS, available once the
documents are signed and the units are pledged / lien marked in favour of SCCL.</li>
<li>Support contact: lassupport@shriramcredit.in. Signed by Shriram Credit Company Limited.</li>
</ul>
<h3>2.2 Annexure A – Key Fact Statement</h3>
<p><b>Part 1 – Interest rate and fees / charges</b></p>
<table class="brd-table"><thead><tr><th>No.</th><th>Item</th><th>Shown as</th></tr></thead><tbody>
<tr><td>1</td><td>Type of loan; loan proposal / customer ID</td><td>Loan against pledge of mutual funds; LAN / customer ID</td></tr>
<tr><td>2–3</td><td>Sanctioned amount; loan term</td><td>From the loan</td></tr>
<tr><td>4</td><td>Instalment details</td><td>Monthly; interest dues = tenure (fixed); principal 1 (bullet at maturity); due amount; days to the first due</td></tr>
<tr><td>5</td><td>Rate of interest</td><td>Rate % a year, fixed</td></tr>
<tr><td>6 (a)</td><td>Fees payable to SCCL</td><td>Processing fee (one-time) + GST; loan renewal ₹999 + GST (annual); annual maintenance ₹999 + GST; bank swap ₹250 + GST</td></tr>
<tr><td>6 (b)</td><td>Payable to third parties through SCCL</td><td>Lien marking ₹450 + GST (one-time); lien removal ₹100 + GST (each event); stamp duty ₹200 + GST (as per the state – Tamil Nadu)</td></tr>
<tr><td>7</td><td>APR</td><td>APR % on the net disbursed amount, IRR and reducing balance method</td></tr>
<tr><td>8</td><td>Purpose of loan</td><td>From the application</td></tr>
<tr><td>9</td><td>Prescribed LTV</td><td>Up to 45% for equity units and 75% for debt units; a mix is worked out pro rata; to be kept for the whole tenure</td></tr>
<tr><td>10–12</td><td>Payment system; valuation; collateral</td><td>EMI or online payment and NACH; NAV declared by the AMC at the end of the previous day; open-ended mutual funds (and approved listed shares)</td></tr>
<tr><td>13</td><td>Contingent charges</td><td>Part payment nil; foreclosure nil; top-up / margin call with invocation and revocation charges; remedy on default (sale of units); bounce charge per instance; penal charge 36% a year on the unpaid interest / EMI</td></tr>
</tbody></table>
<p><b>Part 2 – Other information</b>: recovery agents (not applicable); grievance redressal (footnote 9); nodal grievance officer
(Satya Pravas Parida, Vice President – Lending Business, Mumbai office, +91 898-100-3538, grievanceredressal@shriramcredit.in);
transfer or securitisation (No); co-lending (not applicable); cooling-off period of 3 days from the sanction letter (cancel by
writing to lassupport@shriramcredit.in); LSP as recovery agent (not applicable); LSP grievance officer (filled in); working day
(bank working day).</p>
<h3>2.3 Annexure B – APR working</h3>
<p>Loan amount, term, instalment type and amount, number of instalments, days to the first due, rate type and rate, total interest
over the tenure, fees and charges (processing fee + third-party charges), net disbursed amount, total amount payable, APR and the
due date.</p>
<h3>2.4 Annexure C – Illustrative repayment schedule</h3>
<p>One row per instalment: instalment number, opening principal, instalment amount, principal, interest and closing principal.</p>
<h3>2.5 Footnotes</h3>
<ul>
<li>The KFS is valid for 15 days from e-signing.</li>
<li>Interest for the gap days between disbursement and the first due is added to the first EMI.</li>
<li>Interest accrues daily on a reducing balance, on 365 days (366 in a leap year).</li>
<li>The processing fee is not refundable.</li>
<li>Lien is released within 30 days of full and final settlement.</li>
<li>The customer can exit within the cooling-off period by repaying the principal and the proportionate APR, without penalty;
stamp duty, GST and statutory charges are not refunded.</li>
<li>The repayment bank account can be changed at most two times in the tenure.</li>
<li>An annual renewal charge applies when the loan is renewed or continued beyond the tenure.</li>
<li>Other standard terms: extra documents on request, SCCL’s discretion on disbursement, taxes extra, payments only from verified
bank accounts, change of contact details within a month, indemnity, review and renewal at SCCL’s discretion.</li>
</ul>
<h2>3. Loan agreement</h2>
<h3>3.1 Parties and recitals</h3>
<ul>
<li>The borrower (details at the end of the agreement) and Shriram Credit Company Limited (CIN U65993TN1980PLC008215, registered
office Shriram House, No. 4, Burkit Road, T. Nagar, Chennai 600017, RBI registration B-07.00709).</li>
<li>Loan of the sanctioned amount (in figures and in words), on the terms below and the schedule of charges.</li>
</ul>
<h3>3.2 Clauses</h3>
<ol class="brd-flow">
<li>Definitions and interpretation</li>
<li>Advancement of loan facility (security, eNACH, online disbursement, prepayment, pre-conditions)</li>
<li>Maintenance of LTV</li>
<li>Borrower obligations and undertakings</li>
<li>Repayment of loan</li>
<li>Term of the agreement</li>
<li>Interest rate</li>
<li>Change of designated bank account (bank swap)</li>
<li>Change in residential status</li>
<li>Obligations of borrower</li>
<li>Loan renewal charge</li>
<li>Annual maintenance charge</li>
<li>Bounce charge</li>
<li>Penal charges for default of payment</li>
<li>Notice</li>
<li>SCCL’s rights and obligations</li>
<li>Indemnification</li>
<li>End-use of the loan proceeds</li>
<li>Costs</li>
<li>Amendment</li>
<li>Entire agreement</li>
<li>Events of default</li>
<li>Consequences of events of default</li>
<li>Grievance redressal process</li>
<li>Right to audit</li>
<li>Reporting requirements, data protection and disclosure</li>
<li>Jurisdiction and governing law</li>
<li>Arbitration</li>
<li>Binding</li>
<li>Representations, warranties and undertakings</li>
<li>Confidentiality</li>
<li>Costs and expenses</li>
<li>Appropriation of payments</li>
<li>Miscellaneous</li>
<li>Severability</li>
<li>Counterparts</li>
<li>Electronic media</li>
<li>Non-withdrawal of loan amount after the cooling period</li>
<li>Excess payment and refund</li>
<li>Interest on same-day withdrawal and repayment</li>
</ol>
<p>Points in the clauses that tie to the LOS / LMS journey:</p>
<ul>
<li>eNACH for 2 times the sanctioned amount or ₹1 crore, whichever is lower.</li>
<li>Further withdrawals within the loan limit after a repayment, on a fresh disbursal request.</li>
<li>If the customer does not withdraw within the cooling period and till the end of the tenure, these charges are levied: lien
marking ₹450 + GST, stamp duty ₹200 + GST and lien removal ₹100 + GST. If not paid, SCCL recovers them from the pledged units
(with invocation charges) and then releases the rest.</li>
<li>Excess payment is first adjusted against any dues, and the balance is refunded to the registered bank account, without interest.</li>
<li>A withdrawal repaid on the same day still attracts at least one day’s interest.</li>
</ul>
<h3>3.3 Signatures</h3>
<p>Borrower name, address and signature; SCCL name, mailing address and signature; date of the agreement.</p>
<h3>3.4 Schedule of charges</h3>
<table class="brd-table"><thead><tr><th>No.</th><th>Charge head</th><th>Charges</th></tr></thead><tbody>
<tr><td>1–5</td><td>Loan, purpose, tenure, interest rate, interest frequency</td><td>From the loan; interest monthly</td></tr>
<tr><td>6</td><td>Loan processing charges</td><td>Processing fee + GST</td></tr>
<tr><td>7</td><td>Annual renewal charges</td><td>₹999 + GST</td></tr>
<tr><td>8</td><td>Annual maintenance charge</td><td>₹999 + GST</td></tr>
<tr><td>9</td><td>Bounce charges</td><td>₹100 + GST per instance</td></tr>
<tr><td>10</td><td>Penal charges</td><td>36% a year on the unpaid interest / EMI for the delayed period</td></tr>
</tbody></table>
<p>Other term: the facility is only for the mutual fund units / securities approved by SCCL. Signed by the customer (“I Accept”).</p>
<h3>3.5 Risk disclosure – LAMF</h3>
<p>Explains the market risk of borrowing against securities, the margin % formula ((security value – loan) ÷ security value × 100)
with two examples (20% and 11%), the margin call and sale of units without notice, and advice on tax. Signed with name, place and date.</p>
<h3>3.6 Loan application form</h3>
<p>Name, masked PAN, LAN / customer ID, date of birth, gender, father’s or spouse’s name, mother’s name, permanent address, mobile
number, email ID, occupation, loan amount (in lakhs), tenure, purpose, source of income, income, and the declaration with the
applicant’s signature. Organisation and existing SCCL loan details show NA.</p>
<h2>4. Fields filled in by the system</h2>
<table class="brd-table"><thead><tr><th>Field in the format</th><th>Meaning</th><th>Sanction letter</th><th>Loan agreement</th></tr></thead><tbody>
<tr><td>agreementDateDDMMYYYY / agreementDateDDMMMYYYY</td><td>Date of the document (DD-MM-YYYY / DD-MMM-YYYY)</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>borrowerNameAllCaps</td><td>Customer name in capitals</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>borrowerCorrespondenceAddressLine1 / 2 / 3</td><td>Correspondence address in three lines</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>borrowerCorrespondenceAddress / …City</td><td>Correspondence address in full, and its city (place of signing)</td><td class="c">–</td><td class="c">✓</td></tr>
<tr><td>borrowerPermanentAddress</td><td>Permanent address</td><td class="c">–</td><td class="c">✓</td></tr>
<tr><td>borrowerId</td><td>Customer ID</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>lan</td><td>Loan account number (LAN)</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>borrowerPANMasked</td><td>PAN, masked</td><td class="c">–</td><td class="c">✓</td></tr>
<tr><td>borrowerDobDDMMYYYY / borrowerGender</td><td>Date of birth and gender</td><td class="c">–</td><td class="c">✓</td></tr>
<tr><td>borrowerFathersName / borrowerMothersName</td><td>Father’s or spouse’s name, mother’s name</td><td class="c">–</td><td class="c">✓</td></tr>
<tr><td>borrowerMobileNumber / borrowerEmail</td><td>Registered mobile number and email ID</td><td class="c">–</td><td class="c">✓</td></tr>
<tr><td>borrowerOccupation / incomeSource / borrowerMonthlyIncome</td><td>Occupation, source of income, income</td><td class="c">–</td><td class="c">✓</td></tr>
<tr><td>currency</td><td>Currency symbol (₹)</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>sanctionAmount / sanctionAmountInWords / sanctionAmountInLakhs</td><td>Sanctioned loan amount, in words, and in lakhs</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>purposeOfLoan</td><td>Purpose of the loan</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>tenure</td><td>Loan term in months (also the number of interest dues)</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>interestRate</td><td>Rate of interest per year (fixed)</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>installmentAmount</td><td>Amount of each monthly due</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>firstDebitDateDayGap</td><td>Days from sanction to the first due</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>monthlyDebitDate</td><td>Due date of each instalment</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>processingFee</td><td>Processing fee (plus GST)</td><td class="c">✓</td><td class="c">✓</td></tr>
<tr><td>chargesPayableToThirdParty</td><td>Third-party charges through SCCL (lien marking, stamp duty)</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>totalChargesPayableByCustomer</td><td>Processing fee + third-party charges</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>totalInterestChargedDuringTenure</td><td>Total interest over the tenure at the sanction-date rate</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>sanctionAmountExclOtherChargesInclGST</td><td>Net disbursed amount used for the APR (loan amount less fees and charges)</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>totalAmountToBePaid</td><td>Loan amount + total interest + fees and charges</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>annualPercentageRate</td><td>APR, worked out on the net disbursed amount by the IRR, reducing balance method</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>grievanceDetails</td><td>Grievance officer of the LSP, where an LSP is involved</td><td class="c">✓</td><td class="c">–</td></tr>
<tr><td>rps rows (sno, opening principal, instalment, principal, interest, closing principal)</td><td>One row per instalment in the illustrative repayment schedule</td><td class="c">✓</td><td class="c">–</td></tr>
</tbody></table>
<h2>5. Fixed values in the formats</h2>
<table class="brd-table"><thead><tr><th>Item</th><th>Value</th></tr></thead><tbody>
<tr><td>Loan renewal / annual maintenance charge</td><td>₹999 + GST each</td></tr>
<tr><td>Bank swap charge</td><td>₹250 + GST</td></tr>
<tr><td>Lien marking / lien removal charge</td><td>₹450 + GST / ₹100 + GST</td></tr>
<tr><td>Stamp duty</td><td>₹200 + GST (Tamil Nadu)</td></tr>
<tr><td>Bounce charge</td><td>₹100 + GST per instance</td></tr>
<tr><td>Penal charge</td><td>36% a year on the unpaid interest / EMI</td></tr>
<tr><td>Prescribed LTV</td><td>Equity 45%, debt 75%</td></tr>
<tr><td>Cooling-off period / KFS validity</td><td>3 days / 15 days</td></tr>
<tr><td>eNACH limit</td><td>2 times the sanctioned amount or ₹1 crore, whichever is lower</td></tr>
</tbody></table>
<h2>6. Open points</h2>
<ol class="brd-flow">
<li>The schedule of charges heading has a fixed agreement number (MF0000000000025). Should it be the customer’s LAN?</li>
<li>Annexure numbering: the agreement refers to the schedule of charges and notice details as Annexure-1, but the schedule is
headed Annexure 2, and the loan application form is also headed Annexure 2.</li>
<li>Loan application form: the “Annual Income” row is filled with the monthly income field.</li>
<li>KFS item 12 lists “exchange listed approved shares” as collateral; this product is against mutual funds only.</li>
<li>KFS item 4 shows principal as 1 bullet at maturity, which fits the balloon / interest-only loan only. What should it show for an EMI loan?</li>
<li>Stamp duty is shown with “+ GST”, and only for Tamil Nadu. Should it vary by the customer’s state?</li>
<li>SCCL is called the party “of the Third Part” although the agreement has only two parties.</li>
<li>The definition of “Event of Default” points to Clause 21; please check it against the final clause numbering.</li>
<li>Wording fix: “pro data” should be “pro rata” (KFS item 9).</li>
</ol>
"""


# ---------------------------------------------------------------------------------------------------------------------------
# Waiver BRD – scenario-wise version (DISC-398): same requirements, written scenario by scenario, point by point.
# ---------------------------------------------------------------------------------------------------------------------------
def _waiver_scen_body():
    """Scenario-wise Waiver BRD (DISC-398, rewritten DISC-441): common rules once, then S 1 – S 7 step by step in one flow, with the
    sample templates (To be confirmed) and the UNO entry of each case. Same rules as the main Waiver BRD."""
    TBC = '<span class="brd-tbc">To be confirmed</span>'
    lk = lambda href, t: f'<a href="{href}" target="_blank" rel="noopener">{t}</a>'
    IC = lambda n, v="": lk(f"internal/IC-{n}{'-' + v if v else ''}.html", f"alert {n}")   # DISC-461: v = no / full / s2-no … (sample of that waive-off type)
    NM = lambda f, row: lk(f"new-mails/{f}.html", "sample mail") + " · " + lk("communications.html", f"SMS row {row}")
    S = lambda *x: f' <span class="brd-smp">({" · ".join(x)}) {TBC}</span>'
    BANK = ("SBR", "BS_Asset", "165042", "AXIS BANK - A/C 025010200017480", "HLFCH")
    INC = {"LM": ("SJV", "P&amp;L_Income", "800110", "LIEN MARKING CHARGES LAS/LAMF Loan-1"),
           "LR": ("SJV", "P&amp;L_Income", "800098", "LIEN REMOVAL CHARGES-1"),
           "PF": ("SJV", "P&amp;L_Income", "800102", "LOAN PROCESSING FEES A/C-1"),
           "SD": ("SJV", "P&amp;L_Income", "800111", "STAMP DUTY CHARGES LAS/LAMF Loan-1"),
           "GST": ("SJV", "BS_Liability", "715110", "IGST At Loan-1")}

    def uno(lines):
        if not lines:
            return "<p><b>UNO entry:</b> none – nothing is received.</p>"
        f = lambda v: f"{v:,.2f}"
        tot = round(sum(a for _, a in lines), 2)
        rows = [f"<tr><td>{BANK[0]}</td><td>{BANK[1]}</td><td>{BANK[2]}</td><td>{BANK[3]}</td><td>{f(tot)}</td><td></td><td>{BANK[4]}</td><td>LAN</td></tr>"]
        rows += [f"<tr><td>{INC[k][0]}</td><td>{INC[k][1]}</td><td>{INC[k][2]}</td><td>{INC[k][3]}</td><td></td><td>{f(a)}</td><td>HLTFC</td><td>LAN</td></tr>"
                 for k, a in lines]
        note = " (example for a sanction amount of ₹1,00,000 – Processing Fee* ₹1,499 + GST; the other charges are fixed)" if any(k == "PF" for k, _ in lines) else ""   # DISC-459: only the Processing Fee depends on the sanction
        return (f"<p><b>UNO entry</b> – posted when the customer pays{note}</p>"
                "<table class='brd-table'><thead><tr><th>DocType</th><th>A/c Nature</th><th>A/c code</th><th>Description</th>"
                f"<th>Debit</th><th>Credit</th><th>Subdoctype</th><th>Subaccd</th></tr></thead><tbody>{''.join(rows)}</tbody></table>")

    MAIL = lambda to, cc: f"LMS event mail triggered to <b>{to}</b>, Cc <b>{cc}</b>, to approve or reject quickly."   # DISC-446 / 447
    INFO = lambda to, cc: f"LMS event mail triggered to <b>{to}</b>, Cc <b>{cc}</b>."
    ol = lambda items: "<ol class='brd-steps'>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"
    flow = lambda steps: ("<div class='brd-flow'><div class='fl'>" + "<i>→</i>".join(f"<span class='fs'>{x}</span>" for x in steps) + "</div></div>")

    def chain(action, to, treasury_alert, v=""):
        verb = "Reject" if action == "reject" else "Approve"
        rj = action == "reject"   # DISC-465: on a rejection the checker and Treasury accept the rejection request (not a loan approval)
        ck_act = ("approves the rejection request (<b>Accept Rejection</b>; <b>Decline Rejection</b> cancels it)" if rj else "approves")
        tr_act = ("approves the rejection request (<b>Accept Rejection</b>)" if rj else "gives the final approval")
        return [f"OPS maker (OPS L1) selects the charges, enters the amounts, adds the note (mandatory), uploads the file (mandatory) and clicks <b>{verb}</b>. Nothing "
                "is waived and the LAN status does not change yet. " + MAIL("OPS Checker", "Treasury") + S(IC(16, v)),
                "OPS checker (OPS L2 or OPS L3) checks the request, can change the waive-off, adds the note (mandatory; a file is mandatory only if the waive-off is changed) "
                f"and {ck_act}. " + MAIL("Treasury", "OPS") + S(IC(12, v)),
                f"Treasury (Treasury L1, L2 or L3) adds the note (mandatory) and {tr_act}. "
                f"The waive-off is applied and the LAN status changes to <b>{to}</b>. " + INFO("OPS", "Treasury") + S(treasury_alert(v))]

    PAY = lambda amt, mail, key: [
        f"The customer gets an SMS and mail with the payment link for <b>₹{amt}</b>." + S(*mail),
        "The customer opens the link, verifies the mobile number with an OTP in the LOS and pays the full amount in one payment. "
        f"({lk(f'charges-payment-{key}.html', 'LOS payment journey')} · {lk(f'charges-receipt-{key}.html', 'receipt')})",
        "The paid amount is posted in UNO (each charge separately, entry below). The SOA is not updated, as the LAN is not ACTIVE. The receipt is saved "
        "in the LMS Documents tab. LMS event mail triggered to <b>Treasury</b>, Cc <b>OPS</b>, to confirm the payment is received." + S(IC(14)),
        "Treasury cross-checks that the payment is received and approves it (or rejects it if it is not received). The "
        "balance payable is now ₹0, so LMS enables the Initiate De-pledge CTA. " + INFO("OPS", "Treasury") + " The customer gets an SMS and mail "
        "with the receipt." + S(IC(15), NM("08_Charges_Payment_Received", 38)),
        "OPS maker initiates the de-pledge and OPS checker approves it."]
    NOPAY = lambda mail: [f"The customer gets an SMS and mail that the application is rejected, without a payment link." + S(*mail),
                          "Nothing is payable, so OPS maker initiates the de-pledge straight away and OPS checker approves it."]

    def reject_subs(n, first, lm_lr):
        draft = n in (2, 3, 4)
        t_alert = (lambda v: IC(13, v)) if draft else (lambda v: IC(22, v) + " · " + IC(23, v))
        p2 = "s2-" if lm_lr else ""   # S 2 samples show only Lien Marking and Lien Removal
        m_link = (NM("06_Draft_Application_Rejected_Pay_Charges", 36),) if draft else (lk("mails/28_Application_Rejected_Pay_Charges.html", "sample mail"), lk("communications.html", "SMS row 14"))
        m_none = (NM("07_Draft_Application_Rejected", 37),) if draft else (lk("mails/29_Application_Rejected.html", "sample mail"), lk("communications.html", "SMS row 15"))
        if lm_lr:
            full, part, ptxt = "649.00", "118.00", "Lien Marking ₹531 waived in full, Lien Removal ₹118 payable"
            e_no, e_part = [("LM", 450), ("LR", 100), ("GST", 99)], [("LR", 100), ("GST", 18)]
        else:
            full, part, ptxt = "1,768.82", "1,268.82", "₹500 of the Processing Fee waived, ₹1,268.82 payable"
            e_no = [("PF", 749), ("LM", 450), ("LR", 100), ("SD", 200), ("GST", 269.82)]
            e_part = [("PF", 325.27), ("LM", 450), ("LR", 100), ("SD", 200), ("GST", 193.55)]
        to, k = "REJECTED", first
        kn, kp = ("s2-1", "s2-3") if lm_lr else ("s3-1", "s3-3")   # DISC-450: payment journey and receipt for this case
        return (f"<h4>S {n}.{k} – Reject Without Waive-off</h4>" + ol(chain("reject", to, t_alert, p2 + "no") + PAY(full, m_link, kn)) + uno(e_no)
                + f"<h4>S {n}.{k + 1} – Reject With Full Waive-off</h4>" + ol(chain("reject", to, t_alert, p2 + "full") + NOPAY(m_none)) + uno([])
                + f"<h4>S {n}.{k + 2} – Reject With Partial Waive-off</h4><p>Example: {ptxt}.</p>"
                + ol(chain("reject", to, t_alert, p2 + "partial" if lm_lr else "") + PAY(part, m_link, kp)) + uno(e_part))

    def approve_subs(n):
        to = "ACCOUNT OPENED" if n == 5 else "ACTIVE"
        cust = ("The customer gets no SMS or mail at this stage." if n == 5 else
                "The customer gets the Loan Lodgement Approval SMS and mail (already in use)." + S(lk("communications.html", "SMS row 13")))
        post = lambda what: [cust, what, "There is no de-pledge and no payment link – the loan continues."]
        return (f"<h4>S {n}.1 – Approve Without Waive-off</h4>"
                + ol(["OPS maker (OPS L1) adds the note (mandatory), uploads the file (mandatory) and clicks <b>Approve</b> without a waive-off. " + MAIL("OPS Checker", "Treasury") + S(IC(16, "no")),
                      f"OPS checker (OPS L2 or OPS L3) checks, adds the note (mandatory) and approves. There is no Treasury approval. The LAN status changes to <b>{to}</b>."]
                     + post("LMS shows the full charges (₹1,768.82). They are posted in UNO at the first withdrawal or repayment."))
                + f"<h4>S {n}.2 – Approve With Full Waive-off</h4>"
                + ol(chain("approve", to, lambda v: IC(13, v), "full") + post("LMS shows no charges. There is no UNO entry."))
                + f"<h4>S {n}.3 – Approve With Partial Waive-off</h4><p>Example: ₹500 of the Processing Fee waived.</p>"
                + ol(chain("approve", to, lambda v: IC(13, v)) + post("LMS shows only the balance (₹1,268.82). It is posted in UNO at the first withdrawal or "
                                                         "repayment.")))

    def head(n, st, drop, charges, ops, to, steps):
        return (f"<h3>3.{n} S {n} – {st}: customer dropped off {drop}</h3>"
                f"<p><b>Charges</b> {charges}<br><b>What OPS can do</b> {ops}<br><b>LAN status can change to</b> {to}</p>" + flow(steps))

    DAY30 = ("<p><b>Before the rejection</b> (pledged DRAFT, journey not completed)</p>"
             + ol(["On day 30 from the LAN creation date, the customer gets an SMS and mail that the application is not complete and the units "
                   "are pledged, so please complete the journey. The application is not rejected because of this."
                   + S(NM("10_Application_Pending_Lien_Marked", 40)),
                   "On day 31, OPS gets a mail to check with the customer to complete the journey, or to ask the customer to send a mail to "
                   "de-pledge the units. Until then, the lien stays marked with SCCL. " + INFO("OPS", "Treasury") + S(IC(21)),
                   "OPS maker rejects a pledged DRAFT loan only when the customer asks by mail to remove the lien."]))
    DECLINE = ("<p class='brd-note'>In every case, if the OPS checker or Treasury declines the request, it is cancelled – nothing is waived, "
               "the LAN status does not change, and the maker can raise a new request. " + INFO("OPS Maker", "Treasury") + S(IC(17)) + "</p>")
    PF4 = ("Processing Fee ₹883.82 (any amount), Lien Marking ₹531, Lien Removal ₹118 and Stamp Duty ₹236 (full only) – together the "
           "Processing Fee* ₹1,768.82 the customer sees.")
    START = ["Customer starts the journey", "LAN created – DRAFT", "Units pledged"]

    return f"""
<p class="brd-note">The Charges Waiver BRD, written scenario by scenario for an easy read from start to end. Section 2 has the rules that
apply to every scenario; section 3 walks through each scenario step by step, with the sample mails and the UNO entry; sections 4 to 6 have
the communications, the UNO account codes and the open points.</p>
<h2>1. Purpose</h2>
<ul>
<li>When a customer pledges the mutual fund units and then drops off the journey, charges are already incurred (lien marking, lien removal,
stamp duty or processing fee). Today SCCL bears these charges, and the customer has no option to pay them.</li>
<li>OPS needs an option in LMS to reject or approve such a loan and, in the same request, waive these charges fully, partly or not at all.</li>
<li>The customer needs an option to pay the balance charges online, and OPS needs an option to de-pledge the units after the payment is
confirmed.</li>
<li>For an ACTIVE loan, OPS needs an option to waive charges, and the Statement of Account (SOA) is updated.</li>
</ul>

<h2>2. Rules for Every Scenario</h2>
<h3>2.1 Who Approves</h3>
<table class="brd-table"><thead><tr><th>Maker</th><th>Checker</th><th>Final approval</th></tr></thead><tbody>
<tr><td>OPS L1</td><td>OPS L2 or OPS L3</td><td>Treasury L1, L2 or L3</td></tr></tbody></table>
<ul>
<li>This applies to any sanctioned amount. An approval without a waive-off (S 5.1, S 6.1) needs only the OPS maker and the OPS checker.</li>
<li>The note is mandatory for all three. The file is mandatory for the maker, and for the checker only if the checker changes the waive-off.
Treasury can only approve or decline. Every step is saved in the Audit tab.</li>
<li>If the maker submits without the note or the file, LMS shows “Please add the note and upload a file.”</li>
<li>Once the maker raises a rejection request, the customer cannot continue that loan application in the LOS, and after the LAN is
REJECTED the customer cannot move to any next step of it (LOS shows a message). So no charge can be added after the request – the customer
can only pay through the payment link. The customer can still start a fresh loan application. If the checker or Treasury declines the
request, the customer can continue the existing application. (LOS change – PRD Pending Changes, CR-19.)</li>
<li>A DRAFT loan cannot be approved. For a rejection request (DRAFT, SUBMITTED or ACCOUNT OPENED), the checker and Treasury see the CTAs
<b>Accept Rejection</b> and <b>Decline Rejection</b> – they accept or decline the rejection request, not the loan. Approve is used only to
approve a SUBMITTED or ACCOUNT OPENED loan (S 5.1 – S 5.3, S 6.1 – S 6.3).</li>
<li>Every approve or reject asks for confirmation in a pop-up – “This action is irreversible. Are you sure you want to proceed?”.</li>
</ul>
<h3>2.2 Charges and Waive-off</h3>
<ul>
<li>S 2 has Lien Marking ₹531 and Lien Removal ₹118. From S 3, LMS shows the customer's Processing Fee* (₹1,768.82) in four rows – Processing
Fee ₹883.82, Lien Marking ₹531, Lien Removal ₹118 and Stamp Duty ₹236. LMS shows every charge with GST included, not as a separate GST amount.</li>
<li>Lien Marking, Lien Removal and Stamp Duty can only be waived in full. The Processing Fee and the other charges can be waived by any amount.</li>
<li>The waived amount includes GST. Penal charges carry no GST.</li>
<li>Each request is a No waive-off, Partial waive-off or Full waive-off, set by LMS from the amount left to pay.</li>
<li>Until the LAN is ACTIVE, the waive-off goes with the Reject or Approve in the Approvals tab as one request. For an ACTIVE loan, it is a
separate request from the ≡ menu → Waive-off page, approved in the Approvals tab.</li>
</ul>
<h3>2.3 Customer Payment, Receipt and UNO</h3>
<ul>
<li>The customer pays the full payable amount, including GST, through the payment link (LOS, OTP, Pay Charges page). A failed payment changes nothing, and
the customer can pay again. If the customer does not pay, a reminder SMS and mail is sent every month.{S(NM("09_Charges_Payment_Reminder", 39))}</li>
<li>For a REJECTED LAN with a balance payable, OPS maker (OPS L1) can click <b>Resend Payment Link</b> in LMS whenever the customer asks
for the link. After the confirmation pop-up, the customer gets the same SMS and mail as the monthly reminder, with the same payment link.
No checker or Treasury approval is needed, and LMS records it in the Audit tab. The CTA is disabled while a payment is pending Treasury
confirmation, after the payment is approved, and for a full waive-off.{S(NM("09_Charges_Payment_Reminder", 39))}</li>
<li>On a successful payment, the amount is posted in UNO (each charge separately, one IGST line, Subaccd = LAN), and a
receipt RCPT/LAMF/YYYY/MM/NNNN is saved in the LMS Documents tab. A duplicate or excess payment is refunded through the existing refund option.</li>
<li>The SOA is updated only when the LAN status is ACTIVE. For a DRAFT, SUBMITTED or ACCOUNT OPENED loan, a payment updates UNO only, not the
SOA.</li>
<li>After every payment (the UNO entry is posted first, automatically), Treasury cross-checks that it is received and approves or rejects it. When
Treasury approves, the balance payable is ₹0, so LMS enables the Initiate De-pledge CTA (straight away after a full waive-off).
OPS maker initiates the de-pledge and OPS checker approves it.</li>
<li>If Treasury rejects the payment, the balance and the de-pledge do not change. OPS gets an internal mail that the payment is not
received as per the entries, and the customer is told that the payment is not received and that any debited amount will be returned by the
payment gateway. If the payment was actually received, Treasury handles it in the backend.</li>
</ul>
<p>Each payable case links its own LOS payment journey and receipt (the amounts differ). S 4, S 5 and S 6 have the same amounts as S 3, so
they use the S 3 screens.</p>

<h2>3. Scenarios</h2>
{head(1, "DRAFT", "before pledging the mutual funds", "None.", "No action.", "INACTIVE (on day 31)",
      ["Customer starts the journey", "LAN created – DRAFT", "Units not pledged", "Day 31 – INACTIVE"])}
{ol(["The LAN is created in DRAFT, but the mutual fund units are not pledged.",
     "On day 31 from the LAN creation date, the LAN status changes to INACTIVE automatically.",
     "No charges, no waive-off, no de-pledge and no accounting entry."])}

{head(2, "DRAFT", "after pledging the mutual funds", "Lien Marking ₹531 and Lien Removal ₹118 (full waive-off only).",
      "Reject, with no, full or partial waive-off.", "REJECTED", START + ["Customer asks to remove the lien", "Rejection request", "Checker", "Treasury", "Rejected &amp; Without Waive-off", "Customer Payment", "Receipt &amp; UNO Entry", "Treasury Confirmation", "De-pledge"])}
{DAY30}
{reject_subs(2, 1, True)}

{head(3, "DRAFT", "after the Sanction Letter is generated", PF4, "Reject, with no, full or partial waive-off.", "REJECTED",
      START + ["Sanction Letter", "Customer asks to remove the lien", "Rejection request", "Checker", "Treasury", "Rejected &amp; Without Waive-off", "Customer Payment", "Receipt &amp; UNO Entry", "Treasury Confirmation", "De-pledge"])}
{DAY30}
{reject_subs(3, 1, False)}

{head(4, "DRAFT", "after the Loan Agreement e-Sign", PF4, "Reject, with no, full or partial waive-off.", "REJECTED",
      START + ["Sanction Letter", "Loan Agreement e-Sign", "Customer asks to remove the lien", "Rejection request", "Checker", "Treasury", "Rejected &amp; Without Waive-off", "Customer Payment", "Receipt &amp; UNO Entry", "Treasury Confirmation", "De-pledge"])}
{DAY30}
{reject_subs(4, 1, False)}

{head(5, "SUBMITTED", "after the E-Mandate", PF4, "Approve or reject, with no, full or partial waive-off.", "ACCOUNT OPENED or REJECTED",
      START + ["Sanction Letter", "Loan Agreement e-Sign", "E-Mandate", "SUBMITTED", "Approve or Reject request", "Checker", "Treasury (if waived)", "ACCOUNT OPENED / REJECTED"])}
{approve_subs(5)}
{reject_subs(5, 4, False)}

{head(6, "ACCOUNT OPENED", "after the Loan Account Opening", PF4, "Approve or reject, with no, full or partial waive-off.", "ACTIVE or REJECTED",
      START + ["SUBMITTED", "Loan Account Opening", "ACCOUNT OPENED", "Approve or Reject request", "Checker", "Treasury (if waived)", "ACTIVE / REJECTED"])}
{approve_subs(6)}
{reject_subs(6, 4, False)}

{head(7, "ACTIVE", "after the Loan Lodgement", "Processing Fee, Lien Marking, Lien Removal, Stamp Duty, Bounce, Penal, Loan Renewal, AMC and Bank Swap.",
      "Waive-off only, from the ≡ menu → Waive-off page. The loan cannot be rejected.", "No change – stays ACTIVE",
      ["LAN ACTIVE", "≡ → Waive-off page", "Waive-off request", "Approvals tab – Checker", "Treasury", "SOA updated"])}
<h4>S 7.1 – Without Waive-off</h4>
{ol(["Nothing is selected on the Waive-off page, so the Waive-off button stays disabled and no request is raised.",
     "The charges stay in the SOA and are collected as usual."])}
<h4>S 7.2 – With Full Waive-off</h4>
{ol(["OPS maker (OPS L1) opens ≡ → Waive-off, selects the charges, adds the note (mandatory), uploads the file (mandatory) and clicks Waive-off. On “Yes, Waive Off”, the "
     "request goes to the Approvals tab. " + MAIL("OPS Checker", "Treasury") + S(IC(18, "full")),
     "OPS checker (OPS L2 or OPS L3) approves the request in the Approvals tab with a note (mandatory). " + MAIL("Treasury", "OPS") + S(IC(19, "full")),
     "Treasury (Treasury L1, L2 or L3) gives the final approval with a note (mandatory). " + INFO("OPS", "Treasury") + S(IC(20, "full")),
     "LMS updates the SOA: the waive-off is a credit with a waiver narration. Nothing is posted in UNO. The LAN stays ACTIVE.",
     "The customer gets no communication."])}
<h4>S 7.3 – With Partial Waive-off</h4>
{ol(["Same as S 7.2, with part of a charge waived (Processing Fee and the other charges only).",
     "Example: ₹500 waived (₹423.73 charge plus ₹76.27 IGST) – the SOA balance goes from ₹1,768.82 to ₹1,268.82.",
     "The balance is collected as usual."])}
<p><b>SOA example (ACTIVE) – Part A, application charges (₹500 of the Processing Fee waived)</b></p><table class='brd-table brd-soa'><thead><tr><th>Date</th><th>Transaction Details</th><th>Debit</th><th>Credit</th><th>Balance</th><th>DR / CR</th></tr></thead><tbody><tr><td>14-07-2025</td><td>Processing Fee Charges</td><td>883.82</td><td></td><td>883.82</td><td>DR</td></tr><tr><td>14-07-2025</td><td>Lien Marking Charges</td><td>531.00</td><td></td><td>1,414.82</td><td>DR</td></tr><tr><td>14-07-2025</td><td>Lien Removal Charges</td><td>118.00</td><td></td><td>1,532.82</td><td>DR</td></tr><tr><td>14-07-2025</td><td>Stamp Duty Charges</td><td>236.00</td><td></td><td>1,768.82</td><td>DR</td></tr><tr><td>14-07-2025</td><td>Waive-off – approved by Treasury (waiver narration)</td><td></td><td>500.00</td><td>1,268.82</td><td>DR</td></tr></tbody></table><p><b>SOA example (ACTIVE) – Part B, loan charges (₹500 waived)</b></p><table class='brd-table brd-soa'><thead><tr><th>Date</th><th>Transaction Details</th><th>Debit</th><th>Credit</th><th>Balance</th><th>DR / CR</th></tr></thead><tbody><tr><td>14-07-2025</td><td>Bounce Charge</td><td>118.00</td><td></td><td>118.00</td><td>DR</td></tr><tr><td>14-07-2025</td><td>Penal Charges</td><td>50.00</td><td></td><td>168.00</td><td>DR</td></tr><tr><td>14-07-2025</td><td>Loan Renewal Charge</td><td>1,178.82</td><td></td><td>1,346.82</td><td>DR</td></tr><tr><td>14-07-2025</td><td>Annual Maintenance Charge (AMC)</td><td>1,178.82</td><td></td><td>2,525.64</td><td>DR</td></tr><tr><td>14-07-2025</td><td>Bank Swap Charge</td><td>295.00</td><td></td><td>2,820.64</td><td>DR</td></tr><tr><td>14-07-2025</td><td>Waive-off – approved by Treasury (waiver narration)</td><td></td><td>500.00</td><td>2,320.64</td><td>DR</td></tr></tbody></table>
{DECLINE}
<p><small>*Inclusive of Lien Marking, Lien Removal and Stamp Duty</small></p>

<h2>4. Communication – Internal and Customer</h2>
<table class="brd-table"><thead><tr><th>Scenario</th><th>Recipient</th><th>Communication Type</th><th>Sample template</th><th>Status</th></tr></thead><tbody>
<tr><td>Maker raises a rejection request with the waive-off (DRAFT, SUBMITTED, ACCOUNT OPENED) – to the OPS checker</td><td>Internal</td><td>Email</td><td>{IC(16)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>Checker approves the rejection request – to Treasury</td><td>Internal</td><td>Email</td><td>{IC(12)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>Treasury approves the rejection of a DRAFT loan – to OPS and Treasury</td><td>Internal</td><td>Email</td><td>{IC(13)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>Treasury approves the rejection of a SUBMITTED or ACCOUNT OPENED loan – to OPS (revised alerts 3 and 5)</td><td>Internal</td><td>Email</td><td>{IC(22)} · {IC(23)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>Checker or Treasury declines the request – to the OPS maker</td><td>Internal</td><td>Email</td><td>{IC(17)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>Day 30 – pledged DRAFT LAN not submitted, reminder to complete the journey – to the customer</td><td>Customer</td><td>Email and SMS</td><td>{NM('10_Application_Pending_Lien_Marked', 40)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>Day 31 – pledged DRAFT LAN not submitted, check with the customer – to OPS</td><td>Internal</td><td>Email</td><td>{IC(21)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>DRAFT loan rejected with no or partial waive-off, with the payment link – to the customer</td><td>Customer</td><td>Email and SMS</td><td>{NM('06_Draft_Application_Rejected_Pay_Charges', 36)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>DRAFT loan rejected with full waive-off, without the payment link – to the customer</td><td>Customer</td><td>Email and SMS</td><td>{NM('07_Draft_Application_Rejected', 37)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>SUBMITTED or ACCOUNT OPENED loan rejected with no or partial waive-off, with the payment link – to the customer</td><td>Customer</td><td>Email and SMS</td><td>{lk('mails/28_Application_Rejected_Pay_Charges.html', 'Sample mail')} · {lk('communications.html', 'SMS')}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>SUBMITTED or ACCOUNT OPENED loan rejected with full waive-off, without the payment link – to the customer</td><td>Customer</td><td>Email and SMS</td><td>{lk('mails/29_Application_Rejected.html', 'Sample mail')} · {lk('communications.html', 'SMS')}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>Customer pays the charges – to Treasury and OPS</td><td>Internal</td><td>Email</td><td>{IC(14)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>Treasury confirms the payment, initiate the de-pledge – to OPS</td><td>Internal</td><td>Email</td><td>{IC(15)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>Treasury confirms the payment, with the payment receipt – to the customer</td><td>Customer</td><td>Email and SMS</td><td>{NM('08_Charges_Payment_Received', 38)} · {lk('charges-receipt.html', 'Receipt')}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>Charges not paid, reminder every month – to the customer</td><td>Customer</td><td>Email and SMS</td><td>{NM('09_Charges_Payment_Reminder', 39)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>OPS clicks Resend Payment Link on a REJECTED LAN – to the customer</td><td>Customer</td><td>Email and SMS</td><td>{NM('09_Charges_Payment_Reminder', 39)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>ACCOUNT OPENED loan approved (Loan Lodgement) – to the customer</td><td>Customer</td><td>Email and SMS</td><td>{lk('communications.html', 'Loan Lodgement Approval')}</td><td><span class="brd-tbc">Already in use</span></td></tr>
<tr><td>SUBMITTED loan approved (Loan Account Opening) – to the customer</td><td>Customer</td><td>–</td><td>–</td><td>No communication</td></tr>
<tr><td>ACTIVE loan – maker raises a waive-off request – to the OPS checker</td><td>Internal</td><td>Email</td><td>{IC(18)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>ACTIVE loan – checker approves the waive-off request – to Treasury</td><td>Internal</td><td>Email</td><td>{IC(19)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>ACTIVE loan – Treasury approves the waive-off request – to OPS</td><td>Internal</td><td>Email</td><td>{IC(20)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>ACTIVE loan – checker or Treasury declines the waive-off request – to the OPS maker</td><td>Internal</td><td>Email</td><td>{IC(17)}</td><td><span class="brd-tbc">To be confirmed</span></td></tr>
<tr><td>ACTIVE loan – waive-off approved – to the customer</td><td>Customer</td><td>–</td><td>–</td><td>No communication</td></tr>
</tbody></table>
<ul><li>Internal mails do not need DLT approval. Customer SMS need DLT registration.</li></ul>

<h2>5. Accounting Entry (UNO) – Reference Format and Account Codes</h2>
<p><b>Reference format</b> – how the charges with IGST post in UNO against the LAN</p>
<table class="brd-table"><thead><tr><th>DocType</th><th>A/c Nature</th><th>A/c code</th><th>Description</th><th>Doc. Dt</th>
<th>Debit</th><th>Credit</th><th>Subdoctype</th><th>Subaccd</th></tr></thead><tbody>
<tr><td>SBR</td><td>BS_Asset</td><td>165042</td><td>AXIS BANK - A/C 025010200017480</td><td>05-Nov-2026</td><td>885</td><td></td><td>HLFCH</td><td>LAN</td></tr>
<tr><td>SJV</td><td>P&amp;L_Income</td><td>800110</td><td>LIEN MARKING CHARGES LAS/LAMF Loan-1</td><td>05-Nov-2026</td><td></td><td>450</td><td>HLTFC</td><td>LAN</td></tr>
<tr><td>SJV</td><td>P&amp;L_Income</td><td>800098</td><td>LIEN REMOVAL CHARGES-1</td><td>05-Nov-2026</td><td></td><td>100</td><td>HLTFC</td><td>LAN</td></tr>
<tr><td>SJV</td><td>P&amp;L_Income</td><td>800111</td><td>STAMP DUTY CHARGES LAS/LAMF Loan-1</td><td>05-Nov-2026</td><td></td><td>200</td><td>HLTFC</td><td>LAN</td></tr>
<tr><td>SJV</td><td>BS_Liability</td><td>715110</td><td>IGST At Loan-1</td><td>05-Nov-2026</td><td></td><td>135</td><td>HLTFC</td><td>LAN</td></tr>
</tbody></table>
<ul>
<li>SBR is the bank receipt, where the amount received is debited to the bank account. SJV is the journal, where the charges are credited to income and the GST to the IGST liability account.</li>
<li>For a partial waive-off, only the balance actually paid is posted; the waived part is not posted.</li>
</ul>
<p><b>UNO account codes for the charges</b></p>
<table class="brd-table"><thead><tr><th>A/c code</th><th>Description</th><th>A/c Nature</th></tr></thead><tbody>
<tr><td>800110</td><td>LIEN MARKING CHARGES LAS/LAMF LOAN-1</td><td>P&amp;L – Income</td></tr>
<tr><td>800098</td><td>LIEN REMOVAL CHARGES-1</td><td>P&amp;L – Income</td></tr>
<tr><td>800111</td><td>STAMP DUTY CHARGES LAS/LAMF LOAN-1</td><td>P&amp;L – Income</td></tr>
<tr><td>800102</td><td>LOAN PROCESSING FEES A/C-1</td><td>P&amp;L – Income</td></tr>
<tr><td>800113</td><td>EMI/ INSTALMENT BOUNCE CHARGES-1</td><td>P&amp;L – Income</td></tr>
<tr><td>800114</td><td>AMC-ANNUAL MAINTENANCE CHARGES-1</td><td>P&amp;L – Income</td></tr>
<tr><td>800115</td><td>PENAL INTEREST-1</td><td>P&amp;L – Income</td></tr>
<tr><td>715110</td><td>IGST At Loan-1</td><td>Balance sheet – Liability</td></tr>
<tr><td>165042</td><td>AXIS BANK - A/C 025010200017480</td><td>Balance sheet – Asset</td></tr>
</tbody></table>
<p>The entries for each scenario are under the scenario in section 3.</p>

<h2>6. Open Points</h2>
<ul>
<li>The sample mail and SMS templates (marked To be confirmed) are to be reviewed and confirmed. The SMS also need DLT registration.</li>
<li>New customer template for “payment not received” – to be created.</li>
</ul>
"""


BRDS = [
    {"slug": "waive-off-scenarios", "title": "Charges Waiver & Post-Pledge Drop-off – Scenario-wise", "status": "Draft", "updated": "27-11-2026",
     "summary": "Waive charges (none, partial or full) with reject or approve, scenario by scenario (S 1 – S 7): approvals, mails, payment, de-pledge and UNO entries.",
     "body": _waiver_scen_body()},
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
    {"slug": "loan-risk-stage", "title": "Loan Risk Stage Classification", "status": "Completed", "updated": "17-11-2026",
     "summary": "Every active loan is put into No Risk or Stage 1, 2 or 3 by comparing the loan outstanding with the collateral value "
                "at the L1, L2 and L3 LTV levels (revised grid of 22-09-2026), with a Stage column in LMS and daily alerts in Stage 2.",
     "body": RISK_STAGE},
    {"slug": "additional-fund-fetch", "title": "Additional Fund Fetch through Secondary Mobile Number", "status": "Draft", "updated": "17-11-2026",
     "summary": "Fetch more mutual funds under the same PAN using a secondary mobile number or email ID, re-work the eligibility, "
                "carry the email into KYC and pledge through the mutually inclusive contact; one mobile number can hold two PAN profiles.",
     "body": ADDITIONAL_FUND_FETCH},
    {"slug": "shortfall-emi-default", "title": "Shortfall & EMI Default", "status": "Draft", "updated": "17-11-2026",
     "summary": "EMI bounce, re-presentation, charges and the withdrawal freeze; LTV breach alerts at 90% and invocation at 75%; "
                "invocation reasons in LMS, maker-checker with OTP, and loan closure with refund of the excess.",
     "body": SHORTFALL_EMI_DEFAULT},
    {"slug": "sanction-letter-loan-agreement", "title": "Sanction Letter & Loan Agreement Formats", "status": "Draft", "updated": "17-11-2026",
     "summary": "What the e-Sanction Letter (with KFS, APR working and repayment schedule) and the Loan cum Pledge Agreement contain, "
                "the fields the system fills in, the fixed charges in the formats, and the points to correct.",
     "body": SANCTION_AGREEMENT},
]
