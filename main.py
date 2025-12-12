#!/usr/bin/env python3
"""
Docling GUI - A graphical user interface for the Docling document converter.

This application provides an easy-to-use interface for converting various
document formats (PDF, DOCX, PPTX, HTML, images, etc.) to different output
formats (Markdown, JSON, HTML, text) using the Docling library.
"""

import sys
from ui.main_window import MainWindow


def main():
    """Main entry point for the application."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
