document.querySelectorAll('form[data-guide-form]').forEach(form => {
  const button = form.querySelector('button[type="submit"]');
  const consent = form.querySelector('[name="guide-consent"]');
  const status = form.querySelector('[role="status"]');
  const requestId = form.querySelector('[name="request-id"]');
  let sending = false;
  const update = () => { button.disabled = sending || !consent.checked; };
  requestId.value = crypto.randomUUID();
  consent.addEventListener('change', update);
  update();
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (sending || !form.reportValidity()) return;
    sending = true;
    update();
    form.setAttribute('aria-busy', 'true');
    status.textContent = 'A kérésed küldése folyamatban…';
    status.dataset.state = 'pending';
    try {
      const response = await fetch('/', {method: 'POST', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, body: new URLSearchParams(new FormData(form)).toString()});
      if (!response.ok) throw new Error('Request failed');
      form.reset();
      requestId.value = crypto.randomUUID();
      status.textContent = 'A kérésedet fogadtuk. A Kisokos linkjét külön e-mailben küldjük. Ha nem érkezik meg, nézd meg a Spam mappát, vagy írj a szeviki1020@gmail.com címre.';
      status.dataset.state = 'success';
    } catch {
      status.textContent = 'Nem sikerült elküldeni a kérésedet. A megadott adataid megmaradtak; kérlek, próbáld újra.';
      status.dataset.state = 'error';
    } finally {
      sending = false;
      form.removeAttribute('aria-busy');
      update();
    }
  });
});
