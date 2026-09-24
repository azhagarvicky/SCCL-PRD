# LAMF LOS – Discussion & Decision Log

## Project Information

**Project:** Loan Against Mutual Funds (LAMF)
**System:** LOS – Customer Online Journey
**Document Type:** Discussion & Decision Log
**Status:** Living Document
**Last Updated:** 24-09-2026

**Prototype location:** `LOCAL/lamf-journey/` (37 HTML screens + shared `assets/lamf.css`, `assets/lamf.js`)
**Screenshot source:** `SCCL/LAMF/LOS/LOS/` (38 screenshots, UAT: `uatlamf.shriramcredit.in`)
**PRD (HTML):** `LOCAL/lamf-journey/SCCL_LAMF_LOS_PRD.html` → `http://localhost:8080/SCCL_LAMF_LOS_PRD.html` (regenerate with `python3 tools/build_prd.py`)
**Cloud copy (private):** https://claude.ai/artifact/1Jqh9iJ4WDk4SJppaPojYr — single page, hash routed (`cloud.html`)
**Local URL:** `http://localhost:8080` (`python3 -m http.server 8080 --directory lamf-journey`)
**Repository (public):** https://github.com/azhagarvicky/SCCL-PRD — `dev` = development, `main` = production
**Hosted – Production (`main`):** https://azhagarvicky.github.io/SCCL-PRD/
**Hosted – Development (`dev`):** https://azhagarvicky.github.io/SCCL-PRD/dev/

**How to read this document**

| Marker | Meaning |
| --- | --- |
| **Confirmed** | Explicitly stated by the user in discussion |
| **Observed** | Read from the shared screenshots; reflects UAT behaviour but not yet confirmed as a requirement |
| **Assumption** | Implementation choice made to keep progress; must be confirmed or corrected |
| **TBD – Confirmation Required** | Not known; not to be assumed |

---

## 1. Discussion Summary

