from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

llm=ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0.7

)

prompt=ChatPromptTemplate.from_messages([
    ("system","You are an expert {domain} tutor,Explain concepts simply and clearly"),
    ("human","{question}")
])


#full chain:prompt->llm->parser
parser=StrOutputParser()
chain=prompt|llm|parser

response=chain.invoke({
    "domain":"AI Engineering",
    "question":"what is langchain in 2 sentences"
})

print(response)