"""Collapsible section widget for organized UI layouts."""

import customtkinter as ctk
from typing import Optional, Callable


class CollapsibleSection(ctk.CTkFrame):
    """
    A frame that can be collapsed/expanded with a toggle button.

    Used to organize settings into logical groups that can be hidden
    when not needed, saving screen space.
    """

    def __init__(
        self,
        parent,
        title: str,
        is_expanded: bool = True,
        header_color: Optional[str] = None,
        on_toggle: Optional[Callable[[bool], None]] = None
    ):
        """
        Initialize CollapsibleSection.

        Args:
            parent: Parent widget
            title: Section title text
            is_expanded: Whether section starts expanded
            header_color: Optional background color for header
            on_toggle: Optional callback when section is toggled (receives is_expanded)
        """
        super().__init__(parent)

        self.title = title
        self._is_expanded = is_expanded
        self._on_toggle = on_toggle
        self._header_color = header_color

        self._create_widgets()

        # Set initial state
        if not is_expanded:
            self._content_frame.grid_remove()

    def _create_widgets(self):
        """Create the section widgets."""
        self.grid_columnconfigure(0, weight=1)

        # Header frame
        header_kwargs = {"fg_color": "transparent"}
        if self._header_color:
            header_kwargs["fg_color"] = self._header_color

        self._header_frame = ctk.CTkFrame(self, **header_kwargs)
        self._header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self._header_frame.grid_columnconfigure(1, weight=1)

        # Toggle button
        toggle_text = "▼" if self._is_expanded else "▶"
        self._toggle_btn = ctk.CTkButton(
            self._header_frame,
            text=toggle_text,
            width=30,
            height=24,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="transparent",
            hover_color="gray30",
            command=self.toggle
        )
        self._toggle_btn.grid(row=0, column=0, padx=(5, 5), pady=5)

        # Title label
        self._title_label = ctk.CTkLabel(
            self._header_frame,
            text=self.title,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self._title_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Make header clickable
        self._header_frame.bind("<Button-1>", lambda e: self.toggle())
        self._title_label.bind("<Button-1>", lambda e: self.toggle())

        # Content frame
        self._content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self._content_frame.grid_columnconfigure(0, weight=1)

    @property
    def content(self) -> ctk.CTkFrame:
        """Get the content frame where child widgets should be placed."""
        return self._content_frame

    @property
    def is_expanded(self) -> bool:
        """Check if section is currently expanded."""
        return self._is_expanded

    def toggle(self):
        """Toggle section expanded/collapsed state."""
        if self._is_expanded:
            self.collapse()
        else:
            self.expand()

    def expand(self):
        """Expand the section to show content."""
        if not self._is_expanded:
            self._is_expanded = True
            self._toggle_btn.configure(text="▼")
            self._content_frame.grid()

            if self._on_toggle:
                self._on_toggle(True)

    def collapse(self):
        """Collapse the section to hide content."""
        if self._is_expanded:
            self._is_expanded = False
            self._toggle_btn.configure(text="▶")
            self._content_frame.grid_remove()

            if self._on_toggle:
                self._on_toggle(False)

    def set_expanded(self, expanded: bool):
        """Set the expanded state."""
        if expanded:
            self.expand()
        else:
            self.collapse()

    def add_header_widget(self, widget: ctk.CTkBaseClass, **grid_kwargs):
        """
        Add a widget to the header area (right side).

        Args:
            widget: Widget to add
            **grid_kwargs: Additional grid options
        """
        default_kwargs = {"row": 0, "column": 2, "padx": 10, "pady": 5}
        default_kwargs.update(grid_kwargs)
        widget.grid(**default_kwargs)
