# used accross all addon
from urllib.parse import urlencode
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
# from xbmcvfs import translatePath
import os
from ..plugin import Plugin
from ..DI import DI

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_version = xbmcaddon.Addon().getAddonInfo('version')
ownAddon = xbmcaddon.Addon(id=addon_id)
debugMode = ownAddon.getSetting('debug') or 'false' 
PATH = xbmcaddon.Addon().getAddonInfo("path")
   
def do_log(info):   
    if debugMode. lower() == 'true' :       
        pass
        # xbmc.log(f' > MicroJen Log > \n {info}', xbmc.LOGINFO)

def xbmc_curl_encode(url, headers):
    return f"{url}|{urlencode(headers)}"

class message(Plugin):
    name = "pop up message box"
    priority = 0    
    
    def routes(self, plugin):
        @plugin.route("/show_message/<path:message>")
        def show_message(message, header = 'Information'):
            message = message.replace('message/','')
            if message.lower().startswith("http"):
                message = DI.session.get(message).text
            elif message.lower().startswith("file://"):                
                message = message.replace("file://", "")
                input_file = xbmcvfs.File(os.path.join(PATH, "xml", message))              
                message = input_file.read()
            xbmc.executebuiltin("ActivateWindow(10147)")
            controller = xbmcgui.Window(10147)
            xbmc.sleep(500)
            controller.getControl(1).setLabel(header)
            controller.getControl(5).setText(f"{message}")

def download(url: str, dest_folder: str):
    import os
    import requests
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    if filename == 'final_art.json' : filename = 'art_data.json' 
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("\n" + f"saving to {os.path.abspath(file_path)}" )
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    # os.fsync(f.fileno())
    else:  
        print("\n" + f"Download failed: status code {r.status_code}\n{r.text}")
        
    # download2(url, dest_folder)
        
    
    
def download2(url: str, dest_folder: str) :
    from urllib.request import urlopen
    
    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    if filename == 'final_art.json' : filename = 'art_data.json' 
    file_name = os.path.join(dest_folder, filename)
        
    u = urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()    
    file_size_dl = 0
    block_sz = 1024 * 8 # 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)       
    f.close()
    
    return


def check_cache(chk_cache : str, chk_local : str) :
    from datetime import datetime
    import os
    import requests
    remote_cache = chk_cache 
    local_cache = chk_local 
    
    if not os.path.isfile(local_cache) : 
        # print (' \n' + f'Local Cache Missing') 
        cache_update = 'yes' 
    else :   
        try :   
            # check server file age 
            request = requests.get(remote_cache, timeout=5) # , verify=False)
            server_last_modified = request.headers['Last-Modified']
            server_dt_stamp = datetime.strptime(server_last_modified, '%a, %d %b %Y %H:%M:%S %Z').timestamp()
    
            # check local file age
            stat = os.stat(local_cache)
            if stat.st_mtime == 0: local_dt_stamp = stat.st_ctime
            else : local_dt_stamp = stat.st_mtime
            local_last_modified = 'Unknown' 
            local_last_modified = datetime.fromtimestamp(local_dt_stamp).strftime('%a, %d %b %Y %H:%M:%S %Z')
    
            if local_dt_stamp < server_dt_stamp : cache_update = 'yes' 
            else : cache_update = 'no'  
        except :   
            cache_update = 'yes' 
      
    return cache_update
   
# def use_artID(my_id=None) :
def use_artID(item, my_id=None) :
    ch_data = [] 
    if not my_id : return ch_data
    import xbmcaddon
    from xbmcvfs import translatePath
    import base64, os
    addon = xbmcaddon.Addon()
    def_icon = xbmcaddon.Addon(addon_id).getAddonInfo('icon')
    def_fanart = xbmcaddon.Addon(addon_id).getAddonInfo('fanart')

    USER_DATA_DIR = translatePath(addon.getAddonInfo("profile"))
    ADDON_DATA_DIR = translatePath(addon.getAddonInfo("path"))
    RESOURCES_DIR = os.path.join(ADDON_DATA_DIR, "resources", "lib", "data")

    from os.path import join
    from resources.lib.util import dbase as do_data
    DB = do_data.Database()
    my_db = os.path.join(RESOURCES_DIR, "loop_cache.db")
    my_table  = 'art' 
    
    ch_data = DB.search_db(my_db, my_table, int(my_id)) 
    
    if not ch_data :
        my_thumb = def_icon
        my_art = def_fanart
    else :
        my_thumb = base64.b64decode(ch_data[-2][::-1]).decode()
        my_art = base64.b64decode(ch_data[-1][::-1]).decode()     
           
    if my_thumb.startswith('http') : this_thumb = my_thumb
    else : this_thumb = item.get("thumbnail", def_icon) # def_icon
    if my_art.startswith('http') : this_art = my_art   
    else : this_art = item.get("fanart", def_fanart  )  # def_fanart  
 
   
    return this_thumb, this_art
 
 