import google.genai as genai
from dotenv import load_dotenv
from app.schemas.classify import ClassificationResult
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def gemini(text):
    text_to_classify = text
    prompt = f"""
            Classify the following list of texts. 
            Use the provided schema for the output.

            TEXTS: {text_to_classify}
                """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ClassificationResult,  # Pass the Pydantic model directly
            "temperature": 0.0,  # Keep it deterministic
        },
    )
    return response
