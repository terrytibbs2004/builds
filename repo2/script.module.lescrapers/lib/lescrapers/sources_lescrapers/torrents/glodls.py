# -*- coding: utf-8 -*-
# modified by Venom for LEscrapers (updated 11-05-2021)
"""
	LEscrapers Project
"""

import re
try: #Py2
	from urlparse import parse_qs
	from urllib import urlencode, quote_plus, unquote_plus
except ImportError: #Py3
	from urllib.parse import parse_qs, urlencode, quote_plus, unquote_plus
from lescrapers.modules import client
from lescrapers.modules import source_utils
from lescrapers.modules import workers


class source:
	def __init__(self):
		self.priority = 3
		self.language = ['en']
		self.domains = ['glodls.to', 'gtdb.to']
		self.base_link = 'https://glodls.to/'
		self.moviesearch = 'search_results.php?search={0}&cat=1&incldead=0&inclexternal=0&lang=1&sort=size&order=desc'
		self.tvsearch = 'search_results.php?search={0}&cat=41&incldead=0&inclexternal=0&lang=1&sort=seeders&order=desc'
		self.tvsearch_pack = 'search_results.php?search={0}&cat=41,72&incldead=0&inclexternal=0&lang=1&sort=seeders&order=desc' # cat=72 timeout
# cat=1 is (Movies:all)
# cat=41 is (TV:all)
# cat=71 is (Videos:all)
# cat=72 is (Packs:all)
		self.min_seeders = 0 # to many items with no value but cached links
		self.pack_capable = False

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
		try:
			data = parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			self.title = self.title.replace('&', 'and').replace('Special Victims Unit', 'SVU')
			self.aliases = data['aliases']
			self.episode_title = data['title'] if 'tvshowtitle' in data else None
			self.year = data['year']
			self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else self.year

			query = '%s %s' % (self.title, self.hdlr)
			query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', query)
			if 'tvshowtitle' in data: url = self.tvsearch.format(quote_plus(query))
			else: url = self.moviesearch.format(quote_plus(query))
			url = '%s%s' % (self.base_link, url)
			# log_utils.log('url = %s' % url)
			headers = {'User-Agent': client.agent()}
			result = client.request(url, headers=headers, timeout='5')
			if not result: return sources
			rows = client.parseDOM(result, 'tr', attrs={'class': 't-row'})
			if not rows: return sources
			rows = [i for i in rows if 'racker:' not in i]
		except:
			source_utils.scraper_error('GLODLS')
			return sources
		for row in rows:
			try:
				ref = client.parseDOM(row, 'a', ret='href')
				url = [i for i in ref if 'magnet:' in i][0]
				url = unquote_plus(url).replace('&amp;', '&').replace(' ', '.').split('&tr')[0]
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1).lower()

				name = unquote_plus(client.parseDOM(row, 'a', ret='title')[0])
				name = source_utils.clean_name(name)
				if not source_utils.check_title(self.title, self.aliases, name, self.hdlr, self.year): continue
				name_info = source_utils.info_from_name(name, self.title, self.year, self.hdlr, self.episode_title)
				if source_utils.remove_lang(name_info): continue

				if not self.episode_title: #filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
					ep_strings = [r'[.-]s\d{2}e\d{2}([.-]?)', r'[.-]s\d{2}([.-]?)', r'[.-]season[.-]?\d{1,2}[.-]?']
					if any(re.search(item, name.lower()) for item in ep_strings): continue
				try:
					seeders = int(re.search(r'<td.*?<font\s*color\s*=\s*["\'].+?["\']><b>([0-9]+|[0-9]+,[0-9]+)</b>', row).group(1).replace(',', ''))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', row).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				sources.append({'provider': 'glodls', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info,
											'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('GLODLS')
		return sources

	def sources_packs(self, url, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
		self.sources = []
		if not url: return self.sources
		try:
			self.search_series = search_series
			self.total_seasons = total_seasons
			self.bypass_filter = bypass_filter

			data = parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			self.title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU')
			self.aliases = data['aliases']
			self.imdb = data['imdb']
			self.year = data['year']
			self.season_x = data['season']
			self.season_xx = self.season_x.zfill(2)

			query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', self.title)
			queries = [
						self.tvsearch_pack.format(quote_plus(query + ' S%s' % self.season_xx)),
						self.tvsearch_pack.format(quote_plus(query + ' Season %s' % self.season_x))]
			if search_series:
				queries = [
						self.tvsearch_pack.format(quote_plus(query + ' Season')),
						self.tvsearch_pack.format(quote_plus(query + ' Complete'))]

			threads = []
			for url in queries:
				link = '%s%s' % (self.base_link, url)
				threads.append(workers.Thread(self.get_sources_packs, link))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.sources
		except:
			source_utils.scraper_error('GLODLS')
			return self.sources

	def get_sources_packs(self, link):
		# log_utils.log('link = %s' % str(link))
		try:
			# headers = {'User-Agent': client.agent()}
			headers = {'User-Agent': client.randomagent()}
			result = client.request(link, headers=headers, timeout='5')
			if not result: return
			rows = client.parseDOM(result, 'tr', attrs={'class': 't-row'})
			if not rows: return
			rows = [i for i in rows if 'racker:' not in i]
		except:
			source_utils.scraper_error('GLODLS')
			return

		for row in rows:
			try:
				ref = client.parseDOM(row, 'a', ret='href')
				url = [i for i in ref if 'magnet:' in i][0]
				url = unquote_plus(url).replace('&amp;', '&').replace(' ', '.').split('&tr')[0]
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1).lower()

				name = unquote_plus(client.parseDOM(row, 'a', ret='title')[0])
				name = source_utils.clean_name(name)
				if not self.search_series:
					if not self.bypass_filter:
						if not source_utils.filter_season_pack(self.title, self.aliases, self.year, self.season_x, name):
							continue
					package = 'season'

				elif self.search_series:
					if not self.bypass_filter:
						valid, last_season = source_utils.filter_show_pack(self.title, self.aliases, self.imdb, self.year, self.season_x, name, self.total_seasons)
						if not valid: continue
					else:
						last_season = self.total_seasons
					package = 'show'

				name_info = source_utils.info_from_name(name, self.title, self.year, season=self.season_x, pack=package)
				if source_utils.remove_lang(name_info): continue
				try:
					seeders = int(re.search(r'<td.*?<font\s*color\s*=\s*["\'].+?["\']><b>([0-9]+|[0-9]+,[0-9]+)</b>', row).group(1).replace(',', ''))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', row).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				item = {'provider': 'glodls', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
							'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'package': package}
				if self.search_series: item.update({'last_season': last_season})
				self.sources.append(item)
			except:
				source_utils.scraper_error('GLODLS')

	def resolve(self, url):
		return url