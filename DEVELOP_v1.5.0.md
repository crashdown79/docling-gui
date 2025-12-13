# Development Plan: Docling GUI v1.5.0

**Date:** 2025-12-13
**Status:** Planning Phase
**Target:** Major UI Redesign with Sidebar Layout & Enhanced Batch Queue

---

## Executive Summary

Version 1.5.0 represents a **major architectural redesign** of the Docling GUI, transitioning from a vertical single-column layout to a modern **two-panel sidebar design**. This change improves usability, makes batch processing more prominent, and creates a more professional user experience.

### Key Changes from Mockup Analysis:
1. **Two-panel layout:** Left sidebar (controls) + Right main area (queue + console)
2. **Enhanced batch queue:** Visual file list with drag-and-drop support
3. **Collapsible sidebar sections:** Better organization of options
4. **New enrichment options:** Extract Tables, Enrich Code
5. **Debug & Visualization section:** Dedicated area for debug options
6. **Improved console management:** Clear Log button

---

## Current State Analysis (v1.2.3)

### Existing Infrastructure ✅
- ✅ Queue system fully implemented (`core/queue.py`)
- ✅ Queue integration started in `ui/main_window.py`
- ✅ All core conversion logic working
- ✅ Configuration management working
- ✅ Console logging with file output

### Current Layout Issues ❌
- ❌ Single vertical column layout (cramped)
- ❌ No visual queue representation
- ❌ Options not well organized
- ❌ No drag-and-drop support
- ❌ Queue functionality hidden from user

---

## Architecture Changes Required

### 1. **Refactoring Strategy: Component-Based Architecture**

**Decision:** Split `ui/main_window.py` into modular components

**New File Structure:**
```
ui/
├── __init__.py
├── main_window.py          # Main container, layout orchestration
├── sidebar.py              # NEW: Left sidebar component
├── queue_panel.py          # NEW: Batch queue visualization
├── console_panel.py        # NEW: Console output component
└── widgets/                # NEW: Reusable widget components
    ├── __init__.py
    ├── collapsible_section.py   # NEW: Collapsible frame widget
    ├── file_drop_zone.py        # NEW: Drag-and-drop area
    └── queue_item_widget.py     # NEW: Individual queue item display
```

**Why Refactor?**
- Current `main_window.py` will become too large (already 800+ lines)
- Better separation of concerns
- Easier testing and maintenance
- Reusable components
- Clearer code organization

**Refactoring Approach:**
- ✅ **Keep existing code working** - refactor incrementally
- Create new component files first
- Move code section by section
- Test after each move
- Update imports progressively

---

## Detailed Implementation Plan

### Phase 1: Foundation & Refactoring (Days 1-2)

#### Task 1.1: Create Reusable Widget Components
**Priority:** HIGH
**Estimated Effort:** 4 hours

**Files to create:**
- `ui/widgets/__init__.py`
- `ui/widgets/collapsible_section.py`
- `ui/widgets/file_drop_zone.py`
- `ui/widgets/queue_item_widget.py`

**collapsible_section.py:**
```python
class CollapsibleSection(ctk.CTkFrame):
    """A frame that can be collapsed/expanded with a toggle button."""

    def __init__(self, parent, title: str, is_expanded: bool = True):
        # Header with toggle button (▼/▶)
        # Content container that can be hidden/shown
        # Smooth animation support
```

**file_drop_zone.py:**
```python
class FileDropZone(ctk.CTkFrame):
    """Drag-and-drop area for files."""

    def __init__(self, parent, on_files_dropped: Callable):
        # Visual drop zone with dashed border
        # Drag-and-drop event handlers
        # Highlight on drag-over
        # File validation
```

**queue_item_widget.py:**
```python
class QueueItemWidget(ctk.CTkFrame):
    """Visual representation of a single queue item."""

    def __init__(self, parent, queue_item: QueueItem, on_remove: Callable):
        # Status icon with color coding
        # Filename label
        # File size label
        # Remove button
        # Progress indicator (when processing)
```

**Deliverables:**
- [x] Three new widget files created
- [x] Each widget tested independently
- [x] Documentation/docstrings added

