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
  if (!/^[a-f0-9-]{36}$/i.test(requestId)) throw new Error('Missing request identifier');
  const key = createHash('sha256').update(requestId + ':' + email).digest('hex');
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
    try {
      const error = await response.json();
      const message = typeof error.message === 'string' ? error.message.toLowerCase() : '';
      if (response.status === 401) {
        if (message.includes('key not found') || message.includes('invalid api key')) reason = 'api-key-invalid-or-revoked';
        else if (message.includes('ip') && /authoriz|block|allow|recogni/.test(message)) reason = 'outbound-ip-not-authorized';
        else if (message.includes('not verified')) reason = 'brevo-not-verified-check-ip-security-or-account';
        else reason = 'authentication-rejected';
      } else if (response.status === 403) reason = 'permission-or-account-rejected';
      else if (response.status === 429) reason = 'provider-rate-limit';
    } catch { /* A non-JSON response must not expose raw provider output. */ }
    throw new Error(`Guide email provider returned HTTP ${response.status}; reason=${reason}; diagnostics=v2`);
  }
}

export default {
  async formSubmitted(event) {
    await deliverGuide(event.data);
  }
};
