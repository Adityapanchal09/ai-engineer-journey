from groq import Groq
from dotenv import load_dotenv
import json,math,os

load_dotenv()
client=Groq()

#---Define Tools Plain python functions----
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
        model="llama-3.3-70b-versatile",
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
from duckduckgo_search import DDGS

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
-read_file:reads a text file. Input:file path
-get_joke:fetches a random joke ,Input:any topic string
-summarize_text:summarizes a long text in 2 sentences. Input:the text to summarize
-search_notes:searches  your os notes semantically. Input:a question about os concepts
-save_memory:# In TOOL_DESCRIPTIONS change save_memory description to:
- save_memory: saves a fact permanently. Input format MUST be 'key|value' where key is a simple label. Example: 'name|Aditya' or 'learning|AI Engineering'
-recall_memory:recalls a saved fact. Input:the key
-websearch:searches the web for current information. Input:search query string

If you dont need a tool respond normally with your answer
"""
conversation_history=[] #lives outside run_agent()

def run_agent(user_task):
    print(f"\n TASk:{user_task}")

    #Add new task to shared history
    conversation_history.append({"role":"user","content":user_task})

    messages=[
        {"role":"system","content":TOOLS_DESCRIPTION},
        {"role":"user","content":user_task}
    ]+conversation_history #include all previous exchanges,

    #Agent loop max 5 iterations to prevent for infinite loops
    for i in range(5):
        response=client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        reply=response.choices[0].message.content.strip()


      # Try to parse as a tool call by extracting everything between { and }
        try:
            # Find the start and end of the JSON object in the reply
            start_idx = reply.find('{')
            end_idx = reply.rfind('}')
            
            # If we found curly braces, extract that specific chunk
            if start_idx != -1 and end_idx != -1:
                json_str = reply[start_idx:end_idx+1]
                tool_call = json.loads(json_str)
                tool_name = tool_call["tool"]
                tool_input = tool_call["input"]
                
                print(f"\n Using tool: {tool_name}")
                print(f" input: {tool_input}")
                
                # Execute the tool
                tool_result = TOOLS[tool_name](tool_input)
                print(f" result: {tool_result}")
                
                # Feed result back to agent
                messages.append({"role": "assistant", "content": reply})
                messages.append({"role": "user", "content": f"tool_result: {tool_result}"})
                
            else:
                # No curly braces found, this must be a pure text final answer
                raise json.JSONDecodeError("No JSON found", reply, 0)
                
        except json.JSONDecodeError:
            # Not a tool call, this is a final answer
            print(f"\n Final Answer: {reply}")
            conversation_history.append({"role": "assistant", "content": reply})
            break

#---test the agent----
'''run_agent("what is 1234 multiplied by 5678")
run_agent("count the words in:the quick brown fox runs over the lazy dog")
run_agent("What is the capital of France?") #no tool needed
run_agent("tell me a joke")
run_agent("Search my notes for information about memory management")
run_agent("what si 144 divided by 12 ,then tell me a joke")#multi tool'''
#run_agent("Remember that my name is Aditya and i am learning AI Engineering")
run_agent("what is my name and what i am learning?")
run_agent("What is the latest news about AI today?")
run_agent("Search for python 3.13 new features")
run_agent("What is the current Groq API limit?")
run_agent("search for best practices for RAG systems in 2026")