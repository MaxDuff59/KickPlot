import streamlit as st
from io import BytesIO
import pandas as pd
import fonction
import matplotlib.pyplot as plt
import io
from PIL import Image
import numpy as np

st.set_page_config(layout="wide")

def main():

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Game Analysis Kicking","Player Analysis Kicking","Opponent Analysis Kicking","Experience Collective","Playmaker Mapping"])

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

            kick_types = st.multiselect("Choix du Jeu au Pied : ",[kick for kick in list(df_kicks['Type de jeu au pied'].unique())])

            st.text(kick_types)

            if st.button("Process Images"):
    
                df_players = df_kicks[df_kicks.Joueurs.isin(list_player)].reset_index(drop=True)

                img = fonction.kicking_plot_players(df_players,list_player,kick_types)
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

    with tab5:
        st.title("Playmaker Mapping")

        df_playmaker = pd.read_csv('df_playmaker.csv')

        player_ = st.multiselect('Choix du Joueur :',[player for player in df_playmaker.player.unique()])

        if st.button("Process Mapping"):

                playmaker_nolann = df_playmaker[df_playmaker.player.isin(player_)].reset_index(drop=True)[['team','player','x_coord','y_coord','Actionresult']]
                playmaker_nolann['ActionColor'] = np.select([playmaker_nolann.Actionresult.str.contains('Pass'),playmaker_nolann.Actionresult.str.contains('Kick'),playmaker_nolann.Actionresult.str.contains('Carry')],['lightblue','darkgreen','red'])
                playmaker_nolann['x_coord_graph'] = playmaker_nolann['x_coord'].astype('int') + 10

                action_types = playmaker_nolann['Actionresult'].unique()
                    
                for action_type in action_types:
                    
                    subset = playmaker_nolann[playmaker_nolann['Actionresult'] == action_type]
                
                    (fig, ax) = fonction.draw_pitch_horizontal_v2() 
                    plt.ylim(-2, 72)
                    plt.xlim(-2, 120.4)
                    plt.axis('off')
                    
                    hb = ax.hexbin(subset['x_coord_graph'], subset['y_coord'], gridsize=10, cmap='Reds', mincnt=1)
                    
                    cb = fig.colorbar(hb, ax=ax)
                    cb.set_label('Counts')
                    plt.title(action_type.replace('Playmaker Option - ','') + ' - ' + player_[0],fontsize=14,fontweight='semibold')
                    
                    buf = io.BytesIO()
                    fig.savefig(buf)
                    buf.seek(0)
                    img = Image.open(buf)
                    st.image(img)

if __name__ == "__main__":
    main()