| ID | Date | Module / Screen | Topic | Discussion / Requirement | Decision / Final Understanding | Status |
| --- | --- | --- | --- | --- | --- | --- |
| DISC-001 | 22-09-2026 | Whole journey | Scope & approach | Rebuild the LAMF online journey as a clickable HTML prototype from the shared screenshots, same design, same colour codes, same content | Build all screens first; CTA actions, field logic and dropdown values to be given screen by screen afterwards; PRD to be written at the end in the user's preferred format | Confirmed |
| DISC-002 | 22-09-2026 | Whole journey | File structure | One HTML file per screenshot, named as per the screenshot name with numbering for sort order | 37 screens created with the user's naming (`01) …` to `16.5.9) …`). Shared CSS/JS so one change applies to all pages | Implemented |
| DISC-003 | 22-09-2026 | Whole journey | Assets | Logos, hero image, fund icons, DigiLocker/MF Central logos | Cropped from the shared screenshots (user's choice over placeholders) | Confirmed |
| DISC-004 | 22-09-2026 | Whole journey | Scope boundary | Screens not present in the screenshots (Sl. 15, Photo Verification, Bank Details, Pledging, Agreement & E-Mandate) | Build only what exists in the screenshots; remaining screens to be added when screenshots are shared | Confirmed |
| DISC-005 | 22-09-2026 | Landing page | CTA behaviour | "Check your eligibility in 2 minutes" and "Start Your Application" | Both CTAs start the LAMF journey and open `02) Enter MF linked Mobile Number` (first step = mobile number verification) | Implemented |
| DISC-006 | 22-09-2026 | Mobile Number Verification | Close icon | Close icon on the mobile number popup | Closes the popup and returns the user to the previous page (landing page) | Implemented |
| DISC-007 | 22-09-2026 | Mobile Number Verification | Input rules | Numeric only, min & max 10 characters, no alphabet / space / special characters, number cannot start with 0–5 | Implemented with field-level error messages; entry of a disallowed character or a leading 0–5 is not accepted | Implemented |
| DISC-008 | 22-09-2026 | Mobile Number Verification | Consent checkbox | Ticking the checkbox enables the Continue CTA | Continue stays disabled (grey) until the checkbox is ticked | Implemented |
| DISC-009 | 22-09-2026 | Mobile Number Verification | T&C / Privacy Policy links | Both hyperlinks open a popup with a close icon and an Accept CTA; content from shriramcredit.in | Popups built with all section headings from the two live pages; body text currently a plain-language summary, not verbatim legal text | Implemented (content pending, PEND-005) |
| DISC-010 | 22-09-2026 | Mobile Number Verification | Continue CTA | On Continue, all conditions to be checked first; if anything falls under the not-allowed category, block the user and show the respective validation | Validation order implemented: consent → empty → starting digit → length; only on full pass does it open `03) Enter OTP …` | Implemented |
| DISC-011 | 22-09-2026 | Documentation | Discussion log | Maintain `LAMF_LOS_DISCUSSION_LOG.md` as a living single log of discussions, decisions, changes and pending items; update it as part of the normal workflow, including common and page-wise validation rules | This document created and will be updated after every meaningful requirement/clarification, before continuing development work | Implemented |
| DISC-012 | 23-09-2026 | All popup screens | Background scroll | When a popup is open (mobile number, OTP and all other popups), the background page must not scroll — it has to freeze. Only the popup itself should scroll, and only when required, e.g. when the user has zoomed in far enough that the popup does not fit on screen | Page behind a popup is locked; the popup scrolls inside its own overlay when it is taller than the viewport. Applied as a common rule to every popup screen | Implemented |
| DISC-013 | 23-09-2026 | OTP Verification (mobile) | Full screen behaviour | Close icon → landing page; Edit → previous page with the entered mobile number prefilled; resend timer runs 30 → 01 and then enables Resend OTP; 3 back-to-back resends then blocked for 15 minutes with a dynamic remaining time; OTP box numeric only, max 6, no alphabet/space/special; Submit enabled only when 6 digits entered AND Experian consent ticked; Submit re-checks all conditions; wrong OTP shows validation and 3 wrong attempts block the user for 60 minutes; on success the mobile number is sent to the Experian API for the credit score and the user lands on PAN verification | Implemented as stated. Block state is stored against the mobile number and survives refresh/navigation; remaining minutes are recalculated from the block time, so a user returning after 10 minutes of a 15-minute block sees 5 minutes | Implemented |
| DISC-014 | 23-09-2026 | Documentation | PRD format | Sample PRD shared: `SCCL_LAMF_LOS_PRD_Module_1 (3).docx` — table format with columns SL.No / Screenshot / Functionality / Description / Data Points Required / Status, field-level specs written as Field Name, Field Type, Minimum & Maximum Character, Value Type, Input Value format, Action, Validation, and element-level screenshot crops per field. PRD to be built in parallel as HTML, updated after each discussion, and hosted locally | PRD created at `SCCL_LAMF_LOS_PRD.html` in the same format, covering Module 1 (Mobile Number Verification) and Module 2 (OTP Verification), plus integration and pending-clarification tables. It is regenerated from `tools/build_prd.py` after every confirmed update | Implemented |
| DISC-015 | 23-09-2026 | Hosting | Cloud hosting | Prototype to be hosted in the cloud in addition to the local server; git CLI to be set up. Purpose clarified on 24-09-2026: the user needs to review the prototype from this laptop **and** a second laptop, independent of network and of this machine being switched on | Git already available (2.50.1); local repository created with the first commit. Prototype published as a private cloud page. Because the cloud viewer cannot navigate between separate HTML files, a single-page copy (`cloud.html`) was generated from the same screen templates — the local multi-file copy is unchanged | Implemented |
| DISC-016 | 24-09-2026 | Prototype home | Home page & logo navigation | Replace the screen-list start page with a home page: Shriram Credit logo, a title, and two CTAs in one row at the centre of the page — "Open the PRD document →" on the left (opens the PRD) and "Start the LAMF journey →" on the right (opens a new page listing all screens, same as the old start page but without the PRD CTA). The Shriram Credit logo on every page must navigate back to this home page | `index.html` is now the home page; the screen list moved to `screens.html`; the logo in every screen header, the landing-page footer, the screen list and the PRD header links to the home page. The PRD's "All screens →" button now opens `screens.html`. Screens 16.5.1–16.5.7 (DigiLocker/Digio look-alikes) carry no Shriram logo, so they are unchanged | Implemented |
| DISC-017 | 24-09-2026 | PRD | Integration Requirements column guide | Add an (i) icon next to the "Integration Requirements" heading; placing the cursor on it shows what each column means (ID, Integration, Purpose, Trigger, Input, Expected Output, Success Behaviour, Failure Behaviour) | Implemented in the PRD (local and cloud copy). The guide also opens on keyboard focus or a tap on touch screens, and is left out of the printed / PDF copy. Column texts live in `INT_COLUMNS` in `tools/build_prd.py` | Implemented |
| DISC-018 | 24-09-2026 | PRD | TBD items tracked as pending clarifications | Anything not yet defined (e.g. what Experian returns) must be listed in the PRD's Pending Clarifications until answered; add the same (i) column guide to Pending Clarifications | Added P-09 (Experian response content, PEND-024) and P-10 (OTP vendor + verify failure, PEND-025). Every TBD in Integration Requirements now names its pending item ("TBD, see P-09"). (i) guide added to Pending Clarifications (ID, Module, Clarification Required, what happens when answered) | Implemented |
| DISC-019 | 24-09-2026 | PRD | Pending badges & Completed Clarifications | Make "TBD, see P-xx" references clearly visible as pending. Add a Completed Clarifications section with the same columns as Pending plus a column for the answer, with an (i) guide, collapsed behind a dropdown so the PRD does not get too long | Every undecided item in the PRD (Integration Requirements, Module 1 note, Module 2 PAN note and Experian data point) now shows an amber "Pending · P-xx" badge; clicking it scrolls to that pending row and briefly highlights it. New collapsed "Completed Clarifications" section (count badge, (i) guide, chevron to open/close) with columns ID, Module, Clarification Required, Clarification Provided (+ answered date). It starts with P-11 – P-15 = PEND-006 – PEND-010, answered 23-09-2026. From now on an answered P-xx keeps its ID and moves from Pending to Completed. The printed/PDF copy shows the section expanded | Implemented |
| DISC-020 | 25-09-2026 | PRD | Pending count badge | Show the number of pending clarifications next to the "Pending Clarifications" heading, like the green completed count, in the pending (amber) colour | Amber count added (currently 10); both counts are generated from the lists, so they update automatically as questions move from Pending to Completed | Implemented |
| DISC-021 | 25-09-2026 | PRD | Status badge alignment | "Pending Confirmation" status badge was spilling outside the Status column | Status column widened from 110px to 165px so the badge fits on one line; a status label that is ever too long now wraps inside its cell instead of overflowing. Checked: no badge overflows at 1440px or 1100px wide | Implemented |

---

## 2. Module-Wise Decisions

### 2.1 Landing Page

**Screen:** `01) LAMF Landing Page`

**Confirmed Requirements**

* Public marketing page carrying the Shriram Credit site header, hero, "How to Apply for a Loan Against Mutual Fund (LAMF)?" 8-step block and site footer.
* Two CTAs start the journey.

**CTA Behaviour**

| CTA | Action | Next Screen |
| --- | --- | --- |
| Check your eligibility in 2 minutes (hero) | Start LAMF journey → mobile number verification | `02) Enter MF linked Mobile Number` |
| Start Your Application (below the 8 steps) | Same as above | `02) Enter MF linked Mobile Number` |

**Observed (from screenshot, not confirmed as requirement)**

* Hero claims: interest rate starting at 10.5% p.a.*, 100% paperless, instant loan approval, interest-only repayment and EMI options, RBI regulated NBFC with 25+ years of legacy.
* Header nav items and footer link groups are static marketing links.

**Pending Clarifications**

* PEND-001 – Behaviour of header/footer navigation links inside the prototype (out of journey scope?).

---

### 2.2 Mobile Number Verification

**Screen:** `02) Enter MF linked Mobile Number` (popup over the landing page)

**Confirmed Requirements**

1. First step of the LAMF journey is mobile number entry for mobile number verification.
2. Field is a numeric text box: alphabets, spaces and special characters must not be enterable.
3. Minimum and maximum length is 10 characters.
4. A number starting with 0, 1, 2, 3, 4 or 5 is an invalid mobile number and must not be allowed; the respective validation is shown.
5. Ticking the consent checkbox enables the Continue CTA.
6. The T&C and Privacy Policy hyperlinks each open a popup containing a close icon and an Accept CTA; content is taken from the Shriram Credit website.
7. Close icon on the popup returns the user to the previous page.
8. On Continue, all conditions are checked; anything in the not-allowed category blocks the user with the respective validation message.
9. On successful validation, the user moves to `03) Enter OTP for MF linked Mobile Number Verification`.
10. While the popup is open the landing page behind it must stay frozen; only the popup scrolls, and only if it does not fit the screen (DISC-012).

**CTA Behaviour**

| CTA | Action | Next Screen | Condition |
| --- | --- | --- | --- |
| Close (✕) | Close popup, go back | `01) LAMF Landing Page` | Always |
| T&C (hyperlink) | Open Terms & Conditions popup | – (popup) | Always |
| Privacy Policy (hyperlink) | Open Privacy Policy popup | – (popup) | Always |
| Accept (inside T&C / Privacy popup) | Close popup; **Assumption:** also ticks the consent checkbox | – | Always |
| Close (inside T&C / Privacy popup) | Close popup only, no consent change | – | Always |
| Continue | Validate, then proceed | `03) Enter OTP for MF linked Mobile Number Verification` | Consent ticked + valid 10-digit number starting 6–9 |

**Validation (implemented messages)**

| # | Rule | Error message | Trigger |
| --- | --- | --- | --- |
| V-02.1 | Only numeric allowed | `Only numbers are allowed. Letters, spaces and special characters cannot be entered.` | On typing / pasting a non-numeric character (character is not accepted) |
| V-02.2 | Cannot start with 0–5 | `Mobile number cannot start with 0, 1, 2, 3, 4 or 5. Please enter a valid mobile number.` | On entering/pasting a leading 0–5 (digit is not accepted) |
| V-02.3 | Exactly 10 digits | `Mobile number must be 10 digits.` | On blur with 1–9 digits, and on Continue |
| V-02.4 | Mandatory | `Please enter your MF linked mobile number.` | On Continue with empty field |
| V-02.5 | Consent mandatory | `Please accept the T&C and Privacy Policy to continue.` | On Continue while checkbox is unticked |

**Error behaviour:** message shown in red below the field; field border turns red; message clears when the value becomes valid (10 digits starting 6–9).

**Observed (from screenshot)**

* Placeholder text `9876543210`.
* Consent text: "By proceeding, I agree to T&C and Privacy Policy of Shriram Credit."

**Pending Clarifications**

* PEND-002 – Is the mobile number checked against any backend rule at this stage (existing customer / blacklist / duplicate application)?
* PEND-003 – Should Continue trigger an OTP send API, and what happens on API failure?
* PEND-004 – Should the Accept CTA inside the T&C/Privacy popup tick the consent checkbox (current assumption) or only close the popup?
* PEND-005 – Should the popups carry the full verbatim T&C and Privacy Policy text instead of the current summarised version?

---

### 2.3 OTP Verification (MF linked Mobile Number)

**Screen:** `03) Enter OTP for MF linked Mobile Number Verification` (popup over the landing page)

**Confirmed Requirements** (DISC-013)

1. Close icon closes the popup and the user lands on the landing page.
2. Edit icon takes the user back to the previous page (`02`), with the mobile number the user entered prefilled.
3. Resend timer starts at 30 seconds and runs down to 01; at 0 the **Resend OTP** CTA is enabled.
4. Clicking Resend OTP sends the OTP again and restarts the timer. The user may resend back-to-back 3 times; on the 3rd, a validation is shown and the user cannot proceed for 15 minutes. The wait shown must be based on the block date/time, so a user returning after 10 minutes sees the balance 5 minutes.
5. OTP boxes accept numeric only, maximum 6 characters; alphabets, spaces and special characters are not allowed.
6. Submit OTP is enabled only when the Experian consent is ticked **and** all 6 digits are entered.
7. Submit OTP re-checks every condition: if all are met the user proceeds, otherwise the respective validation is displayed.
8. A wrong OTP shows a validation. After 3 back-to-back wrong attempts the user is blocked for 60 minutes (same dynamic remaining-time behaviour as the resend block).
9. When all conditions are met, the mobile number is sent to the Experian API to retrieve the credit score, and the user lands on the PAN verification page.

**CTA Behaviour**

| CTA | Action | Next Screen | Condition |
| --- | --- | --- | --- |
| Close (✕) | Close popup | `01) LAMF Landing Page` | Always |
| Edit | Back to mobile number entry, prefilled | `02) Enter MF linked Mobile Number` | Always |
| Resend OTP | Resend OTP, restart the 30s timer, clear entered digits | – | Only after the timer reaches 0 and resend count < 3 |
| Submit OTP | Validate all conditions → Experian credit score call (INT-001) | `04) Enter PAN Details` | 6 digits + consent ticked + correct OTP + not blocked |

**Validation (implemented messages)**

| # | Rule | Message |
| --- | --- | --- |
| V-03.1 | Numeric only in OTP boxes | `Only numbers are allowed. Letters, spaces and special characters cannot be entered.` |
| V-03.2 | All 6 digits required | `Please enter the 6-digit OTP.` |
| V-03.3 | Experian consent required | `Please provide the consent to proceed.` |
| V-03.4 | Wrong OTP (attempts 1 and 2) | `The OTP you entered is incorrect. Please try again. N attempt(s) remaining.` |
| V-03.5 | 3 wrong OTP attempts | `You have entered an incorrect OTP 3 times. Please try again after N minutes.` (N recalculated from block time) |
| V-03.6 | 3 resends used | `You have used all 3 OTP resend attempts. Please try again after N minutes.` (N recalculated from block time) |

**Block behaviour:** while blocked, the OTP boxes, consent and Submit OTP are disabled and Resend OTP is greyed out. When the block time passes, the screen unlocks by itself and the attempt counters reset to 0.

**Assumptions (to be confirmed)**

* A-03.1 – Prototype accepts `123456` as the correct OTP (no OTP service is called). PEND-016.
* A-03.2 – Attempt counters and blocks are held against the mobile number in browser storage; in the real system this must be enforced server-side. PEND-017.
* A-03.3 – Both counters reset when the block expires and after a successful verification. PEND-018.
* A-03.4 – The mobile number entered on screen 02 is also carried to the PAN screen's read-only Mobile Number field.

**Observed (from screenshot)**

* Title "Enter OTP"; line "A 6-digit OTP has been sent by Shriram Credit to +91XXXXXXXX" with masking pattern `+91` + first 2 digits + `XXXX` + last 4 digits.
* While the timer runs the line reads "Didn't Receive OTP? 0:28 Resend OTP" in grey; once enabled, "Resend OTP" turns yellow.

---

### 2.4 PAN Verification

**Screen:** `04) Enter PAN Details`

**Status:** Screen built; behaviour **TBD – Confirmation Required**.

**Observed (from screenshot)**

* Fields: Mobile Number (prefilled, appears non-editable/greyed), Name as per PAN, DOB (`DD/MM/YYYY` with calendar icon), PAN Number (placeholder `ABCDE 1234 F`).
* Continue CTA shown enabled in the screenshot.
* Header shows a logout icon instead of dashboard/profile icons.

---

### 2.5 MF Central Consent & Redirection

**Screens:** `05) LOS to MF Central Redirection consent page`, `06) …loading page`, `07) MF Central Mock Page`, `08) MF Central to LOS Redirecting Page`, `09) …Fetching Mutual Fund Portfolio Page`

**Status:** Screens built; behaviour **TBD – Confirmation Required**.

**Observed (from screenshot)**

* Consent screen shows PAN (prefilled, greyed) and the authorisation checkbox: "I authorize Shriram Credit to fetch my mutual fund portfolio holdings from MF Central to assess my eligibility and credit limit for a Loan Against Mutual Funds." Check Credit Limit CTA is disabled until (presumably) the checkbox is ticked.
* Redirect popup: MF Central logo, "Redirecting to MF Central in 3 seconds", progress bar, two instructions (enter 6-digit MF Central OTP; select all AMCs and continue), note that the user returns automatically.
* Loading states: "Fetching your mutual fund portfolio..", "Analyzing your mutual fund portfolio..", "Generating best loan offers for you" — all with "This might take a min, thanks for your patience".
* Left panel content: "Get a Loan up to 75% of your eligible Mutual Fund portfolio", interest-only EMI payments, disbursal in 2 hours post application, and a 9-step "How it works" list.

---

### 2.6 Curated Offers / Dashboard

**Screens:** `12) Curated Offers Page`, `12.2) Curated offers page for dorpoff view`, `12.2) Refresh portfolio`

**Status:** Screens built; behaviour **TBD – Confirmation Required**.

**Observed (from screenshot)**

* Offer card: Credit Limit ₹ 6,19,13,200 (underlined, appears clickable → "How is it calculated"), Interest Rate 10.50% p.a., Processing Fee ₹ 3,09,566, Tenure in Months 12, CTA "Start Application".
* Drop-off view: progress strip "1/4 Complete your application to get cash" with **Discard** and **Continue** CTAs replacing Start Application.
* Total Portfolio Value ₹ 12,04,62,749.99; "Last updated: 21-09-2026 16:11:46" with a "Refresh portfolio" link.
* Fund list: 13 funds with No. of Units (2 decimals) and Current Value; grouped under a mobile-number strip showing "13 Security • ₹ 12,04,62,749.99".
* Top banner text varies between screenshots: "Borrow only what you need and pay interest only on the utilised amount" and "Avail a loan of up to 75% of your eligible Mutual Fund portfolio" (appears to rotate).
* Refresh popup: "Refresh all linked portfolios to continue", mobile number, "Last refreshed Today", "Refresh Portfolio" link.

---

### 2.7 Credit Limit Calculation View ("How is it calculated")

**Screens:** `12.1.1) All Portfolio`, `12.1.2) Eligible Portfolio`, `12.1.3) Non Eligible Portfolio`

**Status:** Screens built; behaviour **TBD – Confirmation Required**.

**Observed (from screenshot)**

* Header card: "Your maximum credit limit is ₹ 6,19,13,200".
* Breakdown: Total Portfolio Value ₹ 12,04,62,749.99 − Non-Eligible Portfolio Value ₹ 3,13,02,090.97 = Eligible Portfolio Value ₹ 8,91,60,659.02; Credit Limit Available ₹ 6,19,13,200.
* Tabs: All (13 securities) / Eligible Portfolio (9) / Non-Eligible Portfolio (4).
* Fund rows show Pledgeable Units (3 decimals), Current Value, Credit Limit; non-eligible funds carry a red "Not Eligible" strip and Credit Limit ₹ 0.
* Eligible tab appears sorted by Credit Limit (highest first); All tab follows the MF Central response order.

---

### 2.8 Mutual Fund Selection

**Screens:** `13.1` – `13.6`

**Status:** Screens built; behaviour **TBD – Confirmation Required**.

**Observed (from screenshot)**

* Stepper: 1 Selection of Mutual Fund · 2 KYC Verification & Bank details · 3 Pledging of Mutual Fund · 4 Agreement & E-Mandate.
* Loan Amount box with editable amount (pencil icon → inline edit with an "Update" link) and a slider from ₹ 10,000 to ₹ 2,00,00,000.
* "Funds selected for pledging", current market value of selected units, number of funds selected, Select All (indeterminate state shown).
* Only the 9 eligible funds are listed ("9 Fund • ₹ 8,91,60,659.02"); each row has a checkbox, Selected Amount (editable, pencil icon), No of Units, Current Value, Max Limit.
* Location permission is required: browser prompt shown; if blocked, a toast appears — "Kindly provide location access in order to proceed with the loan application." with a **Refresh** link, and the Continue CTA is disabled.
* Resume flow: modal "You have an ongoing loan application, would you like to proceed further with it?" with CTAs "No, Take me to the dashboard" and "Yes, Continue".
* Sticky CTA: "Continue to apply ₹ <amount>".
* Example state: loan ₹ 2,00,00,000 split as ICICI ₹ 1,40,30,794 + Axis ₹ 53,69,420 + Kotak ₹ 5,99,786 (3 funds, market value ₹ 2,66,66,667.21).

---

### 2.9 Loan Application Summary

**Screen:** `14) Loan Application Summary`

**Status:** Screen built; behaviour **TBD – Confirmation Required**.

**Observed (from screenshot)**

* Loan amount ₹ 1,55,36,100; Pledge Value ₹ 2,07,14,800.22.
* Tenure 12 months; Disbursement Type Multiple; Repayment Type Interest Only.
* Interest Rate 10.5% p.a; Monthly Interest ₹ 1,35,940.88.
* Charges (inclusive of GST): Processing fee ₹ 91,664; Stamp duty ₹ 236; Lien Marking Charges ₹ 531; Lien Removal Charges ₹ 118.
* Repayment details: Interest autopay — 5th of every month.

---

### 2.10 KYC Verification

**Screens:** `16.1` – `16.4`, `16.5.8`, `16.5.9`

**Status:** Screens built; behaviour **TBD – Confirmation Required**.

**Observed (from screenshot)**

* Five sub-steps in order: 1 Email Verification · 2 PAN Verification · 3 Aadhaar Verification with DigiLocker · 4 Photo Verification · 5 Bank Details.
* Status chips: `Complete` (green) / `Pending` (amber).
* PAN Verification is already Complete when the KYC screen opens (carried from step 04).
* Email: single input with note "We will use this email address for all official communications related to your loan application and account.", Verify CTA, then a 6-digit OTP popup with "Didn't receive OTP? 0:29 Resend OTP".
* Loan strip at top: "Your loan amount is ₹ 1,55,36,100" with a "View details" link opening the Loan details popup (Loan Amount, Market Value of MF selected, No. of MF selected, and the funds selected for pledging).
* Aadhaar step: "Start KYC" CTA → DigiLocker via DIGIO; while polling, an amber "Getting status / This might take up to 2m:58s" button with the note "Your Aadhaar details are being fetched from DigiLocker. This process may take a few minutes. Please keep this tab open and avoid refreshing the page."
* After Aadhaar completes, Photo Verification opens with a "Start" CTA.

---

### 2.11 Aadhaar / DigiLocker (DIGIO) Sub-Journey

**Screens:** `16.5.1` – `16.5.7`

**Status:** Screens built as look-alike mock-ups of the third-party pages; behaviour **TBD – Confirmation Required**.

**Observed (from screenshot)**

* DIGIO gateway (`ext.digio.in`): 4 steps — enter Aadhaar number, enter OTP and PIN (optional), select requested documents (Issued Documents (2): Aadhaar Card, PAN Verification Record), document fetch from DigiLocker; authorisation checkbox naming SHRIRAM CREDIT COMPANY LIMITED; Cancel / Proceed CTAs.
* DigiLocker (`accounts.digitallocker.gov.in`): Sign up → Aadhaar number (3 × 4 digits) → Verify Aadhaar OTP → 6-digit Security PIN → Done.
* DIGIO "Securely fetching documents – Please do not refresh or close the window", then exit page "KYC process completed – Do not close the window. You will be redirected."
* LOS return page: "KYC successfully completed. Redirecting you back to the process in 1 seconds".

---

## 3. Business Rules

| Rule ID | Module | Business Rule | Status | Source / Discussion ID |
| --- | --- | --- | --- | --- |
| BR-001 | Journey entry | The LAMF online journey starts with mobile number verification; both landing page CTAs lead to it | Confirmed | DISC-005 |
| BR-002 | Mobile Verification | Mobile number must be numeric only — alphabets, spaces and special characters are not permitted | Confirmed | DISC-007 |
| BR-003 | Mobile Verification | Mobile number must be exactly 10 digits (min = max = 10) | Confirmed | DISC-007 |
| BR-004 | Mobile Verification | Mobile number must not start with 0, 1, 2, 3, 4 or 5 (valid first digit 6–9) | Confirmed | DISC-007 |
| BR-005 | Mobile Verification | T&C and Privacy Policy consent is mandatory; Continue remains disabled until the consent checkbox is ticked | Confirmed | DISC-008 |
| BR-006 | Mobile Verification | All field conditions must pass before navigation; any not-allowed condition blocks the user with the respective validation message | Confirmed | DISC-010 |
| BR-009 | OTP | OTP is 6 digits, numeric only; alphabets, spaces and special characters are not permitted | Confirmed | DISC-013 |
| BR-010 | OTP | Submit OTP is enabled only when all 6 digits are entered and the Experian consent is ticked | Confirmed | DISC-013 |
| BR-011 | OTP | OTP resend is available only after the 30-second timer ends; a maximum of 3 back-to-back resends is allowed, after which the customer is blocked for 15 minutes | Confirmed | DISC-013 |
| BR-012 | OTP | 3 consecutive wrong OTP attempts block the customer for 60 minutes | Confirmed | DISC-013 |
| BR-013 | OTP | The remaining wait shown during a block is calculated from the block date/time, not a fixed message | Confirmed | DISC-013 |
| BR-014 | OTP | On successful mobile verification, the mobile number is sent to Experian for the credit score; the customer proceeds to PAN verification without waiting for the response | Confirmed | DISC-013 |
| BR-008 | UX – popups | A popup freezes the page behind it; background scrolling is not permitted while a popup is open. The popup itself scrolls only when its content does not fit the screen | Confirmed | DISC-012 |
| BR-007 | Scope | Only screens available as screenshots are to be built; remaining journey steps await screenshots | Confirmed | DISC-004 |

*Observed values such as LTV 75%, ROI 10.50% p.a., tenure 12 months, slider range ₹ 10,000 – ₹ 2,00,00,000 and the charge amounts are **not** listed as business rules yet — they are recorded as Observed in Section 2 and need confirmation (PEND-011).*

---

## 4. CTA & Navigation Decisions

| Screen | CTA | Action | Next Screen | Conditions | Status |
| --- | --- | --- | --- | --- | --- |
| 01) LAMF Landing Page | Check your eligibility in 2 minutes | Start journey | 02) Enter MF linked Mobile Number | None | Implemented |
| 01) LAMF Landing Page | Start Your Application | Start journey | 02) Enter MF linked Mobile Number | None | Implemented |
| 02) Enter MF linked Mobile Number | Close (✕) | Close popup, return to previous page | 01) LAMF Landing Page | None | Implemented |
| 02) Enter MF linked Mobile Number | T&C | Open T&C popup | – | None | Implemented |
| 02) Enter MF linked Mobile Number | Privacy Policy | Open Privacy Policy popup | – | None | Implemented |
| 02) T&C / Privacy popup | Accept | Close popup; ticks consent (Assumption) | – | None | Implemented / PEND-004 |
| 02) T&C / Privacy popup | Close (✕) | Close popup | – | None | Implemented |
| 02) Enter MF linked Mobile Number | Continue | Validate all conditions, then proceed | 03) Enter OTP for MF linked Mobile Number Verification | Consent ticked AND 10-digit number starting 6–9 | Implemented |
| 03) Enter OTP … | Close (✕) | Close popup | 01) LAMF Landing Page | None | Implemented |
| 03) Enter OTP … | Edit | Back to mobile entry, prefilled | 02) Enter MF linked Mobile Number | None | Implemented |
| 03) Enter OTP … | Resend OTP | Resend OTP, restart 30s timer | – | Timer at 0 and resends used < 3 | Implemented |
| 03) Enter OTP … | Submit OTP | Validate all → Experian credit score call | 04) Enter PAN Details | 6 digits + consent + correct OTP + not blocked | Implemented |
| 04) Enter PAN Details | Continue | TBD – Confirmation Required | TBD | TBD | Pending |
| 05) MF Central consent | Check Credit Limit | TBD – Confirmation Required | TBD | TBD | Pending |
| 12) Curated Offers | Start Application / Credit Limit link / Refresh portfolio | TBD – Confirmation Required | TBD | TBD | Pending |
| 12.2) Drop-off view | Discard / Continue | TBD – Confirmation Required | TBD | TBD | Pending |
| 13.x) MF Selection | Continue to apply / Select All / Update / edit amount | TBD – Confirmation Required | TBD | TBD | Pending |
| 14) Loan Application Summary | Continue | TBD – Confirmation Required | TBD | TBD | Pending |
| 16.x) KYC | Verify / Start KYC / Start / View details | TBD – Confirmation Required | TBD | TBD | Pending |