---

#### Task 1.2: Create Console Panel Component
**Priority:** HIGH
**Estimated Effort:** 2 hours

**File:** `ui/console_panel.py`

**Responsibilities:**
- Console output textbox
- Save to log file checkbox
- Clear log button (NEW)
- Scroll to bottom on new output
- Log file management

**Methods to extract from main_window.py:**
- `_create_console_section()` → `ConsolePanel.__init__()`
- `_log_console()` → `ConsolePanel.append()`
- `_create_log_file()` → `ConsolePanel._create_log_file()`
- `_close_log_file()` → `ConsolePanel._close_log_file()`
- `_on_log_enable_change()` → `ConsolePanel._toggle_logging()`

**New methods:**
- `ConsolePanel.clear()` - Clear console output
- `ConsolePanel.get_text()` - Get all console text

**Deliverables:**
- [x] `ui/console_panel.py` created
- [x] Console functionality moved and working
- [x] Clear log button implemented
- [x] Integration tested with main window

---

#### Task 1.3: Create Queue Panel Component
**Priority:** HIGH
**Estimated Effort:** 6 hours

**File:** `ui/queue_panel.py`

**Responsibilities:**
- Queue header with file count
- Clear Completed / Clear All buttons
- Drag-and-drop zone
- Scrollable list of queue items
- Queue statistics display

**Methods:**
- `__init__()` - Setup layout
- `refresh_queue()` - Update queue display from queue data
- `add_queue_item_widget()` - Add item to visual list
- `remove_queue_item_widget()` - Remove item from visual list
- `update_queue_stats()` - Update header file count
- `on_files_dropped()` - Handle drag-and-drop events
- `clear_completed_clicked()` - Remove completed items
- `clear_all_clicked()` - Remove all items

**Layout Structure:**
```
┌─────────────────────────────────────────┐
│  Batch Queue (5 files)  [Clear Completed] [Clear All] │
├─────────────────────────────────────────┤
│                                         │
│   ┌───────────────────────────────┐   │
│   │  Drag files here or add from │   │
│   │  sidebar                      │   │
│   └───────────────────────────────┘   │
│                                         │
│   [⟳] document1.pdf    2.3 MB    [x]  │
│   [✓] report.docx      1.1 MB    [x]  │
│   [⋯] data.xlsx        500 KB    [x]  │
│                                         │
└─────────────────────────────────────────┘
```

**Deliverables:**
- [x] `ui/queue_panel.py` created
- [x] Queue visualization working
- [x] Drag-and-drop functional
- [x] Queue management buttons working

---

#### Task 1.4: Create Sidebar Component
**Priority:** HIGH
**Estimated Effort:** 8 hours

**File:** `ui/sidebar.py`

**Responsibilities:**
- Application title
- Add Files / Folder buttons
- Output Configuration section (collapsible)
- Processing Options section (collapsible)
- Debug & Visualization section (collapsible, NEW)
- Convert / Cancel buttons

**Collapsible Sections:**

1. **Output Configuration** (collapsed by default)
   - Format dropdown
   - Output directory selector with browse button

2. **Processing Options** (expanded by default)
   - Mode dropdown (Online/Offline)
   - Pipeline dropdown
   - OCR Settings (Enable, Force, Language)
   - Enrichment options (6 checkboxes, see Task 2.1)
   - Image Export Mode dropdown
   - Verbose level dropdown
   - Download Models button

3. **Debug & Visualization** (collapsed by default)
   - Debug visualize cells checkbox
   - Debug visualize OCR checkbox
   - Debug visualize layout checkbox
   - Debug visualize tables checkbox

**Methods to extract:**
- `_create_input_section()` → `Sidebar._create_file_buttons()`
- `_create_output_section()` → `Sidebar._create_output_config()`
- `_create_options_section()` → `Sidebar._create_processing_options()`
- `_create_control_section()` → `Sidebar._create_control_buttons()`

**New methods:**
- `Sidebar._create_debug_section()` - Debug options

