// Run with: node api/lead.test.js
const assert = require('assert');
const mod = require('./lead.js');
process.env.RESEND_API_KEY = 're_test'; process.env.LEAD_FROM_EMAIL = 'Stone & Rose <leads@stoneandrosellc.com>';
const mkRes = () => { const r = { code: 0, body: null, headers: {} }; r.status = (c) => { r.code = c; return r; }; r.json = (b) => { r.body = b; return r; }; r.setHeader = (k, v) => { r.headers[k] = v; }; return r; };
(async () => {
  const sent = [];
  const ok = async (url, opts) => { sent.push({ url, opts: JSON.parse(opts.body), auth: opts.headers.Authorization }); return { ok: true }; };
  // 1. homeowner lead sends owner email + auto reply
  let res = mkRes();
  await mod.handler({ method: 'POST', body: { type: 'homeowner', firstName: 'Ana', lastName: '<b>Lee</b>', email: 'ana@example.com', service: 'Full Backyard Design', message: 'Hello\n<script>x</script>' } }, res, ok);
  assert.strictEqual(res.code, 200); assert.strictEqual(sent.length, 2);
  assert.deepStrictEqual(sent[0].opts.to, ['tony@stoneandrosellc.com']); assert.strictEqual(sent[0].opts.reply_to, 'ana@example.com');
  assert.ok(!sent[0].opts.html.includes('<script>'), 'html must be escaped'); assert.ok(sent[0].opts.html.includes('&lt;script&gt;'));
  assert.deepStrictEqual(sent[1].opts.to, ['ana@example.com']); assert.ok(sent[1].opts.text.includes('(480) 650-8957'));
  assert.strictEqual(sent[0].auth, 'Bearer re_test');
  // 2. partner lead needs company and trade
  res = mkRes(); await mod.handler({ method: 'POST', body: { type: 'partner', firstName: 'Sam', email: 's@x.co' } }, res, ok); assert.strictEqual(res.code, 400);
  res = mkRes(); sent.length = 0; await mod.handler({ method: 'POST', body: { type: 'partner', firstName: 'Sam', email: 's@x.co', company: 'Blue Pools', service: 'Pool builder' } }, res, ok);
  assert.strictEqual(res.code, 200); assert.ok(sent[0].opts.subject.includes('Contractor partnership inquiry'));
  // 3. honeypot sends nothing
  res = mkRes(); sent.length = 0; await mod.handler({ method: 'POST', body: { firstName: 'Bot', email: 'b@x.co', service: 'x', website: 'http://spam' } }, res, ok);
  assert.strictEqual(res.code, 200); assert.strictEqual(sent.length, 0);
  // 4. bad email, wrong method, missing config, Resend failure
  res = mkRes(); await mod.handler({ method: 'POST', body: { firstName: 'A', email: 'nope', service: 'x' } }, res, ok); assert.strictEqual(res.code, 400);
  res = mkRes(); await mod.handler({ method: 'GET' }, res, ok); assert.strictEqual(res.code, 405);
  const k = process.env.RESEND_API_KEY; delete process.env.RESEND_API_KEY;
  res = mkRes(); await mod.handler({ method: 'POST', body: { firstName: 'A', email: 'a@x.co', service: 'x' } }, res, ok); assert.strictEqual(res.code, 503);
  process.env.RESEND_API_KEY = k;
  res = mkRes(); await mod.handler({ method: 'POST', body: { firstName: 'A', email: 'a@x.co', service: 'x' } }, res, async () => ({ ok: false, status: 403 })); assert.strictEqual(res.code, 502);
  console.log('lead.js: all 8 checks passed');
})().catch((e) => { console.error(e); process.exit(1); });
