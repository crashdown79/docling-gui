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
        models_dir = artifacts_dir / "models"

        # Check if models directory exists
        if not models_dir.exists():
            return (False, ["models directory not found"])

        # Required models for standard pipeline (minimum needed)
        required_models = [
            "docling-project--docling-layout-heron",  # Layout detection model
        ]

        missing_models = []

        for model_name in required_models:
            model_path = models_dir / model_name
            model_file = model_path / "model.safetensors"
            config_file = model_path / "config.json"

            if not model_path.exists():
                missing_models.append(f"{model_name} (directory not found)")
            elif not model_file.exists():
                missing_models.append(f"{model_name}/model.safetensors")
            elif not config_file.exists():
                missing_models.append(f"{model_name}/config.json")

        return (len(missing_models) == 0, missing_models)

    def check_ocr_engine_available(self, engine: str) -> tuple[bool, str]:
        """
        Check if a specific OCR engine is available on the system.

        Args:
            engine: OCR engine name (auto, easyocr, tesseract, rapidocr, ocrmac, tesserocr)

        Returns:
            Tuple of (is_available: bool, error_message: str)
        """
        if engine == "auto" or engine == "easyocr":
            # easyocr is Python-based and included with docling
            return (True, "")

        if engine == "tesseract":
            # Check if tesseract command is available
            if shutil.which('tesseract'):
                return (True, "")
            else:
                return (False,
                    "Tesseract is not installed.\n\n"
                    "To install:\n"
                    "  macOS: brew install tesseract\n"
                    "  Ubuntu/Debian: sudo apt-get install tesseract-ocr\n"
                    "  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki\n\n"
                    "Or select a different OCR engine like 'easyocr' or 'rapidocr'.")

        if engine == "tesserocr":
            # Check if tesserocr Python package is available
            try:
                import tesserocr
                return (True, "")
            except ImportError:
                return (False,
                    "TesserOCR Python package is not installed.\n\n"
                    "To install:\n"
                    "  pip install tesserocr\n\n"
                    "Note: tesserocr requires tesseract to be installed first.\n"
                    "Or select a different OCR engine like 'easyocr' or 'rapidocr'.")

        if engine == "rapidocr":
            # Check if rapidocr Python package is available
            try:
                import rapidocr_onnxruntime
                return (True, "")
            except ImportError:
                return (False,
                    "RapidOCR is not installed.\n\n"
                    "To install:\n"
                    "  pip install rapidocr-onnxruntime\n\n"
                    "Or select a different OCR engine like 'easyocr' or 'tesseract'.")

        if engine == "ocrmac":
            # ocrmac only works on macOS
            if sys.platform != "darwin":
                return (False,
                    "OCRmac only works on macOS.\n\n"
                    "Please select a different OCR engine like 'easyocr' or 'tesseract'.")
            # Check if ocrmac package is available
            try:
                import ocrmac
                return (True, "")
            except ImportError:
                return (False,
                    "OCRmac is not installed.\n\n"
                    "To install:\n"
                    "  pip install ocrmac\n\n"
                    "Or select a different OCR engine like 'easyocr' or 'tesseract'.")

        # Unknown engine
        return (True, "")  # Don't block unknown engines

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
        pdf_backend: str = "dlparse_v4",
        pdf_password: Optional[str] = None,
        table_mode: str = "accurate",
        artifacts_path: Optional[str] = None,
        ocr_lang: Optional[str] = None,
        ocr_engine: str = "auto",
        vlm_model: Optional[str] = None,
        extract_tables: bool = True,
        enrich_code: bool = False,
        enrich_formula: bool = False,
        enrich_picture_classes: bool = False,
        enrich_picture_description: bool = False,
        show_layout: bool = False,
        debug_visualize_layout: bool = False,
        debug_visualize_cells: bool = False,
        debug_visualize_ocr: bool = False,
        debug_visualize_tables: bool = False,
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

        # VLM Model (when pipeline=vlm)
        if pipeline == "vlm" and vlm_model:
            cmd.extend(["--vlm-model", vlm_model])

        # PDF Backend
        if pdf_backend and pdf_backend != "dlparse_v4":
            cmd.extend(["--pdf-backend", pdf_backend])

        # PDF Password (for protected documents)
        if pdf_password:
            cmd.extend(["--pdf-password", pdf_password])

        # OCR options
        if ocr_enabled:
            cmd.append("--ocr")
            if force_ocr:
                cmd.append("--force-ocr")
        else:
            cmd.append("--no-ocr")

        # OCR engine
        if ocr_engine and ocr_engine != "auto":
            cmd.extend(["--ocr-engine", ocr_engine])

        # OCR language
        if ocr_lang and ocr_lang.strip():
            cmd.extend(["--ocr-lang", ocr_lang.strip()])

        # Image export mode
        cmd.extend(["--image-export-mode", image_export_mode])

        # Table options
        if not extract_tables:
            cmd.append("--no-tables")

        if table_mode != "accurate":
            cmd.extend(["--table-mode", table_mode])

        # Enrichment options
        if enrich_code:
            cmd.append("--enrich-code")

        if enrich_formula:
            cmd.append("--enrich-formula")

        if enrich_picture_classes:
            cmd.append("--enrich-picture-classes")

        if enrich_picture_description:
            cmd.append("--enrich-picture-description")

        # Debug visualization options
        if show_layout:
            cmd.append("--show-layout")

        if debug_visualize_layout:
            cmd.append("--debug-visualize-layout")

        if debug_visualize_cells:
            cmd.append("--debug-visualize-cells")

        if debug_visualize_ocr:
            cmd.append("--debug-visualize-ocr")

        if debug_visualize_tables:
            cmd.append("--debug-visualize-tables")

        # Verbose mode
        if verbose == 1:
            cmd.append("-v")
        elif verbose >= 2:
            cmd.append("-vv")

        # Artifacts path (for offline mode)
        if artifacts_path:
            # Models are in 'models' subdirectory
            models_path = str(Path(artifacts_path) / "models")
            cmd.extend(["--artifacts-path", models_path])

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
        pdf_backend: str = "dlparse_v4",
        pdf_password: Optional[str] = None,
        table_mode: str = "accurate",
        artifacts_path: Optional[str] = None,
        ocr_lang: Optional[str] = None,
        ocr_engine: str = "auto",
        vlm_model: Optional[str] = None,
        extract_tables: bool = True,
        enrich_code: bool = False,
        enrich_formula: bool = False,
        enrich_picture_classes: bool = False,
        enrich_picture_description: bool = False,
        show_layout: bool = False,
        debug_visualize_layout: bool = False,
        debug_visualize_cells: bool = False,
        debug_visualize_ocr: bool = False,
        debug_visualize_tables: bool = False,
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
            pdf_backend: PDF processing backend (dlparse_v4, dlparse_v2, dlparse_v1, pypdfium2)
            pdf_password: Password for protected PDF documents
            table_mode: Table extraction mode (accurate, fast)
            artifacts_path: Path to model artifacts (for offline mode)
            ocr_lang: OCR language codes (comma-separated, e.g., "eng,deu,fra")
            ocr_engine: OCR engine (auto, easyocr, tesseract, rapidocr, ocrmac, tesserocr)
            vlm_model: VLM model choice (for vlm pipeline)
            extract_tables: Enable table extraction
            enrich_code: Enable code enrichment
            enrich_formula: Enable formula enrichment
            enrich_picture_classes: Enable picture classification
            enrich_picture_description: Enable picture description
            show_layout: Show layout bounding boxes
            debug_visualize_layout: Visualize layout clusters
            debug_visualize_cells: Visualize PDF cells
            debug_visualize_ocr: Visualize OCR cells
            debug_visualize_tables: Visualize table cells
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
            pdf_backend=pdf_backend,
            pdf_password=pdf_password,
            table_mode=table_mode,
            artifacts_path=artifacts_path if processing_mode == "offline" else None,
            ocr_lang=ocr_lang,
            ocr_engine=ocr_engine,
            vlm_model=vlm_model,
            extract_tables=extract_tables,
            enrich_code=enrich_code,
            enrich_formula=enrich_formula,
            enrich_picture_classes=enrich_picture_classes,
            enrich_picture_description=enrich_picture_description,
            show_layout=show_layout,
            debug_visualize_layout=debug_visualize_layout,
            debug_visualize_cells=debug_visualize_cells,
            debug_visualize_ocr=debug_visualize_ocr,
            debug_visualize_tables=debug_visualize_tables,
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
