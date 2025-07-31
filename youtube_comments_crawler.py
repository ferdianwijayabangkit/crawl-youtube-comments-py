#!/usr/bin/env python3
"""
YouTube Comments Crawler - Interactive Terminal Version
=====================================================

Sistem crawling komentar YouTube yang dapat dijalankan di terminal CMD secara interaktif.
Dirancang untuk keperluan penelitian akademik dan analisis data.

Original Jupyter Notebook concept by Ferdian Bangkit Wijaya
Adapted and enhanced for terminal-based usage

Author: Ferdian Bangkit Wijaya
Institution: Universitas Sultan Ageng Tirtayasa (UNTIRTA)
Version: 1.0.0
Date: July 2025

© 2025 Ferdian Bangkit Wijaya - Universitas Sultan Ageng Tirtayasa
"""

import os
import sys
import re
import json
import time
import pandas as pd
from datetime import datetime
from pathlib import Path
import configparser
from typing import List, Dict, Optional, Tuple
import argparse

# YouTube API imports
try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Error: google-api-python-client tidak terinstall!")
    print("💡 Jalankan: pip install google-api-python-client")
    sys.exit(1)

# Optional imports for enhanced features
try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except ImportError:
    HAS_TEXTBLOB = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class YouTubeCommentsCrawler:
    """Main class untuk crawling komentar YouTube"""
    
    def __init__(self):
        """Initialize crawler dengan konfigurasi default"""
        self.api_key = None
        self.youtube_service = None
        self.config = self.load_default_config()
        self.results = []
        self.stats = {
            'total_videos': 0,
            'processed_videos': 0,
            'total_comments': 0,
            'total_replies': 0,
            'api_calls': 0,
            'start_time': None,
            'errors': []
        }
        
    def load_default_config(self) -> Dict:
        """Load konfigurasi default untuk crawling"""
        return {
            'max_comments_per_video': 1000,
            'include_replies': True,
            'comment_order': 'relevance',  # relevance, time
            'attributes': {
                'comment_text': True,
                'author_name': True,
                'author_channel_id': True,
                'author_channel_url': True,
                'author_profile_image_url': True,
                'author_is_verified': True,
                'author_is_channel_owner': True,
                'author_is_sponsor': True,
                'is_liked_by_creator': True,
                'is_hearted_by_creator': True,
                'is_pinned': True,
                'publish_date': True,
                'updated_at': True,
                'like_count': True,
                'reply_count': True,
                'parent_id': True,
                'word_count': True,
                'has_links': True,
                'has_mentions': True,
                'sentiment_score': HAS_TEXTBLOB,
                'video_title': True,
                'video_id': True,
                'video_url': True,
                'channel_id': True,
                'channel_title': True,
                'crawl_timestamp': True
            },
            'output': {
                'format': 'excel',  # excel, csv, json
                'filename_prefix': 'youtube_comments',
                'include_timestamp': True,
                'save_config': True
            },
            'delays': {
                'between_videos': 1.0,
                'between_requests': 0.1
            }
        }
    
    def setup_api_key(self) -> bool:
        """Setup API key dengan pilihan input manual atau import dari file/env"""
        print("\n🔐 KONFIGURASI YOUTUBE API KEY")
        print("=" * 50)
        print("Pilih metode input API key:")
        print("  1. Ketik manual di terminal (default)")
        print("  2. Import otomatis dari file konfigurasi/env (api_key.txt, config.ini, .env, environment variable)")
        print("  0. Batal")
        allowed_choices = ['1', '2', '0']
        while True:
            try:
                pilihan = input("\nPilih metode (1/2, 0 untuk batal): ").strip().lower()
                if pilihan == '':
                    pilihan = '1'
                if pilihan not in allowed_choices:
                    print("❌ Pilihan tidak valid! Pilih 1 (manual), 2 (import), atau 0 (batal).")
                    continue
                if pilihan == '1':
                    # Input manual
                    while True:
                        print("\n📝 Input API Key secara manual:")
                        print("💡 Anda bisa mendapatkan API key dari:")
                        print("   https://console.cloud.google.com/apis/credentials")
                        print("💡 Ketik 'back' atau 'b' untuk kembali ke menu sebelumnya (pilihan metode input API key)")
                        try:
                            api_key = input("\n🔑 Masukkan YouTube Data API v3 Key: ").strip()
                            if not api_key:
                                print("❌ API key tidak boleh kosong!")
                                continue
                            if api_key.lower() in ['exit', 'quit', 'q', 'batal', '0']:
                                print("❌ Dibatalkan oleh user")
                                return False
                            if api_key.lower() in ['back', 'kembali', 'b']:
                                print("↩️ Kembali ke menu pemilihan metode input API key.")
                                # Tampilkan ulang menu metode input API key
                                print("\nPilih metode input API key:")
                                print("  1. Ketik manual di terminal (default)")
                                print("  2. Import otomatis dari file konfigurasi/env (api_key.txt, config.ini, .env, environment variable)")
                                print("  0. Batal")
                                break
                            if self.validate_api_key(api_key):
                                self.api_key = api_key
                                while True:
                                    save_choice = input("\n💾 Simpan API key untuk penggunaan berikutnya? (y/n): ").strip().lower()
                                    if save_choice not in ['y', 'yes', 'ya', 'n', 'no', 'tidak', '']:
                                        print("❌ Pilihan tidak valid! Jawab y/n.")
                                        continue
                                    if save_choice in ['y', 'yes', 'ya']:
                                        self.save_api_key_to_config(api_key)
                                        print("✅ API key berhasil disimpan ke file konfigurasi")
                                    break
                                return True
                            else:
                                print("❌ API key tidak valid! Silakan coba lagi.")
                        except KeyboardInterrupt:
                            print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 'exit', 'back', atau '0' untuk membatalkan/kembali.")
                            continue
                elif pilihan == '2':
                    # Import dari file/env
                    env_key = os.getenv('YOUTUBE_API_KEY')
                    config_key = self.load_api_key_from_config()
                    if env_key and env_key != 'YOUR_API_KEY_HERE':
                        print("✅ Ditemukan API key dari environment variable")
                        if self.validate_api_key(env_key):
                            self.api_key = env_key
                            return True
                    elif config_key:
                        print("✅ Ditemukan API key dari file konfigurasi")
                        if self.validate_api_key(config_key):
                            self.api_key = config_key
                            return True
                    print("❌ Tidak ditemukan API key di file/env. Silakan input manual.")
                elif pilihan == '0':
                    print("❌ Setup API key dibatalkan oleh user.")
                    return False
            except KeyboardInterrupt:
                print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 0 (batal) sesuai menu.")
                continue
            except Exception as e:
                print(f"❌ Error: {e}")
        return False
    
    def load_api_key_from_config(self) -> Optional[str]:
        """Load API key dari file konfigurasi"""
        config_files = ['api_key.txt', 'config.ini', '.env']
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    if config_file.endswith('.txt'):
                        with open(config_file, 'r') as f:
                            key = f.read().strip()
                            if key and key != 'YOUR_API_KEY_HERE':
                                return key
                    elif config_file.endswith('.ini'):
                        config = configparser.ConfigParser()
                        config.read(config_file)
                        if 'youtube' in config and 'api_key' in config['youtube']:
                            key = config['youtube']['api_key'].strip()
                            if key and key != 'YOUR_API_KEY_HERE':
                                return key
                    elif config_file.endswith('.env'):
                        with open(config_file, 'r') as f:
                            for line in f:
                                if line.startswith('YOUTUBE_API_KEY='):
                                    key = line.split('=', 1)[1].strip().strip('"\'')
                                    if key and key != 'YOUR_API_KEY_HERE':
                                        return key
                except Exception as e:
                    print(f"⚠️ Error membaca {config_file}: {e}")
                    
        return None
    
    def save_api_key_to_config(self, api_key: str):
        """Simpan API key ke file konfigurasi"""
        try:
            config = configparser.ConfigParser()
            if os.path.exists('config.ini'):
                config.read('config.ini')
            
            if 'youtube' not in config:
                config.add_section('youtube')
                
            config['youtube']['api_key'] = api_key
            config['youtube']['save_date'] = datetime.now().isoformat()
            
            with open('config.ini', 'w') as f:
                config.write(f)
                
        except Exception as e:
            print(f"⚠️ Error menyimpan konfigurasi: {e}")
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validasi API key dengan test request"""
        if not api_key or len(api_key) < 30:
            return False
            
        try:
            print("🔍 Validating API key...")
            youtube = build('youtube', 'v3', developerKey=api_key)
            
            # Test request
            request = youtube.channels().list(
                part="snippet",
                forUsername="YouTube"
            )
            response = request.execute()
            
            print("✅ API key valid!")
            self.youtube_service = youtube
            return True
            
        except HttpError as e:
            print(f"❌ HTTP Error: {e}")
            self.diagnose_api_error(str(e))
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def diagnose_api_error(self, error_message: str):
        """Diagnosa error API key dan berikan solusi"""
        error_str = error_message.lower()
        
        print("\n🔍 DIAGNOSA ERROR:")
        print("-" * 30)
        
        if "403" in error_str or "forbidden" in error_str:
            print("❌ MASALAH: API Key Restricted")
            print("📋 SOLUSI:")
            print("   1. Buka Google Cloud Console")
            print("   2. Edit API Key → Application restrictions → Pilih 'None'")
            print("   3. Save dan coba lagi")
            
        elif "400" in error_str or "invalid" in error_str:
            print("❌ MASALAH: API Key Tidak Valid")
            print("📋 SOLUSI:")
            print("   1. Periksa kembali API Key")
            print("   2. Pastikan tidak ada spasi di awal/akhir")
            print("   3. Buat API Key baru jika perlu")
            
        elif "quota" in error_str:
            print("❌ MASALAH: Quota API Habis")
            print("📋 SOLUSI:")
            print("   1. Tunggu sampai besok (quota reset)")
            print("   2. Gunakan API Key dari project lain")
            
        elif "not enabled" in error_str:
            print("❌ MASALAH: YouTube Data API v3 Belum Aktif")
            print("📋 SOLUSI:")
            print("   1. Buka Google Cloud Console")
            print("   2. APIs & Services → Library")
            print("   3. Cari 'YouTube Data API v3' → Enable")
    
    def get_video_urls(self) -> List[str] | str:
        """Get daftar URL video dengan berbagai metode input"""
        print("\n📺 INPUT VIDEO YOUTUBE")
        print("=" * 40)
        print("💡 Metode input yang tersedia:")
        print("   1. Input manual satu per satu")
        print("   2. Input multiple URLs (pisahkan dengan enter)")
        print("   3. Load dari file Excel")
        print("   4. Load dari file txt")
        print("   0. Exit (keluar dari menu input)")
        print("   b. Back (kembali ke menu sebelumnya jika ada)")
        allowed_choices = ['1', '2', '3', '4', '0', 'b']
        while True:
            try:
                choice = input("\nPilih metode (1-4, 0 untuk exit, b untuk kembali): ").strip().lower()
                if choice not in allowed_choices:
                    print("❌ Pilihan tidak valid! Hanya boleh 1-4, 0 untuk exit, atau b untuk kembali.")
                    continue
                if choice == '0':
                    print("❌ Dibatalkan oleh user dari menu input video.")
                    return []
                elif choice == 'b':
                    # Hanya print jika kembali ke menu input video, bukan ke API key
                    return "__BACK_TO_API_KEY__"
                elif choice == '1':
                    result = self.input_urls_manual()
                    if result is None:
                        continue
                    return result
                elif choice == '2':
                    result = self.input_urls_multiple()
                    if result is None:
                        continue
                    return result
                elif choice == '3':
                    result = self.load_urls_from_excel()
                    if result is None:
                        continue
                    return result
                elif choice == '4':
                    result = self.load_urls_from_txt()
                    if result is None:
                        continue
                    return result
            except KeyboardInterrupt:
                print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 0 (exit) atau b (back) sesuai menu.")
                continue
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def input_urls_manual(self) -> List[str] | None:
        """Input URLs secara manual satu per satu"""
        urls = []
        print("\n📝 Input URL YouTube satu per satu")
        print("💡 Ketik 'done' atau 'selesai' untuk finish")
        print("💡 Ketik 'quit', 'exit', atau 'batal' untuk keluar dari menu ini")
        print("💡 Ketik 'back' atau 'kembali' untuk kembali ke menu utama input video")
        allowed_special = ['done', 'selesai', 'finish', 'quit', 'exit', 'batal', '0', 'back', 'kembali', 'b']
        while True:
            try:
                url = input(f"\nURL #{len(urls)+1}: ").strip()
                if url.lower() not in allowed_special and not url:
                    continue
                if url.lower() in ['done', 'selesai', 'finish']:
                    break
                elif url.lower() in ['quit', 'exit', 'batal', '0']:
                    print("❌ Dibatalkan oleh user dari input manual.")
                    return []
                elif url.lower() in ['back', 'kembali', 'b']:
                    print("↩️ Kembali ke menu utama input video.")
                    return self.get_video_urls()
                elif url.lower() not in allowed_special:
                    video_id = self.extract_video_id(url)
                    if video_id:
                        urls.append(url)
                        print(f"✅ URL valid ditambahkan (Video ID: {video_id})")
                    else:
                        print("❌ URL tidak valid! Format yang didukung:")
                        print("   - https://www.youtube.com/watch?v=VIDEO_ID")
                        print("   - https://youtu.be/VIDEO_ID")
                else:
                    print("❌ Pilihan tidak valid! Ketik URL, 'done', 'exit', 'back', atau sesuai petunjuk.")
            except KeyboardInterrupt:
                print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 'exit', 'back', atau '0' untuk membatalkan/kembali.")
                continue
        return urls
    
    def input_urls_multiple(self) -> List[str] | None:
        """Input multiple URLs sekaligus"""
        print("\n📝 Input multiple URLs")
        print("💡 Paste URLs (satu per baris), tekan Enter 2x untuk selesai")
        print("💡 Ketik 'quit', 'exit', atau 'batal' di baris manapun untuk keluar dari menu ini")
        print("💡 Ketik 'back' atau 'kembali' di baris manapun untuk kembali ke menu utama input video")
        urls = []
        lines = []
        allowed_special = ['quit', 'exit', 'batal', '0', 'back', 'kembali', 'b']
        try:
            while True:
                line = input().strip()
                if line.lower() in allowed_special:
                    if line.lower() in ['quit', 'exit', 'batal', '0']:
                        print("❌ Dibatalkan oleh user dari input multiple URLs.")
                        return []
                    if line.lower() in ['back', 'kembali', 'b']:
                        print("↩️ Kembali ke menu utama input video.")
                        return self.get_video_urls()
                elif not line:
                    if lines:  # Empty line after some input
                        break
                    continue
                elif re.match(r'https?://|[a-zA-Z0-9_-]{11}', line):
                    lines.append(line)
                else:
                    print("❌ Pilihan tidak valid! Ketik URL, 'exit', 'back', atau sesuai petunjuk.")
            for line in lines:
                # Handle multiple URLs in one line
                potential_urls = re.findall(r'https?://[^\s]+', line)
                if not potential_urls:
                    potential_urls = [line]  # Maybe just video ID
                for url in potential_urls:
                    video_id = self.extract_video_id(url)
                    if video_id:
                        urls.append(url)
                        print(f"✅ URL valid: {url}")
                    else:
                        print(f"❌ URL tidak valid: {url}")
        except KeyboardInterrupt:
            print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 'exit', 'back', atau '0' sesuai menu.")
            return self.input_urls_multiple()
        return urls
    
    def load_urls_from_excel(self) -> List[str] | None:
        """Load URLs dari file Excel
        
        Petunjuk:
        - Pastikan file Excel sudah ada di folder ini, misal: youtube_urls_template.xlsx
        - Minimal ada satu kolom yang berisi URL video YouTube.
        - Jika belum ada, buat file template terlebih dahulu.
        - Jalankan dengan memilih opsi 3 pada menu input.
        - Ketik 'quit', 'exit', atau 'batal' di input manapun untuk keluar dari menu ini.
        """
        print("\n📊 Load URLs dari file Excel")
        print("💡 Pastikan file template Excel sudah ada di folder ini (misal: youtube_urls_template.xlsx)")
        print("💡 File harus memiliki kolom berisi URL video YouTube!")
        print("💡 Ketik 'quit', 'exit', atau 'batal' di input manapun untuk keluar dari menu ini")
        print("💡 Ketik 'back' atau 'kembali' di input manapun untuk kembali ke menu utama input video")
        allowed_special = ['quit', 'exit', 'batal', '0', 'back', 'kembali', 'b']
        # Find Excel files
        excel_files = list(Path('.').glob('*.xlsx')) + list(Path('.').glob('*.xls'))
        if excel_files:
            print("\n📋 File Excel yang ditemukan:")
            for i, file in enumerate(excel_files, 1):
                print(f"   {i}. {file.name}")
            print(f"   {len(excel_files)+1}. Input path manual")
            while True:
                try:
                    choice = input(f"\nPilih file (1-{len(excel_files)+1}): ").strip().lower()
                    if choice in allowed_special:
                        if choice in ['quit', 'exit', 'batal', '0']:
                            print("❌ Dibatalkan oleh user dari menu Excel.")
                            return []
                        if choice in ['back', 'kembali', 'b']:
                            print("↩️ Kembali ke menu utama input video.")
                            return self.get_video_urls()
                    elif choice.isdigit() and 1 <= int(choice) <= len(excel_files):
                        filename = excel_files[int(choice)-1]
                        break
                    elif choice == str(len(excel_files)+1):
                        filename = input("Masukkan path file Excel: ").strip()
                        if filename.lower() in allowed_special:
                            if filename.lower() in ['quit', 'exit', 'batal', '0']:
                                print("❌ Dibatalkan oleh user dari menu Excel.")
                                return []
                            if filename.lower() in ['back', 'kembali', 'b']:
                                print("↩️ Kembali ke menu utama input video.")
                                return self.get_video_urls()
                        break
                    else:
                        print("❌ Pilihan tidak valid! Pilih nomor file atau input path manual.")
                except KeyboardInterrupt:
                    print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 'exit', 'back', atau '0' sesuai menu.")
                    continue
        else:
            print("⚠️ Tidak ada file Excel ditemukan! Buat file template terlebih dahulu.")
            while True:
                filename = input("Masukkan path file Excel: ").strip()
                if filename.lower() in allowed_special:
                    if filename.lower() in ['quit', 'exit', 'batal', '0']:
                        print("❌ Dibatalkan oleh user dari menu Excel.")
                        return []
                    if filename.lower() in ['back', 'kembali', 'b']:
                        print("↩️ Kembali ke menu utama input video.")
                        return self.get_video_urls()
                elif filename:
                    break
                else:
                    print("❌ Pilihan tidak valid! Input path file atau exit/back.")
        try:
            # Try to read Excel file
            df = pd.read_excel(filename)
            print(f"✅ File berhasil dibaca: {len(df)} baris")
            print(f"📋 Kolom yang tersedia: {list(df.columns)}")
            # Find URL column
            url_column = None
            for col in df.columns:
                col_str = str(col).lower()
                if any(keyword in col_str for keyword in ['url', 'youtube', 'link']):
                    url_column = col
                    break
            if not url_column:
                print("\n📋 Pilih kolom yang berisi URL:")
                for i, col in enumerate(df.columns, 1):
                    print(f"   {i}. {col}")
                while True:
                    try:
                        choice = input("Pilih kolom: ").strip().lower()
                        if choice in allowed_special:
                            if choice in ['quit', 'exit', 'batal', '0']:
                                print("❌ Dibatalkan oleh user dari menu Excel.")
                                return []
                            if choice in ['back', 'kembali', 'b']:
                                print("↩️ Kembali ke menu utama input video.")
                                return self.get_video_urls()
                        elif choice.isdigit() and 1 <= int(choice) <= len(df.columns):
                            url_column = df.columns[int(choice)-1]
                            break
                        else:
                            print("❌ Pilihan tidak valid! Pilih nomor kolom atau exit/back.")
                    except KeyboardInterrupt:
                        print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 'exit', 'back', atau '0' sesuai menu.")
                        continue
            # Extract URLs
            urls = []
            for idx, value in df[url_column].items():
                if pd.notna(value) and str(value).strip():
                    url = str(value).strip()
                    video_id = self.extract_video_id(url)
                    if video_id:
                        urls.append(url)
            print(f"✅ Berhasil memuat {len(urls)} URL valid dari {len(df)} baris")
            return urls
        except Exception as e:
            print(f"❌ Error membaca file Excel: {e}")
            return []
    
    def load_urls_from_txt(self) -> List[str] | None:
        """Load URLs dari file text
        
        Petunjuk:
        - Pastikan file txt sudah ada di folder ini, misal: youtube_urls_template.txt
        - Satu baris satu URL video YouTube.
        - Jika belum ada, buat file template terlebih dahulu.
        - Jalankan dengan memilih opsi 4 pada menu input.
        - Ketik 'quit', 'exit', atau 'batal' di input manapun untuk keluar dari menu ini.
        """
        print("\n📄 Load URLs dari file text")
        print("💡 Pastikan file template txt sudah ada di folder ini (misal: youtube_urls_template.txt)")
        print("💡 Satu baris satu URL video YouTube!")
        print("💡 Ketik 'quit', 'exit', atau 'batal' di input manapun untuk keluar dari menu ini")
        print("💡 Ketik 'back' atau 'kembali' di input manapun untuk kembali ke menu utama input video")
        allowed_special = ['quit', 'exit', 'batal', '0', 'back', 'kembali', 'b']
        while True:
            filename = input("Masukkan path file text: ").strip()
            if filename.lower() in allowed_special:
                if filename.lower() in ['quit', 'exit', 'batal', '0']:
                    print("❌ Dibatalkan oleh user dari menu TXT.")
                    return []
                if filename.lower() in ['back', 'kembali', 'b']:
                    print("↩️ Kembali ke menu utama input video.")
                    return self.get_video_urls()
            elif filename:
                break
            else:
                print("❌ Pilihan tidak valid! Input path file atau exit/back.")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            urls = []
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if line.lower() in allowed_special:
                    if line.lower() in ['quit', 'exit', 'batal', '0']:
                        print("❌ Dibatalkan oleh user dari menu TXT.")
                        return []
                    if line.lower() in ['back', 'kembali', 'b']:
                        print("↩️ Kembali ke menu utama input video.")
                        return self.get_video_urls()
                elif line and not line.startswith('#'):
                    video_id = self.extract_video_id(line)
                    if video_id:
                        urls.append(line)
                    else:
                        print(f"⚠️ Line {line_num}: URL tidak valid - {line}")
                elif not line:
                    continue
                else:
                    print(f"❌ Line {line_num}: Input tidak valid! Ketik URL, 'exit', 'back', atau sesuai petunjuk.")
            print(f"✅ Berhasil memuat {len(urls)} URL valid dari {len(lines)} baris")
            return urls
        except Exception as e:
            print(f"❌ Error membaca file: {e}")
            print("⚠️ Pastikan file template sudah ada dan formatnya benar!")
            return []
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID dari berbagai format YouTube URL"""
        if not url:
            return None
            
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
            r'^([a-zA-Z0-9_-]{11})$'  # Just video ID
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
                
        return None
    
    def configure_crawling(self):
        """Konfigurasi parameter crawling secara interaktif"""
        print("\n⚙️ KONFIGURASI CRAWLING")
        print("=" * 40)
        allowed_special = ['back', 'b', 'exit', 'quit', 'kembali', 'batal']
        cancelled = False
        # Max comments per video
        default_max_comments = 1000
        while True:
            try:
                prompt_val = default_max_comments
                max_comments = input(f"Max komentar per video [{prompt_val}]: ").strip().lower()
                if max_comments in allowed_special:
                    print("↩️ Kembali/batal dari konfigurasi crawling.")
                    cancelled = True
                    return "__BACK_TO_INPUT_VIDEO__"
                if not max_comments:
                    self.config['max_comments_per_video'] = default_max_comments
                    break
                try:
                    max_comments_int = int(max_comments)
                    if max_comments_int > 0:
                        self.config['max_comments_per_video'] = max_comments_int
                        break
                    else:
                        print("❌ Harus lebih dari 0")
                except ValueError:
                    print("❌ Harus berupa angka atau ketik 'back' untuk kembali.")
            except KeyboardInterrupt:
                print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 'back', 'exit', atau '0' untuk kembali/batal.")
                continue
        # Include replies
        while not cancelled:
            try:
                include_replies = input(f"Include replies? (y/n) [{'y' if self.config['include_replies'] else 'n'}]: ").strip().lower()
                if include_replies in allowed_special:
                    print("↩️ Kembali/batal dari konfigurasi crawling.")
                    cancelled = True
                    return "__BACK_TO_INPUT_VIDEO__"
                if not include_replies:
                    break
                if include_replies in ['y', 'yes', 'ya']:
                    self.config['include_replies'] = True
                    break
                elif include_replies in ['n', 'no', 'tidak']:
                    self.config['include_replies'] = False
                    break
                else:
                    print("❌ Jawab y/n atau ketik 'back' untuk kembali.")
            except KeyboardInterrupt:
                print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 'back', 'exit', atau '0' untuk kembali/batal.")
                continue
        # Comment order
        while not cancelled:
            try:
                order = input("Urutan komentar (relevance/time) [relevance]: ").strip().lower()
                if order in allowed_special:
                    print("↩️ Kembali/batal dari konfigurasi crawling.")
                    cancelled = True
                    return "__BACK_TO_INPUT_VIDEO__"
                if not order:
                    break
                if order in ['relevance', 'time']:
                    self.config['comment_order'] = order
                    break
                else:
                    print("❌ Pilih 'relevance' atau 'time', atau ketik 'back' untuk kembali.")
            except KeyboardInterrupt:
                print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 'back', 'exit', atau '0' untuk kembali/batal.")
                continue
        # Output format
        while not cancelled:
            try:
                output_format = input("Format output (excel/csv/json) [excel]: ").strip().lower()
                if output_format in allowed_special:
                    print("↩️ Kembali/batal dari konfigurasi crawling.")
                    cancelled = True
                    return "__BACK_TO_INPUT_VIDEO__"
                if not output_format:
                    break
                if output_format in ['excel', 'csv', 'json']:
                    self.config['output']['format'] = output_format
                    break
                else:
                    print("❌ Pilih 'excel', 'csv', atau 'json', atau ketik 'back' untuk kembali.")
            except KeyboardInterrupt:
                print("\n❌ Tidak bisa keluar dengan Ctrl+C! Gunakan 'back', 'exit', atau '0' untuk kembali/batal.")
                continue
        if not cancelled:
            print("\n✅ Konfigurasi selesai!")
            self.show_config_summary()
    
    def show_config_summary(self):
        """Tampilkan ringkasan konfigurasi"""
        print("\n📋 RINGKASAN KONFIGURASI:")
        print("-" * 30)
        print(f"Max komentar per video: {self.config['max_comments_per_video']}")
        print(f"Include replies: {'Ya' if self.config['include_replies'] else 'Tidak'}")
        print(f"Urutan komentar: {self.config['comment_order']}")
        print(f"Format output: {self.config['output']['format']}")
        
        # Show enabled attributes
        enabled_attrs = [k for k, v in self.config['attributes'].items() if v]
        print(f"Atribut yang akan dikumpulkan: {len(enabled_attrs)} atribut")
        
        for attr in enabled_attrs[:5]:  # Show first 5
            print(f"  ✓ {attr}")
        if len(enabled_attrs) > 5:
            print(f"  ... dan {len(enabled_attrs)-5} lainnya")
    
    def start_crawling(self, video_urls: List[str]):
        """Mulai proses crawling"""
        if not self.youtube_service:
            print("❌ YouTube service belum ready!")
            return
            
        if not video_urls:
            print("❌ Tidak ada URL video untuk diproses!")
            return
        
        print("\n🚀 MEMULAI CRAWLING")
        print("=" * 40)
        
        self.stats['total_videos'] = len(video_urls)
        self.stats['start_time'] = datetime.now()
        
        print(f"📺 Total video: {len(video_urls)}")
        print(f"⚙️ Max komentar per video: {self.config['max_comments_per_video']}")
        print(f"📊 Include replies: {'Ya' if self.config['include_replies'] else 'Tidak'}")
        print("\n🎬 Memulai proses...")
        
        for i, url in enumerate(video_urls, 1):
            try:
                print(f"\n📹 [{i}/{len(video_urls)}] Processing: {url}")
                
                video_id = self.extract_video_id(url)
                if not video_id:
                    print("❌ Video ID tidak valid, skip")
                    continue
                
                # Get video info
                video_info = self.get_video_info(video_id)
                if not video_info:
                    print("❌ Tidak dapat mengambil info video, skip")
                    continue
                
                # Get comments
                comments, api_calls = self.get_video_comments(video_id, video_info)
                
                if comments:
                    self.results.extend(comments)
                    self.stats['total_comments'] += len(comments)
                    self.stats['api_calls'] += api_calls
                    print(f"✅ Berhasil: {len(comments)} komentar")
                else:
                    print("⚠️ Tidak ada komentar ditemukan")
                
                self.stats['processed_videos'] += 1
                
                # Progress update
                progress = (i / len(video_urls)) * 100
                print(f"📊 Progress: {progress:.1f}% ({i}/{len(video_urls)})")
                
                # Delay between videos
                if i < len(video_urls):
                    time.sleep(self.config['delays']['between_videos'])
                    
            except KeyboardInterrupt:
                print("\n⏹️ Crawling dihentikan oleh user")
                break
            except Exception as e:
                print(f"❌ Error processing {url}: {e}")
                self.stats['errors'].append(f"Video {i}: {str(e)}")
                continue
        
        # Final summary
        self.show_crawling_summary()
        
        # Save results
        if self.results:
            self.save_results()
    
    def get_video_info(self, video_id: str) -> Optional[Dict]:
        """Ambil informasi video"""
        try:
            request = self.youtube_service.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                return response['items'][0]
            else:
                return None
                
        except Exception as e:
            print(f"⚠️ Error getting video info: {e}")
            return None
    
    def get_video_comments(self, video_id: str, video_info: Dict) -> Tuple[List[Dict], int]:
        """Ambil komentar dari video"""
        comments = []
        api_calls = 0
        next_page_token = None
        
        try:
            max_total = self.config['max_comments_per_video']
            while len(comments) < max_total:
                # Request comments
                request = self.youtube_service.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=min(100, max_total - len(comments)),
                    order=self.config['comment_order'],
                    pageToken=next_page_token,
                    textFormat='plainText'
                )
                response = request.execute()
                api_calls += 1
                if not response.get('items'):
                    break
                for item in response['items']:
                    if len(comments) >= max_total:
                        break
                    comment_data = self.process_comment_item(item, video_info)
                    comments.append(comment_data)
                    if len(comments) >= max_total:
                        break
                    # Process replies if enabled
                    if (self.config['include_replies'] and 
                        'replies' in item and 
                        'comments' in item['replies']):
                        for reply_item in item['replies']['comments']:
                            if len(comments) >= max_total:
                                break
                            reply_data = self.process_reply_item(reply_item, video_info, comment_data)
                            comments.append(reply_data)
                            self.stats['total_replies'] += 1
                if len(comments) >= max_total:
                    break
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                # Small delay between requests
                time.sleep(self.config['delays']['between_requests'])
        except Exception as e:
            print(f"⚠️ Error getting comments: {e}")
        # Truncate if over (should not happen, but for safety)
        if len(comments) > max_total:
            comments = comments[:max_total]
        return comments, api_calls
    
    def process_comment_item(self, item: Dict, video_info: Dict) -> Dict:
        """Process item komentar menjadi data yang diperlukan"""
        snippet = item['snippet']['topLevelComment']['snippet']
        comment_data = {}
        # Basic comment info
        if self.config['attributes']['comment_text']:
            comment_data['comment_text'] = self.clean_text(snippet.get('textDisplay', ''))
        if self.config['attributes']['author_name']:
            comment_data['author_name'] = snippet.get('authorDisplayName', '')
        if self.config['attributes']['author_channel_id']:
            comment_data['author_channel_id'] = snippet.get('authorChannelId', {}).get('value', '')
        if self.config['attributes']['author_channel_url']:
            channel_id = snippet.get('authorChannelId', {}).get('value', '')
            comment_data['author_channel_url'] = f'https://www.youtube.com/channel/{channel_id}' if channel_id else ''
        if self.config['attributes']['author_profile_image_url']:
            comment_data['author_profile_image_url'] = snippet.get('authorProfileImageUrl', '')
        if self.config['attributes']['author_is_verified']:
            comment_data['author_is_verified'] = snippet.get('authorIsVerified', False)
        if self.config['attributes']['author_is_channel_owner']:
            comment_data['author_is_channel_owner'] = snippet.get('authorIsChannelOwner', False)
        if self.config['attributes']['author_is_sponsor']:
            comment_data['author_is_sponsor'] = snippet.get('authorIsSponsor', False)
        if self.config['attributes']['is_liked_by_creator']:
            comment_data['is_liked_by_creator'] = snippet.get('viewerRating', '') == 'like'
        if self.config['attributes']['is_hearted_by_creator']:
            comment_data['is_hearted_by_creator'] = snippet.get('viewerRating', '') == 'heart'
        if self.config['attributes']['is_pinned']:
            comment_data['is_pinned'] = item['snippet'].get('isPinned', False)
        if self.config['attributes']['publish_date']:
            comment_data['publish_date'] = snippet.get('publishedAt', '')
        if self.config['attributes']['updated_at']:
            comment_data['updated_at'] = snippet.get('updatedAt', '')
        if self.config['attributes']['like_count']:
            comment_data['like_count'] = snippet.get('likeCount', 0)
        if self.config['attributes']['reply_count']:
            comment_data['reply_count'] = item['snippet'].get('totalReplyCount', 0)
        if self.config['attributes']['parent_id']:
            comment_data['parent_id'] = None  # Top-level comment
        # Video info
        if self.config['attributes']['video_id']:
            comment_data['video_id'] = video_info.get('id', '')
        if self.config['attributes']['video_title']:
            comment_data['video_title'] = video_info.get('snippet', {}).get('title', '')
        if self.config['attributes']['video_url']:
            comment_data['video_url'] = f"https://www.youtube.com/watch?v={video_info.get('id', '')}"
        if self.config['attributes']['channel_id']:
            comment_data['channel_id'] = video_info.get('snippet', {}).get('channelId', '')
        if self.config['attributes']['channel_title']:
            comment_data['channel_title'] = video_info.get('snippet', {}).get('channelTitle', '')
        # Analysis attributes
        if self.config['attributes']['word_count'] and comment_data.get('comment_text'):
            comment_data['word_count'] = len(comment_data['comment_text'].split())
        if self.config['attributes']['has_links'] and comment_data.get('comment_text'):
            comment_data['has_links'] = bool(re.search(r'http[s]?://|www\.', comment_data['comment_text']))
        if self.config['attributes']['has_mentions'] and comment_data.get('comment_text'):
            comment_data['has_mentions'] = bool(re.search(r'@\w+', comment_data['comment_text']))
        if (self.config['attributes']['sentiment_score'] and HAS_TEXTBLOB and comment_data.get('comment_text')):
            try:
                blob = TextBlob(comment_data['comment_text'])
                comment_data['sentiment_score'] = blob.sentiment.polarity
            except:
                comment_data['sentiment_score'] = 0
        if self.config['attributes']['crawl_timestamp']:
            comment_data['crawl_timestamp'] = datetime.now().isoformat()
        # Comment type
        comment_data['comment_type'] = 'main_comment'
        return comment_data
    
    def process_reply_item(self, reply_item: Dict, video_info: Dict, parent_comment: Dict) -> Dict:
        """Process reply item"""
        snippet = reply_item['snippet']
        reply_data = {}
        # Basic reply info
        if self.config['attributes']['comment_text']:
            reply_data['comment_text'] = self.clean_text(snippet.get('textDisplay', ''))
        if self.config['attributes']['author_name']:
            reply_data['author_name'] = snippet.get('authorDisplayName', '')
        if self.config['attributes']['author_channel_id']:
            reply_data['author_channel_id'] = snippet.get('authorChannelId', {}).get('value', '')
        if self.config['attributes']['author_channel_url']:
            channel_id = snippet.get('authorChannelId', {}).get('value', '')
            reply_data['author_channel_url'] = f'https://www.youtube.com/channel/{channel_id}' if channel_id else ''
        if self.config['attributes']['author_profile_image_url']:
            reply_data['author_profile_image_url'] = snippet.get('authorProfileImageUrl', '')
        if self.config['attributes']['author_is_verified']:
            reply_data['author_is_verified'] = snippet.get('authorIsVerified', False)
        if self.config['attributes']['author_is_channel_owner']:
            reply_data['author_is_channel_owner'] = snippet.get('authorIsChannelOwner', False)
        if self.config['attributes']['author_is_sponsor']:
            reply_data['author_is_sponsor'] = snippet.get('authorIsSponsor', False)
        if self.config['attributes']['is_liked_by_creator']:
            reply_data['is_liked_by_creator'] = snippet.get('viewerRating', '') == 'like'
        if self.config['attributes']['is_hearted_by_creator']:
            reply_data['is_hearted_by_creator'] = snippet.get('viewerRating', '') == 'heart'
        if self.config['attributes']['is_pinned']:
            reply_data['is_pinned'] = False  # Replies can't be pinned
        if self.config['attributes']['publish_date']:
            reply_data['publish_date'] = snippet.get('publishedAt', '')
        if self.config['attributes']['updated_at']:
            reply_data['updated_at'] = snippet.get('updatedAt', '')
        if self.config['attributes']['like_count']:
            reply_data['like_count'] = snippet.get('likeCount', 0)
        if self.config['attributes']['reply_count']:
            reply_data['reply_count'] = 0  # Replies don't have replies
        if self.config['attributes']['parent_id']:
            reply_data['parent_id'] = reply_item.get('id', '') or parent_comment.get('video_id', '')
        reply_data['parent_author'] = parent_comment.get('author_name', '')
        reply_data['comment_type'] = 'reply'
        # Video info (same as parent)
        if self.config['attributes']['video_id']:
            reply_data['video_id'] = parent_comment.get('video_id', '')
        if self.config['attributes']['video_title']:
            reply_data['video_title'] = parent_comment.get('video_title', '')
        if self.config['attributes']['video_url']:
            reply_data['video_url'] = parent_comment.get('video_url', '')
        if self.config['attributes']['channel_id']:
            reply_data['channel_id'] = parent_comment.get('channel_id', '')
        if self.config['attributes']['channel_title']:
            reply_data['channel_title'] = parent_comment.get('channel_title', '')
        # Analysis attributes
        if self.config['attributes']['word_count'] and reply_data.get('comment_text'):
            reply_data['word_count'] = len(reply_data['comment_text'].split())
        if self.config['attributes']['has_links'] and reply_data.get('comment_text'):
            reply_data['has_links'] = bool(re.search(r'http[s]?://|www\.', reply_data['comment_text']))
        if self.config['attributes']['has_mentions'] and reply_data.get('comment_text'):
            reply_data['has_mentions'] = bool(re.search(r'@\w+', reply_data['comment_text']))
        if (self.config['attributes']['sentiment_score'] and HAS_TEXTBLOB and reply_data.get('comment_text')):
            try:
                blob = TextBlob(reply_data['comment_text'])
                reply_data['sentiment_score'] = blob.sentiment.polarity
            except:
                reply_data['sentiment_score'] = 0
        if self.config['attributes']['crawl_timestamp']:
            reply_data['crawl_timestamp'] = datetime.now().isoformat()
        return reply_data
    
    def clean_text(self, text: str) -> str:
        """Clean text dari karakter yang tidak diinginkan"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def show_crawling_summary(self):
        """Tampilkan ringkasan hasil crawling"""
        end_time = datetime.now()
        duration = end_time - self.stats['start_time']
        
        print("\n" + "=" * 50)
        print("📊 RINGKASAN HASIL CRAWLING")
        print("=" * 50)
        print(f"📺 Video diproses: {self.stats['processed_videos']}/{self.stats['total_videos']}")
        print(f"💬 Total komentar: {self.stats['total_comments']}")
        print(f"↩️ Total replies: {self.stats['total_replies']}")
        print(f"🔄 API calls: {self.stats['api_calls']}")
        print(f"⏱️ Durasi: {duration}")
        print(f"📊 Rate: {self.stats['total_comments']/(duration.total_seconds()/60):.1f} komentar/menit")
        
        if self.stats['errors']:
            print(f"\n⚠️ Errors: {len(self.stats['errors'])}")
            for error in self.stats['errors'][:3]:  # Show first 3 errors
                print(f"   • {error}")
            if len(self.stats['errors']) > 3:
                print(f"   ... dan {len(self.stats['errors'])-3} error lainnya")
    
    def save_results(self):
        """Simpan hasil crawling ke file"""
        if not self.results:
            print("❌ Tidak ada data untuk disimpan!")
            return
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = self.config['output']['filename_prefix']
        
        if self.config['output']['include_timestamp']:
            base_filename = f"{prefix}_{timestamp}"
        else:
            base_filename = prefix
        
        # Create DataFrame
        df = pd.DataFrame(self.results)
        
        try:
            if self.config['output']['format'] == 'excel':
                filename = f"{base_filename}.xlsx"
                df.to_excel(filename, index=False, engine='openpyxl')
                
            elif self.config['output']['format'] == 'csv':
                filename = f"{base_filename}.csv"
                df.to_csv(filename, index=False, encoding='utf-8')
                
            elif self.config['output']['format'] == 'json':
                filename = f"{base_filename}.json"
                df.to_json(filename, orient='records', indent=2, force_ascii=False)
            
            print(f"\n✅ Hasil berhasil disimpan: {filename}")
            print(f"📊 Total records: {len(df)}")
            print(f"📋 Columns: {len(df.columns)}")
            
            # Save config if enabled
            if self.config['output']['save_config']:
                config_filename = f"{base_filename}_config.json"
                with open(config_filename, 'w') as f:
                    json.dump(self.config, f, indent=2)
                print(f"⚙️ Konfigurasi disimpan: {config_filename}")
                
        except Exception as e:
            print(f"❌ Error menyimpan file: {e}")
    
    def run_interactive(self):
        """Jalankan mode interaktif"""
        print("🎬 YOUTUBE COMMENTS CRAWLER")
        print("=" * 50)
        print("Version: 1.0.0")
        print("Author: Ferdian Bangkit Wijaya")
        print("Institution: Universitas Sultan Ageng Tirtayasa")
        print("Mode: Interactive Terminal")
        print("Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("\n💡 Sistem crawling komentar YouTube untuk penelitian akademik")
        print("📖 Original concept from Jupyter Notebook, enhanced for terminal use")

        try:
            while True:
                # Step 1: Setup API Key
                if not self.setup_api_key():
                    print("❌ Setup API key gagal. Program dihentikan.")
                    return

                # Step 2: Get video URLs
                while True:
                    video_urls = self.get_video_urls()
                    if video_urls == "__BACK_TO_API_KEY__":
                        # User memilih 'b' di menu utama input video, kembali ke menu input API key
                        print("\n↩️ Kembali ke menu input API key.")
                        break
                    if video_urls is None:
                        # User memilih 'b' di sub-menu, tampilkan ulang menu input video
                        print("\n↩️ Kembali ke menu input video.")
                        continue  # ulangi menu input video
                    if not video_urls:
                        print("❌ Tidak ada URL video. Program dihentikan.")
                        return
                    # Jika dapat URL, lanjutkan proses
                    print(f"\n✅ Ditemukan {len(video_urls)} URL video valid")

                    # Step 3: Configure crawling
                    config_choice = input("\nKonfigurasi crawling? (y/n) [y]: ").strip().lower()
                    if config_choice in ['', 'y', 'yes', 'ya']:
                        config_result = self.configure_crawling()
                        if config_result == "__BACK_TO_INPUT_VIDEO__":
                            continue  # Kembali ke menu input video
                    else:
                        print("✅ Menggunakan konfigurasi default")
                        self.show_config_summary()

                    # Step 4: Final confirmation
                    print(f"\n🚀 SIAP MEMULAI CRAWLING")
                    print(f"📺 Video: {len(video_urls)}")
                    print(f"💬 Est. max komentar: {len(video_urls) * self.config['max_comments_per_video']}")

                    allowed_yes = ['y', 'yes', 'ya']
                    allowed_no = ['n', 'no', 'tidak']
                    allowed_back = ['b', 'back']
                    allowed_quit = ['quit', 'exit', 'batal', '0']
                    while True:
                        start_choice = input("\nMulai crawling? (y/n): ").strip().lower()
                        if start_choice in allowed_yes:
                            # Step 5: Start crawling
                            self.start_crawling(video_urls)
                            print("\n🎉 Crawling selesai!")
                            return  # Selesai crawling, keluar
                        elif start_choice in allowed_no:
                            print("❌ Crawling dibatalkan")
                            return
                        elif start_choice in allowed_back:
                            print("↩️ Kembali ke menu konfigurasi crawling.")
                            # Tampilkan ulang menu konfigurasi crawling
                            config_result = self.configure_crawling()
                            if config_result == "__BACK_TO_INPUT_VIDEO__":
                                # Tampilkan ulang menu input video
                                print("\n📺 INPUT VIDEO YOUTUBE")
                                print("=" * 40)
                                print("💡 Metode input yang tersedia:")
                                print("   1. Input manual satu per satu")
                                print("   2. Input multiple URLs (pisahkan dengan enter)")
                                print("   3. Load dari file Excel")
                                print("   4. Load dari file txt")
                                print("   0. Exit (keluar dari menu input)")
                                print("   b. Back (kembali ke menu sebelumnya jika ada)")
                                break  # Kembali ke menu input video
                            else:
                                # Setelah konfigurasi ulang, ulangi konfirmasi mulai crawling
                                print(f"\n🚀 SIAP MEMULAI CRAWLING")
                                print(f"📺 Video: {len(video_urls)}")
                                print(f"💬 Est. max komentar: {len(video_urls) * self.config['max_comments_per_video']}")
                                continue
                        elif start_choice in allowed_quit:
                            print("❌ Crawling dibatalkan oleh user.")
                            return
                        else:
                            print("❌ Input tidak valid! Pilih 'y' untuk mulai, 'n' untuk batal, 'b' untuk kembali ke konfigurasi, atau 'quit' untuk keluar.")
                    # If break from 'b'/'back' to input video, continue outer while loop
                    continue

        except KeyboardInterrupt:
            print("\n\n❌ Program dihentikan oleh user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="YouTube Comments Crawler - Interactive Terminal Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python youtube_comments_crawler.py
  python youtube_comments_crawler.py --api-key YOUR_API_KEY
  
Environment Variables:
  YOUTUBE_API_KEY    YouTube Data API v3 key
        """
    )
    
    parser.add_argument(
        '--api-key',
        help='YouTube Data API v3 key'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='YouTube Comments Crawler 1.0.0 - by Ferdian Bangkit Wijaya (UNTIRTA)'
    )
    
    args = parser.parse_args()
    
    # Create crawler instance
    crawler = YouTubeCommentsCrawler()
    
    # Set API key if provided
    if args.api_key:
        os.environ['YOUTUBE_API_KEY'] = args.api_key
    
    # Run interactive mode
    crawler.run_interactive()


if __name__ == "__main__":
    main()
