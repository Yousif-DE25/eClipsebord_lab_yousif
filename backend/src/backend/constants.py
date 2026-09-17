# LLM-genererad kod
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

SOLAR_CSV = DATA_DIR / "solar.csv"
LUNAR_CSV = DATA_DIR / "lunar.csv"
