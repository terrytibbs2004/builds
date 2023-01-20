# -*- coding: utf-8 -*-

import xbmc

if __name__ == '__main__':
	plugin = 'plugin://plugin.video.le/'
	path = 'RunPlugin(%s?action=tools_contextLESettings&opensettings=false)' % plugin
	xbmc.executebuiltin(path)
	# xbmc.executebuiltin('RunPlugin(%s?action=widgetRefresh)' % plugin) #now part of "tools_contextLESettings" action