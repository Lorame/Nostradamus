import os
import requests
from dotenv import load_dotenv
from collections import Counter

# Loading of the API key from .env file
load_dotenv()

api_token = os.getenv("FOOTBALL_API_TOKEN")

# UCL matches endpoint from the 2024-2025 season
endpoint = "https://api.football-data.org/v4/competitions/CL/matches?season=2024"

headers = {"X-Auth-Token" : api_token}

response = requests.get(endpoint,headers=headers)

print("Status code:", response.status_code)

data = response.json()

matches = data["matches"]

stages = [match["stage"] for match in matches]

print(Counter(stages))