import os
import re
from typing import Annotated,TypedDict

from ddgs import DDGS
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage,SystemMessage
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv

load_dotenv()


#1.DEFINE TOOLS
@tool
def calculator(expression:str)->str:
    """Evaluate a basic math expression. Input like '12 * 7 + 3'."""
    try:
        result=eval(expression,{"__builtins__":{}})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
    

@tool
def get_word_length(word:str)->str:
    """Return the number of characters in a given word."""
    return str(len(word))



@tool
def web_search(query:str)->str:
    """Search the web for current information not known from training data,
    such as recent events, current prices, or live facts. Input a search query
    string like 'current population of Vadodara'."""
    try:
        results=DDGS().text(query,max_results=3)
        if not results:
            return "No results Found"
        formatted=[]
        for r in results:
            title=r.get("title","")
            body=r.get("body","")
            formatted.append(f"-{title}:{body}")
        return "\n".join(formatted)
    except Exception as e:
        return f"Error performing search:{e}" 

tools=[calculator,get_word_length,web_search]       
    


#2.DEFINE STATE
class AgentState(TypedDict):
    messages:Annotated[list,add_messages]


#3.SETUP THE LLM
llm=ChatGroq(
    model="qwen/qwen3.6-27b",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0
) 

#Bind tools to LLM
llm_with_tools=llm.bind_tools(tools)


def strip_think_block(text:str)->str:
    """Your usual Qwen3 think-block stripper."""
    return re.sub(r"<think>.*?</think>","",text,flags=re.DOTALL).strip()


#4.DEFINE NODES
def agent_node(state:AgentState):
    """The 'brain' node. Looks at the conversation so far and either:
       (a) calls a tool, or
       (b) responds directly with a final answer.
    """
    response=llm_with_tools.invoke(state["messages"])

    if isinstance(response.content,str):
        response.content=strip_think_block(response.content)
    return {"messages":[response]}    


#5.BUILD THE GRAPH
graph_builder=StateGraph(AgentState)

graph_builder.add_node("agent",agent_node)
graph_builder.add_node("tools",ToolNode(tools))


graph_builder.add_edge(START,"agent")

graph_builder.add_conditional_edges(
    "agent",
    tools_condition
)

graph_builder.add_edge("tools","agent")

#6.ADD PERSISTENT MEMORY
memory=MemorySaver()
graph=graph_builder.compile(checkpointer=memory)

#7.RUN IT
def chat(user_input:str,thread_id:str="session-1"):
    config={"configurable":{"thread_id":thread_id}}
    result=graph.invoke(
        {"messages":[HumanMessage(content=user_input)]},
        config=config,
    )
    return result["messages"][-1].content


print("======turn1======")
print(chat("Search for the current population of Vadodara, then tell me "
                "what that number would be if it doubled. Use the calculator "
                "tool for the doubling step."))


print("=====turn2=====")
print(chat("what was the double number you just calculated?"))