import streamlit as st
import numpy as np
from PIL import Image
from modules.input_gambar import load_gambar, tampilkan_gambar, get_info_gambar
from modules.grayscale_biner import konversi_grayscale, konversi_biner, konversi_biner_otsu
from modules.aritmatika_logika import (operasi_penjumlahan, operasi_pengurangan,
                                        operasi_perkalian, operasi_pembagian,
                                        operasi_and, operasi_or, 
                                        operasi_not, operasi_xor)
from modules.histogram import tampilkan_histogram
from modules.konvolusi import filter_mean, filter_sharpening, filter_sobel, filter_prewitt
from modules.morfologi import erosi, dilasi, opening, closing

# ── Konfigurasi halaman ──────────────────────────────────────────
st.set_page_config(
    page_title="Pengolahan Citra Digital",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ Aplikasi Pengolahan Citra Digital")
st.markdown("---")

# ── Sidebar ──────────────────────────────────────────────────────
st.sidebar.title("⚙️ Menu Fitur")
menu = st.sidebar.selectbox("Pilih Fitur:", [
    "📁 Input & Tampilkan Gambar",
    "🎨 Grayscale & Citra Biner",
    "➕ Operasi Aritmatika",
    "🔣 Operasi Logika",
    "📊 Histogram",
    "🔍 Konvolusi & Filter",
    "🔷 Operasi Morfologi"
])

# ── Upload Gambar (selalu tampil) ─────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.subheader("📤 Upload Gambar")
image, img_array, filename = load_gambar()

# ── Halaman: Input & Tampilkan Gambar ────────────────────────────
if menu == "📁 Input & Tampilkan Gambar":
    st.header("📁 Input & Tampilkan Gambar")
    
    if image is not None:
        st.success(f"✅ Gambar berhasil diupload: **{filename}**")
        tampilkan_gambar(image, f"Gambar Asli — {filename}")
        get_info_gambar(img_array)
    else:
        st.info("👈 Silakan upload gambar di sidebar kiri")

# ── Halaman: Grayscale & Citra Biner ─────────────────────────────
elif menu == "🎨 Grayscale & Citra Biner":
    st.header("🎨 Grayscale & Citra Biner")
    
    if img_array is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Gambar Asli")
            st.image(image, use_column_width=True)
        
        with col2:
            pilihan = st.radio("Pilih Konversi:", 
                               ["Grayscale", "Citra Biner Manual", "Citra Biner Otsu"])
            
            if pilihan == "Grayscale":
                hasil = konversi_grayscale(img_array)
                st.subheader("Hasil Grayscale")
                st.image(hasil, use_column_width=True, clamp=True)
            
            elif pilihan == "Citra Biner Manual":
                threshold = st.slider("Nilai Threshold (T):", 0, 255, 128)
                hasil = konversi_biner(img_array, threshold)
                st.subheader(f"Hasil Biner (T={threshold})")
                st.image(hasil, use_column_width=True, clamp=True)
            
            elif pilihan == "Citra Biner Otsu":
                hasil, t_val = konversi_biner_otsu(img_array)
                st.subheader(f"Hasil Biner Otsu (T={t_val:.0f})")
                st.image(hasil, use_column_width=True, clamp=True)
    else:
        st.info("👈 Silakan upload gambar di sidebar kiri")

# ── Halaman: Operasi Aritmatika ───────────────────────────────────
elif menu == "➕ Operasi Aritmatika":
    st.header("➕ Operasi Aritmatika")
    
    if img_array is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Gambar Asli")
            st.image(image, use_column_width=True)
        
        with col2:
            operasi = st.selectbox("Pilih Operasi:", 
                                   ["Penjumlahan", "Pengurangan", 
                                    "Perkalian", "Pembagian"])
            
            if operasi in ["Penjumlahan", "Pengurangan"]:
                nilai = st.slider("Nilai:", 0, 255, 50)
            else:
                nilai = st.slider("Nilai:", 0.1, 3.0, 1.5)
            
            if operasi == "Penjumlahan":
                hasil = operasi_penjumlahan(img_array, int(nilai))
            elif operasi == "Pengurangan":
                hasil = operasi_pengurangan(img_array, int(nilai))
            elif operasi == "Perkalian":
                hasil = operasi_perkalian(img_array, nilai)
            else:
                hasil = operasi_pembagian(img_array, nilai)
            
            st.subheader(f"Hasil {operasi}")
            st.image(hasil, use_column_width=True, clamp=True)
    else:
        st.info("👈 Silakan upload gambar di sidebar kiri")

# ── Halaman: Operasi Logika ───────────────────────────────────────
elif menu == "🔣 Operasi Logika":
    st.header("🔣 Operasi Logika")
    
    if img_array is not None:
        operasi = st.selectbox("Pilih Operasi Logika:", 
                               ["NOT", "AND", "OR", "XOR"])
        
        if operasi == "NOT":
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Gambar Asli")
                st.image(image, use_column_width=True)
            with col2:
                hasil = operasi_not(img_array)
                st.subheader("Hasil NOT")
                st.image(hasil, use_column_width=True, clamp=True)
        
        else:
            st.info("Upload gambar kedua untuk operasi AND / OR / XOR")
            image2, img_array2, filename2 = load_gambar()
            
            if img_array2 is not None:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.subheader("Gambar 1")
                    st.image(image, use_column_width=True)
                with col2:
                    st.subheader("Gambar 2")
                    st.image(image2, use_column_width=True)
                with col3:
                    if operasi == "AND":
                        hasil = operasi_and(img_array, img_array2)
                    elif operasi == "OR":
                        hasil = operasi_or(img_array, img_array2)
                    else:
                        hasil = operasi_xor(img_array, img_array2)
                    st.subheader(f"Hasil {operasi}")
                    st.image(hasil, use_column_width=True, clamp=True)
    else:
        st.info("👈 Silakan upload gambar di sidebar kiri")

# ── Halaman: Histogram ────────────────────────────────────────────
elif menu == "📊 Histogram":
    st.header("📊 Histogram")
    
    if img_array is not None:
        st.subheader("Gambar Asli")
        st.image(image, width=300)
        st.subheader("Histogram Gambar")
        tampilkan_histogram(img_array)
    else:
        st.info("👈 Silakan upload gambar di sidebar kiri")

# ── Halaman: Konvolusi & Filter ───────────────────────────────────
elif menu == "🔍 Konvolusi & Filter":
    st.header("🔍 Konvolusi & Filter Spasial")
    
    if img_array is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Gambar Asli")
            st.image(image, use_column_width=True)
        
        with col2:
            filter_pilihan = st.selectbox("Pilih Filter:", [
                "Mean (Blur)", 
                "Sharpening Standar",
                "Sharpening Kuat",
                "Edge Detection Sobel",
                "Edge Detection Prewitt"
            ])
            
            if filter_pilihan == "Mean (Blur)":
                kernel_size = st.slider("Ukuran Kernel:", 3, 11, 3, step=2)
                hasil = filter_mean(img_array, kernel_size)
            elif filter_pilihan == "Sharpening Standar":
                hasil = filter_sharpening(img_array, "standar")
            elif filter_pilihan == "Sharpening Kuat":
                hasil = filter_sharpening(img_array, "kuat")
            elif filter_pilihan == "Edge Detection Sobel":
                hasil = filter_sobel(img_array)
            else:
                hasil = filter_prewitt(img_array)
            
            st.subheader(f"Hasil {filter_pilihan}")
            st.image(hasil, use_column_width=True, clamp=True)
    else:
        st.info("👈 Silakan upload gambar di sidebar kiri")

# ── Halaman: Operasi Morfologi ────────────────────────────────────
elif menu == "🔷 Operasi Morfologi":
    st.header("🔷 Operasi Morfologi")
    
    if img_array is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Gambar Asli")
            st.image(image, use_column_width=True)
        
        with col2:
            operasi_morf = st.selectbox("Pilih Operasi:", [
                "Erosi", "Dilasi", "Opening", "Closing"
            ])
            
            se_pilihan = st.selectbox("Pilih Elemen Penstruktur (SE):", [
                "silang", "kotak", "diagonal", "vertikal", "horizontal"
            ])
            
            if operasi_morf == "Erosi":
                hasil = erosi(img_array, se_pilihan)
            elif operasi_morf == "Dilasi":
                hasil = dilasi(img_array, se_pilihan)
            elif operasi_morf == "Opening":
                hasil = opening(img_array, se_pilihan)
            else:
                hasil = closing(img_array, se_pilihan)
            
            st.subheader(f"Hasil {operasi_morf} ({se_pilihan})")
            st.image(hasil, use_column_width=True, clamp=True)
    else:
        st.info("👈 Silakan upload gambar di sidebar kiri")