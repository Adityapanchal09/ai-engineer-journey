import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import json,os,re,requests,time
from ddgs import DDGS

load_dotenv() # works locally

#works on streamlit cloud too-checks secrets first
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"]=st.secrets["GROQ_API_KEY"]
client=Groq()

st.title("AI AGENT")
st.caption("Multi-tool web agent with websearch,calculator,memory and more")

#---Session State----
if "messages" not in  st.session_state:
    st.session_state.messages=[]        #chat display history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history=[]  #agent context history 

#---tool functions---
def calculator(expression:str)->str:
    try:
        result=eval(expression)
        return f"result:{result}"
    except:
        return "Error: Invalid expression"
    

def word_counter(text:str)->str:
    words=len(text.split())
    chars=len(text)
    return f"words:{words},characters:{chars}"


def read_file(filepath:str)->str:
    try:
        with open(filepath,"r") as f:
            return f.read()[:500] #first 500 charcters
    except:
        return "Error:File not found!"

import requests

def get_joke(topic:str)->str:
    try:
        response=requests.get("https://official-joke-api.appspot.com/random_joke")
        joke=response.json()
        return f"{joke['setup']}.....{joke['punchline']}"
    except:
        return "Could not fetch joke"

def summarize_text(text:str)->str:
    response=client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role":"system","content":"summarize in 2 sentences"},
            {"role":"user","content":text}
        ]
    )    

    return response.choices[0].message.content

from sentence_transformers import SentenceTransformer,util

search_model=SentenceTransformer("all-MiniLM-L6-v2")

knowledge_base=[
    "Deadlock occurs when processes wait for each other forever",
    "Paging divides memory into fixed size blocks",
    "FCFS is the simplest CPU scheduling algorithm",
    "Round robin gives each process a fixed time slice",
]
kb_embeddings=search_model.encode(knowledge_base)   

def search_notes(query:str)->str:
    q_emb=search_model.encode(query)
    sims=util.cos_sim(q_emb,kb_embeddings)[0]
    top_idx=sims.argsort(descending=True)[:2]
    results=[knowledge_base[i] for i in top_idx]
    return "\n".join(results)


MEMORY_FILE="agent_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE) as f:
            return json.load(f)
    return {}

def save_memory(key,value):
    memory=load_memory()
    memory[key]=value
    with open(MEMORY_FILE,"w") as f:
        json.dump(memory,f,indent=2) 

def recall_memory(key):
    memory=load_memory()
    return memory.get(key,"nothing stored for that key")

import time 
from ddgs import DDGS

def websearch(query:str)->str:
    try:
        # 1. Add a 1.5 second delay so DuckDuckGo doesn't block the rapid requests
        time.sleep(1.5)

        with DDGS() as ddgs:
            results=list(ddgs.text(query,max_results=5))
        if not results:
            return "NO result found.Try simplifying your query to just 2 or 3 core keywords"

        #format top 3 reults
        output=[]

        for r in results[:3]:
            # Safely grab the text just in case a field is missing
            title = r.get('title', 'Unknown Title')
            body = r.get('body', 'No summary available.')
            output.append(f"Title:{r['title']}\nSummary:{r['body']}")
        return "\n".join(output)
    except Exception as e:
        return f"Search Failed:{str(e)}"        

#---Tool Registery---
TOOLS={
    "calculator":calculator,
    "word_counter":word_counter,
    "file_reader":read_file,
    "get_joke":get_joke,
    "summarize_text":summarize_text,
    "search_notes":search_notes,
    "save_memory":lambda x:save_memory(*x.split("|",1)) or "Saved!",
    "recall_memory":recall_memory,
    "websearch":websearch

}            

#Tools Description sent to the AI---
TOOLS_DESCRIPTION="""
You Have access to these tools, to use them respond with only JSON object:
{"tool":"tool_name","input":"your input here"}

Availabe Tools:
-calculator: evaluates with expressions, Input:math expression "2+2" or "15*8"
-word_counter: counts word and characters. Input:any text string
-file_reader:reads a text file. Input:file path
-get_joke:fetches a random joke ,Input:any topic string
-summarize_text:summarizes a long text in 2 sentences. Input:the text to summarize
-search_notes:searches  your os notes semantically. Input:a question about os concepts
-save_memory:# In TOOL_DESCRIPTIONS change save_memory description to:
- save_memory: saves a fact permanently. Input format MUST be 'key|value' where key is a simple label. Example: 'name|Aditya' or 'learning|AI Engineering'
-recall_memory:recalls a saved fact. Input:the key
-websearch:searches the web for current information. Input:search query string

If you dont need a tool respond normally with your answer
"""

#---sidebar: memory panel---
with st.sidebar:
    st.header("Agent Memory")
    if os.path.exists("agent_memory.json"):
        with open("agent_memory.json") as f:
            memory=json.load(f)
        for k,v in memory.items():
            st.write(f"**{k}:** {v}")    
    else:
        st.write("No memories yet.")

    if st.button("Clear memory"):
        if os.path.exists("agent_memory.json"):
            os.remove("agent_memory.json")
        st.rerun()

#---chat Display---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "tools_used" in msg and msg["tools_used"]:
            with st.expander("Tools used"):
                for log in msg["tools_used"]:
                    st.write(f"**{log['tool']}** -> {log['result'][:150]}...")

#---chat input + agent loop---
user_input=st.chat_input("Ask your agent anything...")

if user_input:
    #show user input
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role":"user","content":user_input})

    #add to conversation history (same as terminal version)
    st.session_state.conversation_history.append({"role":"user","content":user_input})

    #build messages list same as your run_agent()
    messages=[
        {"role":"system","content":TOOLS_DESCRIPTION},
        {"role":"user","content":user_input}]
    tools_used=[]
    final_reply=""

    with st.chat_message("Assistant"):
        with st.spinner("Agent thinking..."):
             # Agent loop — same logic as your for i in range(5)
            for i in range(5):
                response = client.chat.completions.create(
                    model="qwen/qwen3.6-27b",
                    messages=messages
                )
                reply = response.choices[0].message.content.strip()
 
                # same JSON extraction logic as your AGENT.py
                json_matches = re.findall(r'\{[^{}]+\}', reply)

                if json_matches:
                    try:
                        tool_call = json.loads(json_matches[0])
                        tool_name = tool_call["tool"]
                        tool_input = tool_call["input"]

                        if tool_name in TOOLS:
                            tool_result=TOOLS[tool_name](tool_input)
                            tools_used.append({
                                "tool":tool_name,
                                "input":tool_input,
                                "result":str(tool_result)
                            })

                             # feed result back — same as terminal version
                            messages.append({"role": "assistant", "content": reply})
                            messages.append({"role": "user", "content": f"tool_result: {tool_result}"})
                            continue
 
                    except (json.JSONDecodeError, KeyError):
                        pass
 
                # no tool call found — this is the final answer
                final_reply = reply
                break

            #display final answer+tools used
            st.write(final_reply)
            if tools_used:
                with st.expander("Tools used"):
                    for log in tools_used:
                        st.write(f"**{log['tool']}** (`{log['input'][:50]}`)->{log['result'][:150]}")


            #save session state
            st.session_state.conversation_history.append({"role":"assistant","content":final_reply})
            st.session_state.messages.append({
                "role":"assistant", 
                "content":final_reply,
                "tools_used":tools_used
            })            
            st.rerun()