import pandas as pd
from documentation_labeling_kategori import classify_restaurant

# Path file
csv_path = r'C:\Users\Zidhan Maula Fatih\Kuliah\chatbot-kuliner\dataset\dataset-kuliner-umkm-optimized.csv'

print("[INFO] Membaca dataset...")
df = pd.read_csv(csv_path)

print("[INFO] Membuat kolom 'kategori_saran'...")
df['kategori_saran'] = df.apply(classify_restaurant, axis=1)

# Pindahkan kolom kategori_saran ke sebelah kolom kategori biar enak dilihat
# Ambil index kolom kategori
col_idx = df.columns.get_loc('kategori')
# Pindahkan (pop lalu insert)
cols = list(df.columns)
cols.remove('kategori_saran') # Hapus dari posisi akhir
cols.insert(col_idx + 1, 'kategori_saran') # Masukkan setelah kategori
df = df[cols]

# Hitung perbedaan
mismatches = df[df['kategori'] != df['kategori_saran']]
print(f"[INFO] Total Perbedaan: {len(mismatches)} dari {len(df)} data.")

# Simpan
print("[INFO] Menyimpan ke dataset...")
df.to_csv(csv_path, index=False)

print("[SUCCESS] Selesai! Cek kolom 'kategori_saran' di file CSV Anda.")
