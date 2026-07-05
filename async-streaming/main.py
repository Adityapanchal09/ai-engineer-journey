import os
from fastapi import FastAPI,HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from groq import AsyncGroq
from dotenv import load_dotenv
import asyncio

load_dotenv()

app=FastAPI(title="AI Engineer API - DAY 22",version="0.2.0")
client=AsyncGroq(api_key=os.getenv("GROQ_API_KEY")) #note:AsyncGroq

MODEL="qwen/qwen3.6-27b" 

#---Pydantic Models---
class ChatRequest(BaseModel):
    message:str
    system_prompt:str="You are a helpful AI Assistant"
    max_tokens:int=1024


#---regular async endpoint(no streaming)--- use this when creating an internal data pipeline,groq will give you completely generated answer at once,
                                        #answer will return to client as complete json response generated
@app.post("/chat")                   
async def chat(request: ChatRequest):
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.message}
            ],
            max_tokens=request.max_tokens,
            reasoning_format="hidden" #hides <think> blocks
        )
        return {
            "response": response.choices[0].message.content,
            "model": MODEL,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#---Streaming Endpoint---
"""This is the most important part. Breaking it down:
token_generator() — inner async function

It's a generator — instead of returning all at once, it yields one token at a time
stream=True tells Groq to send tokens as they're generated, not wait for full response
async for chunk in stream — loops through each chunk Groq sends
chunk.choices[0].delta.content — each chunk has a small piece of text (delta means "change/addition")
if token: — sometimes chunks are empty, we skip those
yield token — sends that token immediately to the client

StreamingResponse

Takes the generator and streams its output to the client in real-time
media_type="text/plain" — tells client to expect plain text, not JSON"""
@app.post("/chat/stream")
async def chat_stream(request:ChatRequest):   
    async def token_generator():
        try:
            stream=await client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role":"system","content":request.system_prompt},
                    {"role":"user","content":request.message}
                ],
                max_tokens=request.max_tokens,
                reasoning_format="hidden",
                stream=True

            )

            async for chunk in stream:
                token=chunk.choices[0].delta.content
                if token:
                    yield token
        except Exception as e:
            yield f"\n[ERROR]:{str(e)}"
    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )                    

#---Utility End Points---
@app.get("/")
async def root():
    return {"message":"AI Engineer API v0.2-Async +Streaming"}

@app.get("/health")
async def health():
    return {"status":"ok","model":MODEL}

