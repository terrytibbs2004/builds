# -*- coding: utf-8 -*-
"""
	LEscrapers Module
"""

from sys import argv
try: #Py2
	from urlparse import parse_qsl
except ImportError: #Py3
	from urllib.parse import parse_qsl
from lescrapers import sources_lescrapers
from lescrapers.modules import control

params = dict(parse_qsl(argv[2].replace('?', '')))
action = params.get('action')
mode = params.get('mode')
query = params.get('query')
name = params.get('name')

if action is None:
	xbmc.log('Hello from LEScrapers', 2)
	control.openSettings('0.0', 'script.module.lescrapers')

if action == "LEScrapersSettings":
	control.openSettings('0.0', 'script.module.lescrapers')

elif mode == "LEScrapersSettings":
	control.openSettings('0.0', 'script.module.lescrapers')

elif action == 'ShowChangelog':
	from lescrapers.modules import changelog
	changelog.get()

elif action == 'ShowHelp':
	from lescrapers.help import help
	help.get(name)

elif action == "Defaults":
	sourceList = []
	sourceList = sources_lescrapers.all_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		value = control.getSettingDefault(source_setting)
		control.setSetting(source_setting, value)

elif action == "toggleAll":
	sourceList = []
	sourceList = sources_lescrapers.all_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllHosters":
	sourceList = []
	sourceList = sources_lescrapers.hoster_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllTorrent":
	sourceList = []
	sourceList = sources_lescrapers.torrent_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllPackTorrent":
	control.execute('RunPlugin(plugin://script.module.lescrapers/?action=toggleAllTorrent&amp;setting=false)')
	control.sleep(500)
	sourceList = []
	from lescrapers import pack_sources
	sourceList = pack_sources()
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == 'openYourAccount':
	from youraccounts import openYASettings
	openYASettings('0.0')
	control.sleep(500)
	while control.condVisibility('Window.IsVisible(addonsettings)') or control.homeWindow.getProperty('youraccounts.active') == 'true':
		control.sleep(500)
	control.sleep(100)
	control.syncYourAccounts()
	control.sleep(100)
	if params.get('opensettings') == 'true':
		control.openSettings(query, 'script.module.lescrapers')

elif action == 'syncYourAccount':
	control.syncYourAccounts()
	if params.get('opensettings') == 'true':
		control.openSettings(query, 'script.module.lescrapers')

elif action == 'cleanSettings':
	control.clean_settings()

elif action == 'undesirablesSelect':
	from lescrapers.modules import source_utils
	source_utils.undesirablesSelect()

elif action == 'tools_clearLogFile':
	from lescrapers.modules import log_utils
	cleared = log_utils.clear_logFile()
	if cleared == 'canceled': pass
	elif cleared: control.notification(message='LEScrapers Log File Successfully Cleared')
	else: control.notification(message='Error clearing LEScrapers Log File, see kodi.log for more info')

elif action == 'tools_viewLogFile':
	from lescrapers.modules import log_utils
	log_utils.view_LogFile(name)

elif action == 'tools_uploadLogFile':
	from lescrapers.modules import log_utils
	log_utils.upload_LogFile()