**Deliverables:**
- [x] `ui/sidebar.py` created
- [x] All sections moved and working
- [x] Collapsible behavior implemented
- [x] Debug section added

---

### Phase 2: New Features & Enhancements (Days 3-4)

#### Task 2.1: Add New Enrichment Options
**Priority:** MEDIUM
**Estimated Effort:** 2 hours

**Current enrichment options (v1.1.0):**
- Formulas
- Picture Classes
- Picture Descriptions

**New enrichment options (v1.5.0):**
- **Extract Tables** (NEW)
- **Enrich Code** (NEW)

**Implementation:**
1. Add checkboxes to Processing Options section
2. Add config defaults:
   ```json
   "extractTables": false,
   "enrichCode": false
   ```
3. Update `DoclingConverter.build_command()`:
   ```python
   if extract_tables:
       cmd.append("--enrich-table-structure")
   if enrich_code:
       cmd.append("--enrich-code")
   ```

**Note:** Verify correct Docling CLI parameter names

**Deliverables:**
- [x] New checkboxes in sidebar
- [x] Configuration updated
- [x] Command building updated
- [x] Tested with real conversion

---

#### Task 2.2: Implement Debug & Visualization Section
**Priority:** MEDIUM
**Estimated Effort:** 3 hours

**Parameters to expose:**
- `--debug-visualize-cells` - Visualize PDF cells
- `--debug-visualize-ocr` - Visualize OCR cells
- `--debug-visualize-layout` - Visualize layout clusters
- `--debug-visualize-tables` - Visualize table cells

**Implementation:**
1. Create collapsible section in sidebar
2. Add 4 checkboxes (default: all unchecked)
3. Add to configuration:
   ```json
   "debug": {
     "visualizeCells": false,
     "visualizeOcr": false,
     "visualizeLayout": false,
     "visualizeTables": false
   }
   ```
4. Update `DoclingConverter.build_command()`
5. Add info tooltip explaining what each option does

**Deliverables:**
- [x] Debug section in sidebar
- [x] 4 debug checkboxes
- [x] Command building updated
- [x] Help tooltips added

---

#### Task 2.3: Implement Drag-and-Drop Support
**Priority:** HIGH
**Estimated Effort:** 4 hours

**Requirements:**
- Drop zone shows visual feedback on drag-over
- Accepts multiple files at once
- Validates file types (supported formats only)
- Shows error for unsupported files
- Automatically adds valid files to queue

**Platform Considerations:**
- macOS: TkinterDnD2 or tkinterdnd2
- Windows: Same library support

**Implementation approach:**
1. Research TkinterDnD2 compatibility with CustomTkinter
2. If compatible: Use TkinterDnD2
3. If not: Implement manual file paste or button-based multi-select
4. Add visual states to FileDropZone:
   - Normal: Dashed border, gray
   - Hover: Highlighted border, blue
   - Drop: Animated feedback

**Alternative if drag-and-drop problematic:**
- Enhanced file picker with multi-select
- "Paste file path" option
- Directory browser with preview

**Deliverables:**
- [x] Drag-and-drop working or suitable alternative
- [x] Visual feedback implemented
- [x] File validation working
- [x] Multi-file support tested

---

#### Task 2.4: Console Clear Button
**Priority:** LOW
**Estimated Effort:** 1 hour

**Simple addition:**
- Add "Clear Log" button next to "Save Log" checkbox
- Clears textbox content (not log file)
- Confirm dialog if log has important content
- Keyboard shortcut: Cmd+K (macOS) / Ctrl+K (Windows)

**Deliverables:**
- [x] Clear button added
- [x] Functionality working
- [x] Optional: confirmation dialog

---

### Phase 3: Layout Integration & Testing (Day 5)

#### Task 3.1: Restructure Main Window Layout
**Priority:** CRITICAL
**Estimated Effort:** 6 hours

