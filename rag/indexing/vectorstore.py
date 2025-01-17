# Import du modèle de transformers pour la création d'embeddings (vecteurs) à partir du texte
from sentence_transformers import SentenceTransformer
# Import de ChromaDB pour la base de données vectorielle
import chromadb
# Import des types pour le typage statique
from typing import List, Dict
# Import pour la gestion des chemins de fichiers
import os

class VectorStore:
    """
    Classe responsable de la vectorisation et du stockage des documents.
    Cette classe gère la transformation des textes en vecteurs et leur stockage dans ChromaDB.
    """
    
    def __init__(self, collection_name: str = "documents"):
        """
        Initialise la base de données vectorielle.
        
        Args:
            collection_name (str): Nom de la collection dans ChromaDB. Par défaut "documents"
        """
        # Initialisation du modèle d'embedding multilingue pour la vectorisation des textes
        # Ce modèle spécifique est choisi pour sa capacité à traiter le français
        self.embedding_model = SentenceTransformer('HIT-TMG/KaLM-embedding-multilingual-mini-instruct-v1.5')
        
        # Création d'un client ChromaDB persistant qui stocke les données sur le disque
        # Le chemin './chroma_db' indique où les données seront sauvegardées
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Tentative de récupération ou création de la collection
        try:
            # Essaie d'abord de récupérer une collection existante
            self.collection = self.client.get_collection(name=collection_name)
        except:
            # Si la collection n'existe pas, en crée une nouvelle
            self.collection = self.client.create_collection(name=collection_name)
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Vectorise et stocke les documents dans ChromaDB.
        
        Args:
            documents (List[Dict[str, str]]): Liste des documents à stocker
                Chaque document est un dictionnaire avec 'page_content' et 'metadata'
        """
        # Vérifie si la collection est vide pour éviter les doublons
        if self.collection.count() == 0:
            # Extrait le contenu textuel de chaque document
            texts = [doc['page_content'] for doc in documents]
            
            # Convertit chaque texte en vecteur (embedding)
            # .tolist() convertit les vecteurs numpy en listes Python pour ChromaDB
            embeddings = self.embedding_model.encode(texts).tolist()
            
            # Récupère les métadonnées de chaque document
            metadatas = [doc['metadata'] for doc in documents]
            
            # Génère des identifiants uniques pour chaque document
            ids = [f"doc_{i}" for i in range(len(documents))]
            
            # Ajoute les documents, leurs embeddings et métadonnées à ChromaDB
            self.collection.add(
                embeddings=embeddings,  # Les vecteurs des documents
                documents=texts,        # Le texte brut des documents
                metadatas=metadatas,    # Les métadonnées associées
                ids=ids                 # Les identifiants uniques
            )
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Recherche les documents les plus pertinents pour une requête.
        
        Args:
            query (str): Requête de l'utilisateur à rechercher
            k (int): Nombre de documents à retourner (par défaut 3)
            
        Returns:
            List[Dict]: Liste des k documents les plus pertinents avec leurs scores
        """
        # Convertit la requête en vecteur pour la comparaison
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Effectue une recherche par similarité dans ChromaDB
        # Trouve les k documents les plus proches du vecteur de la requête
        results = self.collection.query(
            query_embeddings=[query_embedding],  # Le vecteur de la requête
            n_results=k                         # Nombre de résultats souhaités
        )
        
        # Retourne les résultats de la recherche
        return results