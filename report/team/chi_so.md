# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu | Chỉ số trong đợt chạy thử là **82,83%** (994/1.200) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại | **27,12%** (48/177) |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu | **4,25%** (51/1.200) |
| Dùng | Nhóm tự đề xuất: % yêu cầu của nhóm can thiệp được mở bằng trợ lý | số `agent_suggestion_shown` chia số `refund_request_created` có `arm` = trợ lý, theo tuần | Không cần tính |
| An toàn | Nhóm tự đề xuất: % đơn hoàn sai tiền qua kiểm tra mẫu hằng tuần (bắt lỗi ngầm) | số `audit_sample_checked` có `so_tien_da_hoan` khác `so_tien_dung`, chia số đơn được kiểm tra mỗi tuần | Không cần tính |

Chỉ số trong đợt chạy thử là 82,83%, 27,12% và 4,25%: đợt chạy thử không có nhóm đối chứng nên không viết "trợ lý đã nâng chỉ số". Ba số này tính từ cột `dong_trong_24h`, `mo_lai_trong_7_ngay`, `quyet_dinh_xem_lai`, không phải cột `_simulated`; do `src/lab13.py` in ra.

## Danh sách event

Mỗi event có `trace_id` để nối với trace của agent.

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | App khách | request_id, loai, so_tien, arm, trace_id | Khi khách gửi yêu cầu |
| `agent_run_completed` | Agent | attempt, tokens_in, tokens_out, tool_calls, status, trace_id | Sau mỗi lần chạy, kể cả lỗi |
| `agent_suggestion_shown` | Giao diện nhân viên | staff_id, so_tien_de_xuat, trace_id | Khi gợi ý hiện ra |
| `staff_review_decision` | Nhân viên | quyet_dinh (giu, sua, bo), phut_xem_lai đo thật, trace_id | Khi bấm gửi, sửa hoặc bỏ |
| `staff_rework_completed` | Nhân viên | phut_lam_lai, ly_do, trace_id | Khi làm lại xong |
| `refund_ledger_write` | Dịch vụ sổ cái | idempotency_key, so_tien, ket_qua, trace_id | Khi ghi sổ |
| `handoff_to_staff` | Agent | reason, tom_tat, trace_id | Khi chuyển nhân viên |
| `request_category_mismatch` | Agent | muc_khach_chon, muc_theo_noi_dung, trace_id | Khi nội dung mô tả lệch mục khách chọn |
| `ticket_closed` | Hệ thống ticket | closed_at, trace_id | Khi đóng yêu cầu |
| `ticket_reopened` | Khách | reopened_at, reason, trace_id | Khi khách mở lại |
| `audit_sample_checked` | Kế toán | so_tien_da_hoan, so_tien_dung, dieu_khoan_trich_dan_hop_le, trace_id | Hằng tuần, 100 đơn mẫu |

**Kiểm tra chéo:** với mỗi chỉ số, event dùng để tính.

- Chỉ số chính: `refund_request_created` (thời điểm gửi) và `ticket_closed` (đóng trong 24 giờ), trừ đi các yêu cầu có `ticket_reopened` trong 7 ngày.
- Tỉ lệ bỏ qua gợi ý: `staff_review_decision` (số quyết định sua hoặc bo, chia số được xem lại).
- Tỉ lệ lỗi lọt đến khách: `ticket_reopened` chia số `refund_request_created`.
- Chỉ số dùng tự đề xuất: `agent_suggestion_shown` chia `refund_request_created` có `arm` = trợ lý.
- Chỉ số an toàn tự đề xuất: `audit_sample_checked`.
- Các cách phát hiện trong `bang_loi.md` (ca 6, 7, 8, 10, 11) dùng `request_category_mismatch`, `refund_ledger_write`, `audit_sample_checked`, `ticket_reopened`, `handoff_to_staff`: đủ event để đo.
- Chi phí mỗi việc thành công (luật dừng thứ hai) cần `agent_run_completed` (token, tool), `staff_review_decision` và `staff_rework_completed` (giờ nhân viên đo thật), `ticket_closed`.

## E2 · Rủi ro kinh tế

Số lấy từ bảng độ nhạy (`bang_chi_phi.md`); mọi số tiền dưới đây là simulated.

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | +51,8%, chi phí mỗi việc thành công lên 6.787 đ (simulated) | Tỉ lệ làm lại theo tuần vượt 7% (đợt chạy thử: 4,9% trong phạm vi, 48/982) | Thu hẹp về noi_dia, rà 20 trace làm lại | PM trợ lý hoàn phí |
| Phải xem lại 100% kéo dài | 11.743 đ = 0,98x của 12.000 đ (12.415 đ = 1,03x nếu làm lại 15,3 phút/ca như dữ liệu), simulated | Tỉ lệ yêu cầu được xem lại còn trên 50% cuối bước rollout 0.25 (đợt chạy thử: 13,0% trong phạm vi) | Giảm xem lại theo bậc khi tỉ lệ sửa + bỏ dưới 15% | Trưởng nhóm CSKH |
| Khối lượng thấp hơn dự kiến | Chi phí cố định 40 triệu đ/tháng: +1.185 đ/việc ở 45.000 yêu cầu/tháng, +2.370 đ/việc nếu còn một nửa (simulated) | Số việc thành công theo tuần dưới 50% kế hoạch | Không mở rộng pilot, xem lại hợp đồng chi phí cố định | PM trợ lý hoàn phí |
