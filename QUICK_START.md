# 🚀 Quick Start Guide - YouTube Comments Crawler

## 📋 Persiapan Cepat (5 menit)

### 1. Setup Environment

```cmd
# Install dependencies
pip install -r requirements.txt

# Atau jalankan setup script
# Di Windows:
setup.bat

# Di macOS/Linux:
chmod +x setup.sh
./setup.sh
```

### 2. Dapatkan API Key YouTube

1. Buka: <https://console.cloud.google.com/>
2. Buat project baru atau pilih existing
3. Enable "YouTube Data API v3"
4. Buat API Key di Credentials
5. Copy API Key

> **Tip**: Butuh panduan lebih detail? Lihat README.md

### 3. Jalankan Crawler

```cmd
# Method 1: Double click
# Di Windows:
run.bat

# Di macOS/Linux:
chmod +x run.sh
./run.sh

# Method 2: Command line
python youtube_comments_crawler.py

# Method 3: Dengan API key
# Ganti YOUR_API_KEY dengan kunci API asli Anda
python youtube_comments_crawler.py --api-key YOUR_API_KEY
```

## 🎯 Workflow Cepat

1. **Input API Key** (pilih salah satu):
   - Set environment: `set YOUTUBE_API_KEY=your_key`
   - Input manual saat program jalan
   - Simpan di file `config.ini`

2. **Input Video URLs** (pilih salah satu):
   - Manual: ketik URL satu per satu
   - Batch: paste multiple URLs
   - Excel: gunakan `youtube_urls_template.xlsx`
   - Text: gunakan `youtube_urls_template.txt`

3. **Konfigurasi** (opsional):
   - Max comments per video
   - Include replies
   - Output format (Excel/CSV/JSON)

4. **Start Crawling**:
   - Confirm settings
   - Monitor progress
   - Wait for completion

5. **Results**:
   - File otomatis tersimpan
   - Format: `youtube_comments_YYYYMMDD_HHMMSS.xlsx`

## 🔧 Tips Cepat

### Untuk Penelitian Akademik

- Set max comments: 500-1000 per video
- Enable replies untuk data lengkap
- Gunakan format Excel untuk analisis

### Untuk Testing

- Set max comments: 10-50 per video
- Disable replies untuk speed
- Test dengan 1-2 video dulu

### Error Handling

- API Key error: cek di Google Cloud Console
- Quota exceeded: tunggu 24 jam atau ganti API key
- Video private: skip dan lanjut video berikutnya

## 📊 Contoh Output Data

| comment_text | author_name | like_count | video_title | sentiment_score |
|--------------|-------------|------------|-------------|-----------------|
| Great video! | John Doe    | 5          | How to Code | 0.8             |
| Thanks for sharing | Jane    | 2          | How to Code | 0.6             |

## 🎓 Best Practices

1. **Start Small**: Test dengan 1-2 video dulu
2. **Check Quota**: Monitor API usage
3. **Backup Results**: Save files secara berkala
4. **Ethical Use**: Ikuti YouTube ToS
5. **Data Privacy**: Jangan share data personal

## 🚨 Troubleshooting Cepat

**API Error 403**: API key restricted → Set restrictions ke "None"
**API Error 400**: API key invalid → Check dan copy ulang
**Quota Exceeded**: Wait 24h atau gunakan API key lain
**No Comments**: Video private atau comments disabled

---

**Need Help?** Baca `README.md` untuk dokumentasi lengkap!