**New Layout:**
```python
# main_window.py

class MainWindow(ctk.CTk):
    def __init__(self):
        # ... initialization ...

    def _create_widgets(self):
        """Create two-panel layout."""

        # Configure grid: 2 columns
        self.grid_columnconfigure(0, weight=0, minsize=320)  # Sidebar fixed
        self.grid_columnconfigure(1, weight=1)               # Main area expands
        self.grid_rowconfigure(0, weight=1)

        # Left: Sidebar
        self.sidebar = Sidebar(
            self,
            on_add_files=self._add_files_clicked,
            on_add_folder=self._add_folder_clicked,
            on_convert=self._start_conversion,
            on_cancel=self._cancel_conversion,
            config=self.config
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Right: Main area (Queue + Console)
        main_area = ctk.CTkFrame(self)
        main_area.grid(row=0, column=1, sticky="nsew")
        main_area.grid_rowconfigure(0, weight=1)  # Queue
        main_area.grid_rowconfigure(1, weight=1)  # Console
        main_area.grid_columnconfigure(0, weight=1)

        # Queue Panel
        self.queue_panel = QueuePanel(
            main_area,
            queue=self.queue,
            on_files_dropped=self._files_dropped
        )
        self.queue_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

        # Console Panel
        self.console_panel = ConsolePanel(main_area, config=self.config)
        self.console_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
```

**Window size update:**
- Current: 900x900
- New: 1200x900 (wider for two panels)

**Deliverables:**
- [x] Two-panel layout implemented
- [x] All components integrated
- [x] Resizing works correctly
- [x] Minimum window size set

---

#### Task 3.2: Update Conversion Flow for Queue Processing
**Priority:** HIGH
**Estimated Effort:** 4 hours

**Current:** Single file conversion
**Target:** Process entire queue sequentially

**Changes needed in main_window.py:**

```python
def _start_conversion(self):
    """Start processing the entire queue."""
    if len(self.queue) == 0:
        messagebox.showwarning("No Files", "Please add files to the queue first.")
        return

    # Validate offline mode models if needed
    # (existing validation logic)

    # Disable UI
    self._set_processing_state(True)

    # Start queue processing
    self._process_next_in_queue()

def _process_next_in_queue(self):
    """Process the next pending item in queue."""
    next_item = self.queue.get_next_pending()

    if next_item is None:
        # Queue complete
        self._on_queue_complete()
        return

    # Update status
    self.queue.update_status(next_item.id, QueueItemStatus.PROCESSING)
    self.queue_panel.refresh_queue()
    self.current_queue_item = next_item

    # Log
    self.console_panel.append(f"\n{'='*60}\n")
    self.console_panel.append(f"Processing: {next_item.filename}\n")
    self.console_panel.append(f"{'='*60}\n")

    # Get conversion parameters from sidebar
    params = self.sidebar.get_conversion_params()

    # Start conversion
    self.converter.convert(
        input_file=next_item.file_path,
        output_format=params['output_format'],
        output_dir=params['output_dir'],
        # ... other params ...
        on_output=self._on_conversion_output,
        on_complete=self._on_conversion_complete,
        on_error=self._on_conversion_error
    )

def _on_conversion_complete(self, return_code: int):
    """Handle single file conversion completion."""
    if self.current_queue_item:
        if return_code == 0:
            status = QueueItemStatus.COMPLETED
            self.console_panel.append(f"✓ Successfully converted: {self.current_queue_item.filename}\n")
        else:
            status = QueueItemStatus.FAILED
            self.console_panel.append(f"✗ Failed to convert: {self.current_queue_item.filename}\n")

        self.queue.update_status(self.current_queue_item.id, status)
        self.queue_panel.refresh_queue()
        self.current_queue_item = None

    # Process next file
    self._process_next_in_queue()

def _on_queue_complete(self):
    """Handle entire queue completion."""
    stats = self.queue.get_statistics()

    self.console_panel.append(f"\n{'='*60}\n")
    self.console_panel.append("[QUEUE COMPLETE]\n")
    self.console_panel.append(f"Total files processed: {stats['total']}\n")
    self.console_panel.append(f"Completed successfully: {stats['completed']}\n")
    self.console_panel.append(f"Failed: {stats['failed']}\n")
    self.console_panel.append(f"{'='*60}\n")

    # Re-enable UI
    self._set_processing_state(False)

    # Show notification
    if stats['failed'] > 0:
        messagebox.showwarning(
            "Queue Complete with Errors",
            f"Processed {stats['total']} files.\n"
            f"Completed: {stats['completed']}\n"
            f"Failed: {stats['failed']}"
        )
    else:
        messagebox.showinfo(
            "Queue Complete",
            f"Successfully processed {stats['completed']} file(s)!"
        )
```

