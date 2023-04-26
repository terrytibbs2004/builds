from ..plugin import Plugin
import xbmc, xbmcgui, xbmcaddon
import json
import resolveurl
import os
import base64

try:
    from resources.lib.util.common import *
except ImportError:
    from .resources.lib.util.common import *


addon_id = xbmcaddon.Addon().getAddonInfo('id')
default_icon = xbmcaddon.Addon(addon_id).getAddonInfo('icon')
default_fanart = xbmcaddon.Addon(addon_id).getAddonInfo('fanart')

from xbmcvfs import translatePath

addon = xbmcaddon.Addon()

USER_DATA_DIR = translatePath(addon.getAddonInfo("profile"))
ADDON_DATA_DIR = translatePath(addon.getAddonInfo("path"))
RESOURCES_DIR = os.path.join(ADDON_DATA_DIR, "resources", "lib", "data")

from os.path import join
from resources.lib.util import dbase as do_data
DB = do_data.Database()
my_db = os.path.join(RESOURCES_DIR, "loop_cache.db")
my_table  = 'art' 

class default_play_video(Plugin):
    name = "default video playback"
    priority = 0

    def play_video(self, item):
        item = json.loads(item)
        if "link" not in item: return False
        link = item["link"]        
        title = item["title"]
        
        my_id = item.get("id", "empty")
        
        if my_id == "empty" :                         
            thumbnail = item.get("thumbnail", default_icon)
            fanart = item.get("fanart", default_fanart)                                       
        else :      
            check_data = DB.search_db(my_db, my_table, int(my_id)) 
            do_log(f'{self.name} - data returned = \n {str(check_data)} ' )  
            if not check_data :
                my_thumb = thumbnail
                my_art = fanart
            else :
                my_thumb = base64.b64decode(check_data[-2][::-1]).decode()
                my_art = base64.b64decode(check_data[-1][::-1]).decode()     


           
            if my_thumb.startswith('http') : thumbnail = my_thumb
            else : thumbnail = default_icon
            if my_art.startswith('http') : fanart = my_art   
            else : fanart = default_fanart       
        
        
        # thumbnail = item.get("thumbnail", default_icon)
        liz = xbmcgui.ListItem(title)
        liz.setInfo('video', {'Title': title})
        liz.setArt({'thumb': thumbnail, 'icon': thumbnail})
        
        if resolveurl.HostedMediaFile(link).valid_url():
        	url = resolveurl.HostedMediaFile(link).resolve()
        	return xbmc.Player().play(url,liz)
        else:
        	return xbmc.Player().play(link,liz)
       
       