from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

subject = input("Which subject do you want to study? ")

SYSTEM_PROMPT = f"""You are a strict {subject} viva examiner at a university.
- Ask one question at a time
- If the answer is correct, say 'Correct' and ask the next question
- If wrong, say 'Incorrect' and give a hint, then ask again
- After 5 questions give a score out of 5
- Start by saying 'Viva starting. First question:'
"""

history = []
print(f"\n📚 {subject} Study Assistant ready! Type 'quit' to end.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Session ended. Keep studying! 💪")
        break

    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    print(f"\nTutor: {reply}\n")