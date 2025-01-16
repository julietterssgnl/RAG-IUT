import streamlit as st
from rag.indexing.document_loader import DocumentLoader
from rag.indexing.text_splitter import TextSplitter
from rag.indexing.vectorstore import VectorStore
from rag.chat.chatbot import Chatbot

def init_components(api_key: str):
    """
    Initialise tous les composants nécessaires au chatbot.
    
    Args:
        api_key (str): Clé API Google AI
    """
    # Chargement des documents
    loader = DocumentLoader("documents")
    documents = loader.load_documents()
    
    # Découpage des documents et enregistrement dans un fichier JSON
    splitter = TextSplitter()
    chunks = splitter.split_documents(documents, output_file="chunks.json")
    
    # Création et remplissage de la base vectorielle
    vector_store = VectorStore()
    vector_store.add_documents(chunks)
    
    # Initialisation du chatbot
    chatbot = Chatbot(api_key)
    
    return vector_store, chatbot

def main():
    st.title("Assistant Assurance OptiSecure")
    
    # Zone de saisie de la clé API dans la barre latérale
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Entrez votre clé API Google AI", type="password")
        if not api_key:
            st.warning("Veuillez entrer votre clé API pour continuer")
            return
            
    # Initialisation des composants (à faire une seule fois)
    if 'initialized' not in st.session_state and api_key:
        try:
            vector_store, chatbot = init_components(api_key)
            
            # Stockage dans la session
            st.session_state.vector_store = vector_store
            st.session_state.chatbot = chatbot
            st.session_state.initialized = True
            st.success("Système initialisé avec succès!")
            
        except Exception as e:
            st.error(f"Erreur lors de l'initialisation: {str(e)}")
            return
    
    # Interface utilisateur principale
    if st.session_state.get('initialized'):
        st.subheader("Posez votre question")
        query = st.text_input("Votre question sur les contrats d'assurance:")
        
        if query:
            with st.spinner("Recherche en cours..."):
                # Recherche des documents pertinents
                context = st.session_state.vector_store.search(query)
                
                # Génération de la réponse
                response = st.session_state.chatbot.generate_response(query, context)
                
                # Affichage de la réponse dans un cadre distinct
                with st.container():
                    st.markdown("---")
                    st.markdown("### Réponse:")
                    st.write(response)
                    st.markdown("---")
                    
        # Ajout d'un bouton pour réinitialiser le système si nécessaire
        if st.button("Réinitialiser le système"):
            st.session_state.clear()
            st.experimental_rerun()

if __name__ == "__main__":
    main()