// Netlify verifies the platform signature before invoking this event handler.
// No public email-sending endpoint; only verified Netlify Forms submissions.
import { createHash } from 'node:crypto';

export async function deliverGuide(data, { env = process.env, fetchEmail = fetch } = {}) {
  if (data['request-kind'] !== 'arcapolasi-kisokos-v1') return;
  const email = String(data.email || '').trim();
  const name = String(data.name || '').trim();
  if (data['guide-consent'] !== 'accepted' || data['bot-field'] ||
      !name || name.length > 100 || email.length > 254 ||
      !/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(email)) {
    throw new Error('Invalid guide request');
  }
  const apiKey = String(env.BREVO_API_KEY || '').trim();
  if (!apiKey) throw new Error('BREVO_API_KEY is not configured');
  const sender = 'szeviki1020@gmail.com';
  const link = 'https://elizaweboldal.netlify.app/letoltesek/arcapolasi-kisokos.pdf';
  const escape = value => value.replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  // Retries of the same browser request keep the same provider idempotency key.
  const requestId = String(data['request-id'] || '');
  if (!/^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i.test(requestId)) throw new Error('Missing request identifier');
  // Brevo requires a UUID, not the full 64-character SHA-256 hex string.
  const bytes = createHash('sha256').update(requestId + ':' + email).digest().subarray(0, 16);
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const hex = bytes.toString('hex');
  const key = `${hex.slice(0,8)}-${hex.slice(8,12)}-${hex.slice(12,16)}-${hex.slice(16,20)}-${hex.slice(20)}`;
  const response = await fetchEmail('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: {'api-key': apiKey, 'Content-Type': 'application/json', accept: 'application/json'},
    signal: AbortSignal.timeout(15000),
    body: JSON.stringify({
      sender: {name: 'Eliza Beauty Salon', email: sender},
      replyTo: {name: 'Eliza Beauty Salon', email: sender},
      to: [{email, name}],
      subject: 'Megérkezett az Arcápolási Kisokosod',
      headers: {idempotencyKey: key},
      htmlContent: `<html lang="hu"><body><p>Kedves ${escape(name)}!</p><p>Köszönöm az érdeklődésedet! Az Arcápolási Kisokost az alábbi linken töltheted le:</p><p><a href="${link}">Arcápolási Kisokos letöltése (PDF)</a></p><p>Egyszerű rutin. Figyelmes gondoskodás.</p><p>Ezt az egyszeri levelet a weboldalon benyújtott kérésedre kaptad. Nem iratkoztál fel hírlevélre.</p><p>Eliza Beauty Salon · tanfolyami mintaoldal</p></body></html>`,
      textContent: `Kedves ${name}!\n\nAz Arcápolási Kisokos letöltése: ${link}\n\nEzt az egyszeri levelet a kérésedre kaptad. Nem iratkoztál fel hírlevélre.\n\nEliza Beauty Salon – tanfolyami mintaoldal`
    })
  });
  if (!response.ok) {
    // Classify the response without ever logging its raw text (keys, IPs or PII).
    let reason = 'provider-rejected-request';
    let providerCode = 'unknown';
    try {
      const error = await response.json();
      const allowedCodes = ['invalid_parameter','missing_parameter','out_of_range','permission_denied','account_not_activated','duplicate_parameter','duplicate_request','unauthorized','not_enough_credits'];
      if (allowedCodes.includes(error.code)) providerCode = error.code;
      const message = typeof error.message === 'string' ? error.message.toLowerCase() : '';
      if (response.status === 401) {
        if (message.includes('key not found') || message.includes('invalid api key')) reason = 'api-key-invalid-or-revoked';
        else if (message.includes('ip') && /authoriz|block|allow|recogni/.test(message)) reason = 'outbound-ip-not-authorized';
        else if (message.includes('not verified')) reason = 'brevo-not-verified-check-ip-security-or-account';
        else reason = 'authentication-rejected';
      } else if (response.status === 400) {
        if (/smtp|transactional|account/.test(message) && /not.*activat|activat.*account|not.*enabl/.test(message)) reason = 'transactional-account-not-activated';
        else if (/suspend|blocked account|account.*block/.test(message)) reason = 'brevo-account-suspended';
        else if (/sender|from email|from address/.test(message)) reason = 'sender-invalid-or-not-verified';
        else if (/credit|quota|balance/.test(message)) reason = 'sending-quota-unavailable';
        else if (/idempotenc|duplicate/.test(message)) reason = 'request-idempotency-rejected';
        else if (/recipient|to email|to address/.test(message)) reason = 'recipient-rejected';
        else if (/htmlcontent|textcontent|subject/.test(message)) reason = 'email-content-rejected';
        else if (providerCode === 'permission_denied') reason = 'brevo-account-or-permission-not-enabled';
        else reason = 'invalid-request-check-provider-code';
      } else if (response.status === 403) reason = 'permission-or-account-rejected';
      else if (response.status === 429) reason = 'provider-rate-limit';
    } catch { /* A non-JSON response must not expose raw provider output. */ }
    throw new Error(`Guide email provider returned HTTP ${response.status}; reason=${reason}; provider-code=${providerCode}; diagnostics=v3`);
  }
}

export default {
  async formSubmitted(event) {
    await deliverGuide(event.data);
  }
};