---

## 5. Field & Validation Decisions

| Screen | Field | Type | Mandatory | Editable | Values / Source | Validation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 02 | MF linked Mobile Number | Numeric text box, max 10 | Yes | Yes | User input; placeholder `9876543210` | V-02.1 to V-02.4 (Section 2.2) | Confirmed |
| 02 | T&C / Privacy consent | Checkbox | Yes | Yes | Unticked by default | V-02.5 – Continue disabled until ticked | Confirmed |
| 03 | OTP | 6 boxes, numeric, 1 char each | Yes | Yes | Sent by Shriram Credit to the registered mobile | V-03.1, V-03.2; 3 wrong attempts → 60 min block | Confirmed |
| 03 | Experian consent | Checkbox | Yes | Yes | Unticked by default | V-03.3; Submit enabled only with consent + 6 digits | Confirmed |
| 04 | Mobile Number | Text, prefilled | – | Non-editable | Carried from step 02 (the number the user entered) | – | Confirmed (A-03.4) |
| 04 | Name as per PAN | Text | TBD | TBD | TBD | TBD (name-match rule?) | Pending |
| 04 | DOB | Date `DD/MM/YYYY` | TBD | TBD | Calendar picker | TBD (18+ check?) | Pending |
| 04 | PAN Number | Text, format `ABCDE1234F` | TBD | TBD | User input | TBD (PAN regex, NSDL check) | Pending |
| 05 | PAN Number | Text, prefilled | TBD | Appears non-editable (observed) | From step 04 | TBD | Pending |
| 05 | MF Central authorisation | Checkbox | TBD (appears mandatory) | TBD | Unticked by default | TBD | Pending |
| 13.x | Loan Amount | Numeric + slider | TBD | Yes (observed) | Range ₹ 10,000 – ₹ 2,00,00,000 (observed) | TBD (rounding, max = credit limit?) | Pending |
| 13.x | Selected Amount per fund | Numeric, inline edit | TBD | Yes (observed) | 0 to Max Limit per fund | TBD (sum must equal loan amount?) | Pending |
| 16.x | Email | Email text box | TBD | Yes | User input | TBD (format, domain, OTP) | Pending |

