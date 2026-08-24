#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Đồng bộ lịch khởi hành từ hệ thống điều hành tour của Triều Hảo
(trieuhaotravel.vn) sang assets/schedule-data.js của trang
trieuhaoandong.com.

Chỉ lấy các trường thông tin công khai/an toàn cho khách hàng xem
(tên tour, mã lịch, ngày đi/về, hãng bay, số chỗ tổng, số chỗ còn,
giá, link PDF chương trình) — KHÔNG lấy dữ liệu nội bộ (tên nhân
viên phụ trách, số đã bán/giữ chỗ, hạn visa nội bộ...).

Chạy độc lập bằng `requests`, không cần trình duyệt.
"""
import datetime
import json
import os
import re
import sys
import unicodedata

import requests

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FILE = os.path.join(SITE_ROOT, "assets", "schedule-data.js")

BASE = "https://trieuhaotravel.vn"
PAGE_URL = BASE + "/DieuHanhTour/DatCho"
LIST_URL = BASE + "/DieuHanhTour/DatCho/Lists"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

REGION_BUCKET = {
    "CHÂU ÂU": "chau-au", "NƯỚC NGA (RUSSIA)": "chau-au", "ANH QUỐC": "chau-au", "THỔ NHĨ KỲ": "chau-au",
    "TRUNG QUỐC": "dong-bac-a", "HÀN QUỐC": "dong-bac-a", "ĐÀI LOAN": "dong-bac-a",
    "HONGKONG": "dong-bac-a", "HONGKONG - THAM QUYEN - QUANG CHAU": "dong-bac-a", "NHẬT BẢN": "dong-bac-a",
    "THÁI LAN": "dong-nam-a", "MALAYSIA - SINGAPORE": "dong-nam-a", "SINGAPORE": "dong-nam-a",
    "LÀO": "dong-nam-a", "BALI": "dong-nam-a",
    "MỸ": "my-canada", "CANADA": "my-canada",
    "ĐÀ NẴNG": "trong-nuoc", "MIỀN BẮC": "trong-nuoc", "PHÚ QUỐC": "trong-nuoc",
}

KNOWN_TOURS = {
    "eu-duc-ao-y-thuy-sy-phap": "duc ao y thuy sy phap",
    "nga-moscow-stpetersburg": "matxcova saint petersburg",
    "nga-stpetersburg-moscow": "st petersburg moscow",
    "eu-phap-thuysy-y-vatican": "phap thuy si y vatican",
    "canada-lien-tuyen": "vancouver montreal quebec ottawa toronto",
    "hongkong-tham-quyen": "hong kong tham quyen",
    "nhat-narita-nagoya-osaka": "narita tokyo yamanashi nagoya osaka",
    "thai-phuket": "phuket",
    "nhat-kansai-osaka-tokyo": "kansai osaka yamanashi tokyo narita",
    "nhat-narita-toyohashi-osaka": "narita tokyo toyohashi osaka",
    "trungquoc-hai-nam": "dao hai nam",
    "hanquoc-busan-seoul": "busan gyeongju ulsan seoul",
}


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d").replace("Đ", "D")
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).strip()


def match_slug(ten, malich):
    n = norm(ten)
    ml = (malich or "").upper()
    if ml.startswith("CH") and "VN11" in ml and "duc" in n:
        return "eu-duc-ao-y-thuy-sy-phap"
    if ml.startswith("NG") and "VN" in ml and "matxcova" in n:
        return "nga-moscow-stpetersburg"
    for slug, key in KNOWN_TOURS.items():
        words = key.split()
        if sum(1 for w in words if w in n) >= max(2, len(words) - 1):
            return slug
    return None


def parse_date_ddmmyyyy(d):
    try:
        dd, mm, yyyy = d.split("/")
        return "%s-%s-%s" % (yyyy, mm, dd)
    except Exception:
        return "9999-99-99"


def extract_row(raw):
    tour_show = raw.get("TourShow") or ""
    so_cho_html = raw.get("SoCho") or ""
    thoi_gian_html = raw.get("ThoiGian") or ""
    hang_bay_html = raw.get("HangBay") or ""
    con_lai_html = raw.get("ConLai") or ""

    m_region = re.search(r'data-rel="tooltip"[^>]*>\s*<b>([^<]+)</b></a>', tour_show)
    vung = m_region.group(1).strip() if m_region else ""

    m_ten = re.search(r'href="#/DieuHanhTour/DatCho/ChiTiet/\d+"[^>]*>\s*<b>([^<]+)</b></a>', tour_show)
    ten = m_ten.group(1).strip() if m_ten else ""

    m_dip = re.search(r'label label-danger">\[([^\]]*)\]</span>', tour_show)
    dip = m_dip.group(1).strip() if m_dip else ""

    m_thoiluong = re.search(r'fa-clock-o"[^>]*></i>\s*([^<]+)</p>', tour_show)
    thoi_luong = m_thoiluong.group(1).strip() if m_thoiluong else ""

    m_malich = re.search(r"Mã Lịch:\s*<b[^>]*>([^<]+)</b>", tour_show)
    ma_lich = m_malich.group(1).strip() if m_malich else ""

    m_pdf = re.search(r'href="([^"]+\.pdf)"', tour_show, re.IGNORECASE)
    pdf = m_pdf.group(1) if m_pdf else None

    m_socho = re.search(r"Số chỗ:\s*<b>(\d+)</b>", so_cho_html)
    so_cho = int(m_socho.group(1)) if m_socho else 0
    m_conCho = re.search(r"Còn:\s*<b>(\d+)</b>", so_cho_html)
    con_cho = int(m_conCho.group(1)) if m_conCho else 0

    m_ngaydi = re.search(r"Đi:\s*<b>([\d/]+)</b>", thoi_gian_html)
    ngay_di = m_ngaydi.group(1) if m_ngaydi else ""
    m_ngayve = re.search(r"Về:\s*<b>([\d/]+)</b>", thoi_gian_html)
    ngay_ve = m_ngayve.group(1) if m_ngayve else ""

    m_baydi = re.search(r"Đi:\s*<b>([^<]+)</b>", hang_bay_html)
    bay_di = m_baydi.group(1).strip() if m_baydi else ""
    m_bayve = re.search(r"Về:\s*<b>([^<]+)</b>", hang_bay_html)
    bay_ve = m_bayve.group(1).strip() if m_bayve else ""

    m_giagoc = re.search(r"line-through;\">([\d,]+)</span>", con_lai_html)
    gia_goc = m_giagoc.group(1) if m_giagoc else ""
    m_giasale = re.search(r"gia-tour-display[^>]*>.*?bold;\">([\d,]+)</span>", con_lai_html, re.S)
    gia_sale = m_giasale.group(1) if m_giasale else "Liên hệ"

    return {
        "id": raw.get("Id"),
        "ten": ten,
        "vung": vung,
        "dip": dip,
        "maLich": ma_lich,
        "thoiLuong": thoi_luong,
        "ngayDi": ngay_di,
        "ngayVe": ngay_ve,
        "bayDi": bay_di,
        "bayVe": bay_ve,
        "soCho": so_cho,
        "conCho": con_cho,
        "giaGoc": gia_goc,
        "giaSale": gia_sale,
        "pdf": pdf,
    }


def fetch_all_rows(session, date_from, date_to, page_size=100):
    ngay_param = "%s - %s" % (date_from, date_to)
    page_url = PAGE_URL + "?Ngay=" + requests.utils.quote(ngay_param) + "&NoiXuatPhatId=1&IsNgay=true"
    session.get(page_url, headers={"User-Agent": UA})

    all_rows = []
    start = 0
    total = None
    while total is None or start < total:
        data = {
            "sEcho": "1", "iColumns": "6", "sColumns": ",,,,,",
            "iDisplayStart": str(start), "iDisplayLength": str(page_size),
            "mDataProp_0": "TourShow", "mDataProp_1": "SoCho", "mDataProp_2": "ThoiGian",
            "mDataProp_3": "HangBay", "mDataProp_4": "ConLai", "mDataProp_5": "Tool",
            "sSearch": "", "bRegex": "false",
            "iSortCol_0": "0", "sSortDir_0": "asc", "iSortingCols": "0",
            "Ngay": ngay_param, "TourId": "", "DiaDiemId": "", "TheLoaiId": "",
            "MaLichTour": "", "NoiXuatPhatId": "1", "SoCho": "", "IsNgay": "true",
            "IsConCho": "false", "IsYeuThich": "false", "isInIFrame": "0", "Url": "",
        }
        for i in range(6):
            data["sSearch_%d" % i] = ""
            data["bRegex_%d" % i] = "false"
            data["bSearchable_%d" % i] = "true"
            data["bSortable_%d" % i] = "true"

        resp = session.post(LIST_URL, data=data, headers={
            "User-Agent": UA,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": page_url,
        }, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        rows = payload.get("aaData") or []
        if total is None:
            total = payload.get("iTotalDisplayRecords", 0)
            print("Tổng số lịch khởi hành trên hệ thống: %d" % total, file=sys.stderr)
        if not rows:
            break
        all_rows.extend(rows)
        start += page_size
    return all_rows


def build_schedule_data(raw_rows):
    out = []
    malich_pdf = {}
    for raw in raw_rows:
        r = extract_row(raw)
        if not r["ten"] or not r["maLich"]:
            continue
        if r["pdf"]:
            malich_pdf[r["maLich"]] = r["pdf"]

        bucket = REGION_BUCKET.get(r["vung"], "khac")
        slug = match_slug(r["ten"], r["maLich"])
        out.append({
            "id": r["id"], "ten": r["ten"], "vung": r["vung"], "bucket": bucket,
            "dip": r["dip"], "maLich": r["maLich"], "thoiLuong": r["thoiLuong"],
            "ngayDi": r["ngayDi"], "ngayVe": r["ngayVe"],
            "ngayDiSort": parse_date_ddmmyyyy(r["ngayDi"]),
            "bayDi": r["bayDi"], "bayVe": r["bayVe"],
            "soCho": r["soCho"], "conCho": r["conCho"],
            "giaGoc": r["giaGoc"], "giaSale": r["giaSale"] or "Liên hệ",
            "coGiaTot": bool(r["giaGoc"] and r["giaGoc"] != r["giaSale"]),
            "slug": slug,
        })

    for row in out:
        if row["slug"]:
            continue
        pdf = malich_pdf.get(row["maLich"])
        if pdf:
            row["pdfExternal"] = BASE + pdf

    out.sort(key=lambda x: x["ngayDiSort"])
    return out


def main():
    today = datetime.date.today()
    date_from = today.strftime("%d/%m/%Y")
    date_to = (today + datetime.timedelta(days=126)).strftime("%d/%m/%Y")

    session = requests.Session()
    raw_rows = fetch_all_rows(session, date_from, date_to)
    print("Đã lấy %d dòng thô" % len(raw_rows), file=sys.stderr)

    data = build_schedule_data(raw_rows)
    print("Đã xử lý %d lịch khởi hành hợp lệ" % len(data), file=sys.stderr)
    if len(data) < 50:
        print("Số lượng lịch quá ít so với dự kiến — có thể request bị lỗi. Dừng lại, không ghi đè file.",
              file=sys.stderr)
        sys.exit(1)

    js = "window.SCHEDULE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(js)
    print("Đã ghi %s (%d dòng)" % (OUT_FILE, len(data)), file=sys.stderr)


if __name__ == "__main__":
    main()
