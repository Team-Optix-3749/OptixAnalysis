import requests
import json

def jprint(obj:dict):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

class APIMain:
    def __init__(self, url:str, headers:dict):
        self.URL = url
        self.HEADERS = headers
        self.USER_DATA = {}
    def add_header(self,headers:dict):
        for k in headers.keys():
            if k in self.HEADERS:
                print("{} header already exists. Overwriting".format(k))

            self.HEADERS[k] = headers[k]
    def remove_header(self,headers:list):
        for header in headers:
            if header not in self.HEADERS:
                raise Warning("{} header does not exist.".format(header))
            else:
                self.HEADERS.pop(header)
    def remove_header(self,header:str):
        if header not in self.HEADERS:
            raise Warning("{} header does not exist.".format(header))
        else:
            self.HEADERS.pop(header)
    def api_pull(self, subdirectory:str) -> requests.Response:

        r = requests.get(self.URL+"/"+subdirectory, headers=self.HEADERS)
        return r

    def update(self):
        return 0

class MatchAPI(APIMain):
    def __init__(self, url:str, headers:dict):
        self.teamHeaders = {"If-Modified-Since":"Thu, 01 Jan 1970 00:00:00 GMT"
        }
        self.teamReturnHeaders = {}
        self.teams = []
        self.teamByNum = {}
        self.teamByNick = {}
        self.teamByName = {}
        super().__init__(url, headers)
    def update(self):
        self.add_header(self.teamHeaders)
        page = 0
        r = self.api_pull("teams/{}".format(page))
        for k in r.headers.keys():
            if k in self.teamReturnHeaders:
                raise Warning("{} header already exists. Overwriting".format(k))

            self.teamReturnHeaders[k] = r.headers[k]
        while len(r.json())>0:
            page+=1
            print(page)

            self.teams+=(r.json())
            for team in r.json():
                self.teamByNum[team["team_number"]] = team
                self.teamByName[team["name"]] = team
                self.teamByNick[team["nickname"]] = team
                
            try:
                r = self.api_pull("teams/{}".format(page))
            except:
                print("Something went wrong")
        #self.teamHeaders["If-Modified-Since"] = self.teamReturnHeaders["Last-Modified"]

    def get_team(self, teamNumber=0,nickname="",name="")->dict:
        if teamNumber!=0:
            return self.teamByNum[teamNumber]
        if nickname!="":
            return self.teamByNick[nickname]
        if name!="":
            return self.teamByName[name]
        raise Warning("Nothing passed. Returning")
    def get_events_by_team(self, team: dict)->list[str]:
        self.add_header(self.teamHeaders)
        events = self.api_pull("team/{}/events/2022".format(str(team["key"])))
        return events.json()
    def get_event_by_key(self, key: dict)->list[str]:
        self.add_header(self.teamHeaders)
        events = self.api_pull("team/{}/events/2022".format(str(key["key"])))
        return events.json()
    def get_matches_by_team(self, team: dict, event: dict)->list[dict]:
        self.add_header(self.teamHeaders)
        matches = self.api_pull("team/{}/event/{}/matches".format(str(team["key"]), str(event["key"])))
        return matches.json()
    def get_match_keys(self, year: int)->list[int]:
        self.add_header(self.teamHeaders)
        matchKeys = self.api_pull("team/{}/keys".format(year))
        return matchKeys.json()
