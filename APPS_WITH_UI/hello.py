import streamlit as st

st.title("My First AI APP")
st.write("Hello!This is Running in browser")

name=st.text_input("WHAT's Your Name: ")
if name:
    st.write(f"Hello,{name}!")
