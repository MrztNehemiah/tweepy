from pydantic import BaseModel, Field
from typing import List


class SingleClassification(BaseModel):
    """Classification for a single text item."""

    text: str = Field(description="The text being classified")
    sentiment: str = Field(
        description="The primary sentiment, must be one of 'Positive', 'Negative', or 'Neutral'."
    )


class ClassificationResult(BaseModel):
    """A Pydantic model for the classification output."""

    results: List[SingleClassification] = Field(
        description="List of classification results for each text"
    )
