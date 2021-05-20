import requests
import json

url = "https://v3.football.api-sports.io/leagues/seasons"

payload = {}
headers = {
    'x-rapidapi-key': '661edf37c32bb2a7fe982cfcce78ee6c',
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

leagues_ids_dictionary = {}


def get_all_countries():
    url = "https://v3.football.api-sports.io/countries"
    countries_names = []

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)['response']

    for elem in data:
        countries_names.append(elem['name'])

    return countries_names
    # list = ["BUTTON"+str(i) for i in range(100)]
    # return list


def get_leagues_for_country(country_name):
    url = "https://v3.football.api-sports.io/leagues?country=" + country_name
    league_names = []

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)['response']
    for league in data:
        if league['league']['type'] == 'League':
            league_names.append(league['league']['name'])
            leagues_ids_dictionary[league['league']['name']] = league['league']['id']
    return league_names
    # return []


def get_league_id(league_name):
    return leagues_ids_dictionary[league_name]


def get_seasons():
    url = "https://v3.football.api-sports.io/leagues/seasons"
    seasons = []

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)['response']
    for season in data:
        seasons.append(season)

    return seasons
    # return [2020, 2019, 2018, 2017]


def get_standings_for_league_and_season(league, season):
    if league == "" or season == "":
        return []

    url = "https://v3.football.api-sports.io/standings?league=" + str(league) + "&season=" + str(season)
    standings_list = []

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)['response']

    if data != []:
        standings = data[0]["league"]["standings"]
    else:
        return data

    for standing in standings[0]:
        standings_list.append(
            (standing["rank"], standing["team"]["name"], standing["points"], standing["all"]["played"],
             standing["all"]["win"], standing["all"]["draw"], standing["all"]["lose"],
             standing["all"]["goals"]["for"], standing["all"]["goals"]["against"], standing["goalsDiff"]))

    return standings_list
    # list = [("1", "Real Madrid", "30", "40", "10", "20", "30", "100", "50", "50") for i in range(20)]
    # return list


def get_scorers_for_league_and_season(league, season):
    if league == "" or season == "":
        return []

    url = "https://v3.football.api-sports.io//players/topscorers?season=" + str(season) + "&" + "league=" + str(league)
    scorers_list = []

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)["response"]

    for elem in data:
        scorers_list.append(
            (elem["player"]["name"], elem["statistics"][0]["team"]["name"], elem["statistics"][0]["goals"]["total"]))

    return scorers_list
    # return []
