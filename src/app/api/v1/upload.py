from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import ALLOWED_EXTENSIONS, UPLOAD_DIR, MAX_FILE_SIZE
from app.utils.file_utils import sanitize_filename
from pathlib import Path

upload_router = APIRouter()


@upload_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Validate filename
        safe_filename = sanitize_filename(file.filename)

        # Check file extension
        file_ext = Path(safe_filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}",
            )

        # Prepare destination
        destination = UPLOAD_DIR / safe_filename

        # Check if file already exists
        # if destination.exists():
        #     raise HTTPException(status_code=409, detail="File already exists")

        # Save file with size limit check
        with open(destination, "wb") as fh:  # Use "wb" for binary mode
            file_size = 0
            while chunk := await file.read(8192):  # Read in chunks
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE:
                    fh.close()
                    destination.unlink()  # Delete partial file
                    raise HTTPException(
                        status_code=413,
                        detail=f"File too large. Max size: {MAX_FILE_SIZE} bytes",
                    )
                fh.write(chunk)

        return {
            "filename": safe_filename,
            "size": file_size,
            "location": str(destination),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed{str(e)}")
