import requests, re, datetime
from dateutil import parser
from ..util.m3u8_src import scan_page

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Rainostreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["rainostreams.com", "bdnewszh.com"]
        self.name = "Rainostreams"
        self.short_name = "RS"

    def get_link(self, url):
        if "rainostreams" in url:
            if "?sport" in url:
                url = url.split("?sport")[0]
            url = url.replace("https", "http").replace(self.domains[0], f"{self.domains[1]}/embed") + ".php"
        m3u8 = scan_page(url, headers={"User-Agent": self.user_agent, "Referer": f"http://{self.domains[0]}/"})
        if m3u8 != None:
            headers = {
                "Origin": f"http://{self.domains[1]}",
                "Referer": f"http://{self.domains[1]}/",
                "User-Agent": self.user_agent
            }
            if requests.head(m3u8.address, headers=headers).status_code == 401:
                headers = {
                    "Origin": f"https://{self.domains[1]}",
                    "Referer": f"https://{self.domains[1]}/",
                    "User-Agent": self.user_agent
                }
            m3u8.is_hls = True
            m3u8.headers = headers
        return m3u8

    def get_games(self):
        games = []
        leagues = ["nfl", "mlb", "nba"]
        for league in leagues:
            r = requests.get(f"http://streamsapi.xyz/api/{league}").json()
            for event in r["events"]:
                game_title = event["title"]
                game_time = event["kickOff"]
                utc_time = datetime.datetime.strptime(game_time, "%Y-%m-%dT%H:%M:%S.000Z")
                link = Link(f"http://{self.domains[1]}/embed/{league}/{game_title.split()[-1].lower()}.php")
                games.append(Game(
                    title=game_title,
                    links=[link],
                    starttime=utc_time,
                    league=league.upper()
                ))

        leagues = ["soccer", "ncaaf", "nba", "nhl", "rugby", "race", "cricket", "mma"]
        for league in leagues:
            try:
                r = requests.get(f"http://api.{self.domains[1]}/{league}.json", headers={"Referer": f"http://{self.domains[0]}/", "User-Agent": self.user_agent}).json()
                games_arr = r["games"] if "games" in r else r["game"]
                for game in games_arr:
                    if "h2h" in game:
                        title = game["h2h"]
                    elif "name" in game:
                        title = game["name"]
                    elif "title" in game:
                        title = game["title"]
                    elif "home_team_name" in game:
                        title = f"{game['home_team_name']} vs {game['away_team_name']}"
                    else:
                        title = f"{game['home']['name']} vs {game['away']['name']}"
                    
                    if "league" in game:
                        game_league = game["league"]
                    elif "raceType" in game:
                        game_league = game["raceType"]
                    elif "turnament" in game:
                        game_league = game["turnament"].capitalize()
                    elif "tournaments" in game:
                        game_league = game["tournaments"]
                    else:
                        game_league = league.upper()

                    if "stream" in game:
                        link = Link(f"http://{self.domains[1]}/embed/{league if 'raceType' not in game else game['raceType'].lower()}/{game['stream']}.php")
                    else:
                        link = Link(f"http://{self.domains[1]}/embed/{league}/{game['home_team_name'].split()[-1].lower()}.php")
                    
                    games.append(Game(
                        title=title,
                        league=game_league,
                        links=[link]
                    ))
            except:
                continue
        
        return games