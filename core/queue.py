"""Queue management for batch processing."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional
from datetime import datetime


class QueueItemStatus(Enum):
    """Status of a queue item."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class QueueItem:
    """Represents a single file in the conversion queue."""

    id: str  # Unique identifier
    file_path: str  # Full path to the file
    filename: str  # Just the filename for display
    file_size: int  # Size in bytes
    file_format: str  # File extension (pdf, docx, etc.)
    status: QueueItemStatus = QueueItemStatus.PENDING
    error_message: Optional[str] = None
    added_time: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    def __post_init__(self):
        """Initialize computed fields."""
        if self.added_time is None:
            self.added_time = datetime.now()

    def get_size_string(self) -> str:
        """Return human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def get_status_icon(self) -> str:
        """Return icon for current status."""
        icons = {
            QueueItemStatus.PENDING: "⋯",
            QueueItemStatus.PROCESSING: "⟳",
            QueueItemStatus.COMPLETED: "✓",
            QueueItemStatus.FAILED: "✗",
            QueueItemStatus.CANCELLED: "⊘"
        }
        return icons.get(self.status, "?")

    def get_status_color(self) -> str:
        """Return color for current status."""
        colors = {
            QueueItemStatus.PENDING: "gray",
            QueueItemStatus.PROCESSING: "blue",
            QueueItemStatus.COMPLETED: "green",
            QueueItemStatus.FAILED: "red",
            QueueItemStatus.CANCELLED: "orange"
        }
        return colors.get(self.status, "gray")


class ConversionQueue:
    """Manages the queue of files to be converted."""

    def __init__(self):
        self.items: List[QueueItem] = []
        self._next_id = 1

    def add_file(self, file_path: str) -> QueueItem:
        """Add a single file to the queue."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Not a file: {file_path}")

        # Create queue item
        item = QueueItem(
            id=str(self._next_id),
            file_path=str(path.absolute()),
            filename=path.name,
            file_size=path.stat().st_size,
            file_format=path.suffix.lstrip('.').lower() or 'unknown'
        )

        self.items.append(item)
        self._next_id += 1

        return item

    def add_files(self, file_paths: List[str]) -> List[QueueItem]:
        """Add multiple files to the queue."""
        added_items = []
        for file_path in file_paths:
            try:
                item = self.add_file(file_path)
                added_items.append(item)
            except (FileNotFoundError, ValueError) as e:
                print(f"Skipping {file_path}: {e}")
                continue
        return added_items

    def add_folder(self, folder_path: str, recursive: bool = True) -> List[QueueItem]:
        """Add all supported files from a folder."""
        path = Path(folder_path)

        if not path.exists() or not path.is_dir():
            raise ValueError(f"Invalid folder: {folder_path}")

        # Supported file extensions (from Docling's --from parameter)
        supported_extensions = {
            'pdf', 'docx', 'pptx', 'html', 'htm', 'md', 'csv', 'xlsx',
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff',
            'mp3', 'mp4', 'wav', 'avi', 'mov'
        }

        # Find all supported files
        file_paths = []
        if recursive:
            for ext in supported_extensions:
                file_paths.extend(path.rglob(f"*.{ext}"))
        else:
            for ext in supported_extensions:
                file_paths.extend(path.glob(f"*.{ext}"))

        # Add found files
        return self.add_files([str(f) for f in file_paths])

    def remove_item(self, item_id: str) -> bool:
        """Remove an item from the queue."""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                # Only allow removal if not currently processing
                if item.status != QueueItemStatus.PROCESSING:
                    del self.items[i]
                    return True
                return False
        return False

    def remove_items(self, item_ids: List[str]) -> int:
        """Remove multiple items from the queue. Returns count of removed items."""
        count = 0
        for item_id in item_ids:
            if self.remove_item(item_id):
                count += 1
        return count

    def clear_queue(self) -> None:
        """Clear all items from the queue (except currently processing)."""
        self.items = [
            item for item in self.items
            if item.status == QueueItemStatus.PROCESSING
        ]

    def clear_completed(self) -> None:
        """Remove all completed and failed items."""
        self.items = [
            item for item in self.items
            if item.status not in (QueueItemStatus.COMPLETED, QueueItemStatus.FAILED)
        ]

    def get_item(self, item_id: str) -> Optional[QueueItem]:
        """Get a specific queue item by ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def get_next_pending(self) -> Optional[QueueItem]:
        """Get the next pending item to process."""
        for item in self.items:
            if item.status == QueueItemStatus.PENDING:
                return item
        return None

    def update_status(self, item_id: str, status: QueueItemStatus,
                      error_message: Optional[str] = None) -> bool:
        """Update the status of a queue item."""
        item = self.get_item(item_id)
        if item:
            item.status = status
            item.error_message = error_message

            # Update timestamps
            if status == QueueItemStatus.PROCESSING:
                item.start_time = datetime.now()
            elif status in (QueueItemStatus.COMPLETED, QueueItemStatus.FAILED,
                          QueueItemStatus.CANCELLED):
                item.end_time = datetime.now()

            return True
        return False

    def get_statistics(self) -> dict:
        """Get queue statistics."""
        total = len(self.items)
        pending = sum(1 for item in self.items if item.status == QueueItemStatus.PENDING)
        processing = sum(1 for item in self.items if item.status == QueueItemStatus.PROCESSING)
        completed = sum(1 for item in self.items if item.status == QueueItemStatus.COMPLETED)
        failed = sum(1 for item in self.items if item.status == QueueItemStatus.FAILED)
        cancelled = sum(1 for item in self.items if item.status == QueueItemStatus.CANCELLED)

        return {
            'total': total,
            'pending': pending,
            'processing': processing,
            'completed': completed,
            'failed': failed,
            'cancelled': cancelled,
            'remaining': pending + processing
        }

    def __len__(self) -> int:
        """Return number of items in queue."""
        return len(self.items)

    def __iter__(self):
        """Iterate over queue items."""
        return iter(self.items)
