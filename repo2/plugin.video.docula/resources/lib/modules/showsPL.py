
import os,sys,xbmc,xbmcaddon
import plugintools

from addon.common.addon import Addon

addonID = 'plugin.video.docula'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)

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

#====================================

channellist=[
        ("[B]All Elite Wrestling Dark[/B]", "playlist/PLILTWWX_AIJQwsdCDzESMR8JuhivhKwH9", mediapath+'playlist.png'),
        ("[B]MLW Fusion Episodes[/B]", "playlist/PLz-1tQr6WGHUdH-CgtnDYPX08iCO0AkT4", mediapath+'playlist.png'),
        ("[B]NWA Wrestling PoweRRR[/B]", "playlist/PLCRb96pNJPq67IUikLOnuH-DL8gc5p5U5", mediapath+'playlist.png'),				
        ("[B]PCW Ultra Mutiny[/B]", "playlist/PLyIxRJj37ULS9kTMqY-d8c1lNMfHwJEa2", mediapath+'playlist.png'),
        ("[B]ROW TV Episodes[/B]", "playlist/PLb6UFvcotwSuTctzlqmzB1TphEjrIosiq", mediapath+'playlist.png'),				
        ("[B]Smash Wrestling Episodes[/B]", "playlist/PL3yDzFetNf2a8QodpBRL7qzk3Bb5U2CHO", mediapath+'playlist.png'),
        ("[B]PPW Powerslam TV Shows[/B]", "playlist/PLlJS4O-ERa_zhzrjzusBysbHLpZNNLlSD", mediapath+'playlist.png'),
        ("[B]HOB Turnbuckle Season I[/B]", "playlist/PLd3VobSJFfMSqURhNn1zBvmAxQcpzd58n", mediapath+'playlist.png'),
        ("[B]HOB Turnbuckle Season II[/B]", "playlist/PLd3VobSJFfMRZKkBojUupThNKsNSMZ1dR", mediapath+'playlist.png'),
        ("[B]HOB Turnbuckle Season III[/B]", "playlist/PLd3VobSJFfMTDKfi2G1QLM2lipw6IkA1y", mediapath+'playlist.png'),
        ("[B]HOB Turnbuckle Season IV[/B]", "playlist/PLd3VobSJFfMQ1C3kGgEDNZhnIvXHBwRMM", mediapath+'playlist.png'),
        ("[B]Innovate Wrestling TV[/B]", "playlist/PLa7T0EXutf8eQEuZVR3Mo-lMBUAFtju_Z", mediapath+'playlist.png'),				
        ("[B]Championship Wrestling[/B]", "playlist/PLXYqkW7VSKIKgnI3M1fibZ3y-ggnnjy-T", mediapath+'playlist.png'),
        ("[B]AMW Television Shows[/B]", "playlist/PLFddunSgY7f_TJAytWoFDwbtA4LVTuWOY", mediapath+'playlist.png'),
        ("[B]PWA OHIO Episodes[/B]", "playlist/PLnzbEnDp0nWSJjCN5aC7aSZSh_ZrfrvkC", mediapath+'playlist.png'),				
        ("[B]WLW Tuesday Night Showdown[/B]", "playlist/PLN9iJGishJotQ12b21pR-vBZqNXvBazfU", mediapath+'playlist.png'),
        ("[B]WTF Wrestling Episodes[/B]", "playlist/PLUXEwb8RqRdbFaevKBtwAQpBs-FJFA6mV", mediapath+'playlist.png'),				
        ("[B]Wrestle-1 TV Episodes[/B]", "playlist/PLRPfnClI5KiMuIYqpQlNktD9Kvzm95zlg", mediapath+'playlist.png'),				
        ("[B]Capitol Wrestling[/B]", "playlist/PLXMVHZO29x1YhXYirmSdfJACCcepX46sV", mediapath+'playlist.png'),				
        ("[B]Empire Underground[/B]", "channel/UCM66j6AFtnUhzJRovyB1qaw", mediapath+'playlist.png'),				
        ("[B]OWE Wrestling Episodes[/B]", "playlist/PLHSnyLpTq8-JB_lCRuttxSYUj1-3hO9kj", mediapath+'playlist.png'),				
        ("[B]ROH Throwback Thursday[/B]", "playlist/PL53kKJBMWATdIPkA-8x6JXUhr8sE5zC9l", mediapath+'playlist.png'),				
        ("[B]CCW Superstars Channel[/B]", "channel/UCEQSsFZSyBZpjKIgSZcTbdg", mediapath+'playlist.png'),
]

#============== Start ================

def showsPL():

    plugintools.log("wrestlers.run")
    params = plugintools.get_params()
		
    #errorMsg="%s" % (params)
    #xbmcgui.Dialog().textviewer("params", errorMsg)
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

#============= Menu =================

def main_list(params):
    plugintools.log("wrestlers.main_list "+repr(params))
		
    #errorMsg="%s" % (params)
    #xbmcgui.Dialog().textviewer("params AT Main_list", errorMsg)

for name, id, icon in channellist:
    plugintools.add_item(title=name,url="plugin://plugin.video.youtube/"+id+"/",thumbnail=icon,fanart=fanart,folder=True )

#====================================
