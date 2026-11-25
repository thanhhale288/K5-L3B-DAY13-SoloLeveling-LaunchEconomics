# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Một trang. Cột trạng thái chỉ nhận: **Xong, có bằng chứng · Chưa · Giả lập**. Mục nào dựa trên cột `_simulated` ghi Giả lập. Người phụ trách là một vai trò, không ghi "cả đội". Gate 2a chỉ duyệt kế hoạch pilot: không viết như thể trợ lý đã được duyệt chạy chính thức (xem quy tắc 5 trong `README.md`).

Nhóm: SoloLeveling (một thành viên) · Lớp: L3B

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | 4.472 đ toàn mẫu; 3.414 đ phạm vi noi_dia + hang_nang, cộng cố định 4.599 đ ở 45.000 yêu cầu/tháng (simulated) | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | Số ca làm lại +51,8% (6.787 đ) · tỉ lệ xem lại +40,7% (6.292 đ) · lương nhân viên +23,1% (5.506 đ); xem lại 100% = 1,03× (12.415 đ) nên không tiết kiệm (simulated) | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | 4.599 đ = 0,38× của 12.000 đ trong phạm vi (5.784 đ = 0,48× nếu còn một nửa khối lượng); quoc_te 1,88× và doi_tac 0,85× bị loại (simulated) | Giả lập | PM trợ lý hoàn phí |
| 4 · Chỉ số chính, chỉ số dùng, chỉ số an toàn | Trong đợt chạy thử (chưa có đối chứng): chính 82,83% (994/1.200) · bỏ qua gợi ý 27,12% (48/177) · lỗi lọt đến khách 4,25% (51/1.200) | Xong, có bằng chứng | Trưởng nhóm CSKH |
| 5 · Bảng lỗi và cách khắc phục | 20 ca gắn nhãn, đồng thuận 20/20; bảng khắc phục 5 ca (6, 7, 8, 10, 11) có ngưỡng đo được: ca 7 ngưỡng 0 ca báo "đã hoàn" khi sổ cái lỗi, ca 8 ngưỡng 1% trích dẫn không tồn tại | Xong, có bằng chứng | Kỹ sư trưởng agent |
| 6 · Pilot plan | Chia theo nhân viên 20 + 20, 859 yêu cầu mỗi nhóm, hệ số thiết kế 6,96, mức chênh phát hiện 6 điểm (power 0,64 nếu tác động thật chỉ 5 điểm); 3 luật dừng; phạm vi noi_dia + hang_nang | Xong, có bằng chứng | Giám đốc vận hành LogiX-VN |
| 7 · Rủi ro kinh tế | Làm lại gấp đôi +51,8% (6.787 đ); xem lại 100% = 0,98x đến 1,03x (11.743 đến 12.415 đ); khối lượng giảm một nửa cộng thêm 2.370 đ/việc (simulated) | Giả lập | PM trợ lý hoàn phí |

**Đề xuất: Go có điều kiện**, chỉ cho pilot phạm vi noi_dia + hang_nang (không phải mọi yêu cầu).

Lý do bằng số (simulated): trong phạm vi, chi phí mỗi việc thành công 3.414 đ, cộng cố định 4.599 đ = 0,38x của 12.000 đ; cả hệ thống 0,49x. quoc_te (1,88x, thành công 27,3%) và doi_tac (0,85x) bị loại.

Con số bất lợi và cách xử lý:
- Xem lại 100% chỉ còn 0,98x đến 1,03x của 12.000 đ, tức không tiết kiệm; pilot phải học được mức xem lại giảm an toàn xuống bao nhiêu, mỗi lần xem lại phải dưới 5,1 phút (4,8 phút nếu làm lại 15,3 phút).
- Pilot chỉ đủ mẫu cho mức chênh 6 điểm; nếu tác động thật là 5 điểm thì power còn 0,64.
- Tỉ lệ mở lại hiện tại 4,25% (51/1.200), nên ngưỡng an toàn so với nhóm đối chứng cộng trần 6%, không đặt 3%.
- Ca 7 và ca 20 cho thấy lỗi báo "đã hoàn" khi sổ cái lỗi và hoàn trùng; phải sửa trước khi chạy.
- Số tiền xem lại và làm lại là phút simulated, cần thay bằng phút đo thật sau tuần 1.

Điều kiện (người phụ trách, ngày kiểm tra; ngày là suy luận cho pilot bắt đầu 2026-12-14):
1. Sửa khoá chống trùng và đối soát sổ cái (ca 7, 20): Kỹ sư trưởng agent, 2026-12-07.
2. Chấp nhận mức chênh 6 điểm (power 0,64 ở mức 5 điểm): Giám đốc vận hành LogiX-VN ký, 2026-12-07.
3. Bật đủ event có `trace_id`; thay phút simulated bằng phút đo thật sau tuần 1: PM trợ lý hoàn phí, 2026-12-21.
4. Kế hoạch giảm xem lại theo bậc (xem lại 100% không tiết kiệm): Trưởng nhóm CSKH, 2026-12-21.