**Deliverables:**
- [x] Queue processing loop implemented
- [x] Status updates working
- [x] Progress tracking visible
- [x] Completion summary shown

---

#### Task 3.3: Enhanced Error Handling & User Feedback
**Priority:** MEDIUM
**Estimated Effort:** 3 hours

**Improvements:**
1. Per-file error tracking in queue
2. Error tooltip on failed queue items
3. Retry failed items option
4. Skip vs Stop on error preference
5. Better error messages in console

**Implementation:**
- Add retry button to failed queue items
- Add "Stop on error" checkbox in Processing Options
- Store detailed error messages in QueueItem
- Show error tooltip on hover

**Deliverables:**
- [x] Error tracking improved
- [x] Retry functionality added
- [x] Stop-on-error option added

---

#### Task 3.4: Comprehensive Testing
**Priority:** CRITICAL
**Estimated Effort:** 4 hours

**Test Cases:**

1. **UI Layout Tests:**
   - [x] Window resizing works correctly
   - [x] Sidebar fixed width maintained
   - [x] Collapsible sections work
   - [x] All buttons clickable and visible

2. **Queue Tests:**
   - [x] Add single file
   - [x] Add multiple files
   - [x] Add folder (recursive)
   - [x] Drag-and-drop files
   - [x] Remove individual items
   - [x] Clear completed
   - [x] Clear all

3. **Conversion Tests:**
   - [x] Process single file queue
   - [x] Process multiple files queue
   - [x] Handle conversion errors
   - [x] Cancel during processing
   - [x] Offline mode validation

4. **Configuration Tests:**
   - [x] Settings persist across restarts
   - [x] Window geometry saved/restored
   - [x] All options work correctly

5. **Platform Tests:**
   - [x] Test on macOS
   - [x] Test on Windows 11

**Deliverables:**
- [x] All test cases passed
- [x] Bugs documented and fixed
- [x] Edge cases handled

---

### Phase 4: Documentation & Release (Day 6)

#### Task 4.1: Update CLAUDE.md
**Priority:** HIGH
**Estimated Effort:** 2 hours

**Updates needed:**
1. Current Status → v1.5.0
2. New Features Implemented section
3. Updated project structure
4. New configuration keys
5. Component documentation
6. Migration notes from v1.2.3

**Deliverables:**
- [x] CLAUDE.md updated
- [x] Accurate documentation

---

#### Task 4.2: Update README.md
**Priority:** HIGH
**Estimated Effort:** 2 hours

**Updates needed:**
1. New screenshot showing two-panel layout
2. Updated feature list
3. Version history
4. Installation/upgrade instructions

**Deliverables:**
- [x] README.md updated
- [x] New screenshot added

---

#### Task 4.3: Create Migration Guide
**Priority:** MEDIUM
**Estimated Effort:** 1 hour

**File:** `MIGRATION_v1.5.0.md`

**Contents:**
- What's changed in v1.5.0
- Breaking changes (none expected)
- New features overview
- Configuration updates (automatic)
- How to use new batch queue

**Deliverables:**
- [x] Migration guide created

---

#### Task 4.4: Version Bump & Release
**Priority:** HIGH
**Estimated Effort:** 1 hour

**Steps:**
1. Update version in `config.py` default config
2. Update version in `main_window.py` title
3. Test fresh install
4. Create git tag: `v1.5.0`
5. Create release notes

**Deliverables:**
- [x] Version bumped to 1.5.0
- [x] Git tag created
- [x] Release published

---

## Configuration Changes

### New Configuration Keys (v1.5.0)

