import cv2
import numpy as np

def filter_mean(img_array, kernel_size=3):
    """Filter Mean - menghaluskan gambar"""
    if img_array is None:
        return None
    kernel = np.ones((kernel_size, kernel_size), np.float32)
    kernel = kernel / (kernel_size * kernel_size)
    hasil = cv2.filter2D(img_array, -1, kernel)
    return hasil

def filter_sharpening(img_array, mode="standar"):
    """Filter Sharpening - mempertajam gambar"""
    if img_array is None:
        return None
    
    if mode == "standar":
        kernel = np.array([
            [ 0, -1,  0],
            [-1,  5, -1],
            [ 0, -1,  0]
        ])
    else:  # lebih kuat
        kernel = np.array([
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ])
    
    hasil = cv2.filter2D(img_array, -1, kernel)
    return hasil

def filter_sobel(img_array):
    """Filter Sobel - deteksi tepi"""
    if img_array is None:
        return None
    
    # Konversi ke grayscale jika perlu
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Sobel horizontal dan vertikal
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Gabungkan hasil
    sobel = np.sqrt(sobel_x**2 + sobel_y**2)
    sobel = np.uint8(np.clip(sobel, 0, 255))
    return sobel

def filter_prewitt(img_array):
    """Filter Prewitt - deteksi tepi"""
    if img_array is None:
        return None
    
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Kernel Prewitt
    kernel_x = np.array([
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ], dtype=np.float32)
    
    kernel_y = np.array([
        [-1, -1, -1],
        [ 0,  0,  0],
        [ 1,  1,  1]
    ], dtype=np.float32)
    
    prewitt_x = cv2.filter2D(gray, -1, kernel_x)
    prewitt_y = cv2.filter2D(gray, -1, kernel_y)
    
    prewitt = np.sqrt(prewitt_x.astype(np.float32)**2 + 
                      prewitt_y.astype(np.float32)**2)
    prewitt = np.uint8(np.clip(prewitt, 0, 255))
    return prewitt