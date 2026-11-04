import assert from 'node:assert/strict';
import { deliverGuide } from '../netlify/functions/kisokos.mjs';
const data = {'request-kind':'arcapolasi-kisokos-v1','guide-consent':'accepted','request-id':'a8f40afc-9d72-411a-a63a-bcb97065a441',name:'Teszt <Anna>',email:'teszt@example.com'};
let calls = [];
const options = {env:{BREVO_API_KEY:'test-only-not-a-real-key'},fetchEmail:async (url, init)=>{calls.push({url,init,body:JSON.parse(init.body)});return {ok:true}}};
await deliverGuide({'request-kind':'contact'}, options);
assert.equal(calls.length,0,'contact requests must not trigger a PDF email');
await assert.rejects(deliverGuide({...data,'guide-consent':''},options),/Invalid/);
await assert.rejects(deliverGuide({...data,email:'bad\r\naddress'},options),/Invalid/);
await assert.rejects(deliverGuide({...data,'bot-field':'spam'},options),/Invalid/);
await assert.rejects(deliverGuide({...data,'request-id':''},options),/identifier/);
await assert.rejects(deliverGuide(data,{...options,env:{}}),/not configured/);
assert.equal(calls.length,0);
await deliverGuide(data,options);
await deliverGuide(data,options);
assert.equal(calls.length,2);
assert.equal(calls[0].body.headers.idempotencyKey,calls[1].body.headers.idempotencyKey);
assert.deepEqual(calls[0].body.to,[{name:'Teszt <Anna>',email:'teszt@example.com'}]);
assert.equal(calls[0].body.sender.email,'szeviki1020@gmail.com');
assert.ok(calls[0].body.textContent.includes('/letoltesek/arcapolasi-kisokos.pdf'));
assert.ok(calls[0].body.htmlContent.includes('Teszt &lt;Anna&gt;'));
assert.equal(calls[0].body.listIds,undefined,'no marketing list subscription');
await assert.rejects(deliverGuide(data,{...options,fetchEmail:async()=>({ok:false,status:429})}),/HTTP 429/);
await assert.rejects(deliverGuide(data,{...options,fetchEmail:async()=>{throw new Error('network')}}),/network/);
for (const [message, reason] of [
  ['Key not found','api-key-invalid-or-revoked'],
  ['not verified','brevo-not-verified-check-ip-security-or-account'],
  ['IP not authorized 192.0.2.1','outbound-ip-not-authorized'],
  ['unexpected private detail teszt@example.com test-only-not-a-real-key','authentication-rejected']
]) {
  await assert.rejects(deliverGuide(data,{...options,fetchEmail:async()=>({ok:false,status:401,json:async()=>({message})})}), error => {
    assert.ok(error.message.includes('reason='+reason));
    assert.ok(!error.message.includes('teszt@example.com'));
    assert.ok(!error.message.includes('192.0.2.1'));
    assert.ok(!error.message.includes('test-only-not-a-real-key'));
    return true;
  });
}
await deliverGuide(data,{...options,env:{BREVO_API_KEY:'  test-only-not-a-real-key\n'}});
assert.equal(calls.at(-1).init.headers['api-key'],'test-only-not-a-real-key');
console.log('Kisokos: validation, consent, contact isolation, safe email, retries and provider failures passed. No real email sent.');

for (const [message, reason] of [
 ['Your SMTP account is not yet activated. Please contact support','transactional-account-not-activated'],
 ['Sender email is not valid','sender-invalid-or-not-verified'],
 ['Not enough credits','sending-quota-unavailable'],
 ['Invalid idempotency key','request-idempotency-rejected']
]) {
 await assert.rejects(deliverGuide(data,{...options,fetchEmail:async()=>({ok:false,status:400,json:async()=>({code:'permission_denied',message})})}), error=>error.message.includes('reason='+reason)&&error.message.includes('provider-code=permission_denied'));
}
