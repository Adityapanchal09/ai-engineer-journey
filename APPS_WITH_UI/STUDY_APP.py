import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = Groq()

st.title("AI STUDY ASSISTANT")   # also fix: remove the "=" — explained below

def load_history(filename="chat_history.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_history(messages, filename="chat_history.json"):
    with open(filename, "w") as f:
        json.dump(messages, f, indent=2)

# Subject Selector — only runs once via session_state
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "messages" not in st.session_state:
    st.session_state.messages = load_history()   # ✅ load saved history on startup

# Sidebar for subject selection
with st.sidebar:
    st.header("Settings")
    subject = st.text_input("subject", value=st.session_state.subject)
    if st.button("start new session"):
        st.session_state.subject = subject
        st.session_state.messages = []
        st.rerun()

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Ask Your Tutor...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    system_prompt = f"You are an expert {st.session_state.subject or 'general'} tutor. Explain simply with analogies."

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    save_history(st.session_state.messages)   # ✅ save only when a new message is added