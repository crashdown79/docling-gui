import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import os
import platform
from typing import Optional

from core.converter import DoclingConverter
from config import Config


class MainWindow(ctk.CTk):
    """Main application window for Docling GUI."""

    def __init__(self):
        super().__init__()

        # Initialize components
        self.config = Config()
        self.converter = DoclingConverter()

        # Window setup
        self.title("Docling GUI - Document Converter")
        width = self.config.get("window", "width", default=900)
        height = self.config.get("window", "height", default=750)
        self.geometry(f"{width}x{height}")

        # Set theme
        theme = self.config.get("interface", "theme", default="dark")
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")

        # State variables
        self.selected_file: Optional[str] = None
        self.is_processing = False

        # Create UI
        self._create_widgets()
        self._check_docling()

        # Window close handler
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_widgets(self):
        """Create all UI widgets."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)  # Console row expands

        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Docling Document Converter",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Input Section
        self._create_input_section()

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
            text="Input File:",
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

        # Select file button
        self.select_btn = ctk.CTkButton(
            input_frame,
            text="Select File",
            command=self._select_file,
            width=120
        )
        self.select_btn.grid(row=0, column=2, padx=10, pady=10)

        # Drag and drop frame
        self.drop_frame = ctk.CTkFrame(input_frame, height=100, fg_color="gray25")
        self.drop_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")

        drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="📄 Drag & drop files here (coming soon) or use 'Select File' button",
            font=ctk.CTkFont(size=12)
        )
        drop_label.place(relx=0.5, rely=0.5, anchor="center")

    def _create_output_section(self):
        """Create output configuration section."""
        output_frame = ctk.CTkFrame(self)
        output_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
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
        options_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
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
        control_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
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
        progress_frame.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")
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

        # Label
        ctk.CTkLabel(
            console_frame,
            text="Console Output",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

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
        status_frame.grid(row=7, column=0, sticky="ew")
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
            text="Docling GUI v1.2.1",
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

    def _start_conversion(self):
        """Start document conversion."""
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
            enrich_formula=self.enrich_formula_var.get(),
            enrich_picture_classes=self.enrich_picture_classes_var.get(),
            enrich_picture_description=self.enrich_picture_description_var.get(),
            image_export_mode=self.image_export_mode_var.get(),
            verbose=self.verbose_var.get(),
            on_output=self._on_conversion_output,
            on_complete=self._on_conversion_complete,
            on_error=self._on_conversion_error
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

    def _reset_ui(self):
        """Reset UI to ready state."""
        self.is_processing = False
        self.convert_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.select_btn.configure(state="normal")
        self.progress_bar.stop()
        self.progress_bar.set(0)

        if self.status_var.get() not in ["Conversion completed successfully!", "Error occurred", "Conversion failed"]:
            self.status_var.set("Ready")
            self.ready_label.configure(text="● Ready", text_color="green")

    def _log_console(self, text: str):
        """Add text to console output."""
        self.console_text.insert("end", text)
        self.console_text.see("end")

    def _clear_console(self):
        """Clear console output."""
        self.console_text.delete("1.0", "end")
        self._log_console("Console cleared.\n")

    def _on_closing(self):
        """Handle window closing."""
        if self.is_processing:
            if not messagebox.askyesno("Quit", "Conversion in progress. Are you sure you want to quit?"):
                return

        # Save window size
        geometry = self.geometry().split('+')[0]  # Get WxH
        width, height = geometry.split('x')
        self.config.set("window", "width", value=int(width))
        self.config.set("window", "height", value=int(height))

        self.destroy()
