import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple
import os

class FeedbackManager:
    """
    Gère le stockage et la récupération des retours utilisateurs.
    """
    
    def __init__(self, db_path: str = "feedback.db"):
        """
        Initialise le gestionnaire de feedback.
        
        Args:
            db_path (str): Chemin vers la base de données SQLite
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialise la base de données si elle n'existe pas."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    response TEXT NOT NULL,
                    is_helpful BOOLEAN NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def add_feedback(self, question: str, response: str, is_helpful: bool):
        """
        Ajoute un nouveau feedback dans la base de données.
        
        Args:
            question (str): Question posée par l'utilisateur
            response (str): Réponse du chatbot
            is_helpful (bool): True si la réponse était utile, False sinon
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT INTO feedback (question, response, is_helpful) VALUES (?, ?, ?)',
                (question, response, is_helpful)
            )
            conn.commit()
    
    def get_statistics(self) -> Tuple[int, int]:
        """
        Récupère les statistiques de satisfaction.
        
        Returns:
            Tuple[int, int]: (nombre de retours positifs, nombre de retours négatifs)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    SUM(CASE WHEN is_helpful THEN 1 ELSE 0 END) as positive,
                    SUM(CASE WHEN NOT is_helpful THEN 1 ELSE 0 END) as negative
                FROM feedback
            ''')
            positive, negative = cursor.fetchone()
            return (positive or 0, negative or 0)