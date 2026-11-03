const {chromium}=require('C:/Users/Asus/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
(async()=>{
 const root=path.resolve(__dirname,'..');
 const out=path.join(__dirname,'qa');fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const directions=JSON.parse(fs.readFileSync(path.join(__dirname,'iranyok.json'),'utf8').replace(/^\uFEFF/,''));
 const requested=process.argv.slice(2);
 const files=['index.html',...directions.directions.map(d=>`koncepcio-${d.id}-${d.slug}.html`)].filter(f=>!requested.length||requested.includes(f));
 const results=[];
 for(const file of files){
  if(!fs.existsSync(path.join(root,file))) {results.push({file,missing:true});continue;}
  const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const width of [1440,375]){
   await page.setViewportSize({width,height:1000});
   await page.goto(pathToFileURL(path.join(root,file)).href,{waitUntil:'networkidle',timeout:45000});
   await page.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));await document.fonts.ready;});
   await page.screenshot({path:path.join(out,`${file.replace('.html','')}-${width}.png`),fullPage:true});
   const details=await page.evaluate(()=>({title:document.title,overflow:document.documentElement.scrollWidth>innerWidth,h1:document.querySelectorAll('h1').length,brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.getAttribute('src')),badAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>a.hash&&a.hash!=='#'&&!document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a=>a.hash),forms:document.forms.length,fonts:document.fonts.check('500 20px "Cormorant Garamond"')&&document.fonts.check('400 20px Jost')}));
   const faq=page.locator('main details summary').first();
   if(await faq.count()){await faq.click();details.faqOpens=await faq.evaluate(e=>e.parentElement.open);}
   if(width===375){const toggle=page.locator('button[aria-expanded]').first();if(await toggle.count()){await toggle.click();details.mobileMenuOpens=await toggle.getAttribute('aria-expanded')==='true';}}
   results.push({file,width,...details,errors:[...errors]});
  }
  await page.close();
 }
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
