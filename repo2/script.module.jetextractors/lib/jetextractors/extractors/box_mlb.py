import requests, re, json, datetime, time
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

from .plytv import PlyTv

class SportsBox(Extractor):
    def __init__(self) -> None:
        self.domains = ["mlbstreams.me"]
        self.name = "BoxMLB"
        self.short_name = "MLBB"

    def get_games(self):
        games = []
        for domain in self.domains:
            slugs = []
            r = requests.get(f"https://{domain}").text
            soup = BeautifulSoup(r, "html.parser")
            categories = soup.select("a.btn-lg")
            for cat in categories:
                cat_name = cat.text.split(" - ")[0].strip()
                cat_href = "https://" + domain + cat.get("href")
                r_cat = requests.get(cat_href, headers={"Referer": f"https://{domain}"}).text
                soup_cat = BeautifulSoup(r_cat, "html.parser")
                site_config = json.loads(re.findall(r"const siteConfig = (.+?);", r_cat)[0])
                for game in soup_cat.select("a.btn-secondary"):
                    game_id = game.get("aria-controls")
                    game_slug = site_config["slugs"][game_id]
                    if game_slug in slugs:
                        continue
                    else:
                        slugs.append(game_slug)
                    game_title = game.get("title")
                    game_links = [Link(address=f"https://{domain}/{game_slug}-live/stream-{i+1}", name=f"{link['player'][1:]} - Link {i+1}") for i, link in enumerate(site_config["links"][game_id])]
                    game_spans = game.find_all("span")
                    if len(game_spans) > 1:
                        game_time = datetime.datetime(*(time.strptime(game_spans[-1].get("content"), "%Y-%m-%dT%H:%M")[:6])) - datetime.timedelta(hours=1)
                    else:
                        game_time = None
                    games.append(Game(title=game_title, links=game_links, league=cat_name, starttime=game_time))
        return games

    def get_link(self, url):
        r = requests.get(url).text
        zmid = re.findall(r'zmid = "(.+?)"', r)[0]
        return PlyTv().plytv_sdembed(zmid, url)