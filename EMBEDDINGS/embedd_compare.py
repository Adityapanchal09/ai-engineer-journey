from sentence_transformers import SentenceTransformer ,util

model=SentenceTransformer("all-MiniLM-L6-v2")

text1="deadlock happens when process stuck forever"
text2="process get stuck waiting for each other"
text3="my favourite pizza topping is pepperoni"

emb1=model.encode(text1)
emb2=model.encode(text2)
emb3=model.encode(text3)

similarity_1_2=util.cos_sim(emb1,emb2)
similarity_1_3=util.cos_sim(emb1,emb3)

print(f"Deadlock vs stuck Waiting:{similarity_1_2.item():.3f}")
print(f"Deadlock vs pizza topping:{similarity_1_3.item():.3f}")