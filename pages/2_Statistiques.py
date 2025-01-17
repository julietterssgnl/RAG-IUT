import streamlit as st  # Importation de la bibliothèque Streamlit pour créer une interface web interactive
import plotly.graph_objects as go  # Importation de Plotly pour créer des graphiques interactifs
from rag.feedback.feedback_manager import FeedbackManager  # Importation du gestionnaire de feedback depuis le module 'rag'

def main():
    # Configuration de la page Streamlit
    st.set_page_config(
        page_title="Statistiques - Assistant Assurance",  # Titre de la page
        page_icon="📊",  # Icône de la page (graphique)
        layout="wide"  # Layout de la page en mode large
    )

    st.title("Statistiques de Satisfaction")  # Titre principal de la page

    # Récupération des statistiques de feedback via FeedbackManager
    feedback_manager = FeedbackManager()  # Création d'une instance de FeedbackManager pour accéder aux données
    positive, negative = feedback_manager.get_statistics()  # Récupération du nombre de retours positifs et négatifs
    total = positive + negative  # Calcul du nombre total de retours

    # Vérification si des retours existent
    if total > 0:
        # Création du graphique en donut avec Plotly
        fig = go.Figure(data=[go.Pie(
            labels=['Satisfait', 'Non satisfait'],  # Labels du graphique (satisfait, non satisfait)
            values=[positive, negative],  # Valeurs correspondant aux retours positifs et négatifs
            hole=.6,  # Taille du trou au centre pour faire un graphique en donut
            marker_colors=['#00CC96', '#EF553B']  # Couleurs personnalisées pour les segments (vert pour satisfait, rouge pour non satisfait)
        )])

        # Personnalisation du graphique (titre et annotation du pourcentage)
        fig.update_layout(
            title="Taux de satisfaction des utilisateurs",  # Titre du graphique
            annotations=[dict(
                text=f'{(positive/total*100):.1f}%',  # Affichage du pourcentage de satisfaction
                x=0.5, y=0.5,  # Position de l'annotation au centre du graphique
                font_size=20,  # Taille de la police de l'annotation
                showarrow=False  # Pas de flèche pointant vers l'annotation
            )]
        )

        # Affichage du graphique interactif sur la page Streamlit
        st.plotly_chart(fig)

        # Affichage des statistiques détaillées dans des colonnes
        col1, col2, col3 = st.columns(3)  # Création de 3 colonnes pour afficher les statistiques
        with col1:
            st.metric("Retours totaux", total)  # Affichage du nombre total de retours
        with col2:
            st.metric("Retours positifs", positive)  # Affichage du nombre de retours positifs
        with col3:
            st.metric("Retours négatifs", negative)  # Affichage du nombre de retours négatifs
    else:
        # Si aucun retour utilisateur n'est enregistré, afficher un message informatif
        st.info("Aucun retour utilisateur n'a encore été enregistré.")

# Exécution de la fonction main lorsque le script est exécuté
if __name__ == "__main__":
    main()