*No dropdown fields have appeared in the screenshots shared so far. Dropdown values will be recorded here when provided (PEND-012).*

---

## 6. Rules & Condition Validations

### 6.1 Common Rules (apply across the journey)

| ID | Rule | Applies to | Status |
| --- | --- | --- | --- |
| CV-001 | Disabled CTAs are grey (`#E9EAEB` background, `#A4A7AE` text) and become yellow (`#FFCB08`) once their enabling condition is met | All screens with a primary CTA | Implemented (from screenshots) |
| CV-002 | Validation messages appear below the concerned field in red, and the field border turns red | All input fields | Implemented (pattern set on screen 02) |
| CV-003 | Mandatory consent checkboxes are unticked by default and gate the CTA | 02 (T&C), 03 (Experian – TBD), 05 (MF Central – TBD) | Partly confirmed |
| CV-004 | OTP entry uses 6 single-character numeric boxes with auto-advance | 03, 16.3 (email OTP), DigiLocker PIN (6 boxes) | Implemented (from screenshots) |
| CV-005 | Resend OTP is locked behind a countdown timer: 30 seconds on screen 03 (confirmed, DISC-013); email OTP timer on 16.3 still TBD | 03, 16.3 | Confirmed for 03 |
| CV-006 | Amounts are displayed in Indian grouping with the ₹ symbol; portfolio values show 2 decimals; units show 3 decimals on calculation/selection screens and 2 decimals on the curated offers list | 12, 12.1.x, 13.x, 14, 16.2 | Observed |
| CV-007 | Popups open over a dimmed, blurred page; a close icon returns to the underlying screen | 02, 03, 06, 09, 10, 11, 12.2, 16.2, 16.3 | Implemented |
| CV-008 | Prefilled data carried from an earlier step is shown greyed / non-editable | 04 (mobile), 05 (PAN) | Observed – to be confirmed |
| CV-009 | Journey progress is shown by a 4-step stepper (Selection of Mutual Fund → KYC Verification & Bank details → Pledging of Mutual Fund → Agreement & E-Mandate) with completed steps in yellow with a tick | 13.x, 14, 16.x | Implemented |
| CV-010 | Location access is mandatory to proceed with the loan application | 13.x (confirmed by screenshot toast); other screens TBD | Observed |
| CV-011 | Long-running operations show a skeleton loader with a title and "This might take a min, thanks for your patience" | 09, 10, 11 | Implemented |
| CV-013 | While a popup is open the page behind it is frozen (no background scroll); the popup scrolls within itself only when it does not fit the viewport (e.g. on zoom). Applies to every popup in the journey | 02, 03, 06, 09, 10, 11, 12.2, 13.4, 16.2, 16.3 and any future popup | Confirmed (DISC-012) |
| CV-012 | Session/back behaviour, timeout and refresh handling across the journey | All | **TBD – Confirmation Required** (PEND-013) |

