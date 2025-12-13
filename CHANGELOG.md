# Changelog

All notable changes to the Docling GUI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.5] - 2025-12-13

### Added
- **Drag-and-Drop File Support**: True drag-and-drop using tkinterdnd2 library
  - Drop files or folders directly into the queue panel
  - Visual feedback during drag operations (icon changes to 📥, background highlights)
  - Cross-platform path parsing for Windows and macOS/Linux
  - Graceful fallback to click-to-add when tkdnd native library unavailable
  - DnD status shown in console on startup ("Drag-and-drop: Enabled/Disabled")

- **Whisper ASR Model Downloads**: Two new model download options
  - Whisper Large v3 (openai/whisper-large-v3) for ASR pipeline
  - Whisper Large v3 Turbo (openai/whisper-large-v3-turbo) for faster ASR
  - Model download dialog expanded to 450x380 to accommodate 5 options

### Changed
- Version updated to 1.5.5
- Added `tkinterdnd2>=0.3.0` to requirements.txt
- Download dialog now has 5 model options (was 3)

### Technical
- Added `DND_AVAILABLE` flag for runtime detection
- Created `_DnDCTk` class combining CTk with TkinterDnD.DnDWrapper
- Added `_init_dnd()` method for graceful DnD initialization
- Added `_setup_dnd()` in FileDropZone for drop target registration
- Added `_parse_dnd_data()` for cross-platform path parsing
- Added `download_whisper_large_v3` and `download_whisper_large_v3_turbo` parameters

### Notes
- tkinterdnd2 requires compatible Tcl/Tk version
- Python 3.14's Tcl/Tk may not be compatible with bundled tkdnd library
- Falls back gracefully to click-to-add functionality

---

## [1.5.2] - 2025-12-13

### Added
- **Complete UI Redesign**: Two-panel sidebar layout
  - Left sidebar with all conversion controls in collapsible sections
  - Right panel with batch queue and console output
  - Component-based modular architecture

- **New Dropdown Controls**:
  - OCR Engine dropdown (auto, easyocr, tesseract, tesserocr, rapidocr, ocrmac)
  - OCR Language dropdown (18 languages with friendly names)
  - PDF Backend dropdown (pypdfium2, dlparse_v1, dlparse_v2, dlparse_v4)
  - Table Mode dropdown (fast, accurate)
  - Image Export Mode dropdown (placeholder, embedded, referenced)

- **New Features**:
  - PDF Password field for protected documents
  - Collapsible sections for Output, Processing, and Debug options
  - Enhanced batch queue visualization with status indicators
  - Clear Log button in console panel

### Changed
- Complete restructure of UI code into modular components
- Version updated to 1.5.2
- Window default size changed to 1200x900

### New Files
- `ui/sidebar.py` - Left sidebar with all controls
- `ui/queue_panel.py` - Batch queue visualization
- `ui/console_panel.py` - Console with Clear Log
- `ui/widgets/collapsible_section.py` - Expandable sections
- `ui/widgets/file_drop_zone.py` - File add zone
- `ui/widgets/queue_item_widget.py` - Individual queue items

---

## [1.4.0] - 2025-12-13

### Added
- **OCR Engine Selection**: Choose from 6 OCR engines
  - auto, easyocr, tesseract, tesserocr, rapidocr, ocrmac
  - Pre-validation with helpful error messages if engine unavailable
  - Installation instructions for missing dependencies

- **VLM Model Selection**: Choose from 6 VLM models
  - smoldocling, smoldocling_vllm, granite_vision
  - granite_vision_vllm, granite_vision_ollama, got_ocr_2

- **New Processing Options**:
  - Extract Tables toggle
  - Enrich Code toggle

- **Advanced Debug & Visualization Section**: 5 toggles
  - Show Layout Boxes
  - Visualize Layout Clusters
  - Visualize PDF Cells
  - Visualize OCR Cells
  - Visualize Table Cells

### Fixed
- TypeError with missing convert() parameters
- AttributeError in queue widget updates

### Changed
- Version updated to 1.4.0
- Better error handling in batch processing

---

## [1.3.0] - 2025-12-13

### Added
- **Batch Queue System**: Process multiple files sequentially
  - Add multiple files via file dialog
  - Add folders with recursive file scanning
  - Per-file status tracking with color-coded icons
  - Queue statistics (pending, processing, completed, failed)
  - Clear Completed / Clear All buttons

- **Queue Visualization**:
  - Visual queue item display with status icons
  - Individual item removal
  - Sequential queue processing
  - Queue completion summary

### Changed
- Version updated to 1.3.0
- UI reorganized to accommodate queue panel
- Convert button shows pending count

### Technical
- Added `core/queue.py` with ConversionQueue and QueueItem classes
- Added QueueItemStatus enum (PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED)
- Added queue statistics tracking
- Added `_process_next_in_queue()` for sequential processing

---

## [1.2.4] - 2025-12-12

### Fixed
- **Critical Bug**: Offline mode now works correctly with downloaded models
  - Fixed artifacts path: Now passes `{artifacts_path}/models` to docling CLI
  - Previous (broken): Was passing `{artifacts_path}` which pointed to wrong location
  - Models are downloaded to `models/` subdirectory by docling-tools
  - Docling CLI expects `--artifacts-path` to point to the models directory
  - Validation now checks correct model directory structure
  - Resolves GitHub issue #1: "After downloading models, offline mode still shows models not loaded"

