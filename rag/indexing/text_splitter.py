from typing import List, Dict
import re
import json

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
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def split_documents(self, documents: List[Dict[str, str]], output_file: str = "chunks.json") -> List[Dict[str, str]]:
        """
        Découpe les documents en chunks par sections principales et enregistre le résultat dans un fichier JSON.
        
        Args:
            documents (List[Dict[str, str]]): Liste des documents à découper
            output_file (str): Chemin du fichier JSON de sortie
            
        Returns:
            List[Dict[str, str]]: Liste des chunks de documents
        """
        chunks = []
        
        for doc in documents:
            text = doc['page_content']
            
            # Découpage en sections principales (grand titre)
            sections = re.split(r'\n\s*\n(?=\d+\.\s)', text)
            
            for section in sections:
                chunks.append({
                    'page_content': section.strip(),
                    'metadata': doc['metadata'].copy()
                })
        
        # Enregistrement des chunks dans un fichier JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=4)
                
        return chunks