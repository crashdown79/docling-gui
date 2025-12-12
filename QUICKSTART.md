# Quick Start Guide

Get up and running with Docling GUI in 5 minutes!

## Installation (One-Time Setup)

### Step 1: Install Python
Ensure you have Python 3.9 or later installed:
```bash
python --version
# Should show Python 3.9.x or higher
```

### Step 2: Set Up Virtual Environment
```bash
# Navigate to project directory
cd /path/to/docling-gui

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**That's it!** You're ready to run the application.

## Running the Application

### Every Time You Use It:

1. **Activate virtual environment** (if not already active):
   ```bash
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

## First Conversion

1. **Click "Select File"** - Choose a PDF, Word doc, or other supported file

2. **Leave defaults** (they're sensible):
   - Format: Markdown
   - Mode: Online
   - OCR: Enabled

3. **Click "Convert"** - Watch the console output

4. **Click "Open Folder"** - View your converted file!

## Tips for Success

### First Run
- The first conversion may take longer (downloading models)
- Ensure you have a stable internet connection
- Try a small test file first (1-2 pages)

### File Types
- ✅ **Best results**: PDFs, DOCX, PPTX
- ✅ **Good results**: HTML, Images (with OCR)
- ⚠️ **Requires specific pipeline**: Audio/Video (use ASR pipeline)

### Common Settings

**For scanned documents or images**:
- Enable "Force OCR"
- Keep OCR enabled

**For complex layouts**:
- Switch pipeline to "VLM"
- May take longer but better quality

**For offline/private use**:
- Switch mode to "Offline"
- First run needs internet to download models
- After that: works offline forever

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Docling not found" | Run: `pip install docling` |
| Conversion fails | Check console output for specific error |
| Slow processing | Normal for large files; check progress in console |
| Can't open output folder | Manually browse to output directory shown in UI |

## Next Steps

Once you're comfortable with basic conversions:

1. Explore different **output formats** (JSON for data, HTML for web)
2. Try **offline mode** for privacy
3. Experiment with **VLM pipeline** for complex documents
4. Read the full [README.md](README.md) for advanced features

## Support

- 📖 Full documentation: [README.md](README.md)
- 🎯 Feature roadmap: [FEATURE_ANALYSIS.md](FEATURE_ANALYSIS.md)
- ⚙️ Technical details: [FRAMEWORK_ANALYSIS.md](FRAMEWORK_ANALYSIS.md)

---

**Happy Converting!** 🎉
