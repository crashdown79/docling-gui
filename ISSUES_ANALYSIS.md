# GitHub Issues & Feature Requests Analysis

**Generated**: 2025-12-13
**Current Version**: v1.3.0 (Phase 2 - Batch Processing)
**Branch**: beta

---

## Executive Summary

**Total Issues**: 4
- **Open**: 3 feature requests
- **Closed**: 1 bug (fixed in v1.2.4)

**Overall Assessment**: All open issues are high-quality feature requests that align well with the Phase 3 and Phase 4 roadmap. They represent natural evolution of the GUI toward a professional-grade tool.

**Recommended Priority**:
1. **Issue #3** - Debug/Visualization Options (Phase 3 - Technical Foundation)
2. **Issue #4** - Sidebar Layout (Phase 4 - UX Polish)
3. **Issue #2** - Configurable Model List (Phase 4 - Advanced Config)

---

## Issue Rankings & Analysis

### 🥇 Priority 1: Issue #3 - Advanced Debug & Visualization Options

**Status**: OPEN
**Type**: Feature Request
**Created**: 2025-12-13
**Impact**: High - Enables power users and debugging
**Complexity**: Medium-High
**Alignment**: Phase 3 (Advanced Options)

#### Problem Statement
Users have no visual feedback when parsing fails or produces suboptimal results. They must switch to CLI to debug issues, creating friction and limiting accessibility for non-technical users.

#### Requested Features

**1. Visualization/Debug Overlays** (5 options):
- `--show-layout` - Show bounding boxes around detected items
- `--debug-visualize-layout` - Visualize layout clusters
- `--debug-visualize-cells` - Show raw PDF cell detection
- `--debug-visualize-ocr` - Show OCR cell detection
- `--debug-visualize-tables` - Show detailed table cell structure

**2. OCR & Text Processing**:
- OCR toggle (already implemented ✅)
- Force OCR toggle (already implemented ✅)
- OCR Engine dropdown: auto, easyocr, tesseract, rapidocr, etc.
- OCR Language input (already implemented ✅)

**3. Structure & Tables**:
- Extract Tables toggle (`--tables` / `--no-tables`)
- Table Mode dropdown (already implemented ✅)

**4. Pipeline & Enrichment**:
- Pipeline type dropdown (already implemented ✅)
- VLM Model dropdown
- Enrich Code toggle (`--enrich-code`)
- Enrich Formulas toggle (already implemented ✅)
- Enrich Images (Classes) toggle (already implemented ✅)
- Enrich Images (Description) toggle (already implemented ✅)

#### Implementation Analysis

**Already Implemented** (8/15 features):
- ✅ OCR enable/disable
- ✅ Force OCR
- ✅ OCR Language input
- ✅ Table Mode dropdown
- ✅ Pipeline selection
- ✅ Enrich Formulas
- ✅ Enrich Picture Classes
- ✅ Enrich Picture Description

**Needs Implementation** (7/15 features):
- ❌ 5 Debug visualization toggles
- ❌ OCR Engine dropdown
- ❌ VLM Model dropdown

**Technical Effort**:
- **UI Changes**: Add Advanced Debug collapsible section (~50 lines)
- **Converter Changes**: Add parameters to `build_command()` (~30 lines)
- **Testing**: Verify each flag works correctly

**Files to Modify**:
1. `ui/main_window.py`:
   - Add debug section in `_create_options_section()`
   - Add checkboxes for 5 visualization flags
   - Add OCR Engine dropdown
   - Add VLM Model dropdown
   - Add Extract Tables toggle
   - Add Enrich Code toggle

2. `core/converter.py`:
   - Add parameters to `build_command()`:
     - `show_layout: bool`
     - `debug_visualize_layout: bool`
     - `debug_visualize_cells: bool`
     - `debug_visualize_ocr: bool`
     - `debug_visualize_tables: bool`
     - `ocr_engine: str`
     - `vlm_model: str`
     - `extract_tables: bool`
     - `enrich_code: bool`

3. `config.py`:
   - Add default values for new options

**Estimated Effort**: 4-6 hours
**Risk**: Low - All are direct CLI flag mappings
**Benefit**: High - Unlocks debugging capabilities, aligns with CLI parity