### 6.2 Page-Wise Validations

| Screen | Validation / condition | Message | Status |
| --- | --- | --- | --- |
| 01) Landing | None (informational page) | – | Confirmed |
| 02) Mobile Number | Numeric only | `Only numbers are allowed. Letters, spaces and special characters cannot be entered.` | Confirmed |
| 02) Mobile Number | Cannot start with 0–5 | `Mobile number cannot start with 0, 1, 2, 3, 4 or 5. Please enter a valid mobile number.` | Confirmed |
| 02) Mobile Number | Exactly 10 digits | `Mobile number must be 10 digits.` | Confirmed |
| 02) Mobile Number | Mandatory field | `Please enter your MF linked mobile number.` | Confirmed |
| 02) Mobile Number | Consent mandatory | `Please accept the T&C and Privacy Policy to continue.` | Confirmed |
| 03) OTP | Numeric only, 6 digits, no alphabet/space/special | `Only numbers are allowed…` / `Please enter the 6-digit OTP.` | Confirmed |
| 03) OTP | Experian consent mandatory; Submit enabled only with consent + 6 digits | `Please provide the consent to proceed.` | Confirmed |
| 03) OTP | Wrong OTP; 3 attempts then 60-minute block | `The OTP you entered is incorrect…` / `You have entered an incorrect OTP 3 times…` | Confirmed |
| 03) OTP | Resend allowed only after the 30s timer; 3 resends then 15-minute block | `You have used all 3 OTP resend attempts…` | Confirmed |
| 03) OTP | OTP validity/expiry period | TBD | **TBD – Confirmation Required** (PEND-021) |
| 04) PAN Details | PAN format, name-as-per-PAN match, DOB/age rule, PAN verification failure | TBD | **TBD – Confirmation Required** |
| 05) MF Central consent | Authorisation checkbox mandatory; PAN non-editable | TBD | **TBD – Confirmation Required** |
| 07) MF Central mock | OTP rules on the MF Central side | TBD | **TBD – Confirmation Required** |
| 12) Curated Offers | Portfolio refresh mandatory before proceeding? Offer validity? | TBD | **TBD – Confirmation Required** |
| 12.1.x) How is it calculated | Eligibility rule that classifies a fund as Eligible / Non-Eligible (equity vs debt, AMC list, LTV) | TBD | **TBD – Confirmation Required** |
| 13.x) MF Selection | Minimum/maximum loan amount, amount vs credit limit, per-fund max limit, at least one fund selected, allocation logic when the loan amount changes, location access mandatory | TBD | **TBD – Confirmation Required** |
| 14) Summary | Any acceptance required before Continue? | TBD | **TBD – Confirmation Required** |
| 16.1–16.4) KYC | Email format, OTP rules, sequencing (can a later step be started before an earlier one completes?) | TBD | **TBD – Confirmation Required** |
| 16.5.x) DigiLocker | Aadhaar format, OTP/PIN rules, polling duration and timeout, cancel/failure handling | TBD | **TBD – Confirmation Required** |

