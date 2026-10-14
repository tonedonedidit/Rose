// Netlify Function: emails the lead to Stone & Rose and sends the lead an automatic reply, both through Resend.
// Reached at /api/lead (see netlify.toml). Environment variables, set in Netlify (never in this repo):
//   RESEND_API_KEY   from resend.com
//   LEAD_FROM_EMAIL  an address on a domain verified in Resend, e.g. "Stone & Rose <leads@stoneandrosellc.com>"
//   LEAD_TO_EMAIL    where new leads go (default tony@stoneandrosellc.com)
'use strict';

const OWNER_PHONE = '(480) 650-8957';
const DEFAULT_TO = 'tony@stoneandrosellc.com';

const esc = (v) => String(v == null ? '' : v)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
const clip = (v, n) => String(v == null ? '' : v).trim().slice(0, n);
const oneLine = (v, n) => clip(v, n).replace(/[\r\n]+/g, ' ');

function clean(body) {
  return {
    type: body.type === 'partner' ? 'partner' : 'homeowner',
    firstName: oneLine(body.firstName, 80),
    lastName: oneLine(body.lastName, 80),
    company: oneLine(body.company, 120),
    email: oneLine(body.email, 160),
    phone: oneLine(body.phone, 40),
    service: oneLine(body.service, 120),
    message: clip(body.message, 4000),
    website: clip(body.website, 200),
    page: oneLine(body.page, 300)
  };
}

function validate(l) {
  if (!l.firstName) return 'Please enter your name.';
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(l.email)) return 'Please enter a valid email address.';
  if (l.type === 'homeowner' && !l.service) return 'Please choose a project type.';
  if (l.type === 'partner' && (!l.company || !l.service)) return 'Please enter your company and trade.';
  return null;
}

function ownerEmail(l, from, to) {
  const name = (l.firstName + ' ' + l.lastName).trim();
  const label = l.type === 'partner' ? 'Contractor partnership inquiry' : 'New project inquiry';
  const rows = [
    ['Name', name], ['Company', l.company], ['Email', l.email], ['Phone', l.phone],
    [l.type === 'partner' ? 'Trade' : 'Project type', l.service], ['Page', l.page]
  ].filter((r) => r[1]);
  const text = rows.map((r) => r[0] + ': ' + r[1]).join('\n') + '\n\nMessage:\n' + (l.message || '(none)');
  const html = '<h2>' + esc(label) + '</h2><table cellpadding="6">' +
    rows.map((r) => '<tr><td><b>' + esc(r[0]) + '</b></td><td>' + esc(r[1]) + '</td></tr>').join('') +
    '</table><p><b>Message</b></p><p>' + esc(l.message || '(none)').replace(/\n/g, '<br>') + '</p>';
  return { from, to: [to], reply_to: l.email, subject: label + ': ' + name + (l.company ? ' (' + l.company + ')' : ''), text, html };
}

function autoReply(l, from, replyTo) {
  const body = l.type === 'partner'
    ? 'Thanks for reaching out about working together. We received your inquiry and will reply within 24 hours.'
    : 'Thanks for contacting Stone & Rose. We received your project details and will reply within 24 hours.';
  const text = 'Hi ' + l.firstName + ',\n\n' + body + '\n\nIf it is urgent, call ' + OWNER_PHONE + '.\n\nStone & Rose Landscaping\nArizona';
  const html = '<p>Hi ' + esc(l.firstName) + ',</p><p>' + esc(body) + '</p><p>If it is urgent, call ' + esc(OWNER_PHONE) + '.</p><p>Stone &amp; Rose Landscaping<br>Arizona</p>';
  return { from, to: [l.email], reply_to: replyTo, subject: 'We received your message', text, html };
}

async function send(payload, key, fetchImpl) {
  const r = await fetchImpl('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!r.ok) throw new Error('Resend ' + r.status);
}

// Pure core: takes the parsed body and env, returns { status, json }. Easy to test.
async function process_(body, env, fetchImpl) {
  const lead = clean(body || {});
  if (lead.website) return { status: 200, json: { ok: true } }; // honeypot: bots fill it, pretend success
  const problem = validate(lead);
  if (problem) return { status: 400, json: { error: problem } };

  const key = env.RESEND_API_KEY;
  const from = env.LEAD_FROM_EMAIL;
  const to = env.LEAD_TO_EMAIL || DEFAULT_TO;
  if (!key || !from) return { status: 503, json: { error: 'Email is not configured' } }; // front end falls back to Formspree

  try { await send(ownerEmail(lead, from, to), key, fetchImpl); }      // the lead must reach the owner
  catch (e) { return { status: 502, json: { error: 'Could not send' } }; }
  try { await send(autoReply(lead, from, to), key, fetchImpl); } catch (e) { /* auto-reply is best effort */ }
  return { status: 200, json: { ok: true } };
}

// Netlify Functions entry point.
exports.handler = async (event) => {
  const headers = { 'Content-Type': 'application/json' };
  if (event.httpMethod !== 'POST') return { statusCode: 405, headers: Object.assign({ Allow: 'POST' }, headers), body: JSON.stringify({ error: 'Method not allowed' }) };
  let body;
  try {
    const raw = event.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString('utf8') : (event.body || '{}');
    body = JSON.parse(raw);
  } catch (e) { return { statusCode: 400, headers, body: JSON.stringify({ error: 'Invalid request.' }) }; }
  const r = await process_(body, process.env, fetch);
  return { statusCode: r.status, headers, body: JSON.stringify(r.json) };
};
exports._process = process_;
