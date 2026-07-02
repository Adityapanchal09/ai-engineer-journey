from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq()

def ask(system,user_msg):
    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg}
        ]
    )

    return response.choices[0].message.content

def clean_notes(raw_text):
    return ask("You are an editor .fix grammer ,punctuation,clarity of these notes.return only the corrected text ,no commentary ",raw_text)

def summarized(cleaned_text):
    return ask("Summarize this in 5 Sentences",cleaned_text)

def extract_key_points(cleaned_text):
    raw=ask( """Extract the 5 most important points.
Return ONLY a JSON array of strings, no markdown, no extra text.""",
        cleaned_text)

    clean=raw.replace("```json","").replace("```","").strip()

    print("DEBUG - raw AI output:")
    print(clean)
    print("---END DEBUG---")
    
    return json.loads(clean)


def generate_questions(summary_text):
    raw = ask(
        """Generate 3 short answer exam questions based on this summary.
Return ONLY a JSON array of strings, no markdown.""",
        summary_text
    )
    clean = raw.replace("```json","").replace("```","").strip()
    return json.loads(clean)

def run_pipeline(raw_text):
    print("⏳ Step 1/4: Cleaning notes...")
    cleaned=clean_notes(raw_text)

    print("⏳ Step 2/4: Summarizing text...")
    summary=summarized(cleaned)

    print("⏳ Step 3/4: extracting key points...")
    key_points=extract_key_points(cleaned)

    print("⏳ Step 4/4: Generating Questions...")
    questions=generate_questions(summary)

    return{
        "cleaned":cleaned,
        "summary":summary,
        "key_points":key_points,
        "questions":questions
    }


#---Main----
raw_notes=input("Enter Your messy Notes: ")
result=run_pipeline(raw_notes)

print("\n"+"="*50)
print("📝 SUMMARY:", result["summary"])
print("\n🔑 KEY POINTS:")
for p in result["key_points"]:
    print(f" - {p}")
print("\n❓ EXAM QUESTIONS:")
for q in result["questions"]:
    print(f"- {q}")


#Save full result to file
with open("pipeline_output.json","w") as f:
    json.dump(result,f,indent=3)        