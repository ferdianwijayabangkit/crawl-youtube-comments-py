# YouTube Comments Crawler 🎬

Sistem crawling komentar YouTube yang dapat dijalankan di terminal CMD secara interaktif. Dirancang khusus untuk keperluan penelitian akademik dan analisis data.

## 🚀 Fitur Utama

- **Ekstraksi Komentar & Balasan Otomatis**: Mengambil komentar, balasan, dan seluruh atribut penting dari YouTube (author, channel, status, like, heart, pinned, dsb)
- **Input URL Fleksibel**: Input manual, batch, file Excel, atau text file
- **Menu Interaktif & Validasi Input**: Semua menu hanya menerima input valid, bisa kembali/back/exit di setiap langkah
- **Konfigurasi Crawling Lengkap**: Atur jumlah komentar (default 1000), urutan, format output, dsb, dengan menu konfigurasi interaktif
- **Manajemen API Key**: Input manual, import dari file/env, dan penyimpanan otomatis
- **Export Multi-Format**: Output ke Excel, CSV, atau JSON, dengan nama file otomatis dan simpan konfigurasi
- **Analisis Sentiment & Statistik**: Dukungan TextBlob (opsional), word count, link/mention detection, dsb
- **Error Handling & Diagnostik**: Penanganan error API, quota, validasi key, dsb
- **Progress & Ringkasan**: Statistik crawling real-time dan ringkasan hasil

## 📋 Persyaratan Sistem

### Python dan Dependencies

- Python 3.7 atau lebih baru
- Libraries yang diperlukan (lihat `requirements.txt`)

### YouTube Data API v3

1. Google Cloud Console account
2. YouTube Data API v3 yang sudah diaktifkan
3. API Key yang valid

### Sistem Operasi

- Windows (dengan PowerShell atau CMD)
- Linux/macOS (kompatibel)

## 🔧 Instalasi

### 1. Clone atau Download Repository

```bash

git clone https://github.com/ferdianwijayabangkit/crawl-youtube-comments-py.git
cd crawl-youtube-comments-py

```

Atau download ZIP dan extract ke folder pilihan Anda.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup YouTube Data API v3

1. **Buka Google Cloud Console**
   - Kunjungi: <https://console.cloud.google.com/>

2. **Buat Project Baru atau Pilih Project Existing**
   - Klik dropdown project di top bar
   - Create new project atau pilih existing

3. **Aktifkan YouTube Data API v3**
   - Buka: APIs & Services → Library
   - Cari "YouTube Data API v3"
   - Klik "Enable"

4. **Buat API Key**
   - Buka: APIs & Services → Credentials
   - Klik "Create Credentials" → "API Key"
   - Copy API Key yang dihasilkan

5. **Konfigurasi API Key (Opsional)**
   - Edit API Key untuk mengatur restrictions
   - Untuk testing, bisa set "Application restrictions" ke "None"

## 🎯 Cara Penggunaan

### Metode 1: Jalankan Langsung

```bash
python youtube_comments_crawler.py
```

### Metode 2: Dengan API Key Parameter

```bash
# Ganti YOUR_API_KEY_HERE dengan kunci API asli Anda
python youtube_comments_crawler.py --api-key YOUR_API_KEY_HERE
```

### Metode 3: Menggunakan Environment Variable

**Windows (PowerShell):**

```powershell
$env:YOUTUBE_API_KEY="YOUR_API_KEY_HERE"
python youtube_comments_crawler.py
```

**Windows (CMD):**

```cmd
set YOUTUBE_API_KEY=YOUR_API_KEY_HERE
python youtube_comments_crawler.py
```

**Linux/macOS:**

```bash
export YOUTUBE_API_KEY="YOUR_API_KEY_HERE"
python youtube_comments_crawler.py
```

## 📖 Panduan Step-by-Step

### Step 1: Setup API Key

Program akan mencari API key dengan urutan:

1. Environment variable `YOUTUBE_API_KEY`
2. File konfigurasi (`config.ini`, `api_key.txt`, `.env`)
3. Input manual secara interaktif (bisa kembali/back/exit di menu input)

### Step 2: Input Video URLs

Pilih salah satu metode input (semua input tervalidasi, bisa kembali/back/exit):

