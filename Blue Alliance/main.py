import utils
import csv

""" 
- climb location
- offense or defense
"""

URL = "https://www.thebluealliance.com/api/v3"
HEADERS = {
    "X-TBA-Auth-Key":"KXIpEFGUnYK944gocTxjUqF8RI33QSHeXyb1ymG6vq1qx5vkTVjSyF7EWNE41yHh",
    "User-Agent":"Optix Agent"
}

matchAPI = utils.MatchAPI(URL, HEADERS)
print("Init")
print(matchAPI.update())


teams: list[int] = [4]
for teamNum in teams:
    team = matchAPI.get_team(teamNum)
    events = matchAPI.get_events_by_team(team)
    for event in events:
        matches = matchAPI.get_matches_by_team(team,event)
        for match in matches:
            print(match)
            blueScore = int(match["score_breakdown"]["blue"]["totalPoints"]) - int(match["score_breakdown"]["blue"]["foulPoints"])  
            print("Blue Score: " + str(blueScore))
            redScore = int(match["score_breakdown"]["red"]["totalPoints"]) - int(match["score_breakdown"]["red"]["foulPoints"])  
            print("Red Score: " + str(redScore))