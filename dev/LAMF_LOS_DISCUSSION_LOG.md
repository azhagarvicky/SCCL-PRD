# LAMF LOS – Discussion & Decision Log

## Project Information

**Project:** Loan Against Mutual Funds (LAMF)
**System:** LOS – Customer Online Journey
**Document Type:** Discussion & Decision Log
**Status:** Living Document
**Last Updated:** 29-09-2026 02:05 IST

**Prototype location:** `LOCAL/lamf-journey/` (37 HTML screens + shared `assets/lamf.css`, `assets/lamf.js`)
**Screenshot source:** `SCCL/LAMF/LOS/LOS/` (38 screenshots, UAT: `uatlamf.shriramcredit.in`)
**PRD (HTML):** `LOCAL/lamf-journey/SCCL_LAMF_LOS_PRD.html` → `http://localhost:8080/SCCL_LAMF_LOS_PRD.html` (regenerate with `python3 tools/build_prd.py`)
**Cloud copy (private):** https://claude.ai/artifact/1Jqh9iJ4WDk4SJppaPojYr — single page, hash routed (`cloud.html`)
**Local URL:** `http://localhost:8080` (`python3 -m http.server 8080 --directory lamf-journey`)
**Repository (public):** https://github.com/azhagarvicky/SCCL-PRD — `dev` = development, `main` = production
**Hosted – Production (`main`):** https://azhagarvicky.github.io/SCCL-PRD/
**Hosted – Development (`dev`):** https://azhagarvicky.github.io/SCCL-PRD/dev/
**Apply for New Loan (Existing Customer) – separate prototype:** `lamf-existing-customer/` → https://azhagarvicky.github.io/SCCL-PRD/dev/lamf-existing-customer/ (DISC-030)

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
| DISC-022 | 25-09-2026 | Whole project | Multi-device continuity | The user works from a MacBook, an office laptop and a mobile. Work must continue from wherever it was last left, e.g. an update done on the Mac must be picked up when the next prompt is typed on the office laptop | GitHub `dev` is the single shared copy. `CLAUDE.md` added at the repo root: every Claude session (local or cloud, any device) first syncs to the latest `dev`, reads this log and reports the last update, and pushes every confirmed change to `dev` immediately, so nothing stays on one device only | Implemented |
| DISC-023 | 27-09-2026 | Landing page | Top navigation phone & Contact Us | Change the top-navigation phone number from 033-23349779 to +91 898-100-3538; clicking the number must call it; clicking Contact Us must navigate the user to https://www.shriramcredit.in/contact-us | Phone number replaced and made a call link (`tel:+918981003538`); Contact Us links to the Shriram Credit contact page in the same tab. Other header nav items and footer links stay static (PEND-001) | Implemented |
| DISC-024 | 27-09-2026 | PRD | Sl. No 1 – Data Points Required | Data Points Required for Sl. No 1 to read: Clicked CTA (Check your eligibility in 2 minutes / Start Your Application) and Clicked Timestamp (DD-MMM-YYYY; HH:MM:SS) | PRD Sl. No 1 Data Points Required replaced with the two confirmed data points; the phone number and Contact Us behaviour (DISC-023) added to the Sl. No 1 description as field specs | Implemented |
| DISC-025 | 27-09-2026 | All journey screens | Fixed top navigation | The top navigation (header) must stay fixed at the top; only the page body scrolls. Apply to every page in the journey | Header made sticky in the shared stylesheet, so it applies to all 37 screens (site header on the landing page, app header elsewhere; the stepper keeps sticking below it where present). Popups still open above it | Implemented |
| DISC-026 | 27-09-2026 | Dev & production | Review comments | On the dev link only: select any text and add a comment on what should change; comments are listed as Open / Closed with dates, like Pending / Completed Clarifications. Claude proceeds with the changes asked in the comments. Production must not allow comments | Built as a review tool: select text → 💬 Comment → the comment is saved as a GitHub issue on the project repository (visible on every device and to Claude). A 💬 Comments panel (bottom-left) lists Open and Closed comments with opened/closed dates, for this page or all pages, and highlights the commented text. Only comments opened by the project owner's GitHub account (`azhagarvicky`) are listed or acted on, because the repository is public and anyone could open an issue; Claude confirms the owner's comments before making the changes and closes each issue with a note of what was done. Asked first for the dev site only; changed the same day to be on production as well (CHG-001) | Implemented |
| DISC-027 | 27-09-2026 | Release process | Dev first, production on confirmation | Every patch goes to dev only. Production is updated only when the user says "push to production"; then everything on dev, including all features, is pushed to production unchanged so both sites are identical | Changes are pushed to `dev` only; `dev` → `main` only on the user's instruction, as a straight copy of dev (no dev-only differences). An earlier instruction the same day to release every change to production at once was withdrawn by the user (CHG-002) | Confirmed |
| DISC-028 | 27-09-2026 | Dev & production | Review comments for the team | Purpose: the prototype and PRD will be presented to the team and management; reviewers must be able to click any text, enter a comment and Save / Cancel, or use the bottom-left Comments button for comments not tied to text (this page or all pages), without opening separate notes. The owner then tells Claude which comments to action. Storage: Google Sheet in the owner's Google Drive (Microsoft 365 Excel considered; needs Power Automate Premium) | Comments rebuilt on a Google Sheet (no sign-in or GitHub account needed): select text → Comment → name + comment → Save / Cancel; + New comment for This page / All pages; name remembered per browser; Open / Closed lists with who, when, closed date and what was done; ⬇ Excel downloads all comments (Open, Closed, All sheets). Claude acts only on comments the owner confirms. Replaces the GitHub-issue version of DISC-026 | Implemented – tested end to end (C-0001) |
| DISC-029 | 27-09-2026 | PRD | Sl. No 1 wording & layout | (1) One line space after each field block in the description; (2) Clicked CTA values as bullet points; (3) remove the top-navigation phone number and Contact Us field specs from Sl. No 1; (4) Functionality to mention that the user can click either CTA | Functionality now reads “User clicking the “Check your eligibility in 2 minutes” CTA or the “Start Your Application” CTA in landing page to start the journey”; Clicked CTA shown as bullets; phone / Contact Us specs removed from the PRD (the prototype behaviour from DISC-023 is unchanged); a line space now separates every field block in all PRD descriptions (`.spec` in `prd.css`) | Implemented |
| DISC-030 | 28-09-2026 | Apply for New Loan (Existing Customer) | New feature, kept separate | Build an "apply for new loan" journey for existing customers, step by step from screenshots the user shares; new pages in the same design and UI style; do not merge it with the current (new-customer) journey | Separate prototype in `lamf-existing-customer/` with its own screens, index, stylesheet, script, images and build script (`lamf-existing-customer/tools/build_pages.py`). Nothing in `lamf-journey/` is changed; its browser storage uses its own `lamfec.` keys so the two journeys never share entered data. Hosted with the rest of the repo at `/dev/lamf-existing-customer/` | Implemented |
| DISC-031 | 28-09-2026 | Apply for New Loan – 01, 02, 03 | First three screens | Recreate the landing page, the MF linked mobile number entry page and the OTP page first | Screens 01 Landing, 02 Enter MF linked Mobile Number and 03 Enter OTP recreated with the same content, validations and OTP rules as the current journey (DISC-005 to DISC-010, DISC-013). OTP Submit does not open a next page yet: after a correct OTP a note says the next screen will be added when its screenshot is shared (PEND-027) | Implemented |
| DISC-032 | 28-09-2026 | Apply for New Loan – 03 OTP | Demo OTP and tag | The OTP vendor is not integrated yet, so the user may enter only OTP 000000; show a tag "Please use OTP 000000 to proceed". Once the vendor is integrated the real OTP is sent and entered | Existing-customer journey only: accepted OTP changed from 123456 to 000000 (`OTP_RULES.demoOtp`); any other OTP is treated as wrong (wrong-attempt count and 60-minute block unchanged). Tag "Please use OTP 000000 to proceed" shown under the OTP boxes; its value comes from `OTP_RULES.demoOtp`. Remove the tag and the fixed OTP when the vendor is integrated (PEND-025). The new-customer journey still uses 123456 | Implemented |
| DISC-033 | 28-09-2026 | Apply for New Loan – 04 Your loans | Landing page after OTP | After OTP verification the existing customer lands on the "Your loans" page (screenshot shared); the header "My Portfolio" CTA is replaced by an "Apply for New Loan" CTA | Screen `04) Your Loans Page` built from the screenshot: Your loans, Loan Against Mutual Fund with Active badge, Available Withdrawal Balance with Repay / Withdraw, six amount cards, tabs (Statements, Transaction Details, Pledged Mutual Funds Details, Loan Details, Repayment Schedule) and the Holding / Client Statement PDF cards. Header shows "Apply for New Loan" (yellow, same place and style as My Portfolio) + dashboard and profile icons. Correct OTP (000000) now opens this page. Repay, Withdraw, the other tabs and the download icons do nothing yet (PEND-031). Answers PEND-027 | Implemented |
| DISC-034 | 28-09-2026 | Apply for New Loan – 04.1 / 04.2 PAN type popup | Apply for New Loan popup | Clicking "Apply for New Loan" opens a popup with a close (X) icon, two radio buttons (Existing PAN, New PAN), none selected by default, and a Continue CTA. Close closes the popup. Continue checks that one radio is selected, else shows "Please select PAN type". Selecting Existing PAN shows the MF Central consent ("I authorize Shriram Credit to fetch my mutual fund portfolio holdings from MF Central to assess my eligibility and credit limit for a Loan Against Mutual Funds."), only for Existing PAN; Continue is enabled only after the consent is ticked; then the user moves to the next page | Built as stated. Continue is grey until it can proceed (New PAN selected, or Existing PAN + consent ticked) but still responds to a click with the reason, like the mobile number popup (DISC-008/010): nothing selected → "Please select PAN type."; Existing PAN without consent → "Please provide the consent to proceed.". The consent row is hidden for New PAN and is cleared when the user switches away from Existing PAN. Close → back to Your loans. Next pages for Existing PAN and New PAN not built yet: a note is shown (PEND-029, PEND-030). Popup heading "Apply for New Loan" and the line "Select the PAN you want to apply the new loan with" are Claude's wording (PEND-032) | Implemented |
| DISC-035 | 28-09-2026 | Apply for New Loan – 04.1 / 04.2 PAN type popup | Existing PAN dropdown | When Existing PAN is selected, show a dropdown listing the PANs already held with the same mobile number (a customer can add at most 3 PANs), each masked as CB*P*****B | Dropdown "Select PAN" appears under the radios only for Existing PAN (with the consent), nothing pre-selected. Mask keeps characters 1, 2, 4 and 10 (CBOPA8195B → CB*P*****B). Demo data: two PANs for the mobile number (CBOPA8195B, AKLPS4321K); the list is capped at 3. Continue order of checks: PAN type → "Please select PAN." → consent; Continue is yellow only when a PAN is chosen and the consent is ticked. Switching to New PAN hides and clears both. The chosen PAN is kept for the MF Central step | Implemented |
| DISC-036 | 28-09-2026 | Apply for New Loan – 05 to 09 | MF Central fetch for Existing PAN | After Existing PAN + Continue: LOS → MF Central redirection popup with a 3, 2, 1 timer, then automatically the MF Central mock page; close (X) on the popup closes it and shows the previous page. Mock page needs a tag "Please use OTP 000000"; after the OTP and Submit: MF Central → LOS Redirecting page → after 1 second Fetching Mutual Fund Portfolio → after 1 second Analysing Mutual Fund Portfolio → after 1 second the next page (to be given). Reference: screens 06–10 of the new-customer journey | Built as screens `05) LOS to MF Central Redirection loading page` (popup over Your loans, "Redirecting to MF Central in 3 / 2 / 1 seconds", close → Your loans and the countdown stops), `06) MF Central Mock Page` (6 OTP boxes, numbers only, tag "Please use OTP 000000 to proceed", Submit yellow when 6 digits entered, only 000000 accepted), `07) MF Central to LOS Redirecting Page`, `08) … Fetching …` and `09) … Analysing …` (loaders over Your loans), each moving on after 1 second. After 09 a note is shown until the next page is shared (PEND-033). Same content and design as the new-customer journey's 06–10 | Implemented |
| DISC-037 | 28-09-2026 | Apply for New Loan – 04.1 / 04.2 PAN type popup | Radio layout | Existing PAN and New PAN radios to sit left and right instead of one below the other | The two radio boxes now sit side by side in two equal columns (Existing PAN left, New PAN right); the PAN dropdown and consent stay below, full width. Only on very narrow phones (≤ 360px) they stack again so the labels fit | Implemented |
| DISC-038 | 28-09-2026 | Apply for New Loan – 10, 11 | Generating loader and Curated offers | After "Analyzing your mutual fund portfolio.." wait 1 second, show the "Generating best loan offers for you" loader (screenshot shared), then open the Curated Offers page automatically (reference: new-customer journey screen 12) | Built as `10) MF Central to LOS Generating Loan Page` (skeleton loader "Generating best loan offers for you / This might take a min, thanks for your patience" over the curated offers page) and `11) Curated Offers Page` (same content and data as the new-customer journey: credit limit ₹ 6,19,13,200, 10.50% p.a., fee ₹ 3,09,566, 12 months, Start Application, total portfolio, Refresh portfolio, 13 fund cards). Chain is now Redirecting → Fetching → Analysing → Generating → Curated offers, 1 second each. The Analysing loader now shows over the curated offers page, as in the reference screen 10 (was over Your loans). Start Application, the credit-limit link and Refresh portfolio do nothing yet (PEND-036). Answers PEND-033 | Implemented |
| DISC-039 | 28-09-2026 | Apply for New Loan – 04.1 / 04.2 / 04.3 | Apply for New Loan as a page (replaces the popup of DISC-034, DISC-035, DISC-037) | Clicking "Apply for New Loan" must open a page like the Shriram Finance FD existing-customer page (screenshot shared) instead of a popup. Existing PAN / New PAN as CTAs (toggle buttons). Existing PAN: PAN dropdown as before; after a PAN is selected the page expands and lists the details already held for that PAN (fields to be given by the user). New PAN: PAN verification fields below, same fields and design as the new-customer journey's `04) Enter PAN Details`. After a PAN is selected / verified, the MF Central consent shows below with a Continue CTA; Continue → MF Central redirection (3, 2, 1) and the rest of the flow as built | Built as `04.1) Apply for New Loan Page`: grey title strip "Apply for a new Loan Against Mutual Fund", welcome box (masked mobile), intro text, "Borrower PAN details" section with two toggle CTAs **Use Existing PAN** / **Apply with New PAN** (nothing selected at first). Use Existing PAN → "Select the PAN to fetch the borrower details" dropdown (masked, max 3) → "Existing details of this PAN" panel (shows the masked PAN; other fields to be confirmed, PEND-037). Apply with New PAN → PAN Details form (Mobile Number read-only, Name as per PAN, DOB, PAN Number) with a **Verify PAN** CTA; on success the fields lock and "PAN verified successfully" shows. MF Central consent + Continue appear only once a PAN is selected (Existing) or verified (New); Continue is yellow only when the consent is ticked, and a click without it shows "Please provide the consent to proceed.". Switching between the two CTAs hides the other part and clears the consent. Close (X) on the MF Central popup now returns to this page, and the popup / Fetching loader show over this page. Review copies: `04.2` (Existing PAN selected), `04.3` (New PAN verified with sample values). CTA labels, headings and texts adapted from the FD page by Claude (PEND-038) | Implemented |
| DISC-040 | 28-09-2026 | Apply for New Loan – 04.1 / 04.2 Existing PAN | Existing details of this PAN | Show PAN Number, DOB and Name as per PAN in the “Existing details of this PAN” section, unmasked and not editable | The panel now shows three read-only fields in the same style as the PAN Details form: PAN Number (unmasked, e.g. CBOPA8195B) and DOB side by side, Name as per PAN below. They fill in as soon as a PAN is picked and change when another PAN is picked; they cannot be typed into. The dropdown itself still shows masked PANs. Demo data: CBOPA8195B – RAVI KUMAR S – 14/05/1988; AKLPS4321K – PRIYA R – 02/11/1992 (`PAN_DETAILS` in `lamf.js`). Answers PEND-037 | Implemented |
| DISC-041 | 28-09-2026 | Apply for New Loan – 11 → 12 | Start Application → Mutual Fund Selection | Clicking “Start Application” on the Curated Offers page opens the Mutual Fund Selection page (reference: new-customer journey `13.2) Mutual Fund Selection Page`) | Built as `12) Mutual Fund Selection Page`, same content and data as the reference: header, 4-step stepper (Selection of Mutual Fund active), Back, Loan Amount ₹ 2,00,00,000 with slider, Funds selected for pledging (market value ₹ 2,66,66,667.21, 3 funds), Select All, 9 eligible fund cards (ICICI, Axis, Kotak selected), “Continue to apply ₹ 2,00,00,000” bar. Back → Curated Offers. Like the reference, the page is static (fund ticks, amounts, slider and loan-amount edit do not react yet); “Continue to apply” shows a note until the next screen is shared (PEND-040). Answers the Start Application part of PEND-036 | Implemented |
| DISC-042 | 28-09-2026 | Apply for New Loan – 12 MF Selection | Change the loan amount on the same page | On the Mutual Fund Selection page the user can change the loan amount, as in the new-customer journey's `13.5` (loan amount edit) and `13.6` (fund-wise amount edit) | Screen 12 is now interactive (the new-customer journey's pages are static pictures of these states). **Loan amount:** pencil → edit box with Update (digits only; Enter also updates); allowed ₹ 10,000 – ₹ 2,00,00,000, else “Loan amount must be between ₹ 10,000 and ₹ 2,00,00,000.”; the new amount is spread over the funds in list order, each filled up to its Max Limit (e.g. ₹ 95,30,700 → ICICI only, as in 13.5). **Slider:** click or drag sets the amount the same way (steps of ₹ 1,000). **Fund-wise:** pencil on a fund → amount box with ✓; more than the fund's Max Limit → “Amount cannot be more than the Max Limit of ₹ …”; total above ₹ 2 crore → “Total loan amount cannot be more than ₹ 2,00,00,000.”; 0 removes the fund. **Tick / untick** a fund: tick adds it at its Max Limit within the ₹ 2 crore cap; untick removes it. **Select All** fills funds in list order up to ₹ 2 crore, or clears all when already at ₹ 2 crore. Loan amount, slider, market value of units selected (amount ÷ 75% LTV), number of funds and the “Continue to apply ₹ …” amount update at once. Continue is grey while an edit box is open or below ₹ 10,000 (“Minimum loan amount is ₹ 10,000. Please select funds or increase the amount.”). Review copies `12.1` (loan edit open, ₹ 95,30,700) and `12.2` (ICICI fund edit open, ₹ 1,00,000). Rules and messages are Claude's (PEND-041) | Implemented |
| DISC-043 | 28-09-2026 | Apply for New Loan – 12 → 13 | Continue to apply → Loan Application Summary | After “Continue to apply” on the Mutual Fund Selection page, show the Loan Application Summary (reference: new-customer journey `14) Loan Application Summary`) | Built as `13) Loan Application Summary`, same layout and texts as the reference (Application details, Tenure 12 months, Disbursement Type Multiple, Repayment Type Interest Only, Interest Rate 10.5% p.a, Monthly Interest, Charges incl. GST, Interest autopay 5th of every month, Continue). The figures follow the loan amount chosen on screen 12, using formulas that reproduce the reference exactly for ₹ 1,55,36,100: Pledge Value = amount ÷ 75%, Monthly Interest = amount × 10.5% ÷ 12 (₹ 1,35,940.88), Processing fee = 0.5% of amount rounded + 18% GST (₹ 91,664); stamp duty ₹ 236, lien marking ₹ 531, lien removal ₹ 118 fixed. Opened directly it shows the reference ₹ 1,55,36,100. Back → screen 12 with the same selection kept. Continue shows a note until the next screen is shared (PEND-042). Answers the next-screen part of PEND-040 | Implemented |
| DISC-044 | 28-09-2026 | Apply for New Loan – 13 → 14 | Summary Continue → KYC Verification | After Continue on the Loan Application Summary, show the KYC Verification page (reference: new-customer journey `16.1) KYC Verification Page`) | Built as `14) KYC Verification Page`, same layout and texts as the reference: stepper at step 2 (Selection of Mutual Fund done), Back, “Your loan amount is ₹ … View details”, KYC Verification with 1 Email Verification (open: email box, note, Verify), 2 PAN Verification (Complete), 3 Aadhaar Verification with DigiLocker (Pending), 4 Photo Verification (Pending), 5 Bank Details (Pending). The loan amount shown is the one chosen on screen 12 (₹ 1,55,36,100 when opened directly). Back → Summary. Verify and View details show a note until those screens are shared (PEND-043). Answers the next-screen part of PEND-042 | Implemented |
| DISC-045 | 28-09-2026 | Apply for New Loan – 14 KYC (Existing PAN) | Email already verified | In the Existing PAN flow the email is not asked again: the KYC page must show Email Verification as completed (reference: new-customer journey `16.4) KYC Verification Page email verification completed`) | Screen 14 now opens like 16.4 when the user came through **Use Existing PAN**: 1 Email Verification – Complete, 2 PAN Verification – Complete, 3 Aadhaar Verification with DigiLocker – open with **Start KYC**, 4 Photo and 5 Bank Details – Pending. Through **Apply with New PAN** it still asks for the email (as 16.1; review copy `14.1) KYC Verification Page New PAN email verification`). The PAN choice is remembered from the Apply for New Loan page (`lamfec.mode`); opened directly, 14 shows the Existing PAN state. Start KYC shows a note until its screen is shared (PEND-044) | Implemented |
| DISC-046 | 28-09-2026 | Apply for New Loan – 04.1 / 04.2 (ETB page) | Personal details section | Show the email ID on the ETB (Apply for New Loan) page in a new “Personal details” section below the PAN section; more personal-detail fields will be added later | New section **Personal details** below “Borrower PAN details”, shown when an existing PAN is selected: Email ID, read-only, in the same style as the existing PAN details. It changes with the selected PAN (demo: CBOPA8195B → ravikumar.s@example.com, AKLPS4321K → priya.r@example.com, in `PAN_DETAILS`). The MF Central consent and Continue now sit below this section. Hidden for Apply with New PAN. Further fields to be given by the user (PEND-045) | Implemented |
| DISC-047 | 28-09-2026 | Apply for New Loan – 14 KYC, 15, 16 | DigiLocker and Photo verification mocks | After Start KYC open a new DigiLocker mock page (like the MF Central mock) with Success and Failure CTAs to check both scenarios; on Success, Aadhaar Verification with DigiLocker is marked complete on the KYC page. Same for Photo Verification | Built `15) DigiLocker Mock Page` (DigiLocker logo, “Mock DigiLocker Page”, Aadhaar verification, Success / Failure) and `16) Photo Verification Mock Page` (same card). Start KYC → 15; **Success** → KYC page with Aadhaar **Complete** and Photo Verification open with **Start** (as 16.5.9 of the new-customer journey); **Failure** → KYC page with “Aadhaar verification failed. Please try again.” under Start KYC, to retry. Photo Start → 16; Success → Photo **Complete**; Failure → “Photo verification failed. Please try again.” under Start. Photo only after Aadhaar is complete; a failed Aadhaar clears the photo result. Progress is kept in `lamfec.kyc` and cleared when a new application starts on the Apply for New Loan page. Review copies: `14.2` (Aadhaar complete, Photo Start), `14.3` (Aadhaar and Photo complete). Bank Details stays Pending (PEND-046). Failure texts are Claude's | Implemented |
| DISC-048 | 28-09-2026 | Apply for New Loan – 14 KYC (Existing PAN) | Bank details already verified; only Aadhaar and Photo asked | For an existing PAN the bank account is already verified and not editable; the KYC page must look like the shared screenshot: Email, PAN, Bank Details complete, only Aadhaar and Photo verification required, bank card “ICICI Bank 0006 IFSC ICIC0002692” with a tick, and a Continue CTA | KYC page (Existing PAN): Email, PAN and **Bank Details – Complete**; Bank Details keeps its number and shows the bank on file as a read-only card (bank logo, bank name + last 4 digits, IFSC, yellow tick) as in the screenshot; Aadhaar and Photo stay the only steps to do (DISC-047). **Continue** added below: grey until Aadhaar and Photo are both Complete (a click before that shows “Please complete Aadhaar and Photo verification to continue.”), then yellow; Continue shows a note until the next screen is shared (PEND-047). The card follows the PAN chosen on the ETB page (CBOPA8195B → ICICI Bank 0006, AKLPS4321K → HDFC Bank 1234). Apply with New PAN is unchanged (Bank Details Pending, no Continue yet) | Implemented |
| DISC-049 | 28-09-2026 | Apply for New Loan – 04.1 / 04.2 (ETB page) | Bank details section | Show the bank details on the ETB page under a “Bank details” section: Account holder name, Account number, IFSC code – fetched from the existing record, not editable | New section **Bank details** below Personal details, shown when an existing PAN is selected (hidden for New PAN): Account holder name, Account number, IFSC code, read-only, changing with the PAN. Demo data: CBOPA8195B – RAVI KUMAR S – 123405670006 – ICIC0002692 (ICICI Bank); AKLPS4321K – PRIYA R – 50100234561234 – HDFC0001234 (HDFC Bank). Account number shown in full (PEND-048) | Implemented |
| DISC-050 | 28-09-2026 | Apply for New Loan – 17 Customer Details | Customer details after KYC | After the KYC / bank step show the customer details page (screenshot shared) in three categories: Personal Details, Other Details, KYC Address. Corrections: (1) remove the Fill Default CTA; (2) remove the Save Details CTAs, keep only Confirm and Continue | Built as `17) Customer Details Page` (KYC Continue → 17, Back → 14), same layout as the screenshot with the three collapsible sections (tick + chevron). Values pre-filled from the existing record of the selected PAN. **Personal Details:** Salutation (dropdown), Name, Date of Birth, Gender (shown as text), Mother's Name, Father's Name (letters, spaces, dots), Marital Status (dropdown). **Other Details:** Loan Purpose, Qualification, Occupation, Nature of Business, Annual Income, Source of Income, Is the applicant financially independent? (dropdowns), declarations “I am not a politically exposed person” and “I am a tax resident of India only”. **KYC Address:** Address Line 1–3, Landmark, Pincode, City (text). No Fill Default, no Save Details; **Confirm and Continue** checks every * field (“Please enter / select …”) and both declarations (“Please confirm both declarations to continue.”), opens the section with the first error; when all is fine a note shows until the next screen is shared (PEND-049). Dropdown option lists are Claude's (PEND-050) | Implemented |
| DISC-051 | 28-09-2026 | Apply for New Loan – 04.1 / 04.2 (ETB page) | All customer details under Personal details | Show all these details on the ETB page under the Personal details section | Personal details section now shows, below Email ID and read-only: sub-headings Personal Details (Salutation, Name, Date of Birth, Gender, Mother's Name, Father's Name, Marital Status), Other Details (Loan Purpose, Qualification, Occupation, Nature of Business, Annual Income, Source of Income, Financially independent, the two declarations as ticked, disabled boxes) and KYC Address (Address Line 1–3, Landmark, Pincode, City). All follow the selected PAN (demo data in `PROFILE`) | Implemented |
| DISC-052 | 28-09-2026 | Apply for New Loan – 04.1 / 04.2 (ETB page), 17 | Three sections and what can be changed | Personal details was repeated inside Personal details; keep three sections only. Personal details: all fields not editable except Salutation and Marital Status (Name, DOB, Gender, Father's Name, Mother's Name not editable). Other details: all editable. KYC Address: not editable | ETB page now has separate sections **Personal details** (Email ID + Salutation, Name, Date of Birth, Gender, Mother's Name, Father's Name, Marital Status), **Other details** (seven dropdowns + the two declarations) and **KYC Address**, then Bank details. Editable: Salutation and Marital Status (dropdowns), every Other details dropdown and both declarations; everything else read-only. Email ID kept read-only because it is already verified (PEND-051). Continue (Existing PAN) now also checks that every editable dropdown has a value (“Please select …”) and both declarations are ticked (“Please confirm both declarations to continue.”), with “Please complete the highlighted details.” above Continue. Changes made here are carried to `17) Customer Details Page`; switching PAN reloads that PAN's record. Screen 17 aligned: Mother's and Father's Name now shown as text (not editable) | Implemented |
| DISC-053 | 28-09-2026 | Apply for New Loan – 04.1 / 04.2 (ETB page) | Section order, layout, Mobile Number | Bank details must come right after the PAN details section; redesign the page to use the empty space; add Mobile Number after Email ID in Personal details | Order is now Borrower PAN details → **Bank details** → Personal details → Other details → KYC Address → consent + Continue. Sections use the full card width with **three fields per row** (two on tablets, one on phones): existing PAN details (PAN Number, DOB, Name as per PAN) in one row, bank details in one row, address in two rows. PAN dropdown limited to 460px and the New PAN form to 560px; consent and Continue centred (460px). Personal details starts with **Email ID** and **Mobile Number** (the verified login number, read-only) | Implemented |
| DISC-054 | 28-09-2026 | Apply for New Loan – 17 Customer Details | Editable fields follow the ETB page | On screen 17 the editable fields must show the same values as the ETB page: first the details fetched from the previous loan, and if the user changed any editable field on the ETB page (e.g. Loan Purpose), that changed value | Confirmed and made robust: every change to an editable field on the ETB page (Salutation, Marital Status, the Other details dropdowns and declarations) is now saved immediately, not only on Continue, and is restored if the user returns to the ETB page (e.g. after closing the MF Central popup). Screen 17 shows the previous-loan record with those changes on top; read-only fields (Name, DOB, Gender, Mother's / Father's Name, KYC Address) always show the record. Checked end to end from the landing page: ETB changes Dr / Single / Medical / Above Rs. 1 Crore / Retired appeared on 17 | Implemented |
| DISC-055 | 29-09-2026 | Apply for New Loan – screen list 14–17 | Screen order follows the journey | The screen list must follow the journey: KYC Verification → DigiLocker Mock → back to KYC Verification with the respective scenarios → Photo Verification Mock → back to KYC Verification with the respective scenarios | Renumbered: `14) KYC Verification Page`, `14.1) … New PAN email verification`, `15) DigiLocker Mock Page`, `15.1) KYC Verification Page Aadhaar verification success`, `15.2) … Aadhaar verification failed`, `16) Photo Verification Mock Page`, `16.1) … Photo verification success` (Continue enabled), `16.2) … Photo verification failed`, `17) Customer Details Page`. The failure states are new review screens; old `14.2` / `14.3` removed. The live journey is unchanged (the mocks still return to 14, which shows the same states) | Implemented |
| DISC-056 | 29-09-2026 | Apply for New Loan – 18 Pledging of Mutual Fund | MF pledging after Customer Details | After Confirm and Continue on Customer Details, the MF pledging (three UAT screenshots shared: review page, OTP popup, “Successfully pledged!”) | Built `18) Pledging of Mutual Fund Page` (stepper step 3; Back; “Please review and confirm the following details”; Loan Amount and Total Pledge Value; MF Central card with Value of Securities and **Pending** badge; View Securities / Pledge Securities; “An OTP will be sent to +91…”), `18.1) … OTP popup` (“Enter OTP to pledge your Mutual Fund”, “OTP has been sent by MF Central to …”, 6 boxes, “Didn't receive OTP? 00:30” countdown then Resend OTP, tag “Please use OTP 000000 to proceed”, Submit OTP, close → 18) and `18.2) … Successfully pledged` (green tick, “Successfully pledged!”, “You will be redirected in 3 / 2 / 1 / 0 seconds.”). Loan amount = amount chosen on 12; pledge value = amount ÷ 75%; mobile masked as in the screenshot. Wrong OTP → “The OTP you entered is incorrect. Please try again.”; empty → “Please enter the 6-digit OTP.”. After the redirect the page shows **Pledged** (badge and button) and a note that Agreement & E-Mandate will be added when shared (PEND-052). View Securities shows a note (PEND-052). Pledge state resets when a new application starts | Implemented |
| DISC-057 | 29-09-2026 | Apply for New Loan – 19 Agreement & E-Mandate | Page after a successful pledge | After “Successfully pledged!” the user lands on the Agreement & E-Mandate page (screenshot shared) | Built `19) Agreement and E-Mandate Page`: stepper step 4 (steps 1–3 done), 1 **Loan Agreement – Pending** with **Sign Agreement**, 2 **E-Mandate – Pending**. The 18.2 countdown now redirects here (was back to 18). Sign Agreement shows a note until its screen is shared (PEND-053). Answers the next-screen part of PEND-052 | Implemented |
| DISC-058 | 29-09-2026 | Apply for New Loan – 20, 21 | Sanction letter and loan agreement e-sign | Sign Agreement redirects to DIGIO (vendor): first the sanction letter is generated (UAT screenshots + sample PDF `sanction_letter_25.pdf`: In principle e-Sanction Letter, KFS; consent “I accept the terms of the Sanction letter and Key Fact Statement (KFS)…” and Submit, enabled once ticked); after Submit it automatically redirects to the loan agreement sign page (Digio e-sign: LOAN CUM PLEDGE AGREEMENT, consents, Sign Now) | Built `20) Sanction Letter Page`: letter as in the PDF (logo, title, date = today, customer name and KYC address, Customer ID, “Reg: Your request for Financial Assistance of ₹ …”, sanction text with the loan purpose, sign-off, company footer) and Annexure A – KFS Part 1 key rows (type of loan, proposal / customer ID, sanctioned amount, 12 months, instalments with monthly interest due = amount × 10.5% ÷ 12, 10.5% fixed, processing fee 0.5% + GST, renewal / swap / lien / stamp duty charges, purpose). Fixed bottom bar with the consent checkbox and Submit (grey until ticked, then blue). Submit → `21) Loan Agreement e-Sign Page`: Digio-style page labelled “Mock e-Sign page (prototype)”, agreement opening clauses with the loan amount in figures and words, the two eSign consents (with the customer's mobile), Sign Now. Sign Now → back to 19 with **Loan Agreement – Complete** and **E-Mandate** now current with **Set up E-Mandate** (note until its screen is shared, PEND-054). Name, address and purpose follow the selected PAN and ETB edits; amount follows screen 12. Demo IDs A000000011 / SCCLMF20260900155 taken from the sample. Review copy `19.1` (Loan Agreement signed). The real Digio page is not copied (no Digio logo image; text wordmark + mock label) | Implemented |

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
| +91 898-100-3538 (top navigation) | Calls the number (`tel:` link) — DISC-023 | Phone dialler |
| Contact Us (top navigation) | Opens the Shriram Credit contact page — DISC-023 | https://www.shriramcredit.in/contact-us |

**Data Points Captured (PRD Sl. No 1, DISC-024)**

* Clicked CTA: Check your eligibility in 2 minutes / Start Your Application
* Clicked Timestamp: DD-MMM-YYYY; HH:MM:SS

**Observed (from screenshot, not confirmed as requirement)**

* Hero claims: interest rate starting at 10.5% p.a.*, 100% paperless, instant loan approval, interest-only repayment and EMI options, RBI regulated NBFC with 25+ years of legacy.
* Header nav items and footer link groups are static marketing links.

**Pending Clarifications**

* PEND-001 – Behaviour of the remaining header nav items and footer links (phone number and Contact Us answered in DISC-023).

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
| CV-014 | The top navigation (header) is fixed at the top of the page; only the body scrolls | All screens with a header | Confirmed (DISC-025) |
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
| CHG-001 | 27-09-2026 | Review comments | Comments tool on the dev site only; production without it (DISC-026) | Comments tool on dev and production alike | User: dev and production should not differ; production is to be an exact copy of dev | Implemented |
| CHG-002 | 27-09-2026 | Release process | Every change released to dev and production together (DISC-027, first version) | Patches to dev only; production updated only on the user's "push to production", as an exact copy of dev | User corrected the earlier instruction the same day | Confirmed |

---

## 8. Pending Clarifications

| Pending ID | Module | Question / Clarification Required | Raised On | Status |
| --- | --- | --- | --- | --- |
| PEND-001 | Landing page | Should header/footer navigation links do anything in the prototype? | 22-09-2026 | **Partly answered 27-09-2026** – phone number and Contact Us defined (DISC-023); About Us, Product & Services, Investors, Learning Lounge, Careers and footer links still open |
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
| PEND-026 | Review comments | Sheet created by Claude and moved into the owner's folder. Owner to deploy the Apps Script web app (tools/comments-apps-script.gs) from the sheet and give Claude the web-app URL | 27-09-2026 | **Answered 27-09-2026** – web app deployed and connected |
| PEND-027 | Apply for New Loan (Existing Customer) | Which screen follows a correct OTP for an existing customer? Screenshot awaited | 28-09-2026 | **Answered 28-09-2026** – `04) Your Loans Page` (DISC-033) |
| PEND-028 | Apply for New Loan (Existing Customer) | Should screens 01–03 of the existing-customer journey differ from the new-customer journey in any way (landing page text, headings, entry point such as a customer login/portal, check that the mobile number belongs to an existing customer)? Currently identical | 28-09-2026 | Open |
| PEND-029 | Apply for New Loan – PAN type popup | Next page after Existing PAN + consent + Continue (screenshot awaited) | 28-09-2026 | **Answered 28-09-2026** – MF Central redirection popup, then MF Central mock and the fetch / analyse loaders (DISC-036) |
| PEND-030 | Apply for New Loan – PAN type popup | Next page / flow after New PAN + Continue; is any consent or PAN entry needed for New PAN? | 28-09-2026 | Open |
| PEND-031 | Apply for New Loan – Your loans | Behaviour of Repay, Withdraw, the dashboard and profile icons, the other four tabs and the statement download icons; should Existing PAN show the customer's masked PAN? | 28-09-2026 | Open |
| PEND-032 | Apply for New Loan – PAN type popup | Confirm the popup heading "Apply for New Loan" and the line "Select the PAN you want to apply the new loan with" (not in any screenshot) | 28-09-2026 | **Taken as confirmed 28-09-2026** – the user shared a screenshot of the popup with this wording when giving the next requirement (DISC-035); correct if not |
| PEND-033 | Apply for New Loan – MF Central flow | Page after "Analysing your mutual fund portfolio" (screenshot awaited). A note is shown after 1 second until then | 28-09-2026 | **Answered 28-09-2026** – Generating loader, then Curated offers (DISC-038) |
| PEND-034 | Apply for New Loan – PAN dropdown | With only one PAN linked, should the dropdown still be shown (currently yes, not pre-selected; still applies on the new page, DISC-039)? Wording of the error "Please select PAN." and label "Select PAN" to be confirmed | 28-09-2026 | Open |
| PEND-035 | Apply for New Loan – MF Central mock | Wrong OTP on the MF Central mock: any attempt limit or block? Currently shows "The OTP you entered is incorrect. Please try again." with no limit (the real MF Central page applies its own rules) | 28-09-2026 | Open |
| PEND-036 | Apply for New Loan – Curated offers | Behaviour of Start Application, the credit limit (How is it calculated) and Refresh portfolio on the existing-customer Curated offers page; same as the new-customer journey or different? | 28-09-2026 | Open |
| PEND-037 | Apply for New Loan – Existing PAN | Which existing details to list after a PAN is selected (e.g. name, DOB, address, bank account, existing loan)? Only the masked PAN is shown now | 28-09-2026 | **Answered 28-09-2026** – PAN Number, DOB, Name as per PAN, unmasked and read-only (DISC-040) |
| PEND-038 | Apply for New Loan – page | Confirm wording: page title "Apply for a new Loan Against Mutual Fund", "Welcome back! Apply for a new loan below.", intro text, section "Borrower PAN details", CTAs "Use Existing PAN" / "Apply with New PAN", "Existing details of this PAN", "Verify PAN", "PAN verified successfully". Welcome box shows the masked mobile number (no name / reference number yet) | 28-09-2026 | Open |
| PEND-039 | Apply for New Loan – New PAN verification | Prototype rules to confirm: Name letters / spaces / dots only; DOB DD/MM/YYYY, real date, age 18+; PAN format ABCDE1234F (typed in capitals, spaces not allowed); a PAN already linked to the mobile number is refused ("…Please choose Use Existing PAN."); a 4th PAN is refused (max 3). Any valid new PAN verifies successfully (no PAN service called). Real service: which vendor, failure / name-mismatch behaviour, attempt limits? | 28-09-2026 | Open |
| PEND-040 | Apply for New Loan – MF Selection | Next screen after “Continue to apply”, and whether fund selection / loan amount / slider should work in this prototype (static in both journeys today) | 28-09-2026 | **Answered 28-09-2026** – loan amount and fund amounts work (DISC-042); Continue → Loan Application Summary (DISC-043) |
| PEND-041 | Apply for New Loan – MF Selection | Confirm the selection rules built in DISC-042: min ₹ 10,000 / max ₹ 2,00,00,000; spreading a loan amount over funds in list order up to each Max Limit (or another order, e.g. by LTV or value?); tick adds a fund at its Max Limit; Select All behaviour; slider step ₹ 1,000; market value = amount ÷ 75% (reference shows ₹ 2,66,66,667.21 from unit prices, prototype ₹ 2,66,66,666.67); any minimum amount per fund; the error wording | 28-09-2026 | Open |
| PEND-042 | Apply for New Loan – Summary | ~~Next screen after Continue on the Loan Application Summary~~ (answered: KYC Verification, DISC-044); confirm the summary formulas (pledge value ÷ 75%, monthly interest, processing fee 0.5% + GST) and whether tenure / fixed charges differ for an existing customer | 28-09-2026 | Open |
| PEND-043 | Apply for New Loan – KYC | For an existing customer: which KYC steps can be skipped or pre-completed (email, Aadhaar, photo, bank details already on file for the existing PAN)? (Email answered 28-09-2026: complete for Existing PAN, DISC-045; rest in PEND-044) Next screens for Verify (email OTP) and View details (loan details popup) | 28-09-2026 | Open |
| PEND-044 | Apply for New Loan – KYC | (Prototype answered 28-09-2026: DigiLocker / Photo mocks with Success / Failure, DISC-047.) Real flow: existing PAN after Start KYC – same screens as the new-customer journey (16.5.x) or skipped when Aadhaar is already on file? Photo and Bank details for an existing PAN: pre-filled or asked again? | 28-09-2026 | Open |
| PEND-045 | Apply for New Loan – Personal details | (Answered 28-09-2026: all customer-details fields added read-only, DISC-051.) Remaining fields for the Personal details section (e.g. address, father's / spouse's name, marital status, occupation, income) – read-only or editable? Should Personal details also appear for Apply with New PAN? | 28-09-2026 | Open |
| PEND-046 | Apply for New Loan – KYC | (Bank Details for existing PAN answered 28-09-2026: complete, bank on file shown read-only, DISC-048; next screen → PEND-047.) Remaining: failure wording for Aadhaar / Photo, any retry limit | 28-09-2026 | Open |
| PEND-047 | Apply for New Loan – KYC | Screen after Continue on the KYC page (Pledging of Mutual Fund?) | 28-09-2026 | Open |
| PEND-048 | Apply for New Loan – ETB Bank details | Account number on the ETB page: full (current) or masked (e.g. XXXXXXXX0006)? New PAN flow: how are bank details captured / verified? | 28-09-2026 | Open |
| PEND-049 | Apply for New Loan – Customer Details | Screen after Confirm and Continue (Pledging of Mutual Fund?) | 28-09-2026 | **Answered 29-09-2026** – MF pledging (DISC-056) |
| PEND-050 | Apply for New Loan – Customer Details | Confirm dropdown values (Salutation, Marital Status, Loan Purpose, Qualification, Occupation, Nature of Business, Annual Income, Source of Income, Financially independent), which fields the existing customer may change on screen 17 (all * fields editable now; Name / DOB / Gender / KYC address read-only), and the error wording | 28-09-2026 | Open |
| PEND-051 | Apply for New Loan – ETB Personal details | Should Email ID be editable on the ETB page (currently read-only because it is already verified; a change would need re-verification)? Should screen 17 still allow changes now that the ETB page does, or become a read-only confirmation? | 28-09-2026 | Open |
| PEND-052 | Apply for New Loan – Pledging | ~~Screen after the pledge redirect~~ (answered: Agreement & E-Mandate, DISC-057); View Securities content (list of selected funds / units?); wrong-OTP limit and resend limit for the pledge OTP (MF Central rules?) | 29-09-2026 | Open |
| PEND-053 | Apply for New Loan – Agreement & E-Mandate | (Sign Agreement answered 29-09-2026: sanction letter → e-sign, DISC-058; E-Mandate → PEND-054.) Screens for Sign Agreement (e-sign / Aadhaar OTP?) and E-Mandate setup; should mocks with Success / Failure be used here as for KYC? | 29-09-2026 | Open |
| PEND-054 | Apply for New Loan – E-Mandate / e-sign | E-Mandate screens (NACH / UPI mandate, bank on file?); should the e-sign include the Aadhaar OTP step and a failure scenario (mock with Success / Failure)? APR and the full KFS (Part 2, Annexure B / C) in the sanction letter – needed in the prototype? | 29-09-2026 | Open |

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
| IMP-025 | After the first production release (25-09-2026) the home page showed unstyled in a browser that had visited earlier: GitHub Pages lets browsers keep files for 10 minutes, so the new page loaded the old cached `lamf.css`. Fix: the publish workflow now tags every local CSS/JS link in the published HTML with the release commit (`assets/lamf.css?v=<commit>`), so each release always loads its own stylesheet and scripts. Source files are unchanged; production and dev are tagged separately | 25-09-2026 |
| IMP-026 | `CLAUDE.md` (repo root) holds the session start and hand-off rules for all devices. Cause found: a cloud session opened from the office laptop started from an older commit (24-09-2026 15:57) and missed the Mac's work up to 25-09-2026 00:54 that was already on `dev`; the new rules make every session start from the latest `dev` | 25-09-2026 |
| IMP-027 | Header change is in `header('site')` in `assets/lamf.js`, so it applies to every screen that uses the site header. Checked in the browser: number shows as +91 898-100-3538 with `tel:+918981003538`, and Contact Us navigates to shriramcredit.in/contact-us. **Pending:** PRD screenshot `prd-assets/screen-01.png` still shows the old number — it must be recaptured on the Mac (the cloud session cannot load the Satoshi font, so a capture there would not match the other PRD images) | 27-09-2026 |
| IMP-028 | Review comments: `lamf-journey/assets/review.js` (loaded by every journey page, the home page, the screen list and the PRD). Comments are GitHub issues titled `[Dev comment] <page> — …`; the page, selected text and comment are in the issue body. The panel reads them from the public GitHub API (cached 1 minute; ↻ reloads). Posting opens GitHub's new-issue page pre-filled, where the user presses Create (no password or token is stored on the site). It runs on dev, production and localhost (not in the single-page cloud copy); each comment records which site it came from. Checked in the browser: select → Comment → pre-filled GitHub link; Open/Closed lists with dates; "What was done" shows Claude's closing note; highlight on the commented text | 27-09-2026 |
| IMP-029 | Comments storage: Google Sheet "LAMF Review Comments" (sheet `Comments`: ID, Created on, Site, Page, Selected text, Comment, Name, Status, Closed on, What was done, Page link) with the Apps Script web app in `tools/comments-apps-script.gs` (POST adds a row with the next ID C-0001…, GET returns all rows; text is stored as plain text, long input is cut, a hidden spam-trap field is ignored). Open/Closed status lives in `comment-status.json` (repo root, maintained by Claude) and the script copies it into the sheet at most once a minute. The site's web-app URL is `ENDPOINT` at the top of `assets/review.js`. Checked in the browser against a simulated web app: save, cancel, name remembered, highlight, Open/Closed lists, Excel download. Sheet: "LAMF Review Comments", ID `1_UB4CDDxL25Zmam53AjmVIeZal3xE6A33OjXHlHomu8` (https://docs.google.com/spreadsheets/d/1_UB4CDDxL25Zmam53AjmVIeZal3xE6A33OjXHlHomu8/edit), owned by azhagar154@gmail.com, in the owner's Drive folder `1gS6yHm0kluXTEtcZk8mPsddu0UjiSBWE`. Web-app URL (deployed by the owner 27-09-2026): `https://script.google.com/macros/s/AKfycbyFISY4pW-qc3pRvRjq8pHpDLH25lcVsGQ8RV1n-6IyXxwRq3ZuP-t4J_oXfB4lxAC6tw/exec` | 27-09-2026 |
| IMP-030 | Production release 27-09-2026 14:40 IST on the user's "push to production": `main` fast-forwarded to `dev`, so production now has the new header phone number and Contact Us link (DISC-023), PRD Sl. No 1 data points (DISC-024), the fixed top navigation (DISC-025) and the review comments tool connected to the Google Sheet (DISC-028). Production and dev are identical | 27-09-2026 |
| IMP-031 | Apply for New Loan (Existing Customer) prototype in `lamf-existing-customer/`: own `assets/lamf.js` (screens 01–03 only, `FLOW` / `BEHAVIOUR` / `OTP_RULES`, storage keys `lamfec.*`), own copy of `assets/lamf.css` (plus an `.ec-toast` note style) and of the two images it needs, and `tools/build_pages.py` that writes the numbered screens and `index.html`. Source files: `assets/lamf.js`, `assets/lamf.css`, `tools/build_pages.py`; the screen `.html` files and `index.html` are generated. Review comments tool, PRD and cloud copy are not added to this folder yet | 28-09-2026 |
| IMP-032 | Existing-customer screens 04, 04.1, 04.2 added to `lamf-existing-customer/` (`T.loans`, `T.panTypeModal`, `panTypeBehaviour` in `assets/lamf.js`; `.yl-*`, `.m-pantype`, `.radio` styles in `assets/lamf.css`). Loan figures are held in `LOAN` in `lamf.js`. 04.2 is the same popup with Existing PAN pre-selected, for review. Checked in the browser: OTP 000000 → 04; Apply for New Loan → popup; all error messages, consent show/hide, Continue enabled states, close → 04; no sideways scroll at 390px wide | 28-09-2026 |
| IMP-033 | Existing-customer screens 05–09 added (`T.mfcModal`, `T.mfMock`, `T.redirecting`, `T.loader` and their `BEHAVIOUR` entries in `lamf-existing-customer/assets/lamf.js`; MF Central logo copied into this folder's `assets/img/`). PANs are held in `CUSTOMER.pans` (cap `MAX_PANS` = 3) and masked by `maskPan`; the chosen PAN is stored as `lamfec.pan`. Screens 05, 07 and 08 move on to the next screen by themselves, as required | 28-09-2026 |
| IMP-034 | Existing-customer screens 10 and 11: `T.curated` (with `PORTFOLIO`, `FUNDS`, `U2`, `fundHead`, `offerCard`) and loader variant 3 copied into `lamf-existing-customer/assets/lamf.js`; banner icon and the 13 fund icons copied into this folder's `assets/img/`. Checked in the browser: OTP 000000 on the mock → 07 → 08 → 09 → 10 → 11 in about 1.3 s steps, no missing images or script errors | 28-09-2026 |
| IMP-035 | Popup `T.panTypeModal` / `panTypeBehaviour` and its styles removed; replaced by `T.applyNew` / `applyNewBehaviour` (`.an-*` styles) in `lamf-existing-customer/`. Old screen file `04.1) Apply for New Loan PAN type popup.html` deleted; new screens 04.1 page, 04.2 Existing PAN selected, 04.3 New PAN verified. Checked in the browser: both paths through to screen 05, all field errors, linked-PAN refusal, under-18 refusal, consent gating, close on 05 → 04.1, no sideways scroll at 390px | 28-09-2026 |
| IMP-036 | Screen 12 added to `lamf-existing-customer/`: `T.selection`, `SEL_ORDER`, `SEL_DEFAULT`, `selectCard`, `stepper` and the back / pencil / info icons copied from the new-customer journey; FLOW: Curated Offers `start-application` → 12, 12 `back` → 11. Checked in the browser: navigation both ways, 9 fund cards, stepper, note on Continue, no missing images or errors | 28-09-2026 |
| IMP-037 | `selectionBehaviour` in `lamf-existing-customer/assets/lamf.js` keeps the fund amounts as state and repaints the selection page from `T.selection` on every change (constants `LOAN_MIN`, `LOAN_MAX`, `LTV` at its top; messages in `SEL_ERR`). `selectCard` / `T.selection` gained data hooks and error slots. Checked in the browser: loan edit valid / below min / above max, slider, fund edit above Max Limit / valid, tick, untick all → min-amount message and Continue off, Select All both ways, review screens 12.1 / 12.2, Back → 11, no script errors | 28-09-2026 |
| IMP-038 | Screen 13 added (`T.summary(amount)` in `lamf-existing-customer/assets/lamf.js`); screen 12 stores the selected fund amounts as `lamfec.sel` on Continue and restores them when the user comes back. Checked in the browser: reference values reproduced, ₹ 5,00,000 example (pledge ₹ 6,66,666.67, interest ₹ 4,375.00, fee ₹ 2,950), Back keeps the selection, Continue note, no script errors | 28-09-2026 |
| IMP-039 | Screen 14 added (`kycRow`, `T.kyc` copied into `lamf-existing-customer/assets/lamf.js`, loan amount parameter added; DigiLocker logo copied to this folder's `assets/img/`). Demo email for later KYC states: ravikumar.s@example.com. Checked in the browser: Summary Continue → 14 with the chosen amount, direct open shows ₹ 1,55,36,100, Back → 13, notes on Verify / View details, no missing images or errors | 28-09-2026 |
| IMP-040 | `kycBehaviour` repaints screen 14 from `T.kyc` using the remembered PAN choice; `PAN_DETAILS` gained `email`; `T.applyNew` has the `an-personal` section and the consent block moved out of the PAN section. Checked in the browser: personal details hidden until an existing PAN is chosen, email follows the PAN, hidden for New PAN; KYC shows Email Complete + Start KYC for Existing PAN and the email box for New PAN; 14.1 review screen; Back → 13 | 28-09-2026 |
| IMP-041 | `T.kycMock`, `kycMockBehaviour` and the `lamfec.kyc` progress added in `lamf-existing-customer/assets/lamf.js`; `T.kyc` gained photo `done` and failure notes (`aadErr`, `photoErr`). Checked in the browser: Start KYC → 15, Failure → error + retry, Success → Aadhaar Complete + Photo Start, Photo Failure / Success, review screens 14.2 / 14.3, no errors | 28-09-2026 |
| IMP-042 | `PAN_DETAILS[pan].bank` added; `T.applyNew` has the `an-bank` section; `kycRow` gained the `doneOpen` state; `T.kyc` takes `bank` and `cont`; `kycBehaviour` picks the bank of the stored PAN and enables Continue when Aadhaar and Photo are done. Checked in the browser: ETB bank fields read-only and following the PAN, hidden for New PAN; KYC card for both PANs, Continue off → message, on after both mocks succeed; 14.1 unchanged | 28-09-2026 |
| IMP-043 | `PROFILE`, `CD_OPTIONS`, `CD_FIELDS`, `T.custDetails`, `custDetailsBehaviour` added in `lamf-existing-customer/assets/lamf.js`; ETB personal section built from `CD_FIELDS` so both pages show the same fields. Stepper made to scroll inside itself on phones (≤ 760px) in this folder's CSS – it widened the page by ~270px on a 390px screen (same issue exists in the new-customer journey, not changed there). Checked in the browser: ETB values for both PANs, read-only; 14 → 17; no Fill Default / Save Details; required-field and declaration errors; collapse / expand; Back → 14; no sideways scroll at 390px | 28-09-2026 |
| IMP-044 | `ETB_EDIT`, `etbSection`, `etbField` build the ETB sections from `CD_FIELDS`; details refresh only when the chosen PAN changes (edits are kept otherwise); edits saved as `lamfec.profile` on Continue and merged into screen 17. Checked in the browser: 4 sections, editable list exactly Salutation, Marital Status, Other details and declarations; errors and clearing; edits shown on 17; PAN switch reloads the record | 28-09-2026 |
| IMP-045 | `T.applyNew`: bank section moved after the PAN section, grids use `.an-ro3`, `an-det-mobile` added; CSS block “ETB page redesign” in `lamf-existing-customer/assets/lamf.css`. Checked in the browser at 1366px (order, three per row, mobile number from `lamfec.mobile`) and 390px (no sideways scroll); New PAN still hides all detail sections | 28-09-2026 |
| IMP-046 | `T.pledge`, `T.pledgeOtpModal`, `T.pledgedModal`, `pledgeBehaviour` and `lamfec.pledge` added in `lamf-existing-customer/assets/lamf.js`, styles “18 Pledging of Mutual Fund” in `lamf.css`. Checked in the browser: 17 → 18 with the chosen amount, View Securities note, empty / wrong OTP, close → 18, 000000 → 18.2 → countdown → 18 Pledged + note, Back → 17, no errors | 29-09-2026 |
| IMP-047 | `T.agreement` and the `openPending` state of `kycRow` added; 18.2 redirects to 19. Checked in the browser: 000000 on the pledge OTP → 18.2 → 19, stepper 3 done + step 4 active, both rows Pending, Sign Agreement note, 18 still shows Pledged | 29-09-2026 |
| IMP-048 | `T.sanction`, `T.esign`, `inWords` (Indian numbering), `loanContext`, `sanctionBehaviour`, `esignBehaviour`, `lamfec.agreement` added; `T.agreement(signed)` shows the signed state. Checked in the browser: 19 → 20 (letter contents, Submit disabled → enabled) → 21 (amount in words, mobile in consent) → 19 with Loan Agreement Complete and Set up E-Mandate; amount-in-words check for ₹ 12,34,567; no sideways scroll at 390px; no errors | 29-09-2026 |

---

*End of document — updated continuously as the LAMF LOS discussion progresses.*
