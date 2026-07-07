import os
from fastapi import FastAPI,HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from groq import AsyncGroq
from dotenv import load_dotenv
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

app=FastAPI(title="AI Engineer API - DAY 22",version="0.2.0")
client=AsyncGroq(api_key=os.getenv("GROQ_API_KEY")) #note:AsyncGroq

MODEL="qwen/qwen3.6-27b" 

#in memory conversation history
conversation_history=[]

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
   #append the new user message to user history
    conversation_history.append({
       "role":"user",
       "content":request.message
   })
   
    async def token_generator():
        full_response="" #accumulate the full reply here
        try:
            stream=await client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role":"system","content":request.system_prompt}
                    
                ]+conversation_history, #system prompt + full history
                max_tokens=request.max_tokens,
                reasoning_format="hidden",
                stream=True

            )

            async for chunk in stream:
                token=chunk.choices[0].delta.content
                if token:
                    full_response+=token  #build the full reply
                    yield token
        except Exception as e:
            yield f"\n[ERROR]:{str(e)}"
        finally:
            #step 3 :after streaming done save assistant reply to history
            if full_response:
                conversation_history.append({
                    "role":"assistant",
                    "content":full_response
                })    
    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )                    

#---Utility End Points---
#Mount Static folder
app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")
     

@app.get("/health")
async def health():
    return {"status":"ok","model":MODEL}

@app.post("/reset")
async def reset_chat():
    conversation_history.clear()
    return {"status":"ok","message":"conversation history cleared"}


@app.get("/history")
async def get_history():
    return {"history":conversation_history,"turns":len(conversation_history)}


