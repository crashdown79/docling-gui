# Docling GUI

A user-friendly graphical interface for the [Docling](https://github.com/docling-project/docling) document converter. Convert PDFs, Word documents, PowerPoint presentations, HTML, images, and more to Markdown, JSON, HTML, or text formats with ease.

## Features

### MVP (Current Version)

- **Simple File Selection**: Click to browse or drag-and-drop support (coming soon)
- **Multiple Output Formats**: Markdown, JSON, HTML, HTML (split page), Text, Doctags
- **Configurable Output**: Choose output directory with quick access to open folder
- **Processing Modes**:
  - **Online Mode**: Default mode with automatic model downloads
  - **Offline Mode**: Privacy-focused, uses local model artifacts
- **OCR Support**:
  - Enable/disable OCR (Optical Character Recognition)
  - Force OCR to replace existing text
- **Pipeline Selection**: Standard, VLM (Vision Language Model), ASR (Audio/Speech Recognition)
- **Real-time Console Output**: See Docling's processing output in real-time
- **Progress Tracking**: Visual feedback during conversion
- **Error Handling**: Clear error messages and validation
- **Persistent Settings**: Remembers your preferences between sessions

## Screenshots

```
┌────────────────────────────────────────────────────────────┐
│              Docling Document Converter                    │
├────────────────────────────────────────────────────────────┤
│  Input File:  document.pdf              [Select File]     │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  📄 Drag & drop files here or use 'Select File'     │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  Format: [Markdown ▼]  Output: /path/to/output [Browse]  │
│                                                            │
│  Mode: (•) Online ( ) Offline  ☑ Enable OCR              │
│  Pipeline: [Standard ▼]                                   │
│                                                            │
│              [    Convert    ]  [Cancel]                  │
│  Progress: [████████░░░░░░░░] Processing...              │
│                                                            │
│  Console Output:                                          │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ [12:34:56] Starting conversion...                    │ │
│  │ [12:34:57] Processing page 1/15...                   │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

## Requirements

- **Python**: 3.9 - 3.14 (3.12+ recommended)
- **Operating System**: macOS or Windows 11
- **Dependencies**: See `requirements.txt`

## Installation

### 1. Clone or Download

```bash
cd /path/to/your/projects
git clone <repository-url> docling-gui
# or download and extract the ZIP file
cd docling-gui
```

### 2. Create Virtual Environment (Recommended)

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `customtkinter` - Modern UI framework
- `docling` - Document conversion library
- `Pillow` - Image processing support

### 4. Verify Docling Installation

```bash
docling --version
```

If this command fails, ensure Docling is properly installed:
```bash
pip install --upgrade docling
```

## Usage

### Starting the Application

```bash
python main.py
```

Or make it executable (macOS/Linux):
```bash
chmod +x main.py
./main.py
```

### Basic Workflow

1. **Select Input File**:
   - Click "Select File" button
   - Choose a document (PDF, DOCX, PPTX, HTML, image, etc.)

2. **Configure Output**:
   - Select output format from dropdown (default: Markdown)
   - Choose output directory (default: ~/Documents/docling_output)

3. **Set Processing Options** (optional):
   - Choose **Online** or **Offline** mode
   - Enable/disable OCR
   - Select processing pipeline (Standard, VLM, ASR)

4. **Convert**:
   - Click "Convert" button
   - Monitor progress in the console output
   - Wait for completion message

5. **Access Output**:
   - Click "Open Folder" to view converted files
   - Files are saved in your selected output directory

### Processing Modes

#### Online Mode (Default)
- Uses default model locations
- May download models as needed (requires internet)
- Always up-to-date with latest models
- **Best for**: Most users, first-time use

#### Offline Mode
- Uses local model artifacts from specified path
- No internet connections required
- Better for privacy and air-gapped environments
- **Best for**: Privacy-conscious users, secure environments

To configure offline mode:
1. Set artifacts path in settings (default: `~/.cache/docling`)
2. Ensure models are downloaded (will be downloaded on first use with internet)
3. Switch to "Offline" mode in the UI

### Output Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| **Markdown** | `.md` | Structured text, ideal for documentation and notes |
| **JSON** | `.json` | Structured data, suitable for further processing |
| **HTML** | `.html` | Web-ready format with styling |
| **HTML (Split)** | `.html` | Separate HTML file per page |
| **Text** | `.txt` | Plain text, no formatting |
| **Doctags** | `.doctags` | Document with semantic tags |

### OCR Options

- **Enable OCR**: Extract text from images and scanned documents
- **Force OCR**: Replace existing text with OCR output (useful for poor-quality PDFs)

### Pipeline Options

- **Standard**: General document processing (recommended for most documents)
- **VLM**: Vision Language Model for complex layouts and visual elements
- **ASR**: Audio/Speech Recognition for video and audio files

## Configuration

Settings are automatically saved to:
- **macOS**: `~/Library/Application Support/DoclingGUI/config.json`
- **Windows**: `%APPDATA%\DoclingGUI\config.json`

The application remembers:
- Last used output directory
- Output format preference
- Processing mode (online/offline)
- OCR settings
- Window size and position

## Project Structure

```
docling-gui/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── CLAUDE.md             # Project guidance
├── FRAMEWORK_ANALYSIS.md # Framework comparison
├── FEATURE_ANALYSIS.md   # Feature specifications
├── core/
│   ├── __init__.py
│   └── converter.py      # Docling integration
└── ui/
    ├── __init__.py
    └── main_window.py    # Main application window
```

## Troubleshooting

### "Docling CLI not found" Error

**Solution**: Install Docling:
```bash
pip install docling
```

Verify installation:
```bash
python -c "import docling; print(docling.__version__)"
```

### "Could not create output directory" Error

**Solution**:
- Check that the output directory path is valid
- Ensure you have write permissions
- Try selecting a different output directory (e.g., Desktop or Documents)

### Conversion Fails or Hangs

**Possible causes**:
1. **Large file**: Processing may take several minutes for large PDFs
2. **Corrupted file**: Try a different document
3. **Missing models**: In offline mode, ensure models are downloaded

**Solutions**:
- Check console output for specific errors
- Try with a smaller test file first
- Switch to online mode if in offline mode
- Ensure stable internet connection for online mode

### Application Won't Start

**Solution**:
```bash
# Reinstall dependencies
pip uninstall customtkinter docling -y
pip install -r requirements.txt

# Check Python version (should be 3.9-3.14)
python --version
```

### macOS: "Application is damaged" or Security Warning

**Solution**:
```bash
# If running from source, no code signing needed
# Just ensure you're running: python main.py
```

For packaged app (future):
```bash
xattr -cr DoclingGUI.app
```

## Development

### Running in Development Mode

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run with Python directly
python main.py
```

### Changing Theme

Edit `config.json` and change:
```json
"interface": {
  "theme": "dark"  // or "light" or "system"
}
```

Or the theme will be adjustable in settings (future feature).

## Roadmap

### Phase 2: Batch Processing (Coming Soon)
- Queue multiple files for batch conversion
- Add folders recursively
- Per-file status tracking
- Batch progress overview

### Phase 3: Advanced Options (Coming Soon)
- Full Docling parameter exposure
- VLM/ASR model selection
- Performance tuning options
- Debug visualization

### Phase 4: Polish (Coming Soon)
- Configuration profiles (save/load presets)
- Enhanced file preview with thumbnails
- Keyboard shortcuts
- Settings dialog

## Support

### Common Use Cases

**Convert PDF to Markdown**:
1. Select PDF file
2. Ensure "Markdown" is selected
3. Click Convert

**Extract Text from Scanned Document**:
1. Select image or scanned PDF
2. Enable "Force OCR"
3. Select "Text" format
4. Click Convert

**Process Document Offline**:
1. Switch to "Offline" mode
2. First time: Ensure internet for model download
3. After models downloaded: Works without internet
4. Click Convert

## License

This project is a GUI wrapper for Docling. For Docling license information, see:
https://github.com/docling-project/docling

## Credits

- **Docling**: Document conversion engine by IBM Research and LF AI & Data Foundation
- **CustomTkinter**: Modern UI framework by Tom Schimansky
- **Python**: Programming language

## Version History

### v1.0.0 - MVP Release (Current)
- Initial release with core features
- Single file conversion
- Online/offline processing modes
- Real-time console output
- Basic error handling
- Persistent configuration

## Contributing

Contributions welcome! Areas for improvement:
- Drag-and-drop file support
- Batch processing queue
- Advanced options panel
- Configuration profiles
- Unit tests
- Platform-specific packaging

## Contact

For issues, feature requests, or questions, please open an issue on the project repository.

---

**Note**: This is an MVP (Minimum Viable Product) release. Additional features are planned for future releases. See FEATURE_ANALYSIS.md for the complete feature roadmap.
