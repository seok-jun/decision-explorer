#!/usr/bin/env node
'use strict';
// Trusted local artifacts only. Real Chromium DOM tests, not a VM sandbox.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const args = process.argv.slice(2);
const options = {};
for (let i=0; i<args.length; i+=2) {
  if (!['--target','--browser','--report'].includes(args[i]) || !args[i+1]) {
    console.error('Usage: node run-memory-ui.cjs [--target fragment.html] [--browser chromium-executable] [--report report.json]');
    process.exit(2);
  }
  options[args[i].slice(2)] = args[i+1];
}
let chromium;
try { ({ chromium } = require('playwright')); }
catch { console.error('Playwright is required for this eval. Install in your development workspace and set NODE_PATH to its node_modules.'); process.exit(2); }
const target = path.resolve(options.target || path.join(__dirname,'fixtures','memory-case.html'));
const html = fs.readFileSync(target,'utf8');
const results = [];
const dataset = JSON.parse(fs.readFileSync(path.join(__dirname, 'evals.json'), 'utf8'));
const report = {
  skill:'decision-explorer', version:dataset.version, target,
  checked_at:new Date().toISOString(), engine:'Playwright / Chromium', results,
  scope:'Browser behavior of the memory fixture and seeded broken variants; not a live host integration or model-generation evaluation.',
  generation_evals:{defined:dataset.evals.length, executed:0},
  limitations:['Host CSS and APIs are emulated.','Distinct visible results do not establish causal truth; semantic grading is separate.']
};
let browser;
async function check(name, fn) {
  try { await fn(); results.push({name,status:'pass'}); }
  catch (error) { results.push({name,status:'fail',error:error.message}); }
}
async function load({source=html, state=null, api='ok', width=736, js=true}={}) {
  const context=await browser.newContext({viewport:{width,height:1000},javaScriptEnabled:js});
  const page=await context.newPage();
  const requests=[], errors=[];
  await context.route('**/*',route=>{requests.push(route.request().url());return route.abort();});
  page.on('pageerror',error=>errors.push(error.message));
  const bootstrap=`window.__saved=[];window.__sent=[];window.openai={widgetState:${JSON.stringify(state).replace(/</g,'\\u003c')},setWidgetState(value){window.__saved.push(JSON.parse(JSON.stringify(value)));${api==='throw'?'throw Error("Unavailable");':api==='reject'?'return Promise.reject(Error("Unavailable"));':'return Promise.resolve();'}},sendFollowUpMessage(value){window.__sent.push(value);}};${api==='absent'?'delete window.openai;':''}`;
  await page.setContent(`<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>
    :root{--font-size-base:14px;--foreground:#242424;--muted-foreground:#555;--viz-series-1:#2255aa;}body{font:14px/1.5 sans-serif;margin:16px;}[hidden]{display:none!important;}*{box-sizing:border-box;}.btn{padding:8px;}.viz-controls,.viz-row{display:flex;flex-wrap:wrap;gap:8px;}.form-label{display:grid;gap:6px;}.form-select{max-width:100%;font:inherit;padding:8px;}.text-small{font-size:12px;}.table{width:100%;border-collapse:collapse;}td,th{text-align:left;padding:5px;}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;}
    </style></head><body><script>${bootstrap}</script>${source}</body></html>`);
  return {page,context,requests,errors};
}
async function withPage(settings, fn) {
  const env=await load(settings);
  try { await fn(env); assert.deepEqual(env.errors,[],'Browser script error'); assert.deepEqual(env.requests,[],'Unexpected network request'); }
  finally { await env.context.close(); }
}
const selectOption=(page,name)=>page.locator(`[data-option="${name}"]`).click();
async function visibility(page) {
  await selectOption(page,'ask');
  assert.equal(await page.locator('#me-boundary').isVisible(),true);
  assert.equal(await page.locator('#me-retry-boundary').isVisible(),false);
  await selectOption(page,'retry');
  assert.equal(await page.locator('#me-boundary').isVisible(),false,'A-only condition exposed on B');
  assert.equal(await page.locator('#me-retry-boundary').isVisible(),true);
}
async function outcomes(page,option,selector,values) {
  await selectOption(page,option);
  const snapshots=[];
  for (const value of values) {
    await page.locator(selector).selectOption(value);
    const next=(await page.locator('#me-next').innerText()).trim();
    const outcome=(await page.locator('#me-outcome').innerText()).trim();
    assert.ok(next && outcome && !/undefined|null/.test(next+outcome));
    snapshots.push({next,outcome});
  }
  assert.equal(new Set(snapshots.map(x=>x.next)).size,values.length,`${option}: next action did not change`);
  assert.equal(new Set(snapshots.map(x=>x.outcome)).size,values.length,`${option}: substantive outcome did not change`);
}
const retryOutcomes=page=>outcomes(page,'retry','#me-retry-boundary',['unknown','recovered','failed']);
async function rejectedMutation(name, replace, oracle) {
  await check(name,async()=>{
    const source=replace(html);
    assert.notEqual(source,html,'Mutation was not applied; eval adapter needs updating');
    await withPage({source},async({page})=>{
      let detected=false;
      try { await oracle(page); } catch (error) { if(error.code!=='ERR_ASSERTION')throw error; detected=true; }
      assert.equal(detected,true,'Broken variant incorrectly passed the behavioral oracle');
    });
  });
}
async function main() {
  browser=await chromium.launch({headless:true,...(options.browser?{executablePath:path.resolve(options.browser)}:{})});
  report.browser_version=browser.version();
  await check('relevant condition visibility',()=>withPage({},({page})=>visibility(page)));
  await check('A: all three conditions change substantive outcomes',()=>withPage({},({page})=>outcomes(page,'ask','#me-boundary',['unknown','supplied','forgotten'])));
  await check('B: all three conditions change substantive outcomes',()=>withPage({},({page})=>retryOutcomes(page)));
  await check('A → B → A preserves separate condition state',()=>withPage({},async({page})=>{
    await page.locator('#me-boundary').selectOption('forgotten');
    const a=await page.locator('#me-outcome').innerText();
    await selectOption(page,'retry');await page.locator('#me-retry-boundary').selectOption('recovered');
    const b=await page.locator('#me-outcome').innerText();
    await selectOption(page,'ask');assert.equal(await page.locator('#me-boundary').inputValue(),'forgotten');assert.equal(await page.locator('#me-outcome').innerText(),a);
    await selectOption(page,'retry');assert.equal(await page.locator('#me-retry-boundary').inputValue(),'recovered');assert.equal(await page.locator('#me-outcome').innerText(),b);
  }));
  await check('preview never becomes decision or sends a response',()=>withPage({},async({page})=>{
    await retryOutcomes(page);
    const saved=await page.evaluate(()=>window.__saved);
    assert.ok(saved.length>=3);
    for(const value of saved){assert.equal(value.modelContent.status,'exploring');assert.equal(value.modelContent.selected_option_id,null);assert.equal(value.modelContent.explicit_response,null);}
    assert.deepEqual(await page.evaluate(()=>window.__sent),[]);
  }));
  await check('stale, foreign, and invalid restored state is ignored',async()=>{
    for(const modelContent of [
      {decision_id:'memory-lookup-timeout-demo',revision:2,status:'exploring',preview_option_id:'retry',boundary:'supplied'},
      {decision_id:'another-case',revision:3,status:'exploring',preview_option_id:'retry'},
      {decision_id:'memory-lookup-timeout-demo',revision:3,status:'exploring',preview_option_id:'invalid',ask_boundary:'recovered',retry_boundary:'supplied'}
    ]) await withPage({state:{modelContent}},async({page})=>{
      assert.equal(await page.locator('[data-option="ask"]').getAttribute('aria-pressed'),'true');
      assert.equal(await page.locator('#me-boundary').inputValue(),'unknown');
      assert.equal(await page.locator('#me-retry-boundary').inputValue(),'unknown');
    });
  });
  await check('matching revision restores correct branch and conditions',()=>withPage({state:{modelContent:{decision_id:'memory-lookup-timeout-demo',revision:3,status:'exploring',preview_option_id:'retry',ask_boundary:'forgotten',retry_boundary:'recovered'}}},async({page})=>{
    assert.equal(await page.locator('[data-option="retry"]').getAttribute('aria-pressed'),'true');
    assert.equal(await page.locator('#me-retry-boundary').inputValue(),'recovered');
    assert.equal(await page.locator('#me-boundary').isVisible(),false);
  }));
  for(const api of ['absent','throw','reject'])await check(`host API ${api}: comparison still works`,()=>withPage({api},({page})=>retryOutcomes(page)));
  await check('keyboard changes the visible B condition and its outcome',()=>withPage({},async({page})=>{
    await selectOption(page,'retry');
    const before=await page.locator('#me-outcome').innerText();
    await page.locator('#me-retry-boundary').focus();await page.keyboard.press('ArrowDown');await page.keyboard.press('Tab');
    assert.equal(await page.locator('#me-retry-boundary').inputValue(),'recovered');
    assert.notEqual(await page.locator('#me-outcome').innerText(),before);
    assert.notEqual(await page.evaluate(()=>document.activeElement?.id),'me-boundary');
  }));
  await check('static fallback includes all six cases without JavaScript',()=>withPage({js:false},async({page})=>{
    await page.locator('summary').click();assert.equal(await page.locator('tbody tr').count(),6);
    for(const row of await page.locator('tbody tr').all()){assert.equal(await row.isVisible(),true);assert.ok((await row.innerText()).trim());}
  }));
  for(const width of [320,736])await check(`layout and interaction at ${width}px`,()=>withPage({width},async({page})=>{
    await retryOutcomes(page);await page.locator('summary').click();
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true,'Horizontal overflow');
    for(const selector of ['#me-retry-boundary','#me-outcome','[data-option="retry"]']){
      const box=await page.locator(selector).boundingBox();assert.ok(box && box.width>0 && box.x>=0 && box.x+box.width<=width+1,`${selector} is clipped`);
    }
  }));
  await rejectedMutation('negative control: frozen B results are rejected',s=>s.replace('const scenario=retryScenarios[retryBoundary];','const scenario=retryScenarios.unknown;'),retryOutcomes);
  await rejectedMutation('negative control: unrelated A condition on B is rejected',s=>s.replace("askCondition.hidden=preview!=='ask';",'askCondition.hidden=false;'),visibility);
  await rejectedMutation('negative control: disconnected B selector is rejected',s=>s.replace("retryBoundaryControl.addEventListener('change',", "retryBoundaryControl.addEventListener('never-fired',"),retryOutcomes);
  await rejectedMutation('negative control: label-only changes are rejected',s=>s.replace('const scenario=retryScenarios[retryBoundary];',"root.querySelector('h3').textContent=retryBoundary;const scenario=retryScenarios.unknown;"),retryOutcomes);
}
(async()=>{
  try { await main(); }
  catch(error){results.push({name:'eval infrastructure',status:'fail',error:error.message});}
  finally { if(browser)await browser.close(); }
  report.summary={passed:results.filter(x=>x.status==='pass').length,failed:results.filter(x=>x.status==='fail').length};
  if(options.report){const destination=path.resolve(options.report);fs.mkdirSync(path.dirname(destination),{recursive:true});fs.writeFileSync(destination,JSON.stringify(report,null,2)+'\n','utf8');}
  console.log(JSON.stringify(report,null,2));
  process.exitCode=report.summary.failed?1:0;
})();
