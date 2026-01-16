from pathlib import Path


# Directory settings
UPLOAD_DIR = Path("../data/input")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

DOWNLOAD_DIR = Path("../data/output")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# File upload constraints
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".js", ".json"}

# CORS settings
CORS_ORIGINS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]
