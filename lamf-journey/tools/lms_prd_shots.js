// LMS PRD screenshots (DISC-536): screen shots and field crops of the LMS prototype (lms-app/*), sample data only.
// Run from the repository root with a local server on port 8098 serving the repository root:
//   python3 -m http.server 8098 &  node lamf-journey/tools/lms_prd_shots.js
// Writes lamf-journey/prd-assets/lms/*.png (used by tools/build_lms_prd.py).
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const OUT = path.join(__dirname, '..', 'prd-assets', 'lms');
const U = 'http://localhost:8098/lamf-journey/lms-app/';
fs.mkdirSync(OUT, { recursive: true });

const TERMS = { 't-sa1': '10000', 't-sa2': '20000000', 't-ri1': '11', 't-ri2': '11', 't-tt': 'Range', 't-te1': '12', 't-te2': '36', 't-pu1': '₹', 't-pf1': '1499', 't-pu2': '%', 't-pf2': '1' };
const PROD = { code: 'LAMF20261103', name: 'TEST Product SCCL', desc: 'This is Testing Creation', from: '2026-11-28', till: '2036-11-28', done: 6,
  disb: 'Revolving Overdraft', terms: TERMS, charges: { 'c-ren': '999', 'c-bou': '100', 'c-bms': '250', 'c-pen': '36', 'c-liq': '0', 'c-pre': '0' },
  coll: { mand: 'Sanction Amount', fa: true, bt: true, mo: true, day: '5th', amt: '', pf: '1st Disbursement' }, kyc: { liv: false },
  status: 'In Review', req: 'tnBtVbQKpQvU', maker: 'opsmaker@shriramcredit.in', on: '28/11/2026' };

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage();
  const user = { v: 'opsmaker@shriramcredit.in' }, prods = { v: [PROD] };
  await p.addInitScript(([u, list]) => {
    sessionStorage.setItem('lamf-access', JSON.stringify({ token: 'x', mods: ['lms', 'prd'], exp: Date.now() + 3.6e6, t: Date.now() }));
    if (!sessionStorage.getItem('lms-user')) sessionStorage.setItem('lms-user', u);
    if (!localStorage.getItem('shots-init')) { localStorage.setItem('lms-products-v4', JSON.stringify(list)); localStorage.setItem('shots-init', '1'); }
  }, [user.v, prods.v]);
  const shot = (n, o = {}) => p.screenshot({ path: path.join(OUT, n + '.png'), ...o });
  const el = (sel, n, pad = 6) => p.locator(sel).first().screenshot({ path: path.join(OUT, n + '.png') }).catch((e) => console.log('miss', n, sel));
  const area = async (sel, n, dx, dy, w, h) => {   // a page area around an element – for open lists that overflow it
    const r = await p.locator(sel).first().boundingBox(); if (!r) return console.log('miss', n);
    await p.screenshot({ path: path.join(OUT, n + '.png'), clip: { x: Math.max(0, r.x + dx), y: Math.max(0, r.y + dy), width: w, height: h } });
  };
  const go = async (u) => { await p.goto(U + u); await p.waitForTimeout(500); };
  const setUser = async (m) => { await p.evaluate((x) => sessionStorage.setItem('lms-user', x), m); };
  const setProds = async (l) => { await p.evaluate((x) => localStorage.setItem('lms-products-v4', JSON.stringify(x)), l); };

  // ---- Module 1 – Login
  await go('login.html'); await shot('l01-login');
  await el('#lg-mail', 'l01-mail'); await el('#lg-send', 'l01-send');
  await p.click('#lg-send'); await el('.lg-card', 'l01-err-empty');
  await p.fill('#lg-mail', 'abc@gmail.com'); await p.click('#lg-send'); await el('.lg-card', 'l01-err-bad');
  await p.fill('#lg-mail', 'abc@shriramcredit.in'); await p.click('#lg-send'); await el('.lg-card', 'l01-err-none');
  await go('otp.html?mail=opsmaker%40shriramcredit.in'); await shot('l02-otp');
  await el('.ot-boxes', 'l02-boxes'); await el('.ot-resend', 'l02-timer'); await el('.ot-back', 'l02-back');
  await p.click('.ot-btn'); await el('.ot-card', 'l02-err-short');
  const bx = await p.$$('.ot-boxes input'); for (const x of bx) await x.fill('1'); await p.click('.ot-btn'); await el('.ot-card', 'l02-err-wrong');
  await go('mail-otp.html?mail=opsmaker%40shriramcredit.in'); await shot('l03-mail');

  // ---- Module 2 – Dashboard
  await go('dashboard.html'); await shot('l04-dashboard'); await el('.sb', 'l04-menu'); await el('#kpis', 'l04-kpis');
  await p.click('#sb-av'); await el('#pf', 'l04-profile'); await p.keyboard.press('Escape');
  await p.click('#sb-x'); await p.waitForTimeout(300); await el('.sb', 'l04-menu-wide'); await p.click('#sb-x');

  // ---- Module 3 – Products
  await setProds([]); await go('products.html'); await shot('l05-products');
  await el('.tb thead', 'l05-head'); await el('.pager', 'l05-pager'); await el('#new-prod', 'l05-new');
  await p.hover('#new-prod'); await el('#new-prod', 'l05-new-hover');
  await p.click('#new-prod'); await p.waitForTimeout(200); await shot('l06-security'); await el('#sec .md', 'l06-modal');
  await go('product-view.html?code=LAMF20261102'); await shot('l07-active');
  await el('.pv-h', 'l07-head'); await el('.pv-tabs', 'l07-tabs'); await el('.pv-c', 'l07-card');
  await p.click('#pv-menu'); await area('#pv-menu', 'l07-menu', -250, -8, 290, 110); await p.click('#pv-upd'); await p.waitForTimeout(200); await el('#ap .md', 'l07-policy');
  await p.click('#ap-c'); await p.click('text=Documents'); await el('#t-doc', 'l07-docs');
  await go('product-view.html?code=LAMF20261101'); await shot('l07-inactive'); await el('.pv-h', 'l07-inactive-head');
  await go('product-view.html?code=LAMF20261001'); await shot('l07-inreview'); await el('#pv-foot', 'l07-inreview-foot');

  // ---- Module 4 – Create a Product
  await setProds([]); await go('create-product.html'); await shot('l08-step1');
  await el('#cp-steps', 'l08-steps'); await el('#cp-draft', 'l08-nodraft'); await el('#p1 .cp-2', 'l08-dates'); await el('.cp-pol', 'l08-policy');
  await p.click('#cp-next'); await el('#p1', 'l08-err-name');
  await p.click('#cp-upd'); await p.waitForTimeout(200); await el('#ap .md', 'l08-policy-pop'); await p.click('#ap-c');
  await p.fill('#cp-n', 'TEST Product SCCL'); await p.fill('#cp-d', 'This is Testing Creation'); await p.click('#cp-next'); await p.waitForTimeout(300);
  await el('#cp-draft', 'l08-draft'); await shot('l09-step2'); await el('.cp-rds', 'l09-radios');
  await p.click('.cp-rd:nth-child(1) .cp-i'); await p.waitForTimeout(200); await el('#inf .md', 'l09-info-ro'); await p.mouse.click(30, 30);
  await p.click('.cp-rd:nth-child(2) .cp-i'); await p.waitForTimeout(200); await el('#inf .md', 'l09-info-single'); await p.mouse.click(30, 30);
  await p.click('.cp-rd:nth-child(3) .cp-i'); await p.waitForTimeout(200); await el('#inf .md', 'l09-info-multi'); await p.mouse.click(30, 30);
  await p.click('#cp-next'); await p.waitForTimeout(300); await shot('l10-terms');
  const rows = await p.$$('#p3 .tm-r'); for (let i = 0; i < rows.length; i++) await rows[i].screenshot({ path: path.join(OUT, `l10-row${i + 1}.png`) });
  await p.click('#cp-next'); await shot('l10-terms-err');
  await p.click('#p3 .tm-3 .sel-b'); await area('#p3 .tm-3 .sel', 'l10-tenure-open', -8, -8, 170, 160); await p.click('#p3 .tm-3 .sel-l li:first-child');
  await p.fill('#t-tch', '12'); await p.press('#t-tch', 'Enter'); await p.fill('#t-tch', '24'); await p.press('#t-tch', 'Enter'); await p.fill('#t-tch', '36'); await p.press('#t-tch', 'Enter');
  await el('#p3 .tm-r:nth-child(3)', 'l10-discrete');
  await p.click('#p3 .tm-3 .sel-b'); await p.click('#p3 .tm-3 .sel-l li:nth-child(2)');
  for (const k in TERMS) if (!k.startsWith('t-pu') && k !== 't-tt') await p.fill('#' + k, TERMS[k]);
  await p.click('#cp-next'); await p.waitForTimeout(300); await shot('l11-charges');
  await p.click('#cp-next'); await shot('l11-charges-err'); await el('#cp-draft', 'l11-cannot');
  for (const [k, v] of Object.entries(PROD.charges)) await p.fill('#' + k, v);
  await p.click('#cp-next'); await p.waitForTimeout(300); await shot('l12-collections');
  await p.click('#p5 .sel-b'); await p.click('#p5 .sel-l li:nth-child(2)'); await p.click('#cp-next'); await shot('l12-collections-err');
  await p.click('#p5 .sel-b'); await p.click('#p5 .sel-l li:nth-child(3)'); await el('#k-amw', 'l12-absolute');
  await p.click('#p5 .sel-b'); await p.click('#p5 .sel-l li:nth-child(1)');
  await p.click('text=Fully Amortized'); await p.click('text=Balloon Type'); await p.click('text=Monthly');
  await p.click('.sel.cal .sel-b'); await area('.co-fr', 'l12-days-open', -8, -8, 1000, 270); await p.click('.sel.cal li:nth-child(5)');
  await el('#p5', 'l12-filled');
  await p.click('#cp-next'); await p.waitForTimeout(300); await shot('l13-kyc'); await el('#p6', 'l13-kyc-list');
  await p.click('text=Liveness'); await p.click('#cp-next'); await p.waitForTimeout(250); await el('#cp-toast', 'l13-toast');
  await p.waitForURL('**/products.html'); await p.waitForTimeout(300); await shot('l13-products-inreview');

  // ---- Module 5 – Approvals
  await setProds([PROD]); await go('product-view.html?code=LAMF20261103'); await shot('l14-maker-view'); await el('.pv-chg', 'l14-change'); await el('#pv-foot', 'l14-maker-foot');
  await go('approvals.html'); await shot('l15-pending-empty'); await p.click('text=All Approvals'); await shot('l15-all');
  await p.click('#ct-b'); await area('.ct-th', 'l15-filter', -8, -8, 400, 440); await shot('l15-filter-open'); await p.keyboard.press('Escape');
  await setUser('opschecker@shriramcredit.in'); await go('approvals.html'); await shot('l15-pending');
  await p.click('.ap-lk'); await p.waitForTimeout(300); await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); await shot('l16-checker');
  await el('#ck', 'l16-upload-note'); await el('#pv-foot', 'l16-buttons');
  await p.click('#pv-apr'); await el('#ck', 'l16-note-err');
  await p.fill('#ck-n', 'Test Approved'); await p.click('#pv-apr'); await p.waitForTimeout(200); await el('#cf .md', 'l16-confirm');
  await p.click('#cf-y'); await p.waitForURL('**/approvals.html*'); await p.waitForTimeout(250); await shot('l16-approved'); await el('#ap-toast', 'l16-toast');
  await go('product-view.html?code=LAMF20261103'); await p.click('#pv-menu'); await p.click('#pv-upd'); await p.waitForTimeout(200); await el('#ap .md', 'l16-policy-all');
  await p.click('#ap-rows tr:nth-child(5) .sw'); await p.click('#ap-c'); await p.click('#pv-menu'); await p.click('#pv-upd'); await p.waitForTimeout(200); await el('#ap .md', 'l16-policy-los');

  // ---- Module 6 – Loans
  await go('loans-active.html'); await shot('l17-active'); await el('.sb-grp', 'l17-menu'); await el('#ln-lsp', 'l17-lsp'); await el('.ln-chips', 'l17-chips'); await el('.ln-tb thead', 'l17-head');
  await p.click('#ln-lsp-b'); await area('#ln-lsp', 'l17-lsp-open', -8, -8, 280, 340); await p.keyboard.press('Escape');
  await p.click('.ln-chips button[data-t="1"]'); await shot('l17-shortfall');
  await go('loan-view.html?lan=SCCLMF20261100043'); await shot('l18-loan'); await el('.lv-h', 'l18-head'); await el('#lv-tabs', 'l18-tabs');
  await area('#lv-menu', 'l18-menu-closed', -300, -10, 340, 50); await el('#lv-loan', 'l18-loan-card');
  await el('#lv-loan > div:nth-child(14)', 'l18-pf'); await p.hover('#lv-loan .lv-i'); await area('#lv-loan .lv-i', 'l18-tip', -130, -40, 360, 110);
  await el('#lv-coll', 'l18-coll'); await el('#lv-cli', 'l18-client'); await el('#lv-kfs', 'l18-kfs');
  await p.mouse.move(5, 5); await p.click('#lv-menu'); await area('#lv-menu', 'l18-menu', -240, -10, 280, 440);
  await b.close();
  console.log('LMS PRD shots:', fs.readdirSync(OUT).length);
})();
