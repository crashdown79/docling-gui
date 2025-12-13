"""Queue item widget for displaying individual files in the queue."""

import customtkinter as ctk
from typing import Callable, Optional
from core.queue import QueueItem, QueueItemStatus


class QueueItemWidget(ctk.CTkFrame):
    """
    Visual representation of a single queue item.

    Shows file name, size, status, and provides a remove button.
    Status is indicated by both icon and color.
    """

    def __init__(
        self,
        parent,
        queue_item: QueueItem,
        on_remove: Optional[Callable[[str], None]] = None
    ):
        """
        Initialize QueueItemWidget.

        Args:
            parent: Parent widget
            queue_item: The QueueItem data to display
            on_remove: Callback when remove button is clicked (receives item_id)
        """
        super().__init__(parent, fg_color="gray25", corner_radius=6)

        self.queue_item = queue_item
        self._on_remove = on_remove

        self._create_widgets()

    def _create_widgets(self):
        """Create the item widgets."""
        self.grid_columnconfigure(2, weight=1)

        # Status icon
        self._status_icon = ctk.CTkLabel(
            self,
            text=self.queue_item.get_status_icon(),
            font=ctk.CTkFont(size=16),
            text_color=self.queue_item.get_status_color(),
            width=30
        )
        self._status_icon.grid(row=0, column=0, padx=(10, 5), pady=8)

        # Filename
        self._filename_label = ctk.CTkLabel(
            self,
            text=self.queue_item.filename,
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self._filename_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        # File info (format and size)
        info_text = f"{self.queue_item.file_format.upper()} • {self.queue_item.get_size_string()}"
        self._info_label = ctk.CTkLabel(
            self,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color="gray60"
        )
        self._info_label.grid(row=0, column=2, padx=5, pady=8, sticky="w")

        # Status text
        self._status_text = ctk.CTkLabel(
            self,
            text=self.queue_item.status.value.capitalize(),
            font=ctk.CTkFont(size=10),
            text_color=self.queue_item.get_status_color(),
            width=80
        )
        self._status_text.grid(row=0, column=3, padx=5, pady=8)

        # Remove button
        self._remove_btn = ctk.CTkButton(
            self,
            text="✕",
            width=28,
            height=24,
            font=ctk.CTkFont(size=12),
            fg_color="gray40",
            hover_color="gray30",
            command=self._on_remove_click
        )
        self._remove_btn.grid(row=0, column=4, padx=(5, 10), pady=8)

        # Disable remove button if processing
        if self.queue_item.status == QueueItemStatus.PROCESSING:
            self._remove_btn.configure(state="disabled")

    def _on_remove_click(self):
        """Handle remove button click."""
        if self._on_remove:
            self._on_remove(self.queue_item.id)

    def update_status(self, status: QueueItemStatus, error_message: Optional[str] = None):
        """
        Update the displayed status.

        Args:
            status: New status
            error_message: Optional error message for failed items
        """
        self.queue_item.status = status
        self.queue_item.error_message = error_message

        # Update visuals
        self._status_icon.configure(
            text=self.queue_item.get_status_icon(),
            text_color=self.queue_item.get_status_color()
        )
        self._status_text.configure(
            text=status.value.capitalize(),
            text_color=self.queue_item.get_status_color()
        )

        # Update remove button state
        if status == QueueItemStatus.PROCESSING:
            self._remove_btn.configure(state="disabled")
        else:
            self._remove_btn.configure(state="normal")

        # Update background for completed/failed
        if status == QueueItemStatus.COMPLETED:
            self.configure(fg_color="gray30")
        elif status == QueueItemStatus.FAILED:
            self.configure(fg_color="#3d2020")
        else:
            self.configure(fg_color="gray25")

    def set_selected(self, selected: bool):
        """
        Set selected visual state.

        Args:
            selected: Whether item is selected
        """
        if selected:
            self.configure(fg_color="#1f538d")
        else:
            # Reset to status-appropriate color
            if self.queue_item.status == QueueItemStatus.COMPLETED:
                self.configure(fg_color="gray30")
            elif self.queue_item.status == QueueItemStatus.FAILED:
                self.configure(fg_color="#3d2020")
            else:
                self.configure(fg_color="gray25")
