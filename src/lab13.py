"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Điền các chỗ ghi VIẾT Ở ĐÂY (đánh dấu TODO CP1…CP4). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
# TODO CP1: viết ba hàm dưới đây cho tới khi kiem_tra_dap_an_biet_truoc() in ĐẠT.
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    return 1 / p if k is None else (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    return 1.0 if k is None else 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
# TODO CP1: viết mo_hinh; CP2 gọi lại hàm này với tham số giá và hệ số đã đổi.
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    reqs = reqs.copy()
    runs = runs[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:  # dùng cho B1, B3
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0
    # Tử số: MỌI lần chạy, kể cả lần lỗi
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai  # simulated
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai  # simulated
    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai
    # Mẫu số: chỉ việc thành công
    thanh_cong = (reqs['ket_qua'] == 'thanh_cong').sum()
    return dict(token=tien_token.sum(), tool=tien_tool.sum(),
                chay_lai=(tien_token + tien_tool)[runs['attempt'] > 1].sum(),
                xem_lai=xem_lai, lam_lai=lam_lai, tong=tong,
                thanh_cong=thanh_cong, cps=tong / thanh_cong,
                hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs))


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    ket_qua = mo_hinh(runs, reqs)
    print('--- A2 (xem_lai, lam_lai, tong, cps: simulated) ---')
    for ten, gia_tri in ket_qua.items():
        print(f'{ten:15s} {gia_tri:>14,.1f}')
    print(f"cps / hoa_don_moi_yc = {ket_qua['cps'] / ket_qua['hoa_don_moi_yc']:.1f} lần")
    for khoan in ('token', 'tool', 'xem_lai', 'lam_lai'):
        print(f"ti trong {khoan:8s} {ket_qua[khoan] / ket_qua['tong']:.1%}")
    # ---------- A3 · Tách theo loại yêu cầu (cps: simulated) ----------
    print('\n--- A3 (cps: simulated) ---')
    print(f"{'loai':10s} {'so_yc':>6s} {'ti_le_tc':>9s} {'lan_chay/yc':>11s} {'cps':>9s} {'so_voi_12k':>10s}")
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        r = reqs[reqs['loai'] == loai]
        kq = mo_hinh(runs, r)
        so_lan = runs[runs['request_id'].isin(r['request_id'])].shape[0] / len(r)
        print(f"{loai:10s} {len(r):6d} {kq['thanh_cong'] / len(r):9.1%} {so_lan:11.2f} {kq['cps']:9,.0f} {kq['cps'] / BASELINE:9.2f}x")
    # Tỉ lệ ok theo từng lần thử × loại: chạy lại có giúp không?
    m = runs.merge(reqs[['request_id', 'loai']], on='request_id')
    m['ok'] = (m['status'] == 'ok').astype(int)
    print('\nTi le ok theo attempt:')
    print(m.pivot_table(index='loai', columns='attempt', values='ok', aggfunc='mean').round(3))

    # ---------- A4 · Chi phí cố định, phạm vi noi_dia + hang_nang (simulated) ----------
    print('\n--- A4 (simulated) ---')
    pv = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    kq_pv = mo_hinh(runs, pv)
    ti_le_pv = kq_pv['thanh_cong'] / len(reqs)  # số việc thành công của phạm vi / 1.200 yêu cầu mẫu
    for ten, yc_thang in [('45.000 yeu cau/thang', 45000), ('Mot nua khoi luong', 22500)]:
        tc_thang = yc_thang * ti_le_pv
        cd = 40_000_000 / tc_thang
        tong = kq_pv['cps'] + cd
        print(f'{ten:22s} tc/thang={tc_thang:9,.0f}  co dinh/viec={cd:7,.0f}  cps+cd={tong:7,.0f}  = {tong / BASELINE:.2f}x')
    print(f"cps trong pham vi (chua co dinh) = {kq_pv['cps']:,.0f}")
    # ---------- B1 · Đổi từng yếu tố (cps: simulated) ----------
    print('\n--- B1 (simulated) ---')
    kich_ban = {
        'Giá token gấp đôi':        dict(gia_vao=52, gia_ra=260),
        'Giá token giảm một nửa':   dict(gia_vao=13, gia_ra=65),
        'Xem lại gấp đôi':          dict(he_so_xem_lai=2),
        'Xem lại giảm một nửa':     dict(he_so_xem_lai=0.5),
        'Làm lại gấp đôi':          dict(he_so_lam_lai=2),
        'Làm lại giảm một nửa':     dict(he_so_lam_lai=0.5),
        'Lương tăng 25%':           dict(luong_phut=2500),
        'Tối đa 2 lần chạy':        dict(max_lan_chay=2),
        'Chỉ 1 lần chạy':           dict(max_lan_chay=1),
    }
    goc = mo_hinh(runs, reqs)['cps']
    print(f"{'Gốc':26s} {goc:8,.0f}")
    for ten, kw in kich_ban.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']
        print(f'{ten:26s} {cps:8,.0f} {(cps / goc - 1) * 100:+6.1f}%')

    # ---------- B2 · Một cặp: token gấp đôi + xem lại gấp đôi ----------
    cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)['cps']
    print(f'\nB2 token x2 + xem lai x2: {cap:,.0f} ({(cap / goc - 1) * 100:+.1f}%)')

    # ---------- B3 · Giới hạn chạy lại: chi phí cả hệ thống ----------
    print('\n--- B3 (simulated) ---')
    for k in (1, 2, 3):
        kq = mo_hinh(runs, reqs, max_lan_chay=k)
        khong_tc = len(reqs) - kq['thanh_cong']
        he_thong = kq['tong'] + BASELINE * khong_tc
        print(f"k={k}: tong_tro_ly={kq['tong']:>11,.0f}  khong_thanh_cong={khong_tc:4d}  ca_he_thong={he_thong:>11,.0f}  cps={kq['cps']:6,.0f}")

    # ---------- B4 · Xem lại 100% (noi_dia + hang_nang) ----------
    print('\n--- B4 (simulated) ---')
    pv = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    runs_pv = runs[runs['request_id'].isin(pv['request_id'])]
    token_tool = ((runs_pv['tokens_in'] / 1000 * GIA_VAO + runs_pv['tokens_out'] / 1000 * GIA_RA).sum()
                  + (runs_pv['tool_calls'] * GIA_TOOL).sum())
    co_ok = runs_pv[runs_pv['status'] == 'ok']['request_id'].nunique()
    n_lam_lai = (pv['ket_qua'] == 'lam_lai').sum()
    tc_pv = (pv['ket_qua'] == 'thanh_cong').sum()
    tb_toan_bo = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated'].mean()  # 15,3 phút trên 74 ca
    for phut_lam_lai in (9, tb_toan_bo, pv.loc[pv['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated'].mean()):
        tong = token_tool + co_ok * 5 * LUONG_PHUT + n_lam_lai * phut_lam_lai * LUONG_PHUT
        hoa_von = (BASELINE * tc_pv - token_tool - n_lam_lai * phut_lam_lai * LUONG_PHUT) / (co_ok * LUONG_PHUT)
        print(f'lam lai {phut_lam_lai:5.1f} phut/ca: yc_xem_lai={co_ok} lam_lai={n_lam_lai} token+tool={token_tool:,.0f} '
              f'tong={tong:,.0f} cps={tong / tc_pv:,.0f} = {tong / tc_pv / BASELINE:.2f}x  hoa_von_xem_lai<={hoa_von:.1f} phut')
    # ---------- D1 · Cỡ mẫu (baseline 0,70; +5 điểm; alpha 0,05; power 0,8; ICC 0,02) ----------
    from statistics import NormalDist
    from statsmodels.stats.proportion import proportion_effectsize
    from statsmodels.stats.power import NormalIndPower

    def co_mau(p1, p2, alpha=0.05, power=0.8):
        za, zb = NormalDist().inv_cdf(1 - alpha / 2), NormalDist().inv_cdf(power)
        pb = (p1 + p2) / 2
        return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                          + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)

    ICC = 0.02
    print('\n--- D1 ---')
    n_a = co_mau(0.70, 0.75)
    print(f'a) chia theo yeu cau: {n_a} yeu cau moi nhom')
    m = 75
    de_b = 1 + (m - 1) * ICC
    n_b = math.ceil(n_a * de_b)
    print(f'b) m={m}: DE={de_b:.2f}, n={n_b} moi nhom -> {math.ceil(n_b / m)} nhan vien moi nhom, tong {2 * math.ceil(n_b / m)} (co 40)')
    print(f'c) 20 nhan vien moi nhom: hieu dung toi da < {20 / ICC:.0f} (can {n_a}) -> {"dat" if 20 / ICC >= n_a else "KHONG dat"}')
    print(f'd) 6 depot moi nhom: hieu dung toi da < {6 / ICC:.0f}')
    n6 = co_mau(0.70, 0.76)
    m_e = math.ceil(n6 * (1 - ICC) / (20 - n6 * ICC))
    print(f'e) chenh 6 diem: {n6} moi nhom; 20 nguoi/nhom -> m >= {m_e} yeu cau moi nguoi (DE={1 + (m_e - 1) * ICC:.2f})')
    es = proportion_effectsize(0.75, 0.70)
    print(f'power neu tac dong that chi 5 diem, n=859/nhom: {NormalIndPower().solve_power(es, nobs1=859, alpha=0.05, ratio=1):.2f}')
    print(f'power neu tac dong 6 diem, n=859/nhom: {NormalIndPower().solve_power(proportion_effectsize(0.76, 0.70), nobs1=859, alpha=0.05, ratio=1):.2f}')

    # ---------- D3 · Tỉ lệ mở lại hiện tại (trước khi đặt ngưỡng an toàn) ----------
    pv = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    print(f"\nmo_lai_trong_7_ngay: toan mau {reqs['mo_lai_trong_7_ngay'].mean():.2%} ({reqs['mo_lai_trong_7_ngay'].sum()}/{len(reqs)}), "
          f"pham vi noi_dia+hang_nang {pv['mo_lai_trong_7_ngay'].mean():.2%} ({pv['mo_lai_trong_7_ngay'].sum()}/{len(pv)})")
    print(f"ti le lam_lai trong pham vi: {(pv['ket_qua'] == 'lam_lai').mean():.2%}; nhan vien={reqs['staff_id'].nunique()}, depot={reqs['depot'].nunique()}")
