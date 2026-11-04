// Native POST remains available without JavaScript; JS adds inline feedback.
document.querySelectorAll('form[data-contact-form]').forEach(form => {
  let sending = false;
  const consent = form.querySelector('[name="privacy-consent"]');
  const submitButton = form.querySelector('button[type="submit"]');
  const updateAvailability = () => { submitButton.disabled = sending || !consent?.checked; };
  consent?.addEventListener('change', updateAvailability);
  form.addEventListener('reset', () => queueMicrotask(updateAvailability));
  updateAvailability();
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (sending || !form.reportValidity()) return;
    const button = form.querySelector('button[type="submit"]');
    const status = form.querySelector('[role="status"]');
    const originalLabel = button.textContent;
    const data = new FormData(form);
    sending = true;
    button.disabled = true;
    button.textContent = 'Küldés folyamatban…';
    form.setAttribute('aria-busy', 'true');
    status.textContent = 'Az üzenet küldése folyamatban…';
    status.dataset.state = 'pending';
    try {
      const response = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(data).toString()
      });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      form.reset();
      status.textContent = 'Köszönöm, az üzeneted megérkezett! Az időpontot külön egyeztetjük, a küldés még nem jelent foglalást.';
      status.dataset.state = 'success';
    } catch {
      status.textContent = 'Az üzenetet nem sikerült elküldeni. Ellenőrizd az internetkapcsolatot, és próbáld újra. A beírt adataid megmaradtak.';
      status.dataset.state = 'error';
    } finally {
      sending = false;
      updateAvailability();
      button.textContent = originalLabel;
      form.removeAttribute('aria-busy');
    }
  });
});
