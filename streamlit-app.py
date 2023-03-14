import streamlit as st
import openai

# Set up OpenAI API key
openai.api_key = st.text_input('API key please:')

# Create input field for user's query
query = st.text_input('Query please:')

# Define function to generate OpenAI response


def generate_response():
    out = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}    ]
    )
    response = out.choices[0]["message"]["content"]
    return response


# Create button to generate OpenAI response
if st.button('Generate Response'):
    response = generate_response()
    st.write(response)


