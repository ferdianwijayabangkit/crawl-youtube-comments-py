# 🎬 YouTube Comments Crawler

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Terminal%2FCMD-lightgrey)

Sistem crawling komentar YouTube interaktif berbasis terminal (CMD/Shell) yang dirancang untuk penelitian akademik dan analisis data mendalam.

## ✨ Fitur Utama

- **Ekstraksi Super Lengkap**: Mengambil komentar, balasan, dan semua atribut penting (penulis, status suka, pin, dll.).
- **Input URL Fleksibel**: Mendukung input manual, batch, dari file **Excel**, atau file **teks (.txt)**.
- **Menu Interaktif & Aman**: Antarmuka berbasis menu yang memvalidasi setiap input dan memungkinkan navigasi kembali/keluar.
- **Konfigurasi Penuh**: Atur jumlah komentar, urutan, sertakan balasan, dan format output melalui menu interaktif.
- **Manajemen API Key**: Mendukung input manual, impor dari file, atau variabel lingkungan (`.env`), dengan penyimpanan otomatis.
- **Analisis Bawaan**: Dilengkapi analisis sentimen (opsional), penghitung kata, dan deteksi tautan/mention.
- **Penanganan Error Cerdas**: Diagnostik otomatis untuk masalah API, kuota habis, atau kunci tidak valid.

## 🔧 Tumpukan Teknologi (Tech Stack)

- **Bahasa**: `Python 3.7+`
- **Interaksi API**: `google-api-python-client`
- **Manipulasi Data**: `Pandas`
- **Antarmuka Terminal**: Logika kustom (input, colorama, dll.)
- **Analisis Teks**: `TextBlob` (opsional)

## 🚀 Cara Memulai

### Prasyarat
- **Python 3.7** atau versi yang lebih baru.
- **Kunci API (API Key)** dari Google Cloud Console yang telah mengaktifkan **YouTube Data API v3**.
- Terminal atau Command Prompt (Windows/macOS/Linux).

### Instalasi & Penggunaan

1.  **Clone Repositori**
    Gunakan `git` untuk mengunduh proyek ke komputer lokal Anda.
    ```bash
    git clone [https://github.com/ferdianwijayabangkit/crawl-youtube-comments-py.git](https://github.com/ferdianwijayabangkit/crawl-youtube-comments-py.git)
    cd crawl-youtube-comments-py
    ```

2.  **Instal Dependensi**
    Jalankan perintah berikut untuk menginstal semua pustaka yang dibutuhkan.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Skrip**
    Buka terminal atau CMD di dalam folder proyek dan jalankan skrip.
    ```bash
    python youtube_comments_crawler.py
    ```
    Program akan memandu Anda melalui menu interaktif untuk memasukkan Kunci API, URL video, dan konfigurasi lainnya.

## 📊 Struktur Data Output

Data yang berhasil diekstrak sangat komprehensif. Berikut adalah beberapa contoh kolom utama:

| Field                   | Deskripsi                                          | Contoh                                     |
| ----------------------- | -------------------------------------------------- | ------------------------------------------ |
| `comment_text`          | Isi teks dari komentar                             | "Tutorial ini sangat jelas dan membantu!"  |
| `author_name`           | Nama channel dari pemberi komentar                 | "Analis Data"                              |
| `author_channel_url`    | URL channel penulis komentar                       | "https://youtube.com/channel/..."          |
| `is_hearted_by_creator` | Apakah komentar disukai oleh pemilik video         | True                                       |
| `like_count`            | Jumlah suka yang diterima komentar                 | 250                                        |
| `reply_count`           | Jumlah balasan untuk komentar tersebut             | 15                                         |
| `publish_date`          | Waktu komentar dipublikasikan                      | "2025-07-30T10:00:00Z"                     |
| `video_title`           | Judul video tempat komentar diambil                | "Belajar Python untuk Pemula"              |
| `sentiment_score`       | Skor sentimen dari komentar (opsional)             | 0.85                                       |
| `comment_type`          | Tipe komentar (main/reply)                         | "main"                                     |

## 💡 Tips & Troubleshooting

- **Error API Key?** Program ini memiliki diagnostik otomatis. Pastikan Kunci API Anda benar, YouTube Data API v3 telah diaktifkan di Google Cloud, dan kuota Anda belum habis.
- **Input File**: Untuk input dari file Excel atau `.txt`, pastikan formatnya sesuai dengan contoh yang diberikan dalam dokumentasi lengkap.
- **Konfigurasi Default**: Anda dapat mengatur Kunci API dan parameter lainnya secara permanen di file `config.ini` untuk mempercepat proses.

## ⚖️ Lisensi & Penafian

- Proyek ini dilisensikan di bawah **Lisensi MIT**.
- Harap gunakan tool ini secara etis dan bertanggung jawab, sesuai dengan **Persyaratan Layanan YouTube API** dan regulasi privasi data yang berlaku.

## 👨‍💻 Author

- **Ferdian Bangkit Wijaya**
- Universitas Sultan Ageng Tirtayasa (UNTIRTA)
- Versi: 1.0.0 (Juli 2025)

---

> Tool ini dirancang untuk memberdayakan para peneliti dengan data yang kaya dari YouTube melalui antarmuka yang kuat dan mudah digunakan. Selamat meneliti!
