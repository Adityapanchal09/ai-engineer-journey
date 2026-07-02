from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
client=Groq()

def load_document(filepath):
    if not os.path.exists(filepath):
        print(f"File not found:{filepath}")
        return None
    with open(filepath,"r",encoding="utf-8") as f:
        return f.read()
    

def ask_ai(document,instruction):

    response=client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[{
            "role":"system","content":f"You are a study Assistant,work with this document only:{document}\n\n"

        },
        {
            "role":"user","content":instruction
        }

        ]
    )

    return response.choices[0].message.content


def chat_with_doc(document):
    history=[]
    SYSTEM=f"You are a study Assistant,Answer feom this document only:\n\n{document}"
    print("\nChat Mode-- Ask Anything About your document.Type 'back' to return")
    while True:
        q=input("You: ")
        if q.lower()=="back":break
        history.append({"role":"user","content":q})
        response=client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            messages=[{"role":"system","content":SYSTEM}]+history
        )

        reply=response.choices[0].message.content
        history.append({"role":"assistant","content":reply})

        print(f"\n AI:{reply}\n")



#----MAIN----
filepath=input("Enter Document Path to your .txt file: ")
document=load_document(filepath)
if not document: exit() 

print(f"\n Loaded:{len(document.split())} words\n")

while True:
    print("\n What do you wnat to do?")
    print("1.Summarize Document")
    print("2.Extract Key Points")
    print("3.Generate Key Points from document")
    print("4.Chat with Document")
    print("5.Exit")

    choice=input("\nEnter choice from (1-5): ")

    if choice=="1":
        print("\n",ask_ai(document,"Give a clear concise summary of this document"))
    elif choice=="2":
        print("\n",ask_ai(document,"Extract the 5 most Key points as numbered list"))
    elif choice=="3":
        print("\n",ask_ai(document,"Generate 3 MCQ based questions from the document,include answers"))
    elif choice=="4":
        chat_with_doc(document)
    elif choice=="5":
        print("GoodBye")
        break
    else:
        print("Invalid Choice,Enter from 1-5")                