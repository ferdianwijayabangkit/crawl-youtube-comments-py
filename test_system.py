#!/usr/bin/env python3
"""
Test Script untuk YouTube Comments Crawler
==========================================

Script ini akan memverifikasi bahwa semua dependencies sudah terinstall
dengan benar dan sistem siap untuk digunakan.

Author: Ferdian Bangkit Wijaya
Institution: Universitas Sultan Ageng Tirtayasa (UNTIRTA)
"""

import sys
import importlib

def test_python_version():
    """Test versi Python"""
    print("🐍 Testing Python version...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.7+")
        return False

def test_dependency(module_name, package_name=None, optional=False):
    """Test apakah dependency tersedia"""
    if package_name is None:
        package_name = module_name
        
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError:
        if optional:
            print(f"⚠️ {package_name} - Not available (optional)")
        else:
            print(f"❌ {package_name} - Missing (required)")
        return not optional

def test_youtube_api_import():
    """Test YouTube API imports"""
    print("\n📺 Testing YouTube API imports...")
    
    try:
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        print("✅ YouTube API imports - OK")
        return True
    except ImportError as e:
        print(f"❌ YouTube API imports - Failed: {e}")
        print("💡 Install with: pip install google-api-python-client")
        return False

def test_file_exists(filename, description):
    """Test apakah file ada"""
    import os
    
    if os.path.exists(filename):
        print(f"✅ {description} - Found")
        return True
    else:
        print(f"⚠️ {description} - Not found")
        return False

def main():
    """Main test function"""
    print("🧪 YOUTUBE COMMENTS CRAWLER - SYSTEM TEST")
    print("=" * 50)
    print("👨‍💻 Developed by: Ferdian Bangkit Wijaya")
    print("🏫 Institution: Universitas Sultan Ageng Tirtayasa")
    print("=" * 50)
    
    all_good = True
    
    # Test Python version
    if not test_python_version():
        all_good = False
    
    print("\n📦 Testing core dependencies...")
    
    # Core dependencies
    core_deps = [
        ('pandas', 'Pandas'),
        ('openpyxl', 'OpenPyXL'),
    ]
    
    for module, name in core_deps:
        if not test_dependency(module, name):
            all_good = False
    
    # Test YouTube API
    if not test_youtube_api_import():
        all_good = False
    
    print("\n🔧 Testing optional dependencies...")
    
    # Optional dependencies
    optional_deps = [
        ('textblob', 'TextBlob (sentiment analysis)'),
        ('requests', 'Requests (IP detection)'),
    ]
    
    for module, name in optional_deps:
        test_dependency(module, name, optional=True)
    
    print("\n📄 Testing project files...")
    
    # Project files
    project_files = [
        ('youtube_comments_crawler.py', 'Main crawler script'),
        ('requirements.txt', 'Requirements file'),
        ('README.md', 'Documentation'),
        ('setup.bat', 'Setup script'),
        ('run.bat', 'Run script'),
    ]
    
    for filename, description in project_files:
        test_file_exists(filename, description)

    # Tambahan: cek file template dan atribut output utama
    print("\n📄 Testing template & config files...")
    template_files = [
        ('youtube_urls_template.xlsx', 'Excel URL template'),
        ('youtube_urls_template.txt', 'Text URL template'),
        ('config_template.ini', 'Config template'),
        ('api_key.txt', 'API key file (optional)'),
        ('config.ini', 'Config file (optional)'),
    ]
    for filename, description in template_files:
        test_file_exists(filename, description)

    print("\n📊 Testing output attributes (if output file exists)...")
    import os
    import pandas as pd
    output_candidates = [f for f in os.listdir('.') if f.startswith('youtube_comments_') and (f.endswith('.xlsx') or f.endswith('.csv'))]
    if output_candidates:
        output_file = output_candidates[0]
        try:
            if output_file.endswith('.xlsx'):
                df = pd.read_excel(output_file)
            else:
                df = pd.read_csv(output_file)
            required_cols = [
                'comment_text', 'author_name', 'author_channel_id', 'author_channel_url', 'author_profile_image_url',
                'author_is_verified', 'author_is_channel_owner', 'author_is_sponsor',
                'is_liked_by_creator', 'is_hearted_by_creator', 'is_pinned_by_creator',
                'publish_date', 'updated_at', 'like_count', 'reply_count', 'parent_id',
                'video_id', 'video_title', 'video_url', 'video_channel_id', 'video_channel_title',
                'word_count', 'has_links', 'has_mentions', 'sentiment_score',
                'crawl_timestamp', 'comment_type'
            ]
            missing = [col for col in required_cols if col not in df.columns]
            if not missing:
                print(f"✅ Output file '{output_file}' contains all main attributes")
            else:
                print(f"⚠️ Output file '{output_file}' missing columns: {missing}")
        except Exception as e:
            print(f"⚠️ Could not read output file '{output_file}': {e}")
    else:
        print("ℹ️ No output file found to check attributes (run crawler first)")
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is ready for YouTube Comments Crawler")
        print("\n🚀 Next steps:")
        print("   1. Get YouTube Data API v3 key")
        print("   2. Run: python youtube_comments_crawler.py")
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 Please fix the issues above before running the crawler")
        print("\n💡 Quick fixes:")
        print("   - Install missing dependencies: pip install -r requirements.txt")
        print("   - Check Python version: python --version")
    
    print("\n📋 System Information:")
    print(f"   Python: {sys.version}")
    print(f"   Platform: {sys.platform}")
    
    return all_good

if __name__ == "__main__":
    success = main()
    
    input("\nPress Enter to exit...")
    
    if not success:
        sys.exit(1)
