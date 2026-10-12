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
    '16.6) KYC Verification Page Photo verification Mock',
    '16.6.1) KYC Verification Page Photo verification failed',
    '16.7) KYC Verification Page Bank details',
    '16.8) KYC Verification Page KYC completed',
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
    '19.2) Agreement and E-Mandate Page E-Mandate failed',
    '23) Loan Application Submitted Page',
    '24) Your Loans Page',
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
    doc: S('<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>'),
    bank: S('<path d="M3 10h18L12 4z"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>'),
    chev: S('<path d="M6 15l6-6 6 6"/>', '0 0 24 24', 'stroke-width="1.8"'),
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
  // Banner ticker (DISC-172): three messages scroll up one after another, 3 seconds each, then repeat
  const TICKER = ['Borrow only what you need and pay interest only on the utilised amount', 'Avail a loan of up to 75% of your eligible Mutual Fund portfolio', 'Quick digital process with fast loan disbursal'];
  T.curated = (o = {}) => `
    ${header('app')}
    <div class="info-banner ticker"><div class="tk-win"><div class="tk-list">${[...TICKER, TICKER[0]].map((t) => `<span>${img('banner-icon.png')}${t}</span>`).join('')}</div></div></div>
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
        <a class="kfs-row" data-cta="kfs-document"><span class="kfs-ico">${ICON.doc}</span>KFS document<span class="kfs-chev">›</span></a>
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

  /* 16.x KYC. o = {email:'input'|'filled'|'done', aadhaar:'pending'|'start'|'status'|'done', photo:'pending'|'start'|'done', photoErr, bank, bankForm, cont:'on'|'off'} */
  const kycRow = (n, title, state, extra = '') => {
    const done = state === 'done';
    if (state === 'openPending') {     // current step, still pending, with its action (Bank Details form, Agreement & E-Mandate)
      return `<div class="kyc-row open"><div class="kyc-h"><span class="kn act">${n}</span><span class="kt">${title}</span><span class="badge pending">Pending</span></div>${extra}</div>`;
    }
    if (state === 'doneOpen') {        // complete, with its details still shown (verified bank account)
      return `<div class="kyc-row open"><div class="kyc-h"><span class="kn done">${ICON.check}</span><span class="kt">${title}</span><span class="badge complete">Complete</span></div>${extra}</div>`;
    }
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
    const failNote = (msg) => (msg ? `<p class="field-err kyc-fail">${msg}</p>` : '');
    const bankRow = o.bank   // 16.8: verified bank account shown as a card
      ? kycRow(5, 'Bank Details', 'doneOpen', `<div class="kyc-bank">${o.bank.logo ? img(o.bank.logo, 'kb-logo') : `<span class="kb-logo kb-gen">${ICON.bank}</span>`}<span>${o.bank.name} <span class="kb-n">${o.bank.account.slice(-4)}</span></span><b>IFSC</b><span class="kb-n">${o.bank.ifsc}</span><span class="kb-ok">${ICON.check}</span></div>`)
      : o.bankForm ? kycRow(5, 'Bank Details', 'openPending', o.bankForm) : kycRow(5, 'Bank Details', 'pending');
    return `
    <div class="sticky-top">${header('app')}${stepper(2)}</div>
    <main class="wrap kyc-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <div class="loan-strip">Your loan amount is ${rs('1,55,36,100')} <a class="link-yellow sm" data-cta="view-details">View details</a></div>
      <h1 class="kyc-title">KYC Verification <small>This step is required as per our lending guidelines.</small></h1>
      ${kycRow(1, 'Email Verification', email === 'done' ? 'done' : 'open', emailExtra)}
      ${kycRow(2, 'PAN Verification', 'done')}
      ${kycRow(3, 'Aadhaar Verification with ' + DL, aad === 'done' ? 'done' : aad === 'pending' ? 'pending' : 'open', aadExtra)}
      ${kycRow(4, 'Photo Verification', photo === 'done' ? 'done' : photo === 'start' ? 'open' : 'pending', photoExtra + failNote(o.photoErr))}
      ${bankRow}
      ${o.cont ? `<button class="btn ${o.cont === 'on' ? 'btn-primary' : 'btn-disabled'} bold kyc-btn kyc-cont" data-cta="kyc-continue">Continue</button>` : ''}
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

  /* ======================================================
     16.6 – 24: Photo Verification, Bank Details, Customer Details, Pledging, Agreement & E-Mandate,
     Sanction letter, e-Sign, E-Mandate, Application submitted, Your loans.
     Taken from the Apply for New Loan prototype (lamf-existing-customer) and set for a new customer:
     every detail is captured in this journey (no record on file). Drafted for review page by page (DISC-171).
     ====================================================== */
  const APP = { loan: '1,55,36,100', amount: 15536100, pledge: '2,07,14,800.22' };
  const inr = (n) => Math.round(n).toLocaleString('en-IN');
  /* Details from PAN (screen 04) and Aadhaar (DigiLocker); the rest is entered on screen 17 */
  const KYC_PROFILE = {
    salutation: '', name: 'AZHAGARSAMY SUBBURAJ', dob: '14/05/1988', gender: 'Male', mother: '', father: '', marital: '',
    purpose: '', qualification: '', occupation: '', business: '', income: '', source: '', independent: '', pep: false, tax: false,
    addr1: '13/33, Kamaraj 3rd Street', addr2: 'Choolaimedu', addr3: 'Chennai, Tamil Nadu, 600094', landmark: 'N/A', pincode: '600094', city: 'Chennai',
  };
  const BANK_DEMO = { holder: 'AZHAGARSAMY SUBBURAJ', account: '001201548736', ifsc: 'ICIC0002692', name: 'ICICI Bank', type: 'Savings', logo: 'funds/icici.png' };

  /* 16.6 Photo verification mock (stands in for the live photo check): Success / Failure */
  T.kycMock = () => `
    ${header('app')}
    <main><div class="card mock-card kyc-mock">
      <h2>Mock Photo Verification Page</h2>
      <h4>Photo verification</h4>
      <p class="mock-p">Prototype only: choose the result to see how the journey continues.</p>
      <div class="mock-2btn">
        <button class="btn btn-primary bold" data-cta="mock-success">Success</button>
        <button class="btn btn-outline" data-cta="mock-failure">Failure</button>
      </div>
    </div></main>`;

  /* 16.7 Bank Details form: enter manually or fetch with a UPI ID (demo IFSC / UPI lookups – no bank service is called) */
  const IFSC_BANKS = { ICIC: 'ICICI Bank', HDFC: 'HDFC Bank', SBIN: 'State Bank of India', UTIB: 'Axis Bank', KKBK: 'Kotak Mahindra Bank', PUNB: 'Punjab National Bank', BARB: 'Bank of Baroda', CNRB: 'Canara Bank', IDIB: 'Indian Bank', IOBA: 'Indian Overseas Bank' };
  T.bankForm = (holder = '') => `
    <div class="bk-form">
      <p class="bk-note"><b>Note:</b> The bank account holder name must match the name as per PAN. In case of a mismatch, the loan cannot be disbursed to this account.</p>
      <p class="bk-l">Select one option to fetch your bank details</p>
      <div class="bk-opts">
        <button class="bk-opt on" data-bk="manual"><span class="bk-dot"></span>Enter manually</button>
        <button class="bk-opt" data-bk="upi"><span class="bk-dot"></span>Fetch the details using UPI ID</button>
      </div>
      <div class="bk-manual">
        <div class="bk-grid">
          <div><label class="field-lbl">Account number<i class="req">*</i></label><input class="input" id="bk-acc" type="password" inputmode="numeric" maxlength="18" autocomplete="off"><p class="field-err" data-bk-err="acc"></p></div>
          <div><label class="field-lbl">Confirm Account Number<i class="req">*</i></label><input class="input" id="bk-acc2" inputmode="numeric" maxlength="18" autocomplete="off"><p class="field-err" data-bk-err="acc2"></p></div>
          <div><label class="field-lbl">IFSC code<i class="req">*</i></label><input class="input" id="bk-ifsc" maxlength="11" placeholder="e.g. HDFC0001234" autocomplete="off"><p class="field-err" data-bk-err="ifsc"></p></div>
          <div><label class="field-lbl">Bank name</label><input class="input readonly" id="bk-bank" readonly tabindex="-1" placeholder="Filled from IFSC"></div>
          <div><label class="field-lbl">Bank branch</label><input class="input readonly" id="bk-branch" readonly tabindex="-1" placeholder="Filled from IFSC"></div>
          <div><label class="field-lbl">Account type<i class="req">*</i></label><select class="input an-select" id="bk-type"><option value="">Select</option><option>Savings</option><option>Current</option></select><p class="field-err" data-bk-err="type"></p></div>
          <div><label class="field-lbl">Account holder name<i class="req">*</i></label><input class="input" id="bk-holder" value="${holder}" maxlength="60" autocomplete="off"><p class="field-err" data-bk-err="holder"></p></div>
        </div>
      </div>
      <div class="bk-upi" hidden>
        <div class="bk-grid">
          <div><label class="field-lbl">UPI ID<i class="req">*</i></label><input class="input" id="bk-upi" placeholder="e.g. name@okhdfcbank" autocomplete="off"><p class="field-err" data-bk-err="upi"></p></div>
        </div>
      </div>
      <button class="btn btn-primary bold kyc-btn" data-cta="verify-bank">Verify Bank Account</button>
    </div>`;

  /* 17 Customer details: Personal Details, Other Details, KYC Address.
     Name, DOB, Gender and the KYC address come from PAN / Aadhaar (shown as text); the rest is entered here. */
  const CD_OPTIONS = {
    salutation: ['Mr', 'Mrs', 'Ms'],
    marital: ['Single', 'Married'],
    purpose: ['Home Renovation', 'Vacation', 'Medical Emergency', 'Education', 'Buying of Vehicle', 'Land Purchases', 'Emergency fund requirement'],
    qualification: ['Below High School', 'High School', 'Graduate', 'Post Graduate', 'Professional', 'Others'],
    occupation: ['Salaried', 'Self Employed', 'Student', 'Retired', 'Home maker', 'Other'],        // Other → “Please specify occupation”
    business: ['Retail & Manufacturing', 'Medical & Health', 'Agriculture', 'Real Estate / Construction', 'Banking / Finance', 'Information Technology',
      'Hotel Industry', 'Others (E-commerce, Education, Export-Import, Services etc.)', 'Investment Income', 'Rental Income', 'Pension'],
    income: ['Up to Rs. 5 Lakhs', 'Rs. 5 Lakhs to Rs. 10 Lakhs', 'Rs. 10 Lakhs to Rs. 25 Lakhs', 'Above Rs. 25 Lakhs'],
    source: ['Salary', 'Business Income', 'Rental Income', 'Investments', 'Agriculture', 'Others'],
    independent: ['Yes', 'No'],
  };
  const CD_FIELDS = {       // key → [label, type]  (type: select | text | show)
    personal: [['salutation', 'Salutation', 'select'], ['name', 'Name', 'show'], ['dob', 'Date of Birth', 'show'], ['gender', 'Gender', 'show'],
      ['mother', 'Mother’s Name', 'text'], ['father', 'Father’s Name', 'text'], ['marital', 'Marital Status', 'select']],
    other: [['purpose', 'Loan Purpose', 'select'], ['qualification', 'Qualification', 'select'], ['occupation', 'Occupation', 'select'], ['occupationOther', 'Please specify occupation', 'text'], ['business', 'Nature of Business', 'select'],
      ['income', 'Annual Income', 'select'], ['source', 'Source of Income', 'select'], ['independent', 'Is the applicant financially independent?', 'select']],
    address: [['addr1', 'Address Line 1', 'show'], ['addr2', 'Address Line 2', 'show'], ['addr3', 'Address Line 3', 'show'], ['landmark', 'Landmark', 'show'],
      ['pincode', 'Pincode', 'show'], ['city', 'City', 'show']],
  };
  const cdField = (p, [key, label, type]) => {
    const v = p[key] || '';
    if (type === 'show') return `<div class="cd-f"><span class="cd-l">${label}</span><p class="cd-v">${v}</p></div>`;
    const input = type === 'select'
      ? `<select class="input cd-in an-select" data-k="${key}"><option value="">Select</option>${CD_OPTIONS[key].map((o) => `<option value="${o.replace(/&/g, '&amp;')}" ${o === v ? 'selected' : ''}>${o.replace(/&/g, '&amp;')}</option>`).join('')}</select>`
      : `<input class="input cd-in" data-k="${key}" value="${v}" maxlength="60" autocomplete="off">`;
    const hide = key === 'occupationOther' && p.occupation !== 'Other' ? ' hidden' : '';
    return `<div class="cd-f"${key === 'occupationOther' ? ' data-other-of="occupation"' : ''}${hide}><label class="cd-l">${label}<i>*</i></label>${input}<p class="field-err" data-err="${key}"></p></div>`;
  };
  const cdSection = (id, title, body) => `
    <section class="cd-sec open" data-sec="${id}">
      <button class="cd-h" data-toggle="${id}"><span class="kn done">${ICON.check}</span><span class="kt">${title}</span><span class="cd-chev">${ICON.chev}</span></button>
      <div class="cd-body">${body}</div>
    </section>`;
  T.custDetails = (p = KYC_PROFILE) => `
    <div class="sticky-top">${header('app')}${stepper(2)}</div>
    <main class="wrap kyc-page cd-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <div class="loan-strip">Your loan amount is ${rs(APP.loan)} <a class="link-yellow sm" data-cta="view-details">View details</a></div>
      ${cdSection('personal', 'Personal Details', `<div class="cd-grid">${CD_FIELDS.personal.map((f) => cdField(p, f)).join('')}</div>`)}
      ${cdSection('other', 'Other Details', `<div class="cd-grid">${CD_FIELDS.other.map((f) => cdField(p, f)).join('')}</div>
        <label class="chk cd-chk"><input type="checkbox" data-k="pep" ${p.pep ? 'checked' : ''}><span>I am not a politically exposed person ${i()}</span></label>
        <label class="chk cd-chk"><input type="checkbox" data-k="tax" ${p.tax ? 'checked' : ''}><span>I am a tax resident of India only</span></label>
        <p class="field-err" data-err="decl"></p>`)}
      ${cdSection('address', 'KYC Address', `<div class="cd-grid">${CD_FIELDS.address.map((f) => cdField(p, f)).join('')}</div>`)}
      <div class="cd-cta"><button class="btn btn-primary bold" data-cta="confirm-continue">Confirm and Continue</button></div>
    </main>`;

  /* 18 Pledging of Mutual Fund (stepper step 3). o = {status:'pending'|'pledged'} */
  T.pledge = (o = {}) => `
    <div class="sticky-top">${header('app')}${stepper(3)}</div>
    <main class="wrap pl-page">
      <a class="back" data-cta="back">${ICON.back}Back</a>
      <h3 class="pl-t">Please review and confirm the following details</h3>
      <div class="pl-sum"><div><span>Loan Amount</span><b>${rs(APP.loan)}</b></div><div><span>Total Pledge Value</span><b>${rs(APP.pledge)}</b></div></div>
      <div class="pl-card">
        <div class="pl-row">
          <span class="pl-logo">${img('mfcentral-logo.png')}</span>
          <div><p class="pl-n">MF Central</p><p class="pl-v">Value of Securities <b>${rs(APP.pledge)}</b></p></div>
          <span class="pl-badge ${o.status === 'pledged' ? 'ok' : ''}">${o.status === 'pledged' ? 'Pledged' : 'Pending'}</span>
        </div>
        <div class="pl-btns">
          <button class="pl-view" data-cta="view-securities">View Securities</button>
          ${o.status === 'pledged' ? '<button class="pl-go done" disabled>Pledged</button>' : '<button class="pl-go" data-cta="pledge-securities">Pledge Securities</button>'}
        </div>
      </div>
      <p class="pl-otp-note">An OTP will be sent to ${CUSTOMER.mobileMasked2}</p>
    </main>`;
  /* 18.1 Pledge OTP popup (MF Central OTP; demo OTP 000000) */
  T.pledgeOtpModal = () => `
    <div class="modal m-otp m-plotp">${closeBtn}
      <h3>Enter OTP to pledge your Mutual Fund</h3>
      <p class="sent">OTP has been sent by MF Central to <b>${CUSTOMER.mobileMasked2}</b></p>
      <div class="otp">${'<input maxlength="1" inputmode="numeric" autocomplete="off">'.repeat(6)}</div>
      <p class="resend">Didn’t receive OTP? <b>00:30</b></p>
      <p class="otp-hint">Please use OTP <b>${OTP_RULES.demoOtp}</b> to proceed</p>
      <p class="field-err" id="demo-otp-err"></p>
      <button class="btn btn-disabled btn-block" data-cta="submit-pledge-otp">Submit OTP</button>
    </div>`;
  /* 18.2 Successfully pledged popup */
  T.pledgedModal = () => `
    <div class="modal m-pledged">
      <span class="pl-tick"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#12A150"/><path d="M6.8 12.4l3.4 3.4 7-7" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      <h3>Successfully pledged!</h3>
      <p>You will be redirected in <span id="pl-count">3</span> seconds.</p>
    </div>`;

  /* 19 Agreement & E-Mandate (stepper step 4). em = '' | 'failed' | 'done' */
  T.agreement = (signed = false, em = '') => `
    <div class="sticky-top">${header('app')}${stepper(4)}</div>
    <main class="wrap kyc-page ag-page">
      ${signed ? kycRow(1, 'Loan Agreement', 'done') : kycRow(1, 'Loan Agreement', 'openPending', '<button class="btn btn-primary bold kyc-btn" data-cta="sign-agreement">Sign Agreement</button>')}
      ${!signed ? kycRow(2, 'E-Mandate', 'pending')
        : em === 'done' ? kycRow(2, 'E-Mandate', 'done')
        : kycRow(2, 'E-Mandate', 'openPending', `<button class="btn btn-primary bold kyc-btn" data-cta="setup-emandate">Set up E-Mandate</button>${em === 'failed' ? '<p class="field-err kyc-fail">E-Mandate was not authenticated. Please try again.</p>' : ''}`)}
    </main>`;

  /* 20 Sanction letter (e-Sanction Letter + KFS) and 21 loan agreement e-sign (Digio look-alike, prototype only).
     Full text from the shared UAT PDFs (assets/docs/*.txt), filled with this application's details. */
  const inWords = (n) => {
    const a = ['', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE', 'THIRTEEN', 'FOURTEEN', 'FIFTEEN', 'SIXTEEN', 'SEVENTEEN', 'EIGHTEEN', 'NINETEEN'];
    const b = ['', '', 'TWENTY', 'THIRTY', 'FORTY', 'FIFTY', 'SIXTY', 'SEVENTY', 'EIGHTY', 'NINETY'];
    const two = (x) => (x < 20 ? a[x] : `${b[Math.floor(x / 10)]}${x % 10 ? ' ' + a[x % 10] : ''}`);
    const out = []; let r = Math.round(n);
    [[10000000, 'CRORE'], [100000, 'LAKH'], [1000, 'THOUSAND'], [100, 'HUNDRED']].forEach(([v, w]) => { const q = Math.floor(r / v); if (q) { out.push(`${two(q)} ${w}`); r %= v; } });
    if (r) out.push(two(r));
    return out.join(' ') || 'ZERO';
  };
  T.sanction = () => `
    <main class="sl-bg"><div class="sl-doc">
      <div class="sl-logo">${img('shriram-logo.png')}</div>
      <div class="doc-text" data-doc="sanction-letter">Loading the sanction letter…</div>
    </div></main>
    <div class="sl-bar">
      <label class="sl-chk"><input type="checkbox" id="sl-accept"><span>I accept the terms of the Sanction letter and Key Fact Statement (KFS), including all applicable charges, interest rates, and repayment schedules. I confirm that I understand these conditions and agree to proceed with the loan agreement.</span></label>
      <button class="sl-submit" data-cta="sanction-submit" disabled>Submit</button>
    </div>`;
  T.esign = () => `
    <header class="dg-hdr"><span class="dg-logo"><b>d</b>igio</span><span class="dg-mock">Mock e-Sign page (prototype)</span></header>
    <main class="dg-bg"><div class="sl-doc dg-doc">
      <div class="sl-logo">${img('shriram-logo.png')}</div>
      <div class="doc-text" data-doc="loan-agreement">Loading the loan agreement…</div>
    </div></main>
    <div class="dg-bar">
      <label class="dg-chk"><input type="checkbox" id="dg-accept" checked><span>1. By continuing, I agree to do eKyc using Aadhaar to eSign with one of ESPs (CVL or Emudra or Protean) Digio is registered as ASP<br>2. I confirm that +91${CUSTOMER.mobile} belongs to me and verified with <b>SHRIRAM CREDIT COMPANY LIMITED</b></span></label>
      <button class="dg-sign" data-cta="sign-now">Sign Now</button>
      <p class="dg-sec">Secured by <b>digio</b></p>
    </div>`;
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

  /* 22 E-Mandate (Digio look-alike, prototype): overview + bank verified on 16.7 + verification mode + consent */
  const fmtDate = (d) => d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
  const titleCase = (t) => t.toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase());
  T.emandate = (bank = BANK_DEMO) => {
    const first = new Date(); const last = new Date(); last.setFullYear(last.getFullYear() + 1);
    const mode = (id, label, ico, on) => `<label class="em-mode ${on ? 'on' : ''}"><input type="radio" name="em-mode" value="${id}" ${on ? 'checked' : ''}><span class="em-ico">${ico}</span>${label}</label>`;
    return `
    <main class="em-bg"><div class="em-card">
      <header class="em-hdr"><span class="dg-logo"><b>d</b>igio</span><span class="dg-mock">Mock e-Mandate page (prototype)</span><span class="em-sec">Secured by <b>digio</b></span></header>
      <div class="em-body">
        <aside class="em-ov">
          <p class="em-ovt">Mandate Overview</p>
          <span>Maximum amount</span><b class="em-max">₹${(10000000).toLocaleString('en-US', { minimumFractionDigits: 2 })}</b>
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
            <div class="em-2"><div><span>IFSC code</span><p><b>${bank.ifsc}</b></p></div><div style="text-align:right"><span>A/C Type</span><p><b>${bank.type || 'Savings'}</b></p></div></div>
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
  T.submitted = () => {
    const amt = APP.amount;
    const row = (l, v, sub = '') => `<div class="sb-row"><div><span>${l}</span>${sub ? `<small>${sub}</small>` : ''}</div><b>${v}</b></div>`;
    return `
    ${header('app')}
    <main class="wrap sb-page">
      <h2 class="sb-t"><span class="sb-tick"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#12A150"/><path d="M6.8 12.4l3.4 3.4 7-7" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span>Your loan application has been submitted</h2>
      <div class="sb-card">
        ${row('Loan Amount', rs(APP.loan))}
        ${row('Mutual Fund Value Pledged', rs(APP.pledge))}
        ${row('Interest Rate', '10.5% p.a.')}
        ${row('Tenure', '12 Months', '(No foreclosure charges)')}
        ${row('Processing Fee (inclusive of taxes)', rs(inr(Math.round(Math.round(amt * 0.005) * 1.18))), 'Will be deducted at the time of first withdrawal')}
        ${row('Repayment Type', 'Interest Only')}
        ${row('Disbursement Type', 'Multiple')}
      </div>
      <div class="sb-cta"><button class="btn btn-primary bold" data-cta="view-loan">View loan details</button></div>
    </main>`;
  };

  /* 24 Your loans – the loan just submitted (withdrawal allowed once the loan is active) */
  T.loanSubmitted = () => {
    const stat2 = (label, v) => `<div class="yl-stat"><span>${label}</span><b>${v}</b></div>`;
    return `
    ${header('app')}
    <main class="yl">
      <h1>Your loans</h1>
      <h2>Loan Against Mutual Fund <span class="yl-badge sub"><i></i>Submitted</span></h2>
      <div class="yl-top">
        <div class="yl-bal">
          <p>Available Withdrawal Balance</p>
          <b>${rs(APP.loan)}</b>
          <p class="yl-note">You can withdraw once your loan is active.</p>
          <div class="yl-btns yl-off"><button class="btn yl-repay" disabled>Repay</button><button class="btn btn-primary yl-withdraw" disabled>Withdraw</button></div>
        </div>
        <div class="yl-stats">
          ${stat2('Sanctioned Amount', rs(APP.loan))}${stat2('Value of Pledged Funds', rs(APP.pledge))}
          ${stat2('Total Withdrawn', rs('0'))}${stat2('Principal Outstanding', '-')}
          ${stat2('Interest Due', rs('0'))}${stat2('Repaid Amount', '-')}
        </div>
      </div>
      <nav class="yl-tabs">${['Statements', 'Transaction Details', 'Pledged Mutual Funds Details', 'Loan Details', 'Repayment Schedule']
        .map((t, k) => `<a class="${k === 0 ? 'on' : ''}">${t}</a>`).join('')}</nav>
      <div class="yl-empty"><svg viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="1.4" stroke-linejoin="round"><path d="M6 2.8h8.5L19 7.3v13.9H6z"/><path d="M14.5 2.8v4.5H19M9 11h7M9 14h7M9 17h7"/></svg><p>All statements will appear here.</p></div>
    </main>`;
  };

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
  // Curated Offers links (DISC-167)
  const CO = '12) Curated Offers Page', SEL = '13.1) Mutual Fund Selection Location access';
  const curatedLinks = () => {
    const on = (cta, to) => document.querySelectorAll(`[data-cta="${cta}"]`).forEach((el) => { if (!el.classList.contains('is-off')) el.onclick = () => go(to); });
    on('how-calculated', '12.1.1) How is it calculated_All Portfolio');
    on('refresh-portfolio', '12.2) Refresh portfolio');
    on('start-application', SEL);
    on('continue', SEL);
  };
  // Success toast (DISC-172): after the portfolio is retrieved from MF Central the Curated Offers page shows
  // “Portfolio fetched successfully” (after Refresh Portfolio: “Portfolio refreshed successfully”) for 3 seconds.
  const TOAST_KEY = 'lamf.toast';
  const successToast = (msg, ms = 3000) => {
    document.body.insertAdjacentHTML('beforeend', `<div class="toast-ok" role="status"><span class="tk-ok">${ICON.check}</span>${msg}</div>`);
    const el = document.body.lastElementChild;
    TIMERS.push(setTimeout(() => el.remove(), ms));
  };
  const curatedToast = () => {
    const t = store.get(TOAST_KEY); if (!t || t === 'refresh-pending') return;
    store.set(TOAST_KEY, null);
    successToast(t === 'refreshed' ? 'Portfolio refreshed successfully' : 'Portfolio fetched successfully');
  };
  ['12) Curated Offers Page', '12.2) Curated offers page for dorpoff view'].forEach((k) => { BEHAVIOUR[k] = () => { curatedAgeCheck(); curatedLinks(); curatedToast(); }; });
  ['12.1.1) How is it calculated_All Portfolio', '12.1.2) How is it calculated_Eligible Portfolio', '12.1.3) How is it calculated_Non Eligible Portfolio'].forEach((k) => {
    BEHAVIOUR[k] = () => {
      const tab = { all: '12.1.1) How is it calculated_All Portfolio', eligible: '12.1.2) How is it calculated_Eligible Portfolio', ne: '12.1.3) How is it calculated_Non Eligible Portfolio' };
      Object.entries(tab).forEach(([t, to]) => { const b = document.querySelector(`[data-cta="tab-${t}"]`); if (b) b.onclick = () => go(to); });
      const back = document.querySelector('[data-cta="back"]'); if (back) back.onclick = () => go(CO);
    };
  });
  BEHAVIOUR['12.2) Refresh portfolio'] = () => {
    const m = document.querySelector('.m-refresh'); if (!m) return;
    m.querySelector('.close').onclick = () => go(CO);
    m.querySelector('[data-cta="refresh-portfolio"]').onclick = () => { store.set(TOAST_KEY, 'refresh-pending'); go('06) LOS to MF Central Redirection loading page'); };   // fetch again from MF Central (P-23)
  };

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

  // MF Central → LOS processing screens advance on their own (DISC-162): 08 for 1.5 s, then 09, 10, 11 for 3 s each, then Curated Offers.
  [['08) MF Central to LOS Redirecting Page', '09) MF Central to LOS Fetching Mutual Fund Portfolio Page', 1500],
   ['09) MF Central to LOS Fetching Mutual Fund Portfolio Page', '10) MF Central to LOS Analysing Mutual Fund Portfolio Page', 3000],
   ['10) MF Central to LOS Analysing Mutual Fund Portfolio Page', '11) MF Central to LOS Generating Loan Page', 3000],
   ['11) MF Central to LOS Generating Loan Page', '12) Curated Offers Page', 3000]]
    .forEach(([from, to, ms]) => { BEHAVIOUR[from] = () => { TIMERS.push(setTimeout(() => go(to), ms)); }; });
  // Back from MF Central with the portfolio → the Curated Offers page shows the success toast
  { const prev08 = BEHAVIOUR['08) MF Central to LOS Redirecting Page'];
    BEHAVIOUR['08) MF Central to LOS Redirecting Page'] = () => { store.set(TOAST_KEY, store.get(TOAST_KEY) === 'refresh-pending' ? 'refreshed' : 'fetched'); prev08(); }; }

  // Screens 13 – 16.5.9 navigation (DISC-168): CTA → next screen; DigiLocker hand-back screens advance on their own.
  const S13 = { loc: '13.1) Mutual Fund Selection Location access', sel: '13.2) Mutual Fund Selection Page', off: '13.3) Mutual Fund Selection page if location disabled',
    sum: '14) Loan Application Summary', kyc: '16.1) KYC Verification Page', det: '16.2) KYC Verification Page view details popup', em: '16.3) KYC Verification Page Email verification popup',
    emOk: '16.4) KYC Verification Page email verification completed', dg1: '16.5.1) KYC Verification Page Aadhar verification', dg2: '16.5.2) KYC Verification Page Aadhar verification Enter aadhar',
    dg3: '16.5.3) KYC Verification Page Aadhar verification Enter aadhar OTP', dg4: '16.5.4) KYC Verification Page Aadhar verification Enter PIN', dg5: '16.5.5) KYC Verification Page Aadhar verification Fetching',
    dg6: '16.5.6) KYC Verification Page Aadhar verification process done in digilocker yet to redirect to los', dg7: '16.5.7) KYC Verification Page Aadhar verification process done in digilocker  to los auto redirection',
    dg8: '16.5.8) KYC Verification Page Aadhar verification process done in digilocker  redirected to los but status getting updated', dg9: '16.5.9) KYC Verification Page Aadhar verification completed' };
  const NAV = {
    [S13.loc]: { 'loc-allow': S13.sel, 'loc-once': S13.sel, 'loc-block': S13.off },
    [S13.off]: { refresh: S13.loc },
    ['13.4) Mutual Fund Selection page if location disabled & proceed']: { 'yes-continue': S13.sel, 'go-dashboard': CO },
    [S13.sel]: { 'continue-to-apply': S13.sum, back: CO },
    ['13.5) Mutual Fund Selection page loan amount edit']: { 'update-loan': S13.sel, 'continue-to-apply': S13.sum, back: CO },
    ['13.6) Mutual Fund Selection page loan amount edit as fund wise']: { 'continue-to-apply': S13.sum, back: CO },
    [S13.sum]: { continue: S13.kyc, back: S13.sel },
    [S13.kyc]: { 'view-details': S13.det, 'verify-email': S13.em, back: S13.sum },
    [S13.det]: { close: S13.kyc, back: S13.sum },
    [S13.emOk]: { 'start-kyc': S13.dg1, 'view-details': S13.det, back: S13.sum },
    [S13.dg1]: { proceed: S13.dg2, cancel: S13.emOk },
    [S13.dg2]: { next: S13.dg3 },
    [S13.dg4]: { done: S13.dg5 },
    [S13.dg9]: { 'view-details': S13.det, back: S13.sum },
  };
  const AUTO = [[S13.dg5, S13.dg6, 2500], [S13.dg6, S13.dg7, 1500], [S13.dg7, S13.dg8, 1500], [S13.dg8, S13.dg9, 3000]];
  Object.entries(NAV).forEach(([scr, map]) => {
    const prev = BEHAVIOUR[scr];
    BEHAVIOUR[scr] = () => {
      if (prev) prev();
      Object.entries(map).forEach(([cta, to]) => {
        const els = cta === 'close' ? document.querySelectorAll('.overlay .close') : document.querySelectorAll(`[data-cta="${cta}"]`);
        els.forEach((el) => { el.style.cursor = 'pointer'; el.onclick = (e) => { e.preventDefault(); go(to); }; });
      });
    };
  });
  AUTO.forEach(([from, to, ms]) => { const prev = BEHAVIOUR[from]; BEHAVIOUR[from] = () => { if (prev) prev(); TIMERS.push(setTimeout(() => go(to), ms)); }; });

  // Screens 16.6 – 24 (DISC-171): Photo → Bank → Customer details → Pledging → Agreement & E-Mandate → Submitted → Your loans.
  const S16 = {
    ph: '16.6) KYC Verification Page Photo verification Mock', phFail: '16.6.1) KYC Verification Page Photo verification failed',
    bank: '16.7) KYC Verification Page Bank details', done: '16.8) KYC Verification Page KYC completed',
    cd: '17) Customer Details Page', pl: '18) Pledging of Mutual Fund Page', plOtp: '18.1) Pledging of Mutual Fund OTP popup', plDone: '18.2) Pledging of Mutual Fund Successfully pledged',
    ag: '19) Agreement and E-Mandate Page', agSigned: '19.1) Agreement and E-Mandate Page Loan Agreement signed', agFail: '19.2) Agreement and E-Mandate Page E-Mandate failed',
    sl: '20) Sanction Letter Page', es: '21) Loan Agreement e-Sign Page', esOtp: '21.1) Loan Agreement e-Sign OTP popup', esDone: '21.2) Loan Agreement e-Sign Signed Successfully', agDone: '21.3) Loan Agreement Signed Successfully',
    em: '22) E-Mandate Page', np: '22.1) E-Mandate NPCI Simulation Page', emDone: '22.2) E-Mandate Authenticated Successfully',
    sb: '23) Loan Application Submitted Page', yl: '24) Your Loans Page',
  };
  const KB = { bank: 'lamf.bank', profile: 'lamf.profile' };
  const NAV2 = {
    [S13.dg9]: { 'start-photo': S16.ph },
    [S16.ph]: { 'mock-success': S16.bank, 'mock-failure': S16.phFail },
    [S16.phFail]: { 'start-photo': S16.ph, 'view-details': S13.det, back: S13.sum },
    [S16.bank]: { 'view-details': S13.det, back: S13.sum },
    [S16.done]: { 'kyc-continue': S16.cd, 'view-details': S13.det, back: S13.sum },
    [S16.cd]: { 'view-details': S13.det, back: S16.done },
    [S16.pl]: { 'pledge-securities': S16.plOtp, 'view-securities': S13.det, back: S16.cd },
    [S16.plOtp]: { close: S16.pl },
    [S16.ag]: { 'sign-agreement': S16.sl },
    [S16.agSigned]: { 'setup-emandate': S16.em },
    [S16.agFail]: { 'setup-emandate': S16.em },
    [S16.es]: { 'sign-now': S16.esOtp },
    [S16.np]: { 'npci-accept': S16.emDone, 'npci-reject': S16.agFail },
    [S16.sb]: { 'view-loan': S16.yl },
  };
  const AUTO2 = [[S16.esDone, S16.agDone, 1500], [S16.emDone, S16.sb, 2000]];
  const countdown = (id, from, to) => {
    let left = from; const c = document.getElementById(id);
    const t = setInterval(() => { left -= 1; if (c) c.textContent = Math.max(left, 0); if (left <= 0) { clearInterval(t); go(to); } }, 1000);
    TIMERS.push(t);
  };
  const q1 = (s) => document.querySelector(s);

  // 16.7 Bank Details: manual entry (account + confirm, IFSC → bank / branch, type, holder) or UPI ID fetch
  BEHAVIOUR[S16.bank] = () => {
    const f = q1('.bk-form'); if (!f) return;
    const $ = (id) => f.querySelector('#' + id);
    const map = { acc: 'bk-acc', acc2: 'bk-acc2', ifsc: 'bk-ifsc', type: 'bk-type', holder: 'bk-holder', upi: 'bk-upi' };
    const err = (k, m) => { const e = f.querySelector(`[data-bk-err="${k}"]`); if (e) e.textContent = m || ''; if (map[k]) $(map[k]).classList.toggle('has-err', !!m); };
    let mode = 'manual';
    f.querySelectorAll('[data-bk]').forEach((b) => { b.onclick = () => {
      mode = b.dataset.bk;
      f.querySelectorAll('[data-bk]').forEach((x) => x.classList.toggle('on', x === b));
      f.querySelector('.bk-manual').hidden = mode !== 'manual';
      f.querySelector('.bk-upi').hidden = mode !== 'upi';
    }; });
    ['bk-acc', 'bk-acc2'].forEach((id) => $(id).addEventListener('input', () => { $(id).value = $(id).value.replace(/\D/g, '').slice(0, 18); err(id === 'bk-acc' ? 'acc' : 'acc2', ''); }));
    $('bk-ifsc').addEventListener('input', () => {
      const v = $('bk-ifsc').value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 11); $('bk-ifsc').value = v; err('ifsc', '');
      const ok = /^[A-Z]{4}0[A-Z0-9]{6}$/.test(v);
      $('bk-bank').value = ok ? (IFSC_BANKS[v.slice(0, 4)] || 'Bank (demo lookup)') : '';
      $('bk-branch').value = ok ? `Branch ${v.slice(5)} (demo)` : '';
    });
    $('bk-type').addEventListener('change', () => err('type', ''));
    $('bk-holder').addEventListener('input', () => { const h = $('bk-holder'); h.value = h.value.replace(/[^A-Za-z .]/g, ''); err('holder', ''); });
    $('bk-upi').addEventListener('input', () => err('upi', ''));
    f.querySelector('[data-cta="verify-bank"]').onclick = () => {
      if (mode === 'upi') {
        const u = $('bk-upi').value.trim();
        if (!/^[\w.\-]{2,}@[A-Za-z]{2,}$/.test(u)) return err('upi', 'Please enter a valid UPI ID (e.g. name@okhdfcbank).');
        store.set(KB.bank, { holder: KYC_PROFILE.name, account: '50100987654321', ifsc: 'HDFC0001234', name: 'HDFC Bank', type: 'Savings' });   // prototype: any valid UPI ID returns this account
        return go(S16.done);
      }
      const a = $('bk-acc').value, a2 = $('bk-acc2').value, ic = $('bk-ifsc').value, t = $('bk-type').value, h = $('bk-holder').value.trim();
      const e = {
        acc: !a ? 'Please enter your account number.' : a.length < 9 ? 'Account number must be 9 to 18 digits.' : '',
        acc2: !a2 ? 'Please confirm your account number.' : a2 !== a ? 'Account numbers do not match.' : '',
        ifsc: /^[A-Z]{4}0[A-Z0-9]{6}$/.test(ic) ? '' : 'Please enter a valid IFSC code (e.g. HDFC0001234).',
        type: t ? '' : 'Please select account type.',
        holder: h ? '' : 'Please enter the account holder name.',
      };
      Object.entries(e).forEach(([k, m]) => err(k, m));
      if (Object.values(e).some(Boolean)) return;
      store.set(KB.bank, { holder: h.toUpperCase(), account: a, ifsc: ic, name: $('bk-bank').value, type: t, logo: ic.startsWith('ICIC') ? 'funds/icici.png' : '' });
      go(S16.done);
    };
  };
  // 16.8 KYC complete: shows the bank account verified on 16.7
  BEHAVIOUR[S16.done] = () => {
    const b = store.get(KB.bank); if (!b) return;
    const tmp = document.createElement('div');
    tmp.innerHTML = T.kyc({ email: 'done', aadhaar: 'done', photo: 'done', bank: b, cont: 'on' });
    q1('main.kyc-page').replaceWith(tmp.querySelector('main.kyc-page'));
  };

  // 17 Customer details: collapse / expand, required fields, Confirm and Continue
  BEHAVIOUR[S16.cd] = () => {
    document.querySelectorAll('[data-toggle]').forEach((b) => { b.onclick = () => b.closest('.cd-sec').classList.toggle('open'); });
    const err = (k, msg) => { const e = q1(`[data-err="${k}"]`); if (e) e.textContent = msg || ''; const f = q1(`.cd-in[data-k="${k}"]`); if (f) f.classList.toggle('has-err', !!msg); };
    document.querySelectorAll('.cd-in').forEach((f) => f.addEventListener(f.tagName === 'SELECT' ? 'change' : 'input', () => {
      if (f.tagName === 'INPUT') { const v = f.value.replace(/[^A-Za-z .&\-/]/g, ''); if (v !== f.value) { f.value = v; return err(f.dataset.k, 'Only letters, spaces and . & - / are allowed.'); } }
      err(f.dataset.k, '');
    }));
    document.querySelectorAll('.cd-chk input').forEach((c) => c.addEventListener('change', () => err('decl', '')));
    const occ = q1('.cd-in[data-k="occupation"]'), other = q1('[data-other-of="occupation"]');
    occ.addEventListener('change', () => { other.hidden = occ.value !== 'Other'; if (other.hidden) { other.querySelector('input').value = ''; err('occupationOther', ''); } });
    q1('[data-cta="confirm-continue"]').onclick = () => {
      let first = null;
      document.querySelectorAll('.cd-in').forEach((f) => {
        if (f.closest('[hidden]')) return;
        const label = f.closest('.cd-f').querySelector('.cd-l').firstChild.textContent.trim();
        const bad = !f.value.trim() ? (f.tagName === 'SELECT' ? `Please select ${label.replace(/\?$/, '').toLowerCase()}.` : f.dataset.k === 'occupationOther' ? 'Please specify your occupation.' : `Please enter ${label.toLowerCase()}.`) : '';
        err(f.dataset.k, bad); if (bad && !first) first = f;
      });
      const decl = [...document.querySelectorAll('.cd-chk input')].every((c) => c.checked);
      err('decl', decl ? '' : 'Please confirm both declarations to continue.');
      if (!decl && !first) first = q1('.cd-chk input');
      if (first) { first.closest('.cd-sec').classList.add('open'); first.scrollIntoView({ block: 'center' }); return; }
      const edits = {}; document.querySelectorAll('.cd-in').forEach((f) => { edits[f.dataset.k] = f.value.trim(); });
      store.set(KB.profile, edits);                        // used in the sanction letter and loan agreement
      go(S16.pl);
    };
  };

  // 18.1 Pledge OTP (demo OTP 000000) → 18.2 Successfully pledged → 3 s → 19
  BEHAVIOUR[S16.plOtp] = demoOtpScreen(joined('.m-plotp'), boxesOf('.m-plotp'), '.m-plotp [data-cta="submit-pledge-otp"]', S16.plDone);
  BEHAVIOUR[S16.plDone] = () => countdown('pl-count', 3, S16.ag);

  // 20 / 21 Sanction letter and loan agreement: full text filled with this application's details
  const docValues = () => {
    const p = { ...KYC_PROFILE, ...(store.get(KB.profile) || {}) }; const amt = APP.amount; const d = new Date(); const p2 = (n) => String(n).padStart(2, '0');
    const mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][d.getMonth()];
    return {
      NAME: p.name, ADDR1: p.addr1, ADDR2: p.addr2, ADDR3: p.addr3, CITY: p.city, DOB: p.dob, GENDER: p.gender,
      FATHER: p.father || '—', MOTHER: p.mother || '—', MOBILE: store.get(K.mobile) || CUSTOMER.mobile, EMAIL: CUSTOMER.email,
      PAN_MASK: 'XXXXX' + ((store.get(K.mobile + '.pan') || {}).pan || 'CBOPA8195B').slice(5), DATE_LONG: `${p2(d.getDate())} ${mon} ${d.getFullYear()}`,
      DATE: `${p2(d.getDate())}/${p2(d.getMonth() + 1)}/${d.getFullYear()}`, PURPOSE: p.purpose || '—', OCCUPATION: p.occupation === 'Other' ? (p.occupationOther || 'Other') : (p.occupation || '—'),
      SOURCE: p.source || '—', INCOME: p.income || '—', LAKHS: (amt / 100000).toFixed(2), AMOUNT_WORDS: inWords(amt), AMOUNT: String(amt),
      DUE: ((amt * 0.105) / 12).toFixed(2), FEE: String(Math.round(amt * 0.005)),
    };
  };
  const loadDoc = () => {
    const el = q1('[data-doc]'); if (!el) return;
    const v = docValues();
    const esc = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    fetch(`assets/docs/${el.dataset.doc}.txt`).then((r) => r.text()).then((t) => {
      el.innerHTML = esc(t)
        .replace(/\{\{(\w+)\}\}/g, (m, k) => `<b>${esc(String(v[k] ?? ''))}</b>`)
        .replace(/^(SHRIRAM CREDIT COMPANY LIMITED ?)$/gm, '<span class="doc-foot">$1</span>');
    }).catch(() => { el.textContent = 'The document could not be loaded.'; });
  };
  BEHAVIOUR[S16.sl] = () => {
    loadDoc();
    const chk = q1('#sl-accept'), btn = q1('[data-cta="sanction-submit"]');
    chk.addEventListener('change', () => { btn.disabled = !chk.checked; });
    btn.onclick = () => { if (chk.checked) go(S16.es); };
  };
  BEHAVIOUR[S16.es] = () => {
    loadDoc();
    const chk = q1('#dg-accept'), btn = q1('[data-cta="sign-now"]');
    chk.addEventListener('change', () => { btn.disabled = !chk.checked; });
  };
  BEHAVIOUR[S16.esOtp] = () => {
    loadDoc();
    const aad = q1('#dg-aadhaar'), boxes = [...document.querySelectorAll('.dg-boxes input')];
    const aErr = (m) => { q1('#dg-aadhaar-err').textContent = m || ''; aad.classList.toggle('has-err', !!m); };
    const oErr = (m) => { q1('#dg-otp-err').textContent = m || ''; boxes.forEach((b) => b.classList.toggle('has-err', !!m)); };
    aad.addEventListener('input', () => { aad.value = aad.value.replace(/\D/g, '').slice(0, 16); aErr(''); });
    boxes.forEach((b) => b.addEventListener('input', () => { b.value = b.value.replace(/\D/g, ''); oErr(''); }));
    q1('[data-cta="esign-submit-otp"]').onclick = () => {
      const a = aad.value, v = boxes.map((b) => b.value).join('');
      const ae = !a ? 'Please enter your Aadhaar number or VID.' : (a.length === 12 || a.length === 16) ? '' : 'Aadhaar number must be 12 digits or VID 16 digits.';
      const oe = v.length !== 6 ? 'Please enter the 6-digit OTP.' : v !== OTP_RULES.demoOtp ? 'The OTP you entered is incorrect. Please try again.' : '';
      aErr(ae); oErr(oe);
      if (ae || oe) { if (oe && v.length === 6) boxes.forEach((b) => { b.value = ''; }); return; }
      go(S16.esDone);
    };
  };
  BEHAVIOUR[S16.agDone] = () => countdown('ag-count', 3, S16.agSigned);

  // 22 E-Mandate: bank verified on 16.7, show / hide account number, consent → Submit → NPCI simulation
  BEHAVIOUR[S16.em] = () => {
    const b = store.get(KB.bank);
    if (b) { const tmp = document.createElement('div'); tmp.innerHTML = T.emandate(b); q1('main.em-bg').replaceWith(tmp.querySelector('main.em-bg')); }
    document.querySelectorAll('.em-mode input').forEach((r) => r.addEventListener('change', () => {
      document.querySelectorAll('.em-mode').forEach((m) => m.classList.toggle('on', m.querySelector('input').checked));
    }));
    const acc = q1('#em-acc'), masked = acc.textContent;
    q1('[data-cta="em-eye"]').onclick = () => { acc.textContent = acc.textContent === masked ? acc.dataset.full.replace(/(\d{4})(?=\d)/g, '$1 ') : masked; };
    const chk = q1('#em-accept'), btn = q1('[data-cta="em-submit"]');
    chk.addEventListener('change', () => { btn.disabled = !chk.checked; });
    btn.onclick = () => { if (chk.checked) go(S16.np); };
  };
  BEHAVIOUR[S16.np] = () => {
    const d = new Date(); const p2 = (n) => String(n).padStart(2, '0');
    const rand = Array.from({ length: 13 }, () => 'ABCDEFGHJKLMNPQRSTUVWXYZ'[Math.floor(Math.random() * 24)]).join('');
    q1('#np-txn').textContent = `MMI${String(d.getFullYear()).slice(2)}${p2(d.getMonth() + 1)}${p2(d.getDate())}${p2(d.getHours())}${p2(d.getMinutes())}${p2(d.getSeconds())}${rand}`;
  };

  Object.entries(NAV2).forEach(([scr, map]) => {
    const prev = BEHAVIOUR[scr];
    BEHAVIOUR[scr] = () => {
      if (prev) prev();
      Object.entries(map).forEach(([cta, to]) => {
        const els = cta === 'close' ? document.querySelectorAll('.overlay .close') : document.querySelectorAll(`[data-cta="${cta}"]`);
        els.forEach((el) => { el.style.cursor = 'pointer'; el.onclick = (e) => { e.preventDefault(); go(to); }; });
      });
    };
  });
  AUTO2.forEach(([from, to, ms]) => { const prev = BEHAVIOUR[from]; BEHAVIOUR[from] = () => { if (prev) prev(); TIMERS.push(setTimeout(() => go(to), ms)); }; });

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
  const PRD_ROW = { '01': '1', '02': '2', '03': '3', '04': '4', '05': '5', '06': '7', '07': '7', '07.1': '7.1', '07.2': '8', '07.3': '9', '07.4': '10', '07.5': '11', '08': '12', '09': '13', '10': '14', '11': '15', '12': '16', '12.1.1': '16.1', '12.1.2': '16.1', '12.1.3': '16.1', '12.2': '16', '13.1': '17.1', '13.2': '17', '13.3': '17.2', '13.4': '17.3', '13.5': '17.4', '13.6': '17.5', '14': '18', '16.1': '19', '16.2': '19.1', '16.3': '19.2', '16.4': '19.3', '16.5.1': '19.4', '16.5.2': '19.5', '16.5.3': '19.6', '16.5.4': '19.7', '16.5.5': '19.8', '16.5.6': '19.9', '16.5.7': '19.10', '16.5.8': '19.11', '16.5.9': '19.12' };
  const prdHref = (screen) => {
    const BY_NAME = { '12.2) Refresh portfolio': '16.2', '12.2) Curated offers page for dorpoff view': '16.3' };   // two screens share 12.2
    const row = BY_NAME[screen] || PRD_ROW[(String(screen).match(/^([\d.]+)\)/) || [])[1]];
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

  window.LAMF = { BANK_DEMO, T, render, renderPRD, withModal, loader, SEL_DEFAULT, SCREENS, FLOW, BEHAVIOUR, OTP_RULES, OTP_ERR, MOBILE_ERR, FUNDS, F, PORTFOLIO, CUSTOMER };
})();
