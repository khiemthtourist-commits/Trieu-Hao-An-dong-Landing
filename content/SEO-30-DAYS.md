# Kế hoạch SEO 30 ngày — Triều Hảo An Đông

Thời gian: 22/10–20/11/2026, múi giờ Asia/Ho_Chi_Minh. Người dùng đã giao quyền tự viết và xuất bản 12 bài, chỉnh sửa SEO có thể đảo ngược, trong chat ngày 21/10/2026. Không cần hỏi lại từng lần xuất bản trong phạm vi này.

Nguồn lịch và trạng thái: `content/seo-plan-30-days.json`. Bốn bài Trung Quốc đã có không tính vào 12 bài mới. Trạng thái ban đầu là `pending`: chưa viết hay đăng trước ngày hẹn.

## Lịch xuất bản

| Ngày | Nội dung |
|---|---|
| 23/10 | Lệ Giang – Shangrila từ TP.HCM |
| 26/10 | Bắc Kinh – Thượng Hải |
| 28/10 | Tour shopping và no-shopping |
| 30/10 | Cáp Nhĩ Tân – Làng Tuyết Hương |
| 02/11 | Đi Trung Quốc tháng 12 |
| 04/11 | Thượng Hải có Disneyland |
| 06/11 | So sánh Lệ Giang – Shangrila và Cửu Trại Câu |
| 09/11 | Tour cho gia đình có trẻ nhỏ |
| 11/11 | Giá tour gồm gì, chi phí phát sinh |
| 13/11 | Tour Trung Quốc Tết 2027 |
| 16/11 | Hồ sơ đi tour Trung Quốc |
| 18/11 | Tour cho người lớn tuổi |

## Quy trình cho mỗi lượt chạy

1. Xác định ngày Việt Nam. Trước 22/10 không đăng bài. Từ 22/10 đến hết 20/11: kiểm tra trạng thái repo và remote, giữ thay đổi người dùng; không reset, force push hay commit tệp không thuộc công việc. Nếu bẩn mà không thể tách an toàn thì báo đúng trở ngại.
2. Đọc manifest và lịch sử bài. Chọn bài pending đến hạn sớm nhất, tối đa một bài mới mỗi lượt/ngày. Ưu tiên hoàn tất xác minh bài đang `awaiting_verification` trước khi đăng tiếp. Nếu máy bỏ lỡ lịch, bù lần lượt trong đợt, không đăng dồn hàng loạt hoặc ghi ngày xuất bản giả. Không vượt 12 bài.
3. Đối chiếu dữ liệu lịch tour mới và nguồn chính thức về điểm đến. Visa, quy định, lịch hoạt động và giá phải kiểm tra nguồn tại thời điểm viết; không suy ra giá/chương trình từ tour cùng tên. Nếu không đủ bằng chứng cho một chi tiết thì bỏ chi tiết ấy, không bịa. Nếu chủ đề không còn phù hợp, giữ lại slot và ghi lý do; chỉ thay đề tài bằng một chủ đề Trung Quốc khác có ý định tìm kiếm rõ, đủ nguồn và không trùng bài hiện có, ghi thay đổi trong manifest.
4. Viết bài tiếng Việt nguyên bản, giải quyết ý định tìm kiếm riêng của slot. Không kéo dài cho đủ từ; không nhân bản chung một đoạn lớn trên 12 trang. Dùng giọng chuyên nghiệp, ấm áp; không giả trải nghiệm, tác giả chuyên gia, khách hàng, đánh giá, giá rẻ nhất hay cam kết visa/thứ hạng. Không chép toàn bài từ hãng/tổng công ty. Giữ liên hệ An Đông 0939 114 311, 93 Trần Hưng Đạo, Phường An Đông, TP.HCM.
5. Dùng giao diện bài hiện có và `assets/articles.css`, H1 duy nhất, heading rõ, title/description riêng, canonical `https://www.trieuhaoandong.com/{slug}.html`, JSON-LD Article/BreadcrumbList trung thực; ngày xuất bản là ngày đăng thật. Ảnh phải đúng địa điểm và có quyền sử dụng, không có thì không bịa ảnh. Không đổi logo hay nén ảnh thành viên.
6. Nút nhận lịch/báo giá ở đầu và cuối bài → `index.html?from=/{slug}.html#lien-he`. Link lịch → `lich-khoi-hanh.html?diem-den=TRUNG+QU%E1%BB%90C`. Kiểm tra slug trong `window.LEAD_GUIDES` để ghi nguồn và chọn sẵn thị trường. Không gửi form thử, không thu thập thêm thông tin cá nhân, không triển khai tracking bên thứ ba mới khi chưa có cấu hình phù hợp.
7. Thêm card HTML server-rendered vào `cam-nang.html`, link từ hub `tour-trung-quoc.html` và 1–2 bài liên quan khi hợp ngữ cảnh. Không tạo link tới trang chưa xuất bản. Chạy `python3 scripts/build_sitemap.py`, `python3 scripts/check_seo.py`, `node --check assets/lead-submit.js`, kiểm tra JS inline khi sửa; kiểm tra mobile bằng trình duyệt nếu có. Không tự gửi Indexing API cho bài du lịch.
8. Cập nhật slot thành `awaiting_verification`, lưu published_at thực, URL và nguồn tham khảo, commit chỉ tệp nhiệm vụ, rebase an toàn khi cần rồi push main. Xác nhận URL public trả HTTP 200 với nội dung đúng, canonical, sitemap chứa URL, CTA và file liên quan tải được. Sau đó đổi `published`, lưu verified_at và commit manifest. Nếu triển khai chậm thì lần sau chỉ xác minh tiếp, không tạo bài trùng.
9. Làm milestone đến hạn chưa hoàn thành; lưu ngày, kết quả và bằng chứng vào manifest. Không tuyên bố đã kiểm tra nếu mới lên kế hoạch. Ưu tiên lỗi crawl, canonical, link sai, tốc độ và bố cục điện thoại; không redesign toàn bộ hoặc thay đổi hệ thống thu lead đang chạy. Với PDF lịch tour, chỉ dùng file chính xác của row/id/ngày, không ghép theo tên tuyến hoặc hãng gần giống.
10. Từ 21/11: không đăng thêm, rà soát cuối đợt, ghi kết quả và phần chưa xong; tự chuyển lịch này về PAUSED sau khi báo cáo. Không kéo dài tự động sang chiến dịch khác. Lịch theo dõi SEO/form hằng tuần hiện có tiếp tục độc lập.

## Báo cáo và giới hạn

- Chỉ báo khi có bài đăng đã xác minh (kèm URL), lỗi ảnh hưởng website/đăng bài, thay đổi đáng kể hoặc kết quả tổng kết. Không thông báo mỗi ngày rằng không có việc.
- Dùng kết nối Windsor.ai đã có để đọc Search Console qua skill; không bịa số liệu khi data trống hay hết quota. Theo dõi hiện có dùng báo cáo Google Sheet riêng tư; không đưa file/ID Sheet hoặc thông tin khách hàng vào repo/website công khai.
- Không suy ra nguồn Google hoặc tỷ lệ chuyển đổi từ bài nguồn, lượt nhấp hay số điện thoại. Phân biệt lượt lưu form, số không trùng và khách được xác minh.
- Đây là lịch thực thi trong ứng dụng có quyền truy cập repo trên máy; không phải dịch vụ AI xuất bản trên GitHub khi máy tắt. GitHub Actions vẫn tự cập nhật sitemap và kiểm tra website từ xa. Không hứa đúng giờ tuyệt đối hoặc thứ hạng trong 30 ngày.
