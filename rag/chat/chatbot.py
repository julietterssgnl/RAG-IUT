import google.generativeai as genai  # Importation de la bibliothèque Google AI pour utiliser le modèle génératif
from typing import List, Dict  # Importation des types pour la typisation statique (List et Dict)

class Chatbot:
    """
    Classe principale du chatbot utilisant Google AI.
    """
    
    def __init__(self, api_key: str):
        """
        Initialise le chatbot.
        
        Args:
            api_key (str): Clé API Google AI
        """
        genai.configure(api_key=api_key)  # Configuration de l'API Google AI avec la clé API fournie
        self.model = genai.GenerativeModel('gemini-pro')  # Initialisation du modèle génératif 'gemini-pro' de Google AI
        
    def generate_response(self, query: str, context: List[Dict]) -> str:
        """
        Génère une réponse à partir de la requête et du contexte.
        
        Args:
            query (str): Question de l'utilisateur
            context (List[Dict]): Contexte récupéré de la base vectorielle
            
        Returns:
            str: Réponse générée
        """
        # Construction du prompt à envoyer au modèle génératif
        prompt = f"""En tant qu'assistant spécialisé dans les documents d'assurance, utilise le contexte suivant 
        pour répondre à la question. Réponds en français, de manière concise et précise.
        
        Contexte:
        {context}  # Le contexte est inséré ici, il est attendu sous forme de liste de dictionnaires
        
        Question: {query}  # La question de l'utilisateur est insérée ici
        """
        
        # Appel du modèle génératif pour générer la réponse
        response = self.model.generate_content(prompt)
        
        # Retour de la réponse générée par le modèle (texte sous forme de chaîne de caractères)
        return response.text
