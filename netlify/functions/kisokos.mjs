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
  if (!env.BREVO_API_KEY) throw new Error('BREVO_API_KEY is not configured');
  const sender = 'szeviki1020@gmail.com';
  const link = 'https://elizaweboldal.netlify.app/letoltesek/arcapolasi-kisokos.pdf';
  const escape = value => value.replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  // Retries of the same browser request keep the same provider idempotency key.
  const requestId = String(data['request-id'] || '');
  if (!/^[a-f0-9-]{36}$/i.test(requestId)) throw new Error('Missing request identifier');
  const key = createHash('sha256').update(requestId + ':' + email).digest('hex');
  const response = await fetchEmail('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: {'api-key': env.BREVO_API_KEY, 'Content-Type': 'application/json', accept: 'application/json'},
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
    // Never log the key, recipient, form body or provider response containing PII.
    throw new Error(`Guide email provider returned HTTP ${response.status}`);
  }
}

export default {
  async formSubmitted(event) {
    await deliverGuide(event.data);
  }
};
