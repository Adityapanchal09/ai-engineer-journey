from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client=Groq()

with open("notes.txt","r") as f:
    content=f.read()


response=client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[{"role":"system","content":"You are a helpful Study Assistant"},
              {"role":"user","content":f"Summarize these notes content:\n\n{content}"}]


)    

print(response.choices[0].message.content)