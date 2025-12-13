# GEMINI.md

This file provides guidance to Gemini (gemini.google.com) when working with code in this repository.

## Project Overview

This is a GUI wrapper for the Docling command-line tool, which converts various document formats (PDF, DOCX, PPTX, HTML, images, etc.) to different output formats (Markdown, JSON, HTML, text).

**Current Status**: v1.5.1 - Major UI redesign with sidebar layout, OCR dropdowns
**Framework**: Python + CustomTkinter
**Architecture**: Component-based modular design with sidebar layout
**Latest Release**: Complete UI overhaul with two-panel sidebar layout, enhanced batch queue visualization, and component-based architecture

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
- `--from`: Input formats (docx, pptx, html, image, pdf, asciidoc, md, csv, xlsx, xml_uspto, xml_jats, mets_gbs, json_docling, audio) - defaults to Markdown
- `--to`: Output formats (md, json, html, html_split_page, text, doctags) - defaults to Markdown
- `--output`: Output directory (defaults to current directory)

**Processing Options:**
- `--pipeline`: Processing pipeline (standard, vlm, asr) - default: standard
- `--vlm-model`: VLM model choice (smoldocling, smoldocling_vllm, granite_vision, granite_vision_vllm, granite_vision_ollama, got_ocr_2)
- `--asr-model`: ASR model for audio/video (whisper_tiny, whisper_small, whisper_medium, whisper_base, whisper_large, whisper_flash, whisper_turbo)
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
```bash
docling /path/to/file.pdf --to md --output /output/dir --ocr --image-export-mode embedded
```

**Error Handling:**
- Validate that Docling CLI is installed and accessible
- Check input paths exist before processing
- Display stderr output from Docling in the console view
- Handle process termination and errors gracefully

## Current Implementation

### Project Structure (v1.5.1)
```
docling-gui/
├── main.py                    # Application entry point
├── config.py                  # Configuration management (JSON-based)
├── requirements.txt           # Dependencies (customtkinter, docling, Pillow)
├── DEVELOP_v1.5.0.md         # Development plan for v1.5.0
├── core/
│   ├── __init__.py
│   ├── converter.py          # DoclingConverter - handles Docling CLI integration
│   └── queue.py              # ConversionQueue - batch queue management
└── ui/
    ├── __init__.py
    ├── main_window.py        # MainWindow - two-panel layout orchestration
    ├── sidebar.py            # Sidebar - left panel with all controls
    ├── queue_panel.py        # QueuePanel - batch queue visualization
    ├── console_panel.py      # ConsolePanel - console output with logging
    └── widgets/
        ├── __init__.py
        ├── collapsible_section.py   # CollapsibleSection - expandable frames
        ├── file_drop_zone.py        # FileDropZone - file add area
        └── queue_item_widget.py     # QueueItemWidget - individual queue items
```

### Features Implemented (v1.5.1)

**UI/UX Overhaul:**
- ✅ Two-panel sidebar layout (sidebar + main area)
- ✅ Component-based architecture (modular, maintainable code)
- ✅ Collapsible sections (Output Config, Processing Options, Debug)
- ✅ Visual batch queue with file status indicators
- ✅ File drop zone with click-to-add functionality
- ✅ Improved console panel with Clear Log button
- ✅ Status bar with progress indicator

**Batch Queue Processing:**
- ✅ Add multiple files via dialog
- ✅ Add folder with recursive file scanning
- ✅ Visual queue item display with status icons
- ✅ Individual item removal
- ✅ Clear Completed / Clear All buttons
- ✅ Sequential queue processing
- ✅ Per-file status tracking (pending, processing, completed, failed)
- ✅ Queue completion summary

**Processing Options:**
- ✅ Online/Offline mode selection
- ✅ Pipeline selection (standard, vlm, asr)
- ✅ OCR settings with language presets
- ✅ Enrichment options: Formulas, Picture Classes, Picture Descriptions
- ✅ Extract Tables option (NEW)
- ✅ Enrich Code option (NEW)
- ✅ Model download functionality

