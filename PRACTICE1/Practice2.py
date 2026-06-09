from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client=Groq()
history=[]

print("chat with AI\n")

while True:
    user_input=input("You: ")

    if user_input.lower()=="quit":
        print("bye")
        break

    history.append({"role":"user","content":user_input})

    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role":"system","content":"hi i am your study ai,ask me anything"

        }]+history
    )

    reply=response.choices[0].message.content
    history.append({"role":"assistant","content":reply})

    print(f"\n AI:{reply}\n")