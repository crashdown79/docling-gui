# Docling GUI v1.1.0 - Release Notes

**Release Date**: December 12, 2025
**Type**: Minor Feature Release
**Status**: ✅ Production Ready

## 🎉 What's New

### OCR Language Selection
Configure which languages Docling should recognize during OCR processing.

**Features**:
- **Text Input Field**: Enter comma-separated language codes (e.g., "eng,deu,fra")
- **Quick Preset Buttons**: One-click buttons for common languages
  - 🇬🇧 EN (English)
  - 🇩🇪 DE (German)
  - 🇫🇷 FR (French)
  - 🇪🇸 ES (Spanish)
  - 🇮🇹 IT (Italian)
  - 🇨🇳 ZH (Chinese Simplified)
- **Smart Adding**: Click preset buttons to add languages automatically
- **Duplicate Detection**: Won't add the same language twice
- **Persistent**: Your language selection is saved for future sessions

**Use Cases**:
- Multi-language documents
- Non-English documents
- Better OCR accuracy for specific languages
- Mixed-language PDFs

**Example**:
```
Click: EN → Field shows: "eng"
Click: DE → Field shows: "eng,deu"
Click: FR → Field shows: "eng,deu,fra"
```

---

### Content Enrichment Options
Enable AI-powered enhancements for better document processing.

**Three New Options**:

#### 1. Formula Enrichment
- **What it does**: Improves recognition and formatting of mathematical formulas
- **When to use**: Documents with equations, mathematical expressions, LaTeX
- **Examples**: Academic papers, scientific reports, math textbooks

#### 2. Picture Classes
- **What it does**: Automatically classifies images by type
- **Categories**: Charts, diagrams, photos, illustrations, tables
- **When to use**: Documents with mixed visual content
- **Examples**: Reports with charts and photos, presentations, infographics

#### 3. Picture Descriptions
- **What it does**: Generates descriptive text for images
- **Output**: Alt-text style descriptions of image content
- **When to use**: Accessibility, content analysis, image-heavy documents
- **Examples**: Photo albums, illustrated guides, catalogs

**How to Use**:
1. Check the boxes for desired enrichment options
2. Process your document as normal
3. Enriched content appears in the output

**Note**: Enrichment options may increase processing time but provide higher quality results.

---

## 🔧 Technical Changes

### Updated Files
1. **core/converter.py**:
   - Added `ocr_lang` parameter to `build_command()`
   - Added `enrich_formula`, `enrich_picture_classes`, `enrich_picture_description` parameters
   - Updated `convert()` method to pass new parameters

2. **ui/main_window.py**:
   - Added OCR language input field with preset buttons
   - Added enrichment option checkboxes
   - Implemented `_add_ocr_language()` helper method
   - Updated `_start_conversion()` to pass new parameters
   - Updated version display to v1.1.0

3. **config.py**:
   - Version bumped to 1.1.0
   - Added `ocrLanguages` default: "eng"
   - Added `enrichFormula` default: false
   - Added `enrichPictureClasses` default: false
   - Added `enrichPictureDescription` default: false

### New Configuration Keys
```json
{
  "version": "1.1.0",
  "defaults": {
    "ocrLanguages": "eng",
    "enrichFormula": false,
    "enrichPictureClasses": false,
    "enrichPictureDescription": false
  }
}
```

### Command Line Generation
With enrichment enabled, generated commands look like:
```bash
/path/to/venv/bin/docling input.pdf \
  --to md \
  --output /output \
  --ocr \
  --ocr-lang eng,deu,fra \
  --enrich-formula \
  --enrich-picture-classes \
  --enrich-picture-description
```

---

## 📊 UI Changes

### Before (v1.0.1)
```
Processing Options:
Row 0: [Mode] [Enable OCR] [Force OCR] [Pipeline]
```

### After (v1.1.0)
```
Processing Options:
Row 0: [Mode] [Enable OCR] [Force OCR] [Pipeline]
Row 1: [OCR Languages: _____] [EN][DE][FR][ES][IT][ZH]
Row 2: [Enrichment: ☐ Formulas ☐ Picture Classes ☐ Picture Descriptions]
```

