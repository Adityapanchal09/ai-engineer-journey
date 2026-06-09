import requests

response=requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random",
                      params={"language":"en"})

data=response.json()
print(data["text"])