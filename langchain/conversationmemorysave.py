from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage
from dotenv import load_dotenv

load_dotenv()


llm=ChatGroq(model="qwen/qwen3.6-27b",temperature=0.7)
parser=StrOutputParser()

prompt=ChatPromptTemplate.from_messages([
    ("system","You are a helpful AI engineering tutor.be concise."),
    MessagesPlaceholder(variable_name="history"),  #<-chat history goes here
    ("human","{question}") 
])

chain =prompt|llm|parser

#we manage history ourselves as list 
chat_history=[]

def chat(question):
    response=chain.invoke({
        "history":chat_history,
        "question":question
    })

    #save this turn to history
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response))
    return response

#multi turn conversation
print(chat("what is langcahin?"))
print("----")
print(chat("what did i just i ask you?"))