**Debug & Visualization:**
- ✅ Show Layout Boxes
- ✅ Visualize Layout Clusters
- ✅ Visualize PDF Cells
- ✅ Visualize OCR Cells
- ✅ Visualize Table Cells

**Inherited Features (from v1.2.x):**
- ✅ All output formats (md, json, html, html_split_page, text, doctags)
- ✅ Console log to file with timestamps
- ✅ Offline mode model validation
- ✅ Persistent configuration
- ✅ Window geometry persistence

### Not Yet Implemented (Future Phases)
- ⏳ True drag-and-drop support (requires tkinterdnd2)
- ⏳ URL input support
- ⏳ File preview panel
- ⏳ Configuration profiles/presets
- ⏳ Settings dialog/window
- ⏳ Export to multiple formats simultaneously

### Key Classes and Methods (v1.5.0)

**config.py - Config**:
- `get(*keys, default)`: Get nested config value
- `set(*keys, value)`: Set nested config value and save

**core/converter.py - DoclingConverter**:
- `check_docling_installed()`: Verify Docling availability
- `check_models_downloaded(artifacts_path)`: Check offline mode models
- `build_command(...)`: Construct Docling CLI command
- `convert(...)`: Execute conversion in background thread
- `download_models(...)`: Download models for offline operation
- `cancel()`: Terminate running conversion

**core/queue.py - ConversionQueue**:
- `add_file(path)` / `add_files(paths)`: Add files to queue
- `add_folder(path, recursive)`: Add folder contents to queue
- `get_next_pending()`: Get next item to process
- `update_status(id, status)`: Update item status
- `clear_completed()` / `clear_queue()`: Queue management
- `get_statistics()`: Get queue stats (pending, completed, failed)

**ui/main_window.py - MainWindow**:
- `_create_widgets()`: Build two-panel layout
- `_add_files_to_queue()`: Handle file addition
- `_start_conversion()`: Start queue processing
- `_process_next_in_queue()`: Process queue items
- `_on_queue_complete()`: Handle queue completion

**ui/sidebar.py - Sidebar**:
- `get_conversion_params()`: Get all conversion parameters
- `set_processing_state(is_processing)`: Update UI state
- `update_convert_button(text)`: Update button text

**ui/queue_panel.py - QueuePanel**:
- `add_item(item)` / `add_items(items)`: Add queue items
- `update_item_status(id, status)`: Update item display
- `refresh()`: Refresh entire queue display
- `clear_completed()` / `clear_all()`: Queue management

**ui/console_panel.py - ConsolePanel**:
- `append(text)`: Add text to console
- `clear()`: Clear console
- `close()`: Close log file

**ui/widgets/collapsible_section.py - CollapsibleSection**:
- `toggle()` / `expand()` / `collapse()`: Control visibility
- `content` property: Access content frame for child widgets

### Configuration File Location
- **macOS**: `~/Library/Application Support/DoclingGUI/config.json`
- **Windows**: `%APPDATA%\DoclingGUI/config.json`

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

### New Features (v1.2.1)

**SmolVLM-256M-Instruct Model Download**:
- **Feature**: Third model option in offline download dialog
- **Implementation**:
  - Added `download_smolvlm` parameter to `DoclingConverter.download_models()`
  - New checkbox in download dialog: "SmolVLM-256M-Instruct (Vision-Language Model)"
  - Downloads HuggingFaceTB/SmolVLM-256M-Instruct model
  - Command: `docling-tools models download-hf-repo HuggingFaceTB/SmolVLM-256M-Instruct`
  - Dialog resized from 400x250 to 500x300 to accommodate three options
- **Benefits**:
  - Vision-Language Model for enhanced document understanding
  - Better handling of complex visual layouts
  - Improved VLM pipeline performance
- **UI Location**: Model download dialog (accessed via "📥 Download Models" button)

