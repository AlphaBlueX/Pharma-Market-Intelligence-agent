import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any
from backend.config import config

class VectorDB:
    def __init__(self):
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2
        self.index_path = config.VECTOR_DB_PATH
        self.metadata_path = f"{config.VECTOR_DB_PATH}_metadata.pkl"
        
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

    def add_document(self, vector: np.ndarray, doc_metadata: Dict[str, Any]):
        self.index.add(np.array([vector]).astype('float32'))
        self.metadata.append(doc_metadata)
        self.save()

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        distances, indices = self.index.search(np.array([query_vector]).astype('float32'), k)
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                res = self.metadata[idx].copy()
                res['distance'] = float(distances[0][i])
                results.append(res)
        return results

    def save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)

vectordb = VectorDB()
