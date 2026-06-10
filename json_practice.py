from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": """You are a data extractor.
Always respond with ONLY valid JSON. No explanation, no markdown, no extra text.
Return exactly this structure:
{
  "topic": "string",
  "summary": "string",
  "key_points": ["point1", "point2", "point3"]
}"""
 },
        {
            "role": "user",
            "content": "Summarize: Operating System Process Scheduling"
        }
    ]
)
raw = response.choices[0].message.content
data = json.loads(raw)  # convert JSON string → Python dict

print("Topic:", data["topic"])
print("Summary:", data["summary"])
print("Key points:")
for point in data["key_points"]:
    print(f"  - {point}")

raw = response.choices[0].message.content

# Sometimes AI adds ```json ... ``` around it — strip it
clean = raw.replace("```json", "").replace("```", "").strip()

try:
    data = json.loads(clean)
    print(data)
except json.JSONDecodeError:
    print("AI didn't return valid JSON. Raw output:", raw)    