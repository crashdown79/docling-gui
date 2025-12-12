# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a GUI wrapper for the Docling command-line tool, which converts various document formats (PDF, DOCX, PPTX, HTML, images, etc.) to different output formats (Markdown, JSON, HTML, text).

**Current Status**: v1.2.0 - Image export mode selector, verbose mode, and model download feature added
**Framework**: Python + CustomTkinter
**Architecture**: Modular design with core conversion logic and UI components separated
**Latest Release**: Added image export mode selector, verbose mode control, and model download button

## Target Platforms

The GUI should be designed to run on:
- **macOS** (primary development platform)
- **Windows 11**

The implementation should handle platform-specific considerations such as:
- File path conventions (forward slashes vs backslashes)
- Command execution methods
- Native UI conventions and behaviors
- File dialog implementations

## Docling CLI Reference

The GUI should expose the following Docling parameters:

**Input/Output:**
- `input_sources` (required): Local file/directory paths or URLs
- `--from`: Input formats (docx, pptx, html, image, pdf, asciidoc, md, csv, xlsx, xml_uspto, xml_jats, mets_gbs, json_docling, audio)
- `--to`: Output formats (md, json, html, html_split_page, text, doctags) - defaults to Markdown
- `--output`: Output directory (defaults to current directory)

**Processing Options:**
- `--pipeline`: Processing pipeline (standard, vlm, asr) - default: standard
- `--vlm-model`: VLM model choice (smoldocling, smoldocling_vllm, granite_vision, granite_vision_vllm, granite_vision_ollama, got_ocr_2)
- `--asr-model`: ASR model for audio/video (whisper_tiny, whisper_small, whisper_medium, whisper_base, whisper_large, whisper_turbo)
- `--pdf-backend`: PDF processing backend (pypdfium2, dlparse_v1, dlparse_v2, dlparse_v4) - default: dlparse_v2
- `--table-mode`: Table structure mode (fast, accurate) - default: accurate

**OCR Options:**
- `--ocr` / `--no-ocr`: Enable/disable OCR (default: enabled)
- `--force-ocr` / `--no-force-ocr`: Replace existing text with OCR (default: disabled)
- `--ocr-engine`: OCR engine (easyocr, ocrmac, rapidocr, tesserocr, tesseract) - default: easyocr
- `--ocr-lang`: Comma-separated language list for OCR

**Image Export:**
- `--image-export-mode`: How to handle images (placeholder, embedded, referenced) - default: embedded
- `--show-layout` / `--no-show-layout`: Show bounding boxes on page images

**Enrichment Options:**
- `--enrich-code` / `--no-enrich-code`: Enable code enrichment model
- `--enrich-formula` / `--no-enrich-formula`: Enable formula enrichment
- `--enrich-picture-classes` / `--no-enrich-picture-classes`: Enable picture classification
- `--enrich-picture-description` / `--no-enrich-picture-description`: Enable picture description

**Advanced Options:**
- `--headers`: HTTP headers for URL sources (JSON string)
- `--artifacts-path`: Model artifacts location
- `--enable-remote-services`: Allow models connecting to remote services
- `--allow-external-plugins`: Enable third-party plugins
- `--abort-on-error`: Stop on first error
- `--document-timeout`: Processing timeout per document (seconds)
- `--num-threads`: Number of processing threads (default: 4)
- `--device`: Accelerator device (auto, cpu, cuda, mps) - default: auto
- `--page-batch-size`: Pages per batch (default: 4)

**Debug Visualization:**
- `--debug-visualize-cells`: Visualize PDF cells
- `--debug-visualize-ocr`: Visualize OCR cells
- `--debug-visualize-layout`: Visualize layout clusters
- `--debug-visualize-tables`: Visualize table cells

**Other:**
- `-v` / `-vv`: Verbosity level (info/debug logging)
- `--version`: Show version information

## GUI Design Considerations

**Essential UI Elements:**
1. File/URL input selector (drag-and-drop support recommended)
2. Output format selection (--to)
3. Output directory selector (--output)
4. Common options section: pipeline, OCR toggle, image export mode
5. Advanced options section (collapsible): all other parameters
6. Process button with progress indicator
7. Output log/console view

**Command Construction:**
The GUI should build and execute commands like:
```
docling /path/to/file.pdf --to md --output /output/dir --ocr --image-export-mode embedded
```

**Error Handling:**
- Validate that Docling CLI is installed and accessible
- Check input paths exist before processing
- Display stderr output from Docling in the console view
- Handle process termination and errors gracefully

## Current Implementation

