"""Console output panel component."""

import customtkinter as ctk
from pathlib import Path
from datetime import datetime
from typing import Optional
from config import Config


class ConsolePanel(ctk.CTkFrame):
    """
    Console output panel for displaying conversion logs and status.

    Features:
    - Scrollable text output
    - Save to log file option
    - Clear console button
    - Auto-scroll to bottom
    """

    def __init__(self, parent, config: Config):
        """
        Initialize ConsolePanel.

        Args:
            parent: Parent widget
            config: Application configuration
        """
        super().__init__(parent)

        self.config = config
        self._log_file_handle = None
        self._current_log_file: Optional[Path] = None

        self._create_widgets()

        # Auto-start logging if enabled
        if self._enable_log_var.get():
            self._create_log_file()

    def _create_widgets(self):
        """Create panel widgets."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header frame
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            header_frame,
            text="Console Output",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        # Buttons container
        btn_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_container.grid(row=0, column=1, sticky="e")

        # Save log checkbox
        enable_logging = self.config.get("general", "enableLogging", default=False)
        self._enable_log_var = ctk.BooleanVar(value=enable_logging)
        self._log_checkbox = ctk.CTkCheckBox(
            btn_container,
            text="Save Log",
            variable=self._enable_log_var,
            command=self._on_log_enable_change,
            font=ctk.CTkFont(size=11),
            width=80
        )
        self._log_checkbox.pack(side="left", padx=(0, 10))

        # Clear button
        self._clear_btn = ctk.CTkButton(
            btn_container,
            text="Clear Log",
            command=self.clear,
            width=80,
            height=26,
            font=ctk.CTkFont(size=11),
            fg_color="gray40",
            hover_color="gray30"
        )
        self._clear_btn.pack(side="left")

        # Console textbox
        self._console_text = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Courier", size=11),
            fg_color="gray10",
            text_color="gray80",
            wrap="word"
        )
        self._console_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Welcome message
        self.append("Docling GUI v1.5.2 initialized.\nReady to convert documents.\n")

    def append(self, text: str):
        """
        Append text to console output.

        Args:
            text: Text to append
        """
        self._console_text.insert("end", text)
        self._console_text.see("end")

        # Write to log file if enabled
        if self._enable_log_var.get() and self._log_file_handle:
            try:
                self._log_file_handle.write(text)
                self._log_file_handle.flush()
            except Exception as e:
                # Disable logging on error
                self._enable_log_var.set(False)
                self.config.set("general", "enableLogging", value=False)
                self._close_log_file()
                self._console_text.insert("end", f"\n[ERROR] Log file write failed: {str(e)}\n")

    def clear(self):
        """Clear console output."""
        self._console_text.delete("1.0", "end")
        self.append("Console cleared.\n")

    def get_text(self) -> str:
        """Get all console text."""
        return self._console_text.get("1.0", "end")

    def _on_log_enable_change(self):
        """Handle log enable checkbox change."""
        enabled = self._enable_log_var.get()
        self.config.set("general", "enableLogging", value=enabled)

        if enabled:
            if self._create_log_file():
                self.append(f"Logging enabled. Saving to: {self._current_log_file}\n")
        else:
            if self._current_log_file:
                log_path = str(self._current_log_file)
                self._close_log_file()
                self.append(f"Logging disabled. Log saved to: {log_path}\n")

    def _create_log_file(self) -> bool:
        """
        Create a new log file with timestamp.

        Returns:
            True if successful, False otherwise
        """
        if self._log_file_handle:
            self._close_log_file()

        log_dir = Path(self.config.get("general", "logDirectory",
                                       default=str(Path.home() / "Documents" / "docling_logs")))

        try:
            log_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"docling_log_{timestamp}.txt"
            self._current_log_file = log_dir / log_filename

            self._log_file_handle = open(self._current_log_file, 'w', encoding='utf-8')
            header = f"Docling GUI Log File\n"
            header += f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            header += "=" * 60 + "\n\n"
            self._log_file_handle.write(header)
            self._log_file_handle.flush()
            return True

        except Exception as e:
            self._enable_log_var.set(False)
            self._current_log_file = None
            self.append(f"[ERROR] Failed to create log file: {str(e)}\n")
            return False

    def _close_log_file(self):
        """Close the current log file."""
        if self._log_file_handle:
            try:
                footer = f"\n{'=' * 60}\n"
                footer += f"Log ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                self._log_file_handle.write(footer)
                self._log_file_handle.close()
            except:
                pass
            finally:
                self._log_file_handle = None
                self._current_log_file = None

    def close(self):
        """Close panel and cleanup resources."""
        self._close_log_file()

    @property
    def logging_enabled(self) -> bool:
        """Check if logging is enabled."""
        return self._enable_log_var.get()

    @property
    def current_log_file(self) -> Optional[Path]:
        """Get current log file path."""
        return self._current_log_file
