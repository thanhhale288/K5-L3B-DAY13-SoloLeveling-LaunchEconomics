# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Hai bộ nhãn độc lập

Người gắn nhãn 1: Lê Thanh Hà · Người gắn nhãn 2: Lã Quốc Nghị (bạn cùng lớp, thuộc nhóm khác, gắn riêng một bộ nhãn độc lập cho bài này). Theo lời hai người, cả hai gắn riêng, không trao đổi, và chưa xem hay tham khảo nhãn của AI trước khi gắn. Đối chiếu thêm: hai subagent AI (context riêng, được giảng viên cho phép theo lời học viên) cũng gắn độc lập và trùng 20/20 với bộ nhãn dưới đây.

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Do người dùng | Có | Do người dùng |
| 2 | Hệ thống | Hệ thống | Có | Hệ thống |
| 3 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 4 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 5 | Ngầm | Ngầm | Có | Ngầm |
| 6 | Do người dùng | Do người dùng | Có | Do người dùng |
| 7 | Hệ thống | Hệ thống | Có | Hệ thống |
| 8 | Ngầm | Ngầm | Có | Ngầm |
| 9 | Do người dùng | Do người dùng | Có | Do người dùng |
| 10 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 11 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 12 | Ngầm | Ngầm | Có | Ngầm |
| 13 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 14 | Do người dùng | Do người dùng | Có | Do người dùng |
| 15 | Hệ thống | Hệ thống | Có | Hệ thống |
| 16 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 17 | Ngầm | Ngầm | Có | Ngầm |
| 18 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 19 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 20 | Hệ thống | Hệ thống | Có | Hệ thống |

**Tỉ lệ đồng thuận:** 20 / 20 = 100%

## Quy tắc phân biệt cho các ca không trùng

Mỗi ca không trùng một câu. Đồng thuận dưới 80% thì ghi định nghĩa đã viết lại.

- Không có ca nào không trùng nên không cần thêm quy tắc phân biệt. Hai bộ nhãn do hai người gắn riêng và trùng hoàn toàn; bộ đối chiếu của hai subagent AI cũng trùng, nên không cần viết lại định nghĩa. Nhóm chưa kiểm được mức độc lập ngoài lời khai của hai người gắn nhãn.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 6 | Do người dùng | Event `input_validation_failed` hoặc `request_category_mismatch` (mục khách chọn khác nội dung mô tả), cảnh báo khi vượt 3% số yêu cầu mỗi ngày | Khi mô tả lệch mục đã chọn, trợ lý hỏi lại "Bạn muốn hoàn phí giao trễ hay báo hàng hỏng?" và chuyển đúng luồng, thay vì từ chối ngay | PM trợ lý hoàn phí |
| 7 | Hệ thống | Đối soát mỗi giờ: tin nhắn "đã hoàn" mà không có bản ghi `refund_ledger_write` ok cùng `trace_id`; ngưỡng 0 ca | Chỉ báo "đã hoàn" khi sổ cái trả ok; sau 3 lần thử lỗi 503 thì báo "đang xử lý" và chuyển nhân viên qua `handoff_to_staff` | Kỹ sư trưởng agent |
| 10 | Ngữ cảnh | Tỉ lệ yêu cầu bị từ chối do bất khả kháng rồi mở lại trong 7 ngày (`ticket_reopened`), theo tuần; cảnh báo khi vượt 10% | Khi từ chối vì bất khả kháng, tin nhắn nêu rõ lý do (bão) và ứng dụng ẩn hoặc đổi dòng "cam kết giao 24 giờ" cho đơn bị ảnh hưởng | Trưởng nhóm CSKH |
| 11 | Giới hạn hệ thống | Event `handoff_to_staff` với `reason = dau_vao_khong_ho_tro` (âm thanh, ảnh), theo ngày; theo dõi khi vượt 2% số yêu cầu | Giữ cách trả lời rõ ràng "vui lòng nhập bằng chữ" kèm nút gọi nhân viên; nếu tỉ lệ vượt ngưỡng thì cân nhắc thêm bước chuyển giọng nói thành văn bản | PM trợ lý hoàn phí |
| 8 | Ngầm | Kiểm tra mẫu 100 câu trả lời mỗi tuần: đối chiếu mọi điều khoản được trích với bản chính sách hiện hành; ngưỡng 1% trích dẫn không tồn tại | Chỉ cho trợ lý trích điều khoản có trong danh sách điều khoản hợp lệ; ghi `policy_version` vào `trace_id` để truy ngược | Trưởng nhóm chính sách |
