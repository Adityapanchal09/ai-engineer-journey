import streamlit as st
# your other imports

# 1. Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Load heavy resources once
@st.cache_resource
def load_model():
    return YourModel()
model = load_model()

# 3. Copy ALL your functions unchanged
def tool1(): ...
def tool2(): ...
TOOLS = {...}
DESCRIPTION = "..."

# 4. Sidebar
with st.sidebar:
    st.header("Settings")
    st.write(...)

# 5. Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. Handle new input
user_input = st.chat_input("Type here...")
if user_input:
    # save input
    st.session_state.messages.append({"role":"user","content":user_input})
    
    # show input
    with st.chat_message("user"):
        st.write(user_input)
    
    # run your logic (what was inside run_agent())
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = your_logic(user_input)
        st.write(reply)
    
    # save output
    st.session_state.messages.append({"role":"assistant","content":reply})
    
    # rerun LAST
    st.rerun()