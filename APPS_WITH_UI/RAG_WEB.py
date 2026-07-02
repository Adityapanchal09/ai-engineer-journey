import streamlit as st
from groq import Groq
from sentence_transformers import SentenceTransformer,util
from dotenv import load_dotenv
import os

#load_dotenv()
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

client=Groq()

st.title("CHAT WITH YOUR NOTES!")
st.caption("Upload a .txt file and ask questions about it")

#---Cache the model so it loads only once----
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedd_model=load_model()

#---Session State---
if "messages" not in st.session_state:
    st.session_state.messages=[]
if "chunks" not in st.session_state:
    st.session_state.chunks=None
if "chunk_embeddings" not in st.session_state:
    st.session_state.chunk_embeddings=None


#---Functions---
def chunk_text(text):
    text = text.replace("\r\n", "\n")  # normalize Windows line endings
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    return chunks

def retrieve(query,chunks,embeddings,messages,top_k=3,threshold=0.3):
    # find the last user message before the current one
    user_messages = [m for m in messages if m["role"] == "user"]
    
    if len(user_messages) >= 2:
        prev_user_q = user_messages[-2]["content"]  # previous user question
        expanded_query = f"{prev_user_q} {query}"
    else:
        expanded_query = query
    
    print("Expanded query:", expanded_query[:100])  # keep debug for now
    
    q_emb = embedd_model.encode(expanded_query)
    sims = util.cos_sim(q_emb, embeddings)[0]
    top_idx = sims.argsort(descending=True)[:top_k]
    
    print("Top scores:", [round(sims[i].item(), 3) for i in top_idx])
    
    return [chunks[i] for i in top_idx if sims[i].item() >= threshold]
    



def answer(query,relevant_chunks):
    context="\n\n".join(relevant_chunks)
    response=client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role":"system","content":f"""Answer only using the CONTEXT below,
             if answer not in context,say"Not found in the document"
             context:{context} """},{
                 "role":"user","content":query
             }
        ]
    )
    return response.choices[0].message.content


#---Side bar:file upload---
with st.sidebar:
    st.header("Upload Document")
    uploaded=st.file_uploader("choose a .txt file: ",type=["txt"])    

    if uploaded and st.button("Process Document"):
        with st.spinner("Chimking and Embedding..."):
            text=uploaded.read().decode("utf-8")
            chunks=chunk_text(text)
            embeddings=embedd_model.encode(chunks)
            st.session_state.chunks=chunks
            st.session_state.chunk_embeddings=embeddings
            st.session_state.messages=[]
        st.success(f"{len(chunks)} chunks ready!")
        

    if st.session_state.chunks:
        st.info(f"📊 {len(st.session_state.chunks)} chunks loaded")


#---Main Area---
if not  st.session_state.chunks:
    st.info("Upload a .txt file at sidebar to start chatting")
else:
    #show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if "chunks" in msg:
                with st.expander("Retrieved Chunks"):
                    for c in msg["chunks"]:
                        st.write(c)
                        st.divider()

    #chat input---
    query=st.chat_input("Ask about your document...")

    if query:
        with st.chat_message("user"):
            st.write(query)
        st.session_state.messages.append({"role":"user","content":query})

        with st.chat_message("assistant"):
            with st.spinner("searching and answering..."):
                relevant=retrieve(
                    query,
                    st.session_state.chunks,
                    st.session_state.chunk_embeddings,
                    st.session_state.messages
                )

                if not relevant:
                    reply="Not found in the document"
                    relevant=[]
                else:
                    reply=answer(query,relevant)
                st.write(reply)
                if relevant:
                    with st.expander("Retrievd chunks"):
                        for c in relevant:
                            st.write(c)
                            st.divider()

        st.session_state.messages.append({
            "role":"assistant",
            "content":reply,
            "chunks":relevant
        })                                                    