from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import feedparser

BASE_URL = "https://statsapi.mlb.com"

# Create your views here.
def standings(request):

    response = requests.get(BASE_URL + "/api/v1/standings?leagueId=103,104")

    teamRecords = response.json()

    order = [201, 204, 202, 205, 200, 203]
    divisons_ordered = []

    for id in order:
        for div in teamRecords['records']:
            if id == div['division']['id']:
                divisons_ordered.append(div)

    feed = feedparser.parse("https://www.mlb.com/feeds/news/rss.xml")

    return render(request, "home.html", {'teamRecords':divisons_ordered, 'feed':feed['entries']})
    pass

def roster(request, id):
    
    response = requests.get(BASE_URL + "/api/v1/teams/" + id + "/roster/Active?hydrate=person(stats(type=season))")
    roster = response.json()

    team_response = requests.get(BASE_URL + "/api/v1/standings?leagueId=103,104")
    team = team_response.json()
    team_info = ""

    for i in team["records"]:
        for p in i["teamRecords"]:
            if p["team"]["id"] == int(id):
                team_info = p
                break

    return render(request, "roster.html", {'roster':roster["roster"], 'team':team_info})
    pass

def player(request, id):

    response = requests.get(BASE_URL + "/api/v1/people/" + id + "?hydrate=stats(group=[hitting,pitching],type=[yearByYear])")
    player = response.json()

    pitching_stats = ""
    hitting_stats = ""

    if "stats" in player["people"][0]:
        for i in player["people"][0]["stats"]:
            if i["group"]["displayName"] == "pitching":
                pitching_stats = i["splits"]
            elif i["group"]["displayName"] == "hitting":
                hitting_stats = i["splits"]
    else:
        pitching_stats = ""
        hitting_stats = ""

    return render(request, "player.html", {'player':player, 'pitching_stats':pitching_stats, 'hitting_stats':hitting_stats})
    pass

def leaders(request):

    hitting_response = requests.get(BASE_URL + "/api/v1/stats/leaders?leaderCategories=homeRuns,runsBattedIn")
    hitting_leaders = hitting_response.json()

    #rbi_reponse = requests.get(BASE_URL + "/api/v1/stats/leaders?leaderCategories=runsBattedIn")
    #rbi_leaders = rbi_reponse.json()

    pitching_reponse = requests.get(BASE_URL + "/api/v1/stats/leaders?leaderCategories=earnedRunAverage,strikeouts")
    pitching_leaders = pitching_reponse.json()

    return render(request, "leaders.html", {'pitching_leaders':pitching_leaders, 'hitting_leaders': hitting_leaders})

