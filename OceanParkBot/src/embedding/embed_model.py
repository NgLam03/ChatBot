# from sentence_transformers import SentenceTransformer

# def load_embedding_model():
#     """
#     Load embedding model (MiniLM).
#     """
#     model_name = "sentence-transformers/all-MiniLM-L6-v2"
#     model = SentenceTransformer(model_name)
#     return model

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel

class PhoBERTEmbedder:
    def __init__(self, model_name="vinai/phobert-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()

    def encode(self, text: str):
        """Encode text thành embedding vector."""
        tokens = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
        
        with torch.no_grad():
            outputs = self.model(**tokens)

        # Mean pooling
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze()
        return embedding.numpy()


def load_embedding_model():
    """
    Trả về PhoBERT embedder.
    """
    return PhoBERTEmbedder()
