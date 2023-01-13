###########################################
#     GIVE CREDIT WHERE CREDIT IS DUE     #
#                                         #
#          T4ILS AND JETJET               #
###########################################




import json, sys, time, operator, os,base64
from ..util.dialogs import link_dialog, remove_name
from xbmcvfs import translatePath
from concurrent.futures import ThreadPoolExecutor
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
from resources.lib.plugin import Plugin
from datetime import datetime, timedelta
import calendar, inputstreamhelper
from jetextractors import extractor
from jetextractors.models.Link import Link
from resources.lib.plugin import run_hook
import urllib.parse
from ..util.common import xbmc_curl_encode

import operator, traceback

CACHE_TIME = 0  # change to wanted cache time in seconds
DEFAULT_DISABLED = ["Full Match TV",  "Topstreams", "Buffstreams","Sling", "USTVGO", "Yahoo Sports","Yahoo Sports - MLB Highlights","Yahoo Sports - NBA Highlights","Yahoo Sports - NCAAB Highlights","Yahoo Sports - NHL Highlights","Freefeds","Direct_CH"]

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class jetextractors(Plugin):
    name = "sportjetextractors"
    priority = 100

    def process_item(self, item):
        if "sportjetextractors" in item:
            link = item.get("sportjetextractors", "")
            thumbnail = item.get("thumbnail", "")
            fanart = item.get("fanart", "")
            icon = item.get("icon", "")
            if not isinstance(link, list):
                if link.startswith("http"):
                    item["is_dir"] = False
                    item["link"] = "/play_video/" + urllib.parse.quote_plus(json.dumps(item))
                elif link == "extractor_settings":
                    item["is_dir"] = False
                    item["link"] = "sportjetextractors/extractor_settings"
                elif link == "iptv_setup":
                    item["is_dir"] = False
                    item["link"] = "sportjetextractors/iptv_setup"
                elif link == "sites":
                    item["is_dir"] = True
                    item["link"] = "sportjetextractors/sites"
                elif link == "dialog":
                    item["is_dir"] = False
                    item["link"] = "sportjetextractors/dialog"
                else:
                    item["link"] = "sportjetextractors/games/" + link if "search" not in link else "sportjetextractors/" + link
                    item["is_dir"] = True
                
                list_item = xbmcgui.ListItem(item.get("title", item.get("name", "")), offscreen=True)
                list_item.setArt({"thumb": thumbnail, "fanart": fanart})
                item["list_item"] = list_item
                return item
        
    def play_video(self, video: str):
        item = json.loads(video)
        link = item.get("sportjetextractors")
        title = item.get("title")
        thumbnail = item.get("thumbnail", "")
        if link:
            if isinstance(link, list):   
                if len(link) == 0:
                    xbmcgui.Dialog().notification("Jetextractors error", "No links specified", icon=xbmcgui.NOTIFICATION_WARNING, time=3000)
                    return True
                if type(link[0]) == str:
                    links = []
                    for l in link:
                        li = Link(l)
                        if "(" in l and l.endswith(")"):
                            split = l.split('(')
                            li.address = split[0]
                            li.name = split[1]
                        links.append(li)
                    link = links
                else:
                    link = [Link.from_dict(l) for l in link]
                    for l in link:
                        if "(" in l.address and l.address.endswith(")"):
                            split = l.address.split('(')
                            l.address = split[0]
                            l.name = split[1]
                link_idx = link_dialog([l.address + (f"({l.name})" if l.name is not None else "") for l in link], return_idx=True)  
                if link_idx == None: return True
                link = link[link_idx]
            else:
                link = Link(link)
            if link.address.startswith("{"):
                link = json.loads(link.address)
            if type(link) == dict:
                link = Link.from_dict(link)
            if link.address.startswith("links://"):
                link.is_links = True
                link.address = link.address.replace("links://", "")
            if link.is_links:
                while link.is_links:
                    e = extractor.find_extractor(link.address)
                    links = e.get_links(link.address)
                    link_idx = link_dialog([l.address + (f"({l.name})" if l.name is not None else "") for l in links], return_idx=True)
                    if link_idx == None: return True
                    link = links[link_idx]
            link.address = urllib.parse.unquote(link.address)
            if link.address.startswith("plugin://"):
                xbmc.executebuiltin(f"RunPlugin({link.address})")
                return True
            if link.address.startswith("direct://"):
                link.address = link.address.replace("direct://", "")
                link.is_direct = True
            if link.address.startswith("ffmpegdirect://"):
                link.address = link.address.replace("ffmpegdirect://", "")
                link.is_ffmpegdirect = True
            if link.address.startswith("jetproxy://"):
                link.address = link.address.replace("jetproxy://", "")
                link.jetproxy = True
                link.is_direct = True
            e = extractor.find_extractor(link.address)
            if e is not None and e.shortener:
                link = e.get_link(link.address)
                e = extractor.find_extractor(link.address)
            if e == None:
                if ".m3u8" not in link.address and not link.is_direct:
                    use_iframe = xbmcgui.Dialog().yesno("No extractor", f"Jetextractors does not have an extractor for this site ({link.address}). Would you like to attempt to search the page for a link?")
                    if not use_iframe: return True
                    iframes = extractor.iframe_extractor(link.address)
                    if len(iframes) > 0:
                        if len(iframes) > 1:
                            link_idx = link_dialog([l.address + (f"({l.name})" if l.name is not None else "") for l in link], return_idx=True)
                            if link_idx == None: return True
                            link = iframes[link_idx]
                        else: link = iframes[0]
                        ext = extractor.find_extractor(link.address)
                        if ext != None:
                            link = ext.get_link(link.address)
                    else:
                        xbmcgui.Dialog().ok("Error", "Jetextractors could not find a playable link for this URL.")
                        return True
            else:
                link.address = remove_name(link.address)
                link = e.get_link(link.address)
            extractor.add_key(link)
            if link.headers != {}:
                link.address = xbmc_curl_encode(link.address, link.headers)
            if link.is_widevine:
                is_helper = inputstreamhelper.Helper('mpd', drm='widevine')
                if not is_helper.check_inputstream():
                    sys.exit()
                liz = xbmcgui.ListItem(item.get("title", link.address), path=link.address)
                if int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0]) >= 19: liz.setProperty('inputstream', 'inputstream.adaptive')
                else: liz.setProperty('inputstreamaddon', 'inputstream.adaptive')
                liz.setProperty('inputstream.adaptive.manifest_type', 'mpd')

                if link.license_url != None:
                    liz.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
                    liz.setProperty('inputstream.adaptive.license_key', link.license_url)
                liz.setMimeType('application/dash+xml')
                liz.setContentLookup(False)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                xbmc.Player().play(link.address, listitem=liz)
            elif link.is_ffmpegdirect:
                liz = xbmcgui.ListItem(item.get("title", link.address), path=link.address)
                
                liz.setInfo('video', {'Title': title})
                liz.setArt({'thumb': thumbnail, 'icon': thumbnail})
                
                if int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0]) >= 19: liz.setProperty('inputstream', 'inputstream.ffmpegdirect')
                else: liz.setProperty('inputstreamaddon', 'inputstream.ffmpegdirect')
                liz.setProperty('inputstream.ffmpegdirect.is_realtime_stream', 'true')
                liz.setProperty('inputstream.ffmpegdirect.stream_mode', 'timeshift')
                liz.setProperty('inputstream.ffmpegdirect.manifest_type', 'hls')
                liz.setMimeType('application/x-mpegURL')
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                xbmc.Player().play(link.address, listitem=liz)
            elif link.jetproxy:
                xbmc.executebuiltin(f"RunPlugin(plugin://plugin.video.jetproxy/play/{link.address})")
            else:
                link.address = link.address.strip()
                liz = xbmcgui.ListItem(title)               
                liz.setInfo('video', {'Title': title})
                liz.setArt({'thumb': thumbnail, 'icon': thumbnail})
                xbmc.Player().play(link.address, liz)
            return True
        
            
    def routes(self, plugin):
        @plugin.route("/sportjetextractors/sites")
        def sites():
            jen_list = []
            extractors = sorted(extractor.get_extractors(), key=lambda x: type(x).__name__)
            for e in extractors:
                if e.name == None:
                    continue
                jen_data = {
                    "title": e.name,
                    "sportjetextractors": e.name,
                    "type": "item"
                }
                jen_list.append(jen_data)
            jen_list = [run_hook("process_item", item) for item in jen_list]
            jen_list = [run_hook("get_metadata", item, return_item_on_failure=True) for item in jen_list]
            run_hook("display_list", jen_list)

        @plugin.route("/sportjetextractors/games/<path:site>")
        def get_games(site):
            for e in extractor.get_extractors():
                if site == e.name:
                    games = e.get_games()
                    jen_list = []
                    for game in games:
                        jen_data = {
                            "title": "[COLORdodgerblue]%s[COLORwhite] |[B][I] %s[/B][/I]\n  [COLORred]%s[/COLOR]" % (game.league.replace("'", "") if game.league is not None else "", game.title, format_time(game.starttime)),
                            "thumbnail": game.icon,
                            "fanart": game.icon,
                            "summary": game.title,
                            "sportjetextractors": [link.to_dict() for link in game.links],
                            "type": "item"
                        }
                        jen_list.append(jen_data)
                    jen_list = [run_hook("process_item", item) for item in jen_list]
                    jen_list = [run_hook("get_metadata", item, return_item_on_failure=True) for item in jen_list]
                    run_hook("display_list", jen_list)
        
        @plugin.route("/sportjetextractors/search/<path:query>")
        def search_games(query):
            if query == "*":
                query = xbmcgui.Dialog().input("Search game")
                if query == "": return
            addon = xbmcaddon.Addon()
            USER_DATA_DIR = translatePath(addon.getAddonInfo("profile"))
            if not os.path.exists(os.path.join(USER_DATA_DIR, f"{self.name}_disabled.json")):
                disabled = DEFAULT_DISABLED
            else:
                f = open(os.path.join(USER_DATA_DIR, f"{self.name}_disabled.json"), "r")
                disabled = json.load(f)
                f.close()
            games = extractor.search_extractors(query, disabled)
            empty_date = datetime(year=2030, month=12, day=31)
            jen_list = []
            for game in games:
                jen_data = {
                    "title": "[COLORdodgerblue]%s[COLORwhite] |[B][I] %s[/B][/I]\n  [COLORred]%s | %s[/COLOR]" % (game.league.replace("'", "") if game.league is not None else "", game.title, game.extractor, format_time(game.starttime)),
                    "thumbnail": game.icon,
                    "fanart": game.icon,
                    "summary": game.title,
                    "sportjetextractors": [link.to_dict() for link in game.links],
                    "time": game.starttime.timestamp() if game.starttime != None else empty_date.timestamp(),
                    "type": "item"
                }
                jen_list.append(jen_data)
            
            jen_list = sorted(jen_list, key=lambda x: x["time"])
            jen_list = [run_hook("process_item", item) for item in jen_list]
            jen_list = [run_hook("get_metadata", item, return_item_on_failure=True) for item in jen_list]
            run_hook("display_list", jen_list)

        @plugin.route("/sportjetextractors/search_dialog/<path:query>")
        def search_dialog(query):
            query = urllib.parse.unquote_plus(query)
            if query == "*":
                query = xbmcgui.Dialog().input("Search game")
                if query == "": return
            addon = xbmcaddon.Addon()
            USER_DATA_DIR = translatePath(addon.getAddonInfo("profile"))
            if not os.path.exists(os.path.join(USER_DATA_DIR, f"{self.name}_disabled.json")):
                disabled = DEFAULT_DISABLED
            else:
                f = open(os.path.join(USER_DATA_DIR, f"{self.name}_disabled.json"), "r")
                disabled = json.load(f)
                f.close()
            games = extractor.search_extractors(query, disabled)
            empty_date = datetime(year=2030, month=12, day=31)
            jen_list = []
            for game in games:
                jen_data = {
                    "title": "[COLORdodgerblue]%s[COLORwhite] |[B][I] %s[/B][/I]\n  [COLORred]%s | %s[/COLOR]" % (game.league.replace("'", "") if game.league is not None else "", game.title, game.extractor, format_time(game.starttime)),
                    "thumbnail": game.icon,
                    "fanart": game.icon,
                    "summary": game.title,
                    "sportjetextractors": [link.to_dict() for link in game.links],
                    "time": game.starttime.timestamp() if game.starttime != None else empty_date.timestamp(),
                    "type": "item"
                }
                jen_list.append(jen_data)
            
            idx = link_dialog([game["title"] for game in jen_list], return_idx=True, hide_links=False)
            if idx == None:
                return True
            self.play_video(json.dumps(jen_list[idx]))
        
        @plugin.route("/sportjetextractors/play")
        def play():
            urls = plugin.args["urls"][0].split("***")
            return self.play_video(json.dumps({"sportjetextractors": urls}))

        @plugin.route("/sportjetextractors/dialog")
        def dialog():
            query = xbmcgui.Dialog().input("Enter link")
            if not query: return
            self.play_video(json.dumps({"sportjetextractors": [query]}))

    
        @plugin.route("/sportjetextractors/extractor_settings")
        def extractor_settings():
            addon = xbmcaddon.Addon()
            USER_DATA_DIR = translatePath(addon.getAddonInfo("profile"))
            if not os.path.exists(USER_DATA_DIR):
                os.makedirs(USER_DATA_DIR)
            if not os.path.exists(os.path.join(USER_DATA_DIR, f"{self.name}_disabled.json")):
                f = open(os.path.join(USER_DATA_DIR, f"{self.name}_disabled.json"), "w")
                f.write(json.dumps(DEFAULT_DISABLED))
                f.close()
            
            options = filter(lambda x: x.name != None, extractor.get_extractors())
            option_names = [module.name for module in options]
            enabled = []
            f = open(os.path.join(USER_DATA_DIR, f"{self.name}_disabled.json"), "r+")
            disabled_extractors = json.load(f)
            for i, option in enumerate(option_names):
                if option not in disabled_extractors:
                    enabled.append(i)
            
            dialog = xbmcgui.Dialog().multiselect("Extractors", options=option_names, preselect=enabled)
            if dialog == None: return
            disabled = []
            for i in range(len(option_names)):
                if i not in dialog:
                    disabled.append(option_names[i])
            
            f.seek(0)
            f.write(json.dumps(disabled))
            f.truncate()
            f.close()
            xbmcgui.Dialog().ok("Success!", "Settings saved.")
        
        @plugin.route("/sportjetextractors/iptv_setup")
        def iptv_setup():
            if not xbmcgui.Dialog().yesno("IPTV Simple Client Setup", "Update IPTV Simple Client settings to use JET TV M3U8 and EPG?"):
                return
            try:
                addon = xbmcaddon.Addon('pvr.iptvsimple')
                addon.setSetting(id="m3uUrl", value=base64.b64decode("aHR0cHM6Ly9tYWduZXRpYzEucmF0cGFjay5hcHBib3hlcy5jby9qZXQvcGxheWxpc3QxLm0zdTg=").decode("utf-8"))
                addon.setSetting(id="epgUrl", value=base64.b64decode("aHR0cHM6Ly9tYWduZXRpYzEucmF0cGFjay5hcHBib3hlcy5jby9qZXQvZXBnLnhtbA==").decode("utf-8"))
                addon.setSetting(id="m3uPathType", value="1")
                addon.setSetting(id="epgPathType", value="1")
                xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}')
                xbmcgui.Dialog().ok("Success", "IPTV Simple Client settings updated.")
            except:
                xbmcgui.Dialog().ok("Error", "IPTV Simple Client is not installed.")
            



def format_time(date):
    return utc_to_local(date).strftime("%m/%d %I:%M %p") if date != None else ""

# https://stackoverflow.com/questions/4563272/convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-standard-lib
def utc_to_local(utc_dt):
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