```json
{
  "version": "1.5.0",
  "window": {
    "width": 1200,    // Changed from 900
    "height": 900
  },
  "defaults": {
    // Existing keys preserved...

    // NEW: Additional enrichment options
    "extractTables": false,
    "enrichCode": false,

    // NEW: Debug visualization options
    "debugVisualizeCells": false,
    "debugVisualizeOcr": false,
    "debugVisualizeLayout": false,
    "debugVisualizeTables": false,

    // NEW: Queue processing options
    "stopOnError": false
  },
  "interface": {
    // Existing keys preserved...

    // NEW: Sidebar preferences
    "sidebarWidth": 320,
    "outputConfigExpanded": false,
    "processingOptionsExpanded": true,
    "debugSectionExpanded": false
  }
}
```

---

## Risk Assessment

### High Risk Items:
1. **Drag-and-drop compatibility** - CustomTkinter may have issues
   - Mitigation: Test early, have fallback solution ready

2. **Component refactoring** - Breaking existing functionality
   - Mitigation: Incremental refactoring, extensive testing

3. **Queue processing complexity** - Race conditions, state management
   - Mitigation: Careful threading, clear state tracking

### Medium Risk Items:
1. **Performance with large queues** - UI responsiveness
   - Mitigation: Lazy loading, virtual scrolling if needed

2. **Window resizing edge cases** - Layout breaking
   - Mitigation: Thorough testing, minimum size constraints

### Low Risk Items:
1. **New enrichment options** - Simple checkbox additions
2. **Console clear button** - Straightforward implementation
3. **Debug section** - Self-contained, optional feature

---

## Estimated Timeline

**Total Development Time:** 5-6 days

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Foundation & Refactoring | 2 days | None |
| Phase 2: New Features | 1.5 days | Phase 1 complete |
| Phase 3: Integration & Testing | 1.5 days | Phases 1-2 complete |
| Phase 4: Documentation & Release | 1 day | All phases complete |

**Parallel Work Opportunities:**
- Console panel & Queue panel can be developed in parallel
- Documentation can start while testing ongoing

---

## Success Criteria

Version 1.5.0 is complete when:

- [x] Two-panel layout fully functional
- [x] Batch queue visualization working
- [x] All existing features working (regression testing passed)
- [x] Drag-and-drop implemented or alternative solution in place
- [x] New enrichment options functional
- [x] Debug section functional
- [x] All components properly refactored
- [x] Configuration system updated
- [x] Documentation complete
- [x] Tested on both macOS and Windows 11
- [x] No critical bugs remaining

---

## Post-Release (v1.6.0 Ideas)

Features to consider for future versions:
- Batch export to multiple formats simultaneously
- Conversion profiles/presets
- Advanced scheduling (process queue at specific time)
- Cloud storage integration
- Preview panel for documents
- Conversion history/audit log
- Performance optimizations for large files
- Custom output filename templates

---

## Notes for Implementation

### Best Practices:
1. **Commit frequently** - After each task completion
2. **Test incrementally** - Don't wait until the end
3. **Keep v1.2.3 working** - Use feature branches
4. **Document as you go** - Update CLAUDE.md progressively
5. **Handle errors gracefully** - Never crash the GUI
6. **Provide user feedback** - Loading indicators, status messages

### Code Style:
- Follow existing patterns in the codebase
- Use type hints consistently
- Add docstrings to all public methods
- Keep methods focused and single-purpose
- Extract magic numbers to constants

### Testing Strategy:
- Manual testing for UI components
- Automated unit tests for queue logic
- Integration tests for conversion flow
- Cross-platform testing critical

---

## Conclusion

Version 1.5.0 represents a significant evolution of the Docling GUI, transforming it from a simple converter wrapper into a professional batch processing tool. The two-panel sidebar layout, enhanced queue visualization, and improved organization make the application more powerful and easier to use.

**Key Takeaway:** This is a **refactoring-first release**. The priority is clean architecture and maintainable code that sets the foundation for future enhancements.

**Recommended Approach:**
1. Start with widget components (lowest risk)
2. Build console and queue panels (medium risk)
3. Integrate sidebar (higher risk, depends on others)
4. Final integration and testing (critical path)

**Ready to begin implementation!**
