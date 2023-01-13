# -*- coding: utf-8 -*-
"""
	Yourscrapers Module
"""

from sys import argv
from urllib.parse import parse_qsl
from yourscrapers import sources_yourscrapers
from yourscrapers.modules import control

params = dict(parse_qsl(argv[2].replace('?', '')))
action = params.get('action')
mode = params.get('mode')
query = params.get('query')
name = params.get('name')

if action is None:
	control.openSettings('0.0', 'script.module.yourscrapers')

if action == "YourScrapersSettings":
	control.openSettings('0.0', 'script.module.yourscrapers')

elif mode == "YourScrapersSettings":
	control.openSettings('0.0', 'script.module.yourscrapers')

elif action == 'ShowChangelog':
	from yourscrapers.modules import changelog
	changelog.get()

elif action == 'ShowHelp':
	from yourscrapers.help import help
	help.get(name)

elif action == "Defaults":
	sourceList = []
	sourceList = sources_yourscrapers.all_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		value = control.getSettingDefault(source_setting)
		control.setSetting(source_setting, value)

elif action == "toggleAll":
	sourceList = []
	sourceList = sources_yourscrapers.all_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllHosters":
	sourceList = []
	sourceList = sources_yourscrapers.hoster_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllTorrent":
	sourceList = []
	sourceList = sources_yourscrapers.torrent_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllPackTorrent":
	control.execute('RunPlugin(plugin://script.module.yourscrapers/?action=toggleAllTorrent&amp;setting=false)')
	control.sleep(500)
	sourceList = []
	from yourscrapers import pack_sources
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
		control.openSettings(query, 'script.module.yourscrapers')

elif action == 'syncYourAccount':
	control.syncYourAccounts()
	if params.get('opensettings') == 'true':
		control.openSettings(query, 'script.module.yourscrapers')

elif action == 'cleanSettings':
	control.clean_settings()

elif action == 'undesirablesSelect':
	from yourscrapers.modules.undesirables import undesirablesSelect
	undesirablesSelect()

elif action == 'undesirablesInput':
	from yourscrapers.modules.undesirables import undesirablesInput
	undesirablesInput()

elif action == 'undesirablesUserRemove':
	from yourscrapers.modules.undesirables import undesirablesUserRemove
	undesirablesUserRemove()

elif action == 'undesirablesUserRemoveAll':
	from yourscrapers.modules.undesirables import undesirablesUserRemoveAll
	undesirablesUserRemoveAll()

elif action == 'tools_clearLogFile':
	from yourscrapers.modules import log_utils
	cleared = log_utils.clear_logFile()
	if cleared == 'canceled': pass
	elif cleared: control.notification(message='YourScrapers Log File Successfully Cleared')
	else: control.notification(message='Error clearing YourScrapers Log File, see kodi.log for more info')

elif action == 'tools_viewLogFile':
	from yourscrapers.modules import log_utils
	log_utils.view_LogFile(name)

elif action == 'tools_uploadLogFile':
	from yourscrapers.modules import log_utils
	log_utils.upload_LogFile()
