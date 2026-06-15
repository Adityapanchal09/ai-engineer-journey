import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client=Groq()

st.title=("AI STUDY ASSISTANT")

#Subject Selector-only runs once via session_state
if "subject" not in st.session_state:
    st.session_state.subject=""
if "messages" not in st.session_state:
    st.session_state.messages=[]


#Sidebar for Sunject Selection
with st.sidebar:
    st.header("Settings")
    subject=st.text_input("subject",value=st.session_state.subject)
    if st.button("start new session"):
        st.session_state.subject=subject
        st.session_state.messages=[]
        st.rerun()


#Show Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

#chat Input-built in Stream Element
user_input=st.chat_input("Ask Your Tutor...")

if user_input:
    #Show user message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role":"user","content":user_input})


#Build System Promp with Subject
system_prompt=f"Your are an expert{st.session_state.subject or 'general'} tutor.Explain Simply With Analogies"


#Get Ai Response
with st.chat_message("ASSISTANT"):
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role":"system","content":system_prompt}] + st.session_state.messages
            )
        reply = response.choices[0].message.content
        st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
