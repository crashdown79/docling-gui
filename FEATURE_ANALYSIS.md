# Docling GUI - Feature Analysis & Design Specification

## Table of Contents
1. [Core Use Cases](#core-use-cases)
2. [User Workflows](#user-workflows)
3. [Feature Hierarchy](#feature-hierarchy)
4. [Detailed Feature Specifications](#detailed-feature-specifications)
5. [UI Layout Design](#ui-layout-design)
6. [Settings & Configuration](#settings--configuration)
7. [Implementation Priorities](#implementation-priorities)

---

## Core Use Cases

### Use Case 1: Quick Single File Conversion
**Actor**: User needing to convert one document quickly
**Goal**: Convert a PDF to Markdown with default settings
**Steps**:
1. Launch application
2. Drag-and-drop PDF file or click "Select File"
3. Verify output format (Markdown is default)
4. Click "Convert"
5. View progress and results
6. Open output file or output directory

**Frequency**: High - Most common use case

---

### Use Case 2: Batch Processing Multiple Documents
**Actor**: User with a folder of documents to convert
**Goal**: Convert 50+ research papers to Markdown for processing
**Steps**:
1. Click "Add Files" or "Add Folder" to build queue
2. Configure common settings (output format, OCR options)
3. Review queue list (show file names, sizes, status)
4. Click "Process Queue"
5. Monitor progress (X of Y completed, per-file status)
6. Review log for any errors
7. Access all converted files in output directory

**Frequency**: Medium - Power users, batch operations

---

### Use Case 3: Advanced Document Processing with Preview
**Actor**: User needing high-quality extraction with custom settings
**Goal**: Convert legal documents with accurate tables and OCR
**Steps**:
1. Select file
2. Preview document (show page count, format info)
3. Enable advanced options:
   - Force OCR for scanned pages
   - Table mode: accurate
   - Enable formula enrichment
4. Configure output (JSON for structured data)
5. Convert and review results
6. Adjust settings and re-convert if needed

**Frequency**: Medium - Quality-focused users

---

### Use Case 4: Offline Processing Configuration
**Actor**: User without internet access or privacy concerns
**Goal**: Process sensitive documents entirely offline
**Steps**:
1. Open Settings/Preferences
2. Select "Offline Processing" mode
3. Configure artifact path (where models are stored)
4. Download required models (if not already cached)
5. Process documents using local models only
6. Verify no network requests are made

**Frequency**: Low-Medium - Privacy-conscious, air-gapped environments

---

### Use Case 5: URL-based Document Conversion
**Actor**: User wanting to convert web-based documents
**Goal**: Convert online PDFs without manual download
**Steps**:
1. Click "Add URL" or paste URL into input field
2. Optionally configure HTTP headers (for authenticated sources)
3. Select output format
4. Convert (app downloads and processes)
5. View results

**Frequency**: Low-Medium - Web-based documents

---

## User Workflows

### Workflow A: Simple Conversion (80% of users)
```
[Launch] → [Select File] → [Convert] → [View Output]
```
**Time**: < 30 seconds interaction + processing time
**Touches**: 2-3 clicks

---

### Workflow B: Batch Processing (15% of users)
```
[Launch] → [Add Multiple Files] → [Configure Settings] → [Process Queue] → [Monitor Progress] → [Review Results]
```
**Time**: 2-5 minutes setup + processing time
**Touches**: 5-10 clicks

---

### Workflow C: Advanced Configuration (5% of users)
```
[Launch] → [Select File] → [Open Advanced Options] → [Configure Multiple Parameters] → [Save Profile] → [Convert] → [Review] → [Iterate]
```
**Time**: 5-15 minutes setup + processing time
**Touches**: 10-20 clicks

---

## Feature Hierarchy

### Tier 1: Essential Features (MVP)
Must be visible and accessible on main screen:

1. **Input Selection**
   - File picker button
   - Drag-and-drop zone
   - Display selected file(s) info

2. **Output Format Selection**
   - Dropdown: Markdown (default), JSON, HTML, Text, Doctags, HTML (split page)

3. **Output Directory Selection**
   - Directory picker
   - Display current output path
   - "Open output folder" button

4. **Convert Button**
   - Large, prominent "Convert" or "Start Processing" button
   - Cancel button when processing

5. **Progress Indication**
   - Progress bar (0-100%)
   - Current file being processed (for batch)
   - Status text (Processing, Complete, Error)

6. **Console/Log Output**
   - Scrollable text area showing Docling output
   - Color-coded messages (info, warning, error)
   - Auto-scroll to bottom

---

### Tier 2: Important Features
Should be easily accessible, possibly in expandable sections:

7. **Batch Queue Management**
   - "Add Files" / "Add Folder" / "Add URL" buttons
   - Queue list view (file name, size, status)
   - Remove items from queue
   - Clear queue
   - Reorder queue (optional nice-to-have)

8. **Processing Mode Selection**
   - Toggle or radio buttons: "Online" / "Offline"
   - Visual indicator of current mode
   - Warning if offline models not available

9. **Common Processing Options** (expandable section)
   - Pipeline: Standard (default) / VLM / ASR
   - OCR Enable/Disable toggle (enabled by default)
   - Force OCR toggle (disabled by default)
   - Image Export Mode: Embedded (default) / Placeholder / Referenced
   - Table Mode: Accurate (default) / Fast

10. **File Preview**
    - Preview pane showing:
      - File format and size
      - Page count (for PDFs)
      - Basic metadata
      - Thumbnail of first page (optional)

---

### Tier 3: Advanced Features
Collapsed by default, in "Advanced Options" section:

11. **PDF Backend Selection**
    - dlparse_v2 (default), dlparse_v1, dlparse_v4, pypdfium2

12. **OCR Engine Selection**
    - easyocr (default), tesseract, rapidocr, ocrmac, tesserocr

13. **OCR Language Configuration**
    - Text input for comma-separated language codes
    - Common presets (eng, deu, fra, spa, etc.)

14. **VLM Model Selection** (when pipeline=VLM)
    - Dropdown: smoldocling, granite_vision, got_ocr_2, etc.

15. **ASR Model Selection** (when pipeline=ASR)
    - Dropdown: whisper_tiny, whisper_small, whisper_medium, etc.

16. **Enrichment Options** (checkboxes)
    - Enable code enrichment
    - Enable formula enrichment
    - Enable picture classification
    - Enable picture description

17. **Performance Options**
    - Number of threads (default: 4)
    - Page batch size (default: 4)
    - Device: auto (default) / CPU / CUDA / MPS
    - Document timeout (seconds)

18. **HTTP Headers** (for URL sources)
    - JSON text input for custom headers

19. **Advanced Settings**
    - Abort on error (checkbox)
    - Enable remote services (checkbox)
    - Allow external plugins (checkbox)
    - Show layout bounding boxes (checkbox)

20. **Debug Visualization Options** (checkboxes)
    - Visualize PDF cells
    - Visualize OCR cells
    - Visualize layout clusters
    - Visualize table cells

---

### Tier 4: Settings & Preferences
Accessible via Settings menu/dialog:

21. **Default Output Directory**
    - Path configuration
    - "Browse" button
    - Reset to default

22. **Offline Processing Configuration**
    - Processing mode preference (Online/Offline)
    - Artifacts path configuration
    - Model download manager
    - Check for model updates

23. **Application Settings**
    - Theme selection (light/dark)
    - Console font size
    - Auto-open output folder after conversion
    - Remember window size/position
    - Check for Docling updates

24. **Configuration Profiles** (optional)
    - Save current settings as named profile
    - Load saved profile
    - Manage profiles (rename, delete)

---

## Detailed Feature Specifications

### 1. Input Selection System

#### File Picker
- **Component**: Button + file dialog
- **Label**: "Select File" or "Add File"
- **Functionality**:
  - Opens native OS file dialog
  - Supports multiple selection (for batch mode)
  - File filters based on Docling's `--from` formats:
    - PDF files (*.pdf)
    - Word documents (*.docx)
    - PowerPoint (*.pptx)
    - HTML (*.html, *.htm)
    - Images (*.jpg, *.jpeg, *.png, *.gif, *.bmp)
    - Markdown (*.md)
    - CSV (*.csv)
    - Excel (*.xlsx)
    - Audio/Video (*.mp3, *.mp4, *.wav, etc.)
    - All supported files (*)
- **Display**: Show selected file path(s) below button

#### Drag-and-Drop Zone
- **Component**: Large drop zone area (300x150px minimum)
- **States**:
  - Default: Dashed border, icon, "Drag files here or click to browse"
  - Hover: Highlighted border, "Drop files to add"
  - Active (file dropped): Brief success animation
- **Functionality**:
  - Accept files and folders
  - Add to queue in batch mode
  - Replace current file in single mode
  - Visual feedback during drag-over

#### URL Input
- **Component**: Text input + "Add URL" button
- **Label**: "Or enter URL:"
- **Functionality**:
  - Validate URL format
  - Support HTTP/HTTPS
  - Add to queue with URL icon/badge
  - Show download progress during processing

#### File Information Display
- **Component**: Info panel
- **Shows**:
  - Filename
  - File size (formatted: KB, MB, GB)
  - File format
  - Path (truncated with tooltip for full path)
  - Status icon (queued, processing, complete, error)

---

### 2. Batch Queue Management

#### Queue List View
- **Component**: Table or list widget
- **Columns**:
  1. Status icon (pending, processing, complete, error)
  2. Filename
  3. Format (PDF, DOCX, etc.)
  4. Size
  5. Action buttons (remove, view details)
- **Features**:
  - Sortable columns
  - Select multiple items
  - Context menu: Remove, Remove All, Clear Completed
  - Keyboard shortcuts (Delete to remove)
  - Visual distinction for current processing item

#### Queue Controls
- **Add Files Button**: Opens multi-select file dialog
- **Add Folder Button**: Opens directory picker, recursively adds supported files
- **Add URL Button**: Opens URL input dialog
- **Clear Queue Button**: Removes all items (with confirmation)
- **Remove Selected Button**: Removes selected items

#### Queue Statistics
- **Display**:
  - Total files: X
  - Completed: Y
  - Failed: Z
  - Remaining: X - Y - Z

---

### 3. Processing Mode: Online vs Offline

#### Mode Selector
- **Component**: Toggle switch or radio buttons
- **Options**:
  - **Online Mode** (default)
    - Uses default model locations
    - May download models as needed
    - Can connect to remote services
    - Faster setup, always up-to-date
  - **Offline Mode**
    - Uses local artifacts path
    - No internet connections
    - Requires pre-downloaded models
    - Better for privacy/air-gapped systems

#### Mode Indicator
- **Component**: Status badge/icon
- **States**:
  - Online: Green indicator, "Online Mode"
  - Offline: Blue indicator, "Offline Mode"
  - Offline (models missing): Yellow warning, "Models not found"

#### Offline Configuration (in Settings)
- **Artifacts Path**:
  - Text field with path
  - Browse button
  - Default: `~/.cache/docling` or platform-appropriate cache location
  - Validate path exists and is writable
- **Model Manager**:
  - List of required models
  - Status: Downloaded / Not Downloaded / Update Available
  - "Download All" button
  - Individual download buttons
  - Storage space required/used

---

### 4. Output Configuration

#### Output Format Selector
- **Component**: Dropdown/combo box
- **Options** (maps to `--to`):
  - Markdown (default) → `md`
  - JSON → `json`
  - HTML → `html`
  - HTML (Split Page) → `html_split_page`
  - Text → `text`
  - Doctags → `doctags`
- **Display**: Show format description on hover/selection
  - Markdown: "Structured text format, ideal for documentation"
  - JSON: "Structured data, suitable for further processing"
  - etc.

#### Output Directory Selector
- **Component**: Text field + Browse button + Open button
- **Functionality**:
  - Browse button: Opens directory picker
  - Open button: Opens directory in OS file manager
  - Text field: Shows current path, editable
  - Validation: Check path exists and is writable
  - Default: Current directory or last used directory
- **Settings Integration**:
  - Save "Default Output Directory" in preferences
  - "Use default" checkbox or button

---

### 5. Common Processing Options Panel

**Layout**: Collapsible/expandable section, expanded by default

#### Pipeline Selection
- **Component**: Dropdown or radio buttons
- **Label**: "Processing Pipeline"
- **Options**:
  - Standard (default) - "General document processing"
  - VLM - "Vision Language Model for complex layouts"
  - ASR - "Audio/Speech Recognition for video/audio files"
- **Behavior**: Show relevant sub-options based on selection
  - If VLM: Show VLM model selector
  - If ASR: Show ASR model selector

#### OCR Options
- **Enable OCR**: Checkbox (checked by default)
  - Label: "Enable OCR (Optical Character Recognition)"
  - Maps to: `--ocr` / `--no-ocr`
- **Force OCR**: Checkbox (unchecked by default)
  - Label: "Force OCR (replace existing text)"
  - Maps to: `--force-ocr` / `--no-force-ocr`
  - Disabled when "Enable OCR" is unchecked
- **OCR Engine**: Dropdown
  - Default: easyocr
  - Options: easyocr, tesseract, rapidocr, ocrmac (macOS only), tesserocr
  - Maps to: `--ocr-engine`

#### Image Export Mode
- **Component**: Dropdown or radio buttons
- **Label**: "Image Handling"
- **Options**:
  - Embedded (default) - "Include images in output"
  - Referenced - "Save images separately, link in output"
  - Placeholder - "Use placeholders instead of images"
- **Maps to**: `--image-export-mode`

#### Table Processing
- **Component**: Dropdown or radio buttons
- **Label**: "Table Extraction Mode"
- **Options**:
  - Accurate (default) - "Higher quality, slower"
  - Fast - "Quick extraction, may be less accurate"
- **Maps to**: `--table-mode`

---

### 6. Advanced Options Panel

**Layout**: Collapsible section, collapsed by default, labeled "Advanced Options"

#### PDF Backend
- **Component**: Dropdown
- **Label**: "PDF Processing Backend"
- **Options**: dlparse_v2 (default), dlparse_v1, dlparse_v4, pypdfium2
- **Help text**: "Choose PDF parsing engine"
- **Maps to**: `--pdf-backend`

#### OCR Language
- **Component**: Text input + preset buttons
- **Label**: "OCR Languages"
- **Input**: Comma-separated language codes (e.g., "eng,deu,fra")
- **Preset buttons**: English, German, French, Spanish, Chinese, Japanese
  - Clicking adds to text input
- **Maps to**: `--ocr-lang`

#### VLM Model (visible when Pipeline=VLM)
- **Component**: Dropdown
- **Options**: smoldocling, smoldocling_vllm, granite_vision, granite_vision_vllm, granite_vision_ollama, got_ocr_2
- **Maps to**: `--vlm-model`

#### ASR Model (visible when Pipeline=ASR)
- **Component**: Dropdown
- **Options**: whisper_tiny, whisper_small, whisper_medium, whisper_base, whisper_large, whisper_turbo
- **Maps to**: `--asr-model`

#### Enrichment Options (Checkboxes)
- **Group label**: "Content Enrichment"
- **Options**:
  - Enable code enrichment (`--enrich-code`)
  - Enable formula enrichment (`--enrich-formula`)
  - Enable picture classification (`--enrich-picture-classes`)
  - Enable picture description (`--enrich-picture-description`)

#### Performance Tuning
- **Number of Threads**: Spinner input (1-16, default: 4)
  - Maps to: `--num-threads`
- **Page Batch Size**: Spinner input (1-16, default: 4)
  - Maps to: `--page-batch-size`
- **Device Selection**: Dropdown
  - Options: Auto (default), CPU, CUDA, MPS
  - Maps to: `--device`
- **Document Timeout**: Spinner input (seconds, 0=unlimited, default: 0)
  - Maps to: `--document-timeout`

#### Other Advanced Options (Checkboxes)
- Abort on first error (`--abort-on-error`)
- Enable remote services (`--enable-remote-services`)
- Allow external plugins (`--allow-external-plugins`)
- Show layout bounding boxes (`--show-layout`)

#### Debug Visualization (Checkboxes)
- **Group label**: "Debug Visualization (for developers)"
- **Options**:
  - Visualize PDF cells (`--debug-visualize-cells`)
  - Visualize OCR cells (`--debug-visualize-ocr`)
  - Visualize layout clusters (`--debug-visualize-layout`)
  - Visualize table cells (`--debug-visualize-tables`)

#### HTTP Headers (for URLs)
- **Component**: Multi-line text input
- **Label**: "HTTP Headers (JSON format)"
- **Placeholder**: `{"Authorization": "Bearer token"}`
- **Validation**: Check valid JSON format
- **Maps to**: `--headers`

---

### 7. Processing Control & Progress

#### Control Buttons
- **Convert / Process Button**
  - State 1: "Convert" (single file) or "Process Queue" (batch)
  - State 2: Disabled during processing
  - Large, prominent, primary color
- **Cancel Button**
  - Visible only during processing
  - Terminates current operation
  - Prompts confirmation if queue is large

#### Progress Indication
- **Progress Bar**: 0-100% for current file
- **Overall Progress** (batch mode): "Processing 3 of 25 files"
- **Current Status**:
  - "Ready" (idle)
  - "Processing: filename.pdf" (active)
  - "Completed successfully" (done)
  - "Failed: error message" (error)
- **Time Estimates** (optional):
  - Elapsed time
  - Estimated time remaining (based on average)

#### Console/Log Output
- **Component**: Multi-line text area, read-only, scrollable
- **Features**:
  - Monospace font
  - Auto-scroll to bottom (with option to disable)
  - Color coding:
    - Black/White: Normal output
    - Blue: Info messages
    - Orange: Warnings
    - Red: Errors
  - Line numbers (optional)
  - Context menu: Copy, Clear, Save to File
- **Content**:
  - Docling command being executed
  - Docling stdout/stderr
  - Timestamp for each entry
  - Processing start/end times
  - Success/failure summaries

---

### 8. File Preview Feature

#### Preview Panel
- **Location**: Side panel or tab
- **Toggle**: Show/Hide preview button

#### Preview Content
- **File Information**:
  - Full path
  - File size
  - Format/MIME type
  - Created/modified dates
  - Page count (for PDFs/DOCX)
- **Visual Preview**:
  - Thumbnail of first page (for PDFs/images)
  - Text snippet (first 200 chars for text formats)
  - "Full preview not available" for unsupported formats
- **Document Metadata** (if available):
  - Title
  - Author
  - Subject
  - Keywords

#### Preview Actions
- **Open in System Viewer**: Button to open file in default application
- **Show in Folder**: Opens file manager to file location

---

### 9. Settings & Preferences Dialog

**Access**: Menu bar → Preferences/Settings, or keyboard shortcut (Cmd+, / Ctrl+,)

#### General Tab
- **Default Output Directory**:
  - Path input + Browse button
  - "Use last used directory" checkbox
- **Default Output Format**:
  - Dropdown (Markdown, JSON, HTML, etc.)
- **Application Behavior**:
  - "Auto-open output folder after conversion" checkbox
  - "Remember window position" checkbox
  - "Show confirmation before clearing queue" checkbox

#### Processing Tab
- **Default Processing Mode**:
  - Radio buttons: Online / Offline
- **Offline Configuration**:
  - Artifacts path: input + Browse
  - "Download models" button
  - Model status list
- **Docling CLI Path** (advanced):
  - Auto-detect or specify custom path
  - Useful if Docling installed in non-standard location

#### Interface Tab
- **Theme**: Light / Dark / System
- **Console Font Size**: Spinner (8-20, default: 10)
- **Language**: Dropdown (for future i18n)

#### Updates Tab
- **Check for Updates**: "Check now" button
- **Auto-check for updates**: Checkbox
- **Current version**: Display app version and Docling version

---

## UI Layout Design

### Main Window Layout (Recommended)

```
┌────────────────────────────────────────────────────────────────┐
│ Menu Bar: File | Edit | View | Settings | Help                 │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────┐  ┌─────────────────────────────┐ │
│  │  INPUT SECTION           │  │  PREVIEW (optional)         │ │
│  │                          │  │                             │ │
│  │  [Drag & Drop Zone]      │  │  File: document.pdf         │ │
│  │   or                     │  │  Size: 2.4 MB               │ │
│  │  [Select File] [Add URL] │  │  Pages: 15                  │ │
│  │                          │  │                             │ │
│  │  Selected: doc.pdf       │  │  [Thumbnail]                │ │
│  │                          │  │                             │ │
│  └──────────────────────────┘  └─────────────────────────────┘ │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  BATCH QUEUE (expandable)                                │  │
│  │  [▼] Show Queue (3 files)                                │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │ ✓ doc1.pdf     PDF  1.2 MB  [Complete]            │  │  │
│  │  │ ⟳ doc2.docx    DOCX 800 KB   [Processing...]       │  │  │
│  │  │ ⋯ doc3.pdf     PDF  2.1 MB   [Queued]             │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │  [Add Files] [Add Folder] [Clear Queue]                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  OUTPUT & OPTIONS                                         │  │
│  │                                                            │  │
│  │  Output Format: [Markdown ▼]  Output Dir: [/path/to ⊙]   │  │
│  │                                                            │  │
│  │  Processing Mode: ( ) Online  (•) Offline                 │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │ [▼] Common Options                                   │  │  │
│  │  │     Pipeline: [Standard ▼]                          │  │  │
│  │  │     ☑ Enable OCR    ☐ Force OCR                     │  │  │
│  │  │     Image Mode: [Embedded ▼]                        │  │  │
│  │  │     Table Mode: [Accurate ▼]                        │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │ [▶] Advanced Options                                 │  │  │
│  │  │     (collapsed - click to expand)                    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  [         Convert / Process Queue         ]  [Cancel]   │  │
│  │  Progress: [████████░░░░░░░░░░░░░░] 40% (2 of 5 files)  │  │
│  │  Status: Processing doc2.docx...                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  CONSOLE OUTPUT                                           │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │ [12:34:56] Starting conversion...                   │  │  │
│  │  │ [12:34:57] Processing with Standard pipeline        │  │  │
│  │  │ [12:34:58] OCR: Enabled | Backend: dlparse_v2      │  │  │
│  │  │ [12:35:02] Page 1/15 processed                     │  │  │
│  │  │ ...                                                 │  │  │
│  │  │ [12:35:45] Conversion complete: output.md          │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │  [Clear Log] [Save Log] [Copy]                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Status Bar: Ready | Docling v2.64.1 | Mode: Offline          │
└────────────────────────────────────────────────────────────────┘
```

### Alternative: Tab-Based Layout

```
┌────────────────────────────────────────────────────────────────┐
│ Menu Bar                                                        │
├────────────────────────────────────────────────────────────────┤
│  [Input] [Options] [Queue] [Console] [Settings]               │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  (Tab content here - each tab shows relevant section)          │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

**Pros**: Cleaner, less cluttered, organized by workflow step
**Cons**: More clicks to access features, less overview

---

## Settings & Configuration

### Application Settings (Persistent)

Settings stored in platform-appropriate locations:
- **Windows**: `%APPDATA%/DoclingGUI/config.json`
- **macOS**: `~/Library/Application Support/DoclingGUI/config.json`

#### Configuration File Structure (JSON)

```json
{
  "version": "1.0",
  "general": {
    "defaultOutputDir": "/Users/username/Documents/converted",
    "useLastOutputDir": true,
    "defaultOutputFormat": "md",
    "autoOpenOutputFolder": true,
    "rememberWindowGeometry": true,
    "showQueueByDefault": true
  },
  "processing": {
    "mode": "online",
    "artifactsPath": "/Users/username/.cache/docling",
    "doclingCliPath": "auto"
  },
  "defaults": {
    "pipeline": "standard",
    "ocrEnabled": true,
    "forceOcr": false,
    "ocrEngine": "easyocr",
    "ocrLanguages": "eng",
    "imageExportMode": "embedded",
    "tableMode": "accurate",
    "pdfBackend": "dlparse_v2",
    "numThreads": 4,
    "pageBatchSize": 4,
    "device": "auto"
  },
  "interface": {
    "theme": "system",
    "consoleFontSize": 10,
    "language": "en"
  },
  "updates": {
    "checkAutomatically": true,
    "lastChecked": "2025-12-12T10:30:00Z"
  },
  "window": {
    "width": 900,
    "height": 700,
    "x": 100,
    "y": 100
  },
  "profiles": [
    {
      "name": "Quick Convert",
      "settings": {
        "outputFormat": "md",
        "pipeline": "standard",
        "ocrEnabled": true
      }
    },
    {
      "name": "High Quality PDF",
      "settings": {
        "outputFormat": "json",
        "pipeline": "vlm",
        "vlmModel": "granite_vision",
        "forceOcr": true,
        "tableMode": "accurate"
      }
    }
  ]
}
```

### Configuration Profiles (Optional Feature)

Allow users to save/load named configuration sets:

- **Save Profile**: Captures current settings with a name
- **Load Profile**: Restores saved settings
- **Manage Profiles**: List, rename, delete saved profiles
- **UI**: Dropdown in toolbar or Settings dialog

**Use Cases**:
- "Quick Markdown" profile for fast conversions
- "High Quality Research Papers" profile with VLM and enrichments
- "Batch OCR" profile optimized for scanned documents

---

## Implementation Priorities

### Phase 1: MVP (Minimum Viable Product)
**Goal**: Basic single-file conversion with essential options
**Timeline**: 1-2 weeks

**Features**:
- [x] File selection (picker and drag-and-drop)
- [x] Output format selection (Markdown, JSON, HTML, Text)
- [x] Output directory selection
- [x] Basic processing controls (Convert, Cancel)
- [x] Progress bar and status text
- [x] Console output display
- [x] Online/Offline mode toggle
- [x] Essential OCR options (enable/disable)
- [x] Error handling and user feedback

**Success Criteria**: User can convert a single PDF to Markdown

---

### Phase 2: Batch Processing & Common Options
**Goal**: Multi-file queue and frequently used options
**Timeline**: 1-2 weeks

**Features**:
- [x] Batch queue view and management
- [x] Add multiple files and folders
- [x] Queue status tracking
- [x] Common processing options panel:
  - Pipeline selection
  - OCR settings (enable, force, engine)
  - Image export mode
  - Table mode
- [x] File preview (basic info and metadata)

**Success Criteria**: User can queue 20+ files and process them with custom OCR settings

---

### Phase 3: Advanced Options & Settings
**Goal**: Full Docling parameter exposure and configuration
**Timeline**: 1-2 weeks

**Features**:
- [x] Advanced options panel (collapsible):
  - PDF backend
  - VLM/ASR model selection
  - Enrichment options
  - Performance tuning
  - Debug visualization
- [x] Settings/Preferences dialog:
  - Default directories and formats
  - Offline artifacts path
  - Interface preferences
  - Update checking
- [x] URL input support
- [x] HTTP headers configuration

**Success Criteria**: Power user can configure all Docling options and save preferences

---

### Phase 4: Polish & Advanced Features
**Goal**: Enhanced UX and optional features
**Timeline**: 1 week

**Features**:
- [x] Configuration profiles (save/load settings)
- [x] Enhanced file preview (thumbnails)
- [x] Improved error messages and help text
- [x] Keyboard shortcuts
- [x] Context menus
- [x] Tooltips for all options
- [x] Auto-save window position and size
- [x] Export/import settings
- [x] Model download manager (for offline mode)

**Success Criteria**: Application feels polished and professional

---

### Phase 5: Future Enhancements (Optional)
**Goal**: Nice-to-have features for future releases

**Features**:
- [ ] Compare before/after output
- [ ] Built-in output viewer (Markdown renderer, JSON tree view)
- [ ] Scheduled/automated conversions
- [ ] Watch folder mode (auto-process new files)
- [ ] CLI mode (use GUI as wrapper but also support command line)
- [ ] Integration with cloud storage (Dropbox, Google Drive)
- [ ] Conversion history and statistics
- [ ] Multi-language UI (internationalization)
- [ ] Themes and customization
- [ ] Plugin system for custom processors

---

## Key Implementation Notes

### Command Construction
The GUI must build Docling commands from selected options:

```python
# Example command construction
cmd = ["docling"]
cmd.append(input_path)
cmd.extend(["--to", output_format])
cmd.extend(["--output", output_dir])

if pipeline != "standard":
    cmd.extend(["--pipeline", pipeline])

if ocr_enabled:
    cmd.append("--ocr")
else:
    cmd.append("--no-ocr")

if force_ocr:
    cmd.append("--force-ocr")

if ocr_engine != "easyocr":
    cmd.extend(["--ocr-engine", ocr_engine])

# ... more options ...

# Execute command
subprocess.run(cmd, capture_output=True)
```

### Process Management
- Use Python's `subprocess` module with `Popen` for async execution
- Capture stdout/stderr in real-time for console output
- Monitor process return codes for success/failure
- Support cancellation via process termination
- Handle multiple simultaneous conversions (threading/multiprocessing)

### Error Handling
- Validate Docling installation before first run
- Check file paths exist and are readable
- Validate output directory is writable
- Handle process errors gracefully with user-friendly messages
- Log detailed errors for debugging
- Provide actionable error messages:
  - "Docling not found. Please install: pip install docling"
  - "Output directory is read-only. Please choose another location."
  - "OCR failed: Language pack 'ara' not installed."

### Performance Considerations
- Don't block UI during processing (use threads/workers)
- Update progress at reasonable intervals (not every line)
- Limit console output buffer (e.g., last 10,000 lines)
- Optimize queue display for large batches (virtualized list)
- Cache file metadata to avoid repeated reads

### Platform-Specific Considerations
- **File Paths**: Use `pathlib.Path` for cross-platform compatibility
- **Dialogs**: Use Qt's native dialogs for consistent look
- **Fonts**: Use monospace fonts for console (Consolas/Menlo/Monaco)
- **Shortcuts**: Follow platform conventions (Cmd vs Ctrl)
- **Icons**: Use platform-appropriate icon sizes and styles

---

## Summary

This feature analysis provides a comprehensive blueprint for the Docling GUI, covering:
- **5 core use cases** from simple to advanced
- **3 user workflows** optimized for different skill levels
- **24+ features** organized into 4 tiers by priority
- **Detailed specifications** for each major component
- **UI layout recommendations** with mockup
- **Settings architecture** with JSON config structure
- **5-phase implementation plan** from MVP to polish

The design prioritizes:
1. **Ease of use** for 80% of users (simple, single-file conversion)
2. **Power features** for advanced users (batch, advanced options)
3. **Maintainability** through clear organization and Python/PySide6
4. **Cross-platform consistency** with native look and feel

Next steps:
1. Review and approve this feature set
2. Create detailed UI mockups/wireframes
3. Set up project structure and dependencies
4. Begin Phase 1 (MVP) implementation