### Project Structure
```
docling-gui/
├── main.py                 # Application entry point
├── config.py              # Configuration management (JSON-based)
├── requirements.txt       # Dependencies (customtkinter, docling, Pillow)
├── core/
│   ├── __init__.py
│   └── converter.py      # DoclingConverter class - handles Docling integration
└── ui/
    ├── __init__.py
    └── main_window.py    # MainWindow class - CustomTkinter UI
```

### Features Implemented (v1.2.0)
- ✅ File selection via dialog picker
- ✅ Output format selection (all 6 formats)
- ✅ Output directory selection with "Open Folder" button
- ✅ Online/Offline processing mode toggle
- ✅ OCR options (Enable OCR, Force OCR)
- ✅ OCR language selection with preset buttons (v1.1.0)
- ✅ Pipeline selection (Standard, VLM, ASR)
- ✅ Enrichment options: Formulas, Picture Classes, Picture Descriptions (v1.1.0)
- ✅ **Image export mode selector**: Dropdown with all 3 options (NEW in v1.2.0)
- ✅ **Verbose mode control**: 0/1/2 for normal/-v/-vv logging (NEW in v1.2.0)
- ✅ **Model download button**: Download models for offline operation (NEW in v1.2.0)
- ✅ Convert/Cancel buttons with state management
- ✅ Real-time console output from Docling
- ✅ Progress bar with indeterminate mode
- ✅ Status indicators and user feedback
- ✅ Error handling and validation
- ✅ Persistent configuration (saves preferences)
- ✅ Window geometry persistence

### Not Yet Implemented (Future Phases)
- ⏳ Drag-and-drop file support (UI placeholder exists)
- ⏳ Batch queue processing
- ⏳ URL input support
- ⏳ Advanced options panel (PDF backend, VLM/ASR models, enrichment, performance tuning, debug)
- ⏳ File preview panel
- ⏳ Configuration profiles
- ⏳ Settings dialog/window

### Key Classes and Methods

**config.py - Config**:
- `__init__()`: Initialize config, load from JSON
- `get(*keys, default)`: Get nested config value
- `set(*keys, value)`: Set nested config value and save
- `save()`: Persist config to JSON file

**core/converter.py - DoclingConverter**:
- `check_docling_installed()`: Verify Docling availability
- `build_command(...)`: Construct Docling CLI command from parameters
- `convert(...)`: Execute conversion in background thread with callbacks
- `cancel()`: Terminate running conversion

**ui/main_window.py - MainWindow**:
- `_create_widgets()`: Build entire UI layout
- `_create_input_section()`: File selection UI
- `_create_output_section()`: Format and directory selection
- `_create_options_section()`: Processing options (mode, OCR, pipeline)
- `_create_control_section()`: Convert/Cancel buttons
- `_create_progress_section()`: Progress bar and status
- `_create_console_section()`: Console output textbox
- `_start_conversion()`: Validate inputs and start conversion
- `_on_conversion_output(text)`: Handle stdout/stderr from Docling
- `_on_conversion_complete(return_code)`: Handle completion
- `_on_conversion_error(error)`: Handle errors

### Configuration File Location
- **macOS**: `~/Library/Application Support/DoclingGUI/config.json`
- **Windows**: `%APPDATA%\DoclingGUI\config.json`

### Running the Application
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run application
python main.py
```

### Recent Fixes (v1.0.1)

**Docling Virtual Environment Isolation**:
- **Problem**: Application was using system-wide Docling installation requiring root privileges
- **Solution**: Modified `DoclingConverter` to automatically detect and use venv's docling
- **Implementation**:
  - Added `_get_docling_path()` method to detect venv docling executable
  - Updated `build_command()` to use full venv path instead of relying on PATH
  - Enhanced console logging to show which docling is being used
- **Result**: Application now runs entirely with user permissions, no sudo required
- **Details**: See DOCLING_FIX.md for complete documentation

The converter now prioritizes the virtual environment's docling installation:
1. First checks: `venv/bin/docling` (virtual environment)
2. Then checks: Python executable's directory
3. Falls back: System PATH (if needed)

This ensures the GUI always uses the correct, user-owned Docling installation.

### New Features (v1.1.0)

**OCR Language Selection**:
- **Feature**: User-configurable OCR language codes for better text recognition
- **Implementation**:
  - Added `ocr_lang` parameter to converter (passed as `--ocr-lang` to docling)
  - Created text input field for comma-separated language codes
  - Added 6 preset buttons for common languages: EN, DE, FR, ES, IT, ZH
  - Clicking preset buttons adds language codes to the field automatically
  - Handles duplicate detection when adding languages
  - Saved in configuration under `defaults.ocrLanguages`
- **UI Location**: Row 1 of Processing Options section
- **Usage**: Enter codes like "eng,deu,fra" or click preset buttons

**Enrichment Options**:
- **Feature**: Enable AI-powered content enrichment for better document processing
- **Implementation**:
  - Added three boolean parameters: `enrich_formula`, `enrich_picture_classes`, `enrich_picture_description`
  - Each maps to corresponding docling flags: `--enrich-formula`, `--enrich-picture-classes`, `--enrich-picture-description`
  - Implemented as checkboxes in the UI
  - Saved in configuration for persistence
- **Options**:
  1. **Formulas**: Enriches mathematical formulas and expressions
  2. **Picture Classes**: Classifies images (charts, diagrams, photos, etc.)
  3. **Picture Descriptions**: Generates descriptive text for images
- **UI Location**: Row 2 of Processing Options section, labeled "Enrichment:"

**Configuration Updates**:
- Version bumped to 1.1.0
- New defaults added:
  - `ocrLanguages`: "eng" (default to English)
  - `enrichFormula`: false
  - `enrichPictureClasses`: false
  - `enrichPictureDescription`: false

**Methods Added**:
- `MainWindow._add_ocr_language(lang_code)`: Helper to add languages to the OCR field
  - Handles empty field (sets directly)
  - Checks for duplicates before adding
  - Maintains comma-separated format

**Command Generation Example**:
```bash
# With OCR languages and enrichment enabled:
/path/to/venv/bin/docling input.pdf \
  --to md \
  --output /output \
  --ocr \
  --ocr-lang eng,deu \
  --enrich-formula \
  --enrich-picture-classes
