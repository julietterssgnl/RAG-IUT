import streamlit as st

def main():
    st.set_page_config(
        page_title="À propos - Assistant Assurance",
        page_icon="ℹ️",
        layout="wide"
    )

    st.title("À propos de l'Assistant Assurance OptiSecure")

    # Image ou logo si vous en avez un
    # st.image("./img/PhotoButSd.jpg", width=600)

    st.markdown("""
    ## Notre Assistant Intelligent pour l'Assurance

    Bienvenue sur l'Assistant Assurance OptiSecure, votre solution intelligente pour naviguer dans 
    vos documents d'assurance. Cet outil utilise les dernières avancées en intelligence artificielle 
    pour vous fournir des réponses précises et pertinentes concernant vos contrats d'assurance.

    ### Fonctionnalités principales

    - **Recherche intelligente** : Notre système analyse en profondeur vos documents d'assurance 
    pour trouver les informations les plus pertinentes
    - **Réponses précises** : Obtenez des réponses claires et concises à vos questions
    - **Support multilingue** : Interface en français avec capacité de compréhension contextuelle
    - **Sécurité des données** : Vos documents sont traités de manière sécurisée

    ### Technologies utilisées

    Cette application utilise des technologies de pointe :
    - RAG (Retrieval-Augmented Generation) pour une recherche précise
    - API Google AI (Gemini) pour le traitement du langage naturel
    - Base de données vectorielle pour une recherche optimisée
    - Interface utilisateur Streamlit pour une expérience fluide

    ### Comment utiliser l'assistant

    1. **Configuration** : Entrez votre clé API Google AI dans la barre latérale
    2. **Posez votre question** : Saisissez votre question dans le champ de texte
    3. **Obtenez votre réponse** : L'assistant analysera vos documents et vous fournira une réponse pertinente

    ### Support et Contact

    Pour toute question ou assistance, contactez notre équipe :
    - Email : support@optisecure.exemple.com
    - Téléphone : 01 23 45 67 89

    ---
    
    *Développé dans le cadre d'un projet académique à l'IUT - 2024*
    """)

    # Affichage des informations techniques dans un expander
    with st.expander("Informations techniques"):
        st.markdown("""
        ### Architecture du système
        
        - **Frontend** : Streamlit
        - **Backend** : Python 3.8+
        - **Base de données** : ChromaDB
        - **Modèle de langage** : Google Gemini Pro
        - **Traitement des documents** : BeautifulSoup4
        
        ### Versions des composants
        
        - streamlit==1.40.2
        - beautifulsoup4==4.12.3
        - chromadb==0.5.21
        - sentence-transformers==3.3.1
        - google-genai==0.4.0
        """)

if __name__ == "__main__":
    main()
