from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client=Groq()

response=client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role":"system", "content":"explain technical terms to me like i am a 10 year old"},
    {"role":"user","content":"explain what is API in simple terms"}
    ]
     
)

reply=response.choices[0].message.content
print(reply)