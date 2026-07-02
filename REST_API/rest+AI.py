import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client=Groq()

fact_response=requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random",params={"langauge":"en"})
fact=fact_response.json()["text"]
print(f"Fact:{fact}")

response=client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[{
        "role":"system","content":"You are a curious Science Explainer"

    },{
        "role":"user","content":f"Explain this fact in 3 sentences:{fact}"
    }]
)

print(f"\nAI: explaination:",response.choices[0].message.content)