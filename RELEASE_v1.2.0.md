# Docling GUI v1.2.0 - Release Notes

**Release Date**: December 12, 2025
**Type**: Minor Feature Release
**Status**: ✅ Production Ready

## 🎉 What's New

### Image Export Mode Selector
Choose how images are handled in your output documents.

**Features**:
- **Dropdown Menu**: Select from three image export modes
  - 🖼️ **Embedded**: Include images directly in output (default)
  - 📝 **Placeholder**: Use placeholders instead of actual images
  - 🔗 **Referenced**: Save images separately and link in output
- **Always Applied**: Mode is now always included in the command (was conditional before)
- **Persistent**: Your selection is saved in configuration

**Use Cases**:
- **Embedded**: Best for self-contained documents, smaller file counts
- **Placeholder**: Faster processing, reduced file sizes, focus on text content
- **Referenced**: Better for large documents with many images, easier image management

**Example**:
```bash
# With referenced mode:
docling input.pdf --to md --output /out --image-export-mode referenced
```

---

### Verbose Mode Control
Control logging verbosity for troubleshooting and detailed progress tracking.

**Features**:
- **Verbosity Levels**: Choose from three logging levels
  - 0️⃣ **Normal**: Standard output (default)
  - 1️⃣ **Info**: Info-level logging with `-v` flag
  - 2️⃣ **Debug**: Debug-level logging with `-vv` flag
- **Real-time Output**: See detailed progress in console
- **Saved Configuration**: Preference persists between sessions

**When to Use**:
- **Level 0 (Normal)**: Production use, clean output
- **Level 1 (Info)**: Moderate detail, useful for tracking conversion progress
- **Level 2 (Debug)**: Maximum detail for troubleshooting issues

**Example**:
```bash
# With debug logging:
docling input.pdf --to md --output /out -vv
```

---

### Model Download Feature
Download models for true offline operation without internet dependency.

**Features**:
- **New Button**: "📥 Download Models" in Processing Options section
- **Modal Dialog**: Choose which models to download
  - ✅ **All Standard Models**: Downloads complete set with `docling-tools models download`
  - ✅ **SmolDocling-256M**: Downloads preview model with `docling-tools models download-hf-repo ds4sd/SmolDocling-256M-preview`
- **Real-time Progress**: Live download progress shown in console
- **Progress Indicators**: Progress bar and status updates during download
- **Background Processing**: UI remains responsive during download
- **Completion Notifications**: Success or warning messages on completion

**Benefits**:
- ✅ Enables true offline operation after download
- ✅ No internet required for processing
- ✅ Better privacy for sensitive documents
- ✅ Faster processing (no download delays)

**How to Use**:
1. Click "📥 Download Models" button
2. Select desired models in the dialog
3. Click "Start Download"
4. Monitor progress in console
5. Wait for completion notification
6. Switch to Offline mode and process without internet

**Commands Run**:
```bash
# All standard models
docling-tools models download

# SmolDocling preview model
docling-tools models download-hf-repo ds4sd/SmolDocling-256M-preview
```

---

## 🔧 Technical Changes

### Updated Files
1. **core/converter.py**:
   - Modified `build_command()` to always include `--image-export-mode`
   - Added `verbose` parameter (0, 1, 2) with flag mapping
   - Added `download_models()` method for model downloads
   - Streams output to console in real-time during downloads
   - Runs downloads in background thread

2. **ui/main_window.py**:
   - Added Image Export Mode dropdown with all 3 options
   - Added Verbosity dropdown with 3 levels
   - Added "📥 Download Models" button
   - Implemented `_download_models()` method with modal dialog
   - Implemented `_on_download_complete()` callback handler
   - Added `_on_verbose_change()` helper for dropdown parsing
   - Updated `_start_conversion()` to pass new parameters
   - Reorganized Row 3 of Processing Options
   - Updated version display to v1.2.0

3. **config.py**:
   - Version bumped to 1.2.0
   - Added `verbose` default: 0
   - Window height increased from 750px to 800px

### New Configuration Keys
```json
{
  "version": "1.2.0",
  "defaults": {
    "imageExportMode": "embedded",
    "verbose": 0
  },
  "window": {
    "height": 800
  }
}
```

### Command Line Generation
With all features enabled:
```bash
/path/to/venv/bin/docling input.pdf \
  --to md \
  --output /output \
  --ocr \
  --ocr-lang eng,deu \
  --image-export-mode referenced \
  -vv \
  --enrich-formula \
  --enrich-picture-classes
```

---

## 📊 UI Changes

### Before (v1.1.0)
```
Processing Options:
Row 0: [Mode] [Enable OCR] [Force OCR] [Pipeline]
Row 1: [OCR Languages: _____] [EN][DE][FR][ES][IT][ZH]
Row 2: [Enrichment: ☐ Formulas ☐ Picture Classes ☐ Picture Descriptions]
```