- Input manual satu per satu (ketik 'done' untuk selesai)
- Paste multiple URLs sekaligus (Enter 2x untuk selesai)
- File Excel (kolom URL otomatis terdeteksi, support .xlsx/.xls)
- File .txt (URL per baris, support komentar dengan #)

### Step 3: Konfigurasi Crawling

Atur parameter sesuai kebutuhan melalui menu interaktif:

- Max komentar per video (default 1000, bisa diubah)
- Include replies atau tidak
- Urutan komentar (relevance/time)
- Format output (excel/csv/json)

### Step 4: Mulai Crawling

- Konfirmasi pengaturan
- Proses crawling dimulai
- Monitor progress real-time dan statistik

## 📁 Format Input File

### Excel File Format

```markdown
| youtube_url                                    |
|------------------------------------------------|
| https://www.youtube.com/watch?v=dQw4w9WgXcQ   |
| https://youtu.be/6e-I3c4w_3E                  |
| https://www.youtube.com/watch?v=kJQP7kiw5Fk   |
```

### Text File Format

```text
# Contoh isi file input (urls.txt)
# Anda bisa menggunakan link video YouTube yang asli
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/6e-I3c4w_3E
https://www.youtube.com/watch?v=kJQP7kiw5Fk

# Comments starting with # are ignored
```

### Config File Format (config.ini)

```ini
[youtube]
api_key = YOUR_API_KEY_HERE
save_date = 2025-07-29T10:30:00
```

## 📊 Output Data

### Kolom Data yang Dikumpulkan

- **Atribut yang dikumpulkan sangat lengkap, antara lain:**
  - `comment_text`: Isi komentar
  - `author_name`: Nama pembuat komentar
  - `author_channel_id`, `author_channel_url`, `author_profile_image_url`
  - `author_is_verified`, `author_is_channel_owner`, `author_is_sponsor`
  - `is_liked_by_creator`, `is_hearted_by_creator`, `is_pinned_by_creator`
  - `publish_date`, `updated_at`, `like_count`, `reply_count`, `parent_id` (untuk reply)
  - `video_id`, `video_title`, `video_url`, `video_channel_id`, `video_channel_title`
  - `word_count`, `has_links`, `has_mentions`, `sentiment_score` (opsional)
  - `crawl_timestamp`, `comment_type` (main/reply)
  - ...dan atribut lain sesuai update API terbaru

Semua atribut ini otomatis tersedia di file output (Excel/CSV/JSON).

### Format Output

- **Excel (.xlsx)**: Recommended untuk analisis data
- **CSV (.csv)**: Kompatibel dengan berbagai tools
- **JSON (.json)**: Untuk integrasi dengan aplikasi lain

## ⚙️ Konfigurasi Lanjutan

### File Konfigurasi

Anda bisa membuat file `config.ini` untuk pengaturan default:

```ini
[youtube]
api_key = YOUR_API_KEY_HERE

[crawling]
max_comments_per_video = 100
include_replies = true
comment_order = relevance

[output]
format = excel
include_timestamp = true
filename_prefix = youtube_comments
```

### Environment Variables

```bash
YOUTUBE_API_KEY=YOUR_API_KEY_HERE
```

## 🔍 Troubleshooting

### Error: API Key Tidak Valid / Quota Habis / API Not Enabled

Semua error API, quota, dan validasi key dideteksi otomatis. Program akan memberikan solusi dan diagnostik di terminal. Jika error:

1. Periksa kembali API key di Google Cloud Console
2. Pastikan YouTube Data API v3 sudah enabled
3. Cek application restrictions pada API key
4. Cek quota dan status billing
5. Jika error lain, baca pesan di terminal (ada saran otomatis)

## 🎓 Penggunaan untuk Penelitian

### Best Practices

1. **Ethical Usage**: Gunakan sesuai dengan YouTube Terms of Service
2. **Rate Limiting**: Program sudah include delay untuk menghormati API limits
3. **Data Privacy**: Jangan simpan data personal yang sensitif
4. **Academic Purpose**: Gunakan hanya untuk keperluan penelitian yang legitimate

### Contoh Use Cases

- Analisis sentiment terhadap video edukasi
- Studi pola interaksi pada konten politik
- Research engagement pada video marketing
- Analisis bahasa dan komunikasi digital

## 📈 Monitoring dan Statistik

Program menyediakan real-time monitoring:

- Progress crawling (%)
- Jumlah video diproses
- Total komentar berhasil dikumpulkan
- Jumlah API calls yang digunakan
- Rate crawling (komentar per menit)
- Error handling dan diagnostic

## 🔄 Update dan Maintenance

### Check for Updates

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Backup Data

- Simpan file output di lokasi aman
- Backup file konfigurasi
- Export pengaturan sebelum update

## 📝 Changelog

### Version 1.1.0 (2025-07-30)

- Menu interaktif dengan validasi input & fitur back/exit di semua langkah
- Input API key fleksibel (manual, file, env, auto-save)
- Input URL video: manual, batch, Excel, txt, validasi otomatis
- Konfigurasi crawling lengkap (jumlah komentar default 1000, urutan, format output, dsb)
- Ekstraksi atribut YouTube API sangat lengkap (status, author, like, heart, dsb)
- Output multi-format (Excel, CSV, JSON) dengan nama file otomatis
- Statistik & progress crawling real-time
- Diagnostik error API, quota, validasi key otomatis
- Dokumentasi & template diperbarui

### Version 1.0.0 (2025-07-29)

- Initial release
- Interactive terminal interface
- Multiple input methods support
- Flexible configuration system
- Multi-format output support
- Comprehensive error handling
- Real-time progress monitoring

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 📞 Support

Jika mengalami masalah:

1. **Check dokumentasi** ini terlebih dahulu
2. **Search existing issues** di GitHub
3. **Create new issue** dengan detail error
4. **Include log output** untuk debugging

## ⚠️ Disclaimer

Tool ini dibuat untuk keperluan penelitian akademik. Pastikan penggunaan sesuai dengan:

- YouTube Terms of Service
- Google API Terms of Service
- Ketentuan ethical research
- Regulasi privasi data yang berlaku

## �‍💻 Author & Credits

**Developed by:** [Ferdian Bangkit Wijaya](https://github.com/ferdianwijayabangkit)  
**Institution:** Universitas Sultan Ageng Tirtayasa (UNTIRTA)  
**Version:** 1.0.0  
**Date:** 29 Juli 2025  

Original Jupyter Notebook concept adapted and enhanced for terminal-based usage

## �🙏 Acknowledgments

- **Ferdian Bangkit Wijaya** - Original concept and notebook development
- **Universitas Sultan Ageng Tirtayasa** - Academic support and research context
- YouTube Data API v3 documentation
- Google Cloud Platform
- Pandas dan Python community
- Open source contributors

---

Happy Researching! 🎓✨

© 2025 Ferdian Bangkit Wijaya - Universitas Sultan Ageng Tirtayasa
