/* Real-browser smoke checks: starts an isolated local server, never publishes. */
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve(__dirname, '..');
const mime = {'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.json':'application/json'};
const checks=[],blockedChecks=[];
async function main(){
 const server=http.createServer(async(req,res)=>{
  try{const url=new URL(req.url,'http://localhost');let target=path.resolve(root,'.'+decodeURIComponent(url.pathname));
   if(target!==root&&!target.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
   if((await fs.stat(target)).isDirectory())target=path.join(target,'index.html');
   res.setHeader('Content-Type',mime[path.extname(target)]||'application/octet-stream');res.end(await fs.readFile(target));
  }catch{res.writeHead(404);res.end('Not found');}
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base=`http://127.0.0.1:${server.address().port}`;
 let browser;
 try{
  const executablePath=process.env.CHROMIUM_PATH || (require('node:fs').existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined);
  browser=await chromium.launch({executablePath,headless:true,args:['--no-sandbox']});
  const context=await browser.newContext({viewport:{width:1280,height:900},acceptDownloads:true});
  const page=await context.newPage();const errors=[];
  page.on('pageerror',err=>errors.push(err.message));
  await page.goto(base);await page.getByRole('heading',{name:/Build useful tools/}).waitFor();
  assert.equal(await page.locator('article a').count(),4);checks.push('Internal product desk loads');
  await page.goto(base+'/dashboard/');await page.locator('#products tr').first().waitFor();
  assert.match(await page.locator('#source').textContent(),/SYNTHETIC/);
  assert.equal(await page.locator('#products tr').count(),3);
  assert.match(await page.locator('#metrics').textContent(),/\$1,874\.00/);checks.push('Synthetic dashboard renders independently verified gross sales');
  page.on('dialog',dialog=>dialog.accept());
  const templateDownload=page.waitForEvent('download');await page.locator('#template').click();
  const template=await templateDownload;const templateText=await fs.readFile(await template.path(),'utf8');
  assert.match(templateText,/new_customers/);checks.push('Dashboard template downloads');
  await page.locator('#import').setInputFiles({name:'bad.csv',mimeType:'text/csv',buffer:Buffer.from('id,price\nx,-5')});
  await page.getByText(/Import rejected; data unchanged/).waitFor();assert.equal(await page.locator('#products tr').count(),3);
  const {exportCSV,demo}=await import('../dashboard/model.mjs');
  const record={...demo[0],id:'browser-actual',product:'<img src=x onerror=alert(1)>',price:40,orders:5,refunds:20,fees:8,ads:30,delivery:5,production:40,fixed:10,visits:100,new_customers:3};
  await page.locator('#import').setInputFiles({name:'records.csv',mimeType:'text/csv',buffer:Buffer.from(exportCSV([record]))});
  await page.getByText(/CSV imported/).waitFor();assert.match(await page.locator('#source').textContent(),/USER-IMPORTED/);
  assert.equal(await page.locator('#products tr').count(),1);assert.match(await page.locator('#metrics').textContent(),/\$87\.00/);
  assert.equal(await page.locator('#products img').count(),0);await page.reload();assert.match(await page.locator('#source').textContent(),/USER-IMPORTED/);
  checks.push('CSV rejection preserves data; valid import computes $87 profit, escapes HTML and persists');
  await page.locator('#empty').click();assert.equal(await page.locator('#products tr').count(),0);
  await page.locator('#reset').click();assert.equal(await page.locator('#products tr').count(),3);checks.push('Dashboard reset and empty controls');
  for(const slug of ['service-pricing','cashflow-planner','project-estimator']){
   await page.goto(base+`/products/${slug}/`);await page.locator('h1').waitFor();
   assert.ok((await page.locator('h1').textContent()).trim().length>5);
   const scenarios={
    'service-pricing':{currency:'USD',hours:40,weeks:50,billable:50,overhead:20000,pay:80000,tax:0,margin:20,fee:0,materials:0,jobHours:10,fixedFee:0},
    'cashflow-planner':{currency:'USD',opening:1000,minimum:800,incomeScale:100,costScale:100,weeks:Array.from({length:13},(_,i)=>({label:'Week '+(i+1),receipts:100,payments:150,financing:0}))},
    'project-estimator':{currency:'USD',rate:100,contingency:10,margin:20,deposit:50,discount:0,changeHours:2,changeCost:0,client:'Fictional independent test',deliverables:'One original design',exclusions:'Hosting',revisions:'One revision',tasks:[{name:'Design',hours:10,cost:100}]}
   };
   const state=scenarios[slug];
   await page.locator('#import').setInputFiles({name:'scenario.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify({product:slug,version:1,state}))});
   const expected={'service-pricing':['$125.00','$1,250.00','$25,000.00'],'cashflow-planner':['$350.00','$450.00','Week 5'],'project-estimator':['$1,512.50','$756.25']};
   await page.waitForFunction(values=>values.every(value=>document.getElementById('results').textContent.includes(value)),expected[slug]);
   for(const value of expected[slug])assert.ok((await page.locator('#results').textContent()).includes(value),`${slug}: independently expected ${value}`);
   if(slug==='project-estimator'){
    assert.match(await page.locator('#change-result').textContent(),/\$275\.00/);
    await page.locator('#add').click();assert.equal(await page.locator('#tasks tr').count(),2);
    await page.getByRole('button',{name:'Remove task 2',exact:true}).click();assert.equal(await page.locator('#tasks tr').count(),1);
   }
   let event=page.waitForEvent('download');await page.locator('#json').click();let file=await event;
   const saved=JSON.parse(await fs.readFile(await file.path(),'utf8'));assert.deepEqual(saved.state,state);
   event=page.waitForEvent('download');await page.locator('#csv').click();file=await event;
   const csv=await fs.readFile(await file.path(),'utf8');assert.ok(csv.length>80);assert.ok(csv.includes('USD'));
   await page.locator('#import').setInputFiles({name:'invalid.json',mimeType:'application/json',buffer:Buffer.from('{broken')});
   await page.locator('#error:not(.hidden)').waitFor();for(const value of expected[slug])assert.ok((await page.locator('#results').textContent()).includes(value));
   const changed={'service-pricing':['#overhead','0','$100.00'],'cashflow-planner':['#opening','2000','$1,350.00'],'project-estimator':['#rate','200','$2,887.50']};
   await page.locator(changed[slug][0]).fill(changed[slug][1]);assert.ok((await page.locator('#results').textContent()).includes(changed[slug][2]));
   await page.evaluate(()=>{window.print=()=>{window.__printRequested=true;};});await page.locator('#print').click();
   assert.equal(await page.evaluate(()=>window.__printRequested),true);
   const pdf=await page.pdf({path:path.join(root,'test-results',`${slug}-print.pdf`),format:'A4',printBackground:true});assert.ok(pdf.length>1000);
   checks.push(`${slug} input recalculation, print control and PDF rendering`);
   await page.locator('#example').click();await page.reload();assert.equal(await page.locator('#error.hidden').count(),1);
   checks.push(`${slug} independent calculations, editable JSON roundtrip, CSV download and invalid import recovery`);
   const offline=await context.newPage();const outside=[];offline.on('request',r=>{if(/^https?:/.test(r.url()))outside.push(r.url());});
   try{
    await offline.goto(require('node:url').pathToFileURL(path.join(root,'products',slug,'index.html')).href);
    assert.ok((await offline.locator('#results strong').count())>=5);assert.deepEqual(outside,[]);
    checks.push(`${slug} direct-file offline startup without network requests`);
   }catch(err){
    if(!err.message.includes('ERR_BLOCKED_BY_ADMINISTRATOR'))throw err;
    blockedChecks.push(`${slug} direct-file startup: managed Chromium policy blocks file URLs; customer-browser verification required`);
    const local=await context.newPage();const destinations=[];local.on('request',r=>destinations.push(r.url()));
    try{await local.goto(base+`/products/${slug}/`);assert.ok((await local.locator('#results strong').count())>=5);
     assert.ok(destinations.every(url=>url.startsWith(base+'/')));checks.push(`${slug} local startup uses no external network destinations`);
    }finally{await local.close();}
   }finally{await offline.close();}
   await page.screenshot({path:path.join(root,'test-results',`${slug}-desktop.png`),fullPage:true});
   await page.setViewportSize({width:390,height:844});
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
   assert.equal(overflow,false,`${slug} must not overflow narrow viewport`);
   await page.screenshot({path:path.join(root,'test-results',`${slug}-mobile.png`),fullPage:true});
   await page.setViewportSize({width:1280,height:900});checks.push(`${slug} desktop and mobile rendering`);
  }
  await page.goto(base+'/dashboard/');await page.setViewportSize({width:390,height:844});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1),false);
  await page.screenshot({path:path.join(root,'test-results','dashboard-mobile.png'),fullPage:true});
  assert.deepEqual(errors,[]);checks.push('No uncaught browser exceptions; dashboard narrow layout');
  const report={status:'passed',checks,blockedChecks,limitations:['Managed Chromium blocks file URLs; direct-file startup remains unverified in customer browsers','Manual screen reader and Safari/Firefox verification pending','No live Shopify delivery or customer demand validation']};
  await fs.writeFile(path.join(root,'test-results','browser-report.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));
 }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
}
fs.mkdir(path.join(root,'test-results'),{recursive:true}).then(main).catch(async err=>{console.error(err);await fs.writeFile(path.join(root,'test-results','browser-report.json'),JSON.stringify({status:'failed',checks,error:err.message},null,2)+'\n');process.exitCode=1;});
