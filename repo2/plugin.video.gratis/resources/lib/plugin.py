import xbmc
import xbmcvfs
import xbmcgui
import xbmcaddon
import xbmcplugin
import sys
import json
import requests
from base64 import b64decode
from urllib.parse import quote_plus, unquote_plus
from bs4 import BeautifulSoup as bs


class Myaddon:
    
    addon_id = xbmcaddon.Addon().getAddonInfo('id')
    addon_name = xbmcaddon.Addon().getAddonInfo('name')
    addon_data = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
    downloads_path = addon_data + 'downloads'
    addon_path = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('path'))
    addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
    addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
    addon_version = xbmcaddon.Addon().getAddonInfo('version')
    get_setting = xbmcaddon.Addon().getSetting
    set_setting = xbmcaddon.Addon().setSetting
    api_key = b64decode('ZDQxZmQ5OTc4NDg2MzIxYjQ2NmUyOWJmZWMyMDM5MDI=').decode('utf-8')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    headers = {"User-Agent":user_agent, "Connection":'keep-alive', 'Accept':'audio/webm,audio/ogg,udio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'}
    
    #---Request and Other Various Methods---#
    
    def get_page(self, page):
        if page.startswith('http'):
            return requests.get(page, headers=Myaddon.headers).text
        return None
    
    def write_to_file(self, _file, _string):
        with open(_file, 'w', encoding='utf-8') as f:
            f.write(_string)

    def get_json(self, page):
        return json.loads(self.get_page(page))
    
    def write_json(self, file_path, items):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({'items': items}, f, indent = 4)
    
    def get_soup(self, url):
        if url.startswith('http'):
            return bs(self.get_page(url), 'html.parser')
        return None
    
    def write_soup(self, file_path, url):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.get_soup(url).prettify())
    
    def textview(self, string: str):
        d = xbmcgui.Dialog()
        return d.textviewer(m.addon_name, string)

    #---Add Directory Method---#

    def add_dir(self, name, url, mode, icon, fanart, description, name2 = '', page='', foldername='', addcontext=False, hls=False, isFolder=True):
        u=sys.argv[0]+'?name='+quote_plus(name)+'&url='+quote_plus(url)+'&mode='+str(mode)+'&icon='+quote_plus(icon) +'&fanart='+quote_plus(fanart)+'&description='+quote_plus(description)+'&name2='+quote_plus(name2)+'&page='+str(page)+'&foldername='+quote_plus(foldername)
        liz=xbmcgui.ListItem(name)
        liz.setArt({'fanart': fanart, 'icon': icon, 'thumb': icon, 'poster': icon})
        liz.setInfo('video', {'title': name, 'plot': description})
        if addcontext is True:
            contextMenu = []
            liz.addContextMenuItems(contextMenu)
        if hls is True:
            liz.setProperty('inputstream', 'inputstream.adaptive')
            liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
            liz.setMimeType('application/vnd.apple.mpegurl')
            liz.setContentLookup(False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder=isFolder)
    
    def append_links(self, lists1, lists2):
        for _list in lists2:
            lists1.append(_list)
        return lists1
    
    def get_multilink(self, lists, lists2=None, trailers=None):
        names = []
        links = []
        counter = 1
        if lists2 is not None:
            for _list in lists2:
                lists.append(_list)
        for name, link in lists:
            names.append(f'Link {str(counter)}: {name}')
            links.append(link)
            counter += 1
        if trailers is not None:
            for name, link in trailers:
                names.append(name)
                links.append(link)
        if len(links) > 1:
            dialog = xbmcgui.Dialog()
            ret = dialog.select('Choose a Link', names)
            if ret > -1:
                return links[ret]
            else:
                return None
        elif len(links) == 1:
            return links[0]
        else:
            return None
    
    def from_keyboard(self, default_text='', header='Search'):
        kb = xbmc.Keyboard(default_text, header, False)
        kb.doModal()
        if (kb.isConfirmed()):
            return kb.getText()
        else:
            return None
    
    #---Video Player---#

    def play_video(self, name, url, icon, description,resolve=True):
           if url is None:
               return
           url = unquote_plus(url)
           liz = xbmcgui.ListItem(name)
           liz.setInfo('video', {'title': name, 'plot':description})
           liz.setArt({'thumb': icon, 'icon': icon})
           if resolve is True:
               import resolveurl
               if resolveurl.HostedMediaFile(url).valid_url():
                   url = resolveurl.HostedMediaFile(url).resolve()
           xbmc.Player().play(url, liz)

m = Myaddon()