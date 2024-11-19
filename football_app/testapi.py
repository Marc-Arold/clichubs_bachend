import requests

url = "https://api-football-v1.p.rapidapi.com/v3/countries"

headers = {
	"X-RapidAPI-Key": "0bcf277bd9mshc90df54cc24dc46p1a1e41jsnf71bfbc56d39",
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())