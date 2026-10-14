// Run with: node netlify/functions/lead.test.js   (uses a mock; sends nothing)
const assert = require('assert');
const mod = require('./lead.js');
const ENV = { RESEND_API_KEY: 're_test', LEAD_FROM_EMAIL: 'Stone & Rose <leads@stoneandrosellc.com>' };
(async () => {
  const sent = [];
  const ok = async (url, opts) => { sent.push({ url, body: JSON.parse(opts.body), auth: opts.headers.Authorization }); return { ok: true }; };
  let r = await mod._process({ type: 'homeowner', firstName: 'Ana', lastName: '<b>Lee</b>', email: 'ana@example.com', service: 'Full Backyard Design', message: 'Hi\n<script>x</script>' }, ENV, ok);
  assert.strictEqual(r.status, 200); assert.strictEqual(sent.length, 2);
  assert.deepStrictEqual(sent[0].body.to, ['tony@stoneandrosellc.com']); assert.strictEqual(sent[0].body.reply_to, 'ana@example.com');
  assert.ok(!sent[0].body.html.includes('<script>') && sent[0].body.html.includes('&lt;script&gt;'));
  assert.deepStrictEqual(sent[1].body.to, ['ana@example.com']); assert.strictEqual(sent[1].body.reply_to, 'tony@stoneandrosellc.com'); assert.ok(sent[1].body.text.includes('(480) 650-8957'));
  assert.strictEqual(sent[0].auth, 'Bearer re_test');
  r = await mod._process({ type: 'partner', firstName: 'Sam', email: 's@x.co' }, ENV, ok); assert.strictEqual(r.status, 400);
  sent.length = 0; r = await mod._process({ type: 'partner', firstName: 'Sam', email: 's@x.co', company: 'Blue Pools', service: 'Pool builder' }, ENV, ok);
  assert.strictEqual(r.status, 200); assert.ok(sent[0].body.subject.includes('Contractor partnership inquiry'));
  sent.length = 0; r = await mod._process({ firstName: 'Bot', email: 'b@x.co', service: 'x', website: 'http://spam' }, ENV, ok); assert.strictEqual(r.status, 200); assert.strictEqual(sent.length, 0);
  r = await mod._process({ firstName: 'A', email: 'nope', service: 'x' }, ENV, ok); assert.strictEqual(r.status, 400);
  r = await mod._process({ firstName: 'A', email: 'a@x.co', service: 'x' }, {}, ok); assert.strictEqual(r.status, 503);
  r = await mod._process({ firstName: 'A', email: 'a@x.co', service: 'x' }, ENV, async () => ({ ok: false, status: 403 })); assert.strictEqual(r.status, 502);
  // Netlify event wrapper: wrong method, bad JSON
  let res = await mod.handler({ httpMethod: 'GET' }); assert.strictEqual(res.statusCode, 405);
  res = await mod.handler({ httpMethod: 'POST', body: '{not json' }); assert.strictEqual(res.statusCode, 400);
  res = await mod.handler({ httpMethod: 'POST', body: JSON.stringify({ firstName: 'A', email: 'nope', service: 'x' }) }); assert.strictEqual(res.statusCode, 400);
  assert.strictEqual(JSON.parse(res.body).error, 'Please enter a valid email address.');
  console.log('netlify lead function: all checks passed');
})().catch((e) => { console.error(e); process.exit(1); });
