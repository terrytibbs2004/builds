# -*- coding: utf-8 -*-
# (updated 11-04-2021)
'''
	LEscrapers Project
'''

import re
import requests
try: #Py2
	from urlparse import parse_qs
	from urllib import urlencode, unquote, quote_plus
except ImportError: #Py3
	from urllib.parse import parse_qs, urlencode, unquote, quote_plus
from lescrapers.modules.control import setting as getSetting
from lescrapers.modules import source_utils

cloudflare_worker_url = getSetting('gdrive.cloudflare_url').strip()


def getResults(searchTerm):
	url = '{}/searchjson/{}'.format(cloudflare_worker_url, searchTerm)
	if not url.startswith("https://"): url = "https://" + url
	# log_utils.log('query url = %s' % url)
	results = requests.get(url).json()
	return results

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.title_chk = (getSetting('gdrive.title.chk') == 'true')

	def movie(self, imdb, title, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('GDRIVE')
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('GDRIVE')
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
			source_utils.scraper_error('GDRIVE')
			return

	def sources(self, url, hostDict):
		sources = []
		if not url: return sources
		try:
			data = parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')
			aliases = data['aliases']
			episode_title = data['title'] if 'tvshowtitle' in data else None
			year = data['year']
			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else year

			query = '%s %s' % (title, hdlr)
			query = quote_plus(re.sub(r'[^A-Za-z0-9\s\.-]+', '', query))
			if cloudflare_worker_url == '': return sources
			results = getResults(query)
			if not results: return sources
		except:
			source_utils.scraper_error('GDRIVE')
			return sources

		for result in results:
			try:
				link = result["link"]
				name = unquote(link.rsplit("/")[-1])
				if self.title_chk:
					if not source_utils.check_title(title, aliases, name, hdlr, year): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title) # needs a decent rewrite to get this

				quality, info = source_utils.get_release_quality(name_info, link)
				try:
					size = str(result["size_gb"]) + ' GB'
					dsize, isize = source_utils._size(size)
					if isize: info.insert(0, isize)
				except:
					source_utils.scraper_error('GDRIVE')
					dsize = 0
				info = ' | '.join(info)

				sources.append({'provider': 'gdrive', 'source': 'direct', 'name': name, 'name_info': name_info,
											'quality': quality, 'language': 'en', 'url': link, 'info': info,  'direct': True, 'debridonly': False, 'size': dsize})
			except:
				source_utils.scraper_error('GDRIVE')
		return sources

	def resolve(self, url):
		return url