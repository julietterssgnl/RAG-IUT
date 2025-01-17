from bs4 import BeautifulSoup  # Importation de BeautifulSoup pour parser les documents HTML
from typing import List, Dict  # Importation des types pour une typisation statique claire
import os  # Importation de la bibliothèque os pour manipuler les fichiers et répertoires

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
        self.documents_path = documents_path  # Le chemin vers le dossier des documents HTML est sauvegardé comme attribut
    
    def load_documents(self) -> List[Dict[str, str]]:
        """
        Charge tous les documents HTML du dossier spécifié et les convertit en format texte.
        
        Returns:
            List[Dict[str, str]]: Liste de dictionnaires contenant le contenu et les métadonnées des documents
        """
        documents = []  # Liste qui stockera les documents chargés sous forme de dictionnaires
        
        # Parcourt tous les fichiers du répertoire spécifié
        for filename in os.listdir(self.documents_path):  # Liste tous les fichiers dans le répertoire documents_path
            if filename.endswith('.html'):  # Vérifie si le fichier est un fichier HTML
                file_path = os.path.join(self.documents_path, filename)  # Construit le chemin complet du fichier HTML
                with open(file_path, 'r', encoding='utf-8') as file:  # Ouvre le fichier en mode lecture avec encodage UTF-8
                    soup = BeautifulSoup(file.read(), 'html.parser')  # Utilise BeautifulSoup pour parser le contenu HTML
                    
                    # Extraction du texte en supprimant les éléments <script> et <style>
                    for script in soup(['script', 'style']):  # Parcourt tous les éléments <script> et <style>
                        script.decompose()  # Supprime ces éléments du document HTML pour ne garder que le texte
                    
                    # Récupère le texte du document HTML en un seul bloc, séparé par des espaces, et supprime les espaces superflus
                    text = soup.get_text(separator=' ', strip=True)
                    
                    # Ajoute le texte extrait et les métadonnées dans un dictionnaire
                    documents.append({
                        'page_content': text,  # Le texte du document
                        'metadata': {  # Les métadonnées associées au document
                            'source': filename,  # Nom du fichier comme source
                            'type': 'assurance'  # Type de document (dans ce cas, "assurance")
                        }
                    })
                    
        return documents  # Retourne la liste des documents sous forme de dictionnaires
