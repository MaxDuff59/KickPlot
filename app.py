import streamlit as st
from io import BytesIO
import pandas as pd
import fonction

st.set_page_config(layout="wide")

def main():
    
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

if __name__ == "__main__":
    main()