#### Recommended Implementation Order
1. Add OCR Engine dropdown (easy, high value)
2. Add 5 debug visualization toggles (medium, high value for debugging)
3. Add VLM Model dropdown (easy)
4. Add Extract Tables toggle (easy)
5. Add Enrich Code toggle (easy)

---

### 🥈 Priority 2: Issue #4 - Sidebar Layout Restructure

**Status**: OPEN
**Type**: Feature Request (UI/UX)
**Created**: 2025-12-13
**Impact**: High - Improves UX and scalability
**Complexity**: High
**Alignment**: Phase 4 (Polish)

#### Problem Statement
Current vertical stacking of options:
- Creates clutter as more options are added
- Pushes console output down, reducing visibility
- Doesn't scale well with debug options from Issue #3
- Doesn't utilize horizontal screen space on wide monitors

#### Proposed Solution
**Persistent Sidebar** with collapsible accordion sections:

```
┌─────────────────┬──────────────────────────────────────┐
│   SIDEBAR       │   MAIN CONTENT AREA                 │
│                 │                                      │
│ [ v ] Options   │   ┌─ Batch Queue ─────────────────┐ │
│   Pipeline      │   │ Files...                      │ │
│   Format        │   └───────────────────────────────┘ │
│   Image Export  │                                      │
│   OCR           │   ┌─ Console Output ──────────────┐ │
│   Enrichment    │   │ Processing logs...            │ │
│                 │   │                                │ │
│ [ > ] Debug     │   │                                │ │
│   (collapsed)   │   │                                │ │
│                 │   │                                │ │
│ [ > ] Settings  │   └───────────────────────────────┘ │
│   (collapsed)   │                                      │
└─────────────────┴──────────────────────────────────────┘
```

**Sidebar Sections**:

**[v] Options** (Core - Always Visible):
- Pipeline dropdown
- Output Format dropdown
- Image Export dropdown
- OCR: Enable, Force, Languages
- Enrichment: Formulas, Pictures

**[>] Debug** (Advanced - Collapsed):
- Verbosity dropdown
- 5 Visualization toggles
- OCR Engine dropdown
- VLM Model dropdown

**[>] Settings** (System - Collapsed):
- Mode: Online/Offline
- Download Models button
- Threads/Workers
- Accelerator dropdown

#### Implementation Analysis

**Technical Approach**:
This is a **major UI refactor**, not an incremental change. Two approaches:

**Option A: Refactor Existing Layout** (Recommended)
- Pros: Works with existing code structure
- Cons: Significant rework of grid positioning
- Effort: High

**Option B: Complete UI Rewrite**
- Pros: Clean slate, modern design patterns
- Cons: Must preserve all existing functionality
- Effort: Very High

**Files to Modify** (Option A):
1. `ui/main_window.py`:
   - Redesign `_create_widgets()` grid layout
   - Create `_create_sidebar()` method
   - Move all option sections into sidebar
   - Update main area to have 2 columns instead of 1
   - Resize window default width (~1200px for sidebar + content)

**UI Framework Considerations**:
- CustomTkinter supports grid and pack layouts
- Sidebar can use `CTkScrollableFrame` for long option lists
- Accordion/collapsible sections already implemented (queue toggle)
- Need to handle window resize gracefully

**Estimated Effort**: 12-16 hours
**Risk**: Medium-High - Major layout changes can introduce regressions
**Benefit**: High - Professional appearance, better scalability

#### Recommended Approach
1. **Phase 1**: Create sidebar structure skeleton (2 hours)
2. **Phase 2**: Move existing options to sidebar sections (4 hours)
3. **Phase 3**: Adjust main content area layout (3 hours)
4. **Phase 4**: Test and fix layout issues (3 hours)
5. **Phase 5**: Polish and responsive behavior (2 hours)

**Prerequisites**:
- Complete Issue #3 first (debug options)
- This ensures all options are known before layout design

---

### 🥉 Priority 3: Issue #2 - Configurable Model Download List

**Status**: OPEN
**Type**: Feature Request
**Created**: 2025-12-12
**Impact**: Medium - Power user feature
**Complexity**: Medium
**Alignment**: Phase 4 (Advanced Features)

#### Problem Statement
Users want to:
- Add custom HuggingFace models for download
- Remove unused models from the download list
- Configure model repositories for specialized tasks

