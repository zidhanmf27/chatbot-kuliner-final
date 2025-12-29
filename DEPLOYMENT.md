# Panduan Deployment ke Streamlit Cloud 🚀

Panduan ini akan membantu Anda men-deploy aplikasi **Chatbot Kuliner Bandung** ke internet agar bisa diakses oleh siapa saja secara gratis menggunakan **Streamlit Community Cloud**.

---

## 📋 Langkah 1: Persiapan File (Sudah Siap!)
Pastikan 3 komponen utama ini sudah ada di folder proyek Anda (Saya sudah memeriksanya, semuanya aman ✅):
1.  **`app.py`**: File utama aplikasi.
2.  **`requirements.txt`**: Daftar library yang dibutuhkan (streamlit, pandas, scikit-learn, Sastrawi, dll).
3.  **Folder `dataset/`**: Berisi file CSV data kuliner.

---

## 🐙 Langkah 2: Upload ke GitHub
Streamlit Cloud mengambil kode langsung dari GitHub. Anda perlu "memasukkan" folder proyek ini ke repository GitHub.

### Jika Anda sudah paham Git:
1.  Buat repository baru di GitHub (set ke **Public**).
2.  Push semua file di folder ini ke repository tersebut.

### Jika Anda belum terbiasa dengan Git (Cara Mudah via Browser):
1.  Login ke [GitHub.com](https://github.com/).
2.  Klik tombol **New** untuk membuat repository baru.
3.  Beri nama, misal `chatbot-kuliner-umkm-bandung`. Pilih **Public**. Klik **Create repository**.
4.  Di halaman selanjutnya, cari link **"uploading an existing file"**.
5.  Drag & Drop (Seret) **SEMUA file dan folder** dari komputer Anda ke halaman upload GitHub tersebut.
    *   *Pastikan folder `style` dan `dataset` ikut ter-upload.*
6.  Tunggu proses upload selesai, lalu klik tombol hijau **Commit changes**.

---

## ☁️ Langkah 3: Deploy di Streamlit Cloud
1.  Buka [share.streamlit.io](https://share.streamlit.io/).
2.  Login menggunakan akun GitHub Anda.
3.  Klik tombol biru **New app** di pojok kanan atas.
4.  **Isi Form Deployment:**
    *   **Repository:** Cari nama repository yang baru Anda buat (misal: `username/chatbot-kuliner-umkm-bandung`).
    *   **Branch:** Biarkan default (`main` atau `master`).
    *   **Main file path:** Ketik `app.py`.
5.  Klik tombol **Deploy!**.

---

## ☕ Langkah 4: Tunggu Proses Build
*   Streamlit akan mulai "membangun" aplikasi Anda. Anda bisa melihat log prosesnya di layar sebelah kanan (ikon oven 🍪).
*   Sistem akan menginstal semua library yang ada di `requirements.txt`.
*   Proses ini biasanya memakan waktu **1-3 menit**.

---

## 🎉 Selesai!
Setelah loading selesai, aplikasi Anda akan terbuka dengan alamat URL unik (contoh: `https://chatbot-kuliner-umkm-bandung.streamlit.app`).

Anda sekarang bisa membagikan link tersebut ke teman, dosen, atau portofolio Anda!

### 💡 Tips Tambahan:
*   Jika terjadi error saat deploy, cek bagian log (pojok kanan bawah layar Streamlit Cloud) untuk melihat pesan errornya.
*   Jika Anda mengupdate kode di komputer dan meng-upload ulang ke GitHub, aplikasi di Streamlit Cloud akan **otomatis terupdate** dalam beberapa saat.
