import cv2
import numpy as np

# Elemen Penstruktur (SE) dari slide minggu 9 & 10
SE_KOTAK = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
], dtype=np.uint8)

SE_SILANG = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
], dtype=np.uint8)

SE_DIAGONAL = np.array([
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
], dtype=np.uint8)

SE_VERTIKAL = np.array([
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
], dtype=np.uint8)

SE_HORIZONTAL = np.array([
    [0, 0, 0],
    [1, 1, 1],
    [0, 0, 0]
], dtype=np.uint8)

def erosi(img_array, se_type="silang"):
    """Operasi Erosi - menipiskan objek"""
    if img_array is None:
        return None
    
    # Pilih elemen penstruktur
    se = pilih_se(se_type)
    
    # Pastikan grayscale
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    hasil = cv2.erode(gray, se, iterations=1)
    return hasil

def dilasi(img_array, se_type="silang"):
    """Operasi Dilasi - menebalkan objek"""
    if img_array is None:
        return None
    
    se = pilih_se(se_type)
    
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    hasil = cv2.dilate(gray, se, iterations=1)
    return hasil


def pilih_se(se_type):
    """Fungsi memilih elemen penstruktur"""
    pilihan = {
        "kotak"     : SE_KOTAK,
        "silang"    : SE_SILANG,
        "diagonal"  : SE_DIAGONAL,
        "vertikal"  : SE_VERTIKAL,
        "horizontal": SE_HORIZONTAL
    }
    return pilihan.get(se_type, SE_SILANG)