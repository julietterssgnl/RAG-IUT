from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict
import os

class VectorStore:
    """
    Classe responsable de la vectorisation et du stockage des documents.
    """
    
    def __init__(self, collection_name: str = "documents"):
        """
        Initialise la base de données vectorielle.
        
        Args:
            collection_name (str): Nom de la collection dans ChromaDB
        """
        self.embedding_model = SentenceTransformer('HIT-TMG/KaLM-embedding-multilingual-mini-instruct-v1.5')
        # Utilisation d'une persistance locale pour ChromaDB
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Gestion de la collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except:
            self.collection = self.client.create_collection(name=collection_name)
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Vectorise et stocke les documents dans ChromaDB.
        
        Args:
            documents (List[Dict[str, str]]): Liste des documents à stocker
        """
        # Vérifier si la collection est vide avant d'ajouter des documents
        if self.collection.count() == 0:
            texts = [doc['page_content'] for doc in documents]
            embeddings = self.embedding_model.encode(texts).tolist()
            metadatas = [doc['metadata'] for doc in documents]
            ids = [f"doc_{i}" for i in range(len(documents))]
            
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Recherche les documents les plus pertinents pour une requête.
        
        Args:
            query (str): Requête de l'utilisateur
            k (int): Nombre de documents à retourner
            
        Returns:
            List[Dict]: Liste des documents les plus pertinents
        """
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        return results