Currently, the model list is hardcoded in the download dialog:
1. All Standard Models
2. SmolDocling-256M
3. SmolVLM-256M-Instruct

#### Proposed Solution
**Configuration-based Model Management**

Two implementation options:

**Option A: UI-based Model Manager**
- Settings dialog with "Manage Models" section
- Table/list view of available models
- Add/Edit/Delete model entries
- Fields: Name, HuggingFace Repo, Description
- Stored in config.json

**Option B: Config File Only**
- Document config.json structure for models
- Users edit JSON manually
- UI reads from config

#### Implementation Analysis

**Recommended: Option A (UI-based)**

**Data Structure** (`config.json`):
```json
{
  "models": {
    "availableModels": [
      {
        "id": "all_standard",
        "name": "All Standard Models",
        "command": "docling-tools models download",
        "enabled": true
      },
      {
        "id": "smoldocling",
        "name": "SmolDocling-256M",
        "command": "docling-tools models download-hf-repo ds4sd/SmolDocling-256M-preview",
        "enabled": true
      },
      {
        "id": "smolvlm",
        "name": "SmolVLM-256M-Instruct",
        "command": "docling-tools models download-hf-repo HuggingFaceTB/SmolVLM-256M-Instruct",
        "enabled": true
      }
    ],
    "customModels": []
  }
}
```

**UI Changes**:

1. **Download Models Dialog**:
   - Read checkboxes from config instead of hardcoding
   - Add "Manage Models..." button
   - Generate checkboxes dynamically from config

2. **Model Manager Dialog** (new):
   - List view of all models (enabled/disabled)
   - Add Model button → dialog with fields:
     - Name
     - HuggingFace Repo (e.g., "owner/model-name")
     - Type: Standard | HF Repo
   - Edit/Delete buttons per model
   - Enable/Disable checkboxes

**Files to Modify**:
1. `config.py`:
   - Add default model structure to `_get_default_config()`
   - Add methods: `get_available_models()`, `add_custom_model()`, `delete_model()`

2. `ui/main_window.py`:
   - Refactor `_download_models()` to read from config
   - Add `_manage_models()` method
   - Create model manager dialog

3. `core/converter.py`:
   - Update `download_models()` to accept dynamic command list

**Estimated Effort**: 6-8 hours
**Risk**: Low - Self-contained feature
**Benefit**: Medium - Useful for advanced users, niche use cases

#### Recommended Implementation
1. Add model config structure (1 hour)
2. Refactor download dialog to read from config (2 hours)
3. Create model manager dialog UI (3 hours)
4. Test with custom HF repos (2 hours)

---

### ✅ Closed Issue: #1 - Offline Mode Bug

**Status**: CLOSED (Fixed in v1.2.4)
**Type**: Bug
**Created**: 2025-12-12
**Closed**: 2025-12-12

#### Problem
Offline mode failed even after downloading models. Validation checked wrong path.

#### Solution Implemented
- Fixed artifacts path: Pass `{artifacts_path}/models` to CLI
- Updated validation to check `models/{model_name}/` directory structure
- Released in v1.2.4

**No further action needed** ✅

---

## Priority Ranking Summary

### Recommended Implementation Order

**Phase 3 Release (v1.4.0) - "Advanced Options"**
1. ✅ Batch Processing (already in beta)
2. 🎯 **Issue #3** - Debug & Visualization Options
   - Add OCR Engine dropdown
   - Add 5 debug visualization toggles
   - Add VLM Model dropdown
   - Add Extract Tables toggle
   - Add Enrich Code toggle
   - **Effort**: 4-6 hours
   - **Impact**: High

**Phase 4 Release (v1.5.0) - "Professional UI & Polish"**
3. 🎯 **Issue #4** - Sidebar Layout
   - Complete UI restructure
   - Sidebar with collapsible sections
   - Better space utilization
   - **Effort**: 12-16 hours
   - **Impact**: High
   - **Prerequisite**: Complete Issue #3 first

4. 🎯 **Issue #2** - Configurable Model List
   - Model manager dialog
   - Custom HF repo support
   - **Effort**: 6-8 hours
   - **Impact**: Medium

---

## Implementation Roadmap

### Immediate (v1.3.0 - Current Beta)
- [x] Batch queue processing
- [x] Multi-file support
- [x] Queue management UI
- **Status**: Complete, ready for merge to main

