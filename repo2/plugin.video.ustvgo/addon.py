import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
from resources.lib.data import Channels
from resources.lib.grab import grab


_URL = sys.argv[0]
_HANDLE = int(sys.argv[1])
_ADDON = xbmcaddon.Addon()

playlistvpn = 'special://home/addons/' + _ADDON.getAddonInfo('id') + '/resources/playlist_vpn.m3u'
playlistnovpn = 'special://home/addons/' + _ADDON.getAddonInfo('id') + '/resources/playlist_novpn.m3u'

def iptvsimple_setup():
    vpn = xbmcplugin.getSetting(_HANDLE, 'vpnchannels') == 'true'
    if vpn:
        try:
            pisc = xbmcaddon.Addon('pvr.iptvsimple')
        except:
            xbmcgui.Dialog().ok(_ADDON.getAddonInfo('name'), _ADDON.getLocalizedString(30010))
            xbmcplugin.setResolvedUrl(_HANDLE, False, xbmcgui.ListItem())
            return
        pisc.setSetting('m3uPathType','0')
        pisc.setSetting('m3uPath',xbmc.translatePath(playlistvpn))
        pisc.setSetting('startNum','1')
        pisc.setSetting('logoPathType','1')
        pisc.setSetting('logoBaseUrl','')
        pisc.setSetting('logoFromEpg','1')
        pisc.setSetting('epgPathType','1')
        pisc.setSetting('epgUrl','https://bit.ly/USTVGO-xml')
    else:
        try:
            pisc = xbmcaddon.Addon('pvr.iptvsimple')
        except:
            xbmcgui.Dialog().ok(_ADDON.getAddonInfo('name'), _ADDON.getLocalizedString(30010))
            xbmcplugin.setResolvedUrl(_HANDLE, False, xbmcgui.ListItem())
            return
        pisc.setSetting('m3uPathType','0')
        pisc.setSetting('m3uPath',xbmc.translatePath(playlistnovpn))
        pisc.setSetting('startNum','1')
        pisc.setSetting('logoPathType','1')
        pisc.setSetting('logoBaseUrl','')
        pisc.setSetting('logoFromEpg','1')
        pisc.setSetting('epgPathType','1')
        pisc.setSetting('epgUrl','https://bit.ly/USTVGO-xml')
    xbmcgui.Dialog().ok(_ADDON.getAddonInfo('name'), 'Done, Restart Kodi to see changes')
    xbmcplugin.setResolvedUrl(_HANDLE, False, xbmcgui.ListItem())


def get_url(**kwargs):
    return '{}?{}'.format(_URL, urlencode(kwargs))



def list_videos():
    xbmcplugin.setContent(_HANDLE, 'videos')
    vpn = xbmcplugin.getSetting(_HANDLE, 'vpnchannels') == 'true'
    for video in Channels:
        if vpn:
            list_item = xbmcgui.ListItem(label=Channels[video]['name'])
            list_item.setInfo('video', {'title': Channels[video]['name'],
                                        'genre': Channels[video]['genre'],
                                        'mediatype': 'video'})
            list_item.setArt({'thumb': Channels[video]['thumb'], 'icon': Channels[video]['thumb'], 'fanart': Channels[video]['thumb']})
            list_item.setProperty('IsPlayable', 'true')
            url = get_url(action='play', video=Channels[video]['url'])
            is_folder = False
            xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
        else:
            try:
                if Channels[video]['name'].split(" | ")[1] == '[VPN]':
                    continue
            except:
                list_item = xbmcgui.ListItem(label=Channels[video]['name'])
                list_item.setInfo('video', {'title': Channels[video]['name'],
                                            'genre': Channels[video]['genre'],
                                            'mediatype': 'video'})
                list_item.setArt({'thumb': Channels[video]['thumb'], 'icon': Channels[video]['thumb'], 'fanart': Channels[video]['thumb']})
                list_item.setProperty('IsPlayable', 'true')
                url = get_url(action='play', video=Channels[video]['url'])
                is_folder = False
                xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)


    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_HANDLE)


def play_video(path):
    play_item = xbmcgui.ListItem(path=grab(path))
    xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listing':
            list_videos(params['category'])
        elif params['action'] == 'play':
            play_video(params['video'])
        elif params['action'] == 'iptvsimple_setup':
            iptvsimple_setup()
        else:
            raise ValueError('Invalid paramstring: {}!'.format(paramstring))
    else:
        list_videos()


if __name__ == '__main__':
    router(sys.argv[2][1:])
