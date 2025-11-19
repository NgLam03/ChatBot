from sentence_transformers import SentenceTransformer

def load_embedding_model():
    """
    Load embedding model (MiniLM).
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)
    return model
