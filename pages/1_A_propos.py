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

    ### Technologies utilisées

    Cette application utilise des technologies avancées pour offrir une expérience utilisateur optimale :
    - RAG (Retrieval-Augmented Generation) pour une recherche précise
    - API Google AI (Gemini) pour le traitement du langage naturel
    - BeautifulSoup4 pour le traitement des documents HTML
    - Sentence Transformers pour la vectorisation des documents
    - ChromaDB pour le stockage et la recherche de documents
    - Streamlit pour l'interface utilisateur
    - Statistiques de satisfaction pour améliorer le service avec Plotly


    ### Comment utiliser l'assistant

    1. **Configuration** : Entrez votre clé API Google AI dans la barre latérale
    2. **Posez votre question** : Saisissez votre question dans le champ de texte
    3. **Obtenez votre réponse** : L'assistant analysera vos documents et vous fournira une réponse pertinente
    4. **Donnez votre avis** : Indiquez si la réponse était utile ou non pour améliorer le service

    ### Support et Contact

    Pour toute question ou assistance, contactez notre équipe :
    - Juliette ROSSIGNOL https://github.com/julietterssgnl/
    - Dorine BARBEY https://github.com/dodoBrb/
    - Thibault DAGUIN https://github.com/ThibaultDAGUIN/

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
        - **Vectorisation des documents** : Sentence Transformers
        - **Statistiques de satisfaction** : Plotly
        - **Base de données de feedback** : SQLite
        
        ### Versions des composants
        
        - streamlit==1.40.2
        - beautifulsoup4==4.12.3
        - chromadb==0.5.21
        - sentence-transformers==3.3.1
        - google-genai==0.4.0
        - google-generativeai==0.4.0
        - plotly==5.3.1
        """)

if __name__ == "__main__":
    main()
