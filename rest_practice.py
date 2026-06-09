import requests

response=requests.get("https://official-joke-api.appspot.com/random_joke")

print("status:",response.status_code)
data=response.json()

print("Setup:",data["setup"])
print("Punchline:",data["punchline"])
