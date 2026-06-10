from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client=Groq()

def Generate_quiz(topic,num_questions=5):
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role":"system","content":f"""You are a quiz generator for CS students.
Return ONLY a valid JSON array of {num_questions} questions.
Each question must have exactly these fields:
- question: string
- options: array of exactly 4 strings  
- answer: the correct option string (must match one of options exactly)
- explanation: one sentence why it's correct
No markdown, no extra text, only the JSON array."""
        },{
            "role":"user",
            "content":f"Generate {num_questions} MCQ Questions on:{topic}"

        }]
    )

    raw=response.choices[0].message.content
    clean=raw.replace("```json","").replace("```","").strip()
    return json.loads(clean)

def run_quiz(questions,topic):
    score=0
    print(f"\n Quiz:{topic} | {len(questions)}questions \n")
    print("-"*50)

    for i,q in enumerate(questions,1):
        print(f"\n Q{i}:{q['question']}")
        for j,opt in enumerate(q['options'],1):
            print(f"{j}. {opt}")


        while True:
            ans=input("Your answer (1-4): ").strip()
            if ans in ["1","2","3","4"]:break
            print("Enter 1,2,3 or 4 only")

        chosen = q['options'][int(ans)-1]
        if chosen == q['answer']:
            print("Correct!")
            score+=1
        else:
            print(f"X Wrong. Correct:{q['answer']}")

        print(f"{q['explanation']}")



    print(f"\n{'='*50}")
    print(f"Score:{score}/{len(questions)}")

    if score==len(questions):
        print("PERFECT SCORE!")
    elif score>=len(questions)*0.6:
        print("Good Job! keep revising")
    else:
        print("Need more Practice.Review the Topic") 



#-----Main-----

topic = input("Enter topic for quiz: ")
num = int(input("How many questions? (3-10): "))
questions = Generate_quiz(topic, num)
run_quiz(questions, topic)                          