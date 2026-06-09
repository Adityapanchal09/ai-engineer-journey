from groq import Groq
from dotenv import load_dotenv

load_dotenv()
history=[]

client=Groq()

print("VIVA BOT: ASK VIVA QUESTIOONS TO BOT\n")

while True:
    user_input=input("VIVA EXAMINER(YOU): ")
    if user_input.lower()=="quit":
        print("VIVA HAS ENDED!")
        break

    history.append({"role":"user","content":user_input})

    response=client.chat.completions.create(

        model="llama-3.3-70b-versatile",
        messages=[{
            "role":"system","content":"you are a student giving a viva of operating systems"
        }]+history

    )

    reply=response.choices[0].message.content
    history.append({"role":"assistant","content":reply})

    print(f"\n AI_STUDENT:{reply}\n")