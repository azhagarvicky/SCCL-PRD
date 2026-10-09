/* ==========================================================
   LAMF Online Journey – shared components, data & templates
   Every screen HTML calls LAMF.render(...) with a template.
   Edit a component here once → it changes on all screens.
   ========================================================== */
(function () {
  const IMG = 'assets/img/';

  /* ---------------- Screen register (sort order) ---------------- */
  const SCREENS = [
    '01) LAMF Landing Page',
    '02) Enter MF linked Mobile Number',
    '03) Enter OTP for MF linked Mobile Number Verification',
    '04) Enter PAN Details',
    '05) LOS to MF Central Redirection consent page',
    '06) LOS to MF Central Redirection loading page',
    '07) MF Central Data Check Mock',
    '07.1) PAN and Mobile Number Combination No Data Available',
    '07.2) MF Central OTP Page',
    '07.3) MF Central Select AMCs Page',
    '07.4) MF Central Portfolio Fetching Page',
    '07.5) MF Central Portfolio Discovery Complete Page',
    '08) MF Central to LOS Redirecting Page',
    '09) MF Central to LOS Fetching Mutual Fund Portfolio Page',
    '10) MF Central to LOS Analysing Mutual Fund Portfolio Page',
    '11) MF Central to LOS Generating Loan Page',
    '12) Curated Offers Page',
    '12.1.1) How is it calculated_All Portfolio',
    '12.1.2) How is it calculated_Eligible Portfolio',
    '12.1.3) How is it calculated_Non Eligible Portfolio',
    '12.2) Curated offers page for dorpoff view',
    '12.2) Refresh portfolio',
    '13.1) Mutual Fund Selection Location access',
    '13.2) Mutual Fund Selection Page',
    '13.3) Mutual Fund Selection page if location disabled',
    '13.4) Mutual Fund Selection page if location disabled & proceed',
    '13.5) Mutual Fund Selection page loan amount edit',
    '13.6) Mutual Fund Selection page loan amount edit as fund wise',
    '14) Loan Application Summary',
    '16.1) KYC Verification Page',
    '16.2) KYC Verification Page view details popup',
    '16.3) KYC Verification Page Email verification popup',
    '16.4) KYC Verification Page email verification completed',
    '16.5.1) KYC Verification Page Aadhar verification',
    '16.5.2) KYC Verification Page Aadhar verification Enter aadhar',
    '16.5.3) KYC Verification Page Aadhar verification Enter aadhar OTP',
    '16.5.4) KYC Verification Page Aadhar verification Enter PIN',
    '16.5.5) KYC Verification Page Aadhar verification Fetching',
    '16.5.6) KYC Verification Page Aadhar verification process done in digilocker yet to redirect to los',
    '16.5.7) KYC Verification Page Aadhar verification process done in digilocker  to los auto redirection',
    '16.5.8) KYC Verification Page Aadhar verification process done in digilocker  redirected to los but status getting updated',
    '16.5.9) KYC Verification Page Aadhar verification completed',
  ];
  /* In the local copy each screen is its own .html file. In the cloud copy
     (single page, see cloud.html) screens are hash routes on one page. */
  const SPA = () => !!window.LAMF_SPA;
  const href = (name) => (SPA() ? '#' + encodeURIComponent(name) : encodeURIComponent(name + '.html'));
  /* The Shriram Credit logo on every screen goes back to the prototype home page */
  const home = () => (SPA() ? '#' : 'index.html');
  const logoLink = (inner) => `<a class="logo" href="${home()}" title="Home">${inner}</a>`;

  /* ---------------- Demo customer data ---------------- */
  const CUSTOMER = {
    mobile: '9597001623', mobileMasked: '+9195XXXX1623', mobileMasked2: '+919XXXX1623',
    pan: 'CBOPA 8195 B', email: 'azhagarsamy.s@shriramcredit.in',
  };
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
    logout: S('<path d="M10 4H5v16h5"/><path d="M14 8l4 4-4 4M18 12H9"/>'),
    back: S('<path d="M20 12H4M10 6l-6 6 6 6"/>'),
    check: S('<path d="M5 12.5l4.5 4.5L19 7.5"/>', '0 0 24 24', 'stroke="#fff" stroke-width="2.6"'),
    close: S('<circle cx="12" cy="12" r="9.5"/><path d="M9 9l6 6M15 9l-6 6"/>', '0 0 24 24', 'stroke="#555" stroke-width="1.3"'),
    pencilSolid: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 17.25V21h3.75L17.8 9.94l-3.75-3.75L3 17.25zM20.7 7.04a1 1 0 0 0 0-1.41l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>`,
    pencil: S('<path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13.5 6.5l4 4"/>', '0 0 24 24', 'stroke-width="1.5"'),
    phone: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25c1.1.37 2.3.57 3.6.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>`,
    calendar: `<svg viewBox="0 0 24 24" fill="#555"><path d="M19 4h-1V2h-2v2H8V2H6v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 16H5V9h14zM12 13h5v5h-5z"/></svg>`,
    refresh: S('<path d="M20 11a8 8 0 0 0-14.3-4.3L4 8.5M4 4v4.5h4.5"/><path d="M4 13a8 8 0 0 0 14.3 4.3L20 15.5M20 20v-4.5h-4.5"/>', '0 0 24 24', 'stroke-width="2"'),
    shield: `<svg viewBox="0 0 24 24" fill="#FFCB08"><path d="M12 2l8 3v6c0 5-3.4 9.4-8 11-4.6-1.6-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5" stroke="#fff" stroke-width="2" fill="none"/></svg>`,
    tick: `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#111"/><path d="M7 12.5l3.2 3.2L17 9" stroke="#fff" stroke-width="2.4" fill="none"/></svg>`,
    pin: S('<path d="M12 21s-6.5-6.2-6.5-11.2a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21z"/><circle cx="12" cy="9.8" r="2.3"/>'),
    coins: S('<ellipse cx="9" cy="7" rx="6" ry="2.5"/><path d="M3 7v4c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5V7"/><path d="M9 13.5v4c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5v-4c0-1.4-2.7-2.5-6-2.5"/>', '0 0 24 24', 'stroke="#FFCB08" stroke-width="1.5"'),
    bolt: S('<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>', '0 0 24 24', 'stroke="#FFCB08" stroke-width="1.5"'),
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

  /* ---------------- Small helpers ---------------- */
  const rs = (v) => `<span class="rs">₹</span> ${v}`;
  const i = () => `<span class="i">i</span>`;
  const img = (f, cls = '', style = '') => `<img src="${IMG}${f}" class="${cls}" style="${style}" alt="">`;

  /* ---------------- Headers ---------------- */
  const header = (type = 'app') => {
    if (type === 'site') return `
      <header class="hdr site">
        ${logoLink(img('shriram-logo.png'))}
        <nav class="site-nav"><a>About Us</a><a>Product &amp; Services</a><a>Investors</a><a>Learning Lounge</a><a>Careers</a></nav>
        <div class="site-right"><a class="phone" href="tel:+918981003538"><span style="width:15px;height:15px;display:inline-block">${ICON.phone}</span>+91 898-100-3538</a><a class="contact" href="https://www.shriramcredit.in/contact-us">Contact Us</a></div>
      </header>`;
    const right = type === 'logout' ? `<a class="logout" data-logout title="Logout" style="width:22px;height:22px;display:block;cursor:pointer">${ICON.logout}</a>`
      : `<a data-credit title="Credit score" style="cursor:pointer">${ICON.gauge}</a><a data-profile title="Profile" style="cursor:pointer">${ICON.user}</a>`;
    return `<header class="hdr">${logoLink(img('shriram-logo.png'))}<div class="hdr-icons">${right}</div></header>`;
  };

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

  // "How is it calculated" card (Pledgeable Units / Current Value / Credit Limit)
  const calcCard = (f) => `
    <div class="fund-card">${f.ne ? '<div class="ne-strip">Not Eligible</div>' : ''}<div class="body">${fundHead(f)}
      <div class="fund-cols three"><div><div class="lbl">Pledgeable Units</div><div class="val">${f.units}</div></div>
      <div><div class="lbl">Current Value</div><div class="val">${rs(f.value)}</div></div>
      <div><div class="lbl">Credit Limit</div><div class="val">${rs(f.cl)}</div></div></div></div></div>`;

  // MF Selection card. opts: {checked, amount, editing}
  const selectCard = (f, o = {}) => {
    const amt = o.editing
      ? `<span class="amt-edit"><span class="rs">₹</span> ${o.editing}<span class="ok">${ICON.check}</span></span>`
      : `<span class="amt">${rs(o.amount || '0')}<span class="pen">${ICON.pencil}</span></span>`;
    return `
    <div class="fund-card sel-card"><div class="body">
      <div class="sel-top">
        <span class="cbx ${o.checked ? 'on' : ''}">${o.checked ? ICON.check : ''}</span>
        ${fundHead(f, f.sel)}
        <div class="sel-amt"><div class="lbl">Selected Amount ${i()}</div>${amt}</div>
      </div>
      <div class="fund-cols three sel-cols"><div><div class="lbl">No of Units ${i()}</div><div class="val">${f.units}</div></div>
      <div><div class="lbl">Current Value ${i()}</div><div class="val">${rs(f.selValue)}</div></div>
      <div><div class="lbl">Max Limit ${i()}</div><div class="val">${rs(f.cl)}</div></div></div></div></div>`;
  };

  /* ---------------- Modals ---------------- */
  const closeBtn = `<button class="close" aria-label="Close">${ICON.close}</button>`;
  const withModal = (bg, modal, dark) => `<div class="blur-bg">${bg}</div><div class="overlay ${dark ? 'dark' : ''}">${modal}</div>`;
  const loader = (title, variant = 1) => {
    const rows = variant === 1
      ? `<div class="skel-row" style="margin-left:22px"><span class="skel-sq" style="width:44px;height:44px"></span><div style="display:grid;gap:9px"><span class="skel-bar" style="width:90px"></span><span class="skel-bar" style="width:107px"></span></div></div>
         <div class="skel-row dark"><span class="skel-sq" style="width:56px;height:56px"></span><div style="display:grid;gap:12px"><span class="skel-bar" style="width:113px"></span><span class="skel-bar" style="width:139px"></span></div></div>`
      : variant === 2
      ? `<div class="skel-row" style="margin-left:22px"><span class="skel-sq" style="width:44px;height:44px"></span><div style="display:grid;gap:9px"><span class="skel-bar" style="width:90px"></span><span class="skel-bar" style="width:107px"></span></div></div>
         <div class="skel-row dark"><span class="skel-sq" style="width:56px;height:56px"></span><div style="display:grid;gap:12px"><span class="skel-bar" style="width:76px"></span><span class="skel-bar" style="width:2px"></span></div></div>`
      : `<div class="skel-row" style="margin-left:22px"><span class="skel-sq" style="width:44px;height:44px"></span><div style="display:grid;gap:9px"><span class="skel-bar" style="width:90px"></span><span class="skel-bar" style="width:107px"></span></div></div>
         <div class="skel-row dark"><span class="skel-sq" style="width:56px;height:56px"></span><div style="display:grid;gap:12px"><span class="skel-bar" style="width:119px"></span><span class="skel-bar" style="width:66px"></span></div></div>`;
    return `<div class="modal loader-modal"><div class="skel">${rows}</div><h3>${title}</h3><p>This might take a min, thanks for your patience</p></div>`;
  };

  /* ======================================================
     PAGE TEMPLATES
     ====================================================== */
  const T = {};

  /* 01 Landing */
  T.landing = () => `
    ${header('site')}
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
        <label class="chk"><input type="checkbox" id="consent"><span>By proceeding, I agree to <a href="https://www.shriramcredit.in/terms-and-conditions" target="_blank" rel="noopener">T&amp;C</a> and <a href="https://www.shriramcredit.in/privacy-policy" target="_blank" rel="noopener">Privacy Policy</a> of Shriram Credit.</span></label>
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

  /* 04 PAN details */
  T.pan = () => `
    ${header('logout')}
    <main class="pan-bg"><div class="card pan-card">
      <h3>PAN Details</h3><p class="sub">Please verify your PAN to get the best loan offers</p>
      <label class="field-lbl">Mobile Number</label><input class="input readonly" value="${store.get(K.mobile) || CUSTOMER.mobile}" readonly>
      <label class="field-lbl">Name as per PAN <span class="lbl-err" id="pan-name-err"></span></label><input class="input" id="pan-name" maxlength="150" autocomplete="off">
      <label class="field-lbl">DOB <span class="lbl-err" id="pan-dob-err"></span></label><div class="dob"><input class="input" id="pan-dob" placeholder="DD/MM/YYYY" maxlength="10" inputmode="numeric" autocomplete="off"><span id="pan-dob-cal" title="Select date" style="cursor:pointer">${ICON.calendar}</span><input type="date" id="pan-dob-picker" tabindex="-1" aria-hidden="true" style="position:absolute;right:0;bottom:0;width:1px;height:1px;opacity:0;border:0;padding:0"></div>
      <label class="field-lbl">PAN Number <span class="lbl-err" id="pan-no-err"></span></label><input class="input" id="pan-no" placeholder="ABCDE 1234 F" maxlength="12" autocomplete="off">
      <button class="btn btn-primary bold btn-block" data-cta="continue">Continue</button>
    </div></main>`;

  /* 05 Consent page (Check credit limit) */
  T.consent = () => `
    ${header('app')}
    <main class="consent">
      <aside class="c-left">
        <div class="c-top">
          <p class="rate">Interest rates starting from 10.5% p.a.*</p>
          <h2>Get a Loan up to 75% of your eligible Mutual Fund portfolio</h2>
          <p class="pt"><span>${ICON.coins}</span>Interest-only EMI payments</p>
          <p class="pt"><span>${ICON.bolt}</span>Disbursal in 2 hours post application</p>
        </div>
        <div class="c-how"><p class="hw">How it works</p><h4>Apply for loan within mins.</h4>
          <ol>${['Check your eligibility, credit limit, and interest rates.', 'Select mutual fund units to pledge.', 'Complete your KYC verification.', 'Pledge your selected mutual fund units.', 'Your loan amount is approved, Sanction Letter with Key Fact Statement (KFS) is issued.', 'e-Sign the loan agreement.', 'Your loan account is ready to use.', 'Withdraw funds as needed.', 'Repay the loan at your convenience and regain complete control of your mutual fund holdings.']
            .map((t, k) => `<li><b>0${k + 1}</b><span>${t}</span></li>`).join('')}</ol></div>
      </aside>
      <section class="c-right"><div class="card cl-card">
        <h3>Credit Limit Against Mutual Fund</h3>
        <p class="sub">Mutual fund will be fetched from MF Central to determine the eligible credit limit and best loan offers</p>
        <label class="field-lbl">PAN Number</label><input class="input readonly" value="${CUSTOMER.pan}" readonly>
        <label class="chk sm"><input type="checkbox"><span>I authorize Shriram Credit to fetch my mutual fund portfolio holdings from MF Central to assess my eligibility and credit limit for a Loan Against Mutual Funds.</span></label>
        <button class="btn btn-disabled btn-block" data-cta="check-credit-limit">Check Credit Limit</button>
      </div></section>
    </main>`;

  /* 06 MF Central redirect modal */
  T.mfcModal = () => `
    <div class="modal m-mfc">${closeBtn}
      ${img('mfcentral-logo.png', 'mfc-logo')}
      <p class="redir">Redirecting to MF Central in <span id="mfc-sec">5</span> seconds</p>
      <div class="prog"><span></span></div>
      <h4>Here’s what you need to do</h4>
      <div class="todo"><span>1</span><p>Enter the 6-digit OTP received from MF Central on your mobile number.</p></div>
      <div class="todo"><span>2</span><p>Select all the AMCs and continue</p></div>
      <div class="note"><b>Note</b> You’ll return to the process automatically after completing this step.</div>
    </div>`;

  /* 07 Prototype only (DISC-157, DISC-158): stands in for MF Central's check of the PAN and mobile number combination */
  T.dataMockModal = () => `
    <div class="modal pan-mock">
      <span class="sim-tag">Prototype only</span>
      <h3>Mock MF Central Data Check</h3>
      <p>For review only: choose whether MF Central has data for this PAN and mobile number.</p>
      <div class="pan-mock-btns">
        <button class="btn btn-primary bold" data-r="yes">Data available</button>
        <button class="btn btn-outline" data-r="no">Data not available</button>
      </div></div>`;

  /* 07.1 PAN and mobile number combination – no data available (DISC-157) */
  T.notLinked = () => `
    ${header('app')}
    <main><div class="card nl-card">
      ${img('mfc-not-linked.png', 'nl-art')}
      <p class="nl-t">The identifier below isn’t linked to the PAN you entered</p>
      <div class="nl-row"><span class="nl-ph">${ICON.phone}</span><b id="nl-mobile">${CUSTOMER.mobileMasked2}</b>
        <a class="nl-ref" data-cta="refresh"><span>${ICON.refresh}</span>Refresh</a></div>
    </div></main>`;

  /* 07 MF Central mock */
  /* 07.2 – 07.5 MF Central pages (DISC-159) – laid out as in the owner's UAT screenshots; OTP 000000 in the prototype */
  const mfcLogo = img('mfc-wordmark.png', 'mfc-wm');
  T.mfMock = () => `
    <main class="mfc-page"><div class="mfc-col">
      ${mfcLogo}
      <div class="mfc-use"><div class="mfc-use-h"><span class="mfc-ring"></span><div><small>Usecase:</small><b>Loan Against Mutual Funds</b></div></div>
        <p>By authenticating, you authorize <b>requesting platform</b> registered with SEBI/RBI to securely access your mutual fund portfolio data from MF Central for <b>Loan Against Mutual Funds</b></p></div>
      <div class="mfc-box mock-card">
        <p class="mfc-otp-l"><span class="mfc-shield">⛨</span> Enter your 6-digit OTP</p>
        <div class="otp mfc-otp" style="justify-content:center">${'<input maxlength="1" inputmode="numeric">'.repeat(6)}</div>
        <p class="otp-hint" style="margin:12px auto 0">Please use OTP <b>${OTP_RULES.demoOtp}</b> to proceed</p>
        <p class="field-err" id="demo-otp-err" style="text-align:center"></p>
        <button class="mfc-btn" data-cta="submit">Authenticate with OTP</button>
      </div>
      <div class="mfc-box mfc-sec"><h4><span class="mfc-shield blue">⛨</span> Secure Authentication for Portfolio Access</h4>
        <ul><li><i class="r">!</i>We do not store your OTP or sensitive credentials</li>
        <li><i class="s">★</i>Data is end to end encrypted and securely shared only on authentication of OTP by Investor</li>
        <li><i class="g">i</i>Access is limited to Personal Finance Management only</li>
        <li><i class="t">✓</i>Consent artifact is valid for one time data sharing</li>
        <li><i class="t">✓</i>MF Central follows an every time consent model for sharing the data</li></ul></div>
    </div></main>`;

  const AMCS = [['amc-dsp.png', 'DSP Mutual Fund', '₹20,008.48'], ['amc-hdfc.png', 'HDFC Mutual Fund', '₹88.9'], ['amc-ppfas.png', 'PPFAS Mutual Fund', '₹972.45'], ['amc-shriram.png', 'Shriram Mutual Fund', '₹0']];
  T.mfcAmc = () => `
    <main class="mfc-page"><div class="mfc-card amc-card">
      ${mfcLogo}
      <span class="mfc-pill">▭ Usecase: Loan Against Mutual Funds</span>
      <h3>Select AMCs for Loan Assessment</h3>
      <label class="amc-all"><input type="checkbox" id="amc-all"><span>Select All AMCs</span></label>
      ${AMCS.map(([lg, n, v], k) => `<label class="amc-row"><input type="checkbox" data-amc="${k}"><span class="amc-box">${img(lg, 'amc-lg')}<b>${n}</b><span class="amc-v"><small>MARKET VALUE</small>${v}</span></span></label>`).join('')}
      <button class="mfc-btn2" data-cta="continue" disabled>Continue to Portfolio Import</button>
    </div></main>`;

  T.mfcFetching = () => `
    <main class="mfc-page">${mfcLogo}<div class="mfc-grad-panel"><div class="mfc-card mfc-center fetch-card">
      ${img('mfc-fetch.png', 'mfc-fetch-ic')}
      <h2>Fetching Your Portfolio...</h2>
      <p>Connecting to MF Central and<br>fetching your investment data</p>
      <div class="mfc-step"><span>Connecting to MF Central</span><i class="spin"></i><div class="bar p"><b></b></div></div>
      <div class="mfc-step"><span>Fetching your portfolio</span><i>⛉</i><div class="bar g"><b></b></div></div>
      <p class="mfc-proc"><i></i><i></i><i></i> Processing portfolio data</p>
      <p class="mfc-foot"><i class="g"></i>256-bit encryption <i></i>ISO 27001 compliant</p>
    </div></div></main>`;

  T.mfcDone = () => `
    <main class="mfc-page mfc-grad">${mfcLogo}<div class="mfc-card mfc-center done-card">
      ${img('mfc-success.png', 'mfc-ok')}
      <h2>Portfolio Discovery Complete!</h2>
      <p>Your mutual fund portfolio has been successfully fetched and will now be sent to the Requested Platform.</p>
      <div class="mfc-okbar"><span>✓</span><div><b>Data fetched successfully</b><small>All portfolio information secured</small></div></div>
      <div class="mfc-redir">Redirecting in <span id="mfc-left">3</span>s →</div>
      <p class="mfc-foot"><i class="g"></i>256-bit encryption <i></i>ISO 27001 compliant</p>
    </div></main>`;

  /* 08 Redirecting */
  T.redirecting = () => `${header('app')}<p class="redirecting">Redirecting to Dashboard...</p>`;

  /* 12 Curated offers */
  T.curated = (o = {}) => `
    ${header('app')}
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

  /* 12.1.x How is it calculated */
  T.calc = (tab = 'all') => {
    const byCL = (a, b) => parseInt(b.cl.replace(/,/g, '')) - parseInt(a.cl.replace(/,/g, ''));
    const list = tab === 'all' ? FUNDS : tab === 'eligible' ? FUNDS.filter((f) => !f.ne).sort(byCL) : FUNDS.filter((f) => f.ne);
    const n = tab === 'all' ? 13 : tab === 'eligible' ? 9 : 4;
    const tabBtn = (k, l) => `<button class="tab ${tab === k ? 'on' : ''}" data-cta="tab-${k}">${l}</button>`;
    return `
    ${header('app')}
    <div class="wrap-980"><a class="back" data-cta="back">${ICON.back}Loan Against Mutual Funds</a></div>
    <main class="wrap-680 calc">
      <div class="cl-hero"><div><p>Your maximum credit limit is</p><h2>${rs(PORTFOLIO.creditLimit)}</h2></div>${img('coins.png', 'coins')}</div>
      <p class="cl-desc">We determine your credit limit based on your eligible mutual fund portfolio and our lending policies. This is the maximum amount you can borrow.</p>
      <div class="cl-rows">
        <div><b>Total Portfolio Value</b><b>${rs(PORTFOLIO.total)}</b></div>
        <div><span>Non-Eligible Portfolio Value</span><span>- ${rs(PORTFOLIO.nonEligible)}</span></div>
        <div><span>Eligible Portfolio Value</span><span>${rs(PORTFOLIO.eligible)}</span></div>
        <div><span>Credit Limit Available</span><span>${rs(PORTFOLIO.creditLimit)}</span></div>
      </div>
      <div class="tabs">${tabBtn('all', 'All')}${tabBtn('eligible', 'Eligible Portfolio')}${tabBtn('ne', 'Non-Eligible Portfolio')}</div>
      <div class="mobile-strip sm"><span>${CUSTOMER.mobileMasked2}</span><span>${n} Security</span></div>
      ${list.map(calcCard).join('')}
    </main>`;
  };

  /* 12.2 Refresh portfolio modal */
  T.refreshModal = () => `
    <div class="modal m-refresh">${closeBtn}
      <h3>Refresh all linked portfolios to continue</h3>
      <p>Please refresh your portfolio to view the current value of your investments and continue with the application.</p>
      <div class="rf-box"><div><b>${CUSTOMER.mobileMasked2}</b><span>Last refreshed Today</span></div><a class="link-yellow" data-cta="refresh-portfolio">Refresh Portfolio</a></div>
    </div>`;

  /* 13.x MF Selection. o = {loan, sliderPct, editLoan, mv, count, selected:{id:amt}, editing:{id:val}, ctaDisabled, cta} */
  const SEL_ORDER = ['icici', 'axis', 'kotak', 'nippontw', 'whiteoak', 'hsbc', 'ednifty', 'canara', 'sbi'];
  T.selection = (o = {}) => {
    const sel = o.selected || {};
    return `
    <div class="sticky-top">${header('app')}${stepper(1)}</div>
    <main class="wrap sel-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <div class="loan-box">
        <p class="lb-t">Loan Amount</p>
        ${o.editLoan
          ? `<div class="lb-edit"><span class="rs">₹</span><input value="${o.editLoan}"><a class="link-yellow" data-cta="update-loan">Update</a></div>`
          : `<p class="lb-v">${rs(o.loan || '2,00,00,000')} <span class="pen">${ICON.pencilSolid}</span></p>`}
        <div class="slider"><div class="track"><span class="fill" style="width:${o.sliderPct ?? 100}%"></span><span class="knob" style="left:${o.sliderPct ?? 100}%"></span></div>
          <div class="ends"><span>${rs('10,000')}</span><span>${rs('2,00,00,000')}</span></div></div>
      </div>
      <h2 class="fs-t">Funds selected for pledging</h2>
      <p class="fs-s">Current market value of units selected for pledging <b>${rs(o.mv || '2,66,66,667.21')}</b> <span class="gap"></span>No. of funds selected <b>${o.count ?? 3}</b></p>
      <label class="sel-all"><span class="cbx part"><i></i></span>Select All</label>
      <div class="mobile-strip"><span>${CUSTOMER.mobileMasked2}</span><span>9 Fund<span class="dotsep">•</span>${rs(PORTFOLIO.eligible)}</span></div>
      ${SEL_ORDER.map((id) => selectCard(F[id], { checked: id in sel || (o.editing && id in o.editing), amount: sel[id], editing: o.editing && o.editing[id] })).join('')}
      <div style="height:30px"></div>
    </main>
    <div class="cta-bar"><button class="btn ${o.ctaDisabled ? 'btn-disabled' : 'btn-primary'}" data-cta="continue-to-apply">Continue to apply ${rs(o.cta || '2,00,00,000')}</button></div>`;
  };
  const SEL_DEFAULT = { selected: { icici: '1,40,30,794', axis: '53,69,420', kotak: '5,99,786' } };

  T.locationPopup = () => `
    <div class="perm"><span class="x">✕</span><div class="t">uatlamf.shriramcredit.in wants to</div>
      <div class="row"><span style="width:16px;height:16px;display:block">${ICON.pin}</span>Know your location</div>
      <div class="btns"><button data-cta="loc-block">Block</button><button data-cta="loc-once">Just this Time</button><button data-cta="loc-allow">Allow</button></div></div>`;

  T.locationToast = () => `<div class="toast"><span class="ico">i</span>Kindly provide location access in order to proceed with the loan application. <a class="link-yellow" data-cta="refresh">Refresh</a></div>`;

  T.ongoingModal = () => `
    <div class="modal m-ongoing"><p>You have an ongoing loan application, would you like to proceed further with it?</p>
      <div class="two"><button class="btn btn-outline" data-cta="go-dashboard">No, Take me to the dashboard</button><button class="btn btn-primary" data-cta="yes-continue">Yes, Continue</button></div></div>`;

  /* 14 Summary */
  T.summary = () => `
    <div class="sticky-top">${header('app')}${stepper(1)}</div>
    <main class="wrap sum-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <div class="wrap-840 sum">
        <h3>Application details</h3>
        <div class="sum-box"><div><span>Loan amount</span><b>${rs('1,55,36,100')}</b></div><div style="text-align:right"><span>Pledge Value</span><b>${rs('2,07,14,800.22')}</b></div></div>
        <div class="kv big"><b>Tenure</b><span>12 months</span></div>
        <div class="kv big"><b>Disbursement Type</b><span>Multiple</span></div>
        <div class="kv big"><b>Repayment Type</b><span>Interest Only</span></div>
        <div class="sum-2"><div><span>Interest Rate ${i()}</span><em>10.5% p.a</em></div><div><span>Monthly Interest ${i()}</span><em>${rs('1,35,940.88')}</em></div></div>
        <h3>Charges (Inclusive of GST)</h3>
        <div class="kv"><span class="g">Processing fee ${i()}</span><em>${rs('91,664')}</em></div>
        <div class="kv"><span class="g">Stamp duty ${i()}</span><span>${rs('236')}</span></div>
        <div class="kv"><span class="g">Lien Marking Charges ${i()}</span><span>${rs('531')}</span></div>
        <div class="kv"><span class="g">Lien Removal Charges ${i()}</span><span>${rs('118')}</span></div>
        <h3>Repayment details</h3>
        <div class="kv"><span class="g">Interest autopay</span><span>5th of every month</span></div>
      </div>
      <div style="height:30px"></div>
    </main>
    <div class="cta-bar"><button class="btn btn-primary" style="width:178px" data-cta="continue">Continue</button></div>`;

  /* 16.x KYC. o = {email:'input'|'filled'|'done', aadhaar:'pending'|'start'|'status'|'done', photo:'pending'|'start'} */
  const kycRow = (n, title, state, extra = '') => {
    const done = state === 'done';
    const badge = state === 'done' ? '<span class="badge complete">Complete</span>' : state === 'pending' ? '<span class="badge pending">Pending</span>' : '';
    return `<div class="kyc-row ${state === 'pending' || done ? '' : 'open'}">
      <div class="kyc-h"><span class="kn ${done ? 'done' : state !== 'pending' ? 'act' : ''}">${done ? ICON.check : n}</span><span class="kt">${title}</span>${badge}</div>${extra}</div>`;
  };
  const DL = img('digilocker-logo.png', 'dl-inline');
  T.kyc = (o = {}) => {
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
    return `
    <div class="sticky-top">${header('app')}${stepper(2)}</div>
    <main class="wrap kyc-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <div class="loan-strip">Your loan amount is ${rs('1,55,36,100')} <a class="link-yellow sm" data-cta="view-details">View details</a></div>
      <h1 class="kyc-title">KYC Verification <small>This step is required as per our lending guidelines.</small></h1>
      ${kycRow(1, 'Email Verification', email === 'done' ? 'done' : 'open', emailExtra)}
      ${kycRow(2, 'PAN Verification', 'done')}
      ${kycRow(3, 'Aadhaar Verification with ' + DL, aad === 'done' ? 'done' : aad === 'pending' ? 'pending' : 'open', aadExtra)}
      ${kycRow(4, 'Photo Verification', photo === 'start' ? 'open' : 'pending', photoExtra)}
      ${kycRow(5, 'Bank Details', 'pending')}
    </main>`;
  };

  /* 16.2 Loan details popup */
  const ldCard = (f, u, cv, sa, ml) => `
    <div class="fund-card"><div class="body">
      <div class="sel-top">${fundHead(f, f.sel)}<div class="sel-amt"><div class="lbl">Selected Amount ${i()}</div><span class="amt">${rs(sa)}</span></div></div>
      <div class="fund-cols three sel-cols" style="margin-left:0"><div><div class="lbl">Selected Units ${i()}</div><div class="val">${u}</div></div>
      <div><div class="lbl">Current Value ${i()}</div><div class="val">${rs(cv)}</div></div>
      <div><div class="lbl">Max Limit ${i()}</div><div class="val">${rs(ml)}</div></div></div></div></div>`;
  T.loanDetailsModal = () => `
    <div class="modal m-ld">${closeBtn}
      <h3>Loan details</h3>
      <div class="ld-3"><div><span>Loan Amount</span><b>${rs('1,55,36,100')}</b></div><div><span>Market Value of MF selected</span><b>${rs('2,07,14,799.99')}</b></div><div><span>No. of MF selected</span><b>2</b></div></div>
      <h3>Mutual Fund selected for pledging</h3>
      ${ldCard(F.icici, '93001.86', '1,87,07,725.33', '1,40,30,794', '1,40,30,794')}
      ${ldCard(F.axis, '19033.17', '20,07,074.66', '15,05,306', '53,69,420')}
    </div>`;

  /* 16.3 Email OTP popup */
  T.emailOtpModal = () => `
    <div class="modal m-eotp">
      <h3>Enter OTP</h3>
      <p class="sent">A 6-digit OTP has been sent to your registered email address<br><b>${CUSTOMER.email}</b></p>
      <div class="otp big">${'<input maxlength="1" inputmode="numeric">'.repeat(6)}</div>
      <p class="otp-hint">Please use OTP <b>${OTP_RULES.demoOtp}</b> to proceed</p>
      <p class="field-err" id="demo-otp-err"></p>
      <p class="resend">Didn’t receive OTP? <b>0:29</b> <span class="mut">Resend OTP</span></p>
      <button class="btn btn-disabled btn-block" data-cta="submit-otp">Submit OTP</button>
    </div>`;

  /* 16.5.1 / 16.5.5 Digio gateway (simulated third-party screen) */
  T.digio = (fetching) => `
    <main class="digio-bg"><div class="digio">
      <div class="dg-h">${img('digio-logo.png', '', 'height:30px')}<span class="dg-r">${img('digio-icons.png', '', 'height:30px')}<span class="sec">Secured by <b>digio</b></span></span></div>
      <div class="dg-body ${fetching ? 'dim' : ''}">
        ${img('digio-digilocker.png', 'dg-dl')}
        <h4>${fetching ? 'Securely fetching documents' : 'Steps to securely fetch documents'}</h4>
        <div class="dg-steps">
          <div class="dg-s">${img('digio-step1.png')}<b>Enter Aadhaar number</b></div>
          <div class="dg-s">${img('digio-step2.png')}<b>Enter OTP and PIN (optional)</b></div>
          <div class="dg-s top">${img('digio-step3.png')}<div><b>Select requested documents:</b>
            <div class="dg-docs"><span class="blue">Issued Documents &nbsp;(2)</span><span class="sa">Select All <i class="cb b ${fetching ? '' : 'on'}"></i></span>
            <span>Aadhaar Card</span><i class="cb g on"></i><span>PAN Verification Record</span><i class="cb g on"></i></div></div></div>
          <div class="dg-s">${img('digio-step4.png')}<b>Document fetch from DigiLocker</b></div>
        </div>
        ${fetching ? '' : `
        <div class="dg-req"><div class="rq"><b>Requested:</b> Aadhaar Card <span class="sep"></span> PAN Card</div>
          <div class="consent-txt">I provide my consent to share my Aadhaar Number, Date of Birth and Name from my Aadhaar eKYC information with the Income Tax Department, All States for the purpose of fetching my PAN Verification Record into DigiLocker.</div></div>`}
      </div>
      ${fetching ? `<div class="dg-fetch">${img('digio-fetch.png', 'spin-img')}<h4>Securely fetching documents</h4><p>Please do not refresh or close the window</p></div>`
        : `<div class="dg-auth"><label><i class="cb b on"></i><span>By proceeding further I hereby authorize Digio to pull my documents from Digilocker and share with <b class="blue">SHRIRAM CREDIT COMPANY LIMITED</b></span></label></div>
           <div class="dg-btns"><button class="dg-cancel" data-cta="cancel">Cancel</button><button class="dg-proceed" data-cta="proceed">Proceed</button></div>`}
    </div></main>`;

  /* 16.5.2 – 16.5.4 DigiLocker (simulated third-party screen) */
  T.digilocker = (step) => {
    let card;
    if (step === 'aadhaar') card = `
      <h3>Sign up</h3><p class="dlm">It takes just a minute</p>
      <div class="dl-lbl"><span>Enter your Aadhaar Number</span>${img('aadhaar-logo.png', '', 'height:22px')}</div>
      <div class="dl-aad"><input placeholder="_ _ _ _" maxlength="4"><input placeholder="_ _ _ _" maxlength="4"><input placeholder="_ _ _ _" maxlength="4"></div>
      <p class="dlm2">DigiLocker uses Aadhaar to enable authentic document access</p>
      <button class="dl-btn" data-cta="next">Next</button>`;
    else if (step === 'otp') card = `
      <h3>Verify Aadhaar OTP</h3>
      <div class="dl-ok">DigiLocker has sent you an OTP to your registered mobile (xxxxxx1623)</div>
      <p class="dl-b">Please enter OTP to complete verification</p>
      <input class="dl-in" maxlength="6" inputmode="numeric">
      <p class="otp-hint">Please use OTP <b>${OTP_RULES.demoOtp}</b> to proceed</p>
      <p class="field-err" id="demo-otp-err"></p>
      <p class="dlm3">Didn't receive OTP? Wait few minutes for the OTP to arrive. Do not refresh or close!</p>
      <button class="dl-btn" data-cta="submit">Submit</button>
      <p class="dl-c">Didn’t get the OTP? <span>Resend OTP</span></p>`;
    else card = `
      <h3 style="margin-bottom:6px">You are already registered with DigiLocker</h3>
      <p class="dlm3" style="font-size:14px;margin:0 0 14px">6 digit PIN provides extra security to your account with two factor authentication. Don't disclose your Security PIN to anyone.</p>
      <p class="dl-b">Please enter your 6 digit Security PIN to Signin</p>
      <div class="dl-pin">${'<input maxlength="1" type="password">'.repeat(6)}<span class="eye">👁</span></div>
      <a class="dl-link">Forgot my PIN</a>
      <button class="dl-btn" data-cta="done">Done</button>`;
    const below = step === 'aadhaar' ? '<a class="dl-under">Try another way</a>' : step === 'otp' ? '<a class="dl-under blue2">Create your account using mobile</a>' : '';
    return `<main class="dl-bg"><div class="dl-top">${img('digilocker-header.png', '', 'height:36px;mix-blend-mode:multiply')}</div>
      <div class="dl-card dls-${step}">${card}</div>${below}</main>`;
  };

  /* 16.5.6 Digio exit */
  T.digioExit = () => `<main class="exit-bg"><div class="exit"><span class="ok-c">${ICON.check}</span><p>KYC process completed</p><small>Do not close the window. You will be redirected.</small></div></main>`;

  /* 16.5.7 LOS auto redirect */
  T.kycRedirect = () => `<main class="kyc-redir">${img('kyc-success.png', '', 'height:72px;mix-blend-mode:multiply')}<h4>KYC successfully completed.</h4><p>Redirecting you back to the process in 1 seconds</p></main>`;

  /* ==========================================================
     FLOW – which CTA on which screen opens which screen.
     One line per rule:  'screen name': { 'cta name': 'target screen name' }
     CTA names are the data-cta="..." values in the templates above.
     ========================================================== */
  const FLOW = {
    '01) LAMF Landing Page': {
      // Both landing CTAs start the LAMF journey at the mobile number step
      'check-eligibility': '02) Enter MF linked Mobile Number',
      'start-application': '02) Enter MF linked Mobile Number',
    },
  };

  const currentScreen = () => (SPA()
    ? decodeURIComponent(location.hash.replace(/^#/, ''))
    : decodeURIComponent(location.pathname.split('/').pop()).replace(/\.html$/, ''));
  const go = (screen) => {
    if (SPA()) { location.hash = encodeURIComponent(screen); return; }   // router re-renders
    location.href = href(screen);
  };

  /* ==========================================================
     BEHAVIOUR – per screen field logic and validations.
     ========================================================== */
  /* Small storage helper – keeps the entered mobile number and the OTP
     attempt/block state so they survive navigation and page refresh. */
  const K = { mobile: 'lamf.mobile', otp: 'lamf.otp', returning: 'lamf.returning' };
  const store = {
    get(k, d = null) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } },
  };
  /* Mask as shown in the journey: +91 + first 2 digits + XXXX + last 4 */
  const maskMobile = (m) => (m && m.length === 10 ? `+91${m.slice(0, 2)}XXXX${m.slice(6)}` : CUSTOMER.mobileMasked);

  /* OTP rules (DISC-013) */
  const OTP_RULES = {
    length: 6,
    resendSeconds: 30,        // timer runs 0:30 → 0:01, then Resend OTP is enabled
    validitySeconds: 30,      // an OTP is valid for 30 seconds after it is sent (P-04)
    maxResend: 3,             // 3 back-to-back resends
    resendBlockMin: 15,       // then blocked for 15 minutes
    maxWrong: 3,              // 3 wrong OTP attempts
    wrongBlockMin: 60,        // then blocked for 60 minutes
    demoOtp: '000000',        // prototype only – the live journey uses the real OTP; here only 000000 is accepted (DISC-156)
  };
  // Current live LOS messages (PRD Sl. No 3, DISC-106)
  const OTP_ERR = {
    wrong: 'Invalid OTP',
    expired: 'Invalid request id',   // OTP submitted after 30 seconds (current live wording, CR-09)
    wrongBlocked: (m) => `Maximum OTP retry limit reached. Please retry again after ${m} minute(s).`,
    resendBlocked: (m) => `Error: Maximum OTP resend limit reached. Please retry again after ${m} minute(s).`,
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
        cta.setAttribute('aria-disabled', String(!consent.checked));
      };
      consent.addEventListener('change', () => { sync(); if (consent.checked) showErr(err.textContent === MOBILE_ERR.consent ? '' : err.textContent); });
      sync();

      // T&C / Privacy Policy open the Shriram Credit pages in a new tab (DISC-090)

      // Coming back from the OTP screen via Edit: prefill what the user entered
      const saved = store.get(K.mobile);
      if (saved) input.value = saved;

      // Continue: check every rule before moving on
      cta.addEventListener('click', () => {
        const v = input.value;
        if (!consent.checked) return;   // grey CTA cannot be clicked, so no validation is shown (DISC-089)
        if (!v) return showErr(MOBILE_ERR.empty);
        if (!/^[6-9]/.test(v)) return showErr(MOBILE_ERR.start);
        if (v.length !== 10) return showErr(MOBILE_ERR.length);
        showErr('');
        store.set(K.mobile, v);                                   // carried to the OTP screen
        customerMock();
      });

      // Prototype only (DISC-129): stands in for the LOS check of whether this mobile number has already
      // verified an OTP before, so both Enter OTP variants can be tried. Not part of the PRD.
      const customerMock = () => {
        document.body.insertAdjacentHTML('beforeend', `<div class="overlay pan-mock-ov"><div class="modal pan-mock">
          <button class="close" data-x title="Close">${ICON.close}</button>
          <span class="sim-tag">Prototype only</span>
          <h3>Mock Customer Check</h3>
          <p>Choose the customer type to see the matching Enter OTP pop up.</p>
          <div class="pan-mock-btns">
            <button class="btn btn-primary bold" data-r="new">New customer – first OTP verification</button>
            <button class="btn btn-outline" data-r="returning">Existing customer – OTP already verified</button>
          </div></div></div>`);
        const ov = document.querySelector('.pan-mock-ov');
        const close = () => ov.remove();
        ov.querySelector('[data-x]').onclick = close;
        ov.querySelectorAll('[data-r]').forEach((bt) => { bt.onclick = () => {
          store.set(K.returning, bt.dataset.r === 'returning');
          close();
          go('03) Enter OTP for MF linked Mobile Number Verification');
        }; });
      };
    },

    /* ---- 03 Enter OTP for MF linked Mobile Number Verification ---- */
    '03) Enter OTP for MF linked Mobile Number Verification': () => {
      const modal = document.querySelector('.m-otp');
      const boxes = [...modal.querySelectorAll('.otp input')];
      const err = document.getElementById('otp-err');
      const consent = document.getElementById('experian-consent');
      // A customer who has already verified the OTP before does not see the Experian consent checkbox (DISC-129)
      if (store.get(K.returning)) { consent.checked = true; consent.closest('label').style.display = 'none'; }
      const cta = modal.querySelector('[data-cta="submit-otp"]');
      const resendSlot = document.getElementById('resend');

      const mobile = store.get(K.mobile) || CUSTOMER.mobile;
      document.getElementById('otp-mobile').textContent = maskMobile(mobile);

      // Blocks are kept against the mobile number (they survive closing the pop up).
      // The wrong-attempt and resend counts are back to back in this pop up only: closing it starts again at 1 (DISC-100).
      const key = `${K.otp}.${mobile}`;
      let st = store.get(key, {});
      st = { wrongUntil: st.wrongUntil || 0, resendUntil: st.resendUntil || 0 };
      const save = () => store.set(key, st);
      let wrong = 0, resends = 0;
      const minsLeft = (until) => Math.max(1, Math.ceil((until - Date.now()) / 60000));   // N = time left in the block

      const showErr = (msg) => { err.textContent = msg || ''; boxes.forEach((b) => b.classList.toggle('has-err', !!msg)); };
      const otpValue = () => boxes.map((b) => b.value).join('');

      // Submit is enabled only when 6 digits are entered AND the consent is ticked
      const sync = () => {
        const ok = otpValue().length === OTP_RULES.length && consent.checked;
        cta.classList.toggle('btn-primary', ok);
        cta.classList.toggle('bold', ok);
        cta.classList.toggle('btn-disabled', !ok);
        cta.setAttribute('aria-disabled', String(!ok));
      };

      // ---- resend timer ----
      let tick = null;
      const stopTick = () => { if (tick) { clearInterval(tick); tick = null; } };
      let sentAt = Date.now();                     // when the current OTP was sent
      const startTimer = () => {
        stopTick();
        sentAt = Date.now();
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
        tick = setInterval(paint, 1000); TIMERS.push(tick);
      };

      // Resend OTP can be clicked 3 times back to back; the next click blocks resending for 15 minutes
      const onResend = () => {
        if (st.resendUntil > Date.now()) return showErr(OTP_ERR.resendBlocked(minsLeft(st.resendUntil)));
        if (resends >= OTP_RULES.maxResend) {
          st.resendUntil = Date.now() + OTP_RULES.resendBlockMin * 60000; save();
          resends = 0;
          return showErr(OTP_ERR.resendBlocked(minsLeft(st.resendUntil)));
        }
        resends += 1;
        boxes.forEach((b) => { b.value = ''; });
        showErr(''); sync();
        startTimer();                                // OTP sent again, timer restarts
      };

      // ---- OTP boxes: numeric only, one digit each, max 6; other characters simply cannot be entered (no message) ----
      boxes.forEach((box, idx) => {
        box.addEventListener('keydown', (e) => {
          if (e.key === 'Backspace' && !box.value && boxes[idx - 1]) { boxes[idx - 1].focus(); return; }
          if (e.key.length > 1 || e.ctrlKey || e.metaKey) return;
          if (!/[0-9]/.test(e.key)) e.preventDefault();
        });
        box.addEventListener('input', () => {
          const digits = box.value.replace(/\D/g, '');
          if (digits.length > 1) {                   // pasted OTP → spread across the boxes
            digits.slice(0, OTP_RULES.length - idx).split('').forEach((d, k) => { if (boxes[idx + k]) boxes[idx + k].value = d; });
            const last = Math.min(idx + digits.length, OTP_RULES.length) - 1;
            boxes[last].focus();
          } else {
            box.value = digits;
            if (digits && boxes[idx + 1]) boxes[idx + 1].focus();
          }
          sync();
        });
      });

      consent.addEventListener('change', sync);

      // Close icon → landing page. Edit → back to the mobile number screen (prefilled).
      modal.querySelector('.close').onclick = () => go('01) LAMF Landing Page');
      modal.querySelector('[data-cta="edit-mobile"]').onclick = () => go('02) Enter MF linked Mobile Number');

      // ---- Submit OTP ----
      cta.addEventListener('click', () => {
        const v = otpValue();
        // grey CTA (fewer than 6 digits or no consent) cannot be clicked, so no validation is shown (DISC-097)
        if (v.length !== OTP_RULES.length || !consent.checked) return;
        // after 3 back to back wrong OTPs the customer is blocked for 60 minutes; shown on the next attempt
        if (st.wrongUntil > Date.now()) return showErr(OTP_ERR.wrongBlocked(minsLeft(st.wrongUntil)));
        if (Date.now() - sentAt > OTP_RULES.validitySeconds * 1000) return showErr(OTP_ERR.expired);   // OTP expired

        if (v !== OTP_RULES.demoOtp) {               // wrong OTP → "Invalid OTP" (1st, 2nd and 3rd attempt)
          wrong += 1;
          if (wrong >= OTP_RULES.maxWrong) {
            st.wrongUntil = Date.now() + OTP_RULES.wrongBlockMin * 60000; save();
            wrong = 0;
          }
          boxes.forEach((b) => { b.value = ''; });
          boxes[0].focus();
          sync();
          return showErr(OTP_ERR.wrong);
        }

        // All conditions met: mobile verified, consent given.
        // Experian credit-score API would be called here with the mobile number (INT-001);
        // the customer continues to PAN verification without waiting for the score.
        st = { wrongUntil: 0, resendUntil: 0 }; save();
        showErr('');
        go('04) Enter PAN Details');
      });

      // initial state
      startTimer();
      sync();
    },

    '04) Enter PAN Details': () => {
      // Current live behaviour (PRD Sl. No 4, DISC-110). Messages other than “*Required” are prototype wording until the
      // live wording is confirmed (P-17).
      const name = document.getElementById('pan-name'), dob = document.getElementById('pan-dob'), pan = document.getElementById('pan-no');
      const picker = document.getElementById('pan-dob-picker');
      const err = (el, msg) => { document.getElementById(el.id + '-err').textContent = msg || ''; el.classList.toggle('has-err', !!msg); };
      const pad = (n) => String(n).padStart(2, '0');
      const today = new Date(); today.setHours(0, 0, 0, 0);
      const iso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
      picker.min = '1920-01-01'; picker.max = iso(today);

      // Name as per PAN: alphanumeric (and spaces), up to 150 characters
      name.addEventListener('input', () => { name.value = name.value.toUpperCase().replace(/[^A-Z ]/g, '').slice(0, 150); err(name, ''); });   // alphabets and space only, captured in capitals (CR-14)
      // DOB: numbers only, typed as DD/MM/YYYY (slashes added automatically) or picked from the calendar icon
      dob.addEventListener('input', () => {
        const d = dob.value.replace(/\D/g, '').slice(0, 8);
        dob.value = d.length > 4 ? `${d.slice(0, 2)}/${d.slice(2, 4)}/${d.slice(4)}` : d.length > 2 ? `${d.slice(0, 2)}/${d.slice(2)}` : d;
        err(dob, d.length === 8 && !dobInRange(dob.value) ? '*Invalid date' : '');   // red as soon as a full date outside 01-Jan-1920 – today is typed (DISC-119)
      });
      document.getElementById('pan-dob-cal').onclick = () => { try { picker.showPicker(); } catch (e) { picker.focus(); picker.click(); } };
      picker.addEventListener('change', () => { if (!picker.value) return; const [y, m, d] = picker.value.split('-'); dob.value = `${d}/${m}/${y}`; err(dob, ''); });
      // PAN (DISC-111): each character must fit its position – 1–5 letters with the 4th always P (individual PAN only),
      // 6–9 numbers, 10th a letter. A character that does not fit is not entered and the message for that position is
      // shown straight away – CR-11 wording (DISC-116). Shown as ABCDE 1234 F.
      const ORD = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th'];
      const PAN_RULE = (i, c) => i === 3 ? (c === 'P' ? '' : 'The 4th character must be (P) – only individual PAN is allowed.')   // only P (individual PAN) – CR-18
        : i >= 5 && i < 9 ? (/[0-9]/.test(c) ? '' : `${ORD[i]} character must be a number (0–9).`)
        : (/[A-Z]/.test(c) ? '' : `${ORD[i]} character must be a letter (A–Z).`);
      pan.addEventListener('input', () => {
        let kept = '', msg = '';
        for (const c of pan.value.toUpperCase().replace(/\s/g, '')) {
          if (kept.length >= 10) break;
          const why = PAN_RULE(kept.length, c);
          if (why) { msg = why; continue; }
          kept += c;
        }
        pan.value = kept.length > 9 ? `${kept.slice(0, 5)} ${kept.slice(5, 9)} ${kept.slice(9)}` : kept.length > 5 ? `${kept.slice(0, 5)} ${kept.slice(5)}` : kept;
        err(pan, msg);
      });

      const parseDob = (v) => {
        const m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(v); if (!m) return null;
        const d = new Date(+m[3], +m[2] - 1, +m[1]);
        return d.getDate() === +m[1] && d.getMonth() === +m[2] - 1 ? d : null;
      };
      const dobInRange = (v) => { const x = parseDob(v); return !!x && x >= new Date(1920, 0, 1) && x <= today; };

      document.querySelector('[data-cta="continue"]').addEventListener('click', () => {
        let ok = true;
        [name, dob, pan].forEach((el) => err(el, ''));   // fresh check each time
        const fail = (el, msg) => { err(el, msg); ok = false; };
        if (!name.value.trim()) fail(name, '*Required');
        const d = parseDob(dob.value);
        if (!dob.value) fail(dob, '*Required');
        else if (!d || d < new Date(1920, 0, 1) || d > today) fail(dob, '*Invalid date');   // live wording (CR-12)
        // The 18–70 age limit is not checked here – it is validated on the Curated Offers page (DISC-119)
        const p = pan.value.replace(/\s/g, '');
        if (!p) fail(pan, '*Required');
        else if (!/^[A-Z]{3}P[A-Z][0-9]{4}[A-Z]$/.test(p)) fail(pan, 'Please enter your valid PAN Number.')   // CR-16;
        if (!ok) return;
        store.set(K.mobile + '.pan', { name: name.value.trim(), dob: dob.value, pan: p });
        panMock();
      });

      // Prototype only (DISC-112): stands in for the PAN verification service, so both outcomes can be tried.
      // Not part of the live journey and not in the PRD.
      // Verification outcomes (DISC-114): each failure is shown next to the field it is about.
      // Prototype wording until the live messages are confirmed (P-17).
      const PAN_FAIL = {
        name: [name, 'Please enter your name exactly as on your PAN card.'],   // name match below 60% – positive wording, % never shown (CR-13)
        dob: [dob, 'Please enter your date of birth exactly as on your PAN card.'],   // DOB differs from the fetched PAN details (CR-15)
        pan: [pan, 'Please enter your PAN Number exactly as on your PAN card.'],      // PAN does not exist (CR-17)
      };
      const panMock = () => {
        document.body.insertAdjacentHTML('beforeend', `<div class="overlay pan-mock-ov"><div class="modal pan-mock">
          <button class="close" data-x title="Close">${ICON.close}</button>
          <span class="sim-tag">Prototype only</span>
          <h3>Mock PAN Verification</h3>
          <p>For review only: choose a result to see how it is shown on the PAN Details page.</p>
          <div class="pan-mock-btns">
            <button class="btn btn-primary bold" data-r="ok">Success</button>
            <button class="btn btn-outline" data-r="pan">Failure 1 – PAN Number mis-matching</button>
            <button class="btn btn-outline" data-r="dob">Failure 2 – PAN DOB mis-matching</button>
            <button class="btn btn-outline" data-r="name">Failure 3 – PAN Name mis-matching</button>
          </div></div></div>`);
        const ov = document.querySelector('.pan-mock-ov');
        document.body.classList.add('modal-open'); document.documentElement.classList.add('modal-open');
        const close = () => { ov.remove(); document.body.classList.remove('modal-open'); document.documentElement.classList.remove('modal-open'); };
        ov.querySelector('[data-x]').onclick = close;
        ov.querySelectorAll('[data-r]').forEach((bt) => { bt.onclick = () => {
          close();
          if (bt.dataset.r === 'ok') { go('05) LOS to MF Central Redirection consent page'); return; }
          const [el, msg] = PAN_FAIL[bt.dataset.r];
          err(el, msg); el.focus();
        }; });
      };
    },
  };

  // Curated Offers (DISC-119): the 18–70 age limit is validated here, from the DOB entered on the PAN page.
  // Outside the limit the offer cannot be started. Message confirmed (DISC-139); exact position on the page to be confirmed (P-18).
  const AGE_MIN = 18, AGE_MAX = 70;
  const curatedAgeCheck = () => {
    const v = (store.get(K.mobile + '.pan') || {}).dob;
    const m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(v || ''); if (!m) return;
    const t = new Date(), b = new Date(+m[3], +m[2] - 1, +m[1]);
    let a = t.getFullYear() - b.getFullYear(); if (t < new Date(t.getFullYear(), b.getMonth(), b.getDate())) a -= 1;
    if (a >= AGE_MIN && a <= AGE_MAX) return;
    const offer = document.querySelector('.curated .offer'); if (!offer) return;
    offer.insertAdjacentHTML('beforebegin', `<div class="age-err" role="alert">Applicant must be between ${AGE_MIN} to ${AGE_MAX} years of age.</div>`);
    offer.querySelectorAll('[data-cta="start-application"], [data-cta="continue"]').forEach((b) => {
      const c = b.cloneNode(true); c.classList.remove('is-live'); c.classList.add('is-off'); c.setAttribute('aria-disabled', 'true'); b.replaceWith(c);
    });
  };
  ['12) Curated Offers Page', '12.2) Curated offers page for dorpoff view'].forEach((k) => { BEHAVIOUR[k] = curatedAgeCheck; });

  // Screen 05 (DISC-140): PAN carried from screen 04; Check Credit Limit is enabled only when the MF Central consent is ticked.
  BEHAVIOUR['05) LOS to MF Central Redirection consent page'] = () => {
    const card = document.querySelector('.cl-card'); if (!card) return;
    const panIn = card.querySelector('input.readonly');
    const saved = (store.get(K.mobile + '.pan') || {}).pan;
    if (saved && saved.length === 10) panIn.value = `${saved.slice(0, 5)} ${saved.slice(5, 9)} ${saved.slice(9)}`;
    const chk = card.querySelector('input[type="checkbox"]');
    const cta = card.querySelector('[data-cta="check-credit-limit"]');
    const sync = () => {
      cta.classList.toggle('btn-primary', chk.checked); cta.classList.toggle('bold', chk.checked);
      cta.classList.toggle('btn-disabled', !chk.checked); cta.setAttribute('aria-disabled', String(!chk.checked));
    };
    chk.addEventListener('change', sync); sync();
    cta.addEventListener('click', () => { if (chk.checked) go('06) LOS to MF Central Redirection loading page'); });   // grey CTA does nothing
  };

  // Header pop ups (DISC-142): Credit Score icon → credit score from Experian; Profile icon → name as per PAN, PAN, Logout.
  const CREDIT = { score: 790 };   // prototype value – the live score comes from Experian (INT-001)
  const BANDS = [['Excellent', 826, 900, '#1E8E3E'], ['Very Good', 776, 825, '#34C759'], ['Good', 701, 775, '#FFC107'], ['Average', 601, 700, '#FF8C1A'], ['Needs Help', 300, 600, '#E02424']];
  const openPopup = (html) => {
    document.body.insertAdjacentHTML('beforeend', `<div class="overlay hdr-pop-ov"><div class="modal hdr-pop">${closeBtn}${html}</div></div>`);
    const ov = document.querySelector('.hdr-pop-ov');
    const close = () => ov.remove();
    ov.querySelector('.close').onclick = close;
    ov.addEventListener('click', (e) => { if (e.target === ov) close(); });
    return ov;
  };
  const creditPopup = () => {
    const sc = CREDIT.score, band = BANDS.find(([, lo, hi]) => sc >= lo && sc <= hi);
    const d = new Date(), date = `${String(d.getDate()).padStart(2, '0')} ${d.toLocaleString('en-GB', { month: 'short' })} ${d.getFullYear()}`;
    const ang = Math.PI * (1 - (sc - 300) / 600), nx = 100 + 70 * Math.cos(ang), ny = 100 - 70 * Math.sin(ang);
    const arc = (lo, hi, col) => { const a1 = Math.PI * (1 - (lo - 300) / 600), a2 = Math.PI * (1 - (hi - 300) / 600);
      return `<path d="M${100 + 80 * Math.cos(a1)} ${100 - 80 * Math.sin(a1)} A80 80 0 0 1 ${100 + 80 * Math.cos(a2)} ${100 - 80 * Math.sin(a2)}" stroke="${col}" stroke-width="18" fill="none"/>`; };
    openPopup(`<h3 class="cs-t">Your credit score as of ${date}</h3>
      <div class="cs-body"><div class="cs-meter"><svg viewBox="0 0 200 120">${BANDS.slice().reverse().map(([, lo, hi, c]) => arc(lo, hi, c)).join('')}
        <circle cx="${nx}" cy="${ny}" r="6" fill="#111"/></svg>
        <div class="cs-score"><b>${sc}</b><span style="color:${band[3]}">${band[0]}</span></div><span class="cs-min">300</span><span class="cs-max">900</span></div>
        <table class="cs-tab"><tr><th>Category</th><th>Score Range</th></tr>${BANDS.map(([n, lo, hi, c]) => `<tr><td><i style="background:${c}"></i>${n}</td><td><b>${lo} - ${hi}</b></td></tr>`).join('')}</table></div>
      <p class="cs-issue">Issue with your Credit Score? <a href="https://www.experian.com/help/dispute-credit/" target="_blank" rel="noopener">Raise an issue</a></p>
      <p class="cs-pow">Powered by <b>experian</b></p>`);
  };
  const profilePopup = () => {
    const pan = store.get(K.mobile + '.pan') || {};
    const name = (pan.name || 'AZHAGARSAMY SUBBURAJ').toUpperCase(), no = pan.pan || CUSTOMER.pan.replace(/\s/g, '');
    const ov = openPopup(`<h3 class="pf-t">Profiles</h3>
      <div class="pf-card"><span class="pf-i">${name[0]}</span><div><b>${name}</b><span>${no}</span></div><span class="pf-tick">✓</span></div>
      <a class="pf-out" data-pf-out>${ICON.logout}<span>Logout</span></a>`);
    ov.querySelector('[data-pf-out]').onclick = () => go('01) LAMF Landing Page');
  };

  // Screen 06 (DISC-154): countdown 5 → 1, then MF Central. Close asks to confirm: Yes → back to screen 05, No → restart at 5.
  BEHAVIOUR['06) LOS to MF Central Redirection loading page'] = () => {
    const box = document.querySelector('.m-mfc'); if (!box) return;
    const sec = document.getElementById('mfc-sec'), bar = box.querySelector('.prog span');
    bar.style.animation = 'none'; bar.style.transition = 'width 1s linear';
    let n = 5, tick = null;
    const paint = () => { sec.textContent = n; bar.style.width = `${((5 - n) / 5) * 100}%`; };
    const stop = () => { clearInterval(tick); tick = null; };
    const start = () => {
      stop(); n = 5; bar.style.transition = 'none'; paint(); void bar.offsetWidth; bar.style.transition = 'width 1s linear';
      tick = setInterval(() => { n -= 1; if (n <= 0) { stop(); bar.style.width = '100%'; go('07) MF Central Data Check Mock'); return; } paint(); }, 1000);
      TIMERS.push(tick);
    };
    box.querySelector('.close').onclick = () => {
      stop();
      document.body.insertAdjacentHTML('beforeend', `<div class="overlay mfc-cancel-ov"><div class="modal mfc-cancel">
        <p>Are you sure you want to cancel your mutual fund portfolio fetch?</p>
        <div class="mfc-cancel-btns"><button class="no" data-no>No, don’t</button><button class="btn btn-primary bold" data-yes>Yes, cancel</button></div></div></div>`);
      const ov = document.querySelector('.mfc-cancel-ov');
      ov.querySelector('[data-no]').onclick = () => { ov.remove(); start(); };
      ov.querySelector('[data-yes]').onclick = () => { ov.remove(); go('05) LOS to MF Central Redirection consent page'); };
    };
    start();
  };

  // Other OTP screens (DISC-156): enabled once 6 digits are entered; only the demo OTP 000000 is accepted.
  const demoOtpScreen = (getValue, inputs, ctaSel, next) => () => {
    const cta = document.querySelector(ctaSel); if (!cta) return;
    const err = document.getElementById('demo-otp-err');
    const sync = () => { const ok = getValue().length === 6; cta.classList.toggle('btn-primary', ok); cta.classList.toggle('bold', ok); cta.classList.toggle('btn-disabled', !ok); };
    inputs().forEach((i) => i.addEventListener('input', () => { i.value = i.value.replace(/\D/g, ''); if (err) err.textContent = ''; sync(); }));
    cta.addEventListener('click', () => {
      if (getValue().length !== 6) return;
      if (getValue() !== OTP_RULES.demoOtp) { if (err) err.textContent = OTP_ERR.wrong; return; }
      go(next);
    });
    sync();
  };
  const boxesOf = (sel) => () => [...document.querySelectorAll(sel + ' .otp input')];
  const joined = (sel) => () => boxesOf(sel)().map((i) => i.value).join('');
  BEHAVIOUR['07.2) MF Central OTP Page'] = demoOtpScreen(joined('.mock-card'), boxesOf('.mock-card'), '.mock-card [data-cta="submit"]', '07.3) MF Central Select AMCs Page');
  BEHAVIOUR['16.3) KYC Verification Page Email verification popup'] = demoOtpScreen(joined('.m-eotp'), boxesOf('.m-eotp'), '.m-eotp [data-cta="submit-otp"]', '16.4) KYC Verification Page email verification completed');
  BEHAVIOUR['16.5.3) KYC Verification Page Aadhar verification Enter aadhar OTP'] = demoOtpScreen(() => (document.querySelector('.dl-in') || {}).value || '', () => [...document.querySelectorAll('.dl-in')], '[data-cta="submit"]', '16.5.4) KYC Verification Page Aadhar verification Enter PIN');

  BEHAVIOUR['07) MF Central Data Check Mock'] = () => {
    document.querySelectorAll('.pan-mock [data-r]').forEach((bt) => { bt.onclick = () => go(bt.dataset.r === 'yes' ? '07.2) MF Central OTP Page' : '07.1) PAN and Mobile Number Combination No Data Available'); });
  };
  BEHAVIOUR['07.1) PAN and Mobile Number Combination No Data Available'] = () => {
    const m = store.get(K.mobile);
    if (m && m.length === 10) document.getElementById('nl-mobile').textContent = `+91${m[0]}XXXX${m.slice(6)}`;
    document.querySelector('[data-cta="refresh"]').onclick = () => go('06) LOS to MF Central Redirection loading page');   // retry the MF Central fetch (P-21)
  };

  BEHAVIOUR['07.3) MF Central Select AMCs Page'] = () => {
    const all = document.getElementById('amc-all'), rows = [...document.querySelectorAll('[data-amc]')], cta = document.querySelector('.amc-card [data-cta="continue"]');
    const sync = () => { const n = rows.filter((r) => r.checked).length; all.checked = n === rows.length; cta.disabled = n === 0; rows.forEach((r) => r.closest('.amc-row').classList.toggle('on', r.checked)); };
    all.addEventListener('change', () => { rows.forEach((r) => { r.checked = all.checked; }); sync(); });
    rows.forEach((r) => r.addEventListener('change', sync));
    cta.addEventListener('click', () => { if (cta.disabled) return; store.set('lamf.amcs', rows.filter((r) => r.checked).map((r) => AMCS[+r.dataset.amc][1])); go('07.4) MF Central Portfolio Fetching Page'); });
    sync();
  };
  BEHAVIOUR['07.4) MF Central Portfolio Fetching Page'] = () => { TIMERS.push(setTimeout(() => go('07.5) MF Central Portfolio Discovery Complete Page'), 2500)); };
  BEHAVIOUR['07.5) MF Central Portfolio Discovery Complete Page'] = () => {
    let n = 3; const el = document.getElementById('mfc-left');
    const t = setInterval(() => { n -= 1; el.textContent = Math.max(n, 0); if (n <= 0) { clearInterval(t); go('08) MF Central to LOS Redirecting Page'); } }, 1000); TIMERS.push(t);
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


  /* Screens 16.5.1 – 16.5.6 imitate DigiLocker / Digio pages. On any host other than
     localhost (e.g. the cloud copy) they carry a visible "simulated" strip so nobody can
     mistake them for the real service. Local screenshots stay untouched. */
  const SIMULATED = [
    '16.5.1) KYC Verification Page Aadhar verification',
    '16.5.2) KYC Verification Page Aadhar verification Enter aadhar',
    '16.5.3) KYC Verification Page Aadhar verification Enter aadhar OTP',
    '16.5.4) KYC Verification Page Aadhar verification Enter PIN',
    '16.5.5) KYC Verification Page Aadhar verification Fetching',
    '16.5.6) KYC Verification Page Aadhar verification process done in digilocker yet to redirect to los',
  ];
  function simulationNotice() {
    const local = ['localhost', '127.0.0.1', ''].includes(location.hostname);
    if (local || !SIMULATED.includes(currentScreen())) return;
    const el = document.createElement('div');
    el.className = 'sim-notice';
    el.textContent = 'SIMULATED SCREEN — Shriram Credit LAMF prototype. This is not DigiLocker or Digio. Do not enter real Aadhaar, OTP or PIN details; nothing entered here is sent anywhere.';
    document.body.prepend(el);
    document.body.classList.add('has-sim-notice');
  }

  /* ---------------- Dev navigator ---------------- */
  // Go to PRD (DISC-153): each screen opens its own row in the PRD; screens without a row yet open the PRD at the top.
  const PRD_ROW = { '01': '1', '02': '2', '03': '3', '04': '4', '05': '5', '06': '7', '07': '7', '07.1': '12', '07.2': '8', '07.3': '9', '07.4': '10', '07.5': '11' };
  const prdHref = (screen) => {
    const row = PRD_ROW[(String(screen).match(/^([\d.]+)\)/) || [])[1]];
    if (SPA()) return '#PRD' + (row ? '/sl-' + row : '');
    return 'SCCL_LAMF_LOS_PRD.html' + (row ? '#sl-' + row : '');
  };

  function devnav() {
    const cur = SPA() ? decodeURIComponent(location.hash.replace(/^#/, '')) : decodeURIComponent(location.pathname.split('/').pop()).replace(/\.html$/, '');
    const k = SCREENS.indexOf(cur);
    const el = document.createElement('div');
    el.id = 'devnav';
    el.innerHTML = `
      <div class="list">${SCREENS.map((s, j) => `<a href="${href(s)}" class="${j === k ? 'on' : ''}">${s}</a>`).join('')}</div>
      <div class="bar">
        ${k > 0 ? `<a href="${href(SCREENS[k - 1])}" title="Previous screen">‹ Prev</a>` : ''}
        <button class="cur" title="All screens">☰ ${k >= 0 ? SCREENS[k] : 'Screens'}</button>
        ${k >= 0 && k < SCREENS.length - 1 ? `<a href="${href(SCREENS[k + 1])}" title="Next screen">Next ›</a>` : ''}
        <a class="to-prd" href="${prdHref(cur)}" target="_blank" rel="noopener" title="Open this screen's row in the PRD">Go to PRD ↗</a>
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
  const TIMERS = [];
  function render(html, opts = {}) {
    TIMERS.splice(0).forEach(clearInterval);       // stop timers from the previous screen
    document.body.className = '';
    document.body.innerHTML = html;
    if (opts.bodyClass) document.body.classList.add(opts.bodyClass);
    // OTP boxes: auto-advance
    document.querySelectorAll('.otp input, .dl-pin input').forEach((inp, idx, all) => {
      inp.addEventListener('input', () => { if (inp.value && all[idx + 1]) all[idx + 1].focus(); });
    });
    if (opts.scroll) requestAnimationFrame(() => window.scrollTo(0, opts.scroll === 'bottom' ? document.body.scrollHeight : opts.scroll));
    wireFlow();
    wireBehaviour();
    document.querySelectorAll('[data-logout]').forEach((a) => { a.onclick = () => go('01) LAMF Landing Page'); });   // logout ends the journey
    document.querySelectorAll('[data-credit]').forEach((a) => { a.onclick = creditPopup; });
    document.querySelectorAll('[data-profile]').forEach((a) => { a.onclick = profilePopup; });
    if (opts.scrollTo) requestAnimationFrame(() => { const t = document.querySelector(opts.scrollTo); if (t) window.scrollTo(0, t.getBoundingClientRect().top + scrollY - (opts.offset || 0)); });
    // Popup open → freeze the page behind it (only the popup scrolls)
    const hasPopup = !!document.querySelector('.overlay');
    document.body.classList.toggle('modal-open', hasPopup);
    document.documentElement.classList.toggle('modal-open', hasPopup);
    simulationNotice();
    devnav();
  }

  /* Cloud copy only: show the generated PRD document as a route on the same page */
  function renderPRD(bodyHtml) {
    TIMERS.splice(0).forEach(clearInterval);
    document.body.className = 'prd';
    document.body.innerHTML = bodyHtml;
    devnav();
  }

  window.LAMF = { T, render, renderPRD, withModal, loader, SEL_DEFAULT, SCREENS, FLOW, BEHAVIOUR, OTP_RULES, OTP_ERR, MOBILE_ERR, FUNDS, F, PORTFOLIO, CUSTOMER };
})();
