from typing import List, Dict  # Importation des types pour un typage statique plus précis
import re  # Importation du module regex pour le découpage en sections
import json  # Importation du module JSON pour enregistrer les résultats dans un fichier

class TextSplitter:
    """
    Classe responsable du découpage des documents en chunks plus petits.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialise le découpeur de texte.
        
        Args:
            chunk_size (int): Taille maximale de chaque chunk en caractères
            chunk_overlap (int): Nombre de caractères de chevauchement entre les chunks
        """
        self.chunk_size = chunk_size  # Taille de chaque chunk en caractères
        self.chunk_overlap = chunk_overlap  # Taille du chevauchement entre les chunks
        
    def split_documents(self, documents: List[Dict[str, str]], output_file: str = "chunks.json") -> List[Dict[str, str]]:
        """
        Découpe les documents en chunks par sections principales et enregistre le résultat dans un fichier JSON.
        
        Args:
            documents (List[Dict[str, str]]): Liste des documents à découper
            output_file (str): Chemin du fichier JSON de sortie
            
        Returns:
            List[Dict[str, str]]: Liste des chunks de documents
        """
        chunks = []  # Liste qui stockera les chunks de documents créés
        
        for doc in documents:  # Parcourt chaque document dans la liste des documents
            text = doc['page_content']  # Récupère le contenu texte du document
            
            # Découpage en sections principales (grand titre). Cela divise le texte par les titres de section
            sections = re.split(r'\n\s*\n(?=\d+\.\s)', text)  # Utilisation d'une expression régulière pour séparer par grands titres (ex: 1., 2., 3., ...)
            
            for section in sections:  # Parcourt chaque section obtenue
                chunks.append({
                    'page_content': section.strip(),  # Nettoie et ajoute le texte de la section
                    'metadata': doc['metadata'].copy()  # Copie les métadonnées associées au document
                })
        
        # Enregistrement des chunks dans un fichier JSON
        with open(output_file, 'w', encoding='utf-8') as f:  # Ouvre le fichier JSON pour écriture
            json.dump(chunks, f, ensure_ascii=False, indent=4)  # Enregistre les chunks au format JSON dans le fichier

        return chunks  # Retourne la liste des chunks créés
