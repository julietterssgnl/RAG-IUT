import streamlit as st
from rag.indexing.document_loader import DocumentLoader
from rag.indexing.text_splitter import TextSplitter
from rag.indexing.vectorstore import VectorStore
from rag.chat.chatbot import Chatbot
from rag.feedback.feedback_manager import FeedbackManager

# Configuration de la page
st.set_page_config(
    page_title="Accueil - Assistant Assurance",
    page_icon="🏠",
    layout="wide"
)

# CSS personnalisé pour les boutons de feedback
st.markdown("""
<style>
    /* Style pour le bouton positif */
    [data-testid="column"]:has(button:contains("👍")) button:hover {
        background-color: #4CAF50 !important;
        border-color: #4CAF50 !important;
        color: white !important;
    }
    
    /* Style pour le bouton négatif */
    [data-testid="column"]:has(button:contains("👎")) button:hover {
        background-color: #f44336 !important;
        border-color: #f44336 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

def init_components(api_key: str):
    """
    Initialise tous les composants nécessaires au chatbot.
    Args:
        api_key (str): Clé API Google AI
    Returns:
        tuple: (vector_store, chatbot, feedback_manager)
    """
    st.session_state.api_key = api_key  # Sauvegarde de la clé API dans la session
    
    # Chargement et traitement des documents
    with st.spinner("Initialisation en cours..."):
        try:
            # Chargement des documents
            st.info("Chargement des documents...")
            loader = DocumentLoader("documents")
            documents = loader.load_documents()
            
            # Découpage des documents
            st.info("Découpage des documents...")
            splitter = TextSplitter()
            chunks = splitter.split_documents(documents)
            
            # Création et remplissage de la base vectorielle
            st.info("Création de la base vectorielle...")
            vector_store = VectorStore()
            vector_store.add_documents(chunks)
            
            # Initialisation du chatbot et du gestionnaire de feedback
            st.info("Initialisation du chatbot...")
            chatbot = Chatbot(api_key)
            feedback_manager = FeedbackManager()
            
            st.success("Initialisation terminée avec succès!")
            return vector_store, chatbot, feedback_manager
            
        except Exception as e:
            st.error(f"Erreur lors de l'initialisation: {str(e)}")
            return None, None, None

def handle_logout():
    """Gère la déconnexion de l'utilisateur."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def main():
    st.title("Assistant Assurance OptiSecure")
    
    # Inclure le CDN Font Awesome dans la page
    st.markdown(""" <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet"> """, unsafe_allow_html=True)

    # Gestion de la connexion dans la barre latérale
    with st.sidebar:
        st.header("Configuration")
        
        # Affichage du statut de connexion
        if 'api_key' in st.session_state:
            st.success("🟢 Connecté")
            if st.button("Déconnexion"):
                handle_logout()
                st.rerun()
        else:
            st.markdown("""
            ### Obtenir une clé API
            1. Rendez-vous sur [Google AI Studio](https://aistudio.google.com/prompts/new_chat?pli=1)
            2. Connectez-vous avec votre compte Google
            3. Dans les paramètres (⚙️), trouvez votre clé API
            """)
            
            st.markdown("---")
            
            api_key = st.text_input("Entrez votre clé API Google AI", type="password")
            if api_key:
                st.session_state.api_key = api_key
                st.rerun()
            else:
                st.warning("Veuillez entrer votre clé API pour continuer")
                return
    
    # Initialisation des composants si nécessaire
    if 'api_key' in st.session_state and 'initialized' not in st.session_state:
        vector_store, chatbot, feedback_manager = init_components(st.session_state.api_key)
        if vector_store and chatbot and feedback_manager:
            st.session_state.vector_store = vector_store
            st.session_state.chatbot = chatbot
            st.session_state.feedback_manager = feedback_manager
            st.session_state.initialized = True
    
    # Interface utilisateur principale
    if st.session_state.get('initialized'):
        st.markdown("<i class='fa fa-user'></i><strong>Posez votre question</strong>", unsafe_allow_html=True)
        query = st.text_input("Votre question sur les contrats d'assurance:")
        
        if query:
            with st.spinner("Recherche en cours..."):
                try:
                    # Recherche et génération de la réponse
                    context = st.session_state.vector_store.search(query)
                    response = st.session_state.chatbot.generate_response(query, context)
                    
                    # Affichage de la réponse et des boutons de feedback
                    with st.container():
                        st.markdown("---")
                        st.markdown("<i class='fa fa-robot'></i><strong>Réponse</strong>", unsafe_allow_html=True)
                        st.write(response)
                        
                        # Boutons de feedback avec styles personnalisés
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("👍 Utile", key="useful"):
                                st.session_state.feedback_manager.add_feedback(
                                    query, response, True
                                )
                                st.success("Merci pour votre retour !")
                        
                        with col2:
                            neg_button = st.button("👎 Pas utile", key="not_useful")
                            if neg_button:
                                st.session_state.feedback_manager.add_feedback(
                                    query, response, False
                                )
                                st.success("Merci pour votre retour !")
                        
                        st.markdown("---")
                except Exception as e:
                    st.error(f"Une erreur est survenue : {str(e)}")
                    # Réinitialisation en cas d'erreur de ChromaDB
                    if "no such table: collections" in str(e):
                        st.warning("Réinitialisation du système...")
                        st.session_state.clear()
                        st.rerun()

if __name__ == "__main__":
    main()