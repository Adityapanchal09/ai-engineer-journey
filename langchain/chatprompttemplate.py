from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm=ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0.7
)

#define a reusable prompt template with variables

prompt=ChatPromptTemplate.from_messages([
    ("system","You are an expert {domain} tutor.explain concepts simply and clearly"),
    ("human","{question}")
])

#chain the prompt and llm together with pipe operator
chain=prompt|llm

#invoke with variables filled in 
response=chain.invoke({
    "domain":"AI Engineering",
    "question":"what is vector database and why do we need it?"
})

print(response.content)
