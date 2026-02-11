import streamlit as st

st.title("Campus AI Chatbot")

user_input = st.text_input("Ask a campus question:")

if user_input:
    st.write("You asked:", user_input)
