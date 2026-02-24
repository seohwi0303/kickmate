from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]  # kickmate/
ENV_PATH = ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(f"DATABASE_URL not found. Looked for .env at: {ENV_PATH}")