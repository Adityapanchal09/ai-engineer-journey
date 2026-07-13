from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

#initialize the llm
llm=ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0.7
)

#simple call
response=llm.invoke("what is machine learning in one sentence?")
print(response.content)