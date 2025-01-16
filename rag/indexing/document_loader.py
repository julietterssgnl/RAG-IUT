from bs4 import BeautifulSoup
from typing import List, Dict
import os

class DocumentLoader:
    """
    Classe responsable du chargement et du parsing des documents HTML.
    """
    
    def __init__(self, documents_path: str):
        """
        Initialise le chargeur de documents.
        
        Args:
            documents_path (str): Chemin vers le dossier contenant les documents HTML
        """
        self.documents_path = documents_path
        
    def load_documents(self) -> List[Dict[str, str]]:
        """
        Charge tous les documents HTML du dossier spécifié et les convertit en format texte.
        
        Returns:
            List[Dict[str, str]]: Liste de dictionnaires contenant le contenu et les métadonnées des documents
        """
        documents = []
        
        for filename in os.listdir(self.documents_path):
            if filename.endswith('.html'):
                file_path = os.path.join(self.documents_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file.read(), 'html.parser')
                    
                    # Extraction du texte en supprimant les scripts et styles
                    for script in soup(['script', 'style']):
                        script.decompose()
                    
                    text = soup.get_text(separator=' ', strip=True)
                    
                    documents.append({
                        'page_content': text,
                        'metadata': {
                            'source': filename,
                            'type': 'assurance'
                        }
                    })
                    
        return documents