```

### New Features (v1.2.0)

**Image Export Mode Selector**:
- **Feature**: Dropdown to choose how images are handled in output
- **Implementation**:
  - Added `image_export_mode` dropdown with all 3 options: "embedded", "placeholder", "referenced"
  - Previously conditional, now always included in command as `--image-export-mode`
  - Default: "embedded" (includes images directly in output)
  - Saved in configuration under `defaults.imageExportMode`
- **Options**:
  1. **Embedded**: Include images directly in output (base64 for JSON/Markdown)
  2. **Placeholder**: Use placeholders instead of actual images
  3. **Referenced**: Save images separately and link in output
- **UI Location**: Row 3 of Processing Options section

**Verbose Mode Control**:
- **Feature**: Control logging verbosity for troubleshooting and detailed progress
- **Implementation**:
  - Added `verbose` parameter to converter (0, 1, 2)
  - Maps to docling flags: 0=no flag, 1=-v, 2=-vv
  - Dropdown shows: "0 (Normal)", "1 (Info)", "2 (Debug)"
  - Saved in configuration under `defaults.verbose`
- **Use Cases**:
  - Level 0: Normal output, production use
  - Level 1: Info-level logging with `-v` for moderate detail
  - Level 2: Debug-level logging with `-vv` for troubleshooting
- **UI Location**: Row 3 of Processing Options section

**Model Download Feature**:
- **Feature**: Download models for true offline operation
- **Implementation**:
  - Added `download_models()` method to `DoclingConverter`
  - Created "📥 Download Models" button in Processing Options
  - Opens modal dialog with two checkbox options:
    1. **All Standard Models**: Runs `docling-tools models download`
    2. **SmolDocling-256M**: Runs `docling-tools models download-hf-repo ds4sd/SmolDocling-256M-preview`
  - Real-time progress shown in console output
  - Progress bar and status indicators during download
  - Success/warning notifications on completion
  - Runs in background thread, doesn't block UI
- **Benefits**:
  - Enables true offline operation after download
  - No internet required for processing
  - Better privacy for sensitive documents
- **UI Location**: Row 3 of Processing Options section

**Configuration Updates**:
- Version bumped to 1.2.0
- Window default height increased from 750px to 800px
- New defaults added:
  - `imageExportMode`: "embedded" (matches previous default behavior)
  - `verbose`: 0 (normal logging)

**UI Layout Changes**:
- Processing Options section now has 4 rows (was 3 in v1.1.0):
  - Row 0: Mode, OCR Enable, Force OCR, Pipeline
  - Row 1: OCR Languages with preset buttons
  - Row 2: Enrichment options (Formulas, Picture Classes, Picture Descriptions)
  - Row 3: Image Export, Verbosity, Download Models button

**Methods Added**:
- `DoclingConverter.download_models(download_all, download_smoldocling, ...)`: Download models for offline use
  - Runs docling-tools commands in background thread
  - Streams output to console in real-time
  - Supports downloading both standard models and SmolDocling
- `MainWindow._download_models()`: Opens modal dialog for model download selection
- `MainWindow._on_download_complete(return_code)`: Handles download completion
- `MainWindow._on_verbose_change(selection)`: Parses verbose dropdown selection

**Command Generation Example**:
```bash
# With all v1.2.0 features:
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
