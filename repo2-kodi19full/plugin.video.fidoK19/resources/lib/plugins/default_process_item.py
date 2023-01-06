from resources.lib.plugins.summary import Summary
from ..plugin import Plugin
import xbmcgui
import base64
import json

import urllib.parse
try:
    from resources.lib.util.common import *
except ImportError:
    from .resources.lib.util.common import *

import xbmcaddon
import xbmcvfs
import requests

addon_data = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
downloads_path = addon_data + 'downloads/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
headers = {"User-Agent": user_agent}
addon_id = xbmcaddon.Addon().getAddonInfo('id')
default_icon = xbmcaddon.Addon(addon_id).getAddonInfo('icon')
default_fanart = xbmcaddon.Addon(addon_id).getAddonInfo('fanart')
    
class default_process_item(Plugin):
    name = "default process item"
    priority = 0

    def process_item(self, item):
        do_log(f'{self.name} - Item = \n {str(item)} ' )  
        is_dir = False
        tag = item["type"]
        link = item.get("link", "")
        summary = item.get("summary")
        context = item.get("contextmenu")
        #if summary:
            #del item["summary"]
        if context:
            del item["contextmenu"]
        if link:
            if tag == "dir":
                if link.endswith(".m3u") or link.endswith(".m3u8"):
                    link = f"m3u|{link}"
                link = f"/get_list/{link}"
                is_dir = True
                
            if tag == "plugin":   
                plug_item = urllib.parse.quote_plus(str(link))  
                if 'youtube' in plug_item:
                    link = f"/get_list/{link}"
                    is_dir = True
                else :
                    link = f"/run_plug/{plug_item}"                 
                    is_dir = False
            if tag == "script":
                script_item = urllib.parse.quote_plus(str(link))
                link = f"/run_script/{script_item}"
                is_dir = False 
        if tag == "item":
            link_item = base64.urlsafe_b64encode(bytes(json.dumps(item), 'utf-8')).decode("utf-8")
            
            if str(link).lower() == 'settings' :
                link = "settings" 
            
            elif str(link).lower() == "clear_cache":
                link = "clear_cache"
                
            elif str(link).lower().startswith("message/") :   
                link = f"show_message/{link}"
                               
            else :     
                link = f"play_video/{link_item}"
                        
        # thumbnail = item.get("thumbnail", "")
        # fanart = item.get("fanart", "")
                        
        thumbnail = gif_check(item.get("thumbnail", default_icon))
        fanart = gif_check(item.get("fanart", default_fanart))
        list_item = xbmcgui.ListItem(
            item.get("title", item.get("name", "")), offscreen=True
        )
        list_item.setArt({"thumb": thumbnail, "icon": thumbnail, "poster": thumbnail, "fanart": fanart})
        item["list_item"] = list_item
        item["link"] = link
        item["is_dir"] = is_dir
        if summary:
            item["summary"] = summary
        if context:
            item["contextmenu"] = context
        '''if item.get("infolabels"):
            list_item.setInfo("video", infoLabels=item['infolabels'])
        if item.get("cast"):
            list_item.setCast(item['cast'])'''
        return item

def gif_check(url: str) -> str:
    if not url or type(url) == str and not url.endswith('.gif'):
        return (url)
    
    if not xbmcvfs.exists(downloads_path):
        xbmcvfs.mkdirs(downloads_path)
    
    file_name = url.split('/')[-1]
    new_url = downloads_path + file_name
    if xbmcvfs.exists(new_url):
        return new_url
        
    with requests.get(url, headers, stream=True) as r:
        with open(new_url, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1000000):
                f.write(chunk)
    
    return new_url