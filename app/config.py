import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT / 'data' / 'customers.db'}")
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", str(ROOT / "data" / "chroma")))
POLICY_DIR = Path(os.getenv("POLICY_DIR", str(ROOT / "documents")))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
