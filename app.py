import streamlit as st
from io import BytesIO
import pandas as pd
import fonction

st.set_page_config(layout="wide")

def main():
    
    st.title("Damien Je t'aime ❤️")
    
    uploaded_file = st.file_uploader("Importer le fichier CSV", type=["csv"])
    
    if uploaded_file is not None:

        st.write("File Uploaded Successfully!")
        
        if st.button("Process Images"):
            
            df = pd.read_csv(uploaded_file)

            img = fonction.kicking_plot(df)
            st.image(img)

            img = fonction.kicking_plot_adv(df)
            st.image(img)

if __name__ == "__main__":
    main()
