import os
import pickle
import numpy as np
import faiss

from OceanParkBot.src.config.path import DATA_VECTOR, DATA_DIR


class FaissDB:
    def __init__(self, dim=384, index_name="faiss_index.bin"):
        """
        dim: kích thước vector (MiniLM = 384)
        index_name: tên file index
        """

        # Đường dẫn file FAISS index
        self.index_path = os.path.join(DATA_DIR, index_name)

        # File metadata
        self.meta_path = self.index_path + "_meta.pkl"

        self.dim = dim
        self.index = None
        self.metadata = None

    def load_embeddings(self, path=None):
        """
        Load embeddings từ file.pkl trong data/vector_store/
        """
        if path is None:
            path = os.path.join(DATA_VECTOR, "embeddings.pkl")

        print("Loading embeddings from:", path)

        with open(path, "rb") as f:
            data = pickle.load(f)

        return data["embeddings"], data["metadata"]

    def build(self, emb_path=None):
        """
        Build FAISS index từ embeddings.pkl
        """
        print("Loading embeddings...")
        embeddings, metadata = self.load_embeddings(emb_path)

        print("Building FAISS index...")
        self.index = faiss.IndexFlatL2(self.dim)
        self.index.add(embeddings.astype("float32"))

        self.metadata = metadata

        # Tạo thư mục nếu chưa có
        os.makedirs(DATA_DIR, exist_ok=True)

        print("Saving FAISS index to:", self.index_path)
        faiss.write_index(self.index, self.index_path)

        print("Saving metadata to:", self.meta_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)

        print("DONE building FAISS index.")

    def load(self):
        """
        Load FAISS index + metadata
        """
        print("Loading FAISS index:", self.index_path)
        self.index = faiss.read_index(self.index_path)

        print("Loading metadata:", self.meta_path)
        with open(self.meta_path, "rb") as f:
            self.metadata = pickle.load(f)

        print("FAISS index loaded.")

    def search(self, query_vector, top_k=5):
        """
        Trả về top_k căn giống nhất theo embedding
        """
        if self.index is None:
            raise RuntimeError("FAISS index chưa load!")

        D, I = self.index.search(
            np.array([query_vector]).astype("float32"),
            top_k
        )

        results = []
        for idx in I[0]:
            results.append(self.metadata[idx])

        return results


if __name__ == "__main__":
    #build index
    db = FaissDB(dim=384)
    db.build()  #load embeddings từ DATA_VECTOR/embeddings.pkl
