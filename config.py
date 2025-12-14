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
            "version": "1.5.6",
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
                "vlmModel": "granite_docling",
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
                "vlm_models": ["granite_docling", "granite_docling_vllm", "smoldocling", "smoldocling_vllm", "granite_vision", "granite_vision_vllm", "granite_vision_ollama", "got_ocr_2"],
                "asr_models": ["whisper_tiny", "whisper_small", "whisper_medium", "whisper_base", "whisper_large", "whisper_flash", "whisper_turbo"],
                "downloadable_models": {
                    "docling": {
                        "title": "Docling Models",
                        "command": "download",
                        "models": [
                            {"name": "layout", "description": "Layout analysis model"},
                            {"name": "tableformer", "description": "Table structure recognition"},
                            {"name": "code_formula", "description": "Code and formula detection"},
                            {"name": "picture_classifier", "description": "Picture classification"},
                            {"name": "smolvlm", "description": "SmolVLM vision-language model"},
                            {"name": "granitedocling", "description": "Granite Docling model"},
                            {"name": "granitedocling_mlx", "description": "Granite Docling (MLX/Apple Silicon)"},
                            {"name": "smoldocling", "description": "SmolDocling model"},
                            {"name": "smoldocling_mlx", "description": "SmolDocling (MLX/Apple Silicon)"},
                            {"name": "granite_vision", "description": "Granite Vision model"},
                            {"name": "rapidocr", "description": "RapidOCR engine"},
                            {"name": "easyocr", "description": "EasyOCR engine"}
                        ]
                    },
                    "huggingface": {
                        "title": "Huggingface Models",
                        "command": "download-hf-repo",
                        "models": [
                            {"name": "ds4sd/SmolDocling-256M-preview", "description": "SmolDocling 256M preview"},
                            {"name": "HuggingFaceTB/SmolVLM-256M-Instruct", "description": "SmolVLM 256M Instruct"}
                        ]
                    }
                }
            }
        }

    def _merge_configs(self, default: Dict, saved: Dict) -> Dict:
        """Recursively merge saved config into default config.

        This ensures new default keys are added while preserving user settings.
        For lists (like model lists), always use the default to get updates.
        """
        result = default.copy()
        for key, value in saved.items():
            if key in result:
                if isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._merge_configs(result[key], value)
                elif isinstance(result[key], list):
                    # For lists like model options, always use defaults to get updates
                    pass
                else:
                    # Use saved value for non-dict, non-list values
                    result[key] = value
            else:
                result[key] = value
        return result

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        defaults = self._get_default_config()
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    saved = json.load(f)
                # Merge saved config with defaults to pick up new keys
                merged = self._merge_configs(defaults, saved)
                return merged
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return defaults
        else:
            return defaults

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
