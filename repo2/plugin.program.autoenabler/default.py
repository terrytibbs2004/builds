# -*- coding: utf-8 -*-
import sys
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
from urllib.parse import quote_plus, unquote_plus

handle = int(sys.argv[1]) 
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
getsetting = addon.getSetting
setsetting = addon.setSetting
addoninfo = addon.getAddonInfo
addon_name = addoninfo('name')
addon_icon = addoninfo("icon")
dialog = xbmcgui.Dialog() 

def addDir(name,mode,iconimage,description, addcontext=False,isFolder=False):
	
	u=sys.argv[0]+"?name="+quote_plus(name)+"&mode="+str(mode)+"&icon="+quote_plus(iconimage) +"&description="+quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name)
	liz.setArt({'fanart':fanart,'icon':'DefaultFolder.png','thumb':iconimage})
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description,})
	if addcontext:
		contextMenu = []
		liz.addContextMenuItems(contextMenu)
	ok=xbmcplugin.addDirectoryItem(handle=handle,url=u,listitem=liz,isFolder=isFolder)
	return ok

def Main():
	addDir('Enable All Addons Now',1,addon_icon,'Enable all the addons that are currently disabled.')
	addDir('Enable All Addons On Next Startup',2,addon_icon, 'Sets Kodi to enable all addons on the next startup.')
	addDir('Cancel Next Startup',3,addon_icon,'Cancels enabling addons on next startup.')
	xbmcplugin.endOfDirectory(handle)

def enable_now():
	yes_enable = dialog.yesno(addon_name, 'Do you want to enable all addons now?', nolabel='Cancel',yeslabel='Enable Addons')
	if yes_enable:
		from resources.lib import addonsEnable
		addonsEnable.enable_addons()
		ok = dialog.ok(addon_name, 'All addons have been enabled.')
	else:
		return
	
def enable_next_start():
	yes_enable = dialog.yesno(addon_name, 'Do you want to enable all addons on next startup?', nolabel='Cancel',yeslabel='Enable Addons')
	if yes_enable:
		setsetting('autoenable','true')
		ok = dialog.ok(addon_name, 'Enable all addons is now set for next startup.')
	else:
		return

def cancel_next_start():
	yes_cancel = dialog.yesno(addon_name, 'Do you want to cancel enable all addons on next startup?', nolabel='Keep Set',yeslabel='Cancel Enable')
	if yes_cancel:
		setsetting('autoenable','false')
		ok = dialog.ok(addon_name, 'Enable addons cancelled')
	else:
		return

def GetParams():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

params=GetParams()
url=None
name=None
name2=None
version=None
mode=None
iconimage=None
fanart=None
description=None
xbmc.log(str(params),xbmc.LOGDEBUG)

try:
	name=unquote_plus(params["name"])
except:
	pass
try:        
	mode=int(params["mode"])
except:
	pass
try:
	iconimage= unquote_plus(params["iconimage"])
except:
	pass
try:
    description= unquote_plus(params["description"])
except:
	pass

if mode==None:
	Main()
elif mode==1:
	enable_now()
	xbmc.executebuiltin('UpdateLocalAddons')
	xbmc.executebuiltin('UpdateAddonRepos')
elif mode==2:
	enable_next_start()
elif mode==3:
	cancel_next_start()