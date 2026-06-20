from sentence_transformers import SentenceTransformer


model=SentenceTransformer("all-MiniLM-L6-v2")

text="deadlocks happen when process wait forever"
embedding=model.encode(text)

print(type(embedding))
print(embedding.shape)
print(embedding[:5])