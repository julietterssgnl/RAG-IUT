# Importation des bibliothèques nécessaires
import streamlit as st  # Import de Streamlit pour créer l'interface utilisateur
from rag.indexing.document_loader import DocumentLoader  # Chargement des documents depuis le disque
from rag.indexing.text_splitter import TextSplitter  # Découpage des documents en morceaux
from rag.indexing.vectorstore import VectorStore  # Gestion de la base de données vectorielle
from rag.chat.chatbot import Chatbot  # Gestion du chatbot
from rag.feedback.feedback_manager import FeedbackManager  # Gestion des retours d'utilisateur

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Accueil - Assistant Assurance",  # Titre de la page
    page_icon="🏠",  # Icône de la page
    layout="wide"  # Disposition de la page (largeur étendue)
)

# Ajout de CSS personnalisé pour modifier le style des boutons de feedback
st.markdown("""
<style>
    /* Style pour le bouton positif (utile) */
    [data-testid="column"]:has(button:contains("👍")) button:hover {
        background-color: #4CAF50 !important;  /* Couleur verte */
        border-color: #4CAF50 !important;      /* Bordure verte */
        color: white !important;               /* Texte blanc */
    }
    
    /* Style pour le bouton négatif (pas utile) */
    [data-testid="column"]:has(button:contains("👎")) button:hover {
        background-color: #f44336 !important;  /* Couleur rouge */
        border-color: #f44336 !important;      /* Bordure rouge */
        color: white !important;               /* Texte blanc */
    }
</style>
""", unsafe_allow_html=True)  # Applique le CSS au rendu HTML de Streamlit

def init_components(api_key: str):
    """
    Initialise tous les composants nécessaires au chatbot.
    Args:
        api_key (str): Clé API Google AI
    Returns:
        tuple: (vector_store, chatbot, feedback_manager)
    """
    st.session_state.api_key = api_key  # Sauvegarde de la clé API dans l'état de la session
    
    # Chargement et traitement des documents dans un bloc d'attente
    with st.spinner("Initialisation en cours..."):  # Affiche un message de chargement
        try:
            # Chargement des documents depuis le répertoire "documents"
            st.info("Chargement des documents...")  # Affiche une information à l'utilisateur
            loader = DocumentLoader("documents")  # Instance de DocumentLoader pour charger les fichiers
            documents = loader.load_documents()  # Chargement des documents
            
            # Découpage des documents en morceaux plus petits
            st.info("Découpage des documents...")  # Affiche une info pendant le découpage
            splitter = TextSplitter()  # Instance de TextSplitter pour découper les documents
            chunks = splitter.split_documents(documents)  # Découpe les documents en morceaux
            
            # Création de la base vectorielle pour stocker les documents découpés
            st.info("Création de la base vectorielle...")  # Affiche une info pendant la création de la base
            vector_store = VectorStore()  # Instance de VectorStore pour gérer les embeddings des documents
            vector_store.add_documents(chunks)  # Ajoute les documents découpés à la base vectorielle
            
            # Initialisation du chatbot et du gestionnaire de feedback
            st.info("Initialisation du chatbot...")  # Affiche une info pendant l'initialisation du chatbot
            chatbot = Chatbot(api_key)  # Instance du chatbot avec la clé API fournie
            feedback_manager = FeedbackManager()  # Instance pour gérer les retours utilisateurs
            
            st.success("Initialisation terminée avec succès!")  # Affiche un message de succès
            return vector_store, chatbot, feedback_manager  # Retourne les objets créés
            
        except Exception as e:
            st.error(f"Erreur lors de l'initialisation: {str(e)}")  # Affiche un message d'erreur si quelque chose ne va pas
            return None, None, None  # Retourne None en cas d'erreur

def handle_logout():
    """Gère la déconnexion de l'utilisateur."""
    for key in list(st.session_state.keys()):  # Parcours toutes les clés dans la session
        del st.session_state[key]  # Supprime chaque clé pour réinitialiser la session