### Next (v1.4.0 - Phase 3)
**Target**: Advanced Options Expansion
**Estimated Timeline**: 1 week

**Scope**:
- [ ] OCR Engine selection
- [ ] VLM Model selection
- [ ] Debug visualization toggles (5 options)
- [ ] Extract Tables toggle
- [ ] Enrich Code toggle

**Deliverables**:
- Full debug/visualization capabilities
- Parity with CLI advanced options
- Enhanced troubleshooting for users

### Future (v1.5.0 - Phase 4)
**Target**: Professional UI & Configuration
**Estimated Timeline**: 2-3 weeks

**Scope**:
- [ ] Sidebar layout restructure
- [ ] Configurable model downloads
- [ ] Settings dialog
- [ ] Window size/position persistence
- [ ] Keyboard shortcuts
- [ ] Drag & drop support

**Deliverables**:
- Modern, scalable UI layout
- Advanced configuration options
- Professional user experience

---

## Technical Debt & Considerations

### Known Limitations
1. **No URL support** - Planned for Phase 2, not yet implemented
2. **No drag & drop** - Placeholder shown, not functional
3. **No preview pane** - Would complement debug visualizations
4. **No configuration profiles** - Save/load presets

### Architecture Notes
1. **CustomTkinter Limitations**:
   - No native sidebar widget (need custom layout)
   - Accordion sections require manual implementation
   - Preview pane would need PDF rendering library

2. **Debug Image Display**:
   - Issue #3 visualization toggles create PNG files
   - Would need image viewer component to show in UI
   - Alternative: Just enable flags, user opens files manually

3. **Config Migration**:
   - v1.2.4 → v1.3.0: No breaking changes
   - v1.3.0 → v1.4.0: Add new option keys
   - v1.4.0 → v1.5.0: May need config migration for sidebar layout

---

## Recommendations

### For v1.4.0 (Phase 3)
**Focus**: Complete Issue #3 (Debug Options)

**Rationale**:
1. Quick wins - most options are simple dropdowns/checkboxes
2. High user value - enables debugging without CLI
3. Aligns with existing Phase 3 roadmap
4. Provides foundation for Issue #4 sidebar (know what options exist)

**Skip for now**:
- Issue #4 (Sidebar) - Wait until all options are known
- Issue #2 (Model Config) - Nice-to-have, not critical

### For v1.5.0 (Phase 4)
**Focus**: Complete Issue #4 (Sidebar), then Issue #2 (Models)

**Rationale**:
1. Sidebar enables scalable option organization
2. Better UX for existing and new options
3. Model config is standalone, can be added anytime

---

## Testing Requirements

### For Issue #3 (Debug Options)
- [ ] Test each debug flag individually
- [ ] Test with different pipelines (standard, vlm, asr)
- [ ] Test with different OCR engines
- [ ] Verify debug images are generated correctly
- [ ] Test combinations of flags

### For Issue #4 (Sidebar)
- [ ] Test window resize behavior
- [ ] Test collapsible section state persistence
- [ ] Test on different screen sizes
- [ ] Verify all existing functionality preserved
- [ ] Test theme switching with sidebar

### For Issue #2 (Model Config)
- [ ] Test adding custom HF repos
- [ ] Test deleting models
- [ ] Test enabling/disabling models
- [ ] Verify downloads work with custom models
- [ ] Test config persistence

---

## Conclusion

All three open issues represent valuable enhancements that align with the project roadmap. The recommended approach is:

1. **Merge v1.3.0 (beta → main)** - Batch processing is complete and tested
2. **Implement v1.4.0** - Focus on Issue #3 (Debug Options) for Phase 3
3. **Plan v1.5.0** - Tackle Issue #4 (Sidebar) and Issue #2 (Models) for Phase 4

This progression:
- ✅ Delivers incremental value
- ✅ Maintains stability (smaller, focused releases)
- ✅ Aligns with existing roadmap
- ✅ Addresses user requests systematically

**Estimated Total Effort**: 22-30 hours across 2 releases
**User Impact**: High - Transforms GUI from basic wrapper to professional tool

---

**Document Version**: 1.0
**Last Updated**: 2025-12-13
**Next Review**: After v1.3.0 release to main