---

## 7. Change Log

| Change ID | Date | Module | Previous Decision | New Decision | Reason / Discussion | Status |
| --- | --- | --- | --- | --- | --- | --- |
| – | – | – | – | – | No requirement changes recorded yet | – |

---

## 8. Pending Clarifications

| Pending ID | Module | Question / Clarification Required | Raised On | Status |
| --- | --- | --- | --- | --- |
| PEND-001 | Landing page | Should header/footer navigation links do anything in the prototype? | 22-09-2026 | Open |
| PEND-002 | Mobile Verification | Any backend check on the mobile number at this step (existing customer, duplicate/ongoing application, blacklist)? | 22-09-2026 | Open |
| PEND-003 | Mobile Verification | Does Continue call an OTP-send API, and what is the failure behaviour? | 22-09-2026 | Open |
| PEND-004 | Mobile Verification | Should Accept in the T&C/Privacy popup tick the consent checkbox, or only close the popup? | 22-09-2026 | Open |
| PEND-005 | Mobile Verification | Should the T&C/Privacy popups carry the full verbatim legal text instead of the summary? | 22-09-2026 | Open |
| PEND-006 | OTP | OTP length, resend timer duration and number of resends allowed | 22-09-2026 | **Answered 23-09-2026** – 6 digits, 30-second timer, 3 resends (DISC-013). Validity period still open → PEND-021 |
| PEND-007 | OTP | Wrong OTP handling — message, maximum attempts, lockout | 22-09-2026 | **Answered 23-09-2026** – validation shown; 3 wrong attempts → 60-minute block (DISC-013) |
| PEND-008 | OTP | Is the Experian consent checkbox mandatory to submit? | 22-09-2026 | **Answered 23-09-2026** – mandatory; Submit enabled only with consent + 6 digits (DISC-013) |
| PEND-009 | OTP | What does the "Edit" link do? | 22-09-2026 | **Answered 23-09-2026** – returns to screen 02 with the entered mobile number prefilled (DISC-013) |
| PEND-010 | OTP | Next screen after successful OTP submission | 22-09-2026 | **Answered 23-09-2026** – `04) Enter PAN Details`, after the Experian call is triggered (DISC-013) |
| PEND-011 | Product | Confirm product parameters observed in screenshots: LTV 75%, ROI 10.50% p.a., tenure 12 months, loan range ₹ 10,000 – ₹ 2,00,00,000, processing fee / stamp duty / lien marking / lien removal charges, interest autopay on the 5th | 22-09-2026 | Open |
| PEND-012 | All | Any dropdown fields in the journey, and their values/source | 22-09-2026 | Open |
| PEND-013 | All | Session timeout, browser back button and page refresh behaviour | 22-09-2026 | Open |
| PEND-014 | Scope | Screenshots for the missing steps (Sl. 15, Photo Verification, Bank Details, Pledging, Sanction Letter/KFS, Agreement & E-Mandate, disbursement) | 22-09-2026 | Open |
| PEND-015 | PRD | Sample file of the user's preferred PRD format | 22-09-2026 | Open |
| PEND-016 | OTP | Prototype currently treats `123456` as the correct OTP — confirm the demo value, or whether a UAT OTP service should be used | 23-09-2026 | Open |
| PEND-017 | OTP | Resend/wrong-attempt counters and blocks are held in browser storage in the prototype — confirm they will be enforced server-side (per mobile number, not per device) | 23-09-2026 | Open |
| PEND-018 | OTP | When do the resend and wrong-attempt counters reset — only on block expiry and successful verification (current behaviour), or also on a new session / number change? | 23-09-2026 | Open |
| PEND-019 | Experian | Failure behaviour if the Experian credit-score call fails or times out; score thresholds and their effect on offers | 23-09-2026 | Open |
| PEND-020 | OTP service | Failure behaviour if OTP send/verify API fails | 23-09-2026 | Open |
| PEND-021 | OTP | OTP validity/expiry period (how long an OTP stays usable) | 23-09-2026 | Open |
| PEND-022 | Module 1 | **Conflict to resolve:** the shared sample PRD lists the mobile-number validations as `*Required`, `*Invalid mobile number` and `Error: Invalid phone number`, while the messages confirmed verbally on 22-09-2026 and built in the prototype are longer and more explicit. Confirm which wording is approved (tracked as P-01 in the PRD) | 23-09-2026 | Open |
| PEND-023 | All | In the live LOS journey, where should the header Shriram Credit logo go (shriramcredit.in, the LAMF landing page, or nowhere)? The prototype sends it to its own review home page (DISC-016) | 24-09-2026 | Open |
| PEND-024 | Experian | What exactly the Experian call returns (INT-001 Expected Output): only the credit score, or the score plus the full credit report (existing loans, EMIs, missed payments, recent enquiries)? How is "No record found" (new-to-credit customer) handled? Depends on the Experian service contracted (PRD P-09) | 24-09-2026 | Open |
| PEND-025 | OTP service | Which vendor provides the OTP send/verify service (INT-002)? Verify-failure behaviour is tracked with PEND-020 (PRD P-10) | 24-09-2026 | Open |

