from sentence_transformers import SentenceTransformer
from backend.config import config

class Embedder:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Embedder, cls).__new__(cls)
            cls._instance.model = SentenceTransformer(config.EMBEDDING_MODEL)
        return cls._instance

    def get_embeddings(self, text: str):
        return self.model.encode(text)

embedder = Embedder()
