# 📁 Project Structure - YouTube Comments Crawler

```text
📦 YouTube Comments Crawler/
├── 🐍 youtube_comments_crawler.py      # Main crawler script
├── 📋 requirements.txt                 # Python dependencies
├── 📖 README.md                        # Complete documentation
├── 🚀 QUICK_START.md                   # Quick start guide
├── 📚 API_DOCS.md                      # API documentation
├── 📝 CHANGELOG.md                     # Version history
├── 📄 LICENSE                          # MIT License
├── 🔧 setup.bat                        # Windows setup script
├── ▶️ run.bat                          # Windows run script
├── 🧪 test_system.py                   # System test script
├── 🛠️ create_template.py               # Template creation utility
├── ⚙️ config_template.ini              # Configuration template
├── 📊 youtube_urls_template.xlsx       # Excel URL template
├── 📄 youtube_urls_template.txt        # Text URL template
├── 🚫 .gitignore                       # Git ignore rules
└── 📓 Youtube_Komentar_v1.0.ipynb     # Original Jupyter notebook
```

## 📂 File Descriptions

### Core Files

#### 🐍 `youtube_comments_crawler.py`

Main crawler application

- Interactive terminal interface (menu interaktif, validasi input, fitur back/exit di semua langkah)
- YouTube Data API v3 integration (diagnostik otomatis, error handling lengkap)
- Multiple input/output methods (manual, batch, Excel, txt, semua input tervalidasi)
- Flexible API key management (env, file, manual, auto-save)
- Multi-format output (Excel, CSV, JSON, atribut lengkap, nama file otomatis)
- Real-time progress & statistik crawling

#### 📋 `requirements.txt`

Python dependencies

- Core: google-api-python-client, pandas, openpyxl
- Optional: textblob, requests
- Development: pytest, black, flake8

### Documentation

#### 📖 `README.md`

Complete user documentation

- Installation instructions
- Step-by-step usage guide
- Configuration options
- Troubleshooting guide
- Best practices for research

#### 🚀 `QUICK_START.md`

Fast setup guide

- 5-minute setup process
- Quick workflow overview
- Common use cases
- Essential tips

#### 📚 `API_DOCS.md`

Developer documentation

- Class and method references
- Configuration structure
- Usage examples
- Integration guide

#### 📝 `CHANGELOG.md`

Version history

- Feature additions
- Bug fixes
- Breaking changes
- Future roadmap

### Setup & Run Scripts

#### 🔧 `setup.bat` (Windows)

Automated setup script

- Python version check
- Dependency installation
- System verification
- Setup validation

#### ▶️ `run.bat` (Windows)

Easy run script

- Pre-flight checks
- Launch crawler
- Error handling
- User-friendly interface

### Utilities

#### 🧪 `test_system.py`

System verification tool

- Dependency checking (wajib & opsional)
- API import testing
- File validation (template, config, output)
- Environment verification
- Output attribute check (pastikan output sesuai update terbaru)

#### 🛠️ `create_template.py`

Template generation utility

- Create Excel & text templates (kolom sesuai input terbaru)
- Sample data generation
- Utility for quick setup

### Templates & Configuration

#### ⚙️ `config_template.ini`

Configuration template

- API key storage
- Crawling parameters
- Output settings
- All configurable options

#### 📊 `youtube_urls_template.xlsx`

Excel input template

- Formatted for URL input (kolom URL auto-detect, contoh valid)
- Sample YouTube URLs
- Description column (opsional)
- Ready to use format (sesuai validasi input terbaru)

#### 📄 `youtube_urls_template.txt`

Text input template

- Simple text format (URL per baris, support komentar dengan #)
- URL examples (valid, siap pakai)
- Instructions included

### Project Files

#### 🚫 `.gitignore`

Git ignore rules

- Python cache files
- Generated output files
- Configuration files with secrets
- IDE and OS specific files

#### 📄 `LICENSE`

MIT License

- Open source license
- Usage permissions
- Liability disclaimers

#### 📓 `Youtube_Komentar_v1.0.ipynb`

Original Jupyter notebook

- Reference implementation
- Widget-based interface
- Research-oriented features

## 🎯 Usage Flow

### 1. Setup Phase

```text
📥 Download/Clone project
⬇️ Run setup.bat (Windows)
🔧 Install dependencies
✅ Verify system (test_system.py)
```

### 2. Configuration Phase

```text
🔑 Get YouTube API key
⚙️ Configure settings (optional)
📄 Prepare URL list (Excel/text)
```

### 3. Execution Phase

```text
▶️ Run youtube_comments_crawler.py
📺 Input video URLs
🚀 Start crawling
📊 Monitor progress
```

### 4. Output Phase

```text
💾 Save results (Excel/CSV/JSON)
📈 Analyze data
🔄 Repeat for more videos
```

## 📊 Generated Files

### During Operation

- `config.ini` - Saved configuration
- `api_key.txt` - API key storage (optional)

### Output Files

- `youtube_comments_YYYYMMDD_HHMMSS.xlsx` - Main results
- `youtube_comments_YYYYMMDD_HHMMSS_config.json` - Used configuration

### Temporary Files

- `__pycache__/` - Python cache (auto-generated)
- `*.tmp` - Temporary processing files

## 🔒 Security Considerations

### Sensitive Files (Not in Git)

- `config.ini` - Contains API key
- `api_key.txt` - API key storage
- `*.xlsx` - Output data files
- `*.csv` - Output data files
- `*.json` - Output data files

### Safe to Share

- All `.md` documentation files
- All `.py` source files
- Template files
- Setup scripts

## 🎓 For Academic Use

### Research Files

- Use `youtube_urls_template.xlsx` for video lists
- Configure for academic research parameters
- Enable sentiment analysis for deeper insights
- Export to Excel for statistical analysis

### Data Files Structure

```text
📊 Generated Data/
├── 📈 youtube_comments_study1_20250729.xlsx
├── ⚙️ youtube_comments_study1_20250729_config.json
├── 📈 youtube_comments_study2_20250730.xlsx
└── ⚙️ youtube_comments_study2_20250730_config.json
```

### Backup Strategy

```text
💾 Backup Essential Files:
├── 🔑 config.ini (API key)
├── 📊 *.xlsx (data files)
├── ⚙️ *_config.json (configurations)
└── 📄 custom_urls.txt (URL lists)
```

## 🌟 Key Features by File

| File | Key Features |
|------|-------------|
| `youtube_comments_crawler.py` | Core functionality, API integration |
| `README.md` | Complete documentation |
| `setup.bat` | One-click setup |
| `test_system.py` | Dependency verification |
| `config_template.ini` | Easy configuration |
| Template files | Quick start examples |

---

**Total Project Size:** ~50KB (source code)  
**Dependencies Size:** ~100MB (when installed)  
**Output Size:** Variable (depends on data collected)  

**Recommended Disk Space:** 500MB minimum for comfortable operation
