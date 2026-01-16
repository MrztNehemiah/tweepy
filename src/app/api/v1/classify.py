from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.data import tweet_data
from app.config import UPLOAD_DIR, DOWNLOAD_DIR
import os
from google.genai import errors
from app.services.ai_client import gemini
from app.services.batching import BatchToken
from app.services.checkpoint import load_checkpoint, save_checkpoint
import random
import time

classify_router = APIRouter()

# data = tweet_data(UPLOAD_DIR)


@classify_router.get("/classify")
async def classify_tweet(file_name):
    file_path = os.path.join(UPLOAD_DIR, file_name)
    if not os.path.exists(file_path):
        return f"File '{file_path}' not found, re-upload file"
    # file_path = f"../data/upload/{file_name}"
    try:
        data = tweet_data(file_path)
        batch_token = BatchToken(data, 10000)
        batches = batch_token.batch()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to load or batch data: {str(e)}"
        )
    download_path = os.path.join(DOWNLOAD_DIR, f"processed_{file_name}")

    checkpoint = load_checkpoint()

    for batch in range(len(batches)):
        # Fix 1: Compare batch_id correctly
        if batch <= checkpoint:
            print(
                f"Batch {batches[batch]['batch_id']} already processed, moving to next batch"
            )
            continue

        # Fix 2: Wrap the retry logic around the actual API call
        success = False
        retry = 5
        base_delay = 5

        for attempt in range(1, retry + 1):
            try:
                result = gemini(batches[batch]["texts"])

                with open(download_path, "a", encoding="utf-8") as fh:
                    fh.write(str(result.text) + "\n")
                # print(result)
                save_checkpoint(batch)
                success = True
                break  # Exit retry loop on success

            except errors.APIError as err:  # (TimeoutError, ConnectionError)
                print(f"Attempt {attempt} failed: {err}")

                # If this was the last attempt, log and move on (or raise)
                if attempt == retry:
                    print(
                        f"Batch {batches[batch]['batch_id']} failed after {retry} attempts"
                    )
                    # Option A: Skip this batch and continue
                    break
                    # Option B: Raise exception to stop entire pipeline
                    # raise

                # Calculate delay with exponential backoff and jitter
                delay = base_delay * (2 ** (attempt - 1))
                jitter = random.uniform(0, 0.3)
                delay += jitter
                print(f"Retrying in {delay:.2f}s...")
                time.sleep(delay)

            # except errors.ClientError as e:
            #     print("Rate limit exceeded", e)
            # # Handle rate limit
            # except errors.ServerError as e:
            #     print(f"Server error: {e}")

            # except Exception as err:
            #     print(f"some Error: {err}")

        # Optional: Handle failed batches
        if not success:
            print(
                f"Skipping batch {batches[batch]['batch_id']} due to persistent errors"
            )

    return FileResponse(
        path=download_path,
        filename=f"processed_{file_name}",
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename=processed_{file_name}",
        },
    )
