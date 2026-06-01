from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SAMPLES_DIR = DATA_DIR / "samples"

SUPPORTED_EXTENSIONS = {".txt", ".md"}
DEFAULT_CONFIDENCE = 0.75
