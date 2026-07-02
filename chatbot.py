from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()
history = []

print("Chat with AI (type 'quit' to exit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Bye!")
        break

    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role": "system", "content": "You are a helpful study assistant for a CS student."}
        ] + history
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    print(f"\nAI: {reply}\n")