import json
import os
import numpy as np

from .embed_model import load_embedding_model
from OceanParkBot.src.config.path import DATA_CLEANED, DATA_VECTOR, path_from_data

def load_cleaned_data(path=None):
    """Load dữ liệu đã clean."""
    if path is None:
        path = os.path.join(DATA_CLEANED, "listings_clean.json")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_embedding_data(embeddings, metadata, out_path=None):
    """Lưu vector + metadata thành file PKL."""
    import pickle
    if out_path is None:
        out_path = os.path.join(DATA_VECTOR, "embeddings.pkl")
        
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "wb") as f:
        pickle.dump({"embeddings": embeddings, "metadata": metadata}, f)

    print("Saved embedding data to:", out_path)


def generate_embeddings():
    print("Loading MiniLM model...")
    model = load_embedding_model()

    print("Loading cleaned listings...")
    listings = load_cleaned_data()

    embeddings = []
    metadata = []

    print(f"Generating embedding for {len(listings)} listings...")

    for item in listings:
        text = item["text_for_embedding"]
        vector = model.encode(text)

        embeddings.append(vector)
        metadata.append(item)

    embeddings = np.array(embeddings)

    # Lưu outputs
    save_embedding_data(embeddings, metadata)

    print("DONE generating embeddings!")


if __name__ == "__main__":
    generate_embeddings()
