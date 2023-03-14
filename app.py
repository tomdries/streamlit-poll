import streamlit as st
import pandas as pd
from IPython.display import HTML

# Load data from CSV
data = pd.read_csv('data.csv')

# Define function to display video player
def show_video(url):
    html = f'<iframe width="560" height="315" src="{url}" frameborder="0" allowfullscreen></iframe>'
    st.write(HTML(html), unsafe_allow_html=True)

# Define main function to run the app
def main():
    # Set app title
    st.title("Search and Play YouTube Videos")

    # Add search bar to sidebar
    query = st.sidebar.text_input("Search for Videos")

    # Filter data based on search query
    results = data[data['text'].str.contains(query, case=False)]

    # Display search results in main panel
    for i, row in results.iterrows():
        if st.button(row['text']):
            show_video(row['start_link'])

if __name__ == '__main__':
    main()