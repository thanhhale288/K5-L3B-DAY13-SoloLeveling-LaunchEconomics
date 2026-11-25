# Báo cáo nhóm

Báo cáo ngắn, tối đa 2 trang. Số liệu chi tiết nằm trong các file hồ sơ; ở đây chỉ dẫn lại con số chính.

## 1. Thông tin nhóm

- Tên nhóm: SoloLeveling (một thành viên)
- Lớp: L3B
- Thành viên: xem `TEAM.md`

## 2. Mục tiêu và cách tiếp cận

Trả lời bốn câu: có đáng chạy không, nhân viên có dùng không, khi hỏng thì sao, pilot thiết kế thế nào. Cách tiếp cận: tính chi phí từ trace bằng `src/lab13.py`, thử độ nhạy, gắn nhãn lỗi, rồi thiết kế pilot có đối chứng. Bài làm bởi một người (Lê Thanh Hà) thay vì nhóm 4 người.

## 3. Giải pháp

Tóm tắt cách nhóm làm từng nhiệm vụ A–E và link tới file hồ sơ tương ứng.

- A (chi phí): `mo_hinh` tính tử số trên mọi lần chạy, mẫu số trên việc thành công; tách theo loại và cộng chi phí cố định. Xem `bang_chi_phi.md`.
- B (độ nhạy): 9 kịch bản, một cặp, giới hạn 1/2/3 lần chạy, xem lại 100%. Xem `bang_chi_phi.md`.
- C (lỗi): gắn nhãn 20 ca, hai bộ nhãn độc lập, bảng khắc phục 5 ca. Xem `bang_loi.md`.
- D (pilot): cỡ mẫu theo ba cách chia, chọn chia theo nhân viên 20 + 20. Xem `pilot_plan.yaml`.
- E (chỉ số, hồ sơ): ba chỉ số, 11 event có `trace_id`, rủi ro kinh tế, hồ sơ 7 mục. Xem `chi_so.md`, `ho_so_launch_v0.md`.

## 4. Kết quả

Con số chính (ghi nhãn `simulated` khi cần) và đề xuất cuối của `ho_so_launch_v0.md`. Kết quả duyệt chéo nhóm nhận được từ hội đồng.

- Chi phí mỗi việc thành công 4.472 đ, gấp 16,3 lần hoá đơn token chia số yêu cầu (simulated). Trong phạm vi noi_dia + hang_nang, cộng cố định 4.599 đ = 0,38× của 12.000 đ (simulated).
- Ba yếu tố nhạy nhất: số ca làm lại (+51,8%), tỉ lệ xem lại (+40,7%), lương nhân viên (+23,1%) (simulated).
- Nhãn lỗi đồng thuận 20/20. Pilot: 20 + 20 nhân viên, 859 yêu cầu mỗi nhóm, mức chênh 6 điểm (power 0,64 nếu thật là 5 điểm).
- Đề xuất: **Go có điều kiện** cho phạm vi noi_dia + hang_nang.
- Kết quả duyệt chéo: chưa có tại thời điểm viết (chưa được xếp cặp chấm chéo); sẽ cập nhật sau khi có phiếu.

## 5. Khó khăn và cách xử lý

- Làm một mình trong khi đề viết cho nhóm 4 người: tự đảm nhận cả 4 vai, tuần tự.
- Nhiệm vụ C cần hai người gắn nhãn độc lập: bộ 1 do Lê Thanh Hà, bộ 2 do bạn cùng lớp Lã Quốc Nghị (nhóm khác) gắn riêng; hai subagent AI (theo lời học viên đã được giảng viên cho phép) gắn thêm để đối chiếu. Cả bốn bộ trùng 20/20 theo lời khai; nhóm chưa kiểm chứng được mức độc lập ngoài lời khai.
- Duyệt chéo Gate 2a: một nhóm một người, phụ thuộc coach xếp cặp; xem mục 4.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md`.

## 7. Hạn chế và hướng cải thiện

- Toàn bộ dữ liệu giả lập; phút xem lại và làm lại là simulated, cần thay bằng phút đo thật sau tuần 1 của pilot.
- Pilot chỉ đủ mẫu cho mức chênh 6 điểm.
- Ngưỡng luật dừng (8.000 đ, 40%, 6%) do nhóm đặt, chưa có căn cứ thống kê riêng.

## 8. Tài liệu tham khảo

- Erol và cộng sự, Cost-of-Pass: An Economic Framework for Evaluating Language Models, arxiv.org/abs/2504.13359
- Google PAIR, People + AI Guidebook, chương Errors + Graceful Failure
- Tài liệu statsmodels, lớp NormalIndPower
- `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md` để đối chiếu số
