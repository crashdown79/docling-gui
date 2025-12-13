import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import os
import platform
from typing import Optional
from datetime import datetime

from core.converter import DoclingConverter
from core.queue import ConversionQueue, QueueItem, QueueItemStatus
from config import Config


class MainWindow(ctk.CTk):
    """Main application window for Docling GUI."""

    def __init__(self):
        super().__init__()

        # Initialize components
        self.config = Config()
        self.converter = DoclingConverter()
        self.queue = ConversionQueue()

        # Window setup
        self.title("Docling GUI - Document Converter")
        width = self.config.get("window", "width", default=900)
        height = self.config.get("window", "height", default=900)  # Increased for queue section
        self.geometry(f"{width}x{height}")

        # Set theme
        theme = self.config.get("interface", "theme", default="dark")
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")

        # State variables
        self.selected_file: Optional[str] = None
        self.is_processing = False
        self.log_file_handle = None
        self.current_log_file = None
        self.current_queue_item: Optional[QueueItem] = None
        self.queue_mode = False  # True when processing queue, False for single file

        # Create UI
        self._create_widgets()
        self._check_docling()

        # Auto-start logging if enabled
        if self.enable_log_var.get():
            self._create_log_file()

        # Window close handler
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_widgets(self):
        """Create all UI widgets."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)  # Console row expands

        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Docling Document Converter",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Input Section
        self._create_input_section()

        # Queue Section (NEW)
        self._create_queue_section()

        # Output Section
        self._create_output_section()

        # Processing Options Section
        self._create_options_section()

        # Control Buttons
        self._create_control_section()

        # Progress Section
        self._create_progress_section()

        # Console Output
        self._create_console_section()

        # Status Bar
        self._create_status_bar()

    def _create_input_section(self):
        """Create file input section."""
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        # Label
        ctk.CTkLabel(
            input_frame,
            text="Input:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # File path display
        self.file_path_var = ctk.StringVar(value="No file selected")
        self.file_path_label = ctk.CTkLabel(
            input_frame,
            textvariable=self.file_path_var,
            anchor="w"
        )
        self.file_path_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Button container
        btn_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=2, padx=10, pady=10)

        # Select file button (single file)
        self.select_btn = ctk.CTkButton(
            btn_frame,
            text="Select File",
            command=self._select_file,
            width=110
        )
        self.select_btn.pack(side="left", padx=(0, 5))

        # Add Files button (multiple files to queue)
        self.add_files_btn = ctk.CTkButton(
            btn_frame,
            text="➕ Add Files",
            command=self._add_files_to_queue,
            width=110,
            fg_color="gray40",
            hover_color="gray30"
        )
        self.add_files_btn.pack(side="left", padx=5)

        # Add Folder button
        self.add_folder_btn = ctk.CTkButton(
            btn_frame,
            text="📁 Add Folder",
            command=self._add_folder_to_queue,
            width=110,
            fg_color="gray40",
            hover_color="gray30"
        )
        self.add_folder_btn.pack(side="left", padx=(5, 0))

    def _create_queue_section(self):
        """Create batch queue section."""
        queue_frame = ctk.CTkFrame(self)
        queue_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        queue_frame.grid_columnconfigure(0, weight=1)

        # Section title with toggle button and stats
        title_frame = ctk.CTkFrame(queue_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        title_frame.grid_columnconfigure(1, weight=1)

        # Toggle button
        self.queue_visible = ctk.BooleanVar(value=False)  # Collapsed by default
        self.queue_toggle_btn = ctk.CTkButton(
            title_frame,
            text="▶",
            width=30,
            height=24,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._toggle_queue
        )
        self.queue_toggle_btn.grid(row=0, column=0, padx=(0, 5))

        # Title
        ctk.CTkLabel(
            title_frame,
            text="Batch Queue",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=1, sticky="w")

        # Queue statistics
        self.queue_stats_var = ctk.StringVar(value="(0 files)")
        self.queue_stats_label = ctk.CTkLabel(
            title_frame,
            textvariable=self.queue_stats_var,
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.queue_stats_label.grid(row=0, column=2, padx=10)

        # Queue container (collapsible)
        self.queue_container = ctk.CTkFrame(queue_frame)
        # Start hidden
        # self.queue_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.queue_container.grid_columnconfigure(0, weight=1)
        self.queue_container.grid_rowconfigure(0, weight=1)

        # Queue list (scrollable)
        self.queue_list_frame = ctk.CTkScrollableFrame(
            self.queue_container,
            height=150,
            label_text="Queue Items"
        )
        self.queue_list_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.queue_list_frame.grid_columnconfigure(0, weight=1)

        # Queue items will be added dynamically
        self.queue_item_widgets = {}  # Maps item_id -> widget frame

        # Queue control buttons
        btn_frame = ctk.CTkFrame(self.queue_container, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=5, pady=5)

        # Clear completed button
        clear_completed_btn = ctk.CTkButton(
            btn_frame,
            text="Clear Completed",
            command=self._clear_completed_queue,
            width=120,
            fg_color="gray40",
            hover_color="gray30"
        )
        clear_completed_btn.pack(side="left", padx=5)

        # Clear all button
        clear_all_btn = ctk.CTkButton(
            btn_frame,
            text="Clear All",
            command=self._clear_all_queue,
            width=100,
            fg_color="gray40",
            hover_color="gray30"
        )
        clear_all_btn.pack(side="left", padx=5)

    def _create_output_section(self):
        """Create output configuration section."""
        output_frame = ctk.CTkFrame(self)
        output_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        output_frame.grid_columnconfigure(1, weight=1)
        output_frame.grid_columnconfigure(3, weight=1)

        # Output format
        ctk.CTkLabel(
            output_frame,
            text="Output Format:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        default_format = self.config.get("general", "defaultOutputFormat", default="md")
        self.output_format_var = ctk.StringVar(value=default_format)
        format_menu = ctk.CTkOptionMenu(
            output_frame,
            variable=self.output_format_var,
            values=["md", "json", "html", "html_split_page", "text", "doctags"],
            width=150
        )
        format_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Output directory
        ctk.CTkLabel(
            output_frame,
            text="Output Directory:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=2, padx=(20, 10), pady=10, sticky="w")

        default_dir = self.config.get("general", "defaultOutputDir", default=str(Path.home() / "Documents"))
        self.output_dir_var = ctk.StringVar(value=default_dir)
        self.output_dir_entry = ctk.CTkEntry(
            output_frame,
            textvariable=self.output_dir_var
        )
        self.output_dir_entry.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # Browse button
        browse_btn = ctk.CTkButton(
            output_frame,
            text="Browse",
            command=self._select_output_dir,
            width=100
        )
        browse_btn.grid(row=0, column=4, padx=10, pady=10)

        # Open folder button
        open_btn = ctk.CTkButton(
            output_frame,
            text="Open Folder",
            command=self._open_output_folder,
            width=100
        )
        open_btn.grid(row=0, column=5, padx=10, pady=10)

    def _create_options_section(self):
        """Create processing options section."""
        options_frame = ctk.CTkFrame(self)
        options_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        options_frame.grid_columnconfigure(0, weight=1)

        # Section title with toggle button
        title_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.options_visible = ctk.BooleanVar(value=True)
        self.toggle_btn = ctk.CTkButton(
            title_frame,
            text="▼",
            width=30,
            height=24,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._toggle_options
        )
        self.toggle_btn.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            title_frame,
            text="Processing Options",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")

        # Options container
        self.opts_container = ctk.CTkFrame(options_frame, fg_color="transparent")
        self.opts_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.opts_container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Processing Mode
        mode_frame = ctk.CTkFrame(self.opts_container, fg_color="transparent")
        mode_frame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(
            mode_frame,
            text="Mode:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))

        default_mode = self.config.get("processing", "mode", default="online")
        self.processing_mode_var = ctk.StringVar(value=default_mode)
        mode_online = ctk.CTkRadioButton(
            mode_frame,
            text="Online",
            variable=self.processing_mode_var,
            value="online"
        )
        mode_online.pack(side="left", padx=5)

        mode_offline = ctk.CTkRadioButton(
            mode_frame,
            text="Offline",
            variable=self.processing_mode_var,
            value="offline"
        )
        mode_offline.pack(side="left", padx=5)

        # OCR Enable
        ocr_enabled = self.config.get("defaults", "ocrEnabled", default=True)
        self.ocr_var = ctk.BooleanVar(value=ocr_enabled)
        ocr_check = ctk.CTkCheckBox(
            self.opts_container,
            text="Enable OCR",
            variable=self.ocr_var,
            font=ctk.CTkFont(weight="bold")
        )
        ocr_check.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Force OCR
        force_ocr = self.config.get("defaults", "forceOcr", default=False)
        self.force_ocr_var = ctk.BooleanVar(value=force_ocr)
        force_ocr_check = ctk.CTkCheckBox(
            self.opts_container,
            text="Force OCR",
            variable=self.force_ocr_var
        )
        force_ocr_check.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Pipeline
        pipeline_frame = ctk.CTkFrame(self.opts_container, fg_color="transparent")
        pipeline_frame.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(
            pipeline_frame,
            text="Pipeline:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))

        default_pipeline = self.config.get("defaults", "pipeline", default="standard")
        self.pipeline_var = ctk.StringVar(value=default_pipeline)
        pipeline_menu = ctk.CTkOptionMenu(
            pipeline_frame,
            variable=self.pipeline_var,
            values=["standard", "vlm", "asr"],
            width=120
        )
        pipeline_menu.pack(side="left")

        # Row 1: OCR Language
        ocr_lang_frame = ctk.CTkFrame(self.opts_container, fg_color="transparent")
        ocr_lang_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            ocr_lang_frame,
            text="OCR Languages:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))

        default_ocr_lang = self.config.get("defaults", "ocrLanguages", default="eng")
        self.ocr_lang_var = ctk.StringVar(value=default_ocr_lang)
        self.ocr_lang_entry = ctk.CTkEntry(
            ocr_lang_frame,
            textvariable=self.ocr_lang_var,
            placeholder_text="e.g., eng,deu,fra",
            width=180
        )
        self.ocr_lang_entry.pack(side="left", padx=5)

        # Language preset buttons
        preset_frame = ctk.CTkFrame(ocr_lang_frame, fg_color="transparent")
        preset_frame.pack(side="left", padx=5)

        lang_presets = [
            ("EN", "eng"),
            ("DE", "deu"),
            ("FR", "fra"),
            ("ES", "spa"),
            ("IT", "ita"),
            ("ZH", "chi_sim")
        ]

        for label, code in lang_presets:
            btn = ctk.CTkButton(
                preset_frame,
                text=label,
                width=35,
                height=24,
                command=lambda c=code: self._add_ocr_language(c)
            )
            btn.pack(side="left", padx=2)

        # Row 2: Enrichment options
        enrich_frame = ctk.CTkFrame(self.opts_container, fg_color="transparent")
        enrich_frame.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(
            enrich_frame,
            text="Enrichment:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))

        # Formula enrichment
        enrich_formula = self.config.get("defaults", "enrichFormula", default=False)
        self.enrich_formula_var = ctk.BooleanVar(value=enrich_formula)
        ctk.CTkCheckBox(
            enrich_frame,
            text="Formulas",
            variable=self.enrich_formula_var
        ).pack(side="left", padx=5)

        # Picture classes enrichment
        enrich_pic_classes = self.config.get("defaults", "enrichPictureClasses", default=False)
        self.enrich_picture_classes_var = ctk.BooleanVar(value=enrich_pic_classes)
        ctk.CTkCheckBox(
            enrich_frame,
            text="Picture Classes",
            variable=self.enrich_picture_classes_var
        ).pack(side="left", padx=5)

        # Picture description enrichment
        enrich_pic_desc = self.config.get("defaults", "enrichPictureDescription", default=False)
        self.enrich_picture_description_var = ctk.BooleanVar(value=enrich_pic_desc)
        ctk.CTkCheckBox(
            enrich_frame,
            text="Picture Descriptions",
            variable=self.enrich_picture_description_var
        ).pack(side="left", padx=5)

        # Row 3: Image Export Mode and Verbose
        settings_frame = ctk.CTkFrame(self.opts_container, fg_color="transparent")
        settings_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        # Image Export Mode
        img_export_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        img_export_frame.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            img_export_frame,
            text="Image Export:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))

        default_image_mode = self.config.get("defaults", "imageExportMode", default="embedded")
        self.image_export_mode_var = ctk.StringVar(value=default_image_mode)
        image_export_menu = ctk.CTkOptionMenu(
            img_export_frame,
            variable=self.image_export_mode_var,
            values=["embedded", "placeholder", "referenced"],
            width=120
        )
        image_export_menu.pack(side="left")

        # Verbose Mode
        verbose_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        verbose_frame.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            verbose_frame,
            text="Verbosity:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))

        default_verbose = self.config.get("defaults", "verbose", default=0)
        self.verbose_var = ctk.IntVar(value=default_verbose)
        verbose_menu = ctk.CTkOptionMenu(
            verbose_frame,
            variable=self.verbose_var,
            values=["0 (Normal)", "1 (Info)", "2 (Debug)"],
            width=120,
            command=self._on_verbose_change
        )
        verbose_menu.pack(side="left")

        # Download Models Button
        download_btn = ctk.CTkButton(
            settings_frame,
            text="📥 Download Models",
            command=self._download_models,
            width=140,
            fg_color="gray40",
            hover_color="gray30"
        )
        download_btn.pack(side="left", padx=(0, 10))

        # Row 4: Advanced Options (OCR Engine, VLM Model, Tables, Code)
        advanced_frame = ctk.CTkFrame(self.opts_container, fg_color="transparent")
        advanced_frame.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        # OCR Engine
        ocr_engine_frame = ctk.CTkFrame(advanced_frame, fg_color="transparent")
        ocr_engine_frame.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            ocr_engine_frame,
            text="OCR Engine:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))

        default_ocr_engine = self.config.get("defaults", "ocrEngine", default="auto")
        self.ocr_engine_var = ctk.StringVar(value=default_ocr_engine)
        ocr_engine_menu = ctk.CTkOptionMenu(
            ocr_engine_frame,
            variable=self.ocr_engine_var,
            values=["auto", "easyocr", "tesseract", "rapidocr", "ocrmac", "tesserocr"],
            width=120
        )
        ocr_engine_menu.pack(side="left")

        # VLM Model (when pipeline=vlm)
        vlm_model_frame = ctk.CTkFrame(advanced_frame, fg_color="transparent")
        vlm_model_frame.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(
            vlm_model_frame,
            text="VLM Model:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))

        default_vlm_model = self.config.get("defaults", "vlmModel", default="smoldocling")
        self.vlm_model_var = ctk.StringVar(value=default_vlm_model)
        vlm_model_menu = ctk.CTkOptionMenu(
            vlm_model_frame,
            variable=self.vlm_model_var,
            values=["smoldocling", "smoldocling_vllm", "granite_vision", "granite_vision_vllm", "granite_vision_ollama", "got_ocr_2"],
            width=150
        )
        vlm_model_menu.pack(side="left")

        # Extract Tables
        extract_tables = self.config.get("defaults", "extractTables", default=True)
        self.extract_tables_var = ctk.BooleanVar(value=extract_tables)
        ctk.CTkCheckBox(
            advanced_frame,
            text="Extract Tables",
            variable=self.extract_tables_var
        ).pack(side="left", padx=5)

        # Enrich Code
        enrich_code = self.config.get("defaults", "enrichCode", default=False)
        self.enrich_code_var = ctk.BooleanVar(value=enrich_code)
        ctk.CTkCheckBox(
            advanced_frame,
            text="Enrich Code",
            variable=self.enrich_code_var
        ).pack(side="left", padx=5)

        # Row 5: Debug Visualization Section (Collapsible)
        debug_section = ctk.CTkFrame(self.opts_container, fg_color="gray25")
        debug_section.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        # Debug section title with toggle
        debug_title_frame = ctk.CTkFrame(debug_section, fg_color="transparent")
        debug_title_frame.pack(fill="x", padx=10, pady=5)

        self.debug_visible = ctk.BooleanVar(value=False)  # Collapsed by default
        self.debug_toggle_btn = ctk.CTkButton(
            debug_title_frame,
            text="▶",
            width=30,
            height=24,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._toggle_debug
        )
        self.debug_toggle_btn.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            debug_title_frame,
            text="Advanced Debug & Visualization",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left")

        # Debug options container (collapsible)
        self.debug_container = ctk.CTkFrame(debug_section, fg_color="transparent")
        # Start hidden
        # self.debug_container.pack(fill="x", padx=10, pady=(0, 10))

        # Debug visualization toggles
        debug_viz_frame = ctk.CTkFrame(self.debug_container, fg_color="transparent")
        debug_viz_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            debug_viz_frame,
            text="Visualizations:",
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=(0, 10))

        # Show Layout
        show_layout = self.config.get("defaults", "showLayout", default=False)
        self.show_layout_var = ctk.BooleanVar(value=show_layout)
        ctk.CTkCheckBox(
            debug_viz_frame,
            text="Show Layout Boxes",
            variable=self.show_layout_var
        ).pack(side="left", padx=5)

        # Debug: Visualize Layout Clusters
        debug_layout = self.config.get("defaults", "debugVisualizeLayout", default=False)
        self.debug_visualize_layout_var = ctk.BooleanVar(value=debug_layout)
        ctk.CTkCheckBox(
            debug_viz_frame,
            text="Layout Clusters",
            variable=self.debug_visualize_layout_var
        ).pack(side="left", padx=5)

        # Debug: Visualize PDF Cells
        debug_cells = self.config.get("defaults", "debugVisualizeCells", default=False)
        self.debug_visualize_cells_var = ctk.BooleanVar(value=debug_cells)
        ctk.CTkCheckBox(
            debug_viz_frame,
            text="PDF Cells",
            variable=self.debug_visualize_cells_var
        ).pack(side="left", padx=5)

        # Debug: Visualize OCR Cells
        debug_ocr = self.config.get("defaults", "debugVisualizeOcr", default=False)
        self.debug_visualize_ocr_var = ctk.BooleanVar(value=debug_ocr)
        ctk.CTkCheckBox(
            debug_viz_frame,
            text="OCR Cells",
            variable=self.debug_visualize_ocr_var
        ).pack(side="left", padx=5)

        # Debug: Visualize Table Cells
        debug_tables = self.config.get("defaults", "debugVisualizeTables", default=False)
        self.debug_visualize_tables_var = ctk.BooleanVar(value=debug_tables)
        ctk.CTkCheckBox(
            debug_viz_frame,
            text="Table Cells",
            variable=self.debug_visualize_tables_var
        ).pack(side="left", padx=5)

    def _toggle_debug(self):
        """Toggle visibility of debug options."""
        if self.debug_visible.get():
            # Hide debug options
            self.debug_container.pack_forget()
            self.debug_toggle_btn.configure(text="▶")
            self.debug_visible.set(False)
        else:
            # Show debug options
            self.debug_container.pack(fill="x", padx=10, pady=(0, 10))
            self.debug_toggle_btn.configure(text="▼")
            self.debug_visible.set(True)

    def _on_verbose_change(self, choice):
        """Handle verbose mode selection change."""
        # Extract the number from the choice string
        verbose_level = int(choice.split()[0])
        self.verbose_var.set(verbose_level)

    def _toggle_options(self):
        """Toggle visibility of processing options."""
        if self.options_visible.get():
            # Hide options
            self.opts_container.grid_remove()
            self.toggle_btn.configure(text="▶")
            self.options_visible.set(False)
        else:
            # Show options
            self.opts_container.grid()
            self.toggle_btn.configure(text="▼")
            self.options_visible.set(True)

    def _add_ocr_language(self, lang_code):
        """Add language code to OCR languages field."""
        current = self.ocr_lang_var.get().strip()
        if not current:
            self.ocr_lang_var.set(lang_code)
        else:
            # Check if language already in list
            langs = [l.strip() for l in current.split(',')]
            if lang_code not in langs:
                langs.append(lang_code)
                self.ocr_lang_var.set(','.join(langs))

    def _create_control_section(self):
        """Create control buttons section."""
        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        control_frame.grid_columnconfigure(0, weight=1)

        # Buttons container
        btn_container = ctk.CTkFrame(control_frame, fg_color="transparent")
        btn_container.pack(expand=True)

        # Convert button
        self.convert_btn = ctk.CTkButton(
            btn_container,
            text="Convert",
            command=self._start_conversion,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.convert_btn.pack(side="left", padx=10)

        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            btn_container,
            text="Cancel",
            command=self._cancel_conversion,
            width=120,
            height=40,
            fg_color="gray40",
            hover_color="gray30",
            state="disabled"
        )
        self.cancel_btn.pack(side="left", padx=10)

    def _create_progress_section(self):
        """Create progress section."""
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")
        progress_frame.grid_columnconfigure(0, weight=1)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(progress_frame, mode="indeterminate")
        self.progress_bar.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.progress_bar.set(0)

        # Status label
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            progress_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=1, column=0, padx=10, pady=5)

    def _create_console_section(self):
        """Create console output section."""
        console_frame = ctk.CTkFrame(self)
        console_frame.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="nsew")
        console_frame.grid_columnconfigure(0, weight=1)
        console_frame.grid_rowconfigure(1, weight=1)

        # Title and log enable checkbox
        title_frame = ctk.CTkFrame(console_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        ctk.CTkLabel(
            title_frame,
            text="Console Output",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")

        # Log enable checkbox
        enable_logging = self.config.get("general", "enableLogging", default=False)
        self.enable_log_var = ctk.BooleanVar(value=enable_logging)
        log_check = ctk.CTkCheckBox(
            title_frame,
            text="💾 Save to Log File",
            variable=self.enable_log_var,
            command=self._on_log_enable_change
        )
        log_check.pack(side="left", padx=20)

        # Text widget
        self.console_text = ctk.CTkTextbox(
            console_frame,
            height=200,
            font=ctk.CTkFont(family="Courier", size=10)
        )
        self.console_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Control buttons
        console_btn_frame = ctk.CTkFrame(console_frame, fg_color="transparent")
        console_btn_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")

        ctk.CTkButton(
            console_btn_frame,
            text="Clear Log",
            command=self._clear_console,
            width=100
        ).pack(side="left", padx=5)

        # Initial message
        self._log_console("Docling GUI initialized. Ready to convert documents.\n")

    def _create_status_bar(self):
        """Create status bar."""
        status_frame = ctk.CTkFrame(self, height=30, fg_color="gray20")
        status_frame.grid(row=8, column=0, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        # Ready indicator
        self.ready_label = ctk.CTkLabel(
            status_frame,
            text="● Ready",
            font=ctk.CTkFont(size=10),
            text_color="green"
        )
        self.ready_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Version info
        version_label = ctk.CTkLabel(
            status_frame,
            text="Docling GUI v1.4.0",
            font=ctk.CTkFont(size=10),
            text_color="gray60"
        )
        version_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")

    def _check_docling(self):
        """Check if Docling is installed."""
        if not self.converter.check_docling_installed():
            messagebox.showwarning(
                "Docling Not Found",
                "Docling CLI not found. Please install it:\n\npip install docling\n\nSome features may not work."
            )
            self._log_console("WARNING: Docling CLI not found. Please install: pip install docling\n")
        else:
            self._log_console(f"Using Docling: {self.converter.docling_path}\n")

    def _select_file(self):
        """Open file dialog to select input file."""
        filetypes = [
            ("All Supported", "*.pdf *.docx *.pptx *.html *.htm *.jpg *.jpeg *.png *.md *.csv *.xlsx"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("PowerPoint", "*.pptx"),
            ("HTML Files", "*.html *.htm"),
            ("Images", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("All Files", "*.*")
        ]

        filename = filedialog.askopenfilename(
            title="Select Document",
            filetypes=filetypes
        )

        if filename:
            self.selected_file = filename
            self.file_path_var.set(filename)
            self._log_console(f"Selected file: {filename}\n")

    def _select_output_dir(self):
        """Open directory dialog to select output directory."""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir_var.get()
        )

        if directory:
            self.output_dir_var.set(directory)
            self.config.set("general", "defaultOutputDir", value=directory)
            self._log_console(f"Output directory: {directory}\n")

    def _open_output_folder(self):
        """Open output folder in file manager."""
        output_dir = self.output_dir_var.get()
        if os.path.exists(output_dir):
            if platform.system() == "Windows":
                os.startfile(output_dir)
            elif platform.system() == "Darwin":  # macOS
                os.system(f'open "{output_dir}"')
            else:  # Linux
                os.system(f'xdg-open "{output_dir}"')
        else:
            messagebox.showerror("Error", f"Directory does not exist:\n{output_dir}")

    # Queue Management Methods

    def _toggle_queue(self):
        """Toggle visibility of queue section."""
        if self.queue_visible.get():
            # Hide queue
            self.queue_container.grid_remove()
            self.queue_toggle_btn.configure(text="▶")
            self.queue_visible.set(False)
        else:
            # Show queue
            self.queue_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
            self.queue_toggle_btn.configure(text="▼")
            self.queue_visible.set(True)

    def _add_files_to_queue(self):
        """Add multiple files to the queue."""
        filetypes = [
            ("All Supported", "*.pdf *.docx *.pptx *.html *.htm *.jpg *.jpeg *.png *.md *.csv *.xlsx"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("PowerPoint", "*.pptx"),
            ("HTML Files", "*.html *.htm"),
            ("Images", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("All Files", "*.*")
        ]

        filenames = filedialog.askopenfilenames(
            title="Select Files to Add to Queue",
            filetypes=filetypes
        )

        if filenames:
            added_items = self.queue.add_files(list(filenames))
            self._log_console(f"Added {len(added_items)} file(s) to queue\n")

            for item in added_items:
                self._add_queue_item_widget(item)

            self._update_queue_stats()

            # Auto-expand queue if files were added
            if not self.queue_visible.get():
                self._toggle_queue()

    def _add_folder_to_queue(self):
        """Add all files from a folder to the queue."""
        folder = filedialog.askdirectory(
            title="Select Folder to Add to Queue"
        )

        if folder:
            try:
                added_items = self.queue.add_folder(folder, recursive=True)
                self._log_console(f"Added {len(added_items)} file(s) from folder: {folder}\n")

                for item in added_items:
                    self._add_queue_item_widget(item)

                self._update_queue_stats()

                # Auto-expand queue if files were added
                if not self.queue_visible.get():
                    self._toggle_queue()

            except Exception as e:
                messagebox.showerror("Error", f"Could not add folder:\n{str(e)}")

    def _add_queue_item_widget(self, item: QueueItem):
        """Create and add a widget for a queue item."""
        # Create item frame
        item_frame = ctk.CTkFrame(self.queue_list_frame, fg_color="gray25")
        item_frame.grid(row=len(self.queue_item_widgets), column=0, padx=5, pady=2, sticky="ew")
        item_frame.grid_columnconfigure(2, weight=1)

        # Status icon
        status_label = ctk.CTkLabel(
            item_frame,
            text=item.get_status_icon(),
            font=ctk.CTkFont(size=16),
            text_color=item.get_status_color(),
            width=30
        )
        status_label.grid(row=0, column=0, padx=5, pady=5)

        # Filename
        filename_label = ctk.CTkLabel(
            item_frame,
            text=item.filename,
            anchor="w",
            font=ctk.CTkFont(size=12)
        )
        filename_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # File size and format
        info_label = ctk.CTkLabel(
            item_frame,
            text=f"{item.file_format.upper()} • {item.get_size_string()}",
            font=ctk.CTkFont(size=10),
            text_color="gray60"
        )
        info_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Status text
        status_text_label = ctk.CTkLabel(
            item_frame,
            text=item.status.value.capitalize(),
            font=ctk.CTkFont(size=10),
            text_color=item.get_status_color(),
            width=80
        )
        status_text_label.grid(row=0, column=3, padx=5, pady=5)

        # Remove button
        remove_btn = ctk.CTkButton(
            item_frame,
            text="✕",
            width=30,
            height=24,
            fg_color="gray40",
            hover_color="gray30",
            command=lambda: self._remove_queue_item(item.id)
        )
        remove_btn.grid(row=0, column=4, padx=5, pady=5)

        # Store widget references
        self.queue_item_widgets[item.id] = {
            'frame': item_frame,
            'status_icon': status_label,
            'status_text': status_text_label
        }

    def _update_queue_item_widget(self, item: QueueItem):
        """Update the widget for a queue item."""
        if item.id in self.queue_item_widgets:
            widgets = self.queue_item_widgets[item.id]
            widgets['status_icon'].configure(
                text=item.get_status_icon(),
                text_color=item.get_status_color()
            )
            widgets['status_text'].configure(
                text=item.status.value.capitalize(),
                text_color=item.get_status_color()
            )

    def _remove_queue_item(self, item_id: str):
        """Remove a specific item from the queue."""
        if self.queue.remove_item(item_id):
            # Remove widget
            if item_id in self.queue_item_widgets:
                self.queue_item_widgets[item_id]['frame'].destroy()
                del self.queue_item_widgets[item_id]

            self._update_queue_stats()
            self._log_console(f"Removed item from queue\n")
        else:
            messagebox.showwarning("Warning", "Cannot remove item that is currently processing")

    def _clear_completed_queue(self):
        """Clear all completed and failed items from the queue."""
        self.queue.clear_completed()

        # Remove widgets
        for item in list(self.queue_item_widgets.keys()):
            if item not in [i.id for i in self.queue.items]:
                self.queue_item_widgets[item]['frame'].destroy()
                del self.queue_item_widgets[item]

        self._update_queue_stats()
        self._log_console("Cleared completed items from queue\n")

    def _clear_all_queue(self):
        """Clear all items from the queue."""
        if len(self.queue) > 0:
            if messagebox.askyesno("Confirm", "Clear all items from queue?"):
                self.queue.clear_queue()

                # Remove all widgets
                for widgets in self.queue_item_widgets.values():
                    widgets['frame'].destroy()
                self.queue_item_widgets.clear()

                self._update_queue_stats()
                self._log_console("Cleared all items from queue\n")

    def _update_queue_stats(self):
        """Update queue statistics display."""
        stats = self.queue.get_statistics()
        total = stats['total']

        if total == 0:
            self.queue_stats_var.set("(0 files)")
        else:
            pending = stats['pending']
            processing = stats['processing']
            completed = stats['completed']
            failed = stats['failed']

            status_parts = []
            if pending > 0:
                status_parts.append(f"{pending} pending")
            if processing > 0:
                status_parts.append(f"{processing} processing")
            if completed > 0:
                status_parts.append(f"{completed} done")
            if failed > 0:
                status_parts.append(f"{failed} failed")

            status_text = ", ".join(status_parts) if status_parts else "all complete"
            self.queue_stats_var.set(f"({total} files: {status_text})")

        # Update convert button text
        self._update_convert_button_text()

    def _update_convert_button_text(self):
        """Update convert button text based on queue status."""
        if len(self.queue) > 0:
            stats = self.queue.get_statistics()
            pending = stats['pending'] + stats['processing']
            if pending > 0:
                self.convert_btn.configure(text=f"Process Queue ({pending})")
            else:
                self.convert_btn.configure(text="Process Queue")
        else:
            self.convert_btn.configure(text="Convert")

    def _start_conversion(self):
        """Start document conversion (single file or batch queue)."""
        # Check if we should process queue or single file
        if len(self.queue) > 0:
            # Queue mode
            self.queue_mode = True
            self._process_queue()
        else:
            # Single file mode
            self.queue_mode = False
            self._process_single_file()

    def _process_single_file(self):
        """Process a single selected file."""
        # Validation
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file to convert.")
            return

        if not os.path.exists(self.selected_file):
            messagebox.showerror("Error", f"Selected file does not exist:\n{self.selected_file}")
            return

        output_dir = self.output_dir_var.get()
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return

        # Create output directory if it doesn't exist
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create output directory:\n{str(e)}")
            return

        # Update UI state
        self.is_processing = True
        self.convert_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.select_btn.configure(state="disabled")
        self.add_files_btn.configure(state="disabled")
        self.add_folder_btn.configure(state="disabled")
        self.progress_bar.start()
        self.status_var.set("Processing...")
        self.ready_label.configure(text="● Processing", text_color="orange")

        self._log_console(f"\n{'='*60}\n")
        self._log_console(f"Starting conversion: {Path(self.selected_file).name}\n")
        self._log_console(f"{'='*60}\n")

        # Get artifacts path for offline mode
        artifacts_path = None
        if self.processing_mode_var.get() == "offline":
            artifacts_path = self.config.get("processing", "artifactsPath")

            # Check if models are downloaded for offline mode
            models_ok, missing_files = self.converter.check_models_downloaded(artifacts_path)
            if not models_ok:
                self._reset_ui()

                error_msg = "Offline Mode: Required models not found!\n\n"
                error_msg += f"Missing files in {artifacts_path}:\n"
                error_msg += "\n".join(f"  • {f}" for f in missing_files)
                error_msg += "\n\nTo use Offline mode:\n"
                error_msg += "1. Click '📥 Download Models' button\n"
                error_msg += "2. Select 'All Standard Models'\n"
                error_msg += "3. Wait for download to complete\n"
                error_msg += "4. Try conversion again\n\n"
                error_msg += "Or switch to Online mode to download models automatically."

                messagebox.showerror("Models Required", error_msg)
                return

        # Check if OCR engine is available (if OCR is enabled)
        if self.ocr_var.get():
            ocr_engine = self.ocr_engine_var.get()
            engine_available, error_msg = self.converter.check_ocr_engine_available(ocr_engine)
            if not engine_available:
                self._reset_ui()
                messagebox.showerror(
                    f"OCR Engine Not Available: {ocr_engine}",
                    error_msg
                )
                return

        # Start conversion
        self.converter.convert(
            input_path=self.selected_file,
            output_format=self.output_format_var.get(),
            output_dir=output_dir,
            processing_mode=self.processing_mode_var.get(),
            ocr_enabled=self.ocr_var.get(),
            force_ocr=self.force_ocr_var.get(),
            pipeline=self.pipeline_var.get(),
            artifacts_path=artifacts_path,
            ocr_lang=self.ocr_lang_var.get() if self.ocr_lang_var.get().strip() else None,
            ocr_engine=self.ocr_engine_var.get(),
            vlm_model=self.vlm_model_var.get() if self.pipeline_var.get() == "vlm" else None,
            extract_tables=self.extract_tables_var.get(),
            enrich_code=self.enrich_code_var.get(),
            enrich_formula=self.enrich_formula_var.get(),
            enrich_picture_classes=self.enrich_picture_classes_var.get(),
            enrich_picture_description=self.enrich_picture_description_var.get(),
            image_export_mode=self.image_export_mode_var.get(),
            show_layout=self.show_layout_var.get(),
            debug_visualize_layout=self.debug_visualize_layout_var.get(),
            debug_visualize_cells=self.debug_visualize_cells_var.get(),
            debug_visualize_ocr=self.debug_visualize_ocr_var.get(),
            debug_visualize_tables=self.debug_visualize_tables_var.get(),
            verbose=self.verbose_var.get(),
            on_output=self._on_conversion_output,
            on_complete=self._on_conversion_complete,
            on_error=self._on_conversion_error
        )

    def _process_queue(self):
        """Process the batch queue."""
        # Get next pending item
        next_item = self.queue.get_next_pending()
        if not next_item:
            # No more pending items
            self._on_queue_complete()
            return

        # Validate output directory
        output_dir = self.output_dir_var.get()
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return

        # Create output directory if it doesn't exist
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create output directory:\n{str(e)}")
            return

        # Update queue item status
        self.queue.update_status(next_item.id, QueueItemStatus.PROCESSING)
        self.current_queue_item = next_item
        self._update_queue_item_widget(next_item)
        self._update_queue_stats()

        # Update UI state
        if not self.is_processing:
            self.is_processing = True
            self.convert_btn.configure(state="disabled")
            self.cancel_btn.configure(state="normal")
            self.select_btn.configure(state="disabled")
            self.add_files_btn.configure(state="disabled")
            self.add_folder_btn.configure(state="disabled")
            self.progress_bar.start()
            self.ready_label.configure(text="● Processing", text_color="orange")

        # Update status
        stats = self.queue.get_statistics()
        current_index = stats['total'] - stats['pending']
        total = stats['total']
        self.status_var.set(f"Processing queue: {current_index}/{total} - {next_item.filename}")

        self._log_console(f"\n{'='*60}\n")
        self._log_console(f"Processing queue item {current_index}/{total}: {next_item.filename}\n")
        self._log_console(f"{'='*60}\n")

        # Get artifacts path for offline mode
        artifacts_path = None
        if self.processing_mode_var.get() == "offline":
            artifacts_path = self.config.get("processing", "artifactsPath")

        # Check if OCR engine is available (if OCR is enabled)
        if self.ocr_var.get():
            ocr_engine = self.ocr_engine_var.get()
            engine_available, error_msg = self.converter.check_ocr_engine_available(ocr_engine)
            if not engine_available:
                # Mark current item as failed
                self.queue.update_status(
                    next_item.id,
                    QueueItemStatus.FAILED,
                    error_message=f"OCR engine '{ocr_engine}' not available"
                )
                self._update_queue_item_widget(next_item.id)

                self._log_console(f"\n[ERROR] OCR Engine '{ocr_engine}' not available\n")
                self._log_console(error_msg + "\n")

                # Continue with next item in queue
                self._process_queue()
                return

        # Start conversion
        self.converter.convert(
            input_path=next_item.file_path,
            output_format=self.output_format_var.get(),
            output_dir=output_dir,
            processing_mode=self.processing_mode_var.get(),
            ocr_enabled=self.ocr_var.get(),
            force_ocr=self.force_ocr_var.get(),
            pipeline=self.pipeline_var.get(),
            artifacts_path=artifacts_path,
            ocr_lang=self.ocr_lang_var.get() if self.ocr_lang_var.get().strip() else None,
            ocr_engine=self.ocr_engine_var.get(),
            vlm_model=self.vlm_model_var.get() if self.pipeline_var.get() == "vlm" else None,
            extract_tables=self.extract_tables_var.get(),
            enrich_code=self.enrich_code_var.get(),
            enrich_formula=self.enrich_formula_var.get(),
            enrich_picture_classes=self.enrich_picture_classes_var.get(),
            enrich_picture_description=self.enrich_picture_description_var.get(),
            image_export_mode=self.image_export_mode_var.get(),
            show_layout=self.show_layout_var.get(),
            debug_visualize_layout=self.debug_visualize_layout_var.get(),
            debug_visualize_cells=self.debug_visualize_cells_var.get(),
            debug_visualize_ocr=self.debug_visualize_ocr_var.get(),
            debug_visualize_tables=self.debug_visualize_tables_var.get(),
            verbose=self.verbose_var.get(),
            on_output=self._on_conversion_output,
            on_complete=self._on_queue_item_complete,
            on_error=self._on_queue_item_error
        )

    def _cancel_conversion(self):
        """Cancel current conversion."""
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel the conversion?"):
            self.converter.cancel()
            self._log_console("\n[CANCELLED] Conversion cancelled by user.\n")
            self._reset_ui()

    def _download_models(self):
        """Download models for offline operation."""
        if self.converter.is_running:
            messagebox.showwarning("Busy", "Please wait for the current operation to complete.")
            return

        # Ask user which models to download
        dialog = ctk.CTkToplevel(self)
        dialog.title("Download Models")
        dialog.geometry("500x300")
        dialog.transient(self)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(
            dialog,
            text="Select Models to Download",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            dialog,
            text="This will download models for offline operation.\nProgress will be shown in the console.",
            font=ctk.CTkFont(size=11)
        ).pack(pady=10)

        download_all_var = ctk.BooleanVar(value=True)
        download_smoldocling_var = ctk.BooleanVar(value=False)
        download_smolvlm_var = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(
            dialog,
            text="All Standard Models (docling-tools models download)",
            variable=download_all_var,
            font=ctk.CTkFont(size=12)
        ).pack(pady=5, padx=20, anchor="w")

        ctk.CTkCheckBox(
            dialog,
            text="SmolDocling-256M (VLM model for complex layouts)",
            variable=download_smoldocling_var,
            font=ctk.CTkFont(size=12)
        ).pack(pady=5, padx=20, anchor="w")

        ctk.CTkCheckBox(
            dialog,
            text="SmolVLM-256M-Instruct (Vision-Language Model)",
            variable=download_smolvlm_var,
            font=ctk.CTkFont(size=12)
        ).pack(pady=5, padx=20, anchor="w")

        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)

        def start_download():
            if not download_all_var.get() and not download_smoldocling_var.get() and not download_smolvlm_var.get():
                messagebox.showwarning("No Selection", "Please select at least one model to download.")
                return

            dialog.destroy()
            self._log_console("\n" + "="*60 + "\n")
            self._log_console("Starting model download...\n")
            self._log_console("="*60 + "\n")

            # Disable UI elements
            self.convert_btn.configure(state="disabled")
            self.select_btn.configure(state="disabled")
            self.progress_bar.start()
            self.status_var.set("Downloading models...")
            self.ready_label.configure(text="● Downloading", text_color="orange")

            self.converter.download_models(
                download_all=download_all_var.get(),
                download_smoldocling=download_smoldocling_var.get(),
                download_smolvlm=download_smolvlm_var.get(),
                on_output=self._on_conversion_output,
                on_complete=self._on_download_complete,
                on_error=lambda err: messagebox.showerror("Download Error", err)
            )

        ctk.CTkButton(
            button_frame,
            text="Download",
            command=start_download,
            width=100
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=100,
            fg_color="gray40",
            hover_color="gray30"
        ).pack(side="left", padx=5)

    def _on_download_complete(self, return_code):
        """Handle model download completion."""
        def update_ui():
            self.progress_bar.stop()
            self.progress_bar.set(0)
            self.convert_btn.configure(state="normal")
            self.select_btn.configure(state="normal")

            if return_code == 0:
                self.status_var.set("Model download completed successfully!")
                self.ready_label.configure(text="● Ready", text_color="green")
                messagebox.showinfo("Success", "Models downloaded successfully!")
            else:
                self.status_var.set("Model download completed with warnings")
                self.ready_label.configure(text="● Ready", text_color="green")
                messagebox.showinfo("Completed", "Model download finished. Check console for details.")

        self.after(0, update_ui)

    def _on_conversion_output(self, text: str):
        """Handle conversion output."""
        self.after(0, lambda: self._log_console(text))

    def _on_conversion_complete(self, return_code: int):
        """Handle conversion completion."""
        def update_ui():
            if return_code == 0:
                self.status_var.set("Conversion completed successfully!")
                self.ready_label.configure(text="● Complete", text_color="green")
                self._log_console(f"\n{'='*60}\n")
                self._log_console("[SUCCESS] Conversion completed successfully!\n")
                self._log_console(f"Output directory: {self.output_dir_var.get()}\n")
                self._log_console(f"{'='*60}\n")
                messagebox.showinfo("Success", "Document converted successfully!")
            else:
                self.status_var.set(f"Conversion failed (exit code: {return_code})")
                self.ready_label.configure(text="● Error", text_color="red")
                self._log_console(f"\n[ERROR] Conversion failed with exit code {return_code}\n")
                messagebox.showerror("Error", f"Conversion failed. Check console for details.")

            self._reset_ui()

        self.after(0, update_ui)

    def _on_conversion_error(self, error: str):
        """Handle conversion error."""
        def update_ui():
            self.status_var.set("Error occurred")
            self.ready_label.configure(text="● Error", text_color="red")
            self._log_console(f"\n[ERROR] {error}\n")
            messagebox.showerror("Error", error)
            self._reset_ui()

        self.after(0, update_ui)

    def _on_queue_item_complete(self, return_code: int):
        """Handle completion of a queue item."""
        def update_ui():
            if self.current_queue_item:
                if return_code == 0:
                    # Success
                    self.queue.update_status(self.current_queue_item.id, QueueItemStatus.COMPLETED)
                    self._log_console(f"\n[SUCCESS] Completed: {self.current_queue_item.filename}\n")
                else:
                    # Failed
                    self.queue.update_status(self.current_queue_item.id, QueueItemStatus.FAILED,
                                            f"Exit code: {return_code}")
                    self._log_console(f"\n[FAILED] {self.current_queue_item.filename} (exit code: {return_code})\n")

                # Update widget
                self._update_queue_item_widget(self.current_queue_item)
                self._update_queue_stats()

            # Process next item in queue
            self._process_queue()

        self.after(0, update_ui)

    def _on_queue_item_error(self, error: str):
        """Handle error for a queue item."""
        def update_ui():
            if self.current_queue_item:
                self.queue.update_status(self.current_queue_item.id, QueueItemStatus.FAILED, error)
                self._log_console(f"\n[ERROR] {self.current_queue_item.filename}: {error}\n")
                self._update_queue_item_widget(self.current_queue_item)
                self._update_queue_stats()

            # Process next item in queue
            self._process_queue()

        self.after(0, update_ui)

    def _on_queue_complete(self):
        """Handle completion of the entire queue."""
        stats = self.queue.get_statistics()

        self.status_var.set("Queue processing complete!")
        self.ready_label.configure(text="● Complete", text_color="green")

        self._log_console(f"\n{'='*60}\n")
        self._log_console("[QUEUE COMPLETE]\n")
        self._log_console(f"Total files processed: {stats['total']}\n")
        self._log_console(f"Completed successfully: {stats['completed']}\n")
        self._log_console(f"Failed: {stats['failed']}\n")
        self._log_console(f"Output directory: {self.output_dir_var.get()}\n")
        self._log_console(f"{'='*60}\n")

        # Show completion dialog
        if stats['failed'] > 0:
            messagebox.showinfo("Queue Complete",
                              f"Queue processing complete!\n\n"
                              f"Successful: {stats['completed']}\n"
                              f"Failed: {stats['failed']}\n\n"
                              f"Check console for details.")
        else:
            messagebox.showinfo("Success",
                              f"All {stats['completed']} files converted successfully!")

        self._reset_ui()

    def _reset_ui(self):
        """Reset UI to ready state."""
        self.is_processing = False
        self.convert_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.select_btn.configure(state="normal")
        self.add_files_btn.configure(state="normal")
        self.add_folder_btn.configure(state="normal")
        self.progress_bar.stop()
        self.progress_bar.set(0)

        if self.status_var.get() not in ["Conversion completed successfully!", "Error occurred", "Conversion failed", "Queue processing complete!"]:
            self.status_var.set("Ready")
            self.ready_label.configure(text="● Ready", text_color="green")

    def _create_log_file(self):
        """Create a new log file with timestamp."""
        if self.log_file_handle:
            self._close_log_file()

        log_dir = Path(self.config.get("general", "logDirectory",
                                       default=str(Path.home() / "Documents" / "docling_logs")))
        log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"docling_log_{timestamp}.txt"
        self.current_log_file = log_dir / log_filename

        try:
            self.log_file_handle = open(self.current_log_file, 'w', encoding='utf-8')
            header = f"Docling GUI Log File\n"
            header += f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            header += f"="*60 + "\n\n"
            self.log_file_handle.write(header)
            self.log_file_handle.flush()
            return True
        except Exception as e:
            messagebox.showerror("Log File Error", f"Failed to create log file: {str(e)}")
            self.enable_log_var.set(False)
            self.current_log_file = None
            return False

    def _close_log_file(self):
        """Close the current log file."""
        if self.log_file_handle:
            try:
                footer = f"\n{'='*60}\n"
                footer += f"Log ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                self.log_file_handle.write(footer)
                self.log_file_handle.close()
            except:
                pass
            finally:
                self.log_file_handle = None
                self.current_log_file = None

    def _on_log_enable_change(self):
        """Handle log enable checkbox change."""
        enabled = self.enable_log_var.get()
        self.config.set("general", "enableLogging", value=enabled)

        if enabled:
            if self._create_log_file():
                self._log_console(f"✓ Logging enabled. Saving to: {self.current_log_file}\n")
        else:
            if self.current_log_file:
                log_path = str(self.current_log_file)
                self._close_log_file()
                self._log_console(f"✓ Logging disabled. Log saved to: {log_path}\n")

    def _log_console(self, text: str):
        """Add text to console output and optionally to log file."""
        self.console_text.insert("end", text)
        self.console_text.see("end")

        # Write to log file if logging is enabled
        if self.enable_log_var.get() and self.log_file_handle:
            try:
                self.log_file_handle.write(text)
                self.log_file_handle.flush()
            except Exception as e:
                # Disable logging on error
                self.enable_log_var.set(False)
                self.config.set("general", "enableLogging", value=False)
                self._close_log_file()
                self.console_text.insert("end", f"\n[ERROR] Log file write failed: {str(e)}\n")

    def _clear_console(self):
        """Clear console output."""
        self.console_text.delete("1.0", "end")
        self._log_console("Console cleared.\n")

    def _on_closing(self):
        """Handle window closing."""
        if self.is_processing:
            if not messagebox.askyesno("Quit", "Conversion in progress. Are you sure you want to quit?"):
                return

        # Close log file if open
        self._close_log_file()

        # Save window size
        geometry = self.geometry().split('+')[0]  # Get WxH
        width, height = geometry.split('x')
        self.config.set("window", "width", value=int(width))
        self.config.set("window", "height", value=int(height))

        self.destroy()
