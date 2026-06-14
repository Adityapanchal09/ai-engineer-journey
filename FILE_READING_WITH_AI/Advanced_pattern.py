from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client=Groq()

with open("notes.txt") as f:
    document=f.read()


SYSTEM=f""" You are a study assistant. 
Answer questions based ONLY on the document below.
If the answer isn't in the document, say 'Not found in notes.'

DOCUMENT:
{document} """

history=[]

while True:
    question=input("Ask any Questions: ")
    if question.lower()=="quit":
        break

    history.append({"role":"user","content":question})    

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"system","content":SYSTEM}]+history
    )

    reply=response.choices[0].message.content
    history.append({"role":"system","content":reply})
    print(f"\nAI:{reply}\n")