**Collapsible Processing Options**:
- **Feature**: Toggle button to show/hide entire Processing Options section
- **Implementation**:
  - Added toggle button (▼/▶) next to "Processing Options" title
  - Uses `grid_remove()`/`grid()` for smooth visibility toggling
  - Stored in `self.opts_container` instance variable
  - State tracked with `options_visible` BooleanVar
  - Button text changes: ▼ when expanded, ▶ when collapsed
- **Benefits**:
  - Saves screen space when options not needed
  - Reduces visual clutter for simple conversions
  - Quick access to toggle without scrolling
  - No window resize needed
- **Default State**: Expanded (visible)
- **UI Location**: Processing Options section header

**Configuration Updates**:
- Version bumped to 1.2.1
- No new configuration keys (backward compatible)

**Methods Added**:
- `MainWindow._toggle_options()`: Toggles visibility of processing options container
  - Manages `grid_remove()` and `grid()` calls
  - Updates toggle button text
  - Updates `options_visible` state

**Variables Changed**:
- Renamed: `download_smol_var` → `download_smoldocling_var` for clarity
- Changed: `opts_container` → `self.opts_container` (instance variable)

**Download Dialog Layout**:
```
┌──────────────────────────────────────────┐
│     Select Models to Download           │
├──────────────────────────────────────────┤
│  ☑ All Standard Models                  │
│  ☐ SmolDocling-256M                     │
│  ☐ SmolVLM-256M-Instruct      [NEW]     │
│                                          │
│        [Download]  [Cancel]              │
└──────────────────────────────────────────┘
```

**Model Download Commands**:
```bash
# All standard models
docling-tools models download

# SmolDocling-256M (VLM for complex layouts)
docling-tools models download-hf-repo ds4sd/SmolDocling-256M-preview

# SmolVLM-256M-Instruct (Vision-Language Model) - NEW
docling-tools models download-hf-repo HuggingFaceTB/SmolVLM-256M-Instruct
```

### New Features (v1.2.2)

**Console Log to File**:
- **Feature**: Save all console output to timestamped log files
- **Implementation**:
  - Added "💾 Save to Log File" checkbox in Console Output section header
  - Checkbox state persists in configuration (`general.enableLogging`)
  - Log directory configurable (`general.logDirectory`)
  - Default location: `~/Documents/docling_logs/`
  - Log files named: `docling_log_YYYYMMDD_HHMMSS.txt`
  - Log file includes header with start timestamp
  - Log file includes footer with end timestamp
  - Real-time writing: every console message immediately written to file
  - Auto-flush after each write for reliability
  - Automatic log file creation when checkbox enabled
  - Automatic log file closure when checkbox disabled or app exits
  - Error handling: disables logging if file write fails
- **Benefits**:
  - Keep permanent records of all conversions
  - Debugging and troubleshooting
  - Track processing history
  - Share conversion logs with team/support
  - Audit trail for document processing
- **UI Location**: Console Output section header, next to title

**Log File Format**:
```
Docling GUI Log File
Started: 2025-12-12 18:57:23
============================================================

[Console output here...]

============================================================
Log ended: 2025-12-12 19:15:42
```

**Configuration Updates**:
- Version bumped to 1.2.2
- New configuration keys:
  - `enableLogging` (boolean, default: false)
  - `logDirectory` (string, default: `~/Documents/docling_logs`)

**Methods Added**:
- `MainWindow._create_log_file()`: Creates new timestamped log file
  - Creates log directory if needed
  - Opens file with UTF-8 encoding
  - Writes header with timestamp
  - Returns success/failure status
- `MainWindow._close_log_file()`: Closes log file gracefully
  - Writes footer with end timestamp
  - Closes file handle
  - Cleans up state variables
- `MainWindow._on_log_enable_change()`: Handles checkbox state changes
  - Saves preference to configuration
  - Creates/closes log file as needed
  - Shows confirmation in console

**Enhanced Methods**:
- `MainWindow._log_console(text)`: Updated to write to file
  - Writes to console textbox (unchanged)
  - Additionally writes to log file if enabled
  - Flushes file after each write
  - Disables logging on write errors
