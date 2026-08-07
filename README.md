# Triều Hảo An Đông — Landing page

Trang landing page giới thiệu tour outbound và dịch vụ visa của **Triều Hảo An Đông**
(THTourist An Đông), chi nhánh của Công ty TNHH TMDV Du Lịch Triều Hảo.

- **Địa chỉ:** 93 Trần Hưng Đạo, Phường An Đông, Tp. Hồ Chí Minh
- **Hotline / Zalo:** 0939 114 311
- **Fanpage:** https://www.facebook.com/thtouristvn
- **TikTok:** https://www.tiktok.com/@trieuhaoandong

## Cấu trúc

Trang tĩnh, một file duy nhất — không cần build step.

- `index.html` — toàn bộ HTML + CSS + JS, logo nhúng sẵn dạng base64
- `assets/thtourist-logo.png` — logo bản rời để dùng lại

## Deploy

Vercel nhận diện đây là static site, không cần cấu hình gì thêm.
Thư mục gốc của repo chính là thư mục xuất bản.

## Việc còn phải làm

- [ ] Thay ảnh placeholder (Unsplash) bằng ảnh thật của công ty
- [ ] Cập nhật số liệu thật: số năm hoạt động, lượt khách/năm, tỉ lệ hồ sơ visa đạt
- [ ] Thay 3 đánh giá khách hàng mẫu bằng đánh giá thật
- [ ] Kiểm tra lại giá và lịch khởi hành của 12 tour
- [ ] Gắn backend cho form tư vấn (xem comment trong `<script>` ở cuối `index.html`)
- [ ] Bổ sung link kênh YouTube (hiện đang là handle tạm)
