import cv2
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def tampilkan_histogram(img_array):
    """Fungsi menampilkan histogram gambar"""
    if img_array is None:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Jika gambar berwarna (RGB)
    if len(img_array.shape) == 3:
        warna = ['red', 'green', 'blue']
        label = ['Merah', 'Hijau', 'Biru']
        
        for i, (w, l) in enumerate(zip(warna, label)):
            histogram = cv2.calcHist([img_array], [i], None, [256], [0, 256])
            ax.plot(histogram, color=w, label=l)
        
        ax.set_title("Histogram RGB")
        ax.legend()
    
    # Jika gambar grayscale
    else:
        histogram = cv2.calcHist([img_array], [0], None, [256], [0, 256])
        ax.plot(histogram, color='gray', label='Grayscale')
        ax.set_title("Histogram Grayscale")
        ax.legend()
    
    ax.set_xlabel("Nilai Piksel (0-255)")
    ax.set_ylabel("Jumlah Piksel")
    ax.set_xlim([0, 256])
    
    st.pyplot(fig)
    plt.close()