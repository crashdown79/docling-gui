"""Drag-and-drop file zone widget with tkinterdnd2 support."""

import customtkinter as ctk
from tkinter import filedialog
from typing import Callable, List, Optional
from pathlib import Path
import os
import re

# Try to import tkinterdnd2 for true drag-and-drop support
DND_AVAILABLE = False
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    pass


class FileDropZone(ctk.CTkFrame):
    """
    A visual drop zone for adding files via drag-and-drop or click.

    Supports true drag-and-drop when tkinterdnd2 is available,
    otherwise provides a clickable alternative that opens a file dialog.
    """

    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        'pdf', 'docx', 'pptx', 'html', 'htm', 'md', 'csv', 'xlsx',
        'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff',
        'mp3', 'mp4', 'wav', 'avi', 'mov', 'xml', 'json'
    }

    def __init__(
        self,
        parent,
        on_files_added: Callable[[List[str]], None],
        height: int = 150,
        placeholder_text: str = "Drag files here or click to add",
        allow_folders: bool = True
    ):
        """
        Initialize FileDropZone.

        Args:
            parent: Parent widget
            on_files_added: Callback when files are added (receives list of paths)
            height: Height of the drop zone
            placeholder_text: Text shown in empty state
            allow_folders: Whether to allow folder selection
        """
        super().__init__(parent, height=height)

        self._on_files_added = on_files_added
        self._placeholder_text = placeholder_text
        self._allow_folders = allow_folders
        self._is_drag_over = False
        self._dnd_enabled = False

        self._create_widgets()
        self._setup_bindings()
        self._setup_dnd()

    def _create_widgets(self):
        """Create the zone widgets."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Inner frame with dashed border effect
        self._inner_frame = ctk.CTkFrame(
            self,
            fg_color="gray20",
            corner_radius=10
        )
        self._inner_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self._inner_frame.grid_columnconfigure(0, weight=1)
        self._inner_frame.grid_rowconfigure(0, weight=1)

        # Content container
        content = ctk.CTkFrame(self._inner_frame, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")

        # Icon
        self._icon_label = ctk.CTkLabel(
            content,
            text="📁",
            font=ctk.CTkFont(size=32)
        )
        self._icon_label.pack(pady=(0, 10))

        # Main text
        self._text_label = ctk.CTkLabel(
            content,
            text=self._placeholder_text,
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        self._text_label.pack()

        # Hint text
        self._hint_label = ctk.CTkLabel(
            content,
            text="Supported: PDF, DOCX, PPTX, HTML, Images, and more",
            font=ctk.CTkFont(size=10),
            text_color="gray50"
        )
        self._hint_label.pack(pady=(5, 0))

        # Button frame
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=(15, 0))

        # Add Files button
        self._add_files_btn = ctk.CTkButton(
            btn_frame,
            text="+ Add Files",
            command=self._on_add_files_click,
            width=100,
            height=30,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        self._add_files_btn.pack(side="left", padx=5)

        # Add Folder button
        if self._allow_folders:
            self._add_folder_btn = ctk.CTkButton(
                btn_frame,
                text="Folder",
                command=self._on_add_folder_click,
                width=80,
                height=30,
                fg_color="gray40",
                hover_color="gray30"
            )
            self._add_folder_btn.pack(side="left", padx=5)

    def _setup_bindings(self):
        """Setup event bindings."""
        # Make entire zone clickable
        self._inner_frame.bind("<Button-1>", lambda e: self._on_add_files_click())
        self._icon_label.bind("<Button-1>", lambda e: self._on_add_files_click())
        self._text_label.bind("<Button-1>", lambda e: self._on_add_files_click())
        self._hint_label.bind("<Button-1>", lambda e: self._on_add_files_click())

        # Hover effects
        self._inner_frame.bind("<Enter>", self._on_hover_enter)
        self._inner_frame.bind("<Leave>", self._on_hover_leave)

    def _setup_dnd(self):
        """Setup drag-and-drop if tkinterdnd2 is available."""
        if not DND_AVAILABLE:
            return

        try:
            # Get the root window
            root = self.winfo_toplevel()

            # Check if root is a TkinterDnD window
            if not hasattr(root, 'drop_target_register'):
                return

            # Register this widget as a drop target
            self._inner_frame.drop_target_register(DND_FILES)
            self._inner_frame.dnd_bind('<<DropEnter>>', self._on_dnd_enter)
            self._inner_frame.dnd_bind('<<DropLeave>>', self._on_dnd_leave)
            self._inner_frame.dnd_bind('<<Drop>>', self._on_dnd_drop)

            self._dnd_enabled = True

            # Update placeholder text to indicate DnD is available
            if "click" in self._placeholder_text.lower():
                self._text_label.configure(text=self._placeholder_text)

        except Exception as e:
            # DnD not available for this widget
            print(f"DnD setup failed: {e}")
            self._dnd_enabled = False

    def _on_dnd_enter(self, event):
        """Handle drag enter event."""
        self.set_drag_over(True)
        return event.action

    def _on_dnd_leave(self, event):
        """Handle drag leave event."""
        self.set_drag_over(False)
        return event.action

    def _on_dnd_drop(self, event):
        """Handle drop event."""
        self.set_drag_over(False)

        # Parse the dropped data
        file_paths = self._parse_dnd_data(event.data)

        # Filter to supported files and expand folders
        valid_files = []
        for path in file_paths:
            if os.path.isdir(path):
                # Scan folder for supported files
                valid_files.extend(self._scan_folder(path))
            elif os.path.isfile(path):
                ext = Path(path).suffix.lower().lstrip('.')
                if ext in self.SUPPORTED_EXTENSIONS:
                    valid_files.append(path)

        if valid_files:
            self._on_files_added(valid_files)

        return event.action

    def _parse_dnd_data(self, data: str) -> List[str]:
        """
        Parse drag-and-drop data string to extract file paths.

        Handles different formats:
        - Space-separated paths (paths with spaces are in braces)
        - Single paths
        - Platform-specific variations

        Args:
            data: Raw DnD data string

        Returns:
            List of file paths
        """
        if not data:
            return []

        paths = []

        # Handle paths enclosed in braces (common when paths have spaces)
        # Format: {/path/with spaces/file.pdf} {/another path/file.docx}
        brace_pattern = r'\{([^}]+)\}'
        brace_matches = re.findall(brace_pattern, data)

        if brace_matches:
            paths.extend(brace_matches)
            # Remove braced parts from data to handle any remaining paths
            data = re.sub(brace_pattern, '', data).strip()

        # Handle any remaining space-separated paths (no spaces in path)
        if data:
            remaining = data.split()
            paths.extend(remaining)

        # Clean up paths
        cleaned_paths = []
        for path in paths:
            # Remove any surrounding whitespace
            path = path.strip()

            # Skip empty strings
            if not path:
                continue

            # On Windows, paths might start with a letter like file:///
            # or have forward slashes that need converting
            if path.startswith('file:///'):
                path = path[8:]  # Remove 'file:///'
                # On Windows, this leaves /C:/path, remove leading /
                if len(path) > 2 and path[0] == '/' and path[2] == ':':
                    path = path[1:]

            # Normalize path separators for the current platform
            path = os.path.normpath(path)

            if path:
                cleaned_paths.append(path)

        return cleaned_paths

    def _on_hover_enter(self, event=None):
        """Handle mouse enter."""
        if not self._is_drag_over:
            self._inner_frame.configure(fg_color="gray25")

    def _on_hover_leave(self, event=None):
        """Handle mouse leave."""
        if not self._is_drag_over:
            self._inner_frame.configure(fg_color="gray20")

    def _on_add_files_click(self):
        """Handle add files button click."""
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
            title="Select Files to Add",
            filetypes=filetypes
        )

        if filenames:
            self._on_files_added(list(filenames))

    def _on_add_folder_click(self):
        """Handle add folder button click."""
        folder = filedialog.askdirectory(
            title="Select Folder to Add"
        )

        if folder:
            # Find all supported files in folder
            files = self._scan_folder(folder)
            if files:
                self._on_files_added(files)

    def _scan_folder(self, folder_path: str, recursive: bool = True) -> List[str]:
        """
        Scan a folder for supported files.

        Args:
            folder_path: Path to folder
            recursive: Whether to scan recursively

        Returns:
            List of file paths
        """
        path = Path(folder_path)
        files = []

        if recursive:
            for ext in self.SUPPORTED_EXTENSIONS:
                files.extend(str(f) for f in path.rglob(f"*.{ext}"))
        else:
            for ext in self.SUPPORTED_EXTENSIONS:
                files.extend(str(f) for f in path.glob(f"*.{ext}"))

        return sorted(files)

    def set_drag_over(self, is_over: bool):
        """
        Set drag-over visual state.

        Args:
            is_over: Whether mouse is dragging over zone
        """
        self._is_drag_over = is_over
        if is_over:
            self._inner_frame.configure(fg_color="#1f538d")
            self._text_label.configure(text="Drop files here!")
            self._icon_label.configure(text="📥")
        else:
            self._inner_frame.configure(fg_color="gray20")
            self._text_label.configure(text=self._placeholder_text)
            self._icon_label.configure(text="📁")

    def update_placeholder(self, text: str):
        """Update the placeholder text."""
        self._placeholder_text = text
        if not self._is_drag_over:
            self._text_label.configure(text=text)

    @property
    def dnd_enabled(self) -> bool:
        """Check if drag-and-drop is enabled."""
        return self._dnd_enabled
