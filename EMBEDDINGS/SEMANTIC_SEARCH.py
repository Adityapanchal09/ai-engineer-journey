from sentence_transformers import SentenceTransformer,util

model=SentenceTransformer("all-MiniLM-L6-v2")

notes=[
    "Deadlock occurs when processes wait for each other forever",
    "Paging divides memory into fixed size blocks",
    "FCFS is the simplest CPU scheduling algorithm",
    "A mutex prevents two threads from accessing shared data simultaneously",
    "Virtual memory lets programs use more memory than physically available",
    "Round robin scheduling gives each process a fixed time slice",
    "Segmentation divides memory based on logical program units",
]

#convert all motes to embeddings once
note_embeddings=model.encode(notes)

def search(query,top_k=3):
    query_embedding=model.encode(query)

    #compare query to all notes at once
    similarities=util.cos_sim(query_embedding,note_embeddings)[0]

    #get indices of top matches highest similarity first
    top_results=similarities.argsort(descending=True)[:top_k]

    print(f"\n🔍 Search: '{query}'\n")
    for idx in top_results:
        score=similarities[idx].item()
        print(f"[{score:.3f}] {notes[idx]}")


#try-----
search("why do programms get stuck")
search("why do memory gets split up")
search("fair CPU time sharing")