- `MainWindow._on_closing()`: Updated to close log file
  - Ensures log file is properly closed on app exit
  - Prevents data loss

**State Variables Added**:
- `self.log_file_handle`: File handle for current log file
- `self.current_log_file`: Path to current log file
- `self.enable_log_var`: BooleanVar for checkbox state

**Auto-Start Behavior**:
- If logging was enabled in previous session, automatically creates new log file on app launch
- User sees immediate feedback in console

**Error Handling**:
- File creation errors shown in error dialog
- Checkbox automatically unchecked on error
- Write errors disable logging and show message in console
- Graceful fallback: continues operation without logging

**Use Cases**:
```
1. Troubleshooting failed conversions
   - Enable logging before conversion
   - Review log file for error details

2. Batch processing audit trail
   - Enable logging at start
   - Run multiple conversions
   - Single log file records all operations

3. Support requests
   - Enable logging
   - Reproduce issue
   - Share log file with support team

4. Process documentation
   - Keep logs for compliance
   - Archive conversion records
   - Track what was converted when
```

### New Features (v1.2.3)

**Offline Mode Model Validation**:
- **Feature**: Prevents conversion errors by validating model availability before offline mode conversion
- **Problem Solved**: Users no longer encounter cryptic `FileNotFoundError: Missing safe tensors file` errors
- **Implementation**:
  - Added `check_models_downloaded(artifacts_path)` method to `DoclingConverter`
  - Validates presence of required model files before starting conversion
  - Checks for: `model.safetensors`, `config.json` in artifacts directory
  - Returns tuple: (all_found: bool, missing_files: list[str])
  - Validation runs automatically when offline mode is selected
  - Shows detailed error dialog if models are missing
  - Lists specific missing files
  - Provides step-by-step instructions to fix the issue
  - UI state properly restored when validation fails
- **Benefits**:
  - Prevents confusing error messages mid-conversion
  - Saves user time by catching issue early
  - Provides actionable guidance on how to fix
  - Improves user experience for offline mode
  - Reduces support requests
- **Trigger**: Automatic validation when user clicks "Convert" in offline mode

**Error Dialog Content**:
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

**Configuration Updates**:
- Version bumped to 1.2.3
- No new configuration keys (backward compatible)

**Methods Added**:
- `DoclingConverter.check_models_downloaded(artifacts_path)`: Validates model file presence
  - Takes artifacts directory path as parameter
  - Checks for required model files
  - Returns success status and list of missing files
  - Used before offline conversions

**Enhanced Methods**:
- `MainWindow._start_conversion()`: Added offline mode validation
  - Calls `check_models_downloaded()` when offline mode selected
  - Shows error dialog if models missing
  - Restores UI state (buttons, progress bar, status)
  - Prevents conversion from starting
  - User can then download models or switch to online mode

**Validation Logic**:
```python
if self.processing_mode_var.get() == "offline":
    artifacts_path = self.config.get("processing", "artifactsPath")
    models_ok, missing_files = self.converter.check_models_downloaded(artifacts_path)
    if not models_ok:
        # Show error dialog with missing files and instructions
        # Restore UI state
        # Return early to prevent conversion
```

**User Flow**:
```
1. User selects file and offline mode
2. User clicks "Convert"
3. System validates model availability
4. If missing:
   - Show error dialog with instructions
   - User downloads models via "📥 Download Models" button
   - User retries conversion
5. If present:
   - Conversion proceeds normally
```

**Error Prevention**:
- **Before v1.2.3**: Conversion would start, then fail mid-process with technical error
- **After v1.2.3**: Validation catches issue immediately with helpful guidance

**Required Files Checked**:
- `model.safetensors`: Layout model weights
- `config.json`: Model configuration

**Future Enhancements** (not yet implemented):
- Check for additional VLM/ASR model files when those pipelines selected
- Estimate download size when suggesting model download
- Auto-download models when offline mode first enabled
