"""Sidebar component with all conversion options."""

import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Optional, Dict, Any
from config import Config
from ui.widgets import CollapsibleSection


class Sidebar(ctk.CTkFrame):
    """
    Left sidebar containing all conversion options and controls.

    Organized into collapsible sections:
    - Output Configuration
    - Processing Options
    - Debug & Visualization
    """

    def __init__(
        self,
        parent,
        config: Config,
        on_add_files: Optional[Callable[[], None]] = None,
        on_add_folder: Optional[Callable[[], None]] = None,
        on_convert: Optional[Callable[[], None]] = None,
        on_cancel: Optional[Callable[[], None]] = None,
        on_download_models: Optional[Callable[[], None]] = None
    ):
        """
        Initialize Sidebar.

        Args:
            parent: Parent widget
            config: Application configuration
            on_add_files: Callback for Add Files button
            on_add_folder: Callback for Add Folder button
            on_convert: Callback for Convert button
            on_cancel: Callback for Cancel button
            on_download_models: Callback for Download Models button
        """
        super().__init__(parent, fg_color="gray17", corner_radius=0)

        self.config = config
        self._on_add_files = on_add_files
        self._on_add_folder = on_add_folder
        self._on_convert = on_convert
        self._on_cancel = on_cancel
        self._on_download_models = on_download_models

        # State variables (BooleanVar, StringVar, etc.)
        self._create_variables()

        # Create UI
        self._create_widgets()

    def _create_variables(self):
        """Initialize state variables."""
        # Output
        self.output_format_var = ctk.StringVar(
            value=self.config.get("general", "defaultOutputFormat", default="md")
        )
        self.output_dir_var = ctk.StringVar(
            value=self.config.get("general", "defaultOutputDir",
                                  default=str(__import__('pathlib').Path.home() / "Documents" / "docling_output"))
        )

        # Processing Mode
        self.processing_mode_var = ctk.StringVar(
            value=self.config.get("processing", "mode", default="online")
        )

        # Pipeline
        self.pipeline_var = ctk.StringVar(
            value=self.config.get("defaults", "pipeline", default="standard")
        )

        # OCR
        self.ocr_var = ctk.BooleanVar(
            value=self.config.get("defaults", "ocrEnabled", default=True)
        )
        self.force_ocr_var = ctk.BooleanVar(
            value=self.config.get("defaults", "forceOcr", default=False)
        )
        self.ocr_lang_var = ctk.StringVar(
            value=self.config.get("defaults", "ocrLanguages", default="eng")
        )
        self.ocr_engine_var = ctk.StringVar(
            value=self.config.get("defaults", "ocrEngine", default="auto")
        )

        # VLM
        self.vlm_model_var = ctk.StringVar(
            value=self.config.get("defaults", "vlmModel", default="smoldocling")
        )

        # Image Export
        self.image_export_mode_var = ctk.StringVar(
            value=self.config.get("defaults", "imageExportMode", default="embedded")
        )

        # PDF Options
        self.pdf_backend_var = ctk.StringVar(
            value=self.config.get("defaults", "pdfBackend", default="dlparse_v4")
        )
        self.pdf_password_var = ctk.StringVar(
            value=self.config.get("defaults", "pdfPassword", default="")
        )
        self.table_mode_var = ctk.StringVar(
            value=self.config.get("defaults", "tableMode", default="accurate")
        )

        # Verbose
        self.verbose_var = ctk.IntVar(
            value=self.config.get("defaults", "verbose", default=0)
        )

        # Enrichment
        self.enrich_formula_var = ctk.BooleanVar(
            value=self.config.get("defaults", "enrichFormula", default=False)
        )
        self.enrich_picture_classes_var = ctk.BooleanVar(
            value=self.config.get("defaults", "enrichPictureClasses", default=False)
        )
        self.enrich_picture_description_var = ctk.BooleanVar(
            value=self.config.get("defaults", "enrichPictureDescription", default=False)
        )
        self.extract_tables_var = ctk.BooleanVar(
            value=self.config.get("defaults", "extractTables", default=True)
        )
        self.enrich_code_var = ctk.BooleanVar(
            value=self.config.get("defaults", "enrichCode", default=False)
        )

        # Debug visualization
        self.show_layout_var = ctk.BooleanVar(
            value=self.config.get("defaults", "showLayout", default=False)
        )
        self.debug_visualize_layout_var = ctk.BooleanVar(
            value=self.config.get("defaults", "debugVisualizeLayout", default=False)
        )
        self.debug_visualize_cells_var = ctk.BooleanVar(
            value=self.config.get("defaults", "debugVisualizeCells", default=False)
        )
        self.debug_visualize_ocr_var = ctk.BooleanVar(
            value=self.config.get("defaults", "debugVisualizeOcr", default=False)
        )
        self.debug_visualize_tables_var = ctk.BooleanVar(
            value=self.config.get("defaults", "debugVisualizeTables", default=False)
        )

    def _create_widgets(self):
        """Create sidebar widgets."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Scrollable area expands

        # Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="ew")

        version = self.config.get("version", default="1.5.5")
        ctk.CTkLabel(
            title_frame,
            text=f"Docling Converter {version}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")

        # File buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        self._add_files_btn = ctk.CTkButton(
            btn_frame,
            text="+ Add Files",
            command=self._on_add_files_click,
            height=32,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self._add_files_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self._add_folder_btn = ctk.CTkButton(
            btn_frame,
            text="Folder",
            command=self._on_add_folder_click,
            height=32,
            fg_color="gray40",
            hover_color="gray30"
        )
        self._add_folder_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # Scrollable options area
        options_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color="gray30",
            scrollbar_button_hover_color="gray40"
        )
        options_scroll.grid(row=2, column=0, padx=5, pady=0, sticky="nsew")
        options_scroll.grid_columnconfigure(0, weight=1)

        # Output Configuration Section
        self._create_output_section(options_scroll)

        # Processing Options Section
        self._create_processing_section(options_scroll)

        # Debug & Visualization Section
        self._create_debug_section(options_scroll)

        # Control buttons at bottom
        self._create_control_buttons()

    def _create_output_section(self, parent):
        """Create output configuration section."""
        output_section = CollapsibleSection(
            parent,
            title="Output Configuration",
            is_expanded=False
        )
        output_section.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        content = output_section.content

        # Format dropdown
        format_frame = ctk.CTkFrame(content, fg_color="transparent")
        format_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            format_frame,
            text="Format:",
            font=ctk.CTkFont(size=12),
            width=100,
            anchor="w"
        ).pack(side="left")

        ctk.CTkOptionMenu(
            format_frame,
            variable=self.output_format_var,
            values=["md", "json", "html", "html_split_page", "text", "doctags"],
            width=150
        ).pack(side="left", fill="x", expand=True)

        # Output directory
        dir_frame = ctk.CTkFrame(content, fg_color="transparent")
        dir_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            dir_frame,
            text="Output Directory:",
            font=ctk.CTkFont(size=12),
            anchor="w"
        ).pack(anchor="w")

        entry_frame = ctk.CTkFrame(dir_frame, fg_color="transparent")
        entry_frame.pack(fill="x", pady=(5, 0))

        self._output_dir_entry = ctk.CTkEntry(
            entry_frame,
            textvariable=self.output_dir_var,
            height=28
        )
        self._output_dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkButton(
            entry_frame,
            text="...",
            command=self._on_browse_output,
            width=40,
            height=28
        ).pack(side="left")

    def _create_processing_section(self, parent):
        """Create processing options section."""
        proc_section = CollapsibleSection(
            parent,
            title="Processing Options",
            is_expanded=True
        )
        proc_section.grid(row=1, column=0, sticky="ew", pady=5)

        content = proc_section.content

        # Mode dropdown
        mode_frame = ctk.CTkFrame(content, fg_color="transparent")
        mode_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            mode_frame,
            text="Mode:",
            font=ctk.CTkFont(size=12),
            width=80,
            anchor="w"
        ).pack(side="left")

        ctk.CTkOptionMenu(
            mode_frame,
            variable=self.processing_mode_var,
            values=["online", "offline"],
            width=150,
            command=lambda v: self.processing_mode_var.set(v)
        ).pack(side="left")

        # Pipeline dropdown
        self.pipeline_frame = ctk.CTkFrame(content, fg_color="transparent")
        self.pipeline_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            self.pipeline_frame,
            text="Pipeline:",
            font=ctk.CTkFont(size=12),
            width=80,
            anchor="w"
        ).pack(side="left")

        ctk.CTkOptionMenu(
            self.pipeline_frame,
            variable=self.pipeline_var,
            values=self.config.get("models", "pipelines", default=["standard", "vlm", "asr"]),
            width=150,
            command=self._on_pipeline_change
        ).pack(side="left")

        # VLM Model dropdown
        self.vlm_model_frame = ctk.CTkFrame(content, fg_color="transparent")

        ctk.CTkLabel(
            self.vlm_model_frame,
            text="VLM Model:",
            font=ctk.CTkFont(size=12),
            width=80,
            anchor="w"
        ).pack(side="left")

        self.vlm_model_menu = ctk.CTkOptionMenu(
            self.vlm_model_frame,
            variable=self.vlm_model_var,
            values=self.config.get("models", "vlm_models", default=["smoldocling"]),
            width=150
        )
        self.vlm_model_menu.pack(side="left")

        # Set initial visibility
        self._on_pipeline_change(self.pipeline_var.get())

        # OCR Settings subsection
        ocr_label = ctk.CTkLabel(
            content,
            text="OCR Settings",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        ocr_label.pack(anchor="w", pady=(10, 5))

        # OCR checkboxes
        ocr_check_frame = ctk.CTkFrame(content, fg_color="transparent")
        ocr_check_frame.pack(fill="x")

        ctk.CTkCheckBox(
            ocr_check_frame,
            text="Enable OCR",
            variable=self.ocr_var,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(0, 15))

        ctk.CTkCheckBox(
            ocr_check_frame,
            text="Force OCR",
            variable=self.force_ocr_var,
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        # OCR Engine dropdown
        engine_frame = ctk.CTkFrame(content, fg_color="transparent")
        engine_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            engine_frame,
            text="OCR Engine:",
            font=ctk.CTkFont(size=11),
            width=80,
            anchor="w"
        ).pack(side="left")

        ctk.CTkOptionMenu(
            engine_frame,
            variable=self.ocr_engine_var,
            values=self.config.get("models", "ocr_engines", default=["auto", "easyocr", "tesseract", "tesserocr", "rapidocr", "ocrmac"]),
            width=140
        ).pack(side="left")

        # OCR Language dropdown
        lang_frame = ctk.CTkFrame(content, fg_color="transparent")
        lang_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            lang_frame,
            text="Language:",
            font=ctk.CTkFont(size=11),
            width=80,
            anchor="w"
        ).pack(side="left")

        # Language options with display names
        self._ocr_lang_options = self.config.get("models", "ocr_languages", default={
            "English": "eng",
            "German": "deu",
            "French": "fra",
            "Spanish": "spa",
            "Italian": "ita",
            "Portuguese": "por",
            "Dutch": "nld",
            "Polish": "pol",
            "Russian": "rus",
            "Chinese (Simplified)": "chi_sim",
            "Chinese (Traditional)": "chi_tra",
            "Japanese": "jpn",
            "Korean": "kor",
            "Arabic": "ara",
            "Hindi": "hin",
            "Turkish": "tur",
            "Vietnamese": "vie",
            "Thai": "tha"
        })

        # Get current language code and find display name
        current_code = self.ocr_lang_var.get()
        current_display = "English"  # Default
        for display, code in self._ocr_lang_options.items():
            if code == current_code:
                current_display = display
                break

        self._ocr_lang_display_var = ctk.StringVar(value=current_display)

        ctk.CTkOptionMenu(
            lang_frame,
            variable=self._ocr_lang_display_var,
            values=list(self._ocr_lang_options.keys()),
            width=140,
            command=self._on_ocr_lang_change
        ).pack(side="left")

        # PDF & Export Options subsection
        pdf_label = ctk.CTkLabel(
            content,
            text="PDF & Export Options",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        pdf_label.pack(anchor="w", pady=(10, 5))

        # PDF Backend dropdown
        backend_frame = ctk.CTkFrame(content, fg_color="transparent")
        backend_frame.pack(fill="x", pady=3)

        ctk.CTkLabel(
            backend_frame,
            text="PDF Backend:",
            font=ctk.CTkFont(size=11),
            width=100,
            anchor="w"
        ).pack(side="left")

        ctk.CTkOptionMenu(
            backend_frame,
            variable=self.pdf_backend_var,
            values=["dlparse_v4", "dlparse_v2", "dlparse_v1", "pypdfium2"],
            width=120
        ).pack(side="left")

        # Table Mode dropdown
        table_frame = ctk.CTkFrame(content, fg_color="transparent")
        table_frame.pack(fill="x", pady=3)

        ctk.CTkLabel(
            table_frame,
            text="Table Mode:",
            font=ctk.CTkFont(size=11),
            width=100,
            anchor="w"
        ).pack(side="left")

        ctk.CTkOptionMenu(
            table_frame,
            variable=self.table_mode_var,
            values=["accurate", "fast"],
            width=120
        ).pack(side="left")

        # Image Export Mode dropdown
        export_frame = ctk.CTkFrame(content, fg_color="transparent")
        export_frame.pack(fill="x", pady=3)

        ctk.CTkLabel(
            export_frame,
            text="Image Export:",
            font=ctk.CTkFont(size=11),
            width=100,
            anchor="w"
        ).pack(side="left")

        ctk.CTkOptionMenu(
            export_frame,
            variable=self.image_export_mode_var,
            values=["embedded", "placeholder", "referenced"],
            width=120
        ).pack(side="left")

        # PDF Password field
        password_frame = ctk.CTkFrame(content, fg_color="transparent")
        password_frame.pack(fill="x", pady=3)

        ctk.CTkLabel(
            password_frame,
            text="PDF Password:",
            font=ctk.CTkFont(size=11),
            width=100,
            anchor="w"
        ).pack(side="left")

        self._pdf_password_entry = ctk.CTkEntry(
            password_frame,
            textvariable=self.pdf_password_var,
            placeholder_text="(optional)",
            show="*",
            height=26,
            width=120
        )
        self._pdf_password_entry.pack(side="left")

        # Enrichment subsection
        enrich_label = ctk.CTkLabel(
            content,
            text="Enrichment",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        enrich_label.pack(anchor="w", pady=(10, 5))

        # Enrichment checkboxes - Row 1
        enrich_row1 = ctk.CTkFrame(content, fg_color="transparent")
        enrich_row1.pack(fill="x")

        ctk.CTkCheckBox(
            enrich_row1,
            text="Formulas",
            variable=self.enrich_formula_var,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkCheckBox(
            enrich_row1,
            text="Picture Classes",
            variable=self.enrich_picture_classes_var,
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        # Enrichment checkboxes - Row 2
        enrich_row2 = ctk.CTkFrame(content, fg_color="transparent")
        enrich_row2.pack(fill="x", pady=(3, 0))

        ctk.CTkCheckBox(
            enrich_row2,
            text="Picture Descriptions",
            variable=self.enrich_picture_description_var,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkCheckBox(
            enrich_row2,
            text="Extract Tables",
            variable=self.extract_tables_var,
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        # Enrichment checkboxes - Row 3
        enrich_row3 = ctk.CTkFrame(content, fg_color="transparent")
        enrich_row3.pack(fill="x", pady=(3, 0))

        ctk.CTkCheckBox(
            enrich_row3,
            text="Enrich Code",
            variable=self.enrich_code_var,
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        # Download Models button
        ctk.CTkButton(
            content,
            text="Download Models",
            command=self._on_download_models_click,
            height=30,
            fg_color="gray35",
            hover_color="gray30"
        ).pack(fill="x", pady=(15, 5))

    def _create_debug_section(self, parent):
        """Create debug & visualization section."""
        debug_section = CollapsibleSection(
            parent,
            title="Debug & Visualization",
            is_expanded=False
        )
        debug_section.grid(row=2, column=0, sticky="ew", pady=5)

        content = debug_section.content

        # Debug checkboxes
        ctk.CTkCheckBox(
            content,
            text="Show Layout Boxes",
            variable=self.show_layout_var,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", pady=2)

        ctk.CTkCheckBox(
            content,
            text="Visualize Layout Clusters",
            variable=self.debug_visualize_layout_var,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", pady=2)

        ctk.CTkCheckBox(
            content,
            text="Visualize PDF Cells",
            variable=self.debug_visualize_cells_var,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", pady=2)

        ctk.CTkCheckBox(
            content,
            text="Visualize OCR Cells",
            variable=self.debug_visualize_ocr_var,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", pady=2)

        ctk.CTkCheckBox(
            content,
            text="Visualize Table Cells",
            variable=self.debug_visualize_tables_var,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", pady=2)

        # Reset Settings button
        ctk.CTkButton(
            content,
            text="🗑 Reset All Settings",
            command=self._reset_settings,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="#8b0000",
            hover_color="#a52a2a"
        ).pack(fill="x", pady=(15, 5))

    def _reset_settings(self):
        """Reset all settings by deleting config.json."""
        if messagebox.askyesno(
            "Reset Settings",
            "This will delete all your settings and restore defaults.\n\n"
            "The application will close and you'll need to restart it.\n\n"
            "Are you sure you want to continue?"
        ):
            try:
                config_file = self.config.config_file
                if config_file.exists():
                    config_file.unlink()
                messagebox.showinfo(
                    "Settings Reset",
                    "Settings have been reset.\n\nPlease restart the application."
                )
                # Close the application
                self.winfo_toplevel().destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not reset settings:\n{str(e)}")

    def _create_control_buttons(self):
        """Create convert/cancel buttons."""
        control_frame = ctk.CTkFrame(self, fg_color="gray20")
        control_frame.grid(row=3, column=0, padx=0, pady=0, sticky="sew")
        control_frame.grid_columnconfigure(0, weight=1)

        # Convert button
        self._convert_btn = ctk.CTkButton(
            control_frame,
            text="CONVERT",
            command=self._on_convert_click,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2d7d46",
            hover_color="#236b38"
        )
        self._convert_btn.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")

        # Cancel button
        self._cancel_btn = ctk.CTkButton(
            control_frame,
            text="Cancel",
            command=self._on_cancel_click,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="gray30",
            text_color="gray60",
            state="disabled"
        )
        self._cancel_btn.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")

    # Event handlers

    def _on_add_files_click(self):
        """Handle add files button click."""
        if self._on_add_files:
            self._on_add_files()

    def _on_add_folder_click(self):
        """Handle add folder button click."""
        if self._on_add_folder:
            self._on_add_folder()

    def _on_convert_click(self):
        """Handle convert button click."""
        if self._on_convert:
            self._on_convert()

    def _on_cancel_click(self):
        """Handle cancel button click."""
        if self._on_cancel:
            self._on_cancel()

    def _on_download_models_click(self):
        """Handle download models button click."""
        if self._on_download_models:
            self._on_download_models()

    def _on_browse_output(self):
        """Handle output directory browse."""
        from tkinter import filedialog
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir_var.get()
        )
        if directory:
            self.output_dir_var.set(directory)
            self.config.set("general", "defaultOutputDir", value=directory)

    def _on_pipeline_change(self, pipeline: str):
        """Handle pipeline dropdown change."""
        if pipeline == "vlm":
            self.vlm_model_frame.pack(fill="x", pady=5, after=self.pipeline_frame)
        else:
            self.vlm_model_frame.pack_forget()


    def _on_ocr_lang_change(self, display_name: str):
        """Handle OCR language dropdown change."""
        if display_name in self._ocr_lang_options:
            lang_code = self._ocr_lang_options[display_name]
            self.ocr_lang_var.set(lang_code)
            self.config.set("defaults", "ocrLanguages", value=lang_code)

    # Public methods

    def set_processing_state(self, is_processing: bool):
        """
        Update UI for processing state.

        Args:
            is_processing: True if conversion is in progress
        """
        if is_processing:
            self._convert_btn.configure(state="disabled")
            self._cancel_btn.configure(state="normal", text_color="white")
            self._add_files_btn.configure(state="disabled")
            self._add_folder_btn.configure(state="disabled")
        else:
            self._convert_btn.configure(state="normal")
            self._cancel_btn.configure(state="disabled", text_color="gray60")
            self._add_files_btn.configure(state="normal")
            self._add_folder_btn.configure(state="normal")

    def update_convert_button(self, text: str):
        """Update convert button text."""
        self._convert_btn.configure(text=text)

    def get_conversion_params(self) -> Dict[str, Any]:
        """
        Get all conversion parameters from sidebar controls.

        Returns:
            Dictionary of conversion parameters
        """
        return {
            'output_format': self.output_format_var.get(),
            'output_dir': self.output_dir_var.get(),
            'processing_mode': self.processing_mode_var.get(),
            'pipeline': self.pipeline_var.get(),
            'ocr_enabled': self.ocr_var.get(),
            'force_ocr': self.force_ocr_var.get(),
            'ocr_lang': self.ocr_lang_var.get() if self.ocr_lang_var.get().strip() else None,
            'ocr_engine': self.ocr_engine_var.get(),
            'vlm_model': self.vlm_model_var.get() if self.pipeline_var.get() == "vlm" else None,
            'image_export_mode': self.image_export_mode_var.get(),
            'pdf_backend': self.pdf_backend_var.get(),
            'pdf_password': self.pdf_password_var.get() if self.pdf_password_var.get().strip() else None,
            'table_mode': self.table_mode_var.get(),
            'verbose': self.verbose_var.get(),
            'enrich_formula': self.enrich_formula_var.get(),
            'enrich_picture_classes': self.enrich_picture_classes_var.get(),
            'enrich_picture_description': self.enrich_picture_description_var.get(),
            'extract_tables': self.extract_tables_var.get(),
            'enrich_code': self.enrich_code_var.get(),
            'show_layout': self.show_layout_var.get(),
            'debug_visualize_layout': self.debug_visualize_layout_var.get(),
            'debug_visualize_cells': self.debug_visualize_cells_var.get(),
            'debug_visualize_ocr': self.debug_visualize_ocr_var.get(),
            'debug_visualize_tables': self.debug_visualize_tables_var.get(),
        }
