/* Gửi form tư vấn về Google Sheet + email, dùng chung cho mọi trang trên trieuhaoandong.com */
window.LEAD_WEBAPP_URL = 'https://script.google.com/macros/s/AKfycbzpH1aIHbZQvGl3S67JM7O3k5vo6CGUkuAr8bBNFY6IZdjdoY2jGnNsTFT5imyy5R4f/exec';

window.submitLead = function (payload) {
  // Only a known public article path is accepted; never copy arbitrary query text.
  var guides = {
    '/tour-trung-quoc.html': 'Tour Trung Quốc',
    '/tour-thuong-hai-o-tran-hang-chau.html': 'Thượng Hải – Ô Trấn – Hàng Châu',
    '/tour-truong-gia-gioi-phuong-hoang-co-tran.html': 'Trương Gia Giới – Phượng Hoàng Cổ Trấn',
    '/tour-thanh-do-cuu-trai-cau.html': 'Thành Đô – Cửu Trại Câu'
  };
  var from = new URLSearchParams(window.location.search).get('from');
  if (!guides[from] && document.referrer) {
    try {
      var ref = new URL(document.referrer);
      if (ref.origin === window.location.origin) from = ref.pathname;
    } catch (e) { /* Invalid referrer is ignored. */ }
  }
  payload = Object.assign({}, payload);
  if (Object.prototype.hasOwnProperty.call(guides, from)) {
    payload.ghiChu = (payload.ghiChu ? payload.ghiChu + '\n' : '') +
      'Bài viết khách đã đọc: ' + guides[from] + ' (' + from + ')';
  }
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
