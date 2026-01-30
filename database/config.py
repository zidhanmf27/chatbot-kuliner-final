"""
=============================================================================
KONFIGURASI DATASET (MODE CSV)
=============================================================================
File ini mengatur path ke file CSV. 
Sistem sekarang berjalan tanpa database SQL (MySQL/SQLite).
"""

import os

# Path Absolut ke Folder Dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

# File Utama Data UMKM
DATA_PATH = os.path.join(DATASET_DIR, "dataset-kuliner-umkm-optimized.csv")

# File Pendaftaran Pending
PENDING_PATH = os.path.join(DATASET_DIR, "pending_registrations.csv")

# File Log Chat (Baru, untuk ganti tabel chat_logs)
LOG_PATH = os.path.join(DATASET_DIR, "chat_logs.csv")

# Pastikan file log ada
if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, 'w') as f:
        f.write("timestamp,user_query,corrected_query,warning_msg,total_recommendations,user_ip\n")

# Pastikan file pending ada
if not os.path.exists(PENDING_PATH):
    with open(PENDING_PATH, 'w') as f:
        f.write("timestamp,nama_rumah_makan,alamat,kategori,range_harga,menu,suasana,tipe_pengunjung,fasilitas,status\n")

