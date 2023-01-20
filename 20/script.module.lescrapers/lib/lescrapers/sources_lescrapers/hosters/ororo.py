# -*- coding: UTF-8 -*-
# (updated 9-20-2021)
'''
	LEscrapers Project
'''

from base64 import b64encode
from json import loads as jsloads
import re
try: #Py2
	from urlparse import urljoin
except ImportError: #Py3
	from urllib.parse import urljoin
from lescrapers.modules import cache
from lescrapers.modules import client
from lescrapers.modules.control import setting as getSetting
from lescrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 25
		self.language = ['en']
		self.domains = ['ororo.tv']
		self.base_link = 'https://ororo.tv'
		self.moviesearch_link = '/api/v2/movies'
		self.tvsearch_link = '/api/v2/shows'
		self.movie_link = '/api/v2/movies/%s'
		self.show_link = '/api/v2/shows/%s'
		self.episode_link = '/api/v2/episodes/%s'
		self.user = getSetting('ororo.user')
		self.password = getSetting('ororo.pass')
		self.headers = {
			'Authorization': self._get_auth(),
			'User-Agent': 'Placenta for Kodi'}

	def _get_auth(self):
		try: # Python 2
			user_info = '%s:%s' % (self.user, self.password)
			auth = 'Basic ' + b64encode(user_info)
		except: # Python 3
			user_info = '%s:%s' % (self.user, self.password)
			user_info = user_info.encode('utf-8')
			auth = 'Basic ' + b64encode(user_info).decode('utf-8')
		return auth

	def movie(self, imdb, title, aliases, year): # seems Ororo does not provide Movies
		try:
			if (self.user == '' or self.password == ''): return
			url = cache.get(self.ororo_moviecache, 60, self.user)
			if not url: return
			url = [i[0] for i in url if imdb == i[1]]
			if not url: return
			url = self.movie_link % url[0]
			return url
		except:
			source_utils.scraper_error('ORORO')
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try:
			if (self.user == '' or self.password == ''): return
			url = cache.get(self.ororo_tvcache, 120, self.user)
			if not url: return
			url = [i[0] for i in url if imdb == i[1]]
			if not url: return
			url = self.show_link % url[0]
			return url
		except:
			source_utils.scraper_error('ORORO')
			return

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if (self.user == '' or self.password == ''): return
			if not url: return
			url = urljoin(self.base_link, url)
			r = client.request(url, headers=self.headers)
			r = jsloads(r)['episodes']
			r = [(str(i['id']), str(i['season']), str(i['number']), str(i['airdate'])) for i in r]
			url = [i for i in r if season == i[1] and episode == i[2]]
			url += [i for i in r if premiered == i[3]]
			if not url: return
			url= self.episode_link % url[0][0]
			return url
		except:
			source_utils.scraper_error('ORORO')
			return

	def ororo_moviecache(self, user):
		try:
			url = urljoin(self.base_link, self.moviesearch_link)
			r = client.request(url, headers=self.headers)
			r = jsloads(r)['movies']
			r = [(str(i['id']), str(i['imdb_id'])) for i in r]
			r = [(i[0], 'tt' + re.sub(r'[^0-9]', '', i[1])) for i in r]
			return r
		except:
			source_utils.scraper_error('ORORO')
			return

	def ororo_tvcache(self, user):
		try:
			url = urljoin(self.base_link, self.tvsearch_link)
			r = client.request(url, headers=self.headers)
			r = jsloads(r)['shows']
			r = [(str(i['id']), str(i['imdb_id'])) for i in r]
			r = [(i[0], 'tt' + re.sub(r'[^0-9]', '', i[1])) for i in r]
			return r
		except:
			source_utils.scraper_error('ORORO')
			return

	def sources(self, url, hostDict):
		sources = []
		if not url: return sources
		try:
			if (self.user == '' or self.password == ''): return sources

			url = urljoin(self.base_link, url)
			url = client.request(url, headers=self.headers)
			if not url: return sources
			url = jsloads(url)['url']
			# log_utils.log('url = %s' % url, __name__)

			name = re.sub(r'(.*?)\/video/file/(.*?)/', '', url).split('.smil')[0].split('-')[0]
			quality, info = source_utils.get_release_quality(name)
			info = ' | '.join(info)

			sources.append({'provider': 'ororo', 'source': 'direct', 'name': name, 'quality': quality, 'language': 'en', 'url': url,
									'info': info, 'direct': True, 'debridonly': False, 'size': 0}) # Ororo does not return a file size
			return sources
		except:
			source_utils.scraper_error('ORORO')
			return sources

	def resolve(self, url):
		return url