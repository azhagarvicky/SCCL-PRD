const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1300,height:1100}});const p=await ctx.newPage();
await ctx.route(x=>!/localhost/.test(x.toString()),r=>r.abort());
await p.goto('http://localhost:8099/communications.html');await p.waitForTimeout(300);
const links=await p.locator('table.sms a.mail-view').all();console.log('view links',links.length);
for(const [k,l] of links.entries()){const [np]=await Promise.all([ctx.waitForEvent('page'),l.click()]);await np.waitForLoadState();await np.waitForTimeout(300);
 console.log(np.url().split('/').pop(),'logo',await np.evaluate(()=>{const i=document.querySelector('img');return i.complete&&i.naturalWidth>0}));
 if(k===2) await np.screenshot({path:'mv4.png'}); await np.close();}
await b.close();})();
