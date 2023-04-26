import requests, re, json, datetime, time
from bs4 import BeautifulSoup
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from .plytv import PlyTv


American = ["football/nfl","basketball","baseball","football","hockey"]
Europe = ["afl","epl","rugby","soccer"]
Fighting = ["boxing","fighting","mma","ufc","wwe"]
Misc = ["golf","tennis","darts","handball","snooker","volleyball"]
Racing = ["cycling","formula-1","motogp","motorsports","nascar","racing"]

class Strikeout(Extractor):
    domains = ["strikeout.ws"]
    name = "StrikeFighting"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        slugs = []
        for sport_page in soup.select("div.col-xxl-2"):
            sport = sport_page.text
            if not sport.lower() in Fighting:
                continue
            
            sport_href = sport_page.select_one("a").get("href")
            if not sport_href.startswith("/"):
                continue
            r_sport = requests.get(f"https://{self.domains[0]}{sport_href}").text
            # r_sport = requests.get(f"https://{self.domains[0]}").text
            soup_sport = BeautifulSoup(r_sport, "html.parser")
            site_config = json.loads(re.findall(r"const siteConfig = (.+?);", r_sport)[0])
            for game in soup_sport.select("a.btn-primary"):
                game_id = game.get("aria-controls")
                game_slug = site_config["slugs"][game_id]
                if game_slug in slugs:
                        continue
                else:
                    slugs.append(game_slug)
                game_title = game.get("title")
                game_links = [Link(address=f"https://{self.domains[0]}/{game_slug}-stream-{i+1}", name=f"{link['player']} - Link {i+1}") for i, link in enumerate(site_config["links"][game_id])]
                game_spans = game.find_all("span")
                if len(game_spans) > 1:
                    game_time = datetime.datetime(*(time.strptime(game_spans[-1].get("content"), "%Y-%m-%dT%H:%M")[:6])) - datetime.timedelta(hours=1)
                else:
                    game_time = None
                games.append(Game(title=game_title, links=game_links, league=sport, starttime=game_time))
        return games
    
    def get_link(self, url):
        r = requests.get(url).text
        zmid = re.findall(r'zmid = "(.+?)"', r)[0]
        return PlyTv().plytv_sdembed(zmid, url)