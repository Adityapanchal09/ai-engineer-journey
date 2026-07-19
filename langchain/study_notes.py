from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import re

load_dotenv(r"C:\Users\ADITYA PANCHAL\ai_engineer\.env")

#step1 Load the document
loader=TextLoader("notes.txt")
documents=loader.load()

print(f"loaded {len(documents)} documents")
print(f"Total Characters:{len(documents[0].page_content)}")

#step2 split into chunks
splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,#max characters per chunk
    chunk_overlap=50 #overlap chunks between context so it doesnt gets lost at boundaries
)

chunks=splitter.split_documents(documents)
print(f"Total Chunks:{len(chunks)}")

#step3 Embedd
print("loading Embedding Model...")
embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-V2")

#step4 Store in FAISS
print("Building vector Store...")
vectorstore=FAISS.from_documents(chunks,embeddings)
print("vector store Ready")

#step5 Create Retriever
Retriever=vectorstore.as_retriever(search_kwargs={"k":2})

#step6 Answer Prompt
prompt=ChatPromptTemplate.from_template(""" 
You are a helpful study assistant. Answer the question based ONLY on the following study notes.
If the answer is not in the notes, say "This topic isn't covered in your notes."

Study Notes:
{context}

Question: {question}""")

#step7 LLM
llm=ChatGroq(model="qwen/qwen3.6-27b",temperature=0)
parser=StrOutputParser()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


#step 8 FULL CHAIN
rag_chain=(
    {"Study Notes":Retriever|format_docs,"question":RunnablePassthrough()}|prompt|llm|parser
)

#step 9 clean the answer

def clean_response(text:str)->str:
    text=re.sub(r'<think>.*?</think>','',text,flags=re.DOTALL)
    return text.strip()

#test it
print("📚 Study Notes Chatbot — Ask me anything from your notes!")
print("Type 'quit' to exit\n")

while True:
    question=input("\nAsk a question(or 'quit to exit')")
    if question.lower()=="quit":
        break
    answer=rag_chain.invoke(question)
    print(f"Answer:{clean_response(answer)}")
