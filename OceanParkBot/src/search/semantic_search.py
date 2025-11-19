import numpy as np
import pickle
import faiss
from sentence_transformers import SentenceTransformer

from OceanParkBot.src.config.path import (
    DATA_VECTOR,
    DATA_DIR,
    path_from_data
)


class SemanticSearch:
    def __init__(self, embedding_model_path=None, faiss_index_path=None, metadata_path=None):
        """
        embedding_model_path: tên model SBERT
        faiss_index_path: đường dẫn tới faiss_index.bin
        metadata_path: pickle chứa metadata
        """

        # 1. Load SBERT embedding model
        model_name = embedding_model_path or "sentence-transformers/all-MiniLM-L6-v2"
        self.model = SentenceTransformer(model_name)

        # 2. Đường dẫn FAISS index
        if faiss_index_path is None:
            faiss_index_path = path_from_data("faiss_index.bin")

        # 3. Đường dẫn metadata
        if metadata_path is None:
            metadata_path = path_from_data("faiss_index.bin_meta.pkl")

        # Load FAISS index
        print(">>> Loading FAISS index from:", faiss_index_path)
        self.index = faiss.read_index(faiss_index_path)

        # Load metadata
        print(">>> Loading metadata from:", metadata_path)
        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def encode_query(self, text: str):
        """Embedding câu hỏi user"""
        return np.array(self.model.encode([text])[0]).astype("float32")

    def search(self, text: str, top_k=10):
        """
        Trả về top-k căn hộ giống nhất theo FAISS
        """
        query_vec = self.encode_query(text)

        # Search trong FAISS
        distances, indices = self.index.search(
            np.array([query_vec]),
            top_k
        )

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < 0:
                continue

            meta = dict(self.metadata[idx])  # copy để không ghi đè
            meta["score"] = float(dist)
            results.append(meta)

        return results


if __name__ == "__main__":
    searcher = SemanticSearch()

    q = "tìm căn 2 ngủ full đồ dưới 10tr view VinUni"
    results = searcher.search(q, top_k=5)

    for item in results:
        print(item.get("ms"), item.get("price"), item.get("text_for_embedding", "")[:60], "score:", item["score"])
