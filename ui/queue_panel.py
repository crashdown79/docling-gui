"""Queue panel component for batch file management."""

import customtkinter as ctk
from typing import Callable, Dict, List, Optional
from core.queue import ConversionQueue, QueueItem, QueueItemStatus
from ui.widgets import FileDropZone, QueueItemWidget


class QueuePanel(ctk.CTkFrame):
    """
    Batch queue visualization panel.

    Displays the list of files to be converted with their status,
    provides drag-and-drop support, and queue management buttons.
    """

    def __init__(
        self,
        parent,
        queue: ConversionQueue,
        on_files_added: Optional[Callable[[List[str]], None]] = None
    ):
        """
        Initialize QueuePanel.

        Args:
            parent: Parent widget
            queue: The ConversionQueue to visualize
            on_files_added: Callback when files are added via drop zone
        """
        super().__init__(parent)

        self.queue = queue
        self._on_files_added = on_files_added
        self._item_widgets: Dict[str, QueueItemWidget] = {}

        self._create_widgets()

    def _create_widgets(self):
        """Create panel widgets."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header frame
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        # Title with file count
        self._title_label = ctk.CTkLabel(
            header_frame,
            text="Batch Queue (0 files)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self._title_label.grid(row=0, column=0, sticky="w")

        # Stats label
        self._stats_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        )
        self._stats_label.grid(row=0, column=1, padx=15, sticky="w")

        # Buttons container
        btn_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_container.grid(row=0, column=2, sticky="e")

        # Clear Completed button
        self._clear_completed_btn = ctk.CTkButton(
            btn_container,
            text="Clear Completed",
            command=self._on_clear_completed,
            width=110,
            height=26,
            font=ctk.CTkFont(size=11),
            fg_color="gray40",
            hover_color="gray30"
        )
        self._clear_completed_btn.pack(side="left", padx=(0, 5))

        # Clear All button
        self._clear_all_btn = ctk.CTkButton(
            btn_container,
            text="Clear All",
            command=self._on_clear_all,
            width=80,
            height=26,
            font=ctk.CTkFont(size=11),
            fg_color="gray40",
            hover_color="gray30"
        )
        self._clear_all_btn.pack(side="left")

        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color="gray15")
        content_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Drop zone (shows when queue is empty)
        self._drop_zone = FileDropZone(
            content_frame,
            on_files_added=self._on_drop_zone_files,
            placeholder_text="Drag files here or add from sidebar"
        )
        self._drop_zone.grid(row=0, column=0, sticky="nsew")

        # Queue list (shows when queue has items)
        self._queue_list = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="transparent"
        )
        self._queue_list.grid(row=0, column=0, sticky="nsew")
        self._queue_list.grid_columnconfigure(0, weight=1)

        # Initially show drop zone, hide list
        self._queue_list.grid_remove()

        # Update display
        self._update_header()

    def _on_drop_zone_files(self, file_paths: List[str]):
        """Handle files from drop zone."""
        if self._on_files_added:
            self._on_files_added(file_paths)

    def add_item(self, item: QueueItem):
        """
        Add a queue item to the display.

        Args:
            item: QueueItem to add
        """
        # Create widget
        widget = QueueItemWidget(
            self._queue_list,
            item,
            on_remove=self._on_item_remove
        )
        widget.grid(row=len(self._item_widgets), column=0, sticky="ew", pady=2)

        # Store reference
        self._item_widgets[item.id] = widget

        # Show list, hide drop zone
        self._drop_zone.grid_remove()
        self._queue_list.grid()

        # Update header
        self._update_header()

    def add_items(self, items: List[QueueItem]):
        """
        Add multiple queue items to the display.

        Args:
            items: List of QueueItems to add
        """
        for item in items:
            self.add_item(item)

    def remove_item(self, item_id: str):
        """
        Remove an item from the display.

        Args:
            item_id: ID of item to remove
        """
        if item_id in self._item_widgets:
            self._item_widgets[item_id].destroy()
            del self._item_widgets[item_id]

            # Reposition remaining items
            self._reposition_items()

            # Show drop zone if empty
            if len(self._item_widgets) == 0:
                self._queue_list.grid_remove()
                self._drop_zone.grid()

            # Update header
            self._update_header()

    def update_item_status(self, item_id: str, status: QueueItemStatus,
                          error_message: Optional[str] = None):
        """
        Update the status of an item.

        Args:
            item_id: ID of item to update
            status: New status
            error_message: Optional error message
        """
        if item_id in self._item_widgets:
            self._item_widgets[item_id].update_status(status, error_message)
            self._update_header()

    def refresh(self):
        """Refresh the entire queue display from queue data."""
        # Clear existing widgets
        for widget in self._item_widgets.values():
            widget.destroy()
        self._item_widgets.clear()

        # Add items from queue
        for item in self.queue.items:
            widget = QueueItemWidget(
                self._queue_list,
                item,
                on_remove=self._on_item_remove
            )
            widget.grid(row=len(self._item_widgets), column=0, sticky="ew", pady=2)
            self._item_widgets[item.id] = widget

        # Update visibility
        if len(self._item_widgets) == 0:
            self._queue_list.grid_remove()
            self._drop_zone.grid()
        else:
            self._drop_zone.grid_remove()
            self._queue_list.grid()

        self._update_header()

    def clear_completed(self):
        """Clear completed and failed items."""
        # Get IDs to remove
        ids_to_remove = [
            item_id for item_id, widget in self._item_widgets.items()
            if widget.queue_item.status in (QueueItemStatus.COMPLETED, QueueItemStatus.FAILED)
        ]

        # Remove widgets
        for item_id in ids_to_remove:
            self._item_widgets[item_id].destroy()
            del self._item_widgets[item_id]

        # Also clear from queue
        self.queue.clear_completed()

        # Reposition
        self._reposition_items()

        # Update visibility
        if len(self._item_widgets) == 0:
            self._queue_list.grid_remove()
            self._drop_zone.grid()

        self._update_header()

    def clear_all(self):
        """Clear all items."""
        # Remove all widgets
        for widget in self._item_widgets.values():
            widget.destroy()
        self._item_widgets.clear()

        # Clear queue
        self.queue.clear_queue()

        # Show drop zone
        self._queue_list.grid_remove()
        self._drop_zone.grid()

        self._update_header()

    def _on_item_remove(self, item_id: str):
        """Handle item remove button click."""
        if self.queue.remove_item(item_id):
            self.remove_item(item_id)

    def _on_clear_completed(self):
        """Handle clear completed button click."""
        self.clear_completed()

    def _on_clear_all(self):
        """Handle clear all button click."""
        from tkinter import messagebox
        if len(self.queue) > 0:
            if messagebox.askyesno("Confirm", "Clear all items from queue?"):
                self.clear_all()

    def _reposition_items(self):
        """Reposition items after removal."""
        for idx, widget in enumerate(self._item_widgets.values()):
            widget.grid(row=idx, column=0, sticky="ew", pady=2)

    def _update_header(self):
        """Update header with current queue stats."""
        stats = self.queue.get_statistics()
        total = stats['total']

        # Update title
        self._title_label.configure(text=f"Batch Queue ({total} files)")

        # Update stats
        if total == 0:
            self._stats_label.configure(text="")
        else:
            parts = []
            if stats['pending'] > 0:
                parts.append(f"{stats['pending']} pending")
            if stats['processing'] > 0:
                parts.append(f"{stats['processing']} processing")
            if stats['completed'] > 0:
                parts.append(f"{stats['completed']} done")
            if stats['failed'] > 0:
                parts.append(f"{stats['failed']} failed")

            self._stats_label.configure(text=" | ".join(parts))

    @property
    def file_count(self) -> int:
        """Get number of files in queue."""
        return len(self.queue)

    @property
    def pending_count(self) -> int:
        """Get number of pending files."""
        return self.queue.get_statistics()['pending']
