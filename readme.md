#  Chatbot Kuliner UMKM Kota Bandung

**Asisten cerdas untuk menemukan rekomendasi kuliner terbaik di Kota Bandung.**

Aplikasi ini adalah chatbot berbasis AI yang menggunakan metode **TF-IDF** dan **Cosine Similarity** untuk memberikan rekomendasi kuliner yang relevan berdasarkan pertanyaan pengguna. Dibangun dengan antarmuka **Streamlit** yang modern, responsif, dan elegan.

---

## Fitur Unggulan

### Sistem Rekomendasi Cerdas
- Menggunakan pemrosesan bahasa alami (NLP) untuk memahami pertanyaan pengguna.
- Memberikan rekomendasi berdasarkan nama tempat, kategori, atau deskripsi menu.
- Menampilkan persentase kecocokan (*match percentage*) untuk setiap rekomendasi.

### Antarmuka User-Friendly & Premium
- **Desain Modern:** Menggunakan font *Plus Jakarta Sans* dan gaya *glassmorphism*.
- **Tema Dinamis:** Mendukung **🌗 Dark Mode** (default) dan **☀️ Light Mode** yang dapat diganti secara instan dengan satu klik.
- **Responsif:** Tampilan optimal di desktop maupun perangkat mobile (HP).

### Fitur Interaktif
- **Pencarian Cepat:** Tombol pintas untuk kategori populer (Kopi Murah, Ramen Pedas, Masakan Sunda, Toko Roti).
- **Sidebar Informatif:** Menampilkan statistik total UMKM, filter kategori yang dapat di-collapse, dan tips pencarian.
- **Integrasi Google Maps:** Tombol langsung untuk melihat lokasi kuliner di Google Maps.

---

## Teknologi yang Digunakan

- **Bahasa Pemrograman:** Python 3.9+
- **Framework Web:** [Streamlit](https://streamlit.io/)
- **Machine Learning:** Scikit-learn (TF-IDF Vectorizer, Cosine Similarity)
- **Data Processing:** Pandas, NLTK (Sastrawi untuk stemming Bahasa Indonesia)
- **Styling:** Custom CSS3 dengan CSS Variables untuk manajemen tema.

---

## Cara Menjalankan Proyek

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal Anda:

### 1. Prasyarat
Pastikan Anda sudah menginstal Python. Jika belum, unduh di [python.org](https://www.python.org/).

### 2. Clone Repository (atau Copy Folder)
Salin folder proyek ini ke komputer Anda.

### 3. Instal Dependensi
Buka terminal/command prompt di dalam folder proyek, lalu jalankan:
```bash
pip install -r requirements.txt
```
*Catatan: Pastikan file `requirements.txt` mencakup: streamlit, pandas, scikit-learn, nltk, sastrawi.*

### 4. Jalankan Aplikasi
Jalankan perintah berikut di terminal:
```bash
streamlit run app.py
```

Aplikasi akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

---

## Struktur Proyek

```
chatbot-kuliner/
├── app.py                  # File utama aplikasi Streamlit (UI & Interaksi)
├── chatbot_engine.py       # Logika Chatbot (Model TF-IDF & Rekomendasi)
├── preprocessing.py        # Pembersihan teks (Stemming, Stopword removal)
├── dataset/
│   └── data-kuliner-umkm-optimized.csv # Data sumber UMKM
├── style/
│   └── app.css             # Styling Custom (Dark/Light Mode, Responsif)
├── DEPLOYMENT.md           # Panduan deployment
└── README.md               # Dokumentasi utama proyek ini
```


---

## Catatan Pengembang
- **Preprocessing:** Teks input pengguna dan data dataset diproses (lowercasing, remove punctuation, stemming) sebelum dihitung kemiripannya.
- **Tema:** Logika pergantian tema ditangani menggunakan Variable CSS yang dinamis.
