from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv(r"C:\Users\ADITYA PANCHAL\ai_engineer\.env")



#step1 load the document
loader=TextLoader("notes.txt")
documents=loader.load()

print(f"loaded {len(documents)} documents")
print(F"total characters:{len(documents[0].page_content)}")


#step2 split into chunks
splitter=RecursiveCharacterTextSplitter(
    chunk_size=500, #max characters per chunk
    chunk_overlap=50 #overlap between chunks so context is'nt lost at boundaries

)

chunks=splitter.split_documents(documents)

print(f"Total chunks:{len(chunks)}")

#step3 embedd
print("loading Embedding Model...")
embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-V2")

#step4 store in FAISS
print("building vector store...")
vectorstore=FAISS.from_documents(chunks,embeddings)
print("vector store ready")

#step 5 create retriever
retriever=vectorstore.as_retriever(search_kwargs={"k":2})

#step6 RAG prompt
prompt=ChatPromptTemplate.from_template("""
Answer the Question based only on the following context.
If the answer is not in the context,say "I don't know based on the provided notes".
Context:{context} Question:{question}  """)

#step 7 LLM
llm=ChatGroq(model="qwen/qwen3.6-27b",temperature=0)
parser=StrOutputParser()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


#step 8 RAG full chain
rag_chain=(
    {"context":retriever|format_docs,"question":RunnablePassthrough()}|prompt|llm|parser
)

#test it
questions=[
    "what is RAG?",
    "WHAT is FAISS?",
    "what is capital of FRANCE?" #not in notes should say -i don't know
]

for q in questions:
    print(f"Q:{q}")
    print(f"A:{rag_chain.invoke(q)}")
    print("-----")