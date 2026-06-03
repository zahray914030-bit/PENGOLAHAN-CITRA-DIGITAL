import streamlit as st
from PIL import Image
import numpy as np
import cv2

def load_gambar():
    """Fungsi untuk upload dan load gambar"""
    uploaded_file = st.file_uploader(
        "Upload Gambar", 
        type=["jpg", "jpeg", "png", "bmp"],
        help="Format yang didukung: JPG, JPEG, PNG, BMP"
    )
    
    if uploaded_file is not None:
        # Baca gambar menggunakan PIL
        image = Image.open(uploaded_file)
        
        # Konversi ke array numpy
        img_array = np.array(image)
        
        return image, img_array, uploaded_file.name
    
    return None, None, None

def tampilkan_gambar(image, judul="Gambar"):
    """Fungsi untuk menampilkan gambar"""
    if image is not None:
        st.image(image, caption=judul, use_column_width=True)
    else:
        st.warning("Tidak ada gambar yang ditampilkan")

def get_info_gambar(img_array):
    """Fungsi untuk menampilkan informasi gambar"""
    if img_array is not None:
        st.write("📊 **Informasi Gambar:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Lebar", f"{img_array.shape[1]} px")
        with col2:
            st.metric("Tinggi", f"{img_array.shape[0]} px")
        with col3:
            if len(img_array.shape) == 3:
                st.metric("Channel", img_array.shape[2])
            else:
                st.metric("Channel", 1)