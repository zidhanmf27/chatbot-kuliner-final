"""
=============================================================================
SCHEDULER SERVICE - PROSES OTOMATIS PENDAFTARAN UMKM (MODE CSV)
=============================================================================
Service ini berjalan secara otomatis untuk memproses pendaftaran UMKM baru.
Mode: CSV Only (Tanpa Database)

Tugas utama:
1. Baca file 'dataset/pending_registrations.csv'
2. Ambil data dengan status 'pending'
3. Labeling & Preprocessing
4. Append data ke 'dataset/dataset-kuliner-umkm-optimized.csv'
5. Update status di 'pending_registrations.csv' menjadi 'approved'
6. Rebuild model chatbot

Jadwal: Berjalan otomatis setiap hari jam 18:06
=============================================================================
"""

import os
import sys
import time
import pandas as pd
import csv
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# Tambahkan parent directory ke path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot_engine import ChatbotEngine
from preprocessing import TextPreprocessor
from utility.labeling_harga import label_price
from utility.generate_description import generate_description_text
from database.config import DATA_PATH, PENDING_PATH

# =============================================================================
# KONFIGURASI LOGGING
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler("scheduler/scheduler.log"),  # Simpan ke file
        logging.StreamHandler()  # Tampilkan di console
    ]
)

MODEL_PATH = os.path.join("dataset", "chatbot_model.pkl")

# =============================================================================
# FUNGSI UTAMA: PROSES DATA PENDING
# =============================================================================

def process_pending_data():
    logging.info("Memulai proses: Pendaftaran Pending (Mode CSV)")
    
    if not os.path.exists(PENDING_PATH):
        logging.info("File pending_registrations.csv tidak ditemukan.")
        return

    try:
        # 1. Baca data pending
        df_pending = pd.read_csv(PENDING_PATH)
        if df_pending.empty:
            logging.info("Tidak ada data pendaftaran.")
            return

        # Filter yang statusnya 'pending'
        # Pastikan kolom status case-insensitive trim
        df_pending['status'] = df_pending['status'].fillna('pending').astype(str).str.lower().str.strip()
        pending_rows = df_pending[df_pending['status'] == 'pending'].copy()
        
        if pending_rows.empty:
            logging.info("Tidak ada data dengan status 'pending'.")
            return
            
        logging.info(f"Ditemukan {len(pending_rows)} pendaftaran pending.")
        
        preprocessor = TextPreprocessor()
        new_data_list = []
        
        # 2. Proses data
        for index, row in pending_rows.iterrows():
            try:
                row_dict = row.to_dict()
                
                # --- LABELING & GENERATOR ---
                row_dict['kategori_harga'] = label_price(str(row_dict.get('range_harga', '')))
                row_dict['deskripsi'] = generate_description_text(row_dict)
                
                # --- METADATA ---
                meta_parts = [
                    str(row_dict.get('nama_rumah_makan', '')),
                    str(row_dict.get('alamat', '')),
                    str(row_dict.get('kategori', '')),
                    str(row_dict.get('menu', '')),
                    str(row_dict.get('deskripsi', '')),
                    str(row_dict.get('kategori_harga', ''))
                ]
                metadata_raw = " ".join([p for p in meta_parts if p and str(p).lower() != 'nan'])
                row_dict['metadata_tfidf'] = metadata_raw
                row_dict['metadata_tfidf_processed'] = preprocessor.preprocess(metadata_raw)
                row_dict['created_at'] = datetime.now().isoformat()
                
                # Hapus kolom yang tidak perlu jika ada (misal timestamp dari pending diganti created_at)
                # Sesuaikan dengan kolom di dataset utama
                
                # Masukkan ke list untuk di-append ke master data
                # Kita perlu memastika kolomnya sesuai dengan dataset utama
                new_data_list.append(row_dict)
                
                # Update status di df_pending (in memory)
                df_pending.at[index, 'status'] = 'approved'
                
            except Exception as e:
                logging.error(f"Error memproses row index {index}: {e}")

        # 3. Simpan ke Dataset Utama
        if new_data_list:
            # Baca dataset utama
            if os.path.exists(DATA_PATH):
                df_main = pd.read_csv(DATA_PATH)
            else:
                df_main = pd.DataFrame()
            
            df_new = pd.DataFrame(new_data_list)
            
            # Align columns. Keep only columns that exist in main or are standard
            # Jika df_main kosong, gunakan semua kolom df_new
            # Kita ingin menjaga kolom: nama, alamat, dll.
            # Hapus kolom 'status' dan 'timestamp' dari pending karena tidak masuk ke master kecuali kita mau
            
            cols_to_keep = ['nama_rumah_makan', 'alamat', 'kategori', 'range_harga', 'menu', 
                            'suasana', 'tipe_pengunjung', 'fasilitas', 'deskripsi', 
                            'kategori_harga', 'metadata_tfidf', 'metadata_tfidf_processed']
            
            # Pastikan kolom ada
            for col in cols_to_keep:
                if col not in df_new.columns:
                    df_new[col] = ""
            
            # Append
            df_final = pd.concat([df_main, df_new[cols_to_keep]], ignore_index=True)
            df_final.to_csv(DATA_PATH, index=False)
            logging.info(f"Berhasil menambahkan {len(new_data_list)} data ke dataset utama.")

            # 4. Update file Pending (Simpan status 'approved')
            df_pending.to_csv(PENDING_PATH, index=False)
            logging.info("Status pendaftaran diperbarui menjadi 'approved'.")

            # 5. Rebuild Model
            logging.info("Rebuild model chatbot...")
            engine = ChatbotEngine(model_path=None) # Akan load CSV baru
            engine.save_model(MODEL_PATH)
            logging.info("Model berhasil di-rebuild.")

    except Exception as e:
        logging.error(f"Error kritis scheduler: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Jalan setiap jam 18:06
    scheduler.add_job(process_pending_data, 'cron', hour=21, minute=27)
    
    logging.info("Scheduler Service (CSV Mode) dimulai. Menunggu jadwal...")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler dihentikan.")
