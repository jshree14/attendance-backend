import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# For development, allow default key. In production, require SECRET_KEY env var
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-use-openssl-rand-hex-32")
if SECRET_KEY == "dev-secret-key-change-in-production-use-openssl-rand-hex-32":
    print("WARNING: Using default SECRET_KEY. Set SECRET_KEY environment variable for production!")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
