# Changelog

All notable changes to the Docling GUI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-12-12

### Added
- **Image Export Mode Selector**: Dropdown to choose how images are handled
  - Embedded: Include images directly in output (default)
  - Placeholder: Use placeholders instead of actual images
  - Referenced: Save images separately and link in output
  - Available for all output formats
  - Saved in configuration for persistence

- **Verbose Mode Selector**: Control logging verbosity
  - 0 (Normal): Standard output
  - 1 (Info): Info-level logging with `-v` flag
  - 2 (Debug): Debug-level logging with `-vv` flag
  - Useful for troubleshooting and detailed progress tracking
  - Saved in configuration

- **Model Download Feature**: Download models for offline operation
  - New "📥 Download Models" button in Processing Options
  - Dialog with two options:
    - All Standard Models: `docling-tools models download`
    - SmolDocling-256M: `docling-tools models download-hf-repo ds4sd/SmolDocling-256M-preview`
  - Real-time download progress shown in console
  - Progress bar and status indicators during download
  - Success/warning notifications on completion
  - Enables true offline operation after download

### Changed
- Image export mode now always included in command (was conditional before)
- Window default height increased from 750px to 800px to accommodate new UI elements
- Processing Options section now has 4 rows (was 3):
  - Row 0: Mode, OCR Enable, Force OCR, Pipeline
  - Row 1: OCR Languages with preset buttons
  - Row 2: Enrichment options
  - Row 3: Image Export, Verbosity, Download Models button
- Configuration version updated to 1.2.0

### Technical
- Added `verbose` parameter to converter (0, 1, 2 mapping to no flag, -v, -vv)
- Added `download_models()` method to `DoclingConverter` class
- Enhanced `build_command()` to include verbose flags
- Added `_download_models()` UI method with modal dialog
- Added `_on_download_complete()` callback handler
- Added `_on_verbose_change()` helper to parse dropdown selection
- Configuration now stores: `verbose` (default: 0)
- Model downloads run in background thread with real-time output

### Documentation
- Updated CHANGELOG.md with version 1.2.0 details
- Will update CLAUDE.md with new features

---

## [1.1.0] - 2025-12-12

### Added
- **OCR Language Selection**: New input field with preset buttons for common languages
  - Text input field for comma-separated language codes (e.g., "eng,deu,fra")
  - Quick preset buttons for: English (EN), German (DE), French (FR), Spanish (ES), Italian (IT), Chinese (ZH)
  - Languages are added to the field automatically when clicking preset buttons
  - Saved in configuration for persistence between sessions

- **Enrichment Options**: Three new checkboxes for content enrichment
  - **Formulas**: Enable formula enrichment for mathematical expressions
  - **Picture Classes**: Enable automatic picture classification
  - **Picture Descriptions**: Generate descriptive text for images
  - All enrichment options are saved in configuration

### Changed
- Reorganized Processing Options section with better layout
  - Row 0: Mode, OCR Enable, Force OCR, Pipeline
  - Row 1: OCR Languages with preset buttons
  - Row 2: Enrichment options (Formulas, Picture Classes, Picture Descriptions)
- Updated configuration version to 1.1.0
- Updated UI version display to show v1.1.0

### Technical
- Enhanced `DoclingConverter.build_command()` to support new parameters
- Enhanced `DoclingConverter.convert()` to pass through enrichment and language options
- Added `_add_ocr_language()` helper method for language preset buttons
- Configuration now stores: `ocrLanguages`, `enrichFormula`, `enrichPictureClasses`, `enrichPictureDescription`

### Documentation
- Updated CHANGELOG.md with version 1.1.0 details
- Updated CLAUDE.md project status

---

## [1.0.1] - 2025-12-12

### Fixed
- **Docling Virtual Environment Isolation**: Application now correctly uses the virtual environment's Docling installation instead of requiring root-owned system installation
  - Added `_get_docling_path()` method to auto-detect venv docling
  - Modified `build_command()` to use full venv path
  - Enhanced console logging to show which docling is being used
  - No more root/sudo required to run conversions

### Changed
- Converter now prioritizes: venv → python dir → system PATH for docling executable
- Console displays docling path on startup for transparency

### Documentation
- Added DOCLING_FIX.md with detailed fix documentation
- Updated CLAUDE.md with v1.0.1 status and fix details

---

## [1.0.0] - 2025-12-12

### Added - Initial MVP Release

#### Core Features
- **File Selection**: Native file picker for document selection
- **Output Formats**: Support for 6 output formats
  - Markdown (default)
  - JSON
  - HTML
  - HTML (split page)
  - Text
  - Doctags
- **Output Directory**: Configurable output location with "Open Folder" button
- **Processing Modes**:
  - Online mode (default, with automatic model downloads)
  - Offline mode (privacy-focused, uses local artifacts)

#### Processing Options
- **OCR Support**: Enable/disable OCR with Force OCR option
- **Pipeline Selection**: Standard, VLM, ASR pipelines
- **Real-time Console**: Live output from Docling during conversion
- **Progress Tracking**: Visual progress bar and status indicators

#### User Experience
- **Modern UI**: CustomTkinter-based dark theme interface
- **Status Indicators**: Ready/Processing/Complete states
- **Error Handling**: Clear, actionable error messages
- **Success Notifications**: Confirmation dialogs on completion
- **Persistent Settings**: Configuration saved between sessions
  - Window size and position
  - Last used directories
  - Processing preferences

#### Technical Implementation
- **Framework**: Python + CustomTkinter
- **Architecture**: Modular design with separated core/UI logic
- **Configuration**: JSON-based persistent settings
- **Platform Support**: macOS and Windows 11
- **Threading**: Non-blocking UI during conversions
- **Dependencies**:
  - customtkinter >= 5.2.0
  - docling >= 2.0.0
  - Pillow >= 10.0.0

### Project Files
- Main application: `main.py`, `config.py`
- Core logic: `core/converter.py`
- UI: `ui/main_window.py`
- Configuration: JSON files in platform-appropriate locations
- Setup scripts: `setup.sh`, `setup.bat`, `run.sh`, `run.bat`
- Documentation: README.md, QUICKSTART.md, FEATURE_ANALYSIS.md, FRAMEWORK_ANALYSIS.md, PROJECT_SUMMARY.md

### Platform Compatibility
- macOS 12+ (Primary, tested)
- Windows 11 (Ready, untested)
- Python 3.9 - 3.14 required

---

## Release Notes

### Version Numbering
- **Major.Minor.Patch** (Semantic Versioning)
- Major: Breaking changes or complete rewrites
- Minor: New features, backward compatible
- Patch: Bug fixes, backward compatible

### Upgrade Notes

#### 1.0.x → 1.1.0
- New configuration keys added for OCR languages and enrichment options
- Existing configurations will be merged with new defaults
- No breaking changes - fully backward compatible
- Window height may need adjustment to accommodate new UI elements

---

**Note**: For detailed feature specifications, see [FEATURE_ANALYSIS.md](FEATURE_ANALYSIS.md)
**Note**: For framework comparison and technical decisions, see [FRAMEWORK_ANALYSIS.md](FRAMEWORK_ANALYSIS.md)
