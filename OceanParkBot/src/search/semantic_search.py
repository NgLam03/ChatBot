import numpy as np
import pickle
import faiss

from OceanParkBot.src.config.path import (
    path_from_data
)

# Load PhoBERT embedder (đã sửa trong embed_model.py)
from OceanParkBot.src.embedding.embed_model import load_embedding_model


class SemanticSearch:
    def __init__(self, faiss_index_path=None, metadata_path=None):
        """
        Semantic Search sử dụng PhoBERT embedding + FAISS (dim = 768)
        """

        # ==== 1) Load PhoBERT model ====
        print(">>> Loading PhoBERT embedder...")
        self.model = load_embedding_model()     # PhoBERTEmbedder()

        # ==== 2) FAISS paths ====
        if faiss_index_path is None:
            faiss_index_path = path_from_data("faiss_index.bin")

        if metadata_path is None:
            metadata_path = path_from_data("faiss_index.bin_meta.pkl")

        # ==== 3) Load FAISS index ====
        print(">>> Loading FAISS index:", faiss_index_path)
        self.index = faiss.read_index(faiss_index_path)

        # ==== 4) Load metadata ====
        print(">>> Loading metadata:", metadata_path)
        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def encode_query(self, text: str):
        """
        Encode text bằng PhoBERT → vector numpy (float32, shape 768)
        """
        vec = self.model.encode(text)
        return vec.astype("float32")

    def search(self, text: str, top_k=10):
        """
        Trả về top-k căn hộ gần nghĩa nhất
        """

        # ==== 1) Encode ====
        query_vec = self.encode_query(text)

        # FAISS yêu cầu shape = (1, dim)
        query_vec = np.array([query_vec], dtype="float32")

        # ==== 2) Search ====
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < 0:
                continue

            item = dict(self.metadata[idx])
            item["score"] = float(dist)
            results.append(item)

        return results


if __name__ == "__main__":
    search = SemanticSearch()
    q = "tìm căn 2 ngủ view vinuni dưới 9tr"
    res = search.search(q, top_k=5)

    for r in res:
        print(r["ms"], r["price"], r["score"])
