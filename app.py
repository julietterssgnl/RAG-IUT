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

def init_components(api_key: str):
    """
    Initialise tous les composants nécessaires au chatbot.
    """
    # Chargement des documents
    loader = DocumentLoader("documents")
    documents = loader.load_documents()
    
    # Découpage des documents
    splitter = TextSplitter()
    chunks = splitter.split_documents(documents)
    
    # Création et remplissage de la base vectorielle
    vector_store = VectorStore()
    vector_store.add_documents(chunks)
    
    # Initialisation du chatbot et du gestionnaire de feedback
    chatbot = Chatbot(api_key)
    feedback_manager = FeedbackManager()
    
    return vector_store, chatbot, feedback_manager

def main():
    st.title("Assistant Assurance OptiSecure")
    
    # Zone de saisie de la clé API dans la barre latérale
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Entrez votre clé API Google AI", type="password")
        if not api_key:
            st.warning("Veuillez entrer votre clé API pour continuer")
            return
            
    # Initialisation des composants
    if 'initialized' not in st.session_state and api_key:
        try:
            vector_store, chatbot, feedback_manager = init_components(api_key)
            
            # Stockage dans la session
            st.session_state.vector_store = vector_store
            st.session_state.chatbot = chatbot
            st.session_state.feedback_manager = feedback_manager
            st.session_state.initialized = True
            st.success("Système initialisé avec succès!")
            
        except Exception as e:
            st.error(f"Erreur lors de l'initialisation: {str(e)}")
            return
    
    # Interface utilisateur principale
    if st.session_state.get('initialized'):
        st.subheader("Posez votre question")
        query = st.text_input("Votre question sur les contrats d'assurance:")
        
        # Si une question est posée
        if query:
            with st.spinner("Recherche en cours..."):
                # Recherche des documents pertinents
                context = st.session_state.vector_store.search(query)
                
                # Génération de la réponse
                response = st.session_state.chatbot.generate_response(query, context)
                
                # Stockage temporaire de la dernière interaction
                st.session_state.last_query = query
                st.session_state.last_response = response
                
                # Affichage de la réponse
                with st.container():
                    st.markdown("---")
                    st.markdown("### Réponse:")
                    st.write(response)
                    
                    # Boutons de feedback
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("👍 Utile"):
                            st.session_state.feedback_manager.add_feedback(
                                query, response, True
                            )
                            st.success("Merci pour votre retour !")
                            
                    with col2:
                        if st.button("👎 Pas utile"):
                            st.session_state.feedback_manager.add_feedback(
                                query, response, False
                            )
                            st.success("Merci pour votre retour !")
                    
                    st.markdown("---")
        
        # Bouton de réinitialisation
        if st.button("Réinitialiser le système"):
            st.session_state.clear()
            st.experimental_rerun()

if __name__ == "__main__":
    main()