# -*- coding: UTF-8 -*-
# (updated 9-20-2021)
'''
	LEscrapers Project
'''

from json import dumps as jsdumps, loads as jsloads
import requests
# import sys
try: #Py2
	from urlparse import parse_qs
	from urllib import urlencode
except ImportError: #Py3
	from urllib.parse import parse_qs, urlencode
from lescrapers.modules.control import setting as getSetting, setSetting
from lescrapers.modules import cleantitle
from lescrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 21
		self.language = ['en']
		self.domain = 'furk.net/'
		self.base_link = 'https://www.furk.net'
		self.search_link = "/api/plugins/metasearch?api_key=%s&q=%s&cached=yes" \
								"&match=%s&moderated=%s%s&sort=relevance&type=video&offset=0&limit=200"
		self.tfile_link = "/api/file/get?api_key=%s&t_files=1&id=%s"
		self.login_link = "/api/login/login?login=%s&pwd=%s"
		self.files = []

	def get_api(self):
		try:
			user_name = getSetting('furk.user_name')
			user_pass = getSetting('furk.user_pass')
			api_key = getSetting('furk.api')
			if api_key == '':
				if user_name == '' or user_pass == '': return
				s = requests.Session()
				link = (self.base_link + self.login_link % (user_name, user_pass))
				p = s.post(link)
				p = jsloads(p.text)
				if p['status'] == 'ok':
					api_key = p['api_key']
					setSetting('furk.api', api_key)
				else: pass
			return api_key
		except:
			source_utils.scraper_error('FURK')

	def movie(self, imdb, title, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			return

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url: return
			url = parse_qs(url)
			url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
			url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
			url = urlencode(url)
			return url
		except:
			return

	def sources(self, url, hostDict):
		sources = []
		if not url: return sources
		api_key = self.get_api()
		if not api_key: return sources
		try:
			data = parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')
			aliases = data['aliases'] # not used atm
			episode_title = data['title'] if 'tvshowtitle' in data else None
			year = data['year']
			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else year

			content_type = 'episode' if 'tvshowtitle' in data else 'movie'
			match = 'extended'
			moderated = 'no' if content_type == 'episode' else 'yes'
			search_in = ''

			if content_type == 'movie':
				years = '%s+|+%s+|+%s' % (str(int(year) - 1), year, str(int(year) + 1))
				query = '@name+%s+%s' % (title, years)

			elif content_type == 'episode':
				season = int(data['season'])
				episode = int(data['episode'])
				seasEpList = self._seas_ep_query_list(season, episode)
				query = '@name+%s+@files+%s+|+%s+|+%s+|+%s+|+%s' % (title, seasEpList[0], seasEpList[1], seasEpList[2], seasEpList[3], seasEpList[4])

			s = requests.Session()
			link = self.base_link + self.search_link % (api_key, query, match, moderated, search_in)

			p = s.get(link)
			p = jsloads(p.text)
			if p.get('status') != 'ok': return

			files = p.get('files')
			if not files: return sources
			for i in files:
				if i['is_ready'] == '1' and i['type'] == 'video':
					try:
						source = 'direct SINGLE'
						if int(i['files_num_video']) > 3:
							source = ' direct PACK (x%02d)' % int(i['files_num_video'])
						file_name = i['name']
						name = source_utils.clean_name(file_name)
						name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)

						file_id = i['id']
						file_dl = i['url_dl']

						if content_type == 'episode':
							url = jsdumps({'content': 'episode', 'file_id': file_id, 'season': season, 'episode': episode})
						else:
							url = jsdumps({'content': 'movie', 'file_id': file_id, 'title': title, 'year': year})

						quality, info = source_utils.get_release_quality(name_info, file_dl)
						try:
							size = float(i['size'])
							if 'PACK' in source:
								size = float(size) / int(i['files_num_video'])
							dsize, isize = source_utils.convert_size(size, to='GB')
							if isize: info.insert(0, isize)
						except:
							source_utils.scraper_error('FURK')
							dsize = 0
						info = ' | '.join(info)

						sources.append({'provider': 'furk', 'source': source, 'name': name, 'name_info': name_info, 'quality': quality, 'language': "en", 'url': url,
													'info': info, 'direct': True, 'debridonly': False, 'size': dsize})
					except:
						source_utils.scraper_error('FURK')
				else:
					continue
			return sources
		except:
			source_utils.scraper_error('FURK')

	def resolve(self, url):
		try:
			api_key = self.get_api()
			if not api_key: return

			url = jsloads(url)
			file_id = url.get('file_id')
			self.content_type = 'movie' if url.get('content') == 'movie' else 'episode'
			if self.content_type == 'episode': self.filtering_list = self._seas_ep_resolve_list(url.get('season'), url.get('episode'))

			link = (self.base_link + self.tfile_link % (api_key, file_id))
			s = requests.Session()
			p = s.get(link)
			p = jsloads(p.text)
			if p['status'] != 'ok' or p['found_files'] != '1': return

			files = p['files'][0]
			files = files['t_files']
			for i in files:
				if 'video' not in i['ct']: pass
				else: self.files.append(i)
			url = self._manage_pack()
			return url
		except:
			source_utils.scraper_error('FURK')

	def _manage_pack(self):
		for i in self.files:
			if self.content_type == 'movie':
				if 'is_largest' in i: url = i['url_dl']
			else:
				name = cleantitle.get_simple(i['name'])
				if 'furk320' not in name.lower() and 'sample' not in name.lower():
					for x in self.filtering_list:
						if x in name.lower(): url = i['url_dl']
						else: pass
		return url

	def _seas_ep_query_list(self, season, episode):
		return ['s%02de%02d' % (season, episode),
				'%dx%02d' % (season, episode),
				'%02dx%02d' % (season, episode),
				'"season %d episode %d"' % (season, episode),
				'"season %02d episode %02d"' % (season, episode)]

	def _seas_ep_resolve_list(self, season, episode):
		return ['s%02de%02d' % (season, episode),
				'%dx%02d' % (season, episode),
				'%02dx%02d' % (season, episode),
				'season%depisode%d' % (season, episode),
				'season%02depisode%02d' % (season, episode)]