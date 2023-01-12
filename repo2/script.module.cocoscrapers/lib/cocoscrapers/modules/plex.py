# -*- coding: utf-8 -*-
"""
	Original From My Accounts
"""

import re
import requests
from platform import system as platform_system, machine as platform_machine
import uuid
from cocoscrapers.modules import control
from cocoscrapers.modules.control import existsPath, dataPath, makeFile, plexSharesFile
from cocoscrapers.modules import dom_parser
from cocoscrapers.modules import log_utils
import sqlite3 as db

base_url = 'https://plex.tv'
kodiVersion = control.getKodiVersion(full=True)


class Plex():
	def __init__(self):
		self.chosen_share = None
		self.token = control.setting('plex.token')
		self.client_id = control.setting('plex.client_id')
		self.device_id = control.setting('plex.device_id')
		self.headers = {
			'X-Plex-Device-Name': 'CocoScrapers',
			'X-Plex-Product': 'PlexNet',
			'X-Plex-Version': '0.3.4',
			'X-Plex-Platform': 'Kodi',
			'X-Plex-Platform-Version': str(kodiVersion),
			'X-Plex-Device': str(platform_system()),
			'X-Plex-Model': str(platform_machine()),
			'X-Plex-Provides': 'player',
			'X-Plex-Client-Identifier': str(hex(uuid.getnode()))}

	def auth_loop(self):
		control.sleep(5000)
		data = requests.get(self.check_url, headers=self.headers)
		if data.status_code != 200: return self.plex_error(data.status_code)
		try: self.token = re.search(r'<auth_token>(.*?)</auth_token>', data.text, re.I).group(1)
		except: self.token = ''
		if self.token:
			self.client_id = re.search(r'<client-identifier>(.*?)</client-identifier>', data.text, re.I).group(1)
			control.progressDialog.close()
			control.setSetting('plex.token', self.token)
			control.setSetting('plex.client_id', self.client_id)
			control.sleep(500)
			new_id = self.get_authID()
			control.setSetting('plex.device_id', new_id)
			self.get_plexshare_resource()

	def auth(self):
		self.token = ''
		url = base_url + '/pins.xml'
		code_data = requests.post(url, headers=self.headers)
		if code_data.status_code != 201: return self.plex_error(code_data.status_code)
		code_data = code_data.text
		code = re.search(r'<code>(.*?)</code>', code_data, re.I).group(1)
		self.device_id = re.search(r'<id.+?>(.*?)</id>', code_data, re.I).group(1)
		control.progressDialog.create('Plex Auth')
		control.progressDialog.update(-1, control.progress_line % (control.lang(32513) % 'https://plex.tv/link/', control.lang(32514) % code, ''))
		self.check_url = base_url + '/pins/%s.xml' % self.device_id
		control.sleep(2000)
		while not self.token:
			if control.progressDialog.iscanceled():
				control.progressDialog.close()
				break
			self.auth_loop()

	def plex_error(self, error_code):
		log_utils.log('Plex api error: %s' % error_code, __name__, log_utils.LOGWARNING)
		control.notification(title='Plex', message='Plex server error: %s, please try again' % error_code)

	def get_authID(self):
		url = base_url + '/devices.xml?X-Plex-Client-Identifier=%s&X-Plex-Token=%s' % (self.client_id, self.token)
		results = requests.get(url, headers=self.headers)
		if results.status_code != 200: return self.plex_error(results.status_code)
		devices = re.findall(r'(<Device\s.+?</Device>)', results.text, flags=re.M | re.S)
		for device in devices:
			device_token = dom_parser.parseDOM(device, 'Device', ret='token')[0]
			if device_token != self.token: continue
			return dom_parser.parseDOM(device, 'Device', ret='id')[0]

	def get_plexshare_resource(self):
		url = base_url + '/api/v2/resources?includeHttps=1&X-Plex-Client-Identifier=%s&X-Plex-Token=%s' % (self.client_id, self.token)
		resources = requests.get(url, headers=self.headers)
		if resources.status_code != 200: return self.plex_error(resources.status_code)
		resources = re.findall(r'(<resource\s.+?</resource>)', resources.text, flags=re.M | re.S)
		share_url = ''
		self.clearPlex()
		for resource in resources:
			product = dom_parser.parseDOM(resource, 'resource', ret='product')[0]
			if product != 'Plex Media Server': continue
			accessToken = dom_parser.parseDOM(resource, 'resource', ret='accessToken')[0]
			if not accessToken: continue
			sourceTitle = dom_parser.parseDOM(resource, 'resource', ret='name')[0]
			connections = re.findall(r'(<connection\s.+?/>)', resource, flags=re.M | re.S)
			for connection in connections:
				share_url = dom_parser.parseDOM(connection, 'connection', ret='uri')[0]
				local = dom_parser.parseDOM(connection, 'connection', ret='local')[0]
				if '.plex.direct:' not in share_url or local == '1': continue
				if share_url:
					if not control.yesnoDialog('plexshare resource found: %s[CR]Add?' % sourceTitle): continue
					log_utils.log('plexshare sourceTitle = %s' % sourceTitle, __name__, level=log_utils.LOGDEBUG)
					log_utils.log('plexshare direct url = %s' % share_url, __name__, level=log_utils.LOGDEBUG)
					self.plex_insert(sourceTitle, accessToken, share_url)
					#control.setSetting('plexshare.sourceTitle', sourceTitle)
					#control.setSetting('plexshare.accessToken', accessToken)
					#control.setSetting('plexshare.url', share_url)
		if not share_url: control.okDialog(message='Failed to retrieve a plexshare resource')

	def revoke(self):
		url = "https://plex.tv/devices/%s.xml?X-Plex-Token=%s" % (self.device_id, self.token)
		result = requests.delete(url)
		if result.status_code != 200: self.plex_error(result.status_code)
		control.setSetting('plex.token', '')
		control.setSetting('plex.client_id', '')
		control.setSetting('plex.device_id', '')
		#control.setSetting('plexshare.sourceTitle', '')
		#control.setSetting('plexshare.accessToken', '')
		#control.setSetting('plexshare.url', '')
		control.notification(title='Plex', message='Plexshare device successfully revoked')
		if self.clearPlex() == True:
			from cocoscrapers.modules import log_utils
			log_utils.log('CocoScrapers Cleared Plex Database.', 1)
		else:
			from cocoscrapers.modules import log_utils
			log_utils.log('CocoScrapers Clear Plex Database Failed.', 1)

	def clearPlex(self):
		try:
			dbcon = self.get_connection_plexshares()
			dbcur = dbcon.cursor()
			dbcur.execute('''DROP TABLE IF EXISTS plexshares''')
			dbcur.execute('''VACUUM''')
			dbcur.connection.commit()
			cleared = True
		except:
			from cocoscrapers.modules import log_utils
			log_utils.error()
			cleared = False
		finally:
			dbcur.close() ; dbcon.close()
		return cleared

	def get_connection_plexshares(self):
		if not existsPath(dataPath): makeFile(dataPath)
		conn = db.connect(plexSharesFile)
		return conn

	def plex_get_all(self):
		try:
			dbcon = self.get_connection_plexshares()
			dbcur = dbcon.cursor()
			sqlite_select_query = """SELECT * FROM plexshares"""
			dbcur.execute(sqlite_select_query)
			records = dbcur.fetchall()
			return records
		except:
			from cocoscrapers.modules import log_utils
			log_utils.error()
			return None
		finally:
			dbcur.close() ; dbcon.close()

	def plex_insert(self, sourceTitle, token, url):
		try:
			dbcon = self.get_connection_plexshares()
			dbcur = dbcon.cursor()
			dbcur.execute('''CREATE TABLE IF NOT EXISTS plexshares (sourceTitle TEXT, accessToken TEXT, plexshareURL TEXT, UNIQUE(plexshareURL));''')
			dbcur.execute('''INSERT OR REPLACE INTO plexshares Values (?, ?, ?)''', (sourceTitle, token, url))
			dbcur.connection.commit()
		except:
			from cocoscrapers.modules import log_utils
			log_utils.error()
		finally:
			dbcur.close() ; dbcon.close()

	def see_active_shares(self):
		plexs = self.plex_get_all()
		active_shares = ''
		for plex in plexs:
			active_shares = active_shares + str(plex[0]) +'[CR]'
		if active_shares == '':
			active_shares = 'None'
		control.okDialog('Active PlexShares', active_shares)