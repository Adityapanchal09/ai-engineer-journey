from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()  # automatically picks GROQ_API_KEY from .env

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! What can you help me with?"}
    ]
)

print(response.choices[0].message.content)