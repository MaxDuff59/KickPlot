import streamlit as st
from io import BytesIO
import pandas as pd
import fonction

st.set_page_config(layout="wide")

def main():

    tab1, tab2 = st.tabs(["Kicking Graphs", "Dog", "Owl"])

    with tab1:
        
        st.title("Racing 92 - Graphiques KICKING 🔵⚪️")
        
        uploaded_file = st.file_uploader("Importer le fichier CSV", type=["csv"])
        
        if uploaded_file is not None:
    
            st.write("File Uploaded Successfully!")
            
            df = pd.read_csv(uploaded_file)
            joueurs_racing = list(df[df.Row == "17.JAP Racing 92"].Joueurs.unique())
    
            player_inputs = {}
        
            for player in joueurs_racing:
    
                player_input = st.text_input(f"N° de {player} : ")
                player_inputs[player] = player_input
            
            st.write("Player Inputs:")
            st.write(player_inputs)
    
            if st.button("Process Images"):
    
                img = fonction.kicking_plot(df,player_inputs)
                st.image(img)
    
                img = fonction.kicking_plot_adv(df)
                st.image(img)

    with tab2:

        st.title('Collective Experience')

        url = st.text_input('URL du match : ', '')

        if st.button('Téléchargement des données'):
            
            df_experience_match, df_summary = fonction.df_exp_compo(url)

            st.write("Experience Individuelle:")
            st.dataframe(df_experience_match)
            st.write("Experience Equipe:")
            st.dataframe(df_summary)
        
            df_experience_match_excel = to_excel(df_experience_match)
            df_summary_excel = to_excel(df_summary)
        
            st.download_button(label="Download Data as Excel (Experience Match)",
                               data=df_experience_match_excel,
                               file_name="experience_match.xlsx",
                               mime="application/vnd.ms-excel")
        
            st.download_button(label="Download Data as Excel (Summary)",
                               data=df_summary_excel,
                               file_name="summary.xlsx",
                               mime="application/vnd.ms-excel")

if __name__ == "__main__":
    main()