---

## 9. Implementation Notes

| ID | Note | Date |
| --- | --- | --- |
| IMP-001 | 37 screens created as individual HTML files named after the shared screenshots, numbered for sort order; `index.html` lists all screens | 22-09-2026 |
| IMP-002 | Shared `assets/lamf.css` (design tokens: primary yellow `#FFCB08`, status colours, borders) and `assets/lamf.js` (header, stepper, fund cards, modals, screen templates) so a change applies to every screen | 22-09-2026 |
| IMP-003 | Images (Shriram logo, hero photo, 13 fund icons, MF Central, DigiLocker, DIGIO, coins, success illustration) cropped from the shared screenshots | 22-09-2026 |
| IMP-004 | Font: Satoshi (closest match to the UAT screenshots), loaded from Fontshare; falls back to a system font when offline | 22-09-2026 |
| IMP-005 | Browser chrome (tabs, address bar, macOS dock) visible in some screenshots is not reproduced; only the page is built. The browser location-permission prompt on 13.1/13.4 is a simulated look-alike | 22-09-2026 |
| IMP-006 | DIGIO and DigiLocker screens (16.5.1–16.5.6) are look-alike mock-ups for the prototype, not the real third-party pages | 22-09-2026 |
| IMP-007 | Scrolled states (13.1, 13.3, 13.4, 13.6, 16.5.8) are rendered by hiding the content above the fold instead of scrolling on load | 22-09-2026 |
| IMP-008 | A review-only screen navigator (Prev / ☰ list / Next, and ← → keys) is present on every page; to be removed when the journey flow is final | 22-09-2026 |
| IMP-009 | CTA wiring is driven by a single `FLOW` map, and screen logic by a `BEHAVIOUR` map, both in `assets/lamf.js`; every CTA carries a `data-cta` name | 22-09-2026 |
| IMP-010 | Screen 02 validations implemented and verified in the browser (numeric-only, 10 digits, first digit 6–9, consent gating, T&C/Privacy popups, close → landing, Continue → screen 03) | 22-09-2026 |
| IMP-011 | Mock data across screens is taken from the screenshots (13 funds, credit limit ₹ 6,19,13,200, portfolio ₹ 12,04,62,749.99, mobile 9597001623, PAN CBOPA 8195 B, email azhagarsamy.s@shriramcredit.in) | 22-09-2026 |
| IMP-014 | Screen 03 implemented end to end and verified in the browser: masked number from the entered mobile (`+9194XXXX8374`), numeric-only 6 boxes with paste support, consent + 6 digits gating Submit, wrong-OTP messages with remaining attempts, 3 wrong → 60-min block, 3 resends → 15-min block, block persisting across refresh with dynamic remaining minutes, auto-unlock and counter reset when the block expires, Edit returning to screen 02 prefilled, correct OTP landing on screen 04 | 23-09-2026 |
| IMP-018 | Local git repository initialised in `LOCAL/` (branch `main`, 93 files, first commit). GitHub CLI (`gh`) is not installed and needs Homebrew + the user's password, so GitHub/Pages hosting is pending the user | 23-09-2026 |
| IMP-021 | Cloud copy is reachable from any device signed in to the same Claude account (no shared network, no local server needed); the URL stays the same on every republish, so it can be bookmarked on both laptops. A second account would need access via the page's Share menu | 24-09-2026 |
| IMP-019 | Cloud copy published as a private page: `cloud.html` renders any screen as a hash route using the same templates, with CSS/JS inlined (the artifact viewer's content security policy blocks external stylesheets, and its wrapper nests the document so inline styles must be moved into `<head>` at boot). Fontshare/Satoshi is blocked there, so the cloud copy loads Plus Jakarta Sans from Google Fonts — the local copy still uses Satoshi | 23-09-2026 |
| IMP-020 | Screens 16.5.1–16.5.6 (DigiLocker / Digio look-alikes) show a red "SIMULATED SCREEN" strip when served from anywhere other than localhost, so the hosted copy cannot be mistaken for the real service. Local screenshots for the PRD are unaffected | 23-09-2026 |
| IMP-016 | PRD generated as HTML at `SCCL_LAMF_LOS_PRD.html` in the shared sample's format, with full-screen and element-level screenshots captured from the prototype into `prd-assets/`; linked from the screens index and hosted at `http://localhost:8080/SCCL_LAMF_LOS_PRD.html`. Print styling included so it can be printed/saved as PDF | 23-09-2026 |
| IMP-017 | PRD content lives in `tools/build_prd.py` (MODULES / INTEGRATIONS / PENDING) and is regenerated after each confirmed discussion, alongside this log | 23-09-2026 |
| IMP-015 | OTP rule values are grouped in `OTP_RULES` in `assets/lamf.js` (length 6, timer 30s, 3 resends/15 min, 3 wrong/60 min, demo OTP) so thresholds can be changed in one place | 23-09-2026 |
| IMP-013 | Popup scroll lock implemented in the shared files: `html`/`body` get a `modal-open` class whenever an `.overlay` is present, and `.overlay` scrolls its own content. Verified on 02, 03 and 16.2 (background frozen, popup scrolls when the viewport is short) and on 12 (no popup — page scrolls normally) | 23-09-2026 |
| IMP-012 | This discussion log created and added to the workflow: it is updated before continuing development whenever a requirement, clarification or correction is given | 22-09-2026 |
| IMP-022 | Project pushed to GitHub (`azhagarvicky/SCCL-PRD`, public) and hosted on GitHub Pages. Root `index.html` forwards to `lamf-journey/`; `.nojekyll` makes Pages serve the files as-is. Supersedes the "hosting pending" note in IMP-018 | 24-09-2026 |
| IMP-023 | Dev → Main release process: all changes are committed to `dev`, and every push to `dev` auto-deploys to the development URL (`/dev/`) via GitHub Actions. `dev` is promoted to `main` only on the user's explicit instruction, which triggers the production deployment to the site root. Both workflows publish into the `gh-pages` branch, each replacing only its own part, and confirm the new commit is live before reporting success (`.github/workflows/`) | 24-09-2026 |
| IMP-024 | Home page and screen list are generated by `tools/build_pages.py` from one definition for both the local files (`index.html`, `screens.html`) and the cloud copy (`cloud.html` routes: `#` home, `#SCREENS`, `#PRD`); their styles moved into `assets/lamf.css` (`page-home`, `page-screens`). The logo link is `logoLink()` in `assets/lamf.js`. Checked in the browser: all 30 screens that show the Shriram logo link to `index.html`, the landing-page footer layout is unchanged, and the home page has no sideways scroll at phone width | 24-09-2026 |

---

*End of document — updated continuously as the LAMF LOS discussion progresses.*