### After (v1.2.0)
```
Processing Options:
Row 0: [Mode] [Enable OCR] [Force OCR] [Pipeline]
Row 1: [OCR Languages: _____] [EN][DE][FR][ES][IT][ZH]
Row 2: [Enrichment: ☐ Formulas ☐ Picture Classes ☐ Picture Descriptions]
Row 3: [Image Export: ▼] [Verbosity: ▼] [📥 Download Models]
```

**Visual Impact**:
- Processing Options section has 4 rows now (was 3)
- Window height increased to 800px (from 750px)
- All options still visible without scrolling
- More compact and organized layout

---

## 🔄 Upgrade Instructions

### From v1.1.0 to v1.2.0

**Automatic** - No action required!
- Configuration auto-upgrades on first launch
- New defaults are added automatically
- Existing settings are preserved
- Window resizes automatically to accommodate new row

**Manual** (optional):
If you want to reset to defaults:
```bash
rm ~/Library/Application\ Support/DoclingGUI/config.json  # macOS
# Then restart the application
```

---

## 📝 Backward Compatibility

✅ **Fully Backward Compatible**
- All v1.1.0 features work exactly the same
- All v1.0.x features work exactly the same
- New features use sensible defaults matching previous behavior
- No breaking changes

**Defaults Behavior**:
- Image Export Mode: "embedded" - matches v1.1.0 behavior
- Verbose: 0 (normal) - matches v1.1.0 behavior
- All v1.1.0 defaults preserved

---

## 🐛 Known Issues

None at this time.

---

## 🚀 Quick Start

### Installing v1.2.0

**New Installation**:
```bash
cd /Users/stefanlenz/scripts/docling-gui
./setup.sh
./run.sh
```

**Upgrading from v1.1.0 or v1.0.x**:
```bash
cd /Users/stefanlenz/scripts/docling-gui
./run.sh  # That's it! Auto-upgrades on launch
```

### Trying the New Features

**Image Export Modes**:
1. Open the GUI
2. In Processing Options, locate the "Image Export:" dropdown
3. Try different modes:
   - "embedded" for self-contained output
   - "placeholder" for faster processing
   - "referenced" for separate image files
4. Process a document and compare results

**Verbose Mode**:
1. Set Verbosity to "1 (Info)" or "2 (Debug)"
2. Click "Convert" on a document
3. Observe detailed logging in the console
4. Use for troubleshooting or understanding processing steps

**Model Download**:
1. Click "📥 Download Models" button
2. In the dialog, check desired models:
   - "All Standard Models" for complete offline support
   - "SmolDocling-256M" for the preview model
3. Click "Start Download"
4. Watch progress in console (may take several minutes)
5. After completion, switch to Offline mode
6. Process documents without internet connection

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
- [RELEASE_v1.1.0.md](RELEASE_v1.1.0.md) - v1.1.0 release notes
- [DOCLING_FIX.md](DOCLING_FIX.md) - v1.0.1 fix documentation

---

## 🎯 Future Plans

Planned for future releases:
- **v1.3.0**: Batch processing queue
- **v1.4.0**: Advanced options panel (PDF backend, performance tuning)
- **v2.0.0**: Drag-and-drop support, file preview

See [FEATURE_ANALYSIS.md](FEATURE_ANALYSIS.md) for complete roadmap.

---

## 💡 Tips & Tricks

**Offline Workflow**:
```
1. Download Models (one-time setup)
2. Switch Mode to "Offline"
3. Process documents without internet
4. Perfect for sensitive documents or air-gapped systems
```

**Troubleshooting**:
```
1. Set Verbosity to "2 (Debug)"
2. Run conversion
3. Check console for detailed logs
4. Share logs for support
```

**Optimize for Speed**:
```
Mode: Online
Image Export: Placeholder
Verbosity: 0 (Normal)
Disable unnecessary enrichment options
```

**Maximum Quality**:
```
Enable: ☑ Force OCR
Enable: ☑ Formulas
Enable: ☑ Picture Classes
Enable: ☑ Picture Descriptions
OCR Languages: [your languages]
Pipeline: VLM
Image Export: Embedded
Verbosity: 1 (Info)
```

**Best for Documentation**:
```
Image Export: Referenced
Verbosity: 1 (Info)
This keeps images separate and trackable
```

---

## 🔍 Comparison: v1.0.0 → v1.1.0 → v1.2.0

| Feature | v1.0.0 | v1.1.0 | v1.2.0 |
|---------|--------|--------|--------|
| OCR Language Selection | ❌ | ✅ | ✅ |
| Enrichment Options | ❌ | ✅ | ✅ |
| Image Export Selector | ❌ | ❌ | ✅ |
| Verbose Mode Control | ❌ | ❌ | ✅ |
| Model Download | ❌ | ❌ | ✅ |
| UI Rows | 2 | 3 | 4 |
| Window Height | 750px | 750px | 800px |

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

**Version**: 1.2.0
**Released**: December 12, 2025
**Tested On**: macOS 15.1 (Sequoia)
**Python**: 3.14.2
**Status**: ✅ Production Ready

**Enjoy the enhanced features!** 🎉
