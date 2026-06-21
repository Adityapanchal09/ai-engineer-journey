from sentence_transformers import SentenceTransformer,util
from  groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()  # Automatically picks GROQ_API_KEY from .env
embedd_model=SentenceTransformer("all-MiniLM-L6-v2")

def load_and_chunk(filepath):
    with open(filepath,"r",encoding="utf-8") as f:
        text=f.read()

    #split by paragraph clean empty ones
    chunks=[c.strip() for c in  text.split("\n\n") if c.strip()]

    return chunks


#print(load_and_chunk(r"C:\Users\ADITYA PANCHAL\ai_engineer\MINI_RAG\notes.txt"))

def retrieve_relevant_chunks(query,chunks,chunk_embeddings,top_k=3,threshold=0.3):
    query_embedding=embedd_model.encode(query)
    similarities=util.cos_sim(query_embedding,chunk_embeddings)[0]
    top_indices=similarities.argsort(descending=True)[:top_k]

     # Only keep chunks above the similarity threshold
    relevant = []
    for i in top_indices:
        score = similarities[i].item()
        if score >= threshold:
            relevant.append(chunks[i])
    
    return relevant  # could be empty list if nothing is relevant enough!
    


def answer_question(query,relevant_chunks):
    context="\n\n".join(relevant_chunks)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content":f"""Answer the Question using only the context below.
             if the answer is not in the context ,say "Not Found in the Document."
             "CONTEXT:{context}"""},
            {"role": "user", "content":query}
        ]
    )

    return response.choices[0].message.content 


#---Main---
filepath=input("Enter path to your .txt file: ")
chunks=load_and_chunk(filepath)
print(f"\n✅ Loaded {len(chunks)} chunks")

print("Embedding all chunks...")
chunk_embeddings=embedd_model.encode(chunks)
print("Ready!ASk About questions of Your document.\n")

while True:
    query=input("You: ")
    if query.lower()=="quit":break

    relevant=retrieve_relevant_chunks(query,chunks,chunk_embeddings)

    if relevant:
        print("\n📌 Retrieved chunks:")
        for c in relevant:
            print(f"  - {c[:80]}...")
    if not relevant:
        print("\n🤖 Answer: Not found in the document (no relevant chunks found).\n")
    else:
        answer = answer_question(query, relevant)
        print(f"\n🤖 Answer: {answer}\n")