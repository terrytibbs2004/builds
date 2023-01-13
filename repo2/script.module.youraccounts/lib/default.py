# -*- coding: utf-8 -*-

'''
	Your Accounts
'''

import sys
try:
	from urlparse import parse_qsl
except ImportError: #Py3
	from urllib.parse import parse_qsl
from youraccounts.modules import control

control.set_active_monitor()

params = {}
for param in sys.argv[1:]:
	param = param.split('=')
	param_dict = dict([param])
	params = dict(params, **param_dict)

action = params.get('action')
query = params.get('query')
addon_id = params.get('addon_id')

if action and not any(i in action for i in ['Auth', 'Revoke']):
	control.release_active_monitor()

if action is None:
	control.openSettings(query, "script.module.youraccounts")

elif action == 'traktAcct':
	from youraccounts.modules import trakt
	trakt.Trakt().account_info_to_dialog()

elif action == 'traktAuth':
	from youraccounts.modules import trakt
	control.function_monitor(trakt.Trakt().auth)

elif action == 'traktRevoke':
	from youraccounts.modules import trakt
	control.function_monitor(trakt.Trakt().revoke)

elif action == 'alldebridAcct':
	from youraccounts.modules import alldebrid
	alldebrid.AllDebrid().account_info_to_dialog()

elif action == 'alldebridAuth':
	from youraccounts.modules import alldebrid
	control.function_monitor(alldebrid.AllDebrid().auth)

elif action == 'alldebridRevoke':
	from youraccounts.modules import alldebrid
	control.function_monitor(alldebrid.AllDebrid().revoke)

elif action == 'premiumizeAcct':
	from youraccounts.modules import premiumize
	premiumize.Premiumize().account_info_to_dialog()

elif action == 'premiumizeAuth':
	from youraccounts.modules import premiumize
	control.function_monitor(premiumize.Premiumize().auth)

elif action == 'premiumizeRevoke':
	from youraccounts.modules import premiumize
	control.function_monitor(premiumize.Premiumize().revoke)

elif action == 'realdebridAcct':
	from youraccounts.modules import realdebrid
	realdebrid.RealDebrid().account_info_to_dialog()

elif action == 'realdebridAuth':
	from youraccounts.modules import realdebrid
	control.function_monitor(realdebrid.RealDebrid().auth)

elif action == 'realdebridRevoke':
	from youraccounts.modules import realdebrid
	control.function_monitor(realdebrid.RealDebrid().revoke)

elif action == 'tmdbAuth':
	from youraccounts.modules import tmdb
	control.function_monitor(tmdb.Auth().create_session_id)

elif action == 'tmdbRevoke':
	from youraccounts.modules import tmdb
	control.function_monitor(tmdb.Auth().revoke_session_id)

elif action == 'ShowChangelog':
	from youraccounts.modules import changelog
	changelog.get()

elif action == 'ShowHelp':
	from youraccounts.help import help
	help.get(params.get('name'))

elif action == 'ShowOKDialog':
	control.okDialog(params.get('title', 'default'), int(params.get('message', '')))

elif action == 'tools_clearLogFile':
	from youraccounts.modules import log_utils
	cleared = log_utils.clear_logFile()
	if cleared == 'canceled': pass
	elif cleared: control.notification(message='Your Accounts Log File Successfully Cleared')
	else: control.notification(message='Error clearing Your Accounts Log File, see kodi.log for more info')

elif action == 'tools_viewLogFile':
	from youraccounts.modules import log_utils
	log_utils.view_LogFile(params.get('name'))

elif action == 'tools_uploadLogFile':
	from youraccounts.modules import log_utils
	log_utils.upload_LogFile()