/* LMS prototype (DISC-520) – turns a product saved from Create a Product (localStorage "lms-products" – DISC-524/525 new key, old test products cleared, this browser only)
   into the texts shown on the Products list and the product page. Source file. */
window.LMS_PROD = (function () {
  var inr = function (v) { var n = Number(String(v).replace(/[^\d.]/g, '')); return isNaN(n) || v === '' ? '' : '₹' + n.toLocaleString('en-IN'); };
  var pct = function (v) { return v === '' || v == null ? '' : String(+v) + '%'; };
  var dmy = function (v) { var p = (v || '').split('-'); return p.length === 3 ? p[2] + '/' + p[1] + '/' + p[0] : '-'; };
  var pf = function (u, v) { return v === '' || v == null ? '' : u === '%' ? pct(v) : inr(v); };
  var dash = function (s) { return s && s !== '₹0' && s !== '0%' ? s : '-'; };
  // DISC-521: who is logged in (mail from the OTP step) and the display name; the maker of a product is the user who submitted it
  function me() { try { return sessionStorage.getItem('lms-user') || 'azhagarsamy.s@shriramcredit.in'; } catch (e) { return 'azhagarsamy.s@shriramcredit.in'; } }
  function nameOf(m) { if (!m) return '-'; if (m === 'azhagarsamy.s@shriramcredit.in') return 'Azhagarsamy S';
    return m.split('@')[0].split(/[._-]+/).map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1); }).join(' '); }
  function rid() { var c = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz', r = ''; for (var i = 0; i < 10; i++) r += c.charAt(Math.floor(Math.random() * c.length)); return r; }
  function save(l) { try { localStorage.setItem('lms-products-v3', JSON.stringify(l)); } catch (e) {} }
  function load() { try { return JSON.parse(localStorage.getItem('lms-products-v3')) || []; } catch (e) { return []; } }
  function list(x) {   // Products list columns
    var t = x.terms;
    return { validity: dmy(x.from) + ' - ' + dmy(x.till),
      sa: t && t['t-sa1'] ? inr(t['t-sa1']) + ' - ' + inr(t['t-sa2']) : '-',
      ri: t && t['t-ri1'] ? pct(t['t-ri1']) + ' - ' + pct(t['t-ri2']) : '-',
      pf: t && t['t-pf1'] ? pf(t['t-pu1'], t['t-pf1']) + ' - ' + pf(t['t-pu2'], t['t-pf2']) : '-' };
  }
  function page(x) {   // product page (same fields as the UAT product page)
    var t = x.terms || {}, c = x.charges || {}, k = x.coll || {}, l = list(x);
    var ten = t['t-tt'] === 'Discrete' ? (t.chips || []).join(', ') + ' months' : t['t-te1'] + ' months - ' + t['t-te2'] + ' months';   // UAT: 12 months - 36 months
    var mand = k.mand === 'Multiple of Loan Amount' ? (k.amt || '') + ' time(s) of Sanction amount' : k.mand === 'Absolute Value' ? inr(k.amt) : 'Sanction amount';
    var rt = [k.bt && 'Interest Only', k.fa && 'Fully Amortized'].filter(Boolean).join('\u2003');   // UAT shows Balloon Type as "Interest Only"
    return { n: x.name, st: x.status || 'Draft', req: x.req, maker: x.maker, on: x.on, v: l.validity, s: x.desc || '-', kyc: x.kyc && x.kyc.liv ? ['Liveness'] : [],
      f: { 'Disbursement Type': ({ 'Revolving Overdraft': 'Revolving', 'Single Disbursement': 'Single', 'Multiple Disbursement': 'Multiple' })[x.disb] || '-',
        'Sanction Amount': l.sa, 'Rate of Interest': t['t-ri1'] === t['t-ri2'] ? pct(t['t-ri1']) : l.ri, 'Tenure': ten, 'Processing Fee': l.pf,
        'Maximum Mandate Amount': mand, 'Repayment Type': rt || '-', 'Repayment Frequency': k.mo && k.day ? k.day + ', Monthly' : '-',
        'Collection of PF': k.pf === '1st Collection' ? 'First Collection' : 'First Disbursement', 'Access Policy': 'Access granted to all clients',
        'Renewal Charges': dash(inr(c['c-ren'])), 'Bounce Charges': dash(inr(c['c-bou'])), 'Bank Mandate Swap Charges': dash(inr(c['c-bms'])),
        'Penal Charges': dash(pct(c['c-pen'])), 'Liquidation Charges': dash(pct(c['c-liq'])), 'Prepayment Charges': dash(pct(c['c-pre'])) } };
  }
  return { load: load, save: save, list: list, page: page, me: me, nameOf: nameOf, rid: rid };
})();
