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
    '04) Your Loans Page',
    '04.1) Apply for New Loan Page',
    '04.2) Apply for New Loan Existing PAN selected',
    '04.3) Apply for New Loan New PAN verified',
    '05) LOS to MF Central Redirection loading page',
    '06) MF Central Mock Page',
    '07) MF Central to LOS Redirecting Page',
    '08) MF Central to LOS Fetching Mutual Fund Portfolio Page',
    '09) MF Central to LOS Analysing Mutual Fund Portfolio Page',
    '10) MF Central to LOS Generating Loan Page',
    '11) Curated Offers Page',
    '12) Mutual Fund Selection Page',
    '12.1) Mutual Fund Selection page loan amount edit',
    '12.2) Mutual Fund Selection page loan amount edit as fund wise',
    '13) Loan Application Summary',
    '14) KYC Verification Page',
    '14.1) KYC Verification Page New PAN email verification',
    '15) DigiLocker Mock Page',
    '15.1) KYC Verification Page Aadhaar verification success',
    '15.2) KYC Verification Page Aadhaar verification failed',
    '16) Photo Verification Mock Page',
    '16.1) KYC Verification Page Photo verification success',
    '16.2) KYC Verification Page Photo verification failed',
    '17) Customer Details Page',
    '18) Pledging of Mutual Fund Page',
    '18.1) Pledging of Mutual Fund OTP popup',
    '18.2) Pledging of Mutual Fund Successfully pledged',
    '19) Agreement and E-Mandate Page',
    '20) Sanction Letter Page',
    '21) Loan Agreement e-Sign Page',
    '21.1) Loan Agreement e-Sign OTP popup',
    '21.2) Loan Agreement e-Sign Signed Successfully',
    '21.3) Loan Agreement Signed Successfully',
    '19.1) Agreement and E-Mandate Page Loan Agreement signed',
    '22) E-Mandate Page',
    '22.1) E-Mandate NPCI Simulation Page',
    '22.2) E-Mandate Authenticated Successfully',
    '23) Loan Application Submitted Page',
  ];
  const href = (name) => encodeURIComponent(name + '.html');
  /* The Shriram Credit logo on every screen goes back to this prototype's home page */
  const logoLink = (inner) => `<a class="logo" href="index.html" title="Home">${inner}</a>`;

  /* ---------------- Demo customer data ---------------- */
  /* pans: PANs already linked to this mobile number (a customer can have at most MAX_PANS) */
  const CUSTOMER = { email: 'ravikumar.s@example.com', mobile: '9597001623', mobileMasked: '+9195XXXX1623', mobileMasked2: '+919XXXX1623', pans: ['CBOPA8195B', 'AKLPS4321K'] };
  const MAX_PANS = 3;
  /* Details already held for each existing PAN (demo data), shown unmasked and read-only */
  const PAN_DETAILS = {
    CBOPA8195B: { name: 'RAVI KUMAR S', dob: '14/05/1988', email: 'ravikumar.s@example.com',
      bank: { holder: 'RAVI KUMAR S', account: '123405670006', ifsc: 'ICIC0002692', name: 'ICICI Bank', logo: 'funds/icici.png' } },
    AKLPS4321K: { name: 'PRIYA R', dob: '02/11/1992', email: 'priya.r@example.com',
      bank: { holder: 'PRIYA R', account: '50100234561234', ifsc: 'HDFC0001234', name: 'HDFC Bank' } },
  };
  /* Customer details on record for each existing PAN (demo data) – used on the ETB page and screen 17 */
  const PROFILE = {
    CBOPA8195B: { salutation: 'Mr', name: 'RAVI KUMAR S', dob: '14/05/1988', gender: 'Male', mother: 'LAKSHMI S', father: 'SUNDARAM K', marital: 'Married',
      purpose: 'Home Renovation', qualification: 'Graduate', occupation: 'Salaried', business: 'Services', income: 'Rs. 10 - 25 Lakhs', source: 'Salary', independent: 'Yes', pep: true, tax: true,
      addr1: 'No. 12, 2nd Street', addr2: 'Anna Nagar West', addr3: 'Chennai, Tamil Nadu, 600040', landmark: 'Near Anna Nagar Tower Park', pincode: '600040', city: 'Chennai' },
    AKLPS4321K: { salutation: 'Ms', name: 'PRIYA R', dob: '02/11/1992', gender: 'Female', mother: 'MEENA R', father: 'RAJAN P', marital: 'Single',
      purpose: 'Education', qualification: 'Post Graduate', occupation: 'Salaried', business: 'Information Technology', income: 'Rs. 5 - 10 Lakhs', source: 'Salary', independent: 'Yes', pep: true, tax: true,
      addr1: 'Flat 4B, Lake View Apartments', addr2: '5th Cross, Koramangala', addr3: 'Bengaluru, Karnataka, 560034', landmark: 'N/A', pincode: '560034', city: 'Bengaluru' },
  };
  /* PAN mask: keep characters 1, 2, 4 and 10 → CBOPA8195B shows as CB*P*****B */
  const maskPan = (p) => p.split('').map((c, k) => ([0, 1, 3, 9].includes(k) ? c : '*')).join('');

  /* Existing loan shown on "Your loans" (values from the shared screenshot) */
  const LOAN = {
    product: 'Loan Against Mutual Fund', status: 'Active',
    available: '5,000', sanctioned: '10,000', pledgedValue: '15,384.61', withdrawn: '5,000',
    principal: '4,500', interestDue: '2.88', repaid: '15,102.88',
    statements: [['Holding Statement', '27/09/2026'], ['Client Statement', '27/09/2026']],
  };

  /* Portfolio fetched from MF Central (demo data, same as the new-customer journey) */
  const PORTFOLIO = {
    total: '12,04,62,749.99', nonEligible: '3,13,02,090.97', eligible: '8,91,60,659.02',
    creditLimit: '6,19,13,200', interest: '10.50% p.a.', fee: '3,09,566', tenure: '12',
    lastUpdated: '21-09-2026 16:11:46', count: 13, eligibleCount: 9, neCount: 4,
  };
  /* Order = MF Central response order (Curated offers / All tab) */
  const FUNDS = [
    { id: 'axis', ico: 'axis', name: 'Axis Quant Fund', sel: 'Axis Quant Fund - Regular Plan - Growth', units: '67891.247', value: '71,59,227.04', selValue: '71,59,227.04', cl: '53,69,420' },
    { id: 'canara', ico: 'canara', name: 'CANARA ROBECO LARGE CAP FUND', sel: 'CANARA ROBECO LARGE CAP FUND - DIRECT PLAN - GROWTH OPTION', units: '16000.568', value: '33,69,214.00', selValue: '33,69,214', cl: '21,89,989' },
    { id: 'edus', ico: 'edelweiss', name: 'Edelweiss US Technology Equity Fund of Fund', units: '67989.436', value: '1,43,37,367.50', cl: '0', ne: true },
    { id: 'icici', ico: 'icici', name: 'ICICI Prudential Global Stable Equity Fund (FOF)', sel: 'ICICI Prudential Global Stable Equity Fund (FOF) - Growth', units: '93001.867', value: '1,87,07,725.46', selValue: '1,87,07,725.46', cl: '1,40,30,794' },
    { id: 'hsbc', ico: 'hsbc', name: 'HSBC Small Cap Fund', sel: 'HSBC Small Cap Fund - Regular Growth', units: '99000.769', value: '1,14,48,795.43', selValue: '1,14,48,795.43', cl: '74,41,717' },
    { id: 'ednifty', ico: 'edelweiss2', name: 'Edelweiss NIFTY PSU Bond Plus SDL Apr 2026 50:50 Index Fund', sel: 'Edelweiss NIFTY PSU Bond Plus SDL Apr 2026 50:50 Index Fund - Direct Plan - Growth', units: '78975.346', value: '52,63,414.60', selValue: '52,63,414.6', cl: '39,47,560' },
    { id: 'nippontw', ico: 'nippon', name: 'Nippon India Taiwan Equity fund- Regular Plan- Growth Option-', sel: 'Nippon India Taiwan Equity fund- Regular Plan- Growth Option', units: '65789.564', value: '2,31,36,498.87', selValue: '2,31,36,498.87', cl: '1,50,38,724' },
    { id: 'motnasdaq', ico: 'motilal', name: 'Motilal Oswal Nasdaq 100 Fund of Fund', units: '87966.345', value: '1,60,86,801.36', cl: '0', ne: true },
    { id: 'kotak', ico: 'kotak', name: 'Kotak Corporate Bond Fund- Direct Plan- Growth Option-', sel: 'Kotak Corporate Bond Fund- Direct Plan- Growth Option', units: '99892.678', value: '55,79,425.62', selValue: '55,79,425.62', cl: '41,84,569' },
    { id: 'sbi', ico: 'sbi', name: 'SBI SAVINGS FUND', sel: 'SBI SAVINGS FUND - REGULAR PLAN - GROWTH', units: '97001.785', value: '28,78,838.38', selValue: '28,78,838.38', cl: '21,59,128' },
    { id: 'nipponhy', ico: 'nippon2', name: 'Nippon India Aggressive Hybrid Fund', units: '7890.867', value: '3,32,478.52', cl: '0', ne: true },
    { id: 'whiteoak', ico: 'whiteoak', name: 'Whiteoak Capital Large & Mid Cap Fund Regular Plan Growth', sel: 'Whiteoak Capital Large & Mid Cap Fund Regular Plan Growth', units: '98000.346', value: '1,16,17,519.62', selValue: '1,16,17,519.62', cl: '75,51,387' },
    { id: 'motbse', ico: 'motilal2', name: 'Motilal Oswal BSE Enhanced Value Index Fund', units: '9870.978', value: '5,45,443.59', cl: '0', ne: true },
  ];
  const F = Object.fromEntries(FUNDS.map((f) => [f.id, f]));
  // Units shown on Curated offers page (2 decimals, as in screenshot)
  const U2 = { axis: '67891.25', canara: '16000.57', edus: '67989.44', icici: '93001.87', hsbc: '99000.77', ednifty: '78975.35', nippontw: '65789.56', motnasdaq: '87966.35', kotak: '99892.68', sbi: '97001.79', nipponhy: '7890.87', whiteoak: '98000.35', motbse: '9870.98' };

  /* ---------------- Icons ---------------- */
  const S = (p, vb = '0 0 24 24', extra = '') => `<svg viewBox="${vb}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" ${extra}>${p}</svg>`;
  const ICON = {
    gauge: S('<path d="M3.5 17.5a9 9 0 1 1 17 0z" /><path d="M12 14l4.5-5" /><path d="M6.5 14h1.5M16 14h1.5"/>'),
    user: S('<circle cx="12" cy="8" r="4.2"/><path d="M4 20.5c1.2-3.8 4.4-5.5 8-5.5s6.8 1.7 8 5.5"/>'),
    download: S('<path d="M12 4v11M7.5 10.5L12 15l4.5-4.5"/><path d="M5 19h14"/>', '0 0 24 24', 'stroke-width="1.8"'),
    pdf: `<svg viewBox="0 0 40 48"><path d="M6 1h21l12 12v31a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3V4a3 3 0 0 1 3-3z" fill="#E4E4E7"/><path d="M27 1v9a3 3 0 0 0 3 3h9z" fill="#C9C9CF"/><rect x="0" y="22" width="30" height="14" rx="2" fill="#E5483B"/><text x="15" y="32.5" text-anchor="middle" font-size="9" font-weight="700" fill="#fff" font-family="Arial, sans-serif">PDF</text></svg>`,
    refresh: S('<path d="M20 11a8 8 0 0 0-14.3-4.3L4 8.5M4 4v4.5h4.5"/><path d="M4 13a8 8 0 0 0 14.3 4.3L20 15.5M20 20v-4.5h-4.5"/>', '0 0 24 24', 'stroke-width="2"'),
    calendar: `<svg viewBox="0 0 24 24" fill="#555"><path d="M19 4h-1V2h-2v2H8V2H6v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 16H5V9h14zM12 13h5v5h-5z"/></svg>`,
    check: S('<path d="M5 12.5l4.5 4.5L19 7.5"/>', '0 0 24 24', 'stroke="#fff" stroke-width="2.6"'),
    back: S('<path d="M20 12H4M10 6l-6 6 6 6"/>'),
    pencil: S('<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13.5 6.5l4 4"/>', '0 0 24 24', 'stroke-width="1.5"'),
    bank: S('<path d="M3 10h18L12 4z"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>'),
    chev: S('<path d="M6 15l6-6 6 6"/>', '0 0 24 24', 'stroke-width="1.8"'),
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

  const rs = (v) => `<span class="rs">₹</span> ${v}`;
  const i = () => `<span class="i">i</span>`;
  const img = (f, cls = '', style = '') => `<img src="${IMG}${f}" class="${cls}" style="${style}" alt="">`;

  /* ---------------- Headers ---------------- */
  // Logged-in header: "Apply for New Loan" replaces "My Portfolio" (existing customer)
  const appHeader = () => `
    <header class="hdr">${logoLink(img('shriram-logo.png'))}
      <div class="hdr-icons"><a class="hdr-cta" data-cta="apply-new-loan">Apply for New Loan</a><span>${ICON.gauge}</span><span>${ICON.user}</span></div>
    </header>`;
  // Logged-in header without the Apply CTA (MF Central hand-off screens)
  const plainHeader = () => `<header class="hdr">${logoLink(img('shriram-logo.png'))}<div class="hdr-icons"><span>${ICON.gauge}</span><span>${ICON.user}</span></div></header>`;
  const header = () => `
    <header class="hdr site">
      ${logoLink(img('shriram-logo.png'))}
      <nav class="site-nav"><a>About Us</a><a>Product &amp; Services</a><a>Investors</a><a>Learning Lounge</a><a>Careers</a></nav>
      <div class="site-right"><a class="phone" href="tel:+918981003538"><span style="width:15px;height:15px;display:inline-block">${ICON.phone}</span>+91 898-100-3538</a><a class="contact" href="https://www.shriramcredit.in/contact-us">Contact Us</a></div>
    </header>`;

  /* ---------------- Stepper ---------------- */
  const STEPS = ['Selection of Mutual Fund', 'KYC Verification & Bank details', 'Pledging of Mutual Fund', 'Agreement & E-Mandate'];
  const stepper = (active = 1) => {
    let h = '<div class="stepper">';
    STEPS.forEach((s, k) => {
      const n = k + 1, cls = n < active ? 'done' : n === active ? 'active' : '';
      h += `<div class="step ${cls}"><span class="dot">${n < active ? ICON.check : n}</span>${s.replace('&', '&amp;')}</div>`;
      if (n < 4) h += `<div class="step-line ${n < active ? 'done' : ''}"></div>`;
    });
    return h + '</div>';
  };

  /* ---------------- Fund cards ---------------- */
  const fundHead = (f, name) => `
    <div class="fund-head"><span class="fund-ico">${img('funds/' + f.ico + '.png')}</span>
      <div><div class="fund-name">${name || f.name}</div><div class="folio">Folio No. 14816008</div></div></div>`;

  // Curated offers list card (No. of Units 2dp + Current Value)
  const offerCard = (f) => `
    <div class="fund-card"><div class="body">${fundHead(f)}
      <div class="fund-cols"><div><div class="lbl">No. of Units</div><div class="val">${U2[f.id]}</div></div>
      <div><div class="lbl">Current Value</div><div class="val">${rs(f.value)}</div></div></div></div></div>`;

  // MF Selection card. opts: {checked, amount, editing, err}. data-id hooks drive the selection logic.
  const selectCard = (f, o = {}) => {
    const amt = o.editing != null
      ? `<span class="amt-edit"><span class="rs">₹</span><input class="fund-in" data-id="${f.id}" value="${o.editing}" inputmode="numeric" maxlength="9" autocomplete="off"><a class="ok" data-fund-ok="${f.id}" title="Update">${ICON.check}</a></span>`
      : `<span class="amt">${rs(o.amount || '0')}<a class="pen" data-fund-edit="${f.id}" title="Edit amount">${ICON.pencil}</a></span>`;
    return `
    <div class="fund-card sel-card" data-card="${f.id}"><div class="body">
      <div class="sel-top">
        <a class="cbx ${o.checked ? 'on' : ''}" data-fund-tick="${f.id}">${o.checked ? ICON.check : ''}</a>
        ${fundHead(f, f.sel)}
        <div class="sel-amt"><div class="lbl">Selected Amount ${i()}</div>${amt}${o.err ? `<p class="field-err sel-err">${o.err}</p>` : ''}</div>
      </div>
      <div class="fund-cols three sel-cols"><div><div class="lbl">No of Units ${i()}</div><div class="val">${f.units}</div></div>
      <div><div class="lbl">Current Value ${i()}</div><div class="val">${rs(f.selValue)}</div></div>
      <div><div class="lbl">Max Limit ${i()}</div><div class="val">${rs(f.cl)}</div></div></div></div></div>`;
  };
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
      <p class="otp-hint">Please use OTP <b>${OTP_RULES.demoOtp}</b> to proceed</p>
      <p class="resend">Didn’t Receive OTP? <span id="resend"></span></p>
      <p class="field-err" id="otp-err"></p>
      <div class="m-foot">
        <label class="chk"><input type="checkbox" id="experian-consent"><span>I hereby consent to appoint Shriram Credit as my authorised representative to receive my credit information from Experian for the purpose of providing/ evaluating loan offers.</span></label>
        <button class="btn btn-disabled btn-block" data-cta="submit-otp">Submit OTP</button>
      </div>
    </div>`;

  /* 04 Your loans (existing customer, after OTP) */
  const stat = (label, v) => `<div class="yl-stat"><span>${label}</span><b><span class="rs">₹</span> ${v}</b></div>`;
  T.loans = () => `
    ${appHeader()}
    <main class="yl">
      <h1>Your loans</h1>
      <h2>${LOAN.product} <span class="yl-badge"><i></i>${LOAN.status}</span></h2>
      <div class="yl-top">
        <div class="yl-bal">
          <p>Available Withdrawal Balance</p>
          <b><span class="rs">₹</span> ${LOAN.available}</b>
          <div class="yl-btns"><a class="btn yl-repay" data-cta="repay">Repay</a><a class="btn btn-primary yl-withdraw" data-cta="withdraw">Withdraw</a></div>
        </div>
        <div class="yl-stats">
          ${stat('Sanctioned Amount', LOAN.sanctioned)}${stat('Value of Pledged Funds', LOAN.pledgedValue)}
          ${stat('Total Withdrawn', LOAN.withdrawn)}${stat('Principal Outstanding', LOAN.principal)}
          ${stat('Interest Due', LOAN.interestDue)}${stat('Repaid Amount', LOAN.repaid)}
        </div>
      </div>
      <nav class="yl-tabs">${['Statements', 'Transaction Details', 'Pledged Mutual Funds Details', 'Loan Details', 'Repayment Schedule']
        .map((t, k) => `<a class="${k === 0 ? 'on' : ''}">${t}</a>`).join('')}</nav>
      <div class="yl-docs">${LOAN.statements.map(([n, d]) => `
        <div class="yl-doc"><div class="yl-doc-top"><span class="yl-pdf">${ICON.pdf}</span><a class="yl-dl" title="Download">${ICON.download}</a></div>
          <div class="yl-doc-foot"><p>${n}</p><small>${d}</small></div></div>`).join('')}
      </div>
    </main>`;

  /* 04.1 – 04.3 Apply for New Loan page (layout modelled on the Shriram Finance FD
     "existing customer" page). o.mode: '' | 'existing' | 'new'; o.pan: pre-selected PAN (review screens) */
  const MFC_CONSENT = 'I authorize Shriram Credit to fetch my mutual fund portfolio holdings from MF Central to assess my eligibility and credit limit for a Loan Against Mutual Funds.';
  /* ETB page customer-details sections (DISC-052): Personal details – only Salutation and Marital Status
     editable; Other details – all editable; KYC Address – read-only. Email ID stays read-only (already verified). */
  const ETB_EDIT = ['salutation', 'marital'];
  const etbSection = (id, title, body, show) => `<section class="an-sec an-personal" id="${id}" ${show ? '' : 'hidden'}><h4>${title}</h4>${body}</section>`;
  const etbField = (pan, [k, label, type], editable) => {
    const v = pan ? PROFILE[pan][k] : '';
    const wide = '';                                        // 3-column grid: every field takes one column
    const input = !editable
      ? `<input class="input readonly" data-pf="${k}" value="${v}" readonly tabindex="-1">`
      : `<select class="input an-select" data-pf="${k}"><option value="">Select</option>${CD_OPTIONS[k].map((opt) => `<option ${opt === v ? 'selected' : ''}>${opt}</option>`).join('')}</select><p class="field-err" data-pf-err="${k}"></p>`;
    return `<div${wide}><label class="field-lbl">${label}${editable ? '<i class="req">*</i>' : ''}</label>${input}</div>`;
  };
  T.applyNew = (o = {}) => `
    ${plainHeader()}
    <div class="an-strip"><div class="an-in">Apply for a new Loan Against Mutual Fund</div></div>
    <main class="an-bg"><div class="an-in"><div class="an-card">
      <div class="an-welcome"><div><small>Welcome Back,</small><b>${maskMobile(store.get(K.mobile) || CUSTOMER.mobile)}</b></div></div>
      <h3 class="an-h">Welcome back! Apply for a new loan below.</h3>
      <p class="an-p">We have fetched the details of your existing loan. You can continue with your existing account by selecting your PAN.<br>To apply with a different PAN, click ‘Apply with New PAN’ and verify it.</p>

      <section class="an-sec">
        <h4>Borrower PAN details</h4>
        <div class="an-toggle">
          <button class="an-opt ${o.mode === 'existing' ? 'on' : ''}" data-mode="existing">Use Existing PAN</button>
          <button class="an-opt ${o.mode === 'new' ? 'on' : ''}" data-mode="new">Apply with New PAN</button>
        </div>
        <p class="field-err" id="an-mode-err"></p>

        <div class="an-existing" id="an-existing" ${o.mode === 'existing' ? '' : 'hidden'}>
          <label class="field-lbl" for="an-pan">Select the PAN to fetch the borrower details</label>
          <select class="input an-select" id="an-pan">
            <option value="">Select PAN</option>
            ${CUSTOMER.pans.slice(0, MAX_PANS).map((p) => `<option value="${p}" ${o.pan === p ? 'selected' : ''}>${maskPan(p)}</option>`).join('')}
          </select>
          <div class="an-details" id="an-details" ${o.pan ? '' : 'hidden'}>
            <h5>Existing details of this PAN</h5>
            <div class="an-ro an-ro3">
              <div><label class="field-lbl" for="an-det-pan">PAN Number</label><input class="input readonly" id="an-det-pan" value="${o.pan || ''}" readonly tabindex="-1"></div>
              <div><label class="field-lbl" for="an-det-dob">DOB</label><div class="dob"><input class="input readonly" id="an-det-dob" value="${o.pan ? PAN_DETAILS[o.pan].dob : ''}" readonly tabindex="-1"><span>${ICON.calendar}</span></div></div>
              <div><label class="field-lbl" for="an-det-name">Name as per PAN</label><input class="input readonly" id="an-det-name" value="${o.pan ? PAN_DETAILS[o.pan].name : ''}" readonly tabindex="-1"></div>
            </div>
          </div>
        </div>

        <div class="an-new" id="an-new" ${o.mode === 'new' ? '' : 'hidden'}>
          <h5>PAN Details</h5><p class="sub">Please verify your PAN to get the best loan offers</p>
          <label class="field-lbl">Mobile Number</label><input class="input readonly" value="${store.get(K.mobile) || CUSTOMER.mobile}" readonly>
          <label class="field-lbl" for="np-name">Name as per PAN</label><input class="input" id="np-name" maxlength="100" autocomplete="off">
          <p class="field-err" id="np-name-err"></p>
          <label class="field-lbl" for="np-dob">DOB</label><div class="dob"><input class="input" id="np-dob" placeholder="DD/MM/YYYY" maxlength="10" inputmode="numeric" autocomplete="off"><span>${ICON.calendar}</span></div>
          <p class="field-err" id="np-dob-err"></p>
          <label class="field-lbl" for="np-pan">PAN Number</label><input class="input" id="np-pan" placeholder="ABCDE1234F" maxlength="10" autocomplete="off">
          <p class="field-err" id="np-pan-err"></p>
          <button class="btn btn-primary bold btn-block" data-cta="verify-pan">Verify PAN</button>
          <p class="an-ok" id="np-ok" hidden><span>${ICON.check}</span>PAN verified successfully</p>
        </div>

      </section>

      <section class="an-sec an-personal" id="an-bank" ${o.pan ? '' : 'hidden'}>
        <h4>Bank details</h4>
        <div class="an-ro an-ro3">
          <div><label class="field-lbl" for="an-bank-holder">Account holder name</label><input class="input readonly" id="an-bank-holder" value="${o.pan ? PAN_DETAILS[o.pan].bank.holder : ''}" readonly tabindex="-1"></div>
          <div><label class="field-lbl" for="an-bank-acc">Account number</label><input class="input readonly" id="an-bank-acc" value="${o.pan ? PAN_DETAILS[o.pan].bank.account : ''}" readonly tabindex="-1"></div>
          <div><label class="field-lbl" for="an-bank-ifsc">IFSC code</label><input class="input readonly" id="an-bank-ifsc" value="${o.pan ? PAN_DETAILS[o.pan].bank.ifsc : ''}" readonly tabindex="-1"></div>
        </div>
      </section>

      ${etbSection('an-personal', 'Personal details', `
        <div class="an-ro an-ro3"><div><label class="field-lbl" for="an-det-email">Email ID</label><input class="input readonly" id="an-det-email" value="${o.pan ? PAN_DETAILS[o.pan].email : ''}" readonly tabindex="-1"></div><div><label class="field-lbl" for="an-det-mobile">Mobile Number</label><input class="input readonly" id="an-det-mobile" value="${store.get(K.mobile) || CUSTOMER.mobile}" readonly tabindex="-1"></div></div>
        <div class="an-ro an-ro3">${CD_FIELDS.personal.map((f) => etbField(o.pan, f, ETB_EDIT.includes(f[0]))).join('')}</div>`, o.pan)}
      ${etbSection('an-other', 'Other details', `
        <div class="an-ro an-ro3">${CD_FIELDS.other.map((f) => etbField(o.pan, f, true)).join('')}</div>
        <div class="an-decl">
          <label class="chk cd-chk"><input type="checkbox" data-pf="pep" ${o.pan && PROFILE[o.pan].pep ? 'checked' : ''}><span>I am not a politically exposed person</span></label>
          <label class="chk cd-chk"><input type="checkbox" data-pf="tax" ${o.pan && PROFILE[o.pan].tax ? 'checked' : ''}><span>I am a tax resident of India only</span></label>
          <p class="field-err" data-pf-err="decl"></p>
        </div>`, o.pan)}
      ${etbSection('an-address', 'KYC Address', `
        <div class="an-ro an-ro3">${CD_FIELDS.address.map((f) => etbField(o.pan, f, false)).join('')}</div>`, o.pan)}


      <div class="an-consent" id="an-consent" hidden>
        <label class="chk sm"><input type="checkbox" id="mfc-consent"><span>${MFC_CONSENT}</span></label>
        <p class="field-err" id="an-err"></p>
        <button class="btn btn-disabled btn-block" data-cta="continue">Continue</button>
      </div>
    </div></div></main>`;

  /* 05 LOS → MF Central redirect popup (countdown 3, 2, 1) */
  T.mfcModal = () => `
    <div class="modal m-mfc">${closeBtn}
      ${img('mfcentral-logo.png', 'mfc-logo')}
      <p class="redir">Redirecting to MF Central in <span id="mfc-count">3</span> seconds</p>
      <div class="prog"><span></span></div>
      <h4>Here’s what you need to do</h4>
      <div class="todo"><span>1</span><p>Enter the 6-digit OTP received from MF Central on your mobile number.</p></div>
      <div class="todo"><span>2</span><p>Select all the AMCs and continue</p></div>
      <div class="note"><b>Note</b> You’ll return to the process automatically after completing this step.</div>
    </div>`;

  /* 06 MF Central mock (stands in for the MF Central OTP page) */
  T.mfMock = () => `
    ${plainHeader()}
    <main><div class="card mock-card">
      <h2>Mock MFCentral Page</h2><h4>Enter Otp</h4>
      <div class="otp" style="justify-content:center">${'<input maxlength="1" inputmode="numeric" autocomplete="off">'.repeat(6)}</div>
      <p class="otp-hint" style="margin:12px auto 0">Please use OTP <b>${OTP_RULES.demoOtp}</b> to proceed</p>
      <p class="field-err" id="mock-err" style="text-align:center"></p>
      <button class="btn btn-disabled btn-block" data-cta="submit">Submit</button>
    </div></main>`;

  /* 15 / 16 KYC mocks (stand in for DigiLocker and the photo check): Success / Failure to try both outcomes */
  T.kycMock = (kind) => {
    const dl = kind === 'aadhaar';
    return `
    ${plainHeader()}
    <main><div class="card mock-card kyc-mock">
      ${dl ? img('digilocker-logo.png', '', 'height:34px;display:block;margin:0 auto 10px') : ''}
      <h2>${dl ? 'Mock DigiLocker Page' : 'Mock Photo Verification Page'}</h2>
      <h4>${dl ? 'Aadhaar verification' : 'Photo verification'}</h4>
      <p class="mock-p">Prototype only: choose the result to see how the journey continues.</p>
      <div class="mock-2btn">
        <button class="btn btn-primary bold" data-cta="mock-success">Success</button>
        <button class="btn btn-outline" data-cta="mock-failure">Failure</button>
      </div>
    </div></main>`;
  };

  /* 07 MF Central → LOS redirecting */
  T.redirecting = () => `${plainHeader()}<p class="redirecting">Redirecting to Dashboard...</p>`;

  /* 08 / 09 loaders (skeleton + title), shown over the Your loans page */
  T.loader = (title, variant = 1) => {
    const bar2 = variant === 1 ? '<span class="skel-bar" style="width:113px"></span><span class="skel-bar" style="width:139px"></span>'
      : variant === 2 ? '<span class="skel-bar" style="width:76px"></span><span class="skel-bar" style="width:2px"></span>'
      : '<span class="skel-bar" style="width:119px"></span><span class="skel-bar" style="width:66px"></span>';
    return `<div class="modal loader-modal"><div class="skel">
      <div class="skel-row" style="margin-left:22px"><span class="skel-sq" style="width:44px;height:44px"></span><div style="display:grid;gap:9px"><span class="skel-bar" style="width:90px"></span><span class="skel-bar" style="width:107px"></span></div></div>
      <div class="skel-row dark"><span class="skel-sq" style="width:56px;height:56px"></span><div style="display:grid;gap:12px">${bar2}</div></div>
      </div><h3>${title}</h3><p>This might take a min, thanks for your patience</p></div>`;
  };

  /* 11 Curated offers (same as the new-customer journey's screen 12) */
  T.curated = (o = {}) => `
    ${plainHeader()}
    <div class="info-banner">${img('banner-icon.png')}${o.banner || 'Borrow only what you need and pay interest only on the utilised amount'}</div>
    <main class="wrap-980 curated">
      <h3 class="co-t">Curated offers for you</h3>
      <p class="co-s">Processing fee and monthly EMI shown are indicative. Final values will depend on the actual loan amount availed.</p>
      <div class="offer ${o.dropoff ? 'drop' : ''}">
        ${o.dropoff ? '<div class="offer-prog">1/4 Complete your application to get cash</div>' : ''}
        <div class="offer-in">
          <div class="offer-row"><span class="ol">Credit Limit</span><a class="ov" data-cta="how-calculated">${rs(PORTFOLIO.creditLimit)}</a></div>
          <div class="offer-grid">
            <div><span>Interest Rate</span><u>${PORTFOLIO.interest}</u></div>
            <div style="text-align:center"><span>Processing Fee</span><u>${rs(PORTFOLIO.fee)}</u></div>
            <div style="text-align:right"><span>Tenure in Months</span><u>${PORTFOLIO.tenure}</u></div>
          </div>
        </div>
        ${o.dropoff ? `<div class="offer-2btn"><button class="discard" data-cta="discard">Discard</button><button class="btn-primary" data-cta="continue">Continue</button></div>`
                    : `<button class="offer-btn" data-cta="start-application">Start Application</button>`}
      </div>
      <p class="tpv">Total Portfolio Value <span>${rs(PORTFOLIO.total)}</span></p>
      <p class="lu">Last updated: ${PORTFOLIO.lastUpdated} <a class="rf" data-cta="refresh-portfolio"><span>${ICON.refresh}</span>Refresh portfolio</a></p>
      <div class="mobile-strip"><span>${CUSTOMER.mobileMasked2}</span><span>13 Security<span class="dotsep">•</span>${rs(PORTFOLIO.total)}</span></div>
      ${FUNDS.map(offerCard).join('')}
    </main>`;

  /* 12 MF Selection (same as the new-customer journey's 13.2 / 13.5 / 13.6, made interactive).
     o = {loan, sliderPct, editLoan, loanErr, mv, count, selected:{id:amt}, editing:{id:val}, fundErr:{id:msg}, allState, ctaDisabled, cta} */
  const SEL_ORDER = ['icici', 'axis', 'kotak', 'nippontw', 'whiteoak', 'hsbc', 'ednifty', 'canara', 'sbi'];
  T.selection = (o = {}) => {
    const sel = o.selected || {};
    const all = o.allState || 'part';
    return `
    <div class="sticky-top">${plainHeader()}${stepper(1)}</div>
    <main class="wrap sel-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <div class="loan-box">
        <p class="lb-t">Loan Amount</p>
        ${o.editLoan != null
          ? `<div class="lb-edit"><span class="rs">₹</span><input id="loan-in" value="${o.editLoan}" inputmode="numeric" maxlength="9" autocomplete="off"><a class="link-yellow" data-cta="update-loan">Update</a></div>`
          : `<p class="lb-v">${rs(o.loan || '2,00,00,000')} <a class="pen" data-cta="edit-loan" title="Edit loan amount">${ICON.pencilSolid}</a></p>`}
        <p class="field-err lb-err" id="loan-err">${o.loanErr || ''}</p>
        <div class="slider"><div class="track" id="loan-track"><span class="fill" style="width:${o.sliderPct ?? 100}%"></span><span class="knob" style="left:${o.sliderPct ?? 100}%"></span></div>
          <div class="ends"><span>${rs('10,000')}</span><span>${rs('2,00,00,000')}</span></div></div>
      </div>
      <h2 class="fs-t">Funds selected for pledging</h2>
      <p class="fs-s">Current market value of units selected for pledging <b>${rs(o.mv || '2,66,66,667.21')}</b> <span class="gap"></span>No. of funds selected <b>${o.count ?? 3}</b></p>
      <label class="sel-all" data-cta="select-all"><span class="cbx ${all === 'all' ? 'on' : all === 'part' ? 'part' : ''}">${all === 'all' ? ICON.check : all === 'part' ? '<i></i>' : ''}</span>Select All</label>
      <div class="mobile-strip"><span>${CUSTOMER.mobileMasked2}</span><span>9 Fund<span class="dotsep">•</span>${rs(PORTFOLIO.eligible)}</span></div>
      ${SEL_ORDER.map((id) => selectCard(F[id], { checked: id in sel || (o.editing && id in o.editing), amount: sel[id], editing: o.editing && o.editing[id], err: o.fundErr && o.fundErr[id] })).join('')}
      <div style="height:30px"></div>
    </main>
    <div class="cta-bar"><button class="btn ${o.ctaDisabled ? 'btn-disabled' : 'btn-primary'}" data-cta="continue-to-apply">Continue to apply ${rs(o.cta || '2,00,00,000')}</button></div>`;
  };
  const SEL_DEFAULT = { selected: { icici: '1,40,30,794', axis: '53,69,420', kotak: '5,99,786' } };
  /* 13 Loan application summary (same layout as the new-customer journey's 14). Figures follow the
     loan amount chosen on screen 12 (reference values: ₹ 1,55,36,100): pledge value = amount ÷ 75% LTV,
     monthly interest = amount × 10.5% ÷ 12, processing fee = 0.5% of amount (rounded) + 18% GST; other charges fixed. */
  T.summary = (amount = 15536100) => {
    const f0 = (n) => Math.round(n).toLocaleString('en-IN');
    const f2 = (n) => n.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return `
    <div class="sticky-top">${plainHeader()}${stepper(1)}</div>
    <main class="wrap sum-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <div class="wrap-840 sum">
        <h3>Application details</h3>
        <div class="sum-box"><div><span>Loan amount</span><b>${rs(f0(amount))}</b></div><div style="text-align:right"><span>Pledge Value</span><b>${rs(f2(amount / 0.75))}</b></div></div>
        <div class="kv big"><b>Tenure</b><span>12 months</span></div>
        <div class="kv big"><b>Disbursement Type</b><span>Multiple</span></div>
        <div class="kv big"><b>Repayment Type</b><span>Interest Only</span></div>
        <div class="sum-2"><div><span>Interest Rate ${i()}</span><em>10.5% p.a</em></div><div><span>Monthly Interest ${i()}</span><em>${rs(f2((amount * 0.105) / 12))}</em></div></div>
        <h3>Charges (Inclusive of GST)</h3>
        <div class="kv"><span class="g">Processing fee ${i()}</span><em>${rs(f0(Math.round(Math.round(amount * 0.005) * 1.18)))}</em></div>
        <div class="kv"><span class="g">Stamp duty ${i()}</span><span>${rs('236')}</span></div>
        <div class="kv"><span class="g">Lien Marking Charges ${i()}</span><span>${rs('531')}</span></div>
        <div class="kv"><span class="g">Lien Removal Charges ${i()}</span><span>${rs('118')}</span></div>
        <h3>Repayment details</h3>
        <div class="kv"><span class="g">Interest autopay</span><span>5th of every month</span></div>
      </div>
      <div style="height:30px"></div>
    </main>
    <div class="cta-bar"><button class="btn btn-primary" style="width:178px" data-cta="continue">Continue</button></div>`;
  };

  /* 14 KYC (same as the new-customer journey's 16.1 – 16.5.9). o = {email:'input'|'filled'|'done', aadhaar:'pending'|'start'|'status'|'done', photo:'pending'|'start'|'done', aadErr, photoErr} */
  const kycRow = (n, title, state, extra = '') => {
    const done = state === 'done';
    if (state === 'openPending') {     // current step, still pending, with its action (Agreement & E-Mandate)
      return `<div class="kyc-row open"><div class="kyc-h"><span class="kn act">${n}</span><span class="kt">${title}</span><span class="badge pending">Pending</span></div>${extra}</div>`;
    }
    if (state === 'doneOpen') {        // complete, but its details stay visible (Bank Details for an existing PAN)
      return `<div class="kyc-row open"><div class="kyc-h"><span class="kn act">${n}</span><span class="kt">${title}</span><span class="badge complete">Complete</span></div>${extra}</div>`;
    }
    const badge = state === 'done' ? '<span class="badge complete">Complete</span>' : state === 'pending' ? '<span class="badge pending">Pending</span>' : '';
    return `<div class="kyc-row ${state === 'pending' || done ? '' : 'open'}">
      <div class="kyc-h"><span class="kn ${done ? 'done' : state !== 'pending' ? 'act' : ''}">${done ? ICON.check : n}</span><span class="kt">${title}</span>${badge}</div>${extra}</div>`;
  };
  const DL = img('digilocker-logo.png', 'dl-inline');
  T.kyc = (o = {}) => {
    const loan = o.loan || '1,55,36,100';                    // loan amount chosen on screen 12
    const email = o.email || 'input';
    const aad = o.aadhaar || 'pending';
    const photo = o.photo || 'pending';
    const emailExtra = email === 'done' ? '' : `
      <input class="input kyc-in ${email === 'filled' ? 'autofill' : ''}" value="${email === 'filled' ? CUSTOMER.email : ''}">
      <p class="kyc-note">We will use this email address for all official communications related to your loan application and account.</p>
      <button class="btn btn-primary bold kyc-btn" data-cta="verify-email">Verify</button>`;
    const aadExtra = aad === 'start' ? `<button class="btn btn-primary bold kyc-btn" data-cta="start-kyc">Start KYC</button>`
      : aad === 'status' ? `<button class="btn kyc-btn status-btn"><b>Getting status</b><small>This might take up to 2m:58s</small></button>
          <p class="kyc-italic">Your Aadhaar details are being fetched from DigiLocker. This process may take a few minutes. Please keep this tab open and avoid refreshing the page.</p>` : '';
    const photoExtra = photo === 'start' ? `<button class="btn btn-primary bold kyc-btn sm" data-cta="start-photo">Start</button>` : '';
    const failNote = (msg) => (msg ? `<p class="field-err kyc-fail">${msg}</p>` : '');
    return `
    <div class="sticky-top">${plainHeader()}${stepper(2)}</div>
    <main class="wrap kyc-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <div class="loan-strip">Your loan amount is ${rs(loan)} <a class="link-yellow sm" data-cta="view-details">View details</a></div>
      <h1 class="kyc-title">KYC Verification <small>This step is required as per our lending guidelines.</small></h1>
      ${kycRow(1, 'Email Verification', email === 'done' ? 'done' : 'open', emailExtra)}
      ${kycRow(2, 'PAN Verification', 'done')}
      ${kycRow(3, 'Aadhaar Verification with ' + DL, aad === 'done' ? 'done' : aad === 'pending' ? 'pending' : 'open', aadExtra + failNote(o.aadErr))}
      ${kycRow(4, 'Photo Verification', photo === 'done' ? 'done' : photo === 'start' ? 'open' : 'pending', photoExtra + failNote(o.photoErr))}
      ${o.bank
        ? kycRow(5, 'Bank Details', 'doneOpen', `<div class="kyc-bank">${o.bank.logo ? img(o.bank.logo, 'kb-logo') : `<span class="kb-logo kb-gen">${ICON.bank}</span>`}<span>${o.bank.name} <span class="kb-n">${o.bank.account.slice(-4)}</span></span><b>IFSC</b><span class="kb-n">${o.bank.ifsc}</span><span class="kb-ok">${ICON.check}</span></div>`)
        : kycRow(5, 'Bank Details', 'pending')}
      ${o.cont ? `<button class="btn ${o.cont === 'on' ? 'btn-primary' : 'btn-disabled'} bold kyc-btn kyc-cont" data-cta="kyc-continue">Continue</button><p class="field-err kyc-fail" id="kyc-cont-err"></p>` : ''}
    </main>`;
  };

  /* 17 Customer details (after KYC, existing PAN): Personal Details, Other Details, KYC Address.
     Values come from the existing record (PROFILE) and can be corrected before Confirm and Continue.
     Name, DOB, Gender and the KYC address are shown as text (from KYC), as in the shared screenshot. */
  const CD_OPTIONS = {
    salutation: ['Mr', 'Mrs', 'Ms', 'Dr'],
    marital: ['Single', 'Married', 'Divorced', 'Widowed'],
    purpose: ['Home Renovation', 'Education', 'Medical', 'Business', 'Travel', 'Wedding', 'Personal Use', 'Others'],
    qualification: ['Below High School', 'High School', 'Graduate', 'Post Graduate', 'Professional', 'Others'],
    occupation: ['Salaried', 'Self Employed Professional', 'Self Employed Business', 'Retired', 'Homemaker', 'Student', 'Others'],
    business: ['Agriculture', 'Manufacturing', 'Trading', 'Services', 'Information Technology', 'Others'],
    income: ['Up to Rs. 5 Lakhs', 'Rs. 5 - 10 Lakhs', 'Rs. 10 - 25 Lakhs', 'Rs. 25 Lakhs - 1 Crore', 'Above Rs. 1 Crore'],
    source: ['Salary', 'Business Income', 'Rental Income', 'Investments', 'Agriculture', 'Others'],
    independent: ['Yes', 'No'],
  };
  const CD_FIELDS = {       // key → [label, type]  (type: select | text | show)
    personal: [['salutation', 'Salutation', 'select'], ['name', 'Name', 'show'], ['dob', 'Date of Birth', 'show'], ['gender', 'Gender', 'show'],
      ['mother', 'Mother’s Name', 'show'], ['father', 'Father’s Name', 'show'], ['marital', 'Marital Status', 'select']],
    other: [['purpose', 'Loan Purpose', 'select'], ['qualification', 'Qualification', 'select'], ['occupation', 'Occupation', 'select'], ['business', 'Nature of Business', 'select'],
      ['income', 'Annual Income', 'select'], ['source', 'Source of Income', 'select'], ['independent', 'Is the applicant financially independent?', 'select']],
    address: [['addr1', 'Address Line 1', 'show'], ['addr2', 'Address Line 2', 'show'], ['addr3', 'Address Line 3', 'show'], ['landmark', 'Landmark', 'show'],
      ['pincode', 'Pincode', 'show'], ['city', 'City', 'show']],
  };
  const cdField = (p, [key, label, type]) => {
    const v = p[key] || '';
    if (type === 'show') return `<div class="cd-f"><span class="cd-l">${label}</span><p class="cd-v">${v}</p></div>`;
    const input = type === 'select'
      ? `<select class="input cd-in an-select" data-k="${key}"><option value="">Select</option>${CD_OPTIONS[key].map((o) => `<option ${o === v ? 'selected' : ''}>${o}</option>`).join('')}</select>`
      : `<input class="input cd-in" data-k="${key}" value="${v}" maxlength="60" autocomplete="off">`;
    return `<div class="cd-f"><label class="cd-l">${label}<i>*</i></label>${input}<p class="field-err" data-err="${key}"></p></div>`;
  };
  const cdSection = (id, title, body) => `
    <section class="cd-sec open" data-sec="${id}">
      <button class="cd-h" data-toggle="${id}"><span class="kn done">${ICON.check}</span><span class="kt">${title}</span><span class="cd-chev">${ICON.chev}</span></button>
      <div class="cd-body">${body}</div>
    </section>`;
  T.custDetails = (p = PROFILE.CBOPA8195B, loan = '1,55,36,100') => `
    <div class="sticky-top">${plainHeader()}${stepper(2)}</div>
    <main class="wrap kyc-page cd-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <div class="loan-strip">Your loan amount is ${rs(loan)} <a class="link-yellow sm" data-cta="view-details">View details</a></div>
      ${cdSection('personal', 'Personal Details', `<div class="cd-grid">${CD_FIELDS.personal.map((f) => cdField(p, f)).join('')}</div>`)}
      ${cdSection('other', 'Other Details', `<div class="cd-grid">${CD_FIELDS.other.map((f) => cdField(p, f)).join('')}</div>
        <label class="chk cd-chk"><input type="checkbox" data-k="pep" ${p.pep ? 'checked' : ''}><span>I am not a politically exposed person ${i()}</span></label>
        <label class="chk cd-chk"><input type="checkbox" data-k="tax" ${p.tax ? 'checked' : ''}><span>I am a tax resident of India only</span></label>
        <p class="field-err" data-err="decl"></p>`)}
      ${cdSection('address', 'KYC Address', `<div class="cd-grid">${CD_FIELDS.address.map((f) => cdField(p, f)).join('')}</div>`)}
      <div class="cd-cta"><button class="btn btn-primary bold" data-cta="confirm-continue">Confirm and Continue</button></div>
    </main>`;

  /* 18 Pledging of Mutual Fund (stepper step 3). o = {loan, pledge, mobile, status:'pending'|'pledged'} */
  const maskMobile2 = (m) => (m && m.length === 10 ? `+91${m[0]}XXXX${m.slice(6)}` : CUSTOMER.mobileMasked2);
  T.pledge = (o = {}) => `
    <div class="sticky-top">${plainHeader()}${stepper(3)}</div>
    <main class="wrap pl-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <h3 class="pl-t">Please review and confirm the following details</h3>
      <div class="pl-sum"><div><span>Loan Amount</span><b>${rs(o.loan || '2,00,00,000')}</b></div><div><span>Total Pledge Value</span><b>${rs(o.pledge || '2,66,66,666.67')}</b></div></div>
      <div class="pl-card">
        <div class="pl-row">
          <span class="pl-logo">${img('mfcentral-logo.png')}</span>
          <div><p class="pl-n">MF Central</p><p class="pl-v">Value of Securities <b>${rs(o.pledge || '2,66,66,666.67')}</b></p></div>
          <span class="pl-badge ${o.status === 'pledged' ? 'ok' : ''}">${o.status === 'pledged' ? 'Pledged' : 'Pending'}</span>
        </div>
        <div class="pl-btns">
          <button class="pl-view" data-cta="view-securities">View Securities</button>
          ${o.status === 'pledged'
            ? '<button class="pl-go done" disabled>Pledged</button>'
            : '<button class="pl-go" data-cta="pledge-securities">Pledge Securities</button>'}
        </div>
      </div>
      <p class="pl-otp-note">An OTP will be sent to ${o.mobile || CUSTOMER.mobileMasked2}</p>
    </main>`;

  /* 19 Agreement & E-Mandate (stepper step 4) */
  T.agreement = (signed = false, em = '') => `
    <div class="sticky-top">${plainHeader()}${stepper(4)}</div>
    <main class="wrap kyc-page ag-page">
      ${signed ? kycRow(1, 'Loan Agreement', 'done') : kycRow(1, 'Loan Agreement', 'openPending', '<button class="btn btn-primary bold kyc-btn" data-cta="sign-agreement">Sign Agreement</button>')}
      ${!signed ? kycRow(2, 'E-Mandate', 'pending')
        : em === 'done' ? kycRow(2, 'E-Mandate', 'done')
        : kycRow(2, 'E-Mandate', 'openPending', `<button class="btn btn-primary bold kyc-btn" data-cta="setup-emandate">Set up E-Mandate</button>${em === 'failed' ? '<p class="field-err kyc-fail">E-Mandate was not authenticated. Please try again.</p>' : ''}`)}
    </main>`;

  /* 18.1 Pledge OTP popup (MF Central OTP; demo OTP 000000) */
  T.pledgeOtpModal = (mobile) => `
    <div class="modal m-otp m-plotp">${closeBtn}
      <h3>Enter OTP to pledge your Mutual Fund</h3>
      <p class="sent">OTP has been sent by MF Central to <b>${mobile || CUSTOMER.mobileMasked2}</b></p>
      <div class="otp">${'<input maxlength="1" inputmode="numeric" autocomplete="off">'.repeat(6)}</div>
      <p class="resend">Didn’t receive OTP? <span id="pl-resend"></span></p>
      <p class="otp-hint">Please use OTP <b>${OTP_RULES.demoOtp}</b> to proceed</p>
      <p class="field-err" id="pl-otp-err"></p>
      <button class="btn btn-primary bold btn-block" data-cta="submit-pledge-otp">Submit OTP</button>
    </div>`;

  /* 18.2 Successfully pledged popup */
  T.pledgedModal = () => `
    <div class="modal m-pledged">
      <span class="pl-tick"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#12A150"/><path d="M6.8 12.4l3.4 3.4 7-7" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <h3>Successfully pledged!</h3>
      <p>You will be redirected in <span id="pl-count">3</span> seconds.</p>
    </div>`;

  /* 20 Sanction letter (in-principle e-Sanction Letter + KFS, from the shared UAT PDF) and
     21 Loan agreement e-sign (Digio look-alike, prototype only). Figures follow the chosen loan. */
  const inWords = (n) => {
    const a = ['', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE', 'THIRTEEN', 'FOURTEEN', 'FIFTEEN', 'SIXTEEN', 'SEVENTEEN', 'EIGHTEEN', 'NINETEEN'];
    const b = ['', '', 'TWENTY', 'THIRTY', 'FORTY', 'FIFTY', 'SIXTY', 'SEVENTY', 'EIGHTY', 'NINETY'];
    const two = (x) => (x < 20 ? a[x] : `${b[Math.floor(x / 10)]}${x % 10 ? ' ' + a[x % 10] : ''}`);
    const parts = [[10000000, 'CRORE'], [100000, 'LAKH'], [1000, 'THOUSAND'], [100, 'HUNDRED']];
    let out = []; let r = Math.round(n);
    parts.forEach(([v, w]) => { const q = Math.floor(r / v); if (q) { out.push(`${two(q)} ${w}`); r %= v; } });
    if (r) out.push(two(r));
    return out.join(' ') || 'ZERO';
  };
  const today = () => { const d = new Date(); return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`; };
  const docFoot = `<div class="sl-foot"><b>SHRIRAM CREDIT COMPANY LIMITED</b><p>Regd. Office: Shriram House, No. 4, Burkit Road, T. Nagar, Chennai – 600017, Phone: 91-44-49052500/2501, Fax: 91-44-49052696/97</p><p>Corporate Office: No. 221, 3<sup>rd</sup> Floor, Thiru Vi Ka Salai, Royapettah High Road, Mylapore, Chennai-600004, Phone: 044-42983690</p><p><b>CIN: U65993TN1980PLC008215</b></p></div>`;
  T.sanction = (o = {}) => {
    const p = o.profile || PROFILE.CBOPA8195B;
    const amt = o.amount || 20000000;
    const r = (v) => `₹ ${v}`;
    return `
    <main class="sl-bg"><div class="sl-doc">
      <div class="sl-logo">${img('shriram-logo.png')}</div>
      <h1 class="sl-h">In principle e-Sanction Letter</h1>
      <p class="sl-date">${today()}</p>
      <p class="sl-name">${p.name}</p>
      <p class="sl-addr">${p.addr1},<br>${p.addr2},<br>${p.addr3}</p>
      <p class="sl-cid">Customer ID : ${o.customerId || 'A000000011'}</p>
      <p>Dear Sir/Madam,</p>
      <p><b>Reg: Your request for Financial Assistance of ${r(amt)}</b></p>
      <p>We are pleased to inform you that based on your online loan application, we are offering you an in-principle e-Sanction of loan against Mutual funds of ${r(amt)} for the purpose of "${p.purpose}" as per the terms and conditions given in Key Fact Statement (KFS). This credit facility will be available to you on execution of all the necessary documents and collateral pledge/lien mark in favor of SHRIRAM CREDIT COMPANY LIMITED.</p>
      <p>In case of any clarification, please do not hesitate to contact us at lassupport@shriramcredit.in</p>
      <p>Thank you, and we assure you of our best services at all times.</p>
      <p>Yours faithfully,<br><b>SHRIRAM CREDIT COMPANY LIMITED</b></p>
      ${docFoot}
      <h2 class="sl-h2">Annexure A: Key Fact Statement</h2>
      <p class="sl-sub">Part 1 – Interest rate and fees / charges</p>
      <table class="sl-t">
        <tr><th>Sr No</th><th>Parameter</th><th>Details</th></tr>
        <tr><td>1 (a)</td><td>Type of Loan</td><td>Loan Against pledge of Mutual Funds</td></tr>
        <tr><td>1 (b)</td><td>Loan proposal / Customer ID</td><td>${o.proposal || 'SCCLMF20260900155'} / ${o.customerId || 'A000000011'}</td></tr>
        <tr><td>2</td><td>Sanctioned Loan Amount (₹)</td><td>${r(amt)}</td></tr>
        <tr><td>3</td><td>Loan Term (months)</td><td>12 Months</td></tr>
        <tr><td>4</td><td>Instalment Details</td><td>Type of instalments: Monthly · Number of Dues: 12 Months<br>– Interest: 12 Months (Fixed) · – Principal: 1 (bullet at maturity)<br>Due: ${r(((amt * 0.105) / 12).toFixed(2))} · Commencement of repayment, post sanction (in days): 36</td></tr>
        <tr><td>5</td><td>Rate of Interest per annum (%) and type</td><td>10.5 % p.a. and Fixed</td></tr>
        <tr><td>6 (a)</td><td>Fees / charges payable to RE</td><td>Processing Fee: One-time | ${r(Math.round(amt * 0.005))} + GST<br>Loan Renewal Charges: Recurring | Annual | ₹ 999 + GST<br>Bank Swap Charges: Recurring | ₹ 250 + GST</td></tr>
        <tr><td>6 (b)</td><td>Payable to Third Party through RE</td><td>Lien Marking Charges: One-time | ₹ 450 + GST<br>Lien Removal Charges: Event-based | ₹ 100 + GST<br>Stamp Duty: One-time (As per State) | ₹ 200 + GST</td></tr>
        <tr><td>8</td><td>Purpose of Loan</td><td>${p.purpose}</td></tr>
      </table>
      ${docFoot}
    </div></main>
    <div class="sl-bar">
      <label class="sl-chk"><input type="checkbox" id="sl-accept"><span>I accept the terms of the Sanction letter and Key Fact Statement (KFS), including all applicable charges, interest rates, and repayment schedules. I confirm that I understand these conditions and agree to proceed with the loan agreement.</span></label>
      <button class="sl-submit" data-cta="sanction-submit" disabled>Submit</button>
    </div>`;
  };

  T.esign = (o = {}) => {
    const amt = o.amount || 20000000;
    return `
    <header class="dg-hdr"><span class="dg-logo"><b>d</b>igio</span><span class="dg-mock">Mock e-Sign page (prototype)</span></header>
    <main class="dg-bg"><div class="sl-doc dg-doc">
      <div class="sl-logo">${img('shriram-logo.png')}</div>
      <h1 class="sl-h dg-h">LOAN CUM PLEDGE AGREEMENT</h1>
      <p>This Agreement made on ${new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })}, between:</p>
      <p>(1) The Borrower the details where of are given at the end of the Agreement, (here in after called the "<b>Borrower</b>") of the First Part</p>
      <p><b>AND</b></p>
      <p>(2) Shriram Credit Company Limited., a Company incorporated under the Companies Act, 1956 having CIN No. U65993TN1980PLC008215 and having its registered office situated at Shriram House, No.4, Burkit Road, T.Nagar, Chennai, TamilNadu, 600017 having RBI registration number-B-07.00709, (here in after called "<b>SCCL</b> or the <b>Lender</b>") of the Third Part.</p>
      <p>(The expression 'Borrower and SCCL/ Lender' shall, unless repugnant to the context or meaning thereof be deemed to include their respective legal heirs, executors and administrators and shall be deemed to include his/her/its/their respective successors and permitted assigns in the case of the Borrower and its assigns in the case of SCCL/ Lender)</p>
      <p>(The expressions Borrower and SCCL shall hereinafter collectively be referred to as the "<b>Parties</b>" and individually as the "<b>Party</b>")</p>
      <p><b>WHEREAS</b> the Borrower being in need of funds has approached SCCL for a loan of Rs. ${amt} (Rupees ${inWords(amt)}) (hereinafter referred to as the "<b>Loan Facility</b>")</p>
      <p class="dg-more">… (remaining clauses of the agreement)</p>
    </div></main>
    <div class="dg-bar">
      <label class="dg-chk"><input type="checkbox" id="dg-accept" checked><span>1. By continuing, I agree to do eKyc using Aadhaar to eSign with one of ESPs (CVL or Emudra or Protean) Digio is registered as ASP<br>2. I confirm that ${o.mobile || '+91XXXXXXXXXX'} belongs to me and verified with <b>SHRIRAM CREDIT COMPANY LIMITED</b></span></label>
      <button class="dg-sign" data-cta="sign-now">Sign Now</button>
      <p class="dg-sec">Secured by <b>digio</b></p>
    </div>`;
  };

  /* 21.1 Digio Verify OTP popup (Aadhaar / VID + OTP; demo OTP 000000) */
  T.esignOtpModal = () => `
    <div class="overlay dg-ov"><div class="modal dg-otp">
      <h3>Verify OTP</h3>
      <input class="dg-in" id="dg-aadhaar" placeholder="Enter Aadhaar or VID" inputmode="numeric" maxlength="16" autocomplete="off">
      <p class="field-err" id="dg-aadhaar-err"></p>
      <div class="otp dg-boxes">${'<input maxlength="1" inputmode="numeric" autocomplete="off">'.repeat(6)}</div>
      <p class="otp-hint dg-hint">Please use OTP <b>${OTP_RULES.demoOtp}</b> to proceed</p>
      <p class="field-err" id="dg-otp-err"></p>
      <button class="dg-submit" data-cta="esign-submit-otp">Submit OTP</button>
    </div></div>`;

  /* 21.2 Digio exit page and 21.3 LOS "Agreement Signed successfully" */
  T.esignDone = () => `
    <span class="dg-mock dg-mock-fixed">Mock e-Sign page (prototype)</span>
    <main class="dg-exit">
      <svg viewBox="0 0 120 120" class="dg-exit-ico"><circle cx="60" cy="60" r="44" fill="#2E8B2E"/><rect x="41" y="38" width="38" height="46" rx="6" fill="#F4F7F4"/><path d="M48 58l8 8 16-17" stroke="#2E8B2E" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M50 72h20M52 77h16" stroke="#9AA59A" stroke-width="2.4" stroke-linecap="round"/><circle cx="18" cy="40" r="3" fill="#E4556B"/><circle cx="104" cy="44" r="3" fill="#4AA3E8"/><circle cx="96" cy="100" r="2.5" fill="#F2B233"/><circle cx="26" cy="92" r="2.5" fill="#8C6BE8"/></svg>
      <p class="dg-exit-t">Signed Successfully</p>
      <p class="dg-exit-s">Do not close the window. You will be redirected.</p>
    </main>`;
  T.agreementSigned = () => `
    <main class="ag-done">
      <svg viewBox="0 0 90 100" class="ag-done-ico"><circle cx="47" cy="10" r="6" fill="#7B5CF0"/><path d="M47 16v22" stroke="#999" stroke-width="1"/><circle cx="45" cy="42" r="5" fill="#222"/><path d="M45 47v22M45 55l-11 7M45 55l10-15M45 69l-8 20M45 69l8 20" stroke="#222" stroke-width="4" stroke-linecap="round"/><circle cx="22" cy="18" r="2" fill="#C9C1F5"/><circle cx="70" cy="22" r="2.5" fill="#C9C1F5"/><circle cx="28" cy="34" r="1.5" fill="#7B5CF0"/><circle cx="64" cy="38" r="1.5" fill="#7B5CF0"/></svg>
      <h4>Agreement Signed successfully.</h4>
      <p>Redirecting you back to the process in <span id="ag-count">3</span> seconds</p>
    </main>`;

  /* 22 E-Mandate (Digio look-alike, prototype): overview + bank on file + verification mode + consent */
  const fmtDate = (d) => d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  const titleCase = (t) => t.toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase());
  T.emandate = (o = {}) => {
    const bank = o.bank || PAN_DETAILS.CBOPA8195B.bank;
    const first = new Date(); const last = new Date(); last.setFullYear(last.getFullYear() + 1);
    const mode = (id, label, ico, on) => `<label class="em-mode ${on ? 'on' : ''}"><input type="radio" name="em-mode" value="${id}" ${on ? 'checked' : ''}><span class="em-ico">${ico}</span>${label}</label>`;
    return `
    <main class="em-bg"><div class="em-card">
      <header class="em-hdr"><span class="dg-logo"><b>d</b>igio</span><span class="dg-mock">Mock e-Mandate page (prototype)</span><span class="em-sec">Secured by <b>digio</b></span></header>
      <div class="em-body">
        <aside class="em-ov">
          <p class="em-ovt">Mandate Overview</p>
          <span>Maximum amount</span><b class="em-max">₹${(o.max || 10000000).toLocaleString('en-US', { minimumFractionDigits: 2 })}</b>
          <span>Frequency</span><p>Monthly</p>
          <span>Purpose</span><p>Loan instalment payment</p>
          <div class="em-val"><b>Validity</b>
            <div><span>First collection date</span><p>${fmtDate(first)}</p></div>
            <div><span>Last collection date</span><p>${fmtDate(last)}</p></div>
          </div>
        </aside>
        <section class="em-main">
          <div class="em-bank">
            <div class="em-bn">${bank.logo ? img(bank.logo) : `<span class="kb-gen">${ICON.bank}</span>`}<b>${bank.name.toUpperCase()} LTD</b></div>
            <span>Account Number</span><p class="em-acc"><b id="em-acc" data-full="${bank.account}">XXXX XXXX ${bank.account.slice(-4)}</b><a class="em-eye" data-cta="em-eye" title="Show / hide">👁</a></p>
            <span>Customer Name (As per bank account)</span><p><b>${titleCase(bank.holder)}</b></p>
            <div class="em-2"><div><span>IFSC code</span><p><b>${bank.ifsc}</b></p></div><div style="text-align:right"><span>A/C Type</span><p><b>Savings</b></p></div></div>
          </div>
          <div class="em-modes">
            <h4>Select Verification Mode</h4>
            <p>The following options are available to you on the given account:</p>
            ${mode('debit', 'Debit Card', '💳', true)}${mode('netbanking', 'Net Banking', '🏦', false)}${mode('aadhaar', 'Aadhaar', '🆔', false)}
          </div>
        </section>
      </div>
      <label class="em-chk"><input type="checkbox" id="em-accept"><span>I hereby authorize <em>SHRIRAM CREDIT COMPANY LIMITED</em> to <em>debit</em> my Bank account, as per the mentioned mandate and bank account details. I understand that the bank where I have authorised the debit may levy mandate processing charges as mentioned in the bank's latest schedule of charges.</span></label>
      <div class="em-foot"><button class="em-submit" data-cta="em-submit" disabled>Submit</button></div>
    </div></main>`;
  };
  /* 22.1 NPCI simulation (Digio sandbox look-alike) */
  T.npci = (txn = 'MMI000000000000000000000000') => `
    <main class="np">
      <h2>NPCI Simulation</h2><p>(This is a simulation of request to NPCI)</p>
      <p class="np-id">Transaction ID <span id="np-txn">${txn}</span></p>
      <div class="np-btns"><button class="np-acc" data-cta="npci-accept">Accept</button><button class="np-rej" data-cta="npci-reject">Reject</button></div>
    </main>`;
  /* 22.2 Digio exit – mandate authenticated */
  T.emandateDone = () => `
    <span class="dg-mock dg-mock-fixed">Mock e-Mandate page (prototype)</span>
    <main class="dg-exit">
      <svg viewBox="0 0 100 100" class="em-ok"><circle cx="50" cy="50" r="44" fill="#2ECC71"/><path d="M30 51l13 13 27-28" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <p class="dg-exit-t">Mandate authenticated successfully.</p>
      <p class="dg-exit-s">Please share your feedback</p><p class="dg-exit-s">You may close the window.</p>
    </main>`;
  /* 23 Loan application submitted (LOS) */
  T.submitted = (o = {}) => {
    const amt = o.amount || 20000000;
    const row = (l, v, sub = '') => `<div class="sb-row"><div><span>${l}</span>${sub ? `<small>${sub}</small>` : ''}</div><b>${v}</b></div>`;
    return `
    ${plainHeader()}
    <main class="wrap sb-page">
      <h2 class="sb-t"><span class="sb-tick"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#12A150"/><path d="M6.8 12.4l3.4 3.4 7-7" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>Your loan application has been submitted</h2>
      <div class="sb-card">
        ${row('Loan Amount', rs(inr(amt)))}
        ${row('Mutual Fund Value Pledged', rs(inr(amt / LTV)))}
        ${row('Interest Rate', '10.5% p.a.')}
        ${row('Tenure', '12 Months', '(No foreclosure charges)')}
        ${row('Processing Fee (inclusive of taxes)', rs(inr(Math.round(Math.round(amt * 0.005) * 1.18))), 'Will be deducted at the time of first withdrawal')}
        ${row('Repayment Type', 'Interest Only')}
        ${row('Disbursement Type', 'Multiple')}
      </div>
      <div class="sb-cta"><button class="btn btn-primary bold" data-cta="view-loan">View loan details</button></div>
    </main>`;
  };

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
    '04) Your Loans Page': {
      'apply-new-loan': '04.1) Apply for New Loan Page',
    },
    '11) Curated Offers Page': {
      'start-application': '12) Mutual Fund Selection Page',
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
  const K = { mobile: 'lamfec.mobile', otp: 'lamfec.otp', pan: 'lamfec.pan', sel: 'lamfec.sel', mode: 'lamfec.mode', kyc: 'lamfec.kyc', profile: 'lamfec.profile', pledge: 'lamfec.pledge', agreement: 'lamfec.agreement', emandate: 'lamfec.emandate', emMode: 'lamfec.emMode' };
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
    demoOtp: '000000',        // until the OTP vendor is integrated, only this OTP is accepted
  };
  const OTP_ERR = {
    chars: 'Only numbers are allowed. Letters, spaces and special characters cannot be entered.',
    incomplete: 'Please enter the 6-digit OTP.',
    consent: 'Please provide the consent to proceed.',
    wrong: (left) => `The OTP you entered is incorrect. Please try again. ${left} attempt${left === 1 ? '' : 's'} remaining.`,
    resendBlocked: (m) => `You have used all ${OTP_RULES.maxResend} OTP resend attempts. Please try again after ${m} minute${m === 1 ? '' : 's'}.`,
    wrongBlocked: (m) => `You have entered an incorrect OTP ${OTP_RULES.maxWrong} times. Please try again after ${m} minute${m === 1 ? '' : 's'}.`,
  };

  const AN_ERR = {
    mode: 'Please select Use Existing PAN or Apply with New PAN.',
    pan: 'Please select PAN.',
    verify: 'Please verify your PAN to continue.',
    consent: 'Please provide the consent to proceed.',
    details: 'Please complete the highlighted details.',
    name: 'Please enter your name as per PAN.',
    nameChars: 'Only letters, spaces and dots are allowed.',
    dob: 'Please enter a valid date of birth (DD/MM/YYYY).',
    age: 'You must be at least 18 years old to apply.',
    panFormat: 'Please enter a valid PAN (e.g. ABCDE1234F).',
    panLinked: 'This PAN is already linked to your account. Please choose Use Existing PAN.',
    panMax: `You can link at most ${MAX_PANS} PANs to one mobile number.`,
  };

  /* 04.1 – 04.3 Apply for New Loan page: Existing PAN (dropdown → details) or New PAN
     (verify) → MF Central consent → Continue → MF Central redirection (05) */
  const applyNewBehaviour = () => {
    const $ = (id) => document.getElementById(id);
    const opts = [...document.querySelectorAll('.an-opt')];
    const pan = $('an-pan'), cta = document.querySelector('[data-cta="continue"]'), consent = $('mfc-consent');
    const name = $('np-name'), dob = $('np-dob'), newPan = $('np-pan');
    let mode = (opts.find((b) => b.classList.contains('on')) || {}).dataset?.mode || '';
    let verified = false;
    let shownPan = '';                                       // PAN whose details are on screen
    const err = (id, msg, input) => { $(id).textContent = msg || ''; if (input) input.classList.toggle('has-err', !!msg); };

    const ready = () => (mode === 'existing' && !!pan.value) || (mode === 'new' && verified);
    const sync = () => {
      opts.forEach((b) => b.classList.toggle('on', b.dataset.mode === mode));
      $('an-existing').hidden = mode !== 'existing';
      $('an-new').hidden = mode !== 'new';
      $('an-details').hidden = !(mode === 'existing' && pan.value);
      if (pan.value && pan.value !== shownPan) {             // existing details of the newly chosen PAN
        shownPan = pan.value;
        $('an-det-pan').value = pan.value;
        $('an-det-dob').value = PAN_DETAILS[pan.value].dob;
        $('an-det-name').value = PAN_DETAILS[pan.value].name;
        $('an-det-email').value = PAN_DETAILS[pan.value].email;
        // record of the previous loan, with any changes the customer already made for this PAN on top
        const prof = store.get(K.profile);
        const rec = { ...PROFILE[pan.value], ...(prof && prof.pan === pan.value ? prof.edits : {}) };
        document.querySelectorAll('[data-pf]').forEach((f) => { const v = rec[f.dataset.pf]; if (f.type === 'checkbox') f.checked = !!v; else f.value = v; });
        document.querySelectorAll('[data-pf-err]').forEach((e) => { e.textContent = ''; });
        const bk = PAN_DETAILS[pan.value].bank;
        $('an-bank-holder').value = bk.holder; $('an-bank-acc').value = bk.account; $('an-bank-ifsc').value = bk.ifsc;
      }
      const showDetails = mode === 'existing' && !!pan.value;          // details held for the existing PAN
      ['an-personal', 'an-other', 'an-address', 'an-bank'].forEach((id) => { $(id).hidden = !showDetails; });
      $('an-consent').hidden = !ready();                     // consent only after a PAN is selected / verified
      if (!ready()) consent.checked = false;
      const ok = ready() && consent.checked;
      cta.classList.toggle('btn-primary', ok);
      cta.classList.toggle('bold', ok);
      cta.classList.toggle('btn-disabled', !ok);
    };

    opts.forEach((b) => b.addEventListener('click', () => { mode = b.dataset.mode; err('an-mode-err', ''); err('an-err', ''); sync(); }));
    pan.addEventListener('change', () => { err('an-err', ''); sync(); });
    consent.addEventListener('change', () => { if (consent.checked) err('an-err', ''); sync(); });
    // Every change to an editable detail is saved at once, so screen 17 always shows the latest values
    const saveEdits = () => {
      if (!pan.value) return;
      const edits = {};
      document.querySelectorAll('select[data-pf], .an-decl input').forEach((f) => { edits[f.dataset.pf] = f.type === 'checkbox' ? f.checked : f.value; });
      store.set(K.profile, { pan: pan.value, edits });
    };
    document.querySelectorAll('select[data-pf], .an-decl input').forEach((f) => f.addEventListener('change', saveEdits));
    document.querySelectorAll('select[data-pf]').forEach((f) => f.addEventListener('change', () => {
      document.querySelector(`[data-pf-err="${f.dataset.pf}"]`).textContent = ''; f.classList.remove('has-err');
      if ($('an-err').textContent === AN_ERR.details) err('an-err', '');
    }));
    document.querySelectorAll('.an-decl input').forEach((c) => c.addEventListener('change', () => {
      document.querySelector('[data-pf-err="decl"]').textContent = '';
      if ($('an-err').textContent === AN_ERR.details) err('an-err', '');
    }));

    // ---- New PAN verification ----
    const lock = (on) => { [name, dob, newPan].forEach((i) => { i.readOnly = on; i.classList.toggle('readonly', on); }); };
    const unverify = () => { if (!verified) return; verified = false; $('np-ok').hidden = true; sync(); };
    name.addEventListener('input', () => {
      const v = name.value.replace(/[^A-Za-z .]/g, '');
      if (v !== name.value) { name.value = v; err('np-name-err', AN_ERR.nameChars, name); } else err('np-name-err', '', name);
      unverify();
    });
    dob.addEventListener('input', () => {                     // digits only, slashes added automatically
      const d = dob.value.replace(/\D/g, '').slice(0, 8);
      dob.value = d.length > 4 ? `${d.slice(0, 2)}/${d.slice(2, 4)}/${d.slice(4)}` : d.length > 2 ? `${d.slice(0, 2)}/${d.slice(2)}` : d;
      err('np-dob-err', '', dob); unverify();
    });
    newPan.addEventListener('input', () => {
      newPan.value = newPan.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 10);
      err('np-pan-err', '', newPan); unverify();
    });
    const dobError = (v) => {
      const m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(v);
      if (!m) return AN_ERR.dob;
      const [dd, mm, yy] = [+m[1], +m[2], +m[3]];
      const d = new Date(yy, mm - 1, dd);
      if (d.getFullYear() !== yy || d.getMonth() !== mm - 1 || d.getDate() !== dd || d > new Date() || yy < 1900) return AN_ERR.dob;
      const adult = new Date(yy + 18, mm - 1, dd);
      return adult > new Date() ? AN_ERR.age : '';
    };
    document.querySelector('[data-cta="verify-pan"]').addEventListener('click', () => {
      const n = name.value.trim(), p = newPan.value;
      const eName = n ? '' : AN_ERR.name;
      const eDob = dobError(dob.value);
      let ePan = /^[A-Z]{5}[0-9]{4}[A-Z]$/.test(p) ? '' : AN_ERR.panFormat;
      if (!ePan && CUSTOMER.pans.includes(p)) ePan = AN_ERR.panLinked;
      else if (!ePan && CUSTOMER.pans.length >= MAX_PANS) ePan = AN_ERR.panMax;
      err('np-name-err', eName, name); err('np-dob-err', eDob, dob); err('np-pan-err', ePan, newPan);
      if (eName || eDob || ePan) return;
      // Prototype: a valid, not-yet-linked PAN is treated as verified (no PAN service is called)
      verified = true; lock(true);
      $('np-ok').hidden = false;
      document.querySelector('[data-cta="verify-pan"]').hidden = true;
      sync();
    });

    // ---- Continue ----
    cta.addEventListener('click', () => {
      if (!mode) return err('an-mode-err', AN_ERR.mode);
      if (mode === 'existing' && !pan.value) return err('an-err', AN_ERR.pan);
      if (mode === 'new' && !verified) return err('an-err', AN_ERR.verify);
      if (mode === 'existing') {                               // editable customer details must be complete
        let bad = null;
        document.querySelectorAll('select[data-pf]').forEach((f) => {
          const label = f.closest('div').querySelector('.field-lbl').firstChild.textContent.trim().replace(/\?$/, '').toLowerCase();
          const e = document.querySelector(`[data-pf-err="${f.dataset.pf}"]`);
          e.textContent = f.value ? '' : `Please select ${label}.`; f.classList.toggle('has-err', !f.value);
          if (!f.value && !bad) bad = f;
        });
        const decl = [...document.querySelectorAll('.an-decl input')].every((c) => c.checked);
        document.querySelector('[data-pf-err="decl"]').textContent = decl ? '' : 'Please confirm both declarations to continue.';
        if (!decl && !bad) bad = document.querySelector('.an-decl input');
        if (bad) { bad.scrollIntoView({ block: 'center' }); return err('an-err', AN_ERR.details); }
        const edits = {};
        document.querySelectorAll('select[data-pf], .an-decl input').forEach((f) => { edits[f.dataset.pf] = f.type === 'checkbox' ? f.checked : f.value; });
        store.set(K.profile, { pan: pan.value, edits });                      // carried to Customer Details (17)
      }
      if (!consent.checked) return err('an-err', AN_ERR.consent);
      err('an-err', '');
      store.set(K.pan, mode === 'existing' ? pan.value : newPan.value);   // PAN used for the MF Central fetch
      store.set(K.mode, mode);
      store.set(K.kyc, {});                                                  // new application: KYC starts afresh
      store.set(K.pledge, '');                                               // … and pledging too
      store.set(K.agreement, '');                                            // … and the agreement
      store.set(K.emandate, '');                                             // … and the e-mandate
      go('05) LOS to MF Central Redirection loading page');
    });

    // Review screen 04.3 opens with a New PAN already verified (sample values)
    if (currentScreen() === '04.3) Apply for New Loan New PAN verified') {
      name.value = 'SAMPLE NAME'; dob.value = '01/01/1990'; newPan.value = 'ABCPD1234E';
      document.querySelector('[data-cta="verify-pan"]').click();
    }
    sync();
  };

  /* ---- 12 MF selection: loan amount (edit box or slider) and fund-wise amounts ----
     Rules: loan ₹ 10,000 – ₹ 2,00,00,000; each fund ≤ its Max Limit; loan = sum of fund amounts;
     a new loan amount is spread over the funds in list order, each filled up to its Max Limit;
     market value of units selected = amount ÷ 75% LTV. */
  const LOAN_MIN = 10000, LOAN_MAX = 20000000, LTV = 0.75;
  const num = (v) => Number(String(v).replace(/[^\d]/g, '')) || 0;
  const inr = (n) => Math.round(n).toLocaleString('en-IN');
  const inr2 = (n) => n.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const SEL_ERR = {
    range: `Loan amount must be between ₹ ${inr(LOAN_MIN)} and ₹ ${inr(LOAN_MAX)}.`,
    fundMax: (f) => `Amount cannot be more than the Max Limit of ₹ ${f.cl}.`,
    total: `Total loan amount cannot be more than ₹ ${inr(LOAN_MAX)}.`,
    min: `Minimum loan amount is ₹ ${inr(LOAN_MIN)}. Please select funds or increase the amount.`,
  };
  const selectionBehaviour = (start = {}) => {
    const maxOf = (id) => num(F[id].cl);
    // Start from the review state, else the selection saved on Continue (Back from 13), else the default
    let amounts = Object.fromEntries(Object.entries(start.selected || store.get(K.sel) || SEL_DEFAULT.selected).map(([k, v]) => [k, num(v)]));
    let editLoan = start.editLoan ?? null;       // string while the loan edit box is open
    let editing = start.editing || {};           // {id: string} fund boxes open
    let loanErr = '', fundErr = {};
    const total = () => Object.values(amounts).reduce((a, b) => a + b, 0);
    const spread = (v) => {                      // fill funds in list order up to each Max Limit
      const out = {}; let left = v;
      SEL_ORDER.forEach((id) => { if (left > 0) { const a = Math.min(left, maxOf(id)); out[id] = a; left -= a; } });
      return out;
    };

    const paint = () => {
      const t = total();
      const ids = Object.keys(amounts).filter((id) => amounts[id] > 0);
      const allState = ids.length === SEL_ORDER.length ? 'all' : ids.length ? 'part' : 'none';
      const busy = editLoan != null || Object.keys(editing).length > 0;
      const html = T.selection({
        loan: inr(t), editLoan, loanErr: loanErr || (!busy && t < LOAN_MIN ? SEL_ERR.min : ''),
        sliderPct: Math.min(100, (t / LOAN_MAX) * 100), mv: inr2(t / LTV), count: ids.length, allState,
        selected: Object.fromEntries(ids.map((id) => [id, inr(amounts[id])])), editing, fundErr,
        ctaDisabled: busy || t < LOAN_MIN || t > LOAN_MAX, cta: inr(t),
      });
      const tmp = document.createElement('div'); tmp.innerHTML = html;
      document.querySelector('main.sel-page').replaceWith(tmp.querySelector('main.sel-page'));
      document.querySelector('.cta-bar').replaceWith(tmp.querySelector('.cta-bar'));
      wire();
    };

    const digitsOnly = (inp) => inp.addEventListener('input', () => { inp.value = inp.value.replace(/\D/g, '').slice(0, 9); });

    const setLoan = (v) => { amounts = spread(v); editing = {}; fundErr = {}; };
    const wire = () => {
      const q = (s) => document.querySelector(s);
      q('[data-cta="back"]').onclick = () => go('11) Curated Offers Page');
      q('[data-cta="continue-to-apply"]').onclick = () => {
        if (editLoan != null || Object.keys(editing).length) return;          // finish editing first
        if (total() < LOAN_MIN) { loanErr = SEL_ERR.min; return paint(); }
        store.set(K.sel, amounts);                                           // kept for the summary and for Back
        go('13) Loan Application Summary');
      };
      // Loan amount: pencil → edit box → Update
      if (q('[data-cta="edit-loan"]')) q('[data-cta="edit-loan"]').onclick = () => { editLoan = String(total()); loanErr = ''; paint(); q('#loan-in').focus(); };
      if (q('#loan-in')) {
        const inp = q('#loan-in'); digitsOnly(inp);
        const update = () => {
          const v = num(inp.value);
          if (v < LOAN_MIN || v > LOAN_MAX) { editLoan = inp.value; loanErr = SEL_ERR.range; return paint(); }
          editLoan = null; loanErr = ''; setLoan(v); paint();
        };
        q('[data-cta="update-loan"]').onclick = update;
        inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') update(); });
      }
      // Slider: click or drag sets the loan amount (steps of ₹ 1,000)
      const track = q('#loan-track');
      const fromX = (x) => { const r = track.getBoundingClientRect(); const p = Math.min(1, Math.max(0, (x - r.left) / r.width)); return Math.max(LOAN_MIN, Math.round((p * LOAN_MAX) / 1000) * 1000); };
      track.onpointerdown = (e) => {
        if (editLoan != null) return;
        e.preventDefault();
        const move = (ev) => { setLoan(fromX(ev.clientX)); loanErr = ''; paint(); };
        move(e);
        const up = () => { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); };
        window.addEventListener('pointermove', move); window.addEventListener('pointerup', up);
      };
      // Fund-wise amount: pencil → box with ✓
      document.querySelectorAll('[data-fund-edit]').forEach((a) => { a.onclick = () => {
        const id = a.dataset.fundEdit; editing = { ...editing, [id]: String(amounts[id] || '') }; paint();
        const inp = document.querySelector(`.fund-in[data-id="${id}"]`); inp.focus();
      }; });
      document.querySelectorAll('.fund-in').forEach((inp) => {
        digitsOnly(inp);
        inp.addEventListener('input', () => { editing[inp.dataset.id] = inp.value; });
        inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') document.querySelector(`[data-fund-ok="${inp.dataset.id}"]`).click(); });
      });
      document.querySelectorAll('[data-fund-ok]').forEach((b) => { b.onclick = () => {
        const id = b.dataset.fundOk; const v = num(editing[id]);
        const others = total() - (amounts[id] || 0);
        if (v > maxOf(id)) { fundErr = { ...fundErr, [id]: SEL_ERR.fundMax(F[id]) }; return paint(); }
        if (others + v > LOAN_MAX) { fundErr = { ...fundErr, [id]: SEL_ERR.total }; return paint(); }
        const next = { ...amounts }; if (v > 0) next[id] = v; else delete next[id];
        amounts = next; delete editing[id]; editing = { ...editing }; delete fundErr[id]; loanErr = ''; paint();
      }; });
      // Tick / untick a fund: tick adds it at its Max Limit (within the ₹ 2 crore cap)
      document.querySelectorAll('[data-fund-tick]').forEach((c) => { c.onclick = () => {
        const id = c.dataset.fundTick; const next = { ...amounts };
        if (next[id]) delete next[id];
        else { const room = LOAN_MAX - total(); if (room <= 0) { fundErr = { ...fundErr, [id]: SEL_ERR.total }; return paint(); } next[id] = Math.min(maxOf(id), room); }
        amounts = next; delete editing[id]; editing = { ...editing }; delete fundErr[id]; loanErr = ''; paint();
      }; });
      q('[data-cta="select-all"]').onclick = (e) => {
        e.preventDefault();
        // Funds can never all be ticked within the ₹ 2 crore cap, so Select All toggles between
        // "fill funds in list order up to ₹ 2 crore" and "clear all" (once at the cap)
        amounts = total() >= LOAN_MAX ? {} : spread(LOAN_MAX); editing = {}; fundErr = {}; loanErr = ''; paint();
      };
    };
    paint();
  };

  /* Auto-advance after a delay (redirect / loader screens). Leaving the page cancels it. */
  const after = (ms, screen) => setTimeout(() => go(screen), ms);

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

        // OTP verified: existing customer lands on "Your loans"
        st = { resend: 0, wrong: 0, blockedUntil: 0, reason: '' }; save();
        showErr('');
        go('04) Your Loans Page');
      });

      // initial state
      if (isBlocked()) showBlocked(); else startTimer();
      sync();
    },

    '04.1) Apply for New Loan Page': applyNewBehaviour,
    '04.2) Apply for New Loan Existing PAN selected': applyNewBehaviour,
    '04.3) Apply for New Loan New PAN verified': applyNewBehaviour,

    /* ---- 05 Redirect popup: 3, 2, 1 then MF Central; close → back to the Apply for New Loan page ---- */
    '05) LOS to MF Central Redirection loading page': () => {
      const count = document.getElementById('mfc-count');
      let left = 3;
      const t = setInterval(() => {
        left -= 1;
        if (left > 0) { count.textContent = left; return; }
        clearInterval(t);
        go('06) MF Central Mock Page');
      }, 1000);
      document.querySelector('.m-mfc .close').onclick = () => { clearInterval(t); go('04.1) Apply for New Loan Page'); };
    },

    /* ---- 06 MF Central mock: 6-digit OTP, only 000000 accepted for now ---- */
    '06) MF Central Mock Page': () => {
      const boxes = [...document.querySelectorAll('.mock-card .otp input')];
      const err = document.getElementById('mock-err');
      const cta = document.querySelector('.mock-card [data-cta="submit"]');
      const value = () => boxes.map((b) => b.value).join('');
      const showErr = (msg) => { err.textContent = msg || ''; boxes.forEach((b) => b.classList.toggle('has-err', !!msg)); };
      const sync = () => {
        const ok = value().length === OTP_RULES.length;
        cta.classList.toggle('btn-primary', ok);
        cta.classList.toggle('bold', ok);
        cta.classList.toggle('btn-disabled', !ok);
      };
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
            boxes[Math.min(idx + digits.length, OTP_RULES.length) - 1].focus();
          } else {
            box.value = digits;
            if (digits && boxes[idx + 1]) boxes[idx + 1].focus();
          }
          if (digits !== before) showErr(OTP_ERR.chars);
          else if (err.textContent) showErr('');
          sync();
        });
      });
      cta.addEventListener('click', () => {
        const v = value();
        if (v.length !== OTP_RULES.length) return showErr(OTP_ERR.incomplete);
        if (v !== OTP_RULES.demoOtp) {
          boxes.forEach((b) => { b.value = ''; }); boxes[0].focus(); sync();
          return showErr('The OTP you entered is incorrect. Please try again.');
        }
        go('07) MF Central to LOS Redirecting Page');
      });
      sync();
    },

    /* ---- 07 → 08 → 09 → 10 → 11: each moves on automatically after 1 second ---- */
    '07) MF Central to LOS Redirecting Page': () => after(1000, '08) MF Central to LOS Fetching Mutual Fund Portfolio Page'),
    '08) MF Central to LOS Fetching Mutual Fund Portfolio Page': () => after(1000, '09) MF Central to LOS Analysing Mutual Fund Portfolio Page'),
    '09) MF Central to LOS Analysing Mutual Fund Portfolio Page': () => after(1000, '10) MF Central to LOS Generating Loan Page'),
    '10) MF Central to LOS Generating Loan Page': () => after(1000, '11) Curated Offers Page'),

    /* ---- 12 MF selection (interactive); 12.1 / 12.2 open with the loan box / a fund box in edit mode ---- */
    '12) Mutual Fund Selection Page': () => selectionBehaviour(),

    /* ---- 13 Summary: figures for the amount chosen on 12; Back → 12; Continue → next screen (pending) ---- */
    '13) Loan Application Summary': () => {
      const saved = store.get(K.sel);
      if (saved) {
        const amount = Object.values(saved).reduce((a, b) => a + b, 0);
        const tmp = document.createElement('div'); tmp.innerHTML = T.summary(amount);
        document.querySelector('main.sum-page').replaceWith(tmp.querySelector('main.sum-page'));
      }
      document.querySelector('[data-cta="back"]').onclick = () => go('12) Mutual Fund Selection Page');
      document.querySelector('[data-cta="continue"]').onclick = () => go('14) KYC Verification Page');
    },

    /* ---- 14 KYC: loan amount from screen 12; Back → 13; other actions pending ---- */
    /* Existing PAN: email is already verified → Email Verification complete, Aadhaar "Start KYC" (as 16.4).
       New PAN: email still to be verified (as 16.1). Screen 14.1 always shows the New PAN state. */
    '14) KYC Verification Page': () => kycBehaviour(),
    '14.1) KYC Verification Page New PAN email verification': () => kycBehaviour('new'),
    // Review copies of the KYC page after each mock result (the live page 14 shows the same states)
    '15.1) KYC Verification Page Aadhaar verification success': () => kycBehaviour('existing', { aadhaar: 'done' }),
    '15.2) KYC Verification Page Aadhaar verification failed': () => kycBehaviour('existing', { aadhaar: 'failed' }),
    '16.1) KYC Verification Page Photo verification success': () => kycBehaviour('existing', { aadhaar: 'done', photo: 'done' }),
    '16.2) KYC Verification Page Photo verification failed': () => kycBehaviour('existing', { aadhaar: 'done', photo: 'failed' }),

    /* ---- 15 / 16 mocks: Success marks the step complete, Failure returns with an error to retry ---- */
    '15) DigiLocker Mock Page': () => kycMockBehaviour('aadhaar'),
    '16) Photo Verification Mock Page': () => kycMockBehaviour('photo'),
    '17) Customer Details Page': () => custDetailsBehaviour(),
    '18) Pledging of Mutual Fund Page': () => pledgeBehaviour('page'),
    '18.1) Pledging of Mutual Fund OTP popup': () => pledgeBehaviour('otp'),
    '18.2) Pledging of Mutual Fund Successfully pledged': () => pledgeBehaviour('done'),
    '19) Agreement and E-Mandate Page': () => {
      const signed = store.get(K.agreement) === 'done';
      const tmp = document.createElement('div'); tmp.innerHTML = T.agreement(signed, store.get(K.emandate));
      document.querySelector('main.ag-page').replaceWith(tmp.querySelector('main.ag-page'));
      const a = document.querySelector('[data-cta="sign-agreement"]'); if (a) a.onclick = () => go('20) Sanction Letter Page');
      const e = document.querySelector('[data-cta="setup-emandate"]'); if (e) e.onclick = () => go('22) E-Mandate Page');
    },
    '19.1) Agreement and E-Mandate Page Loan Agreement signed': () => {
      document.querySelector('[data-cta="setup-emandate"]').onclick = () => go('22) E-Mandate Page');
    },
    '22) E-Mandate Page': () => emandateBehaviour(),
    '22.1) E-Mandate NPCI Simulation Page': () => npciBehaviour(),
    '22.2) E-Mandate Authenticated Successfully': () => emandateDoneBehaviour(),
    '23) Loan Application Submitted Page': () => submittedBehaviour(),
    '20) Sanction Letter Page': () => sanctionBehaviour(),
    '21) Loan Agreement e-Sign Page': () => esignBehaviour(),
    '21.1) Loan Agreement e-Sign OTP popup': () => esignOtpBehaviour(),
    '21.2) Loan Agreement e-Sign Signed Successfully': () => esignDoneBehaviour(),
    '21.3) Loan Agreement Signed Successfully': () => agreementSignedBehaviour(),
  };
  /* ---- 17 Customer details: collapse / expand, required fields, Confirm and Continue ---- */
  function custDetailsBehaviour() {
    const pan = store.get(K.pan);
    const base = PROFILE[pan] || PROFILE.CBOPA8195B;
    const prof = store.get(K.profile);                        // changes made on the ETB page
    const p = prof && prof.pan === pan ? { ...base, ...prof.edits } : base;
    const saved = store.get(K.sel);
    const tmp = document.createElement('div');
    tmp.innerHTML = T.custDetails(p, saved ? inr(Object.values(saved).reduce((x, y) => x + y, 0)) : undefined);
    document.querySelector('main.cd-page').replaceWith(tmp.querySelector('main.cd-page'));
    const q = (s) => document.querySelector(s);
    q('[data-cta="back"]').onclick = () => go('14) KYC Verification Page');
    q('[data-cta="view-details"]').onclick = () => toast('This step will be added once its screenshot is shared.');
    document.querySelectorAll('[data-toggle]').forEach((b) => { b.onclick = () => b.closest('.cd-sec').classList.toggle('open'); });
    const err = (k, msg) => { const e = q(`[data-err="${k}"]`); if (e) e.textContent = msg || ''; const f = q(`.cd-in[data-k="${k}"]`); if (f) f.classList.toggle('has-err', !!msg); };
    document.querySelectorAll('.cd-in').forEach((f) => f.addEventListener(f.tagName === 'SELECT' ? 'change' : 'input', () => {
      if (f.tagName === 'INPUT') { const v = f.value.replace(/[^A-Za-z .]/g, ''); if (v !== f.value) { f.value = v; return err(f.dataset.k, 'Only letters, spaces and dots are allowed.'); } }
      err(f.dataset.k, '');
    }));
    document.querySelectorAll('.cd-chk input').forEach((c) => c.addEventListener('change', () => err('decl', '')));
    q('[data-cta="confirm-continue"]').onclick = () => {
      let first = null;
      document.querySelectorAll('.cd-in').forEach((f) => {
        const label = f.closest('.cd-f').querySelector('.cd-l').firstChild.textContent.trim();
        const bad = !f.value.trim() ? (f.tagName === 'SELECT' ? `Please select ${label.replace(/\?$/, '').toLowerCase()}.` : `Please enter ${label.toLowerCase()}.`) : '';
        err(f.dataset.k, bad); if (bad && !first) first = f;
      });
      const decl = [...document.querySelectorAll('.cd-chk input')].every((c) => c.checked);
      err('decl', decl ? '' : 'Please confirm both declarations to continue.');
      if (!decl && !first) first = q('.cd-chk input');
      if (first) { first.closest('.cd-sec').classList.add('open'); first.scrollIntoView({ block: 'center' }); return; }
      go('18) Pledging of Mutual Fund Page');
    };
  }

  /* ---- 18 / 18.1 / 18.2 Pledging: Pledge Securities → OTP popup → Successfully pledged → back with status ---- */
  function pledgeData() {
    const saved = store.get(K.sel);
    const loan = saved ? Object.values(saved).reduce((x, y) => x + y, 0) : 20000000;
    return { loan: inr(loan), pledge: inr2(loan / LTV), mobile: maskMobile2(store.get(K.mobile) || CUSTOMER.mobile) };
  }
  function pledgeBehaviour(screen) {
    const d = pledgeData();
    const status = store.get(K.pledge) === 'done' ? 'pledged' : 'pending';
    const tmp = document.createElement('div'); tmp.innerHTML = T.pledge({ ...d, status: screen === 'page' ? status : 'pending' });
    document.querySelector('main.pl-page').replaceWith(tmp.querySelector('main.pl-page'));
    const q = (s) => document.querySelector(s);
    q('[data-cta="back"]').onclick = () => go('17) Customer Details Page');
    q('[data-cta="view-securities"]').onclick = () => toast('This step will be added once its screenshot is shared.');
    if (q('[data-cta="pledge-securities"]')) q('[data-cta="pledge-securities"]').onclick = () => go('18.1) Pledging of Mutual Fund OTP popup');

    if (screen === 'otp') {
      const modal = q('.m-plotp');
      modal.querySelector('.sent b').textContent = d.mobile;
      modal.querySelector('.close').onclick = () => go('18) Pledging of Mutual Fund Page');
      const boxes = [...modal.querySelectorAll('.otp input')];
      const errEl = q('#pl-otp-err');
      const showErr = (m) => { errEl.textContent = m || ''; boxes.forEach((b) => b.classList.toggle('has-err', !!m)); };
      boxes.forEach((box, idx) => {
        box.addEventListener('keydown', (e) => {
          if (e.key === 'Backspace' && !box.value && boxes[idx - 1]) { boxes[idx - 1].focus(); return; }
          if (e.key.length > 1 || e.ctrlKey || e.metaKey) return;
          if (!/[0-9]/.test(e.key)) { e.preventDefault(); showErr(OTP_ERR.chars); }
        });
        box.addEventListener('input', () => {
          const digits = box.value.replace(/\D/g, '');
          if (digits.length > 1) {
            digits.slice(0, 6 - idx).split('').forEach((c, k) => { if (boxes[idx + k]) boxes[idx + k].value = c; });
            boxes[Math.min(idx + digits.length, 6) - 1].focus();
          } else { box.value = digits; if (digits && boxes[idx + 1]) boxes[idx + 1].focus(); }
          if (errEl.textContent) showErr('');
        });
      });
      // 30-second timer, then Resend OTP (clears the boxes and restarts the timer)
      const slot = q('#pl-resend'); let t = null;
      const timer = () => {
        clearInterval(t); let left = OTP_RULES.resendSeconds;
        const paint = () => {
          if (left > 0) { slot.innerHTML = `<b>00:${String(left).padStart(2, '0')}</b>`; left -= 1; return; }
          clearInterval(t); slot.innerHTML = '<a class="link-yellow" id="pl-resend-cta">Resend OTP</a>';
          q('#pl-resend-cta').onclick = () => { boxes.forEach((b) => { b.value = ''; }); showErr(''); timer(); };
        };
        paint(); t = setInterval(paint, 1000);
      };
      timer();
      q('[data-cta="submit-pledge-otp"]').onclick = () => {
        const v = boxes.map((b) => b.value).join('');
        if (v.length !== 6) return showErr(OTP_ERR.incomplete);
        if (v !== OTP_RULES.demoOtp) { boxes.forEach((b) => { b.value = ''; }); boxes[0].focus(); return showErr('The OTP you entered is incorrect. Please try again.'); }
        clearInterval(t);
        go('18.2) Pledging of Mutual Fund Successfully pledged');
      };
    }

    if (screen === 'done') {
      store.set(K.pledge, 'done');
      let left = 3; const c = q('#pl-count');
      const t = setInterval(() => {
        left -= 1; c.textContent = Math.max(left, 0);
        if (left <= 0) { clearInterval(t); go('19) Agreement and E-Mandate Page'); }
      }, 1000);
    }

  }

  /* ---- 19 → 20 → 21 → 19: Sign Agreement → sanction letter (accept + Submit) → e-sign → Loan Agreement complete ---- */
  function loanContext() {
    const pan = store.get(K.pan);
    const base = PROFILE[pan] || PROFILE.CBOPA8195B;
    const prof = store.get(K.profile);
    const saved = store.get(K.sel);
    return {
      profile: prof && prof.pan === pan ? { ...base, ...prof.edits } : base,
      amount: saved ? Object.values(saved).reduce((x, y) => x + y, 0) : 20000000,
      mobile: '+91' + (store.get(K.mobile) || CUSTOMER.mobile),
    };
  }
  function sanctionBehaviour() {
    const ctx = loanContext();
    document.body.innerHTML = T.sanction(ctx);
    const chk = document.getElementById('sl-accept');
    const btn = document.querySelector('[data-cta="sanction-submit"]');
    chk.addEventListener('change', () => { btn.disabled = !chk.checked; });
    btn.onclick = () => { if (chk.checked) go('21) Loan Agreement e-Sign Page'); };
  }
  function esignBehaviour() {
    const ctx = loanContext();
    document.body.innerHTML = T.esign(ctx);
    const chk = document.getElementById('dg-accept');
    const btn = document.querySelector('[data-cta="sign-now"]');
    chk.addEventListener('change', () => { btn.disabled = !chk.checked; });
    btn.onclick = () => { if (chk.checked) go('21.1) Loan Agreement e-Sign OTP popup'); };
  }

  /* ---- 21.1 → 21.2 → 21.3 → 19: Digio OTP, signed, back to LOS with Loan Agreement complete ---- */
  function esignOtpBehaviour() {
    const ctx = loanContext();
    document.body.innerHTML = T.esign(ctx) + T.esignOtpModal();
    document.body.classList.add('modal-open'); document.documentElement.classList.add('modal-open');
    const q = (s) => document.querySelector(s);
    const aad = q('#dg-aadhaar');
    const boxes = [...document.querySelectorAll('.dg-boxes input')];
    const aErr = (m) => { q('#dg-aadhaar-err').textContent = m || ''; aad.classList.toggle('has-err', !!m); };
    const oErr = (m) => { q('#dg-otp-err').textContent = m || ''; boxes.forEach((b) => b.classList.toggle('has-err', !!m)); };
    aad.addEventListener('input', () => { aad.value = aad.value.replace(/\D/g, '').slice(0, 16); aErr(''); });
    boxes.forEach((box, idx) => {
      box.addEventListener('keydown', (e) => { if (e.key === 'Backspace' && !box.value && boxes[idx - 1]) boxes[idx - 1].focus(); });
      box.addEventListener('input', () => {
        const d = box.value.replace(/\D/g, '');
        if (d.length > 1) { d.slice(0, 6 - idx).split('').forEach((c, k) => { if (boxes[idx + k]) boxes[idx + k].value = c; }); boxes[Math.min(idx + d.length, 6) - 1].focus(); }
        else { box.value = d; if (d && boxes[idx + 1]) boxes[idx + 1].focus(); }
        oErr('');
      });
    });
    q('[data-cta="esign-submit-otp"]').onclick = () => {
      const a = aad.value; const v = boxes.map((b) => b.value).join('');
      const ae = !a ? 'Please enter your Aadhaar number or VID.' : (a.length === 12 || a.length === 16) ? '' : 'Aadhaar number must be 12 digits or VID 16 digits.';
      const oe = v.length !== 6 ? 'Please enter the 6-digit OTP.' : v !== OTP_RULES.demoOtp ? 'The OTP you entered is incorrect. Please try again.' : '';
      aErr(ae); oErr(oe);
      if (ae || oe) { if (oe && v.length === 6) boxes.forEach((b) => { b.value = ''; }); return; }
      go('21.2) Loan Agreement e-Sign Signed Successfully');
    };
    aad.focus();
  }
  function esignDoneBehaviour() {
    document.body.innerHTML = T.esignDone();
    store.set(K.agreement, 'done');
    setTimeout(() => go('21.3) Loan Agreement Signed Successfully'), 1500);
  }
  function agreementSignedBehaviour() {
    document.body.innerHTML = T.agreementSigned();
    store.set(K.agreement, 'done');
    let left = 3; const c = document.getElementById('ag-count');
    const t = setInterval(() => { left -= 1; c.textContent = Math.max(left, 0); if (left <= 0) { clearInterval(t); go('19) Agreement and E-Mandate Page'); } }, 1000);
  }

  /* ---- 19 → 22 → 22.1 → 22.2 → 23: E-Mandate at Digio, NPCI Accept / Reject, back to LOS submitted ---- */
  function emandateBehaviour() {
    const pan = store.get(K.pan);
    document.body.innerHTML = T.emandate({ bank: (PAN_DETAILS[pan] || PAN_DETAILS.CBOPA8195B).bank });
    const q = (s) => document.querySelector(s);
    document.querySelectorAll('.em-mode input').forEach((r) => r.addEventListener('change', () => {
      document.querySelectorAll('.em-mode').forEach((m) => m.classList.toggle('on', m.querySelector('input').checked));
    }));
    const acc = q('#em-acc'); const masked = acc.textContent;
    q('[data-cta="em-eye"]').onclick = () => { acc.textContent = acc.textContent === masked ? acc.dataset.full.replace(/(\d{4})(?=\d)/g, '$1 ') : masked; };
    const chk = q('#em-accept'); const btn = q('[data-cta="em-submit"]');
    chk.addEventListener('change', () => { btn.disabled = !chk.checked; });
    btn.onclick = () => { if (chk.checked) { store.set(K.emMode, q('.em-mode input:checked').value); go('22.1) E-Mandate NPCI Simulation Page'); } };
  }
  function npciBehaviour() {
    const d = new Date(); const p2 = (n) => String(n).padStart(2, '0');
    const rand = Array.from({ length: 13 }, () => 'ABCDEFGHJKLMNPQRSTUVWXYZ'[Math.floor(Math.random() * 24)]).join('');
    document.body.innerHTML = T.npci(`MMI${String(d.getFullYear()).slice(2)}${p2(d.getMonth() + 1)}${p2(d.getDate())}${p2(d.getHours())}${p2(d.getMinutes())}${p2(d.getSeconds())}${rand}`);
    document.querySelector('[data-cta="npci-accept"]').onclick = () => go('22.2) E-Mandate Authenticated Successfully');
    document.querySelector('[data-cta="npci-reject"]').onclick = () => { store.set(K.emandate, 'failed'); go('19) Agreement and E-Mandate Page'); };
  }
  function emandateDoneBehaviour() {
    document.body.innerHTML = T.emandateDone();
    store.set(K.emandate, 'done');
    setTimeout(() => go('23) Loan Application Submitted Page'), 2000);
  }
  function submittedBehaviour() {
    const ctx = loanContext();
    const tmp = document.createElement('div'); tmp.innerHTML = T.submitted(ctx);
    document.querySelector('main.sb-page').replaceWith(tmp.querySelector('main.sb-page'));
    document.querySelector('[data-cta="view-loan"]').onclick = () => toast('Loan details will be added once its screenshot is shared.');
  }

  function kycMockBehaviour(step) {
    const set = (result) => {
      const kyc = { ...(store.get(K.kyc) || {}), [step]: result };
      if (step === 'aadhaar' && result !== 'done') delete kyc.photo;       // photo comes after Aadhaar
      store.set(K.kyc, kyc);
      go('14) KYC Verification Page');
    };
    document.querySelector('[data-cta="mock-success"]').onclick = () => set('done');
    document.querySelector('[data-cta="mock-failure"]').onclick = () => set('failed');
  }
  function kycBehaviour(forceMode, forceKyc) {
    {
      const mode = forceMode || store.get(K.mode) || 'existing';
      const saved = store.get(K.sel);
      // KYC progress from the mocks: {aadhaar:'done'|'failed', photo:'done'|'failed'} (review screens force a state)
      const kyc = forceKyc || store.get(K.kyc) || {};
      const opts = mode === 'new' ? { email: 'input' } : { email: 'done', aadhaar: 'start' };
      if (mode !== 'new') {
        if (kyc.aadhaar === 'failed') opts.aadErr = 'Aadhaar verification failed. Please try again.';
        if (kyc.aadhaar === 'done') {
          opts.aadhaar = 'done';
          opts.photo = kyc.photo === 'done' ? 'done' : 'start';
          if (kyc.photo === 'failed') opts.photoErr = 'Photo verification failed. Please try again.';
        }
      }
      if (saved) opts.loan = inr(Object.values(saved).reduce((x, y) => x + y, 0));
      // Existing PAN: bank account on file → Bank Details complete; only Aadhaar and Photo are asked
      const kycDone = kyc.aadhaar === 'done' && kyc.photo === 'done';
      if (mode !== 'new') {
        opts.bank = PAN_DETAILS[store.get(K.pan)] ? PAN_DETAILS[store.get(K.pan)].bank : PAN_DETAILS.CBOPA8195B.bank;
        opts.cont = kycDone ? 'on' : 'off';
      }
      const tmp = document.createElement('div');
      tmp.innerHTML = T.kyc(opts);
      document.querySelector('main.kyc-page').replaceWith(tmp.querySelector('main.kyc-page'));
      document.querySelector('[data-cta="back"]').onclick = () => go('13) Loan Application Summary');
      document.querySelectorAll('[data-cta="verify-email"], [data-cta="view-details"]').forEach((el) => {
        el.onclick = () => toast('This step will be added once its screenshot is shared.');
      });
      const on = (cta, fn) => { const el = document.querySelector(`[data-cta="${cta}"]`); if (el) el.onclick = fn; };
      on('start-kyc', () => go('15) DigiLocker Mock Page'));
      on('start-photo', () => go('16) Photo Verification Mock Page'));
      on('kyc-continue', () => {
        if (!kycDone) { document.getElementById('kyc-cont-err').textContent = 'Please complete Aadhaar and Photo verification to continue.'; return; }
        go('17) Customer Details Page');
      });
    }
  }
  Object.assign(BEHAVIOUR, {
    '12.1) Mutual Fund Selection page loan amount edit': () => selectionBehaviour({ selected: { icici: '95,30,700' }, editLoan: '9530700' }),
    '12.2) Mutual Fund Selection page loan amount edit as fund wise': () => selectionBehaviour({ selected: { icici: '95,30,700' }, editing: { icici: '100000' } }),
  });

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

  window.LAMF = { SEL_DEFAULT, T, render, withModal, SCREENS, FLOW, BEHAVIOUR, LEGAL, OTP_RULES, OTP_ERR, MOBILE_ERR, CUSTOMER };
})();