def main():
    st.title("Assistant Assurance OptiSecure")  # Titre de la page principale
    
    # Inclure le CDN Font Awesome dans la page
    st.markdown(""" <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet"> """, unsafe_allow_html=True)

    # Gestion de la connexion dans la barre latérale
    with st.sidebar:
        st.header("Configuration")  # Affiche un en-tête dans la barre latérale
        
        # Affichage du statut de connexion
        if 'api_key' in st.session_state:  # Vérifie si la clé API est enregistrée dans la session
            st.success("🟢 Connecté")  # Affiche un message de succès si la connexion est établie
            if st.button("Déconnexion"):  # Si le bouton de déconnexion est cliqué
                handle_logout()  # Déconnexion de l'utilisateur
                st.rerun()  # Recharge la page
        else:
            # Affiche des instructions pour obtenir une clé API si l'utilisateur n'est pas connecté
            st.markdown("""
            ### Obtenir une clé API
            1. Rendez-vous sur [Google AI Studio](https://aistudio.google.com/prompts/new_chat?pli=1)
            2. Connectez-vous avec votre compte Google
            3. Dans les paramètres (⚙️), trouvez votre clé API
            """)
            
            st.markdown("---")
            
            api_key = st.text_input("Entrez votre clé API Google AI", type="password")  # Saisie de la clé API
            if api_key:  # Si une clé est saisie
                st.session_state.api_key = api_key  # Enregistre la clé API dans l'état de la session
                st.rerun()  # Recharge la page
            else:
                st.warning("Veuillez entrer votre clé API pour continuer")  # Alerte si aucune clé n'est saisie
                return  # Quitte la fonction si aucune clé n'est fournie
    
    # Initialisation des composants si nécessaire
    if 'api_key' in st.session_state and 'initialized' not in st.session_state:  # Si la clé API est présente et l'initialisation n'a pas encore été faite
        vector_store, chatbot, feedback_manager = init_components(st.session_state.api_key)  # Initialise les composants
        if vector_store and chatbot and feedback_manager:  # Si l'initialisation a réussi
            # Enregistre les objets dans l'état de la session pour les réutiliser plus tard
            st.session_state.vector_store = vector_store
            st.session_state.chatbot = chatbot
            st.session_state.feedback_manager = feedback_manager
            st.session_state.initialized = True  # Marque que l'initialisation est terminée
    

    # Interface utilisateur principale si le système est initialisé
    if st.session_state.get('initialized'): # Si le système a été initialisé
        st.markdown("<i class='fa fa-user'></i><strong>Posez votre question</strong>", unsafe_allow_html=True) # Sous-titre pour la section de la question
        query = st.text_input("Votre question sur les contrats d'assurance:") # Champ de saisie de la question

        
        if query:  # Si une question est saisie
            with st.spinner("Recherche en cours..."):  # Affiche un message de chargement pendant la recherche
                try:
                    # Recherche des documents pertinents pour la question posée
                    context = st.session_state.vector_store.search(query)  
                    # Génération de la réponse par le chatbot
                    response = st.session_state.chatbot.generate_response(query, context)
                    
                    # Affichage de la réponse et des boutons de feedback
                    with st.container():  # Crée un conteneur pour afficher la réponse
                        st.markdown("---")

                        st.markdown("<i class='fa fa-robot'></i><strong>Réponse</strong>", unsafe_allow_html=True) # Affiche la réponse générée par le chatbot
                        st.write(response)

                        
                        # Boutons de feedback avec styles personnalisés
                        col1, col2 = st.columns(2)  # Crée deux colonnes pour les boutons
                        with col1:  # Colonne pour le bouton "Utile"
                            if st.button("👍 Utile", key="useful"):
                                st.session_state.feedback_manager.add_feedback(  # Enregistre le feedback
                                    query, response, True
                                )
                                st.success("Merci pour votre retour !")  # Affiche un message de remerciement
                        
                        with col2:  # Colonne pour le bouton "Pas utile"
                            neg_button = st.button("👎 Pas utile", key="not_useful")
                            if neg_button:
                                st.session_state.feedback_manager.add_feedback(  # Enregistre le feedback négatif
                                    query, response, False
                                )
                                st.success("Merci pour votre retour !")
                        
                        st.markdown("---")
                except Exception as e:
                    st.error(f"Une erreur est survenue : {str(e)}")  # Affiche un message d'erreur en cas de problème
                    # Réinitialisation en cas d'erreur de ChromaDB
                    if "no such table: collections" in str(e):  
                        st.warning("Réinitialisation du système...")
                        st.session_state.clear()  # Efface l'état de la session
                        st.rerun()  # Recharge la page pour réinitialiser l'application

# Fonction principale appelée si le script est exécuté
if __name__ == "__main__":
    main()
