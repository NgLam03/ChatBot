import os
import pickle
import numpy as np
import faiss


class FaissDB:
    def __init__(self, dim=384, index_path="data/faiss_index.bin"):
        self.dim = dim
        self.index_path = index_path
        self.index = None
        self.metadata = None

    def load_embeddings(self, path="data/vector_store/embeddings.pkl"):
        with open(path, "rb") as f:
            data = pickle.load(f)
        return data["embeddings"], data["metadata"]

    def build(self, emb_path="data/vector_store/embeddings.pkl"):
        print(">>> Loading embeddings...")
        embeddings, metadata = self.load_embeddings(emb_path)

        print(">>> Building FAISS index...")
        self.index = faiss.IndexFlatL2(self.dim)
        self.index.add(embeddings.astype("float32"))

        self.metadata = metadata

        print(">>> Saving FAISS index...")
        faiss.write_index(self.index, self.index_path)

        with open(self.index_path + "_meta.pkl", "wb") as f:
            pickle.dump(self.metadata, f)

        print(">>> DONE building FAISS index.")

    def load(self):
        print(">>> Loading FAISS index...")
        self.index = faiss.read_index(self.index_path)

        with open(self.index_path + "_meta.pkl", "rb") as f:
            self.metadata = pickle.load(f)

        print(">>> FAISS index loaded.")

    def search(self, query_vector, top_k=5):
        """Trả về top_k căn giống nhất theo embedding."""
        D, I = self.index.search(np.array([query_vector]).astype("float32"), top_k)

        results = []
        for idx in I[0]:
            results.append(self.metadata[idx])

        return results
