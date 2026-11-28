/* LMS prototype – sample loans for Loans → Active and the loan page (DISC-538, DISC-539). SAMPLE data only:
   no real customer names, PANs, mail IDs or phone numbers. Source file. */
window.LMS_LOAN = (function () {
  var PROD = { LAMF20261102: 'LAMF_UAT_SCCL_LOC', LAMF20261101: 'LAMF_UAT_NOV_2026_SCCL_MULTIPLE' };
  // LAN, product, client, PAN, sanction, start (DD/MM/YYYY), LSP, credit score
  var L = [
    ['SCCLMF20261100043', 'LAMF20261102', 'Ravi Kumar Sample', 'ABCPK1234A', 1200000, '26/11/2026', 'SCCL LOS', 767],
    ['SCCLMF20261100042', 'LAMF20261102', 'Priya Test Narayanan', 'BCDPN2345B', 500000, '25/11/2026', 'SCCL LOS', 781],
    ['SCCLMF20261100041', 'LAMF20261102', 'Arun Demo', 'CDEPA3456C', 150000, '24/11/2026', 'Quicklend', 742],
    ['SCCLMF20261100040', 'LAMF20261101', 'Meena Sample Raj', 'DEFPM4567D', 300000, '21/11/2026', 'LARK', 803],
    ['SCCLMF20261100039', 'LAMF20261101', 'Karthik Test', 'EFGPK5678E', 1000000, '18/11/2026', 'Liquify', 755],
    ['SCCLMF20261100038', 'LAMF20261102', 'Divya Demo Iyer', 'FGHPD6789F', 75000, '14/11/2026', 'SCCL LOS', 790],
    ['SCCLMF20261100037', 'LAMF20261101', 'Suresh Sample', 'GHIPS7890G', 400000, '10/11/2026', 'Forward Wealth', 736],
    ['SCCLMF20261100036', 'LAMF20261101', 'Lakshmi Test Devi', 'HIJPL8901H', 250000, '05/11/2026', 'Test', 812]
  ];
  function inr(n, dec) {   // Indian grouping: ₹12,00,000 / ₹1,178.82
    var neg = n < 0, x = Math.abs(n), s = dec ? x.toFixed(2) : String(Math.round(x)), p = s.split('.'), i = p[0], last = i.slice(-3), rest = i.slice(0, -3);
    if (rest) last = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' + last;
    return '₹' + (neg ? '-' : '') + last + (p[1] ? '.' + p[1] : '');
  }
  function endDate(d, months) {   // start + tenure, minus one day
    var a = d.split('/'), t = new Date(+a[2], +a[1] - 1 + months, +a[0] - 1), z = function (v) { return (v < 10 ? '0' : '') + v; };
    return z(t.getDate()) + '/' + z(t.getMonth() + 1) + '/' + t.getFullYear();
  }
  var TENURE = 48;
  function get(r) {
    var fee = Math.round(r[4] * 0.008), gst = Math.round(fee * 0.18), first = r[2].split(' ')[0].toLowerCase();
    return { lan: r[0], product: r[1], productName: PROD[r[1]] || r[1], client: r[2], pan: r[3], sanction: r[4], start: r[5], lsp: r[6], score: r[7],
      end: endDate(r[5], TENURE), tenure: TENURE, roi: '10.5%', fee: fee, gst: gst, pf: fee + gst,
      mail: first + '.sample@example.com', phone: '+9198765' + r[0].slice(-5) };
  }
  return { inr: inr, all: function () { return L.map(get); }, find: function (lan) { for (var i = 0; i < L.length; i++) if (L[i][0] === lan) return get(L[i]); return null; } };
})();
