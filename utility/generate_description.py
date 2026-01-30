"""
=============================================================================
GENERATOR DESKRIPSI OTOMATIS
=============================================================================
File ini berisi fungsi untuk membuat deskripsi tempat makan secara otomatis
berdasarkan data yang tersedia (nama, suasana, tipe pengunjung, fasilitas).

Contoh hasil:
"Warung Nasi Ibu Haji adalah tempat makan dengan nuansa Tradisional yang 
cocok dikunjungi oleh Keluarga. Dilengkapi dengan fasilitas seperti Parkir, 
Mushola. Tempat ini sangat cocok untuk anda kunjungi bersama keluarga."
=============================================================================
"""

import pandas as pd
import random


# =============================================================================
# DAFTAR KALIMAT PEMANIS (Dipilih Secara Acak)
# =============================================================================

SWEETENERS = [
    "Tempat ini sangat cocok untuk anda kunjungi bersama keluarga dan teman-teman.",
    "Rasakan pengalaman kuliner yang otentik dan tak terlupakan di setiap gigitan.",
    "Pilihan yang sempurna untuk melepas penat sambil menikmati hidangan lezat.",
    "Destinasi kuliner yang wajib dicoba saat berada di Bandung.",
    "Nikmati momen bersantap yang santai dengan suasana yang mendukung.",
    "Dijamin ketagihan dengan cita rasa khas yang ditawarkan.",
    "Suasana yang homey bikin betah berlama-lama di sini.",
    "Cocok untuk mengisi waktu luang dengan wisata kuliner yang memanjakan lidah.",
    "Sebuah permata tersembunyi bagi para pencinta makanan enak.",
    "Hadirkan keceriaan di setiap santapan anda di tempat ini."
]


# =============================================================================
# FUNGSI UTAMA: GENERATE DESKRIPSI
# =============================================================================

def generate_description_text(row):
    """
    Membuat deskripsi otomatis untuk tempat makan.
    
    Format deskripsi:
    1. Kalimat utama: "[Nama] adalah tempat makan dengan nuansa [Suasana] 
       yang cocok dikunjungi oleh [Tipe Pengunjung]."
    2. Kalimat fasilitas: "Dilengkapi dengan fasilitas seperti [Fasilitas]."
    3. Kalimat pemanis: Dipilih secara acak dari daftar SWEETENERS
    
    Args:
        row (dict/Series): Baris data yang berisi kolom:
            - nama_rumah_makan
            - suasana
            - tipe_pengunjung
            - fasilitas
    
    Returns:
        str: Deskripsi lengkap yang sudah di-generate
    """
    
    def get_val(col):
        """
        Mengambil nilai kolom dan membersihkannya.
        
        Menangani kasus:
        - Nilai kosong (NaN, None, "")
        - Tanda strip ("-")
        - String "nan" (lowercase)
        
        Returns:
            str: Nilai yang sudah dibersihkan, atau "" jika tidak valid
        """
        val = row.get(col)
        
        # Cek jika null, empty, atau tanda strip '-'
        if pd.isna(val) or str(val).strip() == '' or str(val).strip() == '-':
            return ""
        
        # Bersihkan string
        clean_val = str(val).strip()
        
        # Cek jika string "nan" (hasil konversi NaN ke string)
        if clean_val.lower() == 'nan':
            return ""
            
        return clean_val

    # Ambil nilai dari setiap kolom
    nama = get_val('nama_rumah_makan')
    suasana = get_val('suasana')
    tipe_pengunjung = get_val('tipe_pengunjung')
    fasilitas = get_val('fasilitas')

    # --- BAGIAN 1: KALIMAT UTAMA ---
    parts = []
    
    if nama:
        parts.append(f"{nama} adalah tempat makan")
    
    if suasana:
        parts.append(f"dengan nuansa {suasana}")
    
    if tipe_pengunjung:
        parts.append(f"yang cocok dikunjungi oleh {tipe_pengunjung}")
    
    # Gabungkan bagian-bagian kalimat utama
    main_sentence = " ".join(parts) + "." if parts else ""
    
    # --- BAGIAN 2: KALIMAT FASILITAS ---
    fasilitas_sentence = ""
    if fasilitas:
        fasilitas_sentence = f"Dilengkapi dengan fasilitas seperti {fasilitas}."
    
    # --- BAGIAN 3: KALIMAT PEMANIS (ACAK) ---
    sweetener = random.choice(SWEETENERS)
    
    # --- GABUNGKAN SEMUA BAGIAN ---
    # Format: [Kalimat Utama] [Fasilitas] [Pemanis]
    # Filter string kosong sebelum digabung
    full_desc_parts = [main_sentence, fasilitas_sentence, sweetener]
    full_desc = " ".join([p for p in full_desc_parts if p]).strip()
    
    return full_desc


# =============================================================================
# FUNGSI UNTUK BATCH PROCESSING (Update Seluruh Dataset)
# =============================================================================

def main():
    """
    Fungsi untuk update kolom 'deskripsi' di seluruh dataset CSV.
    
    Proses:
    1. Baca file CSV
    2. Generate deskripsi untuk setiap baris
    3. Simpan kembali ke file CSV
    
    Note: Path CSV di-hardcode, sesuaikan jika perlu
    """
    # Path ke file CSV (sesuaikan dengan lokasi Anda)
    csv_path = r'C:\Users\Zidhan Maula Fatih\Kuliah\chatbot-kuliner\dataset\dataset-kuliner-umkm-optimized.csv'
    
    try:
        print("[INFO] Membaca dataset...")
        
        # Coba baca dengan encoding UTF-8, fallback ke ISO-8859-1
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(csv_path, encoding='ISO-8859-1')
            
        print(f"[INFO] Dataset dimuat. Total baris: {len(df)}")
        
        print("[INFO] Sedang men-generate ulang kolom 'deskripsi'...")
        
        # Generate deskripsi untuk setiap baris
        df['deskripsi'] = df.apply(generate_description_text, axis=1)
        
        # Validasi: cek apakah ada deskripsi yang kosong
        empty_count = df[df['deskripsi'].str.strip() == ''].shape[0]
        if empty_count > 0:
            print(f"[WARNING] Ada {empty_count} baris yang deskripsinya kosong!")

        print("[INFO] Menyimpan perubahan ke CSV...")
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        print("\n[SUCCESS] Selesai! Kolom deskripsi telah diperbarui.")
        print("=" * 60)
        print("SAMPLE DESKRIPSI BARU (Baris Pertama):")
        print(df['deskripsi'].iloc[0])
        print("=" * 60)
        
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")


# =============================================================================
# TESTING (Jalankan file ini langsung untuk update dataset)
# =============================================================================

if __name__ == "__main__":
    main()
