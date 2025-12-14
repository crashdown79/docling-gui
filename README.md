# Docling GUI

A user-friendly graphical interface for the [Docling](https://github.com/docling-project/docling) document converter. Convert PDFs, Word documents, PowerPoint presentations, HTML, images, and more to Markdown, JSON, HTML, or text formats with ease.

![screenshot](docs/screenshot-v1.5.2.png)

---

## Quick Links

- **[QUICKSTART.md](QUICKSTART.md)** - Get up and running in 5 minutes
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes

---

## Disclaimer

This project is a private hobby endeavor and is provided "as is," without any warranties of any kind, express or implied. The developer has no affiliation with Docling or any other third-party projects, tools, or libraries mentioned or used herein. Use at your own risk.

---

## Features

### Core Features
- **Drag-and-Drop Support**: Drag files directly into the queue
- **Batch Queue Processing**: Add multiple files or entire folders for sequential processing
- **Multiple Output Formats**: Markdown, JSON, HTML, HTML (split page), Text, Doctags
- **Processing Modes**: Online (auto-download models) or Offline (privacy-focused)
- **Real-time Console Output**: See Docling's processing output live
- **Persistent Settings**: Remembers your preferences between sessions

### Processing Options
- **OCR Engine Selection**: 6 OCR engines (auto, easyocr, tesseract, rapidocr, ocrmac, tesserocr)
- **Processing Pipelines**: Standard, VLM (Vision Language Model), ASR (Audio/Speech)
- **Enrichment Options**: Tables, Code, Formulas, Picture Classification/Descriptions
- **Debug Visualization**: Layout boxes, clusters, PDF cells, OCR cells, table cells

---

## Requirements

- **Python**: 3.9 - 3.14 (3.12+ recommended)
- **Operating System**: macOS or Windows 11
- **Dependencies**: See `requirements.txt`

---

## Installation

See **[QUICKSTART.md](QUICKSTART.md)** for detailed installation instructions.

**Quick setup:**
```bash
git clone <repository-url> docling-gui
cd docling-gui
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## Configuration

Settings are automatically saved to:
- **macOS**: `~/Library/Application Support/DoclingGUI/config.json`
- **Windows**: `%APPDATA%\DoclingGUI\config.json`

---

## Project Structure

```
docling-gui/
├── main.py                    # Application entry point
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── core/
│   ├── converter.py           # Docling CLI integration
│   └── queue.py               # Batch queue management
└── ui/
    ├── main_window.py         # Main window with two-panel layout
    ├── sidebar.py             # Left sidebar with all controls
    ├── queue_panel.py         # Batch queue visualization
    ├── console_panel.py       # Console output with logging
    └── widgets/               # Reusable UI components
```

---

## Troubleshooting

### "Docling CLI not found" Error
```bash
pip install docling
docling --version
```

### "Could not create output directory" Error
- Check that the output directory path is valid
- Ensure you have write permissions
- Try selecting a different output directory

### Conversion Fails or Hangs
- Check console output for specific errors
- Try with a smaller test file first
- Switch to online mode if in offline mode
- For large files, processing may take several minutes

### Application Won't Start
```bash
pip uninstall customtkinter docling -y
pip install -r requirements.txt
python --version  # Should be 3.9-3.14
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Credits

- **[Docling](https://github.com/docling-project/docling)**: Document conversion engine by IBM Research and LF AI & Data Foundation
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)**: Modern UI framework by Tom Schimansky

---

## Contributing

Contributions welcome! See [CHANGELOG.md](CHANGELOG.md) for current status and roadmap.

For issues, feature requests, or questions, please open an issue on the project repository.
