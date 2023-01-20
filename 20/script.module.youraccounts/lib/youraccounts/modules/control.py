# -*- coding: utf-8 -*-
"""
	Your Accounts
"""

import os.path
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

def getKodiVersion():
	return int(xbmc.getInfoLabel("System.BuildVersion")[:2])

addon = xbmcaddon.Addon
addonObject = addon('script.module.youraccounts')
addonInfo = addonObject.getAddonInfo
getLangString = xbmcaddon.Addon().getLocalizedString
condVisibility = xbmc.getCondVisibility
execute = xbmc.executebuiltin
monitor = xbmc.Monitor()
transPath = xbmc.translatePath if getKodiVersion() < 19 else xbmcvfs.translatePath
joinPath = os.path.join

dialog = xbmcgui.Dialog()
window = xbmcgui.Window(10000)
progressDialog = xbmcgui.DialogProgress()

existsPath = xbmcvfs.exists
openFile = xbmcvfs.File
makeFile = xbmcvfs.mkdir

progress_line = '%s[CR]%s[CR]%s'

def setting(id):
	return xbmcaddon.Addon('script.module.youraccounts').getSetting(id)

def setSetting(id, value):
	return xbmcaddon.Addon('script.module.youraccounts').setSetting(id, value)

def lang(language_id):
	text = getLangString(language_id)
	if getKodiVersion() < 19:
		text = text.encode('utf-8', 'replace')
	return text

def sleep(time):  # Modified `sleep` command that honors a user exit request
	while time > 0 and not monitor.abortRequested():
		xbmc.sleep(min(100, time))
		time = time - 100

def check_version_numbers(current, new): # Compares version numbers and return True if new version is newer
	current = current.split('.')
	new = new.split('.')
	step = 0
	for i in current:
		if int(new[step]) > int(i):
			return True
		if int(i) == int(new[step]):
			step += 1
			continue
	return False

def addonId():
	return addonInfo('id')

def addonName():
	return addonInfo('name')

def addonVersion():
	return addonInfo('version')

def addonIcon():
	return addonInfo('icon')

def addonPath():
	try: return transPath(addonInfo('path').decode('utf-8'))
	except: return transPath(addonInfo('path'))

def artPath():
	return os.path.join(xbmcaddon.Addon('script.module.youraccounts').getAddonInfo('path'), 'resources', 'icons')

def openSettings(query=None, id=addonInfo('id')):
	try:
		idle()
		execute('Addon.OpenSettings(%s)' % id)
		if query is None: return
		c, f = query.split('.')
		if getKodiVersion() >= 18:
			execute('SetFocus(%i)' % (int(c) - 100))
			execute('SetFocus(%i)' % (int(f) - 80))
		else:
			execute('SetFocus(%i)' % (int(c) + 100))
			execute('SetFocus(%i)' % (int(f) + 200))
	except:
		return

def idle():
	if getKodiVersion() >= 18 and condVisibility('Window.IsActive(busydialognocancel)'):
		return execute('Dialog.Close(busydialognocancel)')
	else:
		return execute('Dialog.Close(busydialog)')

def notification(title=None, message=None, icon=None, time=3000, sound=False):
	if title == 'default' or title is None: title = addonName()
	if isinstance(title, int): heading = lang(title)
	else: heading = str(title)
	if isinstance(message, int): body = lang(message)
	else: body = str(message)
	if icon is None or icon == '' or icon == 'default': icon = addonIcon()
	elif icon == 'INFO': icon = xbmcgui.NOTIFICATION_INFO
	elif icon == 'WARNING': icon = xbmcgui.NOTIFICATION_WARNING
	elif icon == 'ERROR': icon = xbmcgui.NOTIFICATION_ERROR
	dialog.notification(heading, body, icon, time, sound=sound)

def yesnoDialog(line, heading=addonInfo('name'), nolabel='', yeslabel=''):
	return dialog.yesno(heading, line, nolabel, yeslabel)

def selectDialog(list, heading=addonInfo('name')):
	return dialog.select(heading, list)

def okDialog(title=None, message=None):
	if title == 'default' or title is None: title = addonName()
	if isinstance(title, int): heading = lang(title)
	else: heading = str(title)
	if isinstance(message, int): body = lang(message)
	else: body = str(message)
	return dialog.ok(heading, body)

def closeAll():
	return execute('Dialog.Close(all, true)')

def jsondate_to_datetime(jsondate_object, resformat, remove_time=False):
	import _strptime  # fix bug in python import
	from datetime import datetime
	import time
	if remove_time:
		try: datetime_object = datetime.strptime(jsondate_object, resformat).date()
		except TypeError: datetime_object = datetime(*(time.strptime(jsondate_object, resformat)[0:6])).date()
	else:
		try: datetime_object = datetime.strptime(jsondate_object, resformat)
		except TypeError: datetime_object = datetime(*(time.strptime(jsondate_object, resformat)[0:6]))
	return datetime_object

def set_active_monitor():
	window.setProperty('youraccounts.active', 'true')

def release_active_monitor():
	window.clearProperty('youraccounts.active')

def function_monitor(func, query='0.0'):
	func()
	sleep(100)
	openSettings(query)
	while not condVisibility('Window.IsVisible(addonsettings)'):
		sleep(250)
	sleep(100)
	release_active_monitor()

def refresh_debugReversed(): # called from service "onSettingsChanged" to clear youraccounts.log if setting to reverse has been changed
	if window.getProperty('youraccounts.debug.reversed') != setting('debug.reversed'):
		window.setProperty('youraccounts.debug.reversed', setting('debug.reversed'))
		execute('RunScript(script.module.youraccounts, action=tools_clearLogFile)')