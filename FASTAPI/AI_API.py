from fastapi import FastAPI
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
import json

load_dotenv()
app=FastAPI(title="AI engineer API",version="1.0")
client=Groq()

#--- Request Models (what the API Accepts)---
class ChatRequest(BaseModel):
    message:str
    system_prompt:str="You are a helpful Assistant!"

class QuizRequest(BaseModel):
    topic:str
    num_questions:int=3

class SummarizeRequest(BaseModel):
    text:str


#---helper Function---
def ask_ai(system:str,user:str)->str:
    response=client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {"role":"system","content":system},
            {"role":"user","content":user}
        ]
    )

    return response.choices[0].message.content

#--Endpoints--
@app.get("/")
def home():
    return {"message":"AI API Enginner is running!","version":"1.0"}

@app.post("/chat")
def chat(request:ChatRequest):
    reply=ask_ai(request.system_prompt,request.message)
    return {"reply":reply}

@app.post("/quiz")
def generate_quiz(request:QuizRequest):
    prompt=f"""Return ONLY a valid JSON array of {request.num_questions} MCQ questions on {request.topic}.
    Format strictly like this: [{{"question": "...", "options": ["str", "str", "str", "str"], "answer": "...", "explain": "..."}}]
    Do not output any markdown, conversational text, or introductions."""
    raw=ask_ai(prompt,f"Generate Quiz on {request.topic}")
    # 2. Clean the markdown backticks just in case it ignores the prompt
    clean = raw.replace("```json", "").replace("```", "").strip()
    # 3. Safely attempt to parse the JSON
    try:
        parsed_questions = json.loads(clean)
        return {"topic": request.topic, "questions": parsed_questions}
    except json.JSONDecodeError as e:
        # If the AI fails to return valid JSON, this prevents a 500 error 
        # and returns exactly what the AI outputted so you can debug it.
        return {
            "error": "The AI failed to return valid JSON.",
            "raw_output": raw,
            "exception": str(e)
        }
@app.post("/summarize")
def summarize_text(request:SummarizeRequest):
    summary=ask_ai("Summarize in 3 bullet points.",request.text)
    return {"summary":summary}
