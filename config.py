import json
import os
from pathlib import Path
from typing import Any, Dict


class Config:
    """Application configuration manager."""

    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()

    def _get_config_dir(self) -> Path:
        """Get platform-appropriate config directory."""
        if os.name == 'nt':  # Windows
            base = Path(os.environ.get('APPDATA', '~'))
        else:  # macOS and Linux
            base = Path.home() / 'Library' / 'Application Support'

        config_dir = base / 'DoclingGUI'
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "version": "1.5.2",
            "general": {
                "defaultOutputDir": str(Path.home() / "Documents" / "docling_output"),
                "useLastOutputDir": True,
                "defaultOutputFormat": "md",
                "autoOpenOutputFolder": False,
                "rememberWindowGeometry": True,
                "enableLogging": False,
                "logDirectory": str(Path.home() / "Documents" / "docling_logs")
            },
            "processing": {
                "mode": "online",
                "artifactsPath": str(Path.home() / ".cache" / "docling"),
                "doclingCliPath": "auto"
            },
            "defaults": {
                "pipeline": "standard",
                "ocrEnabled": True,
                "forceOcr": False,
                "ocrEngine": "auto",
                "ocrLanguages": "eng",
                "vlmModel": "smoldocling",
                "imageExportMode": "embedded",
                "tableMode": "accurate",
                "pdfBackend": "dlparse_v2",
                "extractTables": True,
                "enrichCode": False,
                "enrichFormula": False,
                "enrichPictureClasses": False,
                "enrichPictureDescription": False,
                "showLayout": False,
                "debugVisualizeLayout": False,
                "debugVisualizeCells": False,
                "debugVisualizeOcr": False,
                "debugVisualizeTables": False,
                "verbose": 0
            },
            "interface": {
                "theme": "dark",
                "consoleFontSize": 10,
                "sidebarWidth": 320
            },
            "window": {
                "width": 1200,
                "height": 900
            },
            "models": {
                "pipelines": ["standard", "vlm", "asr"],
                "ocr_engines": ["auto", "easyocr", "tesseract", "tesserocr", "rapidocr", "ocrmac"],
                "ocr_languages": {
                    "English": "eng",
                    "German": "deu",
                    "French": "fra",
                    "Spanish": "spa",
                    "Italian": "ita",
                    "Portuguese": "por",
                    "Dutch": "nld",
                    "Polish": "pol",
                    "Russian": "rus",
                    "Chinese (Simplified)": "chi_sim",
                    "Chinese (Traditional)": "chi_tra",
                    "Japanese": "jpn",
                    "Korean": "kor",
                    "Arabic": "ara",
                    "Hindi": "hin",
                    "Turkish": "tur",
                    "Vietnamese": "vie",
                    "Thai": "tha"
                },
                "vlm_models": ["smoldocling", "smoldocling_vllm", "granite_vision", "granite_vision_vllm", "granite_vision_ollama", "got_ocr_2"],
                "asr_models": ["whisper_tiny", "whisper_small", "whisper_medium", "whisper_base", "whisper_large", "whisper_flash", "whisper_turbo"]
            }
        }

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self._get_default_config()
        else:
            return self._get_default_config()

    def save(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, *keys, default=None) -> Any:
        """Get configuration value by key path."""
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, *keys, value):
        """Set configuration value by key path."""
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        self.save()
