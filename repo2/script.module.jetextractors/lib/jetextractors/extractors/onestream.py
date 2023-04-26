import requests, re, base64
from ..models.Extractor import Extractor
from ..models.Link import Link
from urllib.parse import urlparse
import random

class Onestream(Extractor):
    def __init__(self) -> None:
        self.domains = ["1stream.eu"]

    def get_link(self, url):
        event_id = urlparse(url).path.split("/")[-1]
        path = event_id + "=" + str(round(random.random() * 64))
        r = requests.get(url).text
        token = re.findall(r'"_token": "(.+?)"', r)[0]
        r = requests.post(f"https://{self.domains[0]}/getspurcename?{path}", data={"eventId": event_id, "_token": token, "sport": "other"}, headers={"Referer": url, "User-Agent": self.user_agent, "X-Requested-With": "XMLHttpRequest"}).json()
        link = base64.b64decode(r["source"]).decode("utf-8")
        return Link(link, headers={"Referer": url})