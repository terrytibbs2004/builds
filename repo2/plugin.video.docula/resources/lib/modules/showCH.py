
import os,sys,xbmc,xbmcaddon
import plugintools

from addon.common.addon import Addon

addonID = 'plugin.video.wrestlers'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

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

art = 'special://home/addons/script.j1.artwork/lib/resources/art/'

#====================================

channellist=[
        ("[B]WWE Channel[/B]", "user/WWEFanNation", art+'wwe6.jpg'),
        ("[B]AEW Channel[/B]", "channel/UCFN4JkGP_bVhAdBsoV9xftA", art+'aew.jpg'),
        ("[B]ROH Channel[/B]", "user/ringofhonor", art+'roh.jpg'),				
        ("[B]NWA Channel[/B]", "channel/UCSHCTJS2P4Hvu_reLKtiT6g", art+'nwa.jpg'),
        ("[B]MLW Channel[/B]", "user/majorleaguewrestling", art+'mlw.jpg'),				
        ("[B]RPW Channel[/B]", "channel/UCzaW5OsUJKVrofaK0303Yqg", art+'rpw.jpg'),
        ("[B]EVE Channel[/B]", "user/ProWrestlingEVE", art+'eve.jpg'),				
        ("[B]WOW Channel[/B]", "channel/UCwJi5YBg3nVecmokqEBECcw", art+'wow.jpg'),
        ("[B]NJPW Channel[/B]", "channel/UC1lgJkpCx_0SMzsvrTCdxPw", art+'njpw.jpg'),
        ("[B]Shine Channel[/B]", "user/SHINEWrestling", art+'shine.jpg'),				
        ("[B]Impact Channel[/B]", "user/TNAwrestling", art+'impact.jpg'),
        ("[B]Shimmer Channel[/B]", "channel/UC30Ia39JmGJASWQSyQOQYAQ", art+'shimmer.jpg'),
        ("[B]Progress Channel[/B]", "channel/UCZaS14idYb591IbxLqcyNQA", art+'progress.jpg'),
        ("[B]British Bombshells[/B]", "user/BritishBombshells", art+'bombshells.jpg'),
]

#============== Start ================

def showCH():

    plugintools.log("wrestlers.run")
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

#============= Menu =================

def main_list(params):
    plugintools.log("wrestlers.main_list "+repr(params))

for name, id, icon in channellist:
	plugintools.add_item(title=name,url="plugin://plugin.video.youtube/"+id+"/",thumbnail=icon,fanart=fanart,folder=True )

#====================================

#showCH() FOR STAND-ALONE