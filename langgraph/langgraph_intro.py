from langgraph.graph import StateGraph,END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from typing import TypedDict,List
from dotenv import load_dotenv
import re

load_dotenv(r"C:\Users\ADITYA PANCHAL\ai_engineer\.env")

#step1 -define state
#this is the shared data that flows through every node
class State(TypedDict):
    messages:List[str]
    response:str
    needs_summary:bool


#step2 -define a node(just a python function) Node1-Chat node
llm=ChatGroq(model="qwen/qwen3.6-27b",temperature=0.7)

def chat_node(state:State)->State:
    #get the last message from state
    user_message=state["messages"][-1]
    #call the llm
    response=llm.invoke([HumanMessage(content=user_message)])
    clean=re.sub(r'<think>.*?</think>','',response.content,flags=re.DOTALL).strip()


    #if response is long flat it for summarization
    needs_summary=len(clean)>300
    print(f"Response length: {len(clean)}")  # ← add this
    print(f"needs_summary set to: {needs_summary}")


     # return ALL state keys, not just the ones you changed
    return {
        "messages": state["messages"],
        "response": clean,
        "needs_summary": needs_summary
    }

#step 3-Node 2:Summary node(only runs if response is long)
def summary_node(state:State)->State:
    response=state["response"]
    print(f"Summarizing: '{response}'")  # ← add this
    summary_prompt=f"Summarize this in one sentence:\n\n{response}"
    summary=llm.invoke([HumanMessage(content=summary_prompt)])
    clean=re.sub('<think>.*?</think>','',summary.content,flags=re.DOTALL).strip()
    return {"response":f"SUMMARY:{clean}"}


#step4 - conditional edge function
#decides which node to go to next based on state
def should_summarize(state:State)->str:
    if state["needs_summary"]:
        return "summarize"  #-> goes to summary node
    else:
        return "end" #->goes to end 


#step 5 -buid the graph
graph_builder=StateGraph(State)

graph_builder.add_node("chat",chat_node)
graph_builder.add_node("summarize",summary_node)

#set entry point
graph_builder.set_entry_point("chat")
#conditional edge- chat node decides what comes next
graph_builder.add_conditional_edges(
    "chat",#from this node 
    should_summarize,#call this function to decide
    {
        "summarize":"summarize",#if returns summarize go to summarize node
        "end":END#if returns end->finish
    }
)
graph_builder.add_edge("summarize",END)

#compile the graph
graph=graph_builder.compile()
#test with a question that gives long answer
print("=====TEST 1====Short answer no summary")
result1=graph.invoke({
    "messages":["what is python in one word?"],
    "response":"",
    "needs_summary":False
})

print("Response:",result1["response"])

print("=====TEST 2====long answer triggers summary node")
result2=graph.invoke({
    "messages":["explain how neural networks in detail"],
    "response":"",
    "needs_summary":False
})

print("Response:",result2["response"])