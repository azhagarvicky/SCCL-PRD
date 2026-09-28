/* ==========================================================
   LAMF – Apply for New Loan (Existing Customer)
   Separate prototype from lamf-journey/ (the new-customer journey).
   Every screen HTML calls LAMF.render(...) with a template.
   Edit a component here once → it changes on all screens of this folder.
   ========================================================== */
(function () {
  const IMG = 'assets/img/';

  /* ---------------- Screen register (sort order) ---------------- */
  const SCREENS = [
    '01) LAMF Landing Page',
    '02) Enter MF linked Mobile Number',
    '03) Enter OTP for MF linked Mobile Number Verification',
  ];
  const href = (name) => encodeURIComponent(name + '.html');
  /* The Shriram Credit logo on every screen goes back to this prototype's home page */
  const logoLink = (inner) => `<a class="logo" href="index.html" title="Home">${inner}</a>`;

  /* ---------------- Demo customer data ---------------- */
  const CUSTOMER = { mobile: '9597001623', mobileMasked: '+9195XXXX1623' };

  /* ---------------- Icons ---------------- */
  const S = (p, vb = '0 0 24 24', extra = '') => `<svg viewBox="${vb}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" ${extra}>${p}</svg>`;
  const ICON = {
    close: S('<circle cx="12" cy="12" r="9.5"/><path d="M9 9l6 6M15 9l-6 6"/>', '0 0 24 24', 'stroke="#555" stroke-width="1.3"'),
    pencilSolid: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 17.25V21h3.75L17.8 9.94l-3.75-3.75L3 17.25zM20.7 7.04a1 1 0 0 0 0-1.41l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>`,
    phone: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25c1.1.37 2.3.57 3.6.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>`,
    shield: `<svg viewBox="0 0 24 24" fill="#FFCB08"><path d="M12 2l8 3v6c0 5-3.4 9.4-8 11-4.6-1.6-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5" stroke="#fff" stroke-width="2" fill="none"/></svg>`,
    tick: `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#111"/><path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" stroke-width="2.4" fill="none"/></svg>`,
    // landing step icons (yellow outline)
    s1: S('<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>'),
    s2: S('<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'),
    s3: S('<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3"/><circle cx="12" cy="10" r="2.5"/><path d="M8 16.5c.8-1.8 2.2-2.6 4-2.6s3.2.8 4 2.6"/>'),
    s4: S('<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/><path d="M12 14v2"/>'),
    s5: S('<path d="M3 17c2-1 3-6 4-9s2-3 2 0-2 9-1 9 2-4 3-4 1 3 2 3 1-1 2-1"/><path d="M3 21h18"/>'),
    s6: S('<rect x="3" y="6" width="18" height="14" rx="2"/><path d="M3 10h18M16 15h2"/><path d="M6 6l9-3 1 3"/>'),
    s7: S('<path d="M2 17h4l5 2 7-3a1.5 1.5 0 0 0-1-2.8L13 14"/><path d="M6 15l3-2h4a1 1 0 0 1 0 2h-3"/><path d="M16 3v6M13.5 6.5L16 9l2.5-2.5"/>'),
    s8: S('<path d="M11 17l2 2a1.4 1.4 0 0 0 2-2"/><path d="M14 14l2.5 2.5a1.4 1.4 0 0 0 2-2l-3.9-3.9a2 2 0 0 0-2.8 0l-.9.9a1.4 1.4 0 0 1-2-2l2.8-2.8a3.9 3.9 0 0 1 4.8-.6l.5.3a3 3 0 0 0 2 .4H21v7h-1.5"/><path d="M3 5h2.5l3 1.5M3 12h1.5l6 6"/><path d="M3 5v7"/>'),
  };

  const img = (f, cls = '', style = '') => `<img src="${IMG}${f}" class="${cls}" style="${style}" alt="">`;

  /* ---------------- Header ---------------- */
  const header = () => `
    <header class="hdr site">
      ${logoLink(img('shriram-logo.png'))}
      <nav class="site-nav"><a>About Us</a><a>Product &amp; Services</a><a>Investors</a><a>Learning Lounge</a><a>Careers</a></nav>
      <div class="site-right"><a class="phone" href="tel:+918981003538"><span style="width:15px;height:15px;display:inline-block">${ICON.phone}</span>+91 898-100-3538</a><a class="contact" href="https://www.shriramcredit.in/contact-us">Contact Us</a></div>
    </header>`;

  /* ---------------- Modals ---------------- */
  const closeBtn = `<button class="close" aria-label="Close">${ICON.close}</button>`;
  const withModal = (bg, modal, dark) => `<div class="blur-bg">${bg}</div><div class="overlay ${dark ? 'dark' : ''}">${modal}</div>`;

  /* ======================================================
     PAGE TEMPLATES
     ====================================================== */
  const T = {};

  /* 01 Landing */
  T.landing = () => `
    ${header()}
    <section class="hero"><div class="hero-in">
      <div class="hero-l">
        <span class="safe-pill"><span class="sh">${ICON.shield}</span>100% Safe and Compliant</span>
        <h1>Get <em>Loan Against Mutual Fund</em> for Personal Needs</h1>
        <p class="tag">Smart investors pledge. They don’t sell.</p>
        <p class="desc">A Loan Against Mutual Fund (LAMF) is a secured loan where you pledge or lien mark your Mutual Fund units as collateral to get access to capital - without redeeming your investments.</p>
        <ul class="feat">
          <li>${ICON.tick}Interest rate starting at 10.5% p.a.*</li><li>${ICON.tick}Continue earning returns on your investments</li>
          <li>${ICON.tick}100% paperless process</li><li>${ICON.tick}Interest only repayment and EMI options available</li>
          <li>${ICON.tick}Instant loan approval</li><li>${ICON.tick}RBI regulated NBFC with 25+ years of legacy</li>
        </ul>
        <a class="btn btn-primary hero-cta" data-cta="check-eligibility">Check your eligibility in 2 minutes</a>
      </div>
      <div class="hero-r">${img('hero-person.png', 'hero-img')}</div>
    </div></section>
    <section class="how">
      <h2><span class="ul">How to Apply for a Loan Against<svg viewBox="0 0 610 14" preserveAspectRatio="none"><path d="M2 9 C 150 3, 420 3, 606 10" stroke="#FFCB08" stroke-width="3" fill="none" stroke-linecap="round"/></svg></span><br>Mutual Fund (LAMF)?</h2>
      <p class="how-sub">Getting a Loan Against Mutual Fund for personal needs with Shriram Credit is a paperless process that ensures minimal turnaround time. Here is how it works — from checking eligibility to getting funds credited to your bank account.</p>
      <div class="steps-grid">
        ${[['s1', 'Check your eligibility, credit limit, and interest rates.'], ['s2', 'Select Mutual Fund units to pledge.'], ['s3', 'Complete your KYC verification.'], ['s4', 'Pledge your selected Mutual Fund units.'],
           ['s5', 'e-Sign the loan agreement.'], ['s6', 'Your loan account is ready to use.'], ['s7', 'Withdraw funds as needed.'], ['s8', 'Repay the loan at your convenience and regain complete control of your Mutual Fund holdings.']]
          .map(([ic, t], k) => `<div class="step-card"><span class="sc-ico">${ICON[ic]}</span><b>STEP ${k + 1}</b><p>${t}</p></div>`).join('')}
      </div>
      <div style="text-align:center"><a class="btn btn-primary start-app" data-cta="start-application">Start Your Application</a></div>
    </section>
    <footer class="site-foot"><div class="foot-in">
      <div>${logoLink(img('shriram-logo.png', '', 'height:50px;mix-blend-mode:multiply'))}</div>
      <div><h4>Subsidiaries</h4><a>Shriram Asset Management Co. Ltd.</a><a>Shriram Fortune Solutions Ltd.</a><a>Shriram Insight Share Brokers Ltd.</a><a>Shriram Wealth Ltd.</a><a>Way2Wealth Brokers Pvt. Ltd.</a></div>
      <div><h4>Others</h4><a>About Us</a><a>Product &amp; Services</a><a>Investors</a><a>Learning Lounge</a><a>Careers</a><a>Our Partners</a><a>RBI Sachet</a><a>Terms And Conditions</a><a>Privacy Policy</a></div>
      <div><h4>Contact Us</h4><p>Shriram House, No.4, Burkit Road, T.Nagar,<br>Chennai-600017.<br>Email ID: Info@Shriramcredit.In</p></div>
    </div></footer>`;

  /* 02 Mobile number modal */
  T.mobileModal = () => `
    <div class="modal m-mobile">${closeBtn}
      <h3>Enter your MF linked Mobile Number</h3>
      <input class="input" id="mobile" placeholder="9876543210" maxlength="10" inputmode="numeric" autocomplete="off">
      <p class="field-err" id="mobile-err"></p>
      <div class="m-foot">
        <label class="chk"><input type="checkbox" id="consent"><span>By proceeding, I agree to <a data-legal="tnc">T&amp;C</a> and <a data-legal="privacy">Privacy Policy</a> of Shriram Credit.</span></label>
        <button class="btn btn-disabled btn-block" data-cta="continue">Continue</button>
      </div>
    </div>`;

  /* 03 OTP modal */
  T.otpModal = () => `
    <div class="modal m-otp">${closeBtn}
      <h3>Enter OTP</h3>
      <p class="sent">A 6-digit OTP has been sent by Shriram Credit to<br><span id="otp-mobile">${CUSTOMER.mobileMasked}</span> <a class="edit" data-cta="edit-mobile"><span style="width:12px;height:12px;display:inline-block">${ICON.pencilSolid}</span> Edit</a></p>
      <div class="otp">${'<input maxlength="1" inputmode="numeric" autocomplete="off">'.repeat(6)}</div>
      <p class="resend">Didn’t Receive OTP? <span id="resend"></span></p>
      <p class="field-err" id="otp-err"></p>
      <div class="m-foot">
        <label class="chk"><input type="checkbox" id="experian-consent"><span>I hereby consent to appoint Shriram Credit as my authorised representative to receive my credit information from Experian for the purpose of providing/ evaluating loan offers.</span></label>
        <button class="btn btn-disabled btn-block" data-cta="submit-otp">Submit OTP</button>
      </div>
    </div>`;

  /* ==========================================================
     LEGAL – T&C / Privacy Policy popup content (same summaries as lamf-journey).
     Replace each line with the exact legal wording before this goes live.
     ========================================================== */
  const LEGAL = {
    tnc: {
      title: 'Terms and Conditions',
      source: 'https://www.shriramcredit.in/terms-and-conditions',
      sections: [
        ['About SCCL and these Terms', 'Shriram Credit Company Limited (SCCL) is an RBI-regulated NBFC. These terms govern the website, the apps and the loan services offered on them.'],
        ['Key definitions', 'Defines Borrower, LAMF (Loan Against Mutual Funds), LSP/DLA (lending service providers and digital lending apps) and Applicable Law.'],
        ['Eligibility', 'You must be an Indian resident, 18 years or above, legally competent and solvent, and own unencumbered mutual fund units to pledge.'],
        ['The LAMF facility', 'Interest is charged only on the amount drawn. The facility is non-revolving, units are lien-marked, and margin is monitored.'],
        ['Lending Service Providers and Digital Lending Apps', 'SCCL works with third-party LSPs and digital lending apps for onboarding and servicing. The current list is published on the Partners page.'],
        ['KYC, execution and consents', 'Covers the consents you give for identity verification, Aadhaar authentication, credit checks, document storage and electronic execution of the loan.'],
        ['Key Facts Statement, APR and cooling-off period', 'A Key Facts Statement with the APR is shared before execution, and you may exit during the cooling-off period.'],
        ['Fees, charges, repayment and recovery', 'Charges are as set out in the KFS. Covers order of repayment, penalties on default, and fair recovery practices as per RBI guidelines.'],
        ['Right of lien and set-off', 'SCCL may adjust amounts you owe against funds of yours held with it.'],
        ['Your account and security of credentials', 'You are responsible for keeping your login credentials safe. SCCL uses industry-standard protection but is not liable for losses from shared credentials.'],
        ['Communications and consent', 'You agree to be contacted by call, SMS, email and other channels for servicing and recovery. Marketing messages can be opted out of.'],
        ['Withdrawal of consent and closure', 'Consents can be withdrawn in app settings or by email. Withdrawal applies going forward and does not cancel existing obligations.'],
        ['Your obligations and prohibited uses', 'No unlawful use, false information, malware, unauthorised access, scraping or commercial use of the platform.'],
        ['Intellectual property and licence', 'All platform content belongs to SCCL. You get a limited licence for personal, non-commercial use.'],
        ['Disclaimers and limitation of liability', 'The platform is provided "as is" without warranties. Liability for indirect losses is limited, except for wilful default or gross negligence.'],
        ['Indemnity', 'You cover SCCL for losses arising from breach of these terms, fraud, misrepresentation or unauthorised use of your account.'],
        ['Suspension and termination', 'Access may be suspended or ended for breach, suspected fraud, regulatory orders or insolvency. Repayment obligations continue.'],
        ['Records as evidence', 'SCCL’s records of transactions are conclusive evidence of activity on the platform, except for obvious error.'],
        ['Force majeure', 'SCCL is not liable for failures caused by events beyond its reasonable control, such as natural events or system failures.'],
        ['Grievance redressal', 'Escalation path: customer helpline, then Grievance Officer, then the internal ombudsman, and finally the RBI.'],
        ['Governing law, jurisdiction and limitation', 'Indian law applies, courts at Chennai have jurisdiction, claims must be raised within one year and on an individual basis.'],
        ['Amendments and general', 'Terms may be amended by posting an update. These terms are the entire agreement and SCCL may assign its rights.'],
      ],
    },
    privacy: {
      title: 'Privacy Policy',
      source: 'https://www.shriramcredit.in/privacy-policy',
      sections: [
        ['Introduction', 'Shriram Credit Company Limited is an RBI-registered NBFC. This policy explains how personal information is collected and handled on its website and lending apps.'],
        ['Acknowledgment and Consent', 'By using the platform you consent to the collection of your data and confirm you are 18 or above and that your details are true.'],
        ['Definitions', 'Explains terms such as Personal Data, Data Principal and Processing as used in this policy.'],
        ['Information we collect', 'Four categories: what you provide, what is collected automatically, what comes from third parties, and data handled by vendors for KYC and payments.'],
        ['Lawful grounds for processing', 'Processing is based on your consent, performance of the contract, regulatory compliance and other lawful purposes.'],
        ['KYC, execution and device permissions', 'Identity is verified through CKYC and eKYC. One-time device permissions such as camera, location and SMS are taken with your explicit consent.'],
        ['How we use your information', 'Identity verification, credit assessment, loan servicing, fraud prevention and regulatory compliance, plus analytics.'],
        ['Sharing and disclosure', 'Shared on a need-to-know basis with partners, service providers, regulators and authorities as permitted by law. Your data is not sold.'],
        ['Data localisation', 'Personal data is stored on servers in India with safeguards that meet RBI and DPDP requirements.'],
        ['Retention and erasure', 'Retention runs from one year for transaction data to a minimum of five years for loan data, in line with PMLA and RBI rules.'],
        ['Your rights as a Data Principal', 'You may access, correct and delete your data, withdraw consent and raise grievances, subject to legal limits.'],
        ['Cookies', 'Cookies are used to run the platform and for analytics. You can control them in your browser settings.'],
        ['How we keep your data secure', 'TLS encryption, firewalls, access controls and breach notification as required by DPDP and RBI guidelines.'],
        ['Grievance redressal and contact', 'Contact details for the Grievance Redressal Officer, with escalation to the RBI Ombudsman and the Data Protection Board of India.'],
        ['Children', 'The services are not meant for anyone under 18 and their data is not knowingly processed without parental consent.'],
        ['Changes to this Policy', 'The policy is reviewed annually and may be updated, with material changes notified as required by law.'],
      ],
    },
  };

  T.legalModal = (key) => {
    const d = LEGAL[key];
    return `<div class="overlay legal-overlay"><div class="modal m-legal">
      <div class="lg-head"><h3>${d.title}</h3><button class="close" data-cta="close-legal">${ICON.close}</button></div>
      <div class="lg-body">${d.sections.map(([h, p]) => `<h4>${h}</h4><p>${p}</p>`).join('')}
        <p class="lg-src">Summarised for this prototype from ${d.source}</p></div>
      <div class="lg-foot"><button class="btn btn-primary bold" data-cta="accept-legal">Accept</button></div>
    </div></div>`;
  };

  /* ==========================================================
     FLOW – which CTA on which screen opens which screen.
     ========================================================== */
  const FLOW = {
    '01) LAMF Landing Page': {
      'check-eligibility': '02) Enter MF linked Mobile Number',
      'start-application': '02) Enter MF linked Mobile Number',
    },
  };

  const currentScreen = () => decodeURIComponent(location.pathname.split('/').pop()).replace(/\.html$/, '');
  const go = (screen) => { location.href = href(screen); };

  /* Short on-screen note, used where the next screen is not built yet */
  const toast = (msg) => {
    document.querySelectorAll('.ec-toast').forEach((t) => t.remove());
    const el = document.createElement('div');
    el.className = 'ec-toast';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 4000);
  };

  /* ==========================================================
     BEHAVIOUR – per screen field logic and validations.
     ========================================================== */
  /* Storage keys use their own prefix so this prototype never reads or
     overwrites the new-customer journey's data (same site, same browser). */
  const K = { mobile: 'lamfec.mobile', otp: 'lamfec.otp' };
  const store = {
    get(k, d = null) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } },
  };
  /* Mask as shown in the journey: +91 + first 2 digits + XXXX + last 4 */
  const maskMobile = (m) => (m && m.length === 10 ? `+91${m.slice(0, 2)}XXXX${m.slice(6)}` : CUSTOMER.mobileMasked);

  const OTP_RULES = {
    length: 6,
    resendSeconds: 30,        // timer runs 0:30 → 0:01, then Resend OTP is enabled
    maxResend: 3,             // 3 back-to-back resends
    resendBlockMin: 15,       // then blocked for 15 minutes
    maxWrong: 3,              // 3 wrong OTP attempts
    wrongBlockMin: 60,        // then blocked for 60 minutes
    demoOtp: '123456',        // prototype only – no OTP service is called
  };
  const OTP_ERR = {
    chars: 'Only numbers are allowed. Letters, spaces and special characters cannot be entered.',
    incomplete: 'Please enter the 6-digit OTP.',
    consent: 'Please provide the consent to proceed.',
    wrong: (left) => `The OTP you entered is incorrect. Please try again. ${left} attempt${left === 1 ? '' : 's'} remaining.`,
    resendBlocked: (m) => `You have used all ${OTP_RULES.maxResend} OTP resend attempts. Please try again after ${m} minute${m === 1 ? '' : 's'}.`,
    wrongBlocked: (m) => `You have entered an incorrect OTP ${OTP_RULES.maxWrong} times. Please try again after ${m} minute${m === 1 ? '' : 's'}.`,
  };

  const MOBILE_ERR = {
    empty: 'Please enter your MF linked mobile number.',
    chars: 'Only numbers are allowed. Letters, spaces and special characters cannot be entered.',
    start: 'Mobile number cannot start with 0, 1, 2, 3, 4 or 5. Please enter a valid mobile number.',
    length: 'Mobile number must be 10 digits.',
    consent: 'Please accept the T&C and Privacy Policy to continue.',
  };

  const BEHAVIOUR = {
    /* ---- 02 Enter MF linked Mobile Number ---- */
    '02) Enter MF linked Mobile Number': () => {
      const modal = document.querySelector('.m-mobile');
      const input = document.getElementById('mobile');
      const err = document.getElementById('mobile-err');
      const consent = document.getElementById('consent');
      const cta = modal.querySelector('[data-cta="continue"]');

      const showErr = (msg) => { err.textContent = msg || ''; input.classList.toggle('has-err', !!msg); };

      // Close icon: back to the previous page (the landing page)
      modal.querySelector('.close').onclick = () => go('01) LAMF Landing Page');

      // Numeric only, 10 digits, cannot start with 0-5
      input.addEventListener('keydown', (e) => {
        if (e.key.length > 1 || e.ctrlKey || e.metaKey) return;      // arrows, backspace, shortcuts
        if (!/[0-9]/.test(e.key)) { e.preventDefault(); showErr(MOBILE_ERR.chars); return; }
        if (input.selectionStart === 0 && /[0-5]/.test(e.key)) { e.preventDefault(); showErr(MOBILE_ERR.start); }
      });
      input.addEventListener('input', () => {
        const before = input.value;
        const digits = before.replace(/\D/g, '').slice(0, 10);       // keep digits only (also covers paste)
        const v = digits.replace(/^[0-5]+/, '');                     // an invalid first digit is not accepted
        input.value = v;
        if (v !== digits) showErr(MOBILE_ERR.start);
        else if (digits !== before) showErr(MOBILE_ERR.chars);       // something non-numeric was removed
        else if (/^[6-9]\d{9}$/.test(v)) showErr('');                // valid: clear the message
      });
      input.addEventListener('blur', () => {
        if (input.value && input.value.length < 10) showErr(MOBILE_ERR.length);
      });

      // Checkbox enables the Continue CTA
      const sync = () => {
        cta.classList.toggle('btn-primary', consent.checked);
        cta.classList.toggle('bold', consent.checked);
        cta.classList.toggle('btn-disabled', !consent.checked);
      };
      consent.addEventListener('change', () => { sync(); if (consent.checked) showErr(err.textContent === MOBILE_ERR.consent ? '' : err.textContent); });
      sync();

      // T&C / Privacy Policy popups
      const openLegal = (key) => {
        if (document.querySelector('.legal-overlay')) return;   // one popup at a time
        document.body.insertAdjacentHTML('beforeend', T.legalModal(key));
        const ov = document.querySelector('.legal-overlay');
        const close = () => ov.remove();
        ov.querySelector('[data-cta="close-legal"]').onclick = close;
        ov.querySelector('[data-cta="accept-legal"]').onclick = () => { consent.checked = true; sync(); showErr(err.textContent === MOBILE_ERR.consent ? '' : err.textContent); close(); };
        ov.addEventListener('click', (e) => { if (e.target === ov) close(); });
      };
      modal.querySelectorAll('[data-legal]').forEach((a) => { a.onclick = () => openLegal(a.dataset.legal); });
      if (location.hash === '#tnc' || location.hash === '#privacy') openLegal(location.hash.slice(1));

      // Coming back from the OTP screen via Edit: prefill what the user entered
      const saved = store.get(K.mobile);
      if (saved) input.value = saved;

      // Continue: check every rule before moving on
      cta.addEventListener('click', () => {
        const v = input.value;
        if (!consent.checked) return showErr(MOBILE_ERR.consent);
        if (!v) return showErr(MOBILE_ERR.empty);
        if (!/^[6-9]/.test(v)) return showErr(MOBILE_ERR.start);
        if (v.length !== 10) return showErr(MOBILE_ERR.length);
        showErr('');
        store.set(K.mobile, v);                                   // carried to the OTP screen
        go('03) Enter OTP for MF linked Mobile Number Verification');
      });
    },

    /* ---- 03 Enter OTP for MF linked Mobile Number Verification ---- */
    '03) Enter OTP for MF linked Mobile Number Verification': () => {
      const modal = document.querySelector('.m-otp');
      const boxes = [...modal.querySelectorAll('.otp input')];
      const err = document.getElementById('otp-err');
      const consent = document.getElementById('experian-consent');
      const cta = modal.querySelector('[data-cta="submit-otp"]');
      const resendSlot = document.getElementById('resend');

      const mobile = store.get(K.mobile) || CUSTOMER.mobile;
      document.getElementById('otp-mobile').textContent = maskMobile(mobile);

      const key = `${K.otp}.${mobile}`;
      let st = store.get(key, { resend: 0, wrong: 0, blockedUntil: 0, reason: '' });
      const save = () => store.set(key, st);
      const minsLeft = () => Math.max(1, Math.ceil((st.blockedUntil - Date.now()) / 60000));
      const isBlocked = () => st.blockedUntil > Date.now();

      const showErr = (msg) => { err.textContent = msg || ''; boxes.forEach((b) => b.classList.toggle('has-err', !!msg)); };
      const otpValue = () => boxes.map((b) => b.value).join('');

      // Submit is enabled only when 6 digits are entered AND the consent is ticked
      const sync = () => {
        const ok = otpValue().length === OTP_RULES.length && consent.checked && !isBlocked();
        cta.classList.toggle('btn-primary', ok);
        cta.classList.toggle('bold', ok);
        cta.classList.toggle('btn-disabled', !ok);
      };

      // ---- resend timer / blocked state ----
      let tick = null;
      const stopTick = () => { if (tick) { clearInterval(tick); tick = null; } };
      const startTick = (fn, ms) => { tick = setInterval(fn, ms); };

      const setEnabled = (on) => {
        boxes.forEach((b) => { b.disabled = !on; });
        consent.disabled = !on;
        modal.classList.toggle('is-blocked', !on);
      };

      const showBlocked = () => {
        stopTick();
        setEnabled(false);
        resendSlot.innerHTML = '<span class="mut">Resend OTP</span>';
        const paint = () => {
          if (!isBlocked()) {                       // block time is over → fresh start
            st = { resend: 0, wrong: 0, blockedUntil: 0, reason: '' }; save();
            stopTick(); setEnabled(true); showErr(''); startTimer(); sync(); return;
          }
          showErr(st.reason === 'wrong' ? OTP_ERR.wrongBlocked(minsLeft()) : OTP_ERR.resendBlocked(minsLeft()));
        };
        paint();
        startTick(paint, 1000);                     // remaining minutes stay correct over time
        sync();
      };

      const startTimer = () => {
        stopTick();
        let left = OTP_RULES.resendSeconds;
        const paint = () => {
          if (left > 0) {
            resendSlot.innerHTML = `<span class="mut">0:${String(left).padStart(2, '0')} Resend OTP</span>`;
            left -= 1;
          } else {
            stopTick();
            resendSlot.innerHTML = '<a class="link-yellow" id="resend-cta">Resend OTP</a>';
            document.getElementById('resend-cta').onclick = onResend;
          }
        };
        paint();
        startTick(paint, 1000);
      };

      const onResend = () => {
        st.resend += 1; save();
        boxes.forEach((b) => { b.value = ''; });
        sync();
        if (st.resend >= OTP_RULES.maxResend) {     // 3rd resend used → block
          st.blockedUntil = Date.now() + OTP_RULES.resendBlockMin * 60000;
          st.reason = 'resend'; save();
          showBlocked();
          return;
        }
        showErr('');
        startTimer();                                // OTP sent again, timer restarts
      };

      // ---- OTP boxes: numeric only, one digit each, max 6 ----
      boxes.forEach((box, idx) => {
        box.addEventListener('keydown', (e) => {
          if (e.key === 'Backspace' && !box.value && boxes[idx - 1]) { boxes[idx - 1].focus(); return; }
          if (e.key.length > 1 || e.ctrlKey || e.metaKey) return;
          if (!/[0-9]/.test(e.key)) { e.preventDefault(); showErr(OTP_ERR.chars); }
        });
        box.addEventListener('input', () => {
          const before = box.value;
          const digits = before.replace(/\D/g, '');
          if (digits.length > 1) {                   // pasted OTP → spread across the boxes
            digits.slice(0, OTP_RULES.length - idx).split('').forEach((d, k) => { if (boxes[idx + k]) boxes[idx + k].value = d; });
            const last = Math.min(idx + digits.length, OTP_RULES.length) - 1;
            boxes[last].focus();
          } else {
            box.value = digits;
            if (digits && boxes[idx + 1]) boxes[idx + 1].focus();
          }
          if (digits !== before) showErr(OTP_ERR.chars);
          else if (err.textContent === OTP_ERR.incomplete && otpValue().length === OTP_RULES.length) showErr('');
          sync();
        });
      });

      consent.addEventListener('change', () => { if (err.textContent === OTP_ERR.consent) showErr(''); sync(); });

      // Close icon → landing page. Edit → back to the mobile number screen (prefilled).
      modal.querySelector('.close').onclick = () => go('01) LAMF Landing Page');
      modal.querySelector('[data-cta="edit-mobile"]').onclick = () => go('02) Enter MF linked Mobile Number');

      // ---- Submit OTP ----
      cta.addEventListener('click', () => {
        if (isBlocked()) return showBlocked();
        const v = otpValue();
        if (v.length !== OTP_RULES.length) return showErr(OTP_ERR.incomplete);
        if (!consent.checked) return showErr(OTP_ERR.consent);

        if (v !== OTP_RULES.demoOtp) {               // wrong OTP
          st.wrong += 1; save();
          if (st.wrong >= OTP_RULES.maxWrong) {
            st.blockedUntil = Date.now() + OTP_RULES.wrongBlockMin * 60000;
            st.reason = 'wrong'; save();
            showBlocked();
            return;
          }
          boxes.forEach((b) => { b.value = ''; });
          boxes[0].focus();
          sync();
          return showErr(OTP_ERR.wrong(OTP_RULES.maxWrong - st.wrong));
        }

        // OTP verified. The next screen for the existing customer is not built yet,
        // so the user stays here with a note until that screenshot is shared.
        st = { resend: 0, wrong: 0, blockedUntil: 0, reason: '' }; save();
        showErr('');
        toast('OTP verified. The next screen will be added once its screenshot is shared.');
      });

      // initial state
      if (isBlocked()) showBlocked(); else startTimer();
      sync();
    },
  };

  function wireBehaviour() {
    const fn = BEHAVIOUR[currentScreen()];
    if (fn) fn();
  }

  function wireFlow() {
    const rules = FLOW[currentScreen()] || {};
    document.querySelectorAll('[data-cta]').forEach((el) => {
      const target = rules[el.dataset.cta];
      if (!target) return;
      el.classList.add('is-live');
      el.addEventListener('click', (e) => { e.preventDefault(); location.href = href(target); });
    });
  }

  /* ---------------- Dev navigator (review only) ---------------- */
  function devnav() {
    const k = SCREENS.indexOf(currentScreen());
    const el = document.createElement('div');
    el.id = 'devnav';
    el.innerHTML = `
      <div class="list">${SCREENS.map((s, j) => `<a href="${href(s)}" class="${j === k ? 'on' : ''}">${s}</a>`).join('')}</div>
      <div class="bar">
        ${k > 0 ? `<a href="${href(SCREENS[k - 1])}" title="Previous screen">‹ Prev</a>` : ''}
        <button class="cur" title="All screens">☰ ${k >= 0 ? SCREENS[k] : 'Screens'}</button>
        ${k >= 0 && k < SCREENS.length - 1 ? `<a href="${href(SCREENS[k + 1])}" title="Next screen">Next ›</a>` : ''}
      </div>`;
    el.querySelector('.cur').onclick = () => el.classList.toggle('open');
    document.body.appendChild(el);
    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT') return;
      if (e.key === 'ArrowRight' && k < SCREENS.length - 1) location.href = href(SCREENS[k + 1]);
      if (e.key === 'ArrowLeft' && k > 0) location.href = href(SCREENS[k - 1]);
    });
  }

  /* ---------------- Render ---------------- */
  function render(html, opts = {}) {
    document.body.className = '';
    document.body.innerHTML = html;
    if (opts.bodyClass) document.body.classList.add(opts.bodyClass);
    wireFlow();
    wireBehaviour();
    // Popup open → freeze the page behind it (only the popup scrolls)
    const hasPopup = !!document.querySelector('.overlay');
    document.body.classList.toggle('modal-open', hasPopup);
    document.documentElement.classList.toggle('modal-open', hasPopup);
    devnav();
  }

  window.LAMF = { T, render, withModal, SCREENS, FLOW, BEHAVIOUR, LEGAL, OTP_RULES, OTP_ERR, MOBILE_ERR, CUSTOMER };
})();
