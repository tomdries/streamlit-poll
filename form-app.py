import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define Google Sheets credentials and sheet name
sheet_name = 'Form-app'
secret_file = 'client_secret.json'

gc = gspread.service_account(filename=secret_file)

# Define main function to run the app
def main():
    # Set app title
    st.title("Collect User Input")

    # Add a text input field to the app
    user_name = st.text_input("Name")

    # Add a slider to the app
    input_slider = st.slider("Choose a number", 0, 10, 5)

    # # Add a button to the app
    if st.button("Add to Sheet"):
        
        # insert row
        sh = gc.open(sheet_name)
        # timestamp = st._arrow.now()
        sh.sheet1.insert_row([user_name, input_slider], 2)
 


if __name__ == '__main__':
    main()