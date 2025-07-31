# API Documentation - YouTube Comments Crawler

## 📚 Class: YouTubeCommentsCrawler

Main class untuk melakukan crawling komentar YouTube dengan berbagai konfigurasi dan opsi.

### Constructor

```python
crawler = YouTubeCommentsCrawler()
```

### Public Methods

#### setup_api_key() -> bool

Setup API key dengan berbagai metode input (environment variable, config file, manual input).

**Returns:**

- `True` jika API key berhasil disetup dan valid
- `False` jika gagal

**Example:**

```python
if crawler.setup_api_key():
    print("API key ready!")
```

#### get_video_urls() -> List[str]

Mengumpulkan daftar URL video YouTube dengan berbagai metode input.

**Returns:** List URL video yang valid

**Methods:**

1. Input manual satu per satu
2. Input multiple URLs batch
3. Load dari file Excel
4. Load dari file text

#### configure_crawling()

Konfigurasi parameter crawling secara interaktif.

**Configurable parameters:**

- Max comments per video
- Include replies
- Comment order (relevance/time)
- Output format (excel/csv/json)

#### start_crawling(video_urls: List[str])

Memulai proses crawling dengan daftar URL yang diberikan.

**Parameters:**

- `video_urls`: List URL video YouTube

**Process:**

1. Validasi setiap URL
2. Ekstrak video info
3. Crawl comments dan replies
4. Process dan clean data
5. Save results

#### extract_video_id(url: str) -> Optional[str]

Extract video ID dari berbagai format YouTube URL.

**Parameters:**

- `url`: YouTube URL dalam berbagai format

**Returns:**

- Video ID (11 karakter) jika valid
- `None` jika tidak valid

**Supported formats:**

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `VIDEO_ID` (just the ID)

#### run_interactive()

Menjalankan mode interaktif lengkap (main entry point).

## 📊 Configuration Structure

### Default Config

```python
{
    'max_comments_per_video': 100,
    'include_replies': True,
    'comment_order': 'relevance',  # atau 'time'
    'attributes': {
        'comment_text': True,
        'author_name': True,
        'publish_date': True,
        'like_count': True,
        'reply_count': True,
        # ... dan lainnya
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
```

### Attributes yang Dikumpulkan

- `comment_text`: Teks komentar
- `author_name`: Nama penulis
- `publish_date`: Tanggal publikasi
- `like_count`: Jumlah likes
- `reply_count`: Jumlah replies
- `video_id`: YouTube video ID
- `video_title`: Judul video
- `video_url`: URL video lengkap
- `word_count`: Jumlah kata
- `has_links`: Boolean ada link
- `has_mentions`: Boolean ada mention (@)
- `sentiment_score`: Skor sentiment (-1 to 1, jika TextBlob tersedia)
- `comment_type`: 'main_comment' atau 'reply'
- `crawl_timestamp`: Waktu crawling

## 🔧 Internal Methods

### validate_api_key(api_key: str) -> bool

Validasi API key dengan test request ke YouTube API.

### get_video_info(video_id: str) -> Optional[Dict]

Mengambil informasi video (title, statistics, etc).

### get_video_comments(video_id: str, video_info: Dict) -> Tuple[List[Dict], int]

Mengambil semua komentar dari satu video.

### process_comment_item(item: Dict, video_info: Dict) -> Dict

Process raw comment item menjadi format data yang diinginkan.

### process_reply_item(reply_item: Dict, video_info: Dict, parent_comment: Dict) -> Dict

Process reply comment dengan referensi ke parent comment.

### clean_text(text: str) -> str

Pembersihan teks dari karakter yang tidak diinginkan.

### save_results()

Simpan hasil crawling ke file sesuai format yang dipilih.

## 📈 Statistics Tracking

### Stats Object

```python
{
    'total_videos': 0,
    'processed_videos': 0,
    'total_comments': 0,
    'total_replies': 0,
    'api_calls': 0,
    'start_time': None,
    'errors': []
}
```

## 🚨 Error Handling

### API Errors

- **403 Forbidden**: API key restricted
- **400 Bad Request**: Invalid API key
- **Quota Exceeded**: Daily quota habis
- **Access Not Configured**: API belum enabled

### Video Errors

- **Video Private**: Video tidak public
- **Comments Disabled**: Komentar dinonaktifkan
- **Video Not Found**: Video dihapus/tidak ada

## 💡 Usage Examples

### Basic Usage

```python
from youtube_comments_crawler import YouTubeCommentsCrawler

# Create instance
crawler = YouTubeCommentsCrawler()

# Setup API key
if not crawler.setup_api_key():
    exit("API key setup failed")

# Get video URLs
urls = crawler.get_video_urls()

# Configure (optional)
crawler.configure_crawling()

# Start crawling
crawler.start_crawling(urls)
```

### Programmatic Usage

```python
import os
from youtube_comments_crawler import YouTubeCommentsCrawler

# Set API key via environment
os.environ['YOUTUBE_API_KEY'] = 'your_api_key_here'

# Create and configure crawler
crawler = YouTubeCommentsCrawler()
crawler.setup_api_key()

# Set custom config
crawler.config['max_comments_per_video'] = 50
crawler.config['include_replies'] = False
crawler.config['output']['format'] = 'csv'

# Define URLs
video_urls = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://youtu.be/9bZkp7q19f0'
]

# Start crawling
crawler.start_crawling(video_urls)
```

### Batch Processing

```python
# Load URLs from Excel
excel_file = 'my_videos.xlsx'
df = pd.read_excel(excel_file)
urls = df['youtube_url'].tolist()

# Process in batches
batch_size = 10
for i in range(0, len(urls), batch_size):
    batch_urls = urls[i:i+batch_size]
    
    crawler = YouTubeCommentsCrawler()
    crawler.setup_api_key()
    crawler.start_crawling(batch_urls)
    
    # Optional: delay between batches
    time.sleep(60)
```

## 🔒 API Key Management

### Environment Variable

```bash
set YOUTUBE_API_KEY=your_api_key_here
```

### Config File (config.ini)

```ini
[youtube]
api_key = your_api_key_here
```

### Text File (api_key.txt)

```text
your_api_key_here
```

### .env File

```env
YOUTUBE_API_KEY=your_api_key_here
```

## 📁 File I/O Formats

### Excel Input Format

| youtube_url | description |
|-------------|-------------|
| <https://www.youtube.com/watch?v=...> | Video 1 |
| <https://youtu.be/...> | Video 2 |

### Text Input Format

```text
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/9bZkp7q19f0
# Comments are ignored
```

### Output Formats

- **Excel**: `.xlsx` dengan semua columns
- **CSV**: `.csv` UTF-8 encoded
- **JSON**: `.json` dengan records format
