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
        joke=response.json
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

#---Tool Registery---
TOOLS={
    "calculator":calculator,
    "word_counter":word_counter,
    "file_reader":read_file,
    "get_joke":get_joke,
    "summarize_text":summarize_text,
    "search_notes":search_notes,
    "save_memory":lambda x:save_memory(*x.split("|",1)) or "Saved!",
    "recall_memory":recall_memory

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


        # try to parse as tool call
        try:
            #tool_call=json.loads(reply)
            first_line = reply.strip().split("\n")[0]
            tool_call = json.loads(first_line)
            tool_name=tool_call["tool"]
            tool_input=tool_call["input"]

            if tool_name in TOOLS:
                print(f"\n Using tool:{tool_name}")
                print(f"input:{tool_input}")
                tool_result=TOOLS[tool_name](tool_input)
                print(f"result:{tool_result}")

                #feed result back to agent
                messages.append({"role":"assistant","content":reply})
                messages.append({"role":"user","content":f"tool_result:{tool_result}"})
            else:
                print(f"\n Answer:{reply}")

        except json.JSONDecodeError:
            # not a tool call this is a final answer
            #save final answer to shared history
            print(f"\nanswer:{reply}")
            conversation_history.append({"role":"assistant","content":reply})
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
