# -*- coding: utf-8 -*-
import xbmc, xbmcaddon

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
getsetting = addon.getSetting
setsetting = addon.setSetting

if __name__ == '__main__':
	
	if getsetting('autoenable') == 'true':
		from resources.lib import addonsEnable
		addonsEnable.enable_addons()
		xbmc.executebuiltin('UpdateLocalAddons')
		xbmc.executebuiltin('UpdateAddonRepos')
		xbmc.executebuiltin('ReloadSkin()')
		setsetting('autoenable','false')