**Visual Impact**:
- Processing Options section is slightly taller
- More compact and organized layout
- All options still visible without scrolling

---

## 🔄 Upgrade Instructions

### From v1.0.x to v1.1.0

**Automatic** - No action required!
- Configuration auto-upgrades on first launch
- New defaults are added automatically
- Existing settings are preserved
- Window may resize slightly to accommodate new options

**Manual** (optional):
If you want to reset to defaults:
```bash
rm ~/Library/Application\ Support/DoclingGUI/config.json  # macOS
# Then restart the application
```

---

## 📝 Backward Compatibility

✅ **Fully Backward Compatible**
- All v1.0.x features work exactly the same
- New features are opt-in (all disabled by default except basic OCR)
- Configuration from v1.0.x loads correctly
- No breaking changes

**Defaults Behavior**:
- OCR Language: "eng" (English) - matches v1.0.x behavior
- All enrichment options: Off - matches v1.0.x behavior

---

## 🐛 Known Issues

None at this time.

---

## 🚀 Quick Start

### Installing v1.1.0

**New Installation**:
```bash
cd /Users/stefanlenz/scripts/docling-gui
./setup.sh
./run.sh
```

**Upgrading from v1.0.x**:
```bash
cd /Users/stefanlenz/scripts/docling-gui
./run.sh  # That's it! Auto-upgrades on launch
```

### Trying the New Features

**OCR Languages**:
1. Click "Select File" and choose a non-English PDF
2. Click the language preset buttons (e.g., DE for German)
3. Check "Enable OCR"
4. Click "Convert"

**Enrichment**:
1. Select a document with formulas or images
2. Check "Formulas" and/or picture enrichment boxes
3. Click "Convert"
4. Compare output quality with enrichment off vs. on

---

## 📚 Documentation

Updated files:
- ✅ [CHANGELOG.md](CHANGELOG.md) - Detailed version history
- ✅ [CLAUDE.md](CLAUDE.md) - Project status and implementation details
- ✅ This release notes document

Still accurate:
- [README.md](README.md) - Main user documentation
- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [FEATURE_ANALYSIS.md](FEATURE_ANALYSIS.md) - Feature specifications
- [FRAMEWORK_ANALYSIS.md](FRAMEWORK_ANALYSIS.md) - Technical decisions

---

## 🎯 Future Plans

Planned for future releases:
- **v1.2.0**: Advanced options panel (PDF backend, performance tuning)
- **v1.3.0**: Batch processing queue
- **v2.0.0**: Drag-and-drop support, file preview

See [FEATURE_ANALYSIS.md](FEATURE_ANALYSIS.md) for complete roadmap.

---

## 💡 Tips & Tricks

**Multilingual Documents**:
```
For English/German document:
OCR Languages: eng,deu
```

**Academic Papers**:
```
Enable: ☑ Formulas
Enable: ☑ Picture Classes
```

**Image-Heavy Documents**:
```
Enable: ☑ Picture Classes
Enable: ☑ Picture Descriptions
```

**Maximum Quality**:
```
Enable: ☑ Force OCR
Enable: ☑ Formulas
Enable: ☑ Picture Classes
Enable: ☑ Picture Descriptions
OCR Languages: [your languages]
Pipeline: VLM
```

---

## 🙏 Acknowledgments

Built with:
- **Docling**: IBM Research document conversion engine
- **CustomTkinter**: Modern UI framework
- **Python**: Programming language
- **Claude Code**: Development assistance

---

## 📧 Support

For issues or questions:
- Check [README.md](README.md) troubleshooting section
- Review [CHANGELOG.md](CHANGELOG.md) for changes
- See [CLAUDE.md](CLAUDE.md) for technical details

---

**Version**: 1.1.0
**Released**: December 12, 2025
**Tested On**: macOS 15.1 (Sequoia)
**Python**: 3.14.2
**Status**: ✅ Production Ready

**Enjoy the new features!** 🎉
