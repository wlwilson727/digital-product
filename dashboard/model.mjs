export const fields=['id','date','product','development','approval','listing','price','orders','refunds','fees','ads','delivery','production','fixed','visits','new_customers'];
const numeric=fields.slice(6);
export function parseCSV(text){
 if(typeof text!=='string'||text.length>2000000)throw Error('CSV must be text under 2 MB.');
 const rows=[];let row=[],cell='',quoted=false,closed=false;
 for(let i=0;i<text.length;i++){const c=text[i];if(quoted){if(c==='"'){if(text[i+1]==='"'){cell+='"';i++;}else{quoted=false;closed=true;}}else cell+=c;}else if(c==='"'){if(cell||closed)throw Error('Unexpected quote.');quoted=true;}else if(c===','){row.push(cell);cell='';closed=false;}else if(c==='\n'||c==='\r'){if(c==='\r'&&text[i+1]==='\n')i++;row.push(cell);rows.push(row);row=[];cell='';closed=false;}else{if(closed)throw Error('Characters after closing quote.');cell+=c;}}
 if(quoted)throw Error('Unclosed quoted field.');if(cell||row.length||closed){row.push(cell);rows.push(row);}return rows;
}
export function validate(rows){
 if(!Array.isArray(rows)||rows.length>10000)throw Error('Expected at most 10,000 records.');const ids=new Set();
 return rows.map((r,i)=>{if(!r||Object.keys(r).length!==fields.length||fields.some(k=>!(k in r)))throw Error(`Row ${i+1}: schema mismatch.`);const out={};for(const k of fields){if(numeric.includes(k)){if(String(r[k]).trim()===''||!Number.isFinite(Number(r[k]))||Number(r[k])<0||Number(r[k])>1e12)throw Error(`Row ${i+1}: invalid ${k}.`);out[k]=Number(r[k]);}else{if(typeof r[k]!=='string'||!r[k].trim()||r[k].length>200)throw Error(`Row ${i+1}: invalid ${k}.`);out[k]=r[k];}}
 if(!/^\d{4}-\d{2}-\d{2}$/.test(out.date)||!Number.isFinite(Date.parse(out.date))||new Date(out.date).toISOString().slice(0,10)!==out.date)throw Error('Invalid date.');
 if(ids.has(out.id))throw Error('Duplicate record ID.');ids.add(out.id);
 if(!['planned','building','ready'].includes(out.development)||!['pending','approved','rejected'].includes(out.approval)||!['draft','live','archived'].includes(out.listing))throw Error('Invalid status.');
 if(out.price*out.orders>1e12)throw Error('Gross sales exceeds supported range.');
 for(const k of ['orders','visits','new_customers'])if(!Number.isSafeInteger(out[k]))throw Error(`${k} must be an integer.`);
 if(out.new_customers>out.orders||out.refunds>out.orders*out.price)throw Error('Refunds or customers exceed sales.');return out;});
}
export function importCSV(text){const [header,...rows]=parseCSV(text.replace(/^\uFEFF/,''));if(!header||header.join(',')!==fields.join(','))throw Error('Headers must exactly match the template.');return validate(rows.map(r=>{if(r.length!==fields.length)throw Error('Incorrect column count.');return Object.fromEntries(fields.map((k,i)=>[k,r[i]]));}));}
export function exportCSV(rows){return [fields,...rows.map(r=>fields.map(k=>r[k]))].map(r=>r.map(v=>{let s=String(v);if(/^[\s]*[=+\-@]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';}).join(',')).join('\r\n');}
export function totals(rows){rows=validate(rows);const t={gross:0,refunds:0,fees:0,ads:0,delivery:0,production:0,fixed:0,orders:0,visits:0,new_customers:0};for(const r of rows){t.gross+=r.price*r.orders;for(const k of Object.keys(t).filter(k=>k!=='gross'))t[k]+=r[k];}t.net=t.gross-t.refunds-t.fees;t.contribution=t.net-t.ads-t.delivery;t.profit=t.contribution-t.production-t.fixed;t.conversion=t.visits?t.orders/t.visits:null;t.cac=t.new_customers?t.ads/t.new_customers:null;t.margin=t.gross?t.contribution/t.gross:null;return t;}
export const demo=validate([
 {id:'demo-1',date:'2026-09-01',product:'service-pricing',development:'ready',approval:'pending',listing:'draft',price:39,orders:12,refunds:39,fees:15,ads:80,delivery:0,production:120,fixed:20,visits:400,new_customers:10},
 {id:'demo-2',date:'2026-09-01',product:'cashflow-planner',development:'ready',approval:'pending',listing:'draft',price:49,orders:8,refunds:0,fees:12,ads:75,delivery:0,production:150,fixed:20,visits:300,new_customers:7},
 {id:'demo-3',date:'2026-10-01',product:'project-estimator',development:'ready',approval:'pending',listing:'draft',price:39,orders:10,refunds:39,fees:13,ads:85,delivery:0,production:100,fixed:20,visits:350,new_customers:9},
 {id:'demo-4',date:'2026-10-01',product:'service-pricing',development:'ready',approval:'pending',listing:'draft',price:39,orders:16,refunds:0,fees:18,ads:95,delivery:0,production:0,fixed:20,visits:430,new_customers:14}
]);
