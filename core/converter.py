import subprocess
import threading
import sys
import os
from pathlib import Path
from typing import Callable, Optional, List
import shutil


class DoclingConverter:
    """Handles Docling document conversion operations."""

    def __init__(self):
        self.current_process: Optional[subprocess.Popen] = None
        self.is_running = False
        self.docling_path = self._get_docling_path()

    def _get_docling_path(self) -> str:
        """Get the correct docling executable path from virtual environment."""
        # First priority: Use venv's docling if we're in a venv
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            # We're in a virtual environment
            venv_bin = Path(sys.prefix) / 'bin' / 'docling'
            if venv_bin.exists():
                return str(venv_bin)

        # Second priority: Look for docling in the same directory as python
        python_dir = Path(sys.executable).parent
        docling_in_python_dir = python_dir / 'docling'
        if docling_in_python_dir.exists():
            return str(docling_in_python_dir)

        # Fall back to system PATH
        docling_in_path = shutil.which('docling')
        if docling_in_path:
            return docling_in_path

        # Default fallback
        return 'docling'

    def check_docling_installed(self) -> bool:
        """Check if Docling CLI is available."""
        try:
            # Try to import docling first
            import docling
            return True
        except ImportError:
            # Check if docling executable exists
            return os.path.exists(self.docling_path) or shutil.which('docling') is not None

    def check_models_downloaded(self, artifacts_path: str) -> tuple[bool, list[str]]:
        """
        Check if required models are downloaded for offline operation.

        Args:
            artifacts_path: Path to model artifacts directory

        Returns:
            Tuple of (all_found: bool, missing_files: list[str])
        """
        artifacts_dir = Path(artifacts_path)

        # Required model files for standard pipeline
        required_files = [
            "model.safetensors",  # Layout model
            "config.json",        # Model config
        ]

        missing_files = []

        for file in required_files:
            file_path = artifacts_dir / file
            if not file_path.exists():
                missing_files.append(file)

        return (len(missing_files) == 0, missing_files)

    def build_command(
        self,
        input_path: str,
        output_format: str,
        output_dir: str,
        processing_mode: str,
        ocr_enabled: bool,
        force_ocr: bool = False,
        pipeline: str = "standard",
        image_export_mode: str = "embedded",
        table_mode: str = "accurate",
        artifacts_path: Optional[str] = None,
        ocr_lang: Optional[str] = None,
        enrich_formula: bool = False,
        enrich_picture_classes: bool = False,
        enrich_picture_description: bool = False,
        verbose: int = 0,
        **kwargs
    ) -> List[str]:
        """Build Docling command from parameters."""
        cmd = [self.docling_path, input_path]

        # Output settings
        cmd.extend(["--to", output_format])
        cmd.extend(["--output", output_dir])

        # Pipeline
        if pipeline != "standard":
            cmd.extend(["--pipeline", pipeline])

        # OCR options
        if ocr_enabled:
            cmd.append("--ocr")
            if force_ocr:
                cmd.append("--force-ocr")
        else:
            cmd.append("--no-ocr")

        # OCR language
        if ocr_lang and ocr_lang.strip():
            cmd.extend(["--ocr-lang", ocr_lang.strip()])

        # Image export mode
        cmd.extend(["--image-export-mode", image_export_mode])

        # Table mode
        if table_mode != "accurate":
            cmd.extend(["--table-mode", table_mode])

        # Enrichment options
        if enrich_formula:
            cmd.append("--enrich-formula")

        if enrich_picture_classes:
            cmd.append("--enrich-picture-classes")

        if enrich_picture_description:
            cmd.append("--enrich-picture-description")

        # Verbose mode
        if verbose == 1:
            cmd.append("-v")
        elif verbose >= 2:
            cmd.append("-vv")

        # Artifacts path (for offline mode)
        if artifacts_path:
            cmd.extend(["--artifacts-path", artifacts_path])

        return cmd

    def convert(
        self,
        input_path: str,
        output_format: str,
        output_dir: str,
        processing_mode: str,
        ocr_enabled: bool,
        force_ocr: bool = False,
        pipeline: str = "standard",
        image_export_mode: str = "embedded",
        table_mode: str = "accurate",
        artifacts_path: Optional[str] = None,
        ocr_lang: Optional[str] = None,
        enrich_formula: bool = False,
        enrich_picture_classes: bool = False,
        enrich_picture_description: bool = False,
        verbose: int = 0,
        on_output: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[int], None]] = None,
        on_error: Optional[Callable[[str], None]] = None
    ):
        """
        Convert document using Docling.

        Args:
            input_path: Path to input file
            output_format: Output format (md, json, html, text, doctags)
            output_dir: Output directory path
            processing_mode: "online" or "offline"
            ocr_enabled: Enable OCR
            force_ocr: Force OCR (replace existing text)
            pipeline: Processing pipeline (standard, vlm, asr)
            image_export_mode: Image handling (embedded, placeholder, referenced)
            table_mode: Table extraction mode (accurate, fast)
            artifacts_path: Path to model artifacts (for offline mode)
            ocr_lang: OCR language codes (comma-separated, e.g., "eng,deu,fra")
            enrich_formula: Enable formula enrichment
            enrich_picture_classes: Enable picture classification
            enrich_picture_description: Enable picture description
            verbose: Verbosity level (0=normal, 1=-v, 2=-vv)
            on_output: Callback for stdout/stderr output
            on_complete: Callback for completion (receives return code)
            on_error: Callback for errors
        """
        if self.is_running:
            if on_error:
                on_error("Conversion already in progress")
            return

        # Build command
        cmd = self.build_command(
            input_path=input_path,
            output_format=output_format,
            output_dir=output_dir,
            processing_mode=processing_mode,
            ocr_enabled=ocr_enabled,
            force_ocr=force_ocr,
            pipeline=pipeline,
            image_export_mode=image_export_mode,
            table_mode=table_mode,
            artifacts_path=artifacts_path if processing_mode == "offline" else None,
            ocr_lang=ocr_lang,
            enrich_formula=enrich_formula,
            enrich_picture_classes=enrich_picture_classes,
            enrich_picture_description=enrich_picture_description,
            verbose=verbose
        )

        # Run in separate thread
        def run_conversion():
            self.is_running = True
            try:
                if on_output:
                    on_output(f"Executing: {' '.join(cmd)}\n")

                # Start process
                self.current_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )

                # Read output line by line
                if self.current_process.stdout:
                    for line in self.current_process.stdout:
                        if on_output:
                            on_output(line)

                # Wait for completion
                return_code = self.current_process.wait()

                if on_complete:
                    on_complete(return_code)

            except FileNotFoundError:
                error_msg = "Docling CLI not found. Please install it: pip install docling"
                if on_error:
                    on_error(error_msg)
                if on_output:
                    on_output(f"\nERROR: {error_msg}\n")
            except Exception as e:
                error_msg = f"Conversion error: {str(e)}"
                if on_error:
                    on_error(error_msg)
                if on_output:
                    on_output(f"\nERROR: {error_msg}\n")
            finally:
                self.is_running = False
                self.current_process = None

        thread = threading.Thread(target=run_conversion, daemon=True)
        thread.start()

    def cancel(self):
        """Cancel current conversion."""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            finally:
                self.current_process = None
                self.is_running = False

    def download_models(
        self,
        download_all: bool = True,
        download_smoldocling: bool = False,
        download_smolvlm: bool = False,
        on_output: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[int], None]] = None,
        on_error: Optional[Callable[[str], None]] = None
    ):
        """
        Download models for offline operation.

        Args:
            download_all: If True, run 'docling-tools models download'
            download_smoldocling: If True, download SmolDocling model
            download_smolvlm: If True, download SmolVLM model
            on_output: Callback for stdout/stderr output
            on_complete: Callback for completion (receives return code)
            on_error: Callback for errors
        """
        if self.is_running:
            if on_error:
                on_error("Conversion already in progress. Cannot download models now.")
            return

        def run_download():
            self.is_running = True
            total_return_code = 0

            try:
                # Download all models
                if download_all:
                    if on_output:
                        on_output("\n" + "="*60 + "\n")
                        on_output("Downloading all required models...\n")
                        on_output("="*60 + "\n")

                    cmd = ["docling-tools", "models", "download"]
                    if on_output:
                        on_output(f"Executing: {' '.join(cmd)}\n\n")

                    self.current_process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1,
                        universal_newlines=True
                    )

                    if self.current_process.stdout:
                        for line in self.current_process.stdout:
                            if on_output:
                                on_output(line)

                    return_code = self.current_process.wait()
                    if return_code != 0:
                        total_return_code = return_code
                        if on_output:
                            on_output(f"\n[WARNING] Model download returned code {return_code}\n")

                # Download SmolDocling model
                if download_smoldocling:
                    if on_output:
                        on_output("\n" + "="*60 + "\n")
                        on_output("Downloading SmolDocling-256M model...\n")
                        on_output("="*60 + "\n")

                    cmd = ["docling-tools", "models", "download-hf-repo", "ds4sd/SmolDocling-256M-preview"]
                    if on_output:
                        on_output(f"Executing: {' '.join(cmd)}\n\n")

                    self.current_process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1,
                        universal_newlines=True
                    )

                    if self.current_process.stdout:
                        for line in self.current_process.stdout:
                            if on_output:
                                on_output(line)

                    return_code = self.current_process.wait()
                    if return_code != 0:
                        total_return_code = return_code
                        if on_output:
                            on_output(f"\n[WARNING] SmolDocling download returned code {return_code}\n")

                # Download SmolVLM model
                if download_smolvlm:
                    if on_output:
                        on_output("\n" + "="*60 + "\n")
                        on_output("Downloading SmolVLM-256M-Instruct model...\n")
                        on_output("="*60 + "\n")

                    cmd = ["docling-tools", "models", "download-hf-repo", "HuggingFaceTB/SmolVLM-256M-Instruct"]
                    if on_output:
                        on_output(f"Executing: {' '.join(cmd)}\n\n")

                    self.current_process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        bufsize=1,
                        universal_newlines=True
                    )

                    if self.current_process.stdout:
                        for line in self.current_process.stdout:
                            if on_output:
                                on_output(line)

                    return_code = self.current_process.wait()
                    if return_code != 0:
                        total_return_code = return_code
                        if on_output:
                            on_output(f"\n[WARNING] SmolVLM download returned code {return_code}\n")

                if on_output:
                    on_output("\n" + "="*60 + "\n")
                    if total_return_code == 0:
                        on_output("[SUCCESS] Model download completed!\n")
                    else:
                        on_output("[COMPLETED] Model download finished with warnings.\n")
                    on_output("="*60 + "\n")

                if on_complete:
                    on_complete(total_return_code)

            except FileNotFoundError:
                error_msg = "docling-tools command not found. Please ensure Docling is installed: pip install docling"
                if on_error:
                    on_error(error_msg)
                if on_output:
                    on_output(f"\nERROR: {error_msg}\n")
            except Exception as e:
                error_msg = f"Model download error: {str(e)}"
                if on_error:
                    on_error(error_msg)
                if on_output:
                    on_output(f"\nERROR: {error_msg}\n")
            finally:
                self.is_running = False
                self.current_process = None

        thread = threading.Thread(target=run_download, daemon=True)
        thread.start()
