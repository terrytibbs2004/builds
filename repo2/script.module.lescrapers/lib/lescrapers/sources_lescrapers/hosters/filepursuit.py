# -*- coding: UTF-8 -*-
# (updated 9-20-2021)
'''
	LEscrapers Project
'''

from json import loads as jsloads
import re
import requests
try: #Py2
	from urlparse import parse_qs
	from urllib import urlencode, quote_plus
except ImportError: #Py3
	from urllib.parse import parse_qs, urlencode, quote_plus
from lescrapers.modules.control import setting as getSetting
from lescrapers.modules import client
from lescrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 23
		self.language = ['en']
		self.base_link = 'https://filepursuit.p.rapidapi.com' # 'https://rapidapi.com/azharxes/api/filepursuit' to obtain key
		self.search_link = '/?type=video&q=%s'

	def movie(self, imdb, title, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('FILEPURSUIT')
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('FILEPURSUIT')
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
			source_utils.scraper_error('FILEPURSUIT')
			return

	def sources(self, url, hostDict):
		sources = []
		if not url: return sources
		try:
			api_key = getSetting('filepursuit.api')
			if api_key == '': return sources
			headers = {"x-rapidapi-host": "filepursuit.p.rapidapi.com", "x-rapidapi-key": api_key}

			data = parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')
			aliases = data['aliases']
			episode_title = data['title'] if 'tvshowtitle' in data else None
			year = data['year']
			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else year

			query = '%s %s' % (title, hdlr)
			query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)
			url = '%s%s' % (self.base_link, self.search_link % quote_plus(query))
			# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)

			r = client.request(url, headers=headers)
			if not r: return sources
			r = jsloads(r)
			if 'not_found' in r['status']: return sources
			results = r['files_found']
		except:
			source_utils.scraper_error('FILEPURSUIT')
			return sources
		for item in results:
			try:
				url = item['file_link']
				try: size = int(item['file_size_bytes'])
				except: size = 0
				try: name = item['file_name']
				except: name = item['file_link'].split('/')[-1]
				name = source_utils.clean_name(name)

				if not source_utils.check_title(title, aliases, name, hdlr, year): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)
				if source_utils.remove_lang(name_info): continue

				# link_header = client.request(url, output='headers', timeout='5') # to slow to check validity of links
				# if not any(value in str(link_header) for value in ['stream', 'video/mkv']): continue

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					dsize, isize = source_utils.convert_size(size, to='GB')
					if isize: info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				sources.append({'provider': 'filepursuit', 'source': 'direct', 'quality': quality, 'name': name, 'name_info': name_info, 'language': "en",
							'url': url, 'info': info, 'direct': True, 'debridonly': False, 'size': dsize})
			except:
				source_utils.scraper_error('FILEPURSUIT')
		return sources

	def resolve(self, url):
		return url