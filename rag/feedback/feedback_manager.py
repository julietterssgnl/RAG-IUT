import sqlite3  # Importation de sqlite3 pour interagir avec la base de données SQLite
from datetime import datetime  # Importation de datetime pour gérer les horodatages
from typing import Dict, List, Tuple  # Importation des types pour la typisation statique
import os  # Importation de la bibliothèque os pour manipuler les chemins de fichiers et répertoires

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
        self.db_path = db_path  # Sauvegarde du chemin de la base de données dans un attribut
        self._init_db()  # Appelle la méthode pour initialiser la base de données

    def _init_db(self):
        """Initialise la base de données si elle n'existe pas."""
        # Connexion à la base de données SQLite (elle sera créée si elle n'existe pas)
        with sqlite3.connect(self.db_path) as conn:
            # Création de la table 'feedback' si elle n'existe pas déjà
            conn.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    response TEXT NOT NULL,
                    is_helpful BOOLEAN NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()  # Applique les changements dans la base de données

    def add_feedback(self, question: str, response: str, is_helpful: bool):
        """
        Ajoute un nouveau feedback dans la base de données.
        
        Args:
            question (str): Question posée par l'utilisateur
            response (str): Réponse du chatbot
            is_helpful (bool): True si la réponse était utile, False sinon
        """
        # Connexion à la base de données pour ajouter un retour
        with sqlite3.connect(self.db_path) as conn:
            # Exécution de la commande d'insertion dans la table 'feedback'
            conn.execute(
                'INSERT INTO feedback (question, response, is_helpful) VALUES (?, ?, ?)',
                (question, response, is_helpful)  # Remplacement des paramètres par les valeurs réelles
            )
            conn.commit()  # Applique les changements dans la base de données

    def get_statistics(self) -> Tuple[int, int]:
        """
        Récupère les statistiques de satisfaction.
        
        Returns:
            Tuple[int, int]: (nombre de retours positifs, nombre de retours négatifs)
        """
        # Connexion à la base de données pour récupérer les statistiques
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()  # Création d'un curseur pour exécuter des requêtes SQL
            # Requête SQL pour compter les retours positifs et négatifs
            cursor.execute('''
                SELECT 
                    SUM(CASE WHEN is_helpful THEN 1 ELSE 0 END) as positive,
                    SUM(CASE WHEN NOT is_helpful THEN 1 ELSE 0 END) as negative
                FROM feedback
            ''')
            # Récupère les résultats de la requête
            positive, negative = cursor.fetchone()
            # Retourne les statistiques, en s'assurant que si aucune donnée n'est présente, on retourne 0
            return (positive or 0, negative or 0)
