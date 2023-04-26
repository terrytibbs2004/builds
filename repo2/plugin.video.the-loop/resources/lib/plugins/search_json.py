from ..util.dialogs import link_dialog
from ..plugin import Plugin
from ..DI import DI
import requests, xbmcgui, json, xbmc
from bs4 import BeautifulSoup
from resources.lib.plugin import run_hook
import urllib

class SearchJSON(Plugin):
    name = "search_json"
    priority = 100
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

    def process_item(self, item):
        if self.name in item:
            query = item.get(self.name, "*")
            thumbnail = item.get("thumbnail", "")
            fanart = item.get("fanart", "")
            dialog = query.startswith("dialog:")
            if dialog:
                query = query.replace("dialog:", "")
            item["link"] = f"{self.name}/{item.get('link')}?query={query}&dialog={str(dialog).lower()}"
            item["is_dir"] = not dialog
            item["list_item"] = xbmcgui.ListItem(item.get("title", item.get("name", "")))
            item["list_item"].setArt({"thumb": thumbnail, "fanart": fanart})
            return item

    def routes(self, plugin):
        @plugin.route(f"/{self.name}/<path:dir>")
        def directory(dir):
            jen_list = []
            dir = urllib.parse.unquote_plus(dir)
            query = plugin.args["query"][0] if "query" in plugin.args else None
            if query == None or query == "*":
                query = xbmcgui.Dialog().input("Search").lower()
                if query == "": return
            dialog = plugin.args["dialog"][0] == "true" if "dialog" in plugin.args else False
            jen_list = list(filter(lambda x: query in x.get("title", x.get("name", "")).lower(), requests.get(dir).json()["items"]))
            if dialog:
                idx = link_dialog([res["title"] for res in jen_list], return_idx=True, hide_links=False)
                if idx == None:
                    return True
                run_hook("play_video", json.dumps(jen_list[idx]))
            else:
                jen_list = [run_hook("process_item", item) for item in jen_list]
                jen_list = [run_hook("get_metadata", item, return_item_on_failure=True) for item in jen_list]
                run_hook("display_list", jen_list)
            