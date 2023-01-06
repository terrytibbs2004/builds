
import urllib, sys, re, os, unicodedata
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs

try:
    # Python 3
    from urllib.request import urlopen, Request
except ImportError:
    # Python 2
    from urllib2 import urlopen, Request

try:
    # Python 3
    from html.parser import HTMLParser
except ImportError:
    # Python 2
    from HTMLParser import HTMLParser

try:
    # Python 3
    from urllib.parse import unquote_plus, quote_plus
except ImportError:
    # Python 2
    from urllib import unquote_plus, quote_plus

from resources.lib.modules.docula import *
from resources.lib.modules.diyfix import *
from resources.lib.modules.scraper import *
from resources.lib.modules.common import *
from resources.lib.modules.showVID import *

addon_id     = xbmcaddon.Addon().getAddonInfo('id') 
artAddon     = 'script.j1.artwork'

selfAddon = xbmcaddon.Addon(id=addon_id)
plugin_handle = int(sys.argv[1])
dialog = xbmcgui.Dialog()
mysettings = xbmcaddon.Addon(id = 'plugin.video.docula')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')

try:
    datapath= xbmcvfs.translatePath(selfAddon.getAddonInfo('profile'))
except:
    datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))

try:
    fanart = xbmcvfs.translatePath(os.path.join(home, 'fanart.jpg'))
    icon = xbmcvfs.translatePath(os.path.join(home, 'icon.png'))
except:
    fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
    icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

mediapath = 'http://j1wizard.net/media/'

#=========================================================================================================================

def Main():

	add_link_info('[B][COLORorange]== Docula ==[/COLOR][/B]', mediapath+'docula.png', fanart)

	addDirMain('[COLOR white][B]Documentary: Live Streams[/B][/COLOR]',BASE,21,mediapath+'docula_live.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Muzic Docs[/B][/COLOR]',BASE,405,mediapath+'docula_muzic.jpg',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Sports Docs[/B][/COLOR]',BASE,404,mediapath+'docula_sportz.jpg',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Wrestling[/B][/COLOR]',BASE,403,mediapath+'docula_wrestle.jpg',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: History[/B][/COLOR]',BASE,402,mediapath+'docula_history.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Channels[/B][/COLOR]',BASE,22,mediapath+'docula_channels.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Crime[/B][/COLOR]',BASE,20,mediapath+'docula_crime.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: For Kids[/B][/COLOR]',BASE,30,mediapath+'docula_kids.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Music[/B][/COLOR]',BASE,23,mediapath+'docula_music.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Mystery[/B][/COLOR]',BASE,24,mediapath+'docula_mystery.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Nature[/B][/COLOR]',BASE,25,mediapath+'docula_nature.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Scary[/B][/COLOR]',BASE,26,mediapath+'docula_scary.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Space[/B][/COLOR]',BASE,27,mediapath+'docula_space.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Sports[/B][/COLOR]',BASE,28,mediapath+'docula_sports.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: Wildlife[/B][/COLOR]',BASE,292,mediapath+'docula_wild.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: UFO[/B][/COLOR]',BASE,29,mediapath+'docula_ufo.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Documentary: DIY FIX[/B][/COLOR]',BASE,40,mediapath+'docula_diyfix.png',mediapath+'fanart.jpg')

	add_link_info('[B][COLORorange] [/COLOR][/B]', mediapath+'docula.png', fanart)

#=========================================================================================================================

def Diyfix_main():

	add_link_info('[B][COLORorange]=== DIY FIX ===[/COLOR][/B]', mediapath+'diyfix.png', fanart)
	
	addDirMain('[COLOR white][B]Fix Musical Instruments[/B][/COLOR]',BASE,44,mediapath+'diy_musical.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Sm. Appliance Repair[/B][/COLOR]',BASE,41,mediapath+'diy_gadgets.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Appliance Repair[/B][/COLOR]',BASE,42,mediapath+'diy_appliance.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Lawnmower Repair[/B][/COLOR]',BASE,45,mediapath+'diy_lawn.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Home Repair And More[/B][/COLOR]',BASE,46,mediapath+'diy_home.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Electronics Repair[/B][/COLOR]',BASE,47,mediapath+'diy_electronics.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Gardening And More[/B][/COLOR]',BASE,43,mediapath+'diy_garden.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Automotive Repair[/B][/COLOR]',BASE,48,mediapath+'diy_auto.png',mediapath+'fanart.jpg')
	addDirMain('[COLOR white][B]Pets Info And Tips[/B][/COLOR]',BASE,49,mediapath+'diy_pets.png',mediapath+'fanart.jpg')

	add_link_info('[B][COLORlime] [/COLOR][/B]', mediapath+'diyfix.png', fanart)
		
params=get_params()
url=None
name=None
iconimage=None
mode=None
description=None

#=====================================================

try:
        url=unquote_plus(params["url"])
except:
        pass
try:
        name=unquote_plus(params["name"])
except:
        pass
try:
        mode = unquote_plus(params["mode"])
except:
        pass
try:
        iconimage=unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

#======= DOCULA =======

if mode == 20:
	CrimeDoc()
		
elif mode == 21:
	LiveChannel()		
		
elif mode == 22:
	Docula_Channels()

elif mode == 23:
	MusicDoc()
	
elif mode == 24:
	Mystery()

elif mode == 25:
	Nature()

elif mode == 26:
	Scary()

elif mode == 27:
	Space()
	
elif mode == 28:
	Docula_sports()

elif mode == 29:
	UFO()

elif mode == 292:
	Docula_Wild()

elif mode == 30:
	Docula_kids()
	
#===== DIY FIX =====
	
elif mode == 40:
    Diyfix_main()

elif mode == 41:
	Gadgets()		
		
elif mode == 42:
	Appliance()

elif mode == 43:
	Garden()
	
elif mode == 44:
	DIY_Musical()

elif mode == 45:
	Lawn()

elif mode == 46:
	Home()

elif mode == 47:
	Electronics()
	
elif mode == 48:
	Auto()

elif mode == 49:
	Pets()

elif mode==None:
	Main()
		
#----------------------------------------------------------------
	
elif mode == 402:
    Listing.Genres("All","History")
	
elif mode == 403:
    Listing.Genres("All","Wrestling")
	
elif mode == 404:
    Listing.Genres("All","Sports")
	
elif mode == 405:
    Listing.Genres("All","Music")

#=========================================

elif mode == 801:
		
	#errorMsg="%s" % (url)
	#xbmcgui.Dialog().ok("url", errorMsg)

	Common.getVID(url)

#=========================================

#elif mode in muziclib.Common.get_singles_genres():
#    Singles.genre_list(mode)

elif mode is None:
	Main()
		
#----------------------------------------------------------------
		
xbmcplugin.endOfDirectory(plugin_handle)
		
#----------------------------------------------------------------
