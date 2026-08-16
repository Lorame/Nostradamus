import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Let's create the function responsible for collecting the data for a given edition of the UEFA Champions League:
 
def collect_ucl_matches(season):
    
    #your api token
    api_token = os.getenv("FOOTBALL_API_TOKEN")
    
    if not api_token:
        raise ValueError("FOOTBALL_API_TOKEN is missing.")
    
    endpoint = (
        f"https://api.football-data.org/v4/competitions/CL/matches"
        f"?season={season}"
    )
    
    headers = {
        "X-Auth-Token": api_token
    }
    
    response = requests.get(endpoint,headers=headers)
    
    response.raise_for_status()
    
    matches = response.json()["matches"]
    
    #Create folder if needed
    os.makedirs("data/raw",exist_ok=True)
    
    filename = f"data/raw/champions_league_{season}_{season+1}.json"
    
    with open(filename,"w",encoding="utf-8") as file:
        json.dump(matches,file,indent=4,ensure_ascii=False)
    
    print(
        f"Champions League {season}/{season+1}: collected ✅!\n"
        f"{len(matches)} matches saved in {filename}"
    )
    return matches

if __name__ == "__main__":

    seasons = [2024, 2025]

    for season in seasons:
        collect_ucl_matches(season)