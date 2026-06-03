"""
matrix_viz.py — Modul Visualisasi Matriks Citra
================================================
Menampilkan representasi nilai piksel (pixel matrix) sebelum dan sesudah
proses pengolahan citra sebagai media pembelajaran.

PENTING:
- Modul ini HANYA menambahkan tampilan informatif.
- Tidak mengubah algoritma, fungsi, atau logika apa pun yang sudah ada.
- Semua fungsi di sini bersifat "display only" dan dapat dipanggil
  setelah proses utama selesai tanpa mempengaruhi hasilnya.
"""

import numpy as np
import streamlit as st
import pandas as pd

# ── Konstanta tampilan ─────────────────────────────────────────────────────────
MAX_DIM = 12          # Ukuran maksimum baris/kolom matriks yang ditampilkan
KERNEL_COLOR  = "#A97CF8"   # Warna highlight area kernel (ungu pastel)
KERNEL_BG     = "rgba(200,162,255,0.22)"
RESULT_COLOR  = "#FF8C69"   # Warna highlight hasil (peach)
RESULT_BG     = "rgba(255,186,155,0.22)"


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER: ambil potongan matriks untuk ditampilkan
# ══════════════════════════════════════════════════════════════════════════════

def _crop_matrix(arr: np.ndarray, max_dim: int = MAX_DIM) -> np.ndarray:
    """
    Potong matriks agar tidak terlalu besar di layar.
    Untuk citra RGB, ambil channel pertama (R) sebagai representasi.
    """
    if arr is None:
        return None

    # Normalise to 2-D
    if len(arr.shape) == 3:
        display = arr[:, :, 0]          # channel R sebagai representasi
    else:
        display = arr

    h, w = display.shape
    rows = min(h, max_dim)
    cols = min(w, max_dim)
    return display[:rows, :cols].astype(int)


def _caption_crop(arr: np.ndarray, max_dim: int = MAX_DIM) -> str:
    """Buat teks keterangan ukuran matriks yang dipotong."""
    if arr is None:
        return ""
    h = arr.shape[0] if len(arr.shape) >= 1 else 0
    w = arr.shape[1] if len(arr.shape) >= 2 else 0
    rows = min(h, max_dim)
    cols = min(w, max_dim)
    if h > max_dim or w > max_dim:
        return (f"⚠️ Ukuran asli **{h}×{w}** piksel — ditampilkan **{rows}×{cols}** "
                f"piksel pertama saja.")
    return f"Ukuran gambar: **{h}×{w}** piksel."


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER: render HTML table berwarna
# ══════════════════════════════════════════════════════════════════════════════

def _matrix_to_html(matrix: np.ndarray,
                    highlight_cells: set = None,
                    highlight_bg: str = KERNEL_BG,
                    highlight_color: str = KERNEL_COLOR,
                    font_size: str = "0.72rem") -> str:
    """
    Konversi array 2-D ke tabel HTML rapi dengan opsional highlight sel.

    Parameters
    ----------
    matrix        : np.ndarray 2-D
    highlight_cells : set of (row, col) yang diberi warna berbeda
    """
    if matrix is None:
        return "<p><em>Data tidak tersedia.</em></p>"

    highlight_cells = highlight_cells or set()

    rows_html = []
    for r, row in enumerate(matrix):
        cells = []
        for c, val in enumerate(row):
            if (r, c) in highlight_cells:
                bg    = highlight_bg
                color = highlight_color
                fw    = "700"
                border = f"1.5px solid {highlight_color}"
            else:
                bg    = "transparent"
                color = "#3B3650"
                fw    = "400"
                border = "1px solid #EEEAF7"
            cell = (
                f'<td style="'
                f'background:{bg};color:{color};font-weight:{fw};'
                f'border:{border};padding:4px 6px;'
                f'text-align:center;font-size:{font_size};'
                f'min-width:32px;border-radius:4px;">'
<<<<<<< HEAD
                f'{int(val) if val == int(val) else round(float(val), 4)}</td>'
=======
<<<<<<< HEAD
                f'{int(val) if val == int(val) else round(float(val), 4)}</td>'
=======
                f'{int(val)}</td>'
>>>>>>> 6a7b541bfb5a1ec24e238ac21acb4151762d2686
>>>>>>> ff1b6e8435dab4fa42c9203bd0444c83af2fcd00
            )
            cells.append(cell)
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    table = (
        '<div style="overflow-x:auto;margin:6px 0;">'
        '<table style="border-collapse:separate;border-spacing:2px;'
        'font-family:\'Poppins\',monospace;">'
        + "".join(rows_html)
        + '</table></div>'
    )
    return table


def _col_header_html(labels: list, color: str = "#7B7690",
                     font_size: str = "0.65rem") -> str:
    """Buat baris header kolom (0, 1, 2, …)."""
    cells = ['<td style="width:20px;"></td>']
    for lbl in labels:
        cells.append(
            f'<th style="text-align:center;font-size:{font_size};'
            f'color:{color};font-weight:600;padding:2px 6px;">{lbl}</th>'
        )
    return "<tr>" + "".join(cells) + "</tr>"


def _matrix_to_html_indexed(matrix: np.ndarray,
                             highlight_cells: set = None,
                             highlight_bg: str = KERNEL_BG,
                             highlight_color: str = KERNEL_COLOR) -> str:
    """
    Seperti _matrix_to_html tetapi dilengkapi nomor baris & kolom (indeks).
    """
    if matrix is None:
        return "<p><em>Data tidak tersedia.</em></p>"

    highlight_cells = highlight_cells or set()
    n_cols = matrix.shape[1]
    font_size = "0.68rem"

    col_labels = list(range(n_cols))
    header_row = _col_header_html(col_labels)

    rows_html = [header_row]
    for r, row in enumerate(matrix):
        row_num_cell = (
            f'<td style="text-align:right;font-size:0.6rem;'
            f'color:#ADA8C0;padding-right:4px;font-weight:600;">{r}</td>'
        )
        cells = [row_num_cell]
        for c, val in enumerate(row):
            if (r, c) in highlight_cells:
                bg    = highlight_bg
                color = highlight_color
                fw    = "700"
                border = f"1.5px solid {highlight_color}"
            else:
                bg    = "transparent"
                color = "#3B3650"
                fw    = "400"
                border = "1px solid #EEEAF7"
            cell = (
                f'<td style="'
                f'background:{bg};color:{color};font-weight:{fw};'
                f'border:{border};padding:4px 5px;'
                f'text-align:center;font-size:{font_size};'
                f'min-width:30px;border-radius:4px;">'
<<<<<<< HEAD
                f'{int(val) if val == int(val) else round(float(val), 4)}</td>'
=======
<<<<<<< HEAD
                f'{int(val) if val == int(val) else round(float(val), 4)}</td>'
=======
                f'{int(val)}</td>'
>>>>>>> 6a7b541bfb5a1ec24e238ac21acb4151762d2686
>>>>>>> ff1b6e8435dab4fa42c9203bd0444c83af2fcd00
            )
            cells.append(cell)
        rows_html.append("<tr>" + "".join(cells) + "</tr>")

    table = (
        '<div style="overflow-x:auto;margin:6px 0;">'
        '<table style="border-collapse:separate;border-spacing:2px;'
        'font-family:\'Poppins\',monospace;">'
        + "".join(rows_html)
        + '</table></div>'
    )
    return table


# ══════════════════════════════════════════════════════════════════════════════
#  KOMPONEN UI UTAMA
# ══════════════════════════════════════════════════════════════════════════════

def _section_divider(label: str):
    """Garis pembatas dengan label di tengah."""
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;margin:1.2rem 0 .8rem;">'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,'
        f'transparent,#EEEAF7);"></div>'
        f'<span style="font-size:0.65rem;font-weight:700;letter-spacing:1.6px;'
        f'text-transform:uppercase;color:#A97CF8;white-space:nowrap;">'
        f'🔢 {label}</span>'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,'
        f'#EEEAF7,transparent);"></div>'
        f'</div>',
        unsafe_allow_html=True
    )


def _info_note():
    """Catatan kaki yang selalu ditampilkan di bawah matriks."""
    st.markdown(
        '<p style="font-size:0.7rem;color:#ADA8C0;margin-top:4px;'
        'font-style:italic;">'
        '📌 Setiap sel mewakili satu piksel. Angka di dalamnya adalah '
        '<b>nilai intensitas piksel</b> (0 = hitam, 255 = putih/penuh).</p>',
        unsafe_allow_html=True
    )


def _matrix_card(title: str, html_table: str, caption: str = "",
                 accent: str = "#A97CF8"):
    """Wrapper kartu glassmorphism untuk satu matriks."""
    caption_html = (
        f'<p style="font-size:0.68rem;color:#ADA8C0;margin-top:4px;">{caption}</p>'
        if caption else ""
    )
    st.markdown(
        f'<div style="background:rgba(255,255,255,.80);backdrop-filter:blur(12px);'
        f'border-radius:16px;border:1px solid #EEEAF7;padding:1rem 1.2rem;'
        f'box-shadow:0 2px 12px rgba(163,124,248,.09);margin-bottom:.6rem;">'
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:.6rem;">'
        f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;'
        f'background:{accent};flex-shrink:0;"></span>'
        f'<span style="font-size:0.78rem;font-weight:700;color:#3B3650;">{title}</span>'
        f'</div>'
        f'{html_table}'
        f'{caption_html}'
        f'</div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
#  FUNGSI PUBLIK — dipanggil dari app.py
# ══════════════════════════════════════════════════════════════════════════════

def tampilkan_matriks_dasar(arr_asli: np.ndarray, arr_hasil: np.ndarray,
                             label_asli: str = "Matriks Citra Asli",
                             label_hasil: str = "Matriks Hasil Proses"):
    """
    Tampilkan matriks sebelum dan sesudah proses berdampingan.
    Fungsi utama yang dipakai sebagian besar halaman.

    Parameters
    ----------
    arr_asli  : numpy array gambar asli (2-D atau 3-D)
    arr_hasil : numpy array hasil proses (2-D atau 3-D)
    label_asli  : judul panel kiri
    label_hasil : judul panel kanan
    """
    if arr_asli is None:
        return

    _section_divider("Visualisasi Matriks Piksel")

    if arr_hasil is None:
        # Hanya tampilkan matriks asli (single column, lebih rapi)
        m_asli = _crop_matrix(arr_asli)
        caption_a = _caption_crop(arr_asli)
        if len(arr_asli.shape) == 3:
            caption_a += " (menampilkan channel R)"
        _matrix_card(
            label_asli,
            _matrix_to_html_indexed(m_asli),
            caption_a,
            accent="#A97CF8"
        )
    else:
        col_l, col_r = st.columns(2)

        with col_l:
            m_asli = _crop_matrix(arr_asli)
            caption_a = _caption_crop(arr_asli)
            if len(arr_asli.shape) == 3:
                caption_a += " (menampilkan channel R)"
            _matrix_card(
                label_asli,
                _matrix_to_html_indexed(m_asli, highlight_bg=KERNEL_BG,
                                        highlight_color=KERNEL_COLOR),
                caption_a,
                accent="#A97CF8"
            )

        with col_r:
            m_hasil = _crop_matrix(arr_hasil)
            caption_h = _caption_crop(arr_hasil)
            if len(arr_hasil.shape) == 3:
                caption_h += " (menampilkan channel R)"
            _matrix_card(
                label_hasil,
                _matrix_to_html_indexed(m_hasil, highlight_bg=RESULT_BG,
                                        highlight_color=RESULT_COLOR),
                caption_h,
                accent="#FF8C69"
            )

    _info_note()


def tampilkan_matriks_konvolusi(arr_asli: np.ndarray, arr_hasil: np.ndarray,
                                 kernel: np.ndarray, nama_filter: str,
                                 anchor_row: int = 5, anchor_col: int = 5):
    """
    Tampilkan visualisasi proses konvolusi:
    - Matriks asli + highlight area kernel
    - Kernel yang digunakan
    - Contoh perhitungan pada posisi anchor
    - Matriks hasil

    Parameters
    ----------
    arr_asli   : gambar asli (np.ndarray)
    arr_hasil  : gambar setelah difilter (np.ndarray)
    kernel     : kernel filter (np.ndarray 2-D)
    nama_filter: nama filter untuk judul
    anchor_row : baris piksel tengah yang dijadikan contoh perhitungan
    anchor_col : kolom piksel tengah yang dijadikan contoh perhitungan
    """
    if arr_asli is None:
        return

    _section_divider(f"Visualisasi Matriks & Kernel — {nama_filter}")

    # Konversi ke grayscale 2-D untuk keperluan visualisasi
    if len(arr_asli.shape) == 3:
        import cv2
        gray_asli = cv2.cvtColor(arr_asli, cv2.COLOR_RGB2GRAY)
    else:
        gray_asli = arr_asli

    if arr_hasil is not None:
        if len(arr_hasil.shape) == 3:
            import cv2
            gray_hasil = cv2.cvtColor(arr_hasil, cv2.COLOR_RGB2GRAY)
        else:
            gray_hasil = arr_hasil
    else:
        gray_hasil = None

    kh, kw = kernel.shape
    pad_r = kh // 2
    pad_c = kw // 2

    # Pastikan anchor ada di dalam batas aman
    H, W = gray_asli.shape
    ar = max(pad_r, min(anchor_row, H - pad_r - 1))
    ac = max(pad_c, min(anchor_col, W - pad_c - 1))

    # Tentukan sel-sel yang termasuk area kernel pada matriks crop
    # (relatif terhadap matriks crop MAX_DIM×MAX_DIM)
    highlight_input = set()
    for dr in range(-pad_r, pad_r + 1):
        for dc in range(-pad_c, pad_c + 1):
            rr = ar + dr
            cc = ac + dc
            if 0 <= rr < MAX_DIM and 0 <= cc < MAX_DIM:
                highlight_input.add((rr, cc))

    # ── Baris atas: gambar asli (highlight kernel) + kernel ──────────────────
    col_a, col_k = st.columns([2, 1])

    with col_a:
        m_asli = _crop_matrix(gray_asli)
        caption_a = _caption_crop(arr_asli)
        caption_a += (f" | Contoh kernel 3×3 di posisi piksel "
                      f"({ar},{ac}) — area ungu.")
        _matrix_card(
            "Matriks Citra Asli (area kernel disorot)",
            _matrix_to_html_indexed(m_asli,
                                    highlight_cells=highlight_input,
                                    highlight_bg=KERNEL_BG,
                                    highlight_color=KERNEL_COLOR),
            caption_a,
            accent="#A97CF8"
        )

    with col_k:
        kernel_int = kernel.astype(float)
        _matrix_card(
            f"Kernel {nama_filter} ({kh}×{kw})",
            _matrix_to_html(kernel_int,
                            font_size="0.82rem"),
<<<<<<< HEAD
            f"Kernel diterapkan ke setiap piksel gambar. Untuk Sobel/Prewitt: hasil akhir = √(Gx² + Gy²).",
=======
<<<<<<< HEAD
            f"Kernel diterapkan ke setiap piksel gambar. Untuk Sobel/Prewitt: hasil akhir = √(Gx² + Gy²).",
=======
            f"Kernel diterapkan ke setiap piksel gambar.",
>>>>>>> 6a7b541bfb5a1ec24e238ac21acb4151762d2686
>>>>>>> ff1b6e8435dab4fa42c9203bd0444c83af2fcd00
            accent="#A97CF8"
        )

    # ── Contoh perhitungan ────────────────────────────────────────────────────
    st.markdown(
        f'<div style="background:rgba(200,162,255,.07);border:1px solid '
        f'rgba(200,162,255,.25);border-radius:12px;padding:.9rem 1.1rem;'
        f'margin:.5rem 0;font-size:0.8rem;color:#3B3650;">'
        f'<b style="color:#A97CF8;">📐 Contoh Perhitungan Kernel</b>'
        f' — posisi piksel <b>({ar},{ac})</b><br>',
        unsafe_allow_html=True
    )

    patch = gray_asli[ar - pad_r: ar + pad_r + 1,
                      ac - pad_c: ac + pad_c + 1].astype(float)
    terms = []
    total = 0.0
    for rr in range(kh):
        for cc in range(kw):
            pv = float(patch[rr, cc]) if (rr < patch.shape[0] and cc < patch.shape[1]) else 0.0
            kv = float(kernel[rr, cc])
            product = pv * kv
            total += product
            terms.append(f"{int(pv)}×({kv:g})")

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> ff1b6e8435dab4fa42c9203bd0444c83af2fcd00
    # Gabungkan formula: pisahkan dengan " + " tapi hindari "+ -" 
    formula_parts = []
    for i, t in enumerate(terms):
        if i == 0:
            formula_parts.append(t)
        elif t.startswith("-") or "×(-" in t:
            formula_parts.append(" + " + t)
        else:
            formula_parts.append(" + " + t)
    formula = "".join(formula_parts)
<<<<<<< HEAD
=======
=======
    formula = " + ".join(terms)
>>>>>>> 6a7b541bfb5a1ec24e238ac21acb4151762d2686
>>>>>>> ff1b6e8435dab4fa42c9203bd0444c83af2fcd00
    result_val = int(np.clip(total, 0, 255))
    st.markdown(
        f'<div style="background:white;border-radius:8px;padding:.6rem .9rem;'
        f'margin-top:.5rem;font-family:monospace;font-size:0.75rem;'
        f'color:#3B3650;border:1px solid #EEEAF7;">'
        f'{formula}<br>'
        f'<b>= {total:.2f}</b> → di-clip ke [0,255] → '
        f'<b style="color:{RESULT_COLOR};">{result_val}</b>'
        f'</div></div>',
        unsafe_allow_html=True
    )

    # ── Matriks hasil ──────────────────────────────────────────────────────
    if gray_hasil is not None:
        highlight_output = set()
        if 0 <= ar < MAX_DIM and 0 <= ac < MAX_DIM:
            highlight_output.add((ar, ac))

        m_hasil = _crop_matrix(gray_hasil)
        _matrix_card(
            "Matriks Hasil Proses (piksel output disorot)",
            _matrix_to_html_indexed(m_hasil,
                                    highlight_cells=highlight_output,
                                    highlight_bg=RESULT_BG,
                                    highlight_color=RESULT_COLOR),
            _caption_crop(arr_hasil) + " | Nilai oranye = hasil konvolusi kernel di posisi tersebut.",
            accent="#FF8C69"
        )

    _info_note()


def tampilkan_matriks_morfologi(arr_asli: np.ndarray, arr_hasil: np.ndarray,
                                 se: np.ndarray, nama_operasi: str,
                                 se_type: str,
                                 anchor_row: int = 5, anchor_col: int = 5):
    """
    Tampilkan visualisasi proses morfologi:
    - Matriks input + highlight area SE
    - Elemen Penstruktur (SE)
    - Penjelasan proses (erosi/dilasi min/max)
    - Matriks hasil

    Parameters
    ----------
    arr_asli     : gambar asli
    arr_hasil    : gambar setelah morfologi
    se           : structuring element (np.ndarray 2-D)
    nama_operasi : "Erosi" / "Dilasi" / "Opening" / "Closing"
    se_type      : nama SE ("silang", "kotak", dsb.)
    anchor_row/col: posisi piksel contoh perhitungan
    """
    if arr_asli is None:
        return

    _section_divider(f"Visualisasi Matriks & SE — {nama_operasi}")

    import cv2
    if len(arr_asli.shape) == 3:
        gray_asli = cv2.cvtColor(arr_asli, cv2.COLOR_RGB2GRAY)
    else:
        gray_asli = arr_asli

    if arr_hasil is not None:
        if len(arr_hasil.shape) == 3:
            gray_hasil = cv2.cvtColor(arr_hasil, cv2.COLOR_RGB2GRAY)
        else:
            gray_hasil = arr_hasil.copy()
    else:
        gray_hasil = None

    kh, kw = se.shape
    pad_r = kh // 2
    pad_c = kw // 2

    H, W = gray_asli.shape
    ar = max(pad_r, min(anchor_row, H - pad_r - 1))
    ac = max(pad_c, min(anchor_col, W - pad_c - 1))

    # Sel-sel yang aktif dalam SE (bernilai 1) relatif terhadap anchor di crop
    highlight_input = set()
    se_active = []
    for dr in range(-pad_r, pad_r + 1):
        for dc in range(-pad_c, pad_c + 1):
            rse = dr + pad_r
            cse = dc + pad_c
            if se[rse, cse] == 1:
                rr = ar + dr
                cc = ac + dc
                se_active.append((rr, cc))
                if 0 <= rr < MAX_DIM and 0 <= cc < MAX_DIM:
                    highlight_input.add((rr, cc))

    col_a, col_k = st.columns([2, 1])

    with col_a:
        m_asli = _crop_matrix(gray_asli)
        caption_a = _caption_crop(arr_asli)
        caption_a += (f" | SE diterapkan di posisi ({ar},{ac}) — "
                      f"sel ungu = area aktif SE.")
        _matrix_card(
            "Matriks Citra Asli (area SE disorot)",
            _matrix_to_html_indexed(m_asli,
                                    highlight_cells=highlight_input,
                                    highlight_bg=KERNEL_BG,
                                    highlight_color=KERNEL_COLOR),
            caption_a,
            accent="#A97CF8"
        )

    with col_k:
        _matrix_card(
            f"Elemen Penstruktur — {se_type} ({kh}×{kw})",
            _matrix_to_html(se.astype(float), font_size="0.88rem"),
            "1 = aktif, 0 = tidak aktif",
            accent="#A97CF8"
        )

    # ── Penjelasan proses ──────────────────────────────────────────────────
    patch_vals = []
    for rr, cc in se_active:
        if 0 <= rr < H and 0 <= cc < W:
            patch_vals.append(int(gray_asli[rr, cc]))

    if nama_operasi in ("Erosi", "Opening"):
        op_label = "MIN"
        op_result = min(patch_vals) if patch_vals else "—"
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> ff1b6e8435dab4fa42c9203bd0444c83af2fcd00
        if nama_operasi == "Erosi":
            op_desc = "Erosi: ambil nilai <b>minimum</b> piksel di area aktif SE."
        else:  # Opening
            op_desc = "Opening = Erosi → Dilasi. Tahap 1 (Erosi): ambil nilai <b>minimum</b> piksel di area aktif SE."
    else:  # Dilasi, Closing
        op_label = "MAX"
        op_result = max(patch_vals) if patch_vals else "—"
        if nama_operasi == "Dilasi":
            op_desc = "Dilasi: ambil nilai <b>maksimum</b> piksel di area aktif SE."
        else:  # Closing
            op_desc = "Closing = Dilasi → Erosi. Tahap 1 (Dilasi): ambil nilai <b>maksimum</b> piksel di area aktif SE."
<<<<<<< HEAD
=======
=======
        op_desc = "Erosi mengambil nilai <b>minimum</b> piksel di area aktif SE."
    else:  # Dilasi, Closing
        op_label = "MAX"
        op_result = max(patch_vals) if patch_vals else "—"
        op_desc = "Dilasi mengambil nilai <b>maksimum</b> piksel di area aktif SE."
>>>>>>> 6a7b541bfb5a1ec24e238ac21acb4151762d2686
>>>>>>> ff1b6e8435dab4fa42c9203bd0444c83af2fcd00

    vals_str = ", ".join(str(v) for v in patch_vals) if patch_vals else "—"

    st.markdown(
        f'<div style="background:rgba(200,162,255,.07);border:1px solid '
        f'rgba(200,162,255,.25);border-radius:12px;padding:.9rem 1.1rem;'
        f'margin:.5rem 0;font-size:0.8rem;color:#3B3650;">'
        f'<b style="color:#A97CF8;">📐 Contoh Perhitungan {nama_operasi}</b>'
        f' — posisi piksel <b>({ar},{ac})</b><br>'
        f'<span style="font-size:0.75rem;color:#7B7690;">{op_desc}</span>'
        f'<div style="background:white;border-radius:8px;padding:.6rem .9rem;'
        f'margin-top:.5rem;font-family:monospace;font-size:0.75rem;'
        f'color:#3B3650;border:1px solid #EEEAF7;">'
        f'Nilai piksel di area SE: [{vals_str}]<br>'
        f'<b>{op_label}([{vals_str}])</b> = '
        f'<b style="color:{RESULT_COLOR};">{op_result}</b>'
        f'</div></div>',
        unsafe_allow_html=True
    )

    # ── Matriks hasil ──────────────────────────────────────────────────────
    if gray_hasil is not None:
        highlight_output = set()
        if 0 <= ar < MAX_DIM and 0 <= ac < MAX_DIM:
            highlight_output.add((ar, ac))

        m_hasil = _crop_matrix(gray_hasil)
        _matrix_card(
            "Matriks Hasil Proses (piksel output disorot)",
            _matrix_to_html_indexed(m_hasil,
                                    highlight_cells=highlight_output,
                                    highlight_bg=RESULT_BG,
                                    highlight_color=RESULT_COLOR),
            _caption_crop(arr_hasil) + " | Nilai oranye = output operasi morfologi.",
            accent="#FF8C69"
        )

    _info_note()


def tampilkan_matriks_histogram(arr_asli: np.ndarray):
    """
    Untuk halaman histogram: hanya tampilkan matriks asli saja
    (tidak ada "hasil" karena histogram bukan transformasi gambar).
    """
    if arr_asli is None:
        return

    _section_divider("Matriks Piksel Gambar")

    m = _crop_matrix(arr_asli)
    caption = _caption_crop(arr_asli)
    if len(arr_asli.shape) == 3:
        caption += " (menampilkan channel R)"

    _matrix_card(
        "Matriks Citra Asli",
        _matrix_to_html_indexed(m),
        caption,
        accent="#A97CF8"
    )
    _info_note()


def tampilkan_matriks_dua_input(arr1: np.ndarray, arr2: np.ndarray,
                                 arr_hasil: np.ndarray,
                                 label1: str = "Matriks Gambar 1",
                                 label2: str = "Matriks Gambar 2",
                                 label_hasil: str = "Matriks Hasil"):
    """
    Khusus untuk operasi logika AND/OR/XOR yang memakai dua gambar.
    Tampilkan tiga kolom: matriks input-1, input-2, dan hasil.
    """
    if arr1 is None:
        return

    _section_divider("Visualisasi Matriks Piksel")

    col1, col2, col3 = st.columns(3)

    with col1:
        m = _crop_matrix(arr1)
        caption = _caption_crop(arr1)
        if len(arr1.shape) == 3:
            caption += " (channel R)"
        _matrix_card(label1, _matrix_to_html_indexed(m), caption, accent="#A97CF8")

    with col2:
        if arr2 is not None:
            m2 = _crop_matrix(arr2)
            caption2 = _caption_crop(arr2)
            if len(arr2.shape) == 3:
                caption2 += " (channel R)"
            _matrix_card(label2, _matrix_to_html_indexed(m2), caption2, accent="#A97CF8")

    with col3:
        if arr_hasil is not None:
            mh = _crop_matrix(arr_hasil)
            captionh = _caption_crop(arr_hasil)
            if len(arr_hasil.shape) == 3:
                captionh += " (channel R)"
            _matrix_card(
                label_hasil,
                _matrix_to_html_indexed(mh, highlight_bg=RESULT_BG,
                                        highlight_color=RESULT_COLOR),
                captionh,
                accent="#FF8C69"
            )

    _info_note()
