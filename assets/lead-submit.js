/* Gửi form tư vấn về Google Sheet + email, dùng chung cho mọi trang trên trieuhaoandong.com */
window.LEAD_WEBAPP_URL = 'https://script.google.com/macros/s/AKfycbzpH1aIHbZQvGl3S67JM7O3k5vo6CGUkuAr8bBNFY6IZdjdoY2jGnNsTFT5imyy5R4f/exec';

window.submitLead = function (payload) {
  return fetch(window.LEAD_WEBAPP_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify(payload)
  })
    .then(function (r) { return r.text(); })
    .then(function (t) {
      try { return JSON.parse(t); } catch (e) { return { ok: false, raw: t }; }
    })
    .catch(function (err) { return { ok: false, error: String(err) }; });
};
