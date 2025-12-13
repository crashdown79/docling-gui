"""Main application window for Docling GUI v1.5.2."""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import os
import platform
from typing import Optional, List

from core.converter import DoclingConverter
from core.queue import ConversionQueue, QueueItem, QueueItemStatus
from config import Config
from ui.sidebar import Sidebar
from ui.queue_panel import QueuePanel
from ui.console_panel import ConsolePanel


class MainWindow(ctk.CTk):
    """
    Main application window for Docling GUI.

    Features a two-panel layout:
    - Left: Sidebar with all conversion options
    - Right: Queue panel (top) and Console panel (bottom)
    """

    VERSION = "1.5.2"

    def __init__(self):
        super().__init__()

        # Initialize components
        self.config = Config()
        self.converter = DoclingConverter()
        self.queue = ConversionQueue()

        # Window setup
        self.title(f"Docling GUI v{self.VERSION} - Document Converter")
        width = self.config.get("window", "width", default=1200)
        height = self.config.get("window", "height", default=900)
        self.geometry(f"{width}x{height}")
        self.minsize(1000, 700)

        # Set theme
        theme = self.config.get("interface", "theme", default="dark")
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")

        # State variables
        self.is_processing = False
        self.current_queue_item: Optional[QueueItem] = None

        # Create UI
        self._create_widgets()
        self._check_docling()

        # Window close handler
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_widgets(self):
        """Create the two-panel layout."""
        # Configure grid: 2 columns
        self.grid_columnconfigure(0, weight=0, minsize=320)  # Sidebar fixed
        self.grid_columnconfigure(1, weight=1)               # Main area expands
        self.grid_rowconfigure(0, weight=1)

        # Left: Sidebar
        self.sidebar = Sidebar(
            self,
            config=self.config,
            on_add_files=self._add_files_to_queue,
            on_add_folder=self._add_folder_to_queue,
            on_convert=self._start_conversion,
            on_cancel=self._cancel_conversion,
            on_download_models=self._download_models
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Right: Main area (Queue + Console)
        main_area = ctk.CTkFrame(self, fg_color="gray14")
        main_area.grid(row=0, column=1, sticky="nsew")
        main_area.grid_rowconfigure(0, weight=1)  # Queue
        main_area.grid_rowconfigure(1, weight=1)  # Console
        main_area.grid_columnconfigure(0, weight=1)

        # Queue Panel
        self.queue_panel = QueuePanel(
            main_area,
            queue=self.queue,
            on_files_added=self._on_files_dropped
        )
        self.queue_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

        # Console Panel
        self.console_panel = ConsolePanel(main_area, config=self.config)
        self.console_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        # Status bar at bottom
        self._create_status_bar(main_area)

    def _create_status_bar(self, parent):
        """Create status bar at bottom of main area."""
        status_frame = ctk.CTkFrame(parent, height=30, fg_color="gray20")
        status_frame.grid(row=2, column=0, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)

        # Ready indicator
        self._ready_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=ctk.CTkFont(size=10),
            text_color="green"
        )
        self._ready_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Progress bar (hidden by default)
        self._progress_bar = ctk.CTkProgressBar(status_frame, mode="indeterminate", width=200)
        self._progress_bar.grid(row=0, column=1, padx=10, pady=5)
        self._progress_bar.grid_remove()

        # Version info
        version_label = ctk.CTkLabel(
            status_frame,
            text=f"v{self.VERSION}",
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
            self.console_panel.append("WARNING: Docling CLI not found. Please install: pip install docling\n")
        else:
            self.console_panel.append(f"Using Docling: {self.converter.docling_path}\n")

    # File/Queue Management

    def _add_files_to_queue(self):
        """Add multiple files to the queue via dialog."""
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
            self._on_files_dropped(list(filenames))

    def _add_folder_to_queue(self):
        """Add all files from a folder to the queue."""
        folder = filedialog.askdirectory(
            title="Select Folder to Add to Queue"
        )

        if folder:
            try:
                added_items = self.queue.add_folder(folder, recursive=True)
                self.console_panel.append(f"Added {len(added_items)} file(s) from folder: {folder}\n")

                for item in added_items:
                    self.queue_panel.add_item(item)

                self._update_convert_button()

            except Exception as e:
                messagebox.showerror("Error", f"Could not add folder:\n{str(e)}")

    def _on_files_dropped(self, file_paths: List[str]):
        """Handle files added via drop zone or dialog."""
        added_items = self.queue.add_files(file_paths)
        self.console_panel.append(f"Added {len(added_items)} file(s) to queue\n")

        for item in added_items:
            self.queue_panel.add_item(item)

        self._update_convert_button()

    def _update_convert_button(self):
        """Update convert button text based on queue."""
        if len(self.queue) > 0:
            stats = self.queue.get_statistics()
            pending = stats['pending']
            if pending > 0:
                self.sidebar.update_convert_button(f"CONVERT ({pending})")
            else:
                self.sidebar.update_convert_button("CONVERT")
        else:
            self.sidebar.update_convert_button("CONVERT")

    # Conversion

    def _start_conversion(self):
        """Start processing the queue."""
        if len(self.queue) == 0:
            messagebox.showwarning("No Files", "Please add files to the queue first.")
            return

        # Get params from sidebar
        params = self.sidebar.get_conversion_params()

        # Validate output directory
        output_dir = params['output_dir']
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return

        # Create output directory if needed
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create output directory:\n{str(e)}")
            return

        # Validate offline mode models if needed
        if params['processing_mode'] == "offline":
            artifacts_path = self.config.get("processing", "artifactsPath")
            models_ok, missing_files = self.converter.check_models_downloaded(artifacts_path)
            if not models_ok:
                error_msg = "Offline Mode: Required models not found!\n\n"
                error_msg += f"Missing files:\n"
                error_msg += "\n".join(f"  - {f}" for f in missing_files)
                error_msg += "\n\nClick 'Download Models' in the sidebar to download them."
                messagebox.showerror("Models Required", error_msg)
                return

        # Start processing
        self._set_processing_state(True)
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
        self.queue_panel.update_item_status(next_item.id, QueueItemStatus.PROCESSING)
        self.current_queue_item = next_item

        # Log
        stats = self.queue.get_statistics()
        current_index = stats['total'] - stats['pending']
        total = stats['total']

        self.console_panel.append(f"\n{'=' * 60}\n")
        self.console_panel.append(f"Processing [{current_index}/{total}]: {next_item.filename}\n")
        self.console_panel.append(f"{'=' * 60}\n")

        self._ready_label.configure(text=f"Processing {current_index}/{total}...", text_color="orange")

        # Get conversion parameters
        params = self.sidebar.get_conversion_params()
        artifacts_path = None
        if params['processing_mode'] == "offline":
            artifacts_path = self.config.get("processing", "artifactsPath")

        # Start conversion
        self.converter.convert(
            input_path=next_item.file_path,
            output_format=params['output_format'],
            output_dir=params['output_dir'],
            processing_mode=params['processing_mode'],
            ocr_enabled=params['ocr_enabled'],
            force_ocr=params['force_ocr'],
            pipeline=params['pipeline'],
            artifacts_path=artifacts_path,
            ocr_lang=params['ocr_lang'],
            ocr_engine=params.get('ocr_engine', 'auto'),
            vlm_model=params['vlm_model'],
            extract_tables=params['extract_tables'],
            enrich_code=params['enrich_code'],
            enrich_formula=params['enrich_formula'],
            enrich_picture_classes=params['enrich_picture_classes'],
            enrich_picture_description=params['enrich_picture_description'],
            image_export_mode=params['image_export_mode'],
            pdf_backend=params['pdf_backend'],
            pdf_password=params['pdf_password'],
            table_mode=params['table_mode'],
            show_layout=params['show_layout'],
            debug_visualize_layout=params['debug_visualize_layout'],
            debug_visualize_cells=params['debug_visualize_cells'],
            debug_visualize_ocr=params['debug_visualize_ocr'],
            debug_visualize_tables=params['debug_visualize_tables'],
            verbose=params['verbose'],
            on_output=self._on_conversion_output,
            on_complete=self._on_item_complete,
            on_error=self._on_item_error
        )

    def _cancel_conversion(self):
        """Cancel current conversion."""
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel?"):
            self.converter.cancel()
            self.console_panel.append("\n[CANCELLED] Conversion cancelled by user.\n")

            # Mark current item as cancelled
            if self.current_queue_item:
                self.queue.update_status(self.current_queue_item.id, QueueItemStatus.CANCELLED)
                self.queue_panel.update_item_status(
                    self.current_queue_item.id, QueueItemStatus.CANCELLED
                )

            self._set_processing_state(False)

    def _on_conversion_output(self, text: str):
        """Handle conversion output."""
        self.after(0, lambda: self.console_panel.append(text))

    def _on_item_complete(self, return_code: int):
        """Handle single item conversion completion."""
        def update_ui():
            if self.current_queue_item:
                if return_code == 0:
                    status = QueueItemStatus.COMPLETED
                    self.console_panel.append(f"\n[SUCCESS] Completed: {self.current_queue_item.filename}\n")
                else:
                    status = QueueItemStatus.FAILED
                    self.console_panel.append(f"\n[FAILED] {self.current_queue_item.filename} (exit code: {return_code})\n")

                self.queue.update_status(self.current_queue_item.id, status)
                self.queue_panel.update_item_status(self.current_queue_item.id, status)
                self.current_queue_item = None

            # Process next item
            self._process_next_in_queue()

        self.after(0, update_ui)

    def _on_item_error(self, error: str):
        """Handle item conversion error."""
        def update_ui():
            if self.current_queue_item:
                self.queue.update_status(
                    self.current_queue_item.id,
                    QueueItemStatus.FAILED,
                    error
                )
                self.queue_panel.update_item_status(
                    self.current_queue_item.id,
                    QueueItemStatus.FAILED,
                    error
                )
                self.console_panel.append(f"\n[ERROR] {self.current_queue_item.filename}: {error}\n")
                self.current_queue_item = None

            # Process next item
            self._process_next_in_queue()

        self.after(0, update_ui)

    def _on_queue_complete(self):
        """Handle entire queue completion."""
        stats = self.queue.get_statistics()

        self.console_panel.append(f"\n{'=' * 60}\n")
        self.console_panel.append("[QUEUE COMPLETE]\n")
        self.console_panel.append(f"Total files processed: {stats['total']}\n")
        self.console_panel.append(f"Completed successfully: {stats['completed']}\n")
        self.console_panel.append(f"Failed: {stats['failed']}\n")
        params = self.sidebar.get_conversion_params()
        self.console_panel.append(f"Output directory: {params['output_dir']}\n")
        self.console_panel.append(f"{'=' * 60}\n")

        # Show completion dialog
        if stats['failed'] > 0:
            messagebox.showinfo(
                "Queue Complete",
                f"Queue processing complete!\n\n"
                f"Successful: {stats['completed']}\n"
                f"Failed: {stats['failed']}\n\n"
                f"Check console for details."
            )
        else:
            messagebox.showinfo(
                "Success",
                f"All {stats['completed']} files converted successfully!"
            )

        self._set_processing_state(False)

    def _set_processing_state(self, is_processing: bool):
        """Update UI for processing state."""
        self.is_processing = is_processing
        self.sidebar.set_processing_state(is_processing)

        if is_processing:
            self._progress_bar.grid()
            self._progress_bar.start()
            self._ready_label.configure(text="Processing...", text_color="orange")
        else:
            self._progress_bar.stop()
            self._progress_bar.grid_remove()
            self._ready_label.configure(text="Ready", text_color="green")
            self._update_convert_button()

    # Model Download

    def _download_models(self):
        """Open model download dialog."""
        if self.converter.is_running:
            messagebox.showwarning("Busy", "Please wait for the current operation to complete.")
            return

        # Create dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Download Models")
        dialog.geometry("450x280")
        dialog.transient(self)
        dialog.grab_set()

        # Center
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
            text="Models will be downloaded for offline operation.\nProgress will be shown in the console.",
            font=ctk.CTkFont(size=11)
        ).pack(pady=10)

        download_all_var = ctk.BooleanVar(value=True)
        download_smoldocling_var = ctk.BooleanVar(value=False)
        download_smolvlm_var = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(
            dialog,
            text="All Standard Models",
            variable=download_all_var,
            font=ctk.CTkFont(size=12)
        ).pack(pady=5, padx=20, anchor="w")

        ctk.CTkCheckBox(
            dialog,
            text="SmolDocling-256M (VLM model)",
            variable=download_smoldocling_var,
            font=ctk.CTkFont(size=12)
        ).pack(pady=5, padx=20, anchor="w")

        ctk.CTkCheckBox(
            dialog,
            text="SmolVLM-256M-Instruct",
            variable=download_smolvlm_var,
            font=ctk.CTkFont(size=12)
        ).pack(pady=5, padx=20, anchor="w")

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)

        def start_download():
            if not any([download_all_var.get(), download_smoldocling_var.get(), download_smolvlm_var.get()]):
                messagebox.showwarning("No Selection", "Please select at least one model.")
                return

            dialog.destroy()
            self.console_panel.append("\n" + "=" * 60 + "\n")
            self.console_panel.append("Starting model download...\n")
            self.console_panel.append("=" * 60 + "\n")

            self._set_processing_state(True)
            self._ready_label.configure(text="Downloading models...", text_color="orange")

            self.converter.download_models(
                download_all=download_all_var.get(),
                download_smoldocling=download_smoldocling_var.get(),
                download_smolvlm=download_smolvlm_var.get(),
                on_output=self._on_conversion_output,
                on_complete=self._on_download_complete,
                on_error=lambda err: messagebox.showerror("Download Error", err)
            )

        ctk.CTkButton(
            btn_frame,
            text="Download",
            command=start_download,
            width=100
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            width=100,
            fg_color="gray40",
            hover_color="gray30"
        ).pack(side="left", padx=5)

    def _on_download_complete(self, return_code: int):
        """Handle model download completion."""
        def update_ui():
            self._set_processing_state(False)

            if return_code == 0:
                messagebox.showinfo("Success", "Models downloaded successfully!")
            else:
                messagebox.showinfo("Completed", "Model download finished. Check console for details.")

        self.after(0, update_ui)

    # Cleanup

    def _on_closing(self):
        """Handle window closing."""
        if self.is_processing:
            if not messagebox.askyesno("Quit", "Processing in progress. Are you sure you want to quit?"):
                return

        # Close console panel (closes log file)
        self.console_panel.close()

        # Save window size
        geometry = self.geometry().split('+')[0]
        width, height = geometry.split('x')
        self.config.set("window", "width", value=int(width))
        self.config.set("window", "height", value=int(height))

        self.destroy()
