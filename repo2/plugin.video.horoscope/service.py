import xbmc
import xbmcvfs
import xbmcaddon
from horoscope import get_horoscope, INDEX, BASE_URL

get_setting = xbmcaddon.Addon().getSetting
addon_data = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))

def startup(_name: str, _url: str):
    get_horoscope(_name, _url, startup = True)

if __name__ == '__main__':
    if get_setting('startup') == 'true':
        xbmc.sleep(5000)
        if not xbmcvfs.exists(addon_data):
            xbmcvfs.mkdirs(addon_data)
        names = [name for name in INDEX.keys()]
        selected = int(get_setting('name'))
        name = names[selected]
        url = f'{BASE_URL}{INDEX[name][0]}'
        startup(name, url)