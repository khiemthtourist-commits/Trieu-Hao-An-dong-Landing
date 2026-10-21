# Vận hành SEO và form tư vấn

- Workflow `seo-maintenance.yml` tạo sitemap khi có thay đổi HTML trên main. Chỉ đưa trang công khai vào sitemap, loại noindex và bản trùng canonical; không bịa ngày cập nhật. Một commit sitemap mới sẽ kích hoạt Vercel như các thay đổi website khác.
- Kiểm tra website lúc 08:30 Việt Nam mỗi ngày, hoặc chạy thủ công workflow. Khi lỗi, job thất bại trong GitHub Actions; email phụ thuộc cài đặt thông báo của tài khoản GitHub, không có cấu hình email riêng mới.
- Giám sát tải các URL sitemap, kiểm tra HTTP, noindex, H1, các trường form và cấu hình script gửi. Không thử ghi Google Sheet, gửi email hoặc tạo khách giả. PASS không chứng minh hệ thống nhận lead đầu cuối đang hoạt động, cũng không chứng minh Google đã lập chỉ mục.
- Khách từ các bài Trung Quốc bấm nút tư vấn sẽ được chọn sẵn thị trường Trung Quốc. Khi gửi form, tên và đường dẫn bài nguồn được thêm vào trường `ghiChu` hiện có để backend Google Sheet/email có thể giữ nguyên. Không lưu lịch sử duyệt, cookie theo dõi, query tự do hoặc thông tin cá nhân vào công cụ phân tích. Không suy ra từ khóa Google từ thông tin này.
- Chưa kết nối API Search Console/GA4, nên chưa có tự động báo cáo clicks/impressions/CTR, thứ hạng hay tỷ lệ chuyển đổi. Cần người sở hữu cấp quyền qua luồng chính thức; không đặt mật khẩu, token hoặc khóa riêng trong repo.
- Một lịch rà soát trong ứng dụng chạy hằng tuần, thứ Hai 09:00; chỉ báo khi có vấn đề hoặc phát hiện hữu ích. Đây là lịch trong ứng dụng, khác workflow chạy trên GitHub.
- Không dùng Indexing API cho bài du lịch, không ping sitemap endpoint đã ngừng hoạt động, không tự gửi yêu cầu lập chỉ mục hàng loạt.

Chạy kiểm tra: `python3 scripts/build_sitemap.py` và `python3 scripts/check_site.py` (chỉ đọc website công khai).
