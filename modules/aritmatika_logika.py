import cv2
import numpy as np

def operasi_penjumlahan(img_array, nilai=50):
    """Menambah kecerahan gambar"""
    if img_array is None:
        return None
    hasil = cv2.add(img_array, np.ones(img_array.shape, dtype=np.uint8) * nilai)
    return hasil

def operasi_pengurangan(img_array, nilai=50):
    """Mengurangi kecerahan gambar"""
    if img_array is None:
        return None
    hasil = cv2.subtract(img_array, np.ones(img_array.shape, dtype=np.uint8) * nilai)
    return hasil

def operasi_perkalian(img_array, nilai=1.5):
    """Mengalikan nilai piksel gambar"""
    if img_array is None:
        return None
    hasil = cv2.multiply(img_array, np.ones(img_array.shape, dtype=np.float32) * nilai)
    hasil = np.clip(hasil, 0, 255).astype(np.uint8)
    return hasil

def operasi_pembagian(img_array, nilai=1.5):
    """Membagi nilai piksel gambar"""
    if img_array is None:
        return None
    hasil = img_array.astype(np.float32) / nilai
    hasil = np.clip(hasil, 0, 255).astype(np.uint8)
    return hasil

def operasi_and(img_array1, img_array2):
    """Operasi logika AND antara dua gambar"""
    if img_array1 is None or img_array2 is None:
        return None
    # Samakan ukuran
    img2_resized = cv2.resize(img_array2, 
                              (img_array1.shape[1], img_array1.shape[0]))
    hasil = cv2.bitwise_and(img_array1, img2_resized)
    return hasil

def operasi_or(img_array1, img_array2):
    """Operasi logika OR antara dua gambar"""
    if img_array1 is None or img_array2 is None:
        return None
    img2_resized = cv2.resize(img_array2,
                              (img_array1.shape[1], img_array1.shape[0]))
    hasil = cv2.bitwise_or(img_array1, img2_resized)
    return hasil

def operasi_not(img_array):
    """Operasi logika NOT (inversi gambar)"""
    if img_array is None:
        return None
    hasil = cv2.bitwise_not(img_array)
    return hasil

def operasi_xor(img_array1, img_array2):
    """Operasi logika XOR antara dua gambar"""
    if img_array1 is None or img_array2 is None:
        return None
    img2_resized = cv2.resize(img_array2,
                              (img_array1.shape[1], img_array1.shape[0]))
    hasil = cv2.bitwise_xor(img_array1, img2_resized)
    return hasil