import streamlit as st
from io import BytesIO
import pandas as pd
import fonction

st.set_page_config(layout="wide")

def main():

    tab1, tab2, tab3, tab4 = st.tabs(["Game Analysis Kicking","Player Analysis Kicking","Opponent Analysis Kicking","Experience Collective"])

    with tab1:
        
        st.title("Game Analysis Kicking 🔵⚪️")
        
        uploaded_file = st.file_uploader("Importer le fichier CSV", type=["csv"],key="file_uploader1")
        
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
    
                img = fonction.kicking_plot_adv(df,opta=False)
                st.image(img)

    with tab2:

        st.title("Player Analysis Kicking 🔵⚪️")
        
        uploaded_files = st.file_uploader("Importer le(s) fichier(s) CSV", type=["csv"], accept_multiple_files=True,key="file_uploader2")

        if uploaded_files:

            df = pd.concat((pd.read_csv(file) for file in uploaded_files))
            st.write("File(s) Uploaded Successfully!")
            
            df_kicks = df[df.Row == "17.JAP Racing 92"].reset_index(drop=True)

            list_player = st.multiselect("Choix du Joueur : ",[player for player in list(df_kicks.Joueurs.unique())])

            st.text(list_player)

            if st.button("Process Images"):
    
                df_players = df_kicks[df_kicks.Joueurs.isin(list_player)].reset_index(drop=True)

                img = fonction.kicking_plot_players(df_players,list_player)
                st.image(img)

    with tab3:

        st.title("Opponent Analysis Kicking 🔵⚪️")
        
        uploaded_opponent = st.file_uploader("Importer le(s) fichier(s) CSV", type=["csv"], accept_multiple_files=True, key="file_uploader3")

        if uploaded_opponent:

            df = pd.concat((pd.read_csv(file) for file in uploaded_opponent))
            st.write("File(s) Uploaded Successfully!")

            teams = [value.replace(" Restart","") for value in list(df[(df.Row.str.contains('Restart'))&(df.Row.str.contains('Reception') == False)].reset_index(drop=True).Row.unique())]
            
            team = st.selectbox("Choix de l'équipe : ",teams)
            team_kick = team + " Kicks"

            if st.button("Process Images"):
    
                df_team = df[df.Row == team_kick].reset_index(drop=True)

                img = fonction.kicking_plot_adv(df_team,opta=True)
                st.image(img)

    with tab4:
        st.title('Collective Experience')

        url = st.text_input('URL du match : ', '')

        if st.button('Téléchargement des données'):
            # Only run this when the button is clicked
            df_experience_match, df_summary = fonction.df_exp_compo(url)

            st.write("Experience Individuelle:")
            st.dataframe(df_experience_match)
            st.write("Experience Equipe:")
            st.dataframe(df_summary)

            df_experience_match_excel = fonction.to_excel(df_experience_match)

            st.download_button(label="Download Data as Excel (Experience Individuelle)",
                            data=df_experience_match_excel,
                            file_name="experience_match.xlsx",
                            mime="application/vnd.ms-excel")


if __name__ == "__main__":
    main()
