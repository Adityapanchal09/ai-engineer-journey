import os
import json
import re
from groq import Groq
from models import JobAnalysis
from dotenv import load_dotenv

load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT="""You are an expert Job post analyser.
when given a job description,extract structured information and return only a valid JSON object.
No explanation,No markdowns,No tickbacks-raw JSON only.

The JSON must have these exact keys:
- job_title (string)
- company_name (string or null)
- experience_level (one of: "Intern", "Junior", "Mid", "Senior", "Lead")
- experience_years (string or null, e.g. "2-4 years")
- employment_type (one of: "Full-time", "Part-time", "Contract", "Internship")
- work_mode (one of: "Remote", "On-site", "Hybrid")
- required_skills (list of strings)
- preferred_skills (list of strings)
- salary_range (string or null)
- location (string or null)
- responsibilities (list of strings)
- red_flags (list of strings — things like unpaid trials, unrealistic experience demands, vague compensation, excessive unpaid overtime hints)
- summary (2-3 sentence plain English overview of the role)


if a field's info is not present in the job post,use null for optional fields or empty list [] for list fields"""

def clean_response(text: str) -> str:
    # Remove <think>...</think> block
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Remove markdown backticks
    text = re.sub(r'```json|```', '', text)
    text = text.strip()
    
    # Extract just the JSON object - handles any leftover noise
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        text = text[start:end+1]
    
    return text


def analyze_job_post(job_description:str)->JobAnalysis:
    response=client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        max_tokens=4096,
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":f"Analyse this job post:\n\n{job_description}"}
        ]
    )

    raw = response.choices[0].message.content
    cleaned = clean_response(raw)
    try:
        data = json.loads(cleaned)
        print("JSON parsed OK")
        return JobAnalysis(**data)
    except json.JSONDecodeError as e:
        print(f"JSON ERROR: {e}")
        raise
    except Exception as e:
        print(f"PYDANTIC ERROR: {e}")
        raise