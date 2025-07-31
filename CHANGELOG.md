
# Changelog - YouTube Comments Crawler

## [1.1.0] - 2025-07-30

### Added

#### Core Features (v1.1.0)

- Menu interaktif dengan validasi input & fitur back/exit di semua langkah
- Input API key fleksibel (manual, file, env, auto-save)
- Input URL video: manual, batch, Excel, txt, validasi otomatis
- Konfigurasi crawling lengkap (jumlah komentar default 1000, urutan, format output, dsb)
- Ekstraksi atribut YouTube API sangat lengkap (status, author, like, heart, dsb)
- Output multi-format (Excel, CSV, JSON) dengan nama file otomatis
- Statistik & progress crawling real-time
- Diagnostik error API, quota, validasi key otomatis
- Dokumentasi & template diperbarui

#### Data Collection (v1.1.0)

- Semua atribut penting YouTube API: text, author, channel, status, like, heart, pinned, dsb
- Output file otomatis berisi seluruh atribut terbaru

#### User Experience (v1.1.0)

- Menu konfigurasi interaktif, rekomendasi default, validasi input
- Diagnostik otomatis, solusi error API/quota
- Troubleshooting otomatis di terminal

#### Documentation & Support (v1.1.0)

- README, QUICK_START, PROJECT_SUMMARY, PROJECT_STRUCTURE, CHANGELOG diperbarui
- Template input Excel/txt disesuaikan

### Changed

- Default max_comments_per_video menjadi 1000
- Semua menu bisa kembali/back/exit

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Author:** Ferdian Bangkit Wijaya  
**Institution:** Universitas Sultan Ageng Tirtayasa (UNTIRTA)  
**Original Concept:** Jupyter Notebook adaptation enhanced for terminal usage

## [1.0.0] - 2025-07-29

### Added (v1.0.0)

#### Core Features (v1.0.0)

- Interactive terminal-based YouTube comments crawler
- Support for YouTube Data API v3 integration
- Multiple input methods for video URLs (manual, batch, Excel, text file)
- Flexible API key management (environment variables, config files, manual input)
- Configurable crawling parameters (max comments, include replies, etc.)
- Multi-format output support (Excel, CSV, JSON)
- Real-time progress monitoring and statistics

#### Data Collection (v1.0.0)

- Comment text extraction with cleaning
- Author name and publish date collection
- Like count and reply count tracking
- Video metadata extraction (title, ID, URL)
- Word count analysis
- Link and mention detection
- Optional sentiment analysis (with TextBlob)
- Crawl timestamp recording
- Comment type classification (main/reply)

#### User Experience (v1.0.0)

- Step-by-step interactive setup
- Comprehensive error handling with diagnostics
- API key validation with detailed troubleshooting
- Progress tracking with ETA and statistics
- Automatic file naming with timestamps
- Configuration saving and loading

#### Documentation

- Complete README with installation and usage guide
- Quick start guide for fast setup
- API documentation for developers
- System test script for dependency verification
- Multiple example files and templates

#### Support Files

- Automated setup script for Windows (setup.bat)
- Easy run script for Windows (run.bat)
- Requirements file with all dependencies
- Git ignore file for clean repository
- Excel and text templates for URL input
- Configuration template file
- MIT License for open source usage

#### Technical Features

- Robust error handling for API limits and restrictions
- Rate limiting to respect YouTube API guidelines
- Memory-efficient processing for large datasets
- Cross-platform compatibility (Windows, Linux, macOS)
- Extensible architecture for future enhancements

#### Quality Assurance

- Comprehensive system testing
- Input validation and sanitization
- Safe file handling with proper encoding
- Graceful handling of interrupted operations
- Detailed logging and error reporting

### Dependencies

- google-api-python-client >= 2.0.0 (YouTube API)
- pandas >= 1.5.0 (data manipulation)
- openpyxl >= 3.0.0 (Excel support)
- textblob >= 0.17.0 (optional, sentiment analysis)
- requests >= 2.25.0 (optional, IP detection)

### System Requirements

- Python 3.7 or higher
- Internet connection for API access
- YouTube Data API v3 key from Google Cloud Console
- Minimum 100MB free disk space for output files

### Security Features

- Secure API key handling with multiple storage options
- No hardcoded credentials in source code
- Input sanitization to prevent injection attacks
- Safe file operations with proper permissions
- Privacy-conscious data handling

### Performance Optimizations

- Efficient API usage with proper pagination
- Configurable delays to respect rate limits
- Batch processing capabilities
- Memory-efficient data structures
- Optimized file I/O operations

## [Planned for Future Versions]

### [1.1.0] - Planned

- GUI interface option
- Advanced filtering options
- Export to additional formats (PDF, Word)
- Integration with popular analysis tools
- Automated report generation

### [1.2.0] - Planned

- Multi-language sentiment analysis
- Advanced text analytics
- Keyword extraction and analysis
- Comment threading visualization
- Statistical analysis dashboard

### [2.0.0] - Planned

- Web-based interface
- Database integration
- Real-time monitoring
- Scheduled crawling
- API for third-party integration

## Contributing

We welcome contributions! Please see our contributing guidelines for details on:

- How to report bugs
- How to suggest enhancements
- Development setup
- Code style guidelines
- Testing requirements

## Support

For support and questions:

- Check the documentation first
- Search existing issues on GitHub
- Create a new issue with detailed information
- Include log outputs for debugging

## License

This project is licensed under the MIT License - see the LICENSE file for details.
