# data_transform.py
import prefect
from prefect import task
import re
import pandas as pd



@task
def transform_news(raw_data: list[dict]) -> pd.DataFrame:
    """
    Transform raw news data into a clean dataframe.
    Expects input: list of dicts with keys 'title', 'publishedDate', etc.
    """
    df = pd.DataFrame(raw_data)

    if "title" not in df.columns:
        raise ValueError("Expected 'title' column in raw data")
    
    def clean_headline(text: str) -> str:
        """Remove special characters, lower case, and strip extra spaces."""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)  # keep only letters, numbers, spaces
        text = re.sub(r"\s+", " ", text)  # collapse multiple spaces
        return text.strip()

    # Clean titles
    df["clean_title"] = df["title"].astype(str).apply(clean_headline)

    # Drop duplicates
    df = df.drop_duplicates(subset="clean_title")

    return df
