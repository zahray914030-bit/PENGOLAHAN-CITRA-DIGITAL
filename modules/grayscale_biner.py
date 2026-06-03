import cv2
import numpy as np
from PIL import Image

def konversi_grayscale(img_array):
    """Fungsi mengubah gambar menjadi grayscale"""
    if img_array is None:
        return None
    
    # Jika gambar sudah grayscale
    if len(img_array.shape) == 2:
        return img_array
    
    # Konversi RGB ke Grayscale
    grayscale = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    return grayscale

def konversi_biner(img_array, threshold=128):
    """Fungsi mengubah gambar menjadi citra biner"""
    if img_array is None:
        return None
    
    # Pastikan gambar dalam grayscale dulu
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Terapkan thresholding
    _, biner = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return biner

def konversi_biner_otsu(img_array):
    """Fungsi mengubah gambar menjadi citra biner dengan metode Otsu"""
    if img_array is None:
        return None
    
    # Pastikan gambar dalam grayscale dulu
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Terapkan thresholding Otsu (otomatis cari nilai T terbaik)
    threshold_val, biner = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return biner, threshold_val