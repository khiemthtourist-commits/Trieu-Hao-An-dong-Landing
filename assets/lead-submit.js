window.LEAD_GUIDES = {
  "/tour-trung-quoc.html": "Tour Trung Quốc",
  "/tour-thuong-hai-o-tran-hang-chau.html": "Thượng Hải – Ô Trấn – Hàng Châu",
  "/tour-truong-gia-gioi-phuong-hoang-co-tran.html": "Trương Gia Giới – Phượng Hoàng Cổ Trấn",
  "/tour-thanh-do-cuu-trai-cau.html": "Thành Đô – Cửu Trại Câu",
  "/tour-le-giang-shangrila.html": "Tour Lệ Giang – Shangrila từ TP.HCM: chọn hành trình nào?",
  "/tour-bac-kinh-thuong-hai.html": "Tour Bắc Kinh – Thượng Hải: phù hợp với ai?",
  "/tour-trung-quoc-shopping-no-shopping.html": "Tour Trung Quốc shopping và no-shopping khác nhau thế nào?",
  "/tour-cap-nhi-tan-lang-tuyet-huong.html": "Tour Cáp Nhĩ Tân – Làng Tuyết Hương: chuẩn bị gì?",
  "/tour-trung-quoc-thang-12.html": "Đi Trung Quốc tháng 12: chọn tuyến theo sở thích",
  "/tour-thuong-hai-disneyland.html": "Tour Thượng Hải có Disneyland: kiểm tra gì trước khi đặt?",
  "/le-giang-shangrila-hay-cuu-trai-cau.html": "Lệ Giang – Shangrila hay Cửu Trại Câu: nên chọn tuyến nào?",
  "/tour-trung-quoc-gia-dinh-tre-nho.html": "Tour Trung Quốc cho gia đình có trẻ nhỏ: cách chọn",
  "/gia-tour-trung-quoc-bao-gom-gi.html": "Giá tour Trung Quốc gồm những gì, có thể phát sinh khoản nào?",
  "/tour-trung-quoc-tet-2027.html": "Tour Trung Quốc Tết 2027: cách chọn lịch và dịch vụ",
  "/ho-so-di-tour-trung-quoc.html": "Hồ sơ đi tour Trung Quốc: cần chuẩn bị gì?",
  "/tour-trung-quoc-nguoi-lon-tuoi.html": "Tour Trung Quốc cho người lớn tuổi: đọc lịch trình thế nào?"
};

/* Gửi form tư vấn về Google Sheet + email, dùng chung cho mọi trang trên trieuhaoandong.com */
window.LEAD_WEBAPP_URL = 'https://script.google.com/macros/s/AKfycbzpH1aIHbZQvGl3S67JM7O3k5vo6CGUkuAr8bBNFY6IZdjdoY2jGnNsTFT5imyy5R4f/exec';

window.submitLead = function (payload) {
  // Only a known public article path is accepted; never copy arbitrary query text.
  var guides = window.LEAD_GUIDES;
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
