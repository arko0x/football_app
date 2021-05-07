import requests
import json

url = "https://v3.football.api-sports.io/leagues/seasons"

payload = {}
headers = {
    'x-rapidapi-key': '661edf37c32bb2a7fe982cfcce78ee6c',
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

def get_leagues_for_country(country_name):
    url = "https://v3.football.api-sports.io/leagues?country=" + country_name
    league_names = []

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)['response']
    for league in data:
        if league['league']['type'] == 'League':
            league_names.append(league['league']['name'])
    return league_names

print(get_leagues_for_country("england"))
