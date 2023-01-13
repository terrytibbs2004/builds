# -*- coding: utf-8 -*-
# (updated 05-19-2021)
'''
	Fenomscrapers Project
'''

import re
import requests
try: #Py2
	from urllib import unquote, quote_plus, unquote_plus
except ImportError: #Py3
	from urllib.parse import unquote, quote_plus, unquote_plus
from WolfPackScrapers.modules import control
from WolfPackScrapers.modules import source_utils

cloudflare_worker_url = control.setting('gdrive.cloudflare_url').strip()

def getResults(searchTerm):
	url = '{}/searchjson/{}'.format(cloudflare_worker_url, searchTerm)
	if not url.startswith("https://"): url = "https://" + url
	# log_utils.log('query url = %s' % url)
	results = requests.get(url).json()
	return results

def get_simple(title):
	title = title.lower()
	if "/" in title:
		title = title.split("/")[-1]
	title = unquote_plus(title)
	title = title.replace('&', 'and').replace("'", '').replace('.', ' ')
	title = re.sub(r'[^a-z0-9\s\.]+', '', title) # query keeps dashes if they exist in actual title. dash is removed in title check and links returned for comp
	while "  " in title:
		title = title.replace("  ", " ")
	title = title.strip()
	return title

def filteredResults(results, simpleQuery):
	filtered = []
	for result in results:
		if get_simple(result["link"]).startswith(simpleQuery):
			filtered.append(result)
	return filtered


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']

	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try:
			query = tvshowtitle.replace('&', 'and')
			query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', query)
			return query
		except:
			source_utils.scraper_error('GDRIVE')
			return

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			query = url + " S" + str(season).zfill(2) + "E" + str(episode).zfill(2)
			query = quote_plus(query)
			return query
		except:
			source_utils.scraper_error('GDRIVE')
			return

	def movie(self, imdb, title, aliases, year):
		try:
			title = title.replace('&', 'and')
			query = '%s %s' % (title, str(year))
			query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', query)
			query = quote_plus(query)
			return query
		except:
			source_utils.scraper_error('GDRIVE')
			return

	def sources(self, url, hostDict):
		sources = []
		if not url: return sources
		try:
			if cloudflare_worker_url == '': return sources
			results = getResults(url)
			if not results: return sources
			if control.setting('gdrive.title.chk') == 'true':
				simpleQuery = get_simple(url)
				results = filteredResults(results, simpleQuery)
		except:
			source_utils.scraper_error('GDRIVE')
			return sources
		for result in results:
			try:
				link = result["link"]
				name = unquote(link.rsplit("/")[-1])
				# name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title) # needs a decent rewrite to get this
				release_title = name.lower().replace('&', 'and').replace("'", "")
				release_title = re.sub(r'[^a-z0-9]+', '.', release_title)

				quality, info = source_utils.get_release_quality(release_title, link)
				try:
					size = str(result["size_gb"]) + ' GB'
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except:
					source_utils.scraper_error('GDRIVE')
					dsize = 0
				info = ' | '.join(info)

				sources.append({'provider': 'gdrive', 'source': 'Google Drive', 'quality': quality, 'name': name, 'language': 'en',
											'info': info, 'url': link, 'direct': True, 'debridonly': False, 'size': dsize})
			except:
				source_utils.scraper_error('GDRIVE')
		return sources

	def resolve(self, url):
		return url