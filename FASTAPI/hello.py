from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"message":"API is running!"}

@app.get("/hello/{name}")
def greet(name: str):
    return {"greeting":f"Hello {name}"}