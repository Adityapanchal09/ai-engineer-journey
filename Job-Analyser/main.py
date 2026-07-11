from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from analyzer import analyze_job_post
import re

app=FastAPI(title="Job Post Analyzer")

#serve static files from /static folder
app.mount("/static",StaticFiles(directory="static"),name="static")

class JobRequest(BaseModel):
    job_description:str

@app.post("/analyze",response_model=dict)
async def analyze(request:JobRequest):
    if not request.job_description.strip():
        raise HTTPException(status_code=400,detail="Job description cannot be empty")
    try:
        result=analyze_job_post(request.job_description)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Analysis failed:{str(e)}")


@app.get("/")
async def root():
    return FileResponse("static/index.html")        
