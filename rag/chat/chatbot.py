import google.generativeai as genai
from typing import List, Dict

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
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_response(self, query: str, context: List[Dict]) -> str:
        """
        Génère une réponse à partir de la requête et du contexte.
        
        Args:
            query (str): Question de l'utilisateur
            context (List[Dict]): Contexte récupéré de la base vectorielle
            
        Returns:
            str: Réponse générée
        """
        prompt = f"""En tant qu'assistant spécialisé dans les documents d'assurance, utilise le contexte suivant 
        pour répondre à la question. Réponds en français, de manière concise et précise.
        
        Contexte:
        {context}
        
        Question: {query}
        """
        
        response = self.model.generate_content(prompt)
        return response.text