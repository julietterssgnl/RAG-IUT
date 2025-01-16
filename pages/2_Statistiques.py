import streamlit as st
import plotly.graph_objects as go
from rag.feedback.feedback_manager import FeedbackManager

def main():
    st.set_page_config(
        page_title="Statistiques - Assistant Assurance",
        page_icon="📊",
        layout="wide"
    )

    st.title("Statistiques de Satisfaction")

    # Récupération des statistiques
    feedback_manager = FeedbackManager()
    positive, negative = feedback_manager.get_statistics()
    total = positive + negative
    
    if total > 0:
        # Création du graphique en donut
        fig = go.Figure(data=[go.Pie(
            labels=['Satisfait', 'Non satisfait'],
            values=[positive, negative],
            hole=.6,
            marker_colors=['#00CC96', '#EF553B']
        )])
        
        # Personnalisation du graphique
        fig.update_layout(
            title="Taux de satisfaction des utilisateurs",
            annotations=[dict(
                text=f'{(positive/total*100):.1f}%',
                x=0.5, y=0.5,
                font_size=20,
                showarrow=False
            )]
        )
        
        # Affichage du graphique
        st.plotly_chart(fig)
        
        # Affichage des statistiques détaillées
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Retours totaux", total)
        with col2:
            st.metric("Retours positifs", positive)
        with col3:
            st.metric("Retours négatifs", negative)
    else:
        st.info("Aucun retour utilisateur n'a encore été enregistré.")

if __name__ == "__main__":
    main()