### Changed
- Updated `build_command()` to append `/models` to artifacts path
- Updated `check_models_downloaded()` to check proper directory structure
- Now validates `models/docling-project--docling-layout-heron/` directory
- Checks for both `model.safetensors` and `config.json` in model directory
- Better error messages showing actual missing model names

### Technical
- `build_command()` now passes `{artifacts_path}/models` to `--artifacts-path` flag
- `check_models_downloaded()` checks `{artifacts_path}/models/{model_name}/`
- Validates layout model: `docling-project--docling-layout-heron`
- Returns descriptive missing model messages (e.g., "model_name/model.safetensors")
- Handles missing models directory gracefully

### Example
Before: `--artifacts-path /Users/user/.cache/docling` ❌ (wrong)
After: `--artifacts-path /Users/user/.cache/docling/models` ✅ (correct)

---

## [1.2.3] - 2025-12-12

### Added
- **Offline Mode Model Validation**: Prevents conversion errors by checking if models are downloaded
  - Added `check_models_downloaded()` method to verify required model files exist
  - Validates model availability before starting offline mode conversion
  - Shows detailed error dialog if models are missing
  - Lists missing files and provides step-by-step guidance
  - Suggests downloading models or switching to online mode
  - Prevents `FileNotFoundError: Missing safe tensors file` error

### Changed
- Offline mode conversion now validates model availability first
- Error messages are more helpful with actionable instructions
- Configuration version updated to 1.2.3

### Fixed
- **Critical**: Offline mode no longer fails with cryptic error when models not downloaded
- Users now get clear guidance on how to fix missing models issue
- UI state properly restored when validation fails

### Technical
- Added `check_models_downloaded(artifacts_path)` to `DoclingConverter` class
  - Returns tuple: (all_found: bool, missing_files: list[str])
  - Checks for required files: model.safetensors, config.json
- Added validation in `_start_conversion()` before processing
- Restores UI state (buttons, progress bar) when validation fails
- Error dialog provides detailed troubleshooting steps

### Error Message Example
```
Offline Mode: Required models not found!

Missing files in /Users/user/.cache/docling:
  • model.safetensors
  • config.json

To use Offline mode:
1. Click '📥 Download Models' button
2. Select 'All Standard Models'
3. Wait for download to complete
4. Try conversion again

Or switch to Online mode to download models automatically.
```

---

## [1.2.2] - 2025-12-12

### Added
- **Console Log to File Feature**: Save console output to timestamped log files
  - New checkbox "💾 Save to Log File" in Console Output section
  - Automatically creates timestamped log files (format: `docling_log_YYYYMMDD_HHMMSS.txt`)
  - Default log directory: `~/Documents/docling_logs/`
  - Custom log directory configurable in settings
  - Log files include header with start time and footer with end time
  - Real-time writing to log file as console output appears
  - Auto-closes log file on application exit or when logging disabled
  - Persistent setting saved in configuration
  - Error handling with automatic fallback if file write fails

### Changed
- Console Output section title bar now includes log enable checkbox
- Log files are automatically created when checkbox is enabled
- Log files are automatically closed when checkbox is disabled or app closes
- Configuration version updated to 1.2.2

### Technical
- Added `enableLogging` boolean to configuration (default: false)
- Added `logDirectory` path to configuration (default: `~/Documents/docling_logs`)
- Added `log_file_handle` and `current_log_file` state variables
- Added `_create_log_file()` method to create timestamped log files
- Added `_close_log_file()` method to properly close log files with footer
- Added `_on_log_enable_change()` callback for checkbox state changes
- Enhanced `_log_console()` to write to file when logging enabled
- Updated `_on_closing()` to close log file on application exit
- Added auto-start logging on app launch if previously enabled
- Imported `datetime` module for timestamp generation

### UI Changes
- Console Output section title bar reorganized with checkbox on right
- Log file path shown in console when logging enabled/disabled
- Visual confirmation messages for log enable/disable actions

---

## [1.2.1] - 2025-12-12

### Added
- **SmolVLM-256M-Instruct Model Download**: Third option in model download dialog
  - New checkbox for HuggingFaceTB/SmolVLM-256M-Instruct model
  - Command: `docling-tools models download-hf-repo HuggingFaceTB/SmolVLM-256M-Instruct`
  - Vision-Language Model for enhanced document understanding
  - Dialog expanded from 400x250 to 500x300 to accommodate new option

- **Collapsible Processing Options**: Toggle visibility of options section
  - New toggle button (▼/▶) next to "Processing Options" title
  - Click to show/hide all processing options
  - Saves screen space when options not needed
  - Default state: visible (expanded)

### Changed
- Model download dialog now has 3 checkboxes (was 2):
  1. All Standard Models
  2. SmolDocling-256M
  3. SmolVLM-256M-Instruct (NEW)
- Processing Options section can now be collapsed/expanded
- Variable renamed: `download_smol_var` → `download_smoldocling_var` for clarity

### Technical
- Added `download_smolvlm` parameter to `DoclingConverter.download_models()`
- Added SmolVLM download logic in `download_models()` method
- Added `_toggle_options()` method to toggle visibility
- Added `options_visible` BooleanVar to track state
- Added `toggle_btn` button widget for expand/collapse
- Changed `opts_container` to instance variable `self.opts_container`
- Updated all references to use `self.opts_container`

### UI Changes
- Toggle button shows ▼ when expanded, ▶ when collapsed
- Options container uses `grid_remove()`/`grid()` for smooth hiding/showing
- No window resize needed - space is reclaimed when collapsed

---

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
