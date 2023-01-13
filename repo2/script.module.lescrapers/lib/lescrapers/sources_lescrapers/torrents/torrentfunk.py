# -*- coding: utf-8 -*-
# created by Venom for LEscrapers (updated 11-05-2021)
"""
	LEscrapers Project
"""

import re
try: #Py2
	from urlparse import parse_qs
	from urllib import urlencode, quote_plus
except ImportError: #Py3
	from urllib.parse import parse_qs, urlencode, quote_plus
from lescrapers.modules import client
from lescrapers.modules import source_utils
from lescrapers.modules import workers


class source:
	def __init__(self):
		self.priority = 8
		self.language = ['en']
		self.domains = ['torrentfunk.com', 'torrentfunk2.com']
		self.base_link = 'https://www.torrentfunk.com'
		self.search_link = '/all/torrents/%s.html?v=&smi=&sma=&i=100&sort=size&o=desc'
		self.min_seeders = 0
		self.pack_capable = True

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
		self.sources = []
		if not url: return self.sources
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
			url = '%s%s' % (self.base_link, self.search_link % quote_plus(query))
			# log_utils.log('url = %s' % url)
			r = client.request(url, timeout='5')
			if not r: return self.sources
			r = client.parseDOM(r, 'table', attrs={'class': 'tmain'})[0]

			links = re.findall(r'<a\s*href\s*=\s*["\'](/torrent/.+?)["\']>(.+?)</a>', r, re.DOTALL | re.I)
			threads = []
			for link in links:
				threads.append(workers.Thread(self.get_sources, link))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.sources
		except:
			source_utils.scraper_error('TORRENTFUNK')
			return self.sources

	def get_sources(self, link):
		try:
			try: url = link[0].encode('ascii', errors='ignore').decode('ascii', errors='ignore').replace('&nbsp;', ' ')
			except: url = link[0].replace('&nbsp;', ' ')
			if '/torrent/' not in url: return

			try: name = link[1].encode('ascii', errors='ignore').decode('ascii', errors='ignore').replace('&nbsp;', '.')
			except: name = link[1].replace('&nbsp;', '.')
			if '<span' in name: name = name.split('<span')[0].rstrip(' [')
			name = source_utils.clean_name(name)
			if not source_utils.check_title(self.title, self.aliases, name, self.hdlr, self.year): return
			name_info = source_utils.info_from_name(name, self.title, self.year, self.hdlr, self.episode_title)
			if source_utils.remove_lang(name_info): return

			if not self.episode_title: #filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
				ep_strings = [r'[.-]s\d{2}e\d{2}([.-]?)', r'[.-]s\d{2}([.-]?)', r'[.-]season[.-]?\d{1,2}[.-]?']
				if any(re.search(item, name.lower()) for item in ep_strings): return

			if not url.startswith('http'): link = '%s%s' % (self.base_link, url)
			link = client.request(link, timeout='5')
			if link is None: 	return
			hash = re.search(r'Infohash.*?>(?!<)(.+?)</', link, re.I).group(1)
			url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name)
			if url in str(self.sources): return
			try:
				seeders = int(re.search(r'Swarm.*?>(?!<)([0-9]+)</', link, re.I).group(1).replace(',', ''))
				if self.min_seeders > seeders: return
			except: seeders = 0

			quality, info = source_utils.get_release_quality(name_info, url)
			try:
				size = re.search(r'<b>Size:</b>.*?((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', link).group(1)
				dsize, isize = source_utils._size(size)
				info.insert(0, isize)
			except: dsize = 0
			info = ' | '.join(info)

			self.sources.append({'provider': 'torrentfunk', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info,
												'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
		except:
			source_utils.scraper_error('TORRENTFUNK')

	def sources_packs(self, url, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
		self.sources = []
		self.items = []
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
						self.search_link % quote_plus(query + ' S%s' % self.season_xx),
						self.search_link % quote_plus(query + ' Season %s' % self.season_x)]
			if search_series:
				queries = [
						self.search_link % quote_plus(query + ' Season'),
						self.search_link % quote_plus(query + ' Complete')]
			threads = []
			for url in queries:
				link = '%s%s' % (self.base_link, url)
				threads.append(workers.Thread(self.get_pack_items, link))
			[i.start() for i in threads]
			[i.join() for i in threads]

			threads2 = []
			for i in self.items:
				threads2.append(workers.Thread(self.get_pack_sources, i))
			[i.start() for i in threads2]
			[i.join() for i in threads2]
			return self.sources
		except:
			source_utils.scraper_error('TORRENTFUNK')
			return self.sources

	def get_pack_items(self, url):
		# log_utils.log('url = %s' % url)
		try:
			r = client.request(url, timeout='5')
			if not r: return
			r = client.parseDOM(r, 'table', attrs={'class': 'tmain'})[0]
			links = re.findall(r'<a\s*href\s*=\s*["\'](/torrent/.+?)["\']>(.+?)</a>', r, re.DOTALL | re.I)
		except:
			source_utils.scraper_error('TORRENTFUNK')
			return
		for link in links:
			try:
				try: url = link[0].encode('ascii', errors='ignore').decode('ascii', errors='ignore').replace('&nbsp;', ' ')
				except: url = link[0].replace('&nbsp;', ' ')
				if '/torrent/' not in url: continue

				try: name = link[1].encode('ascii', errors='ignore').decode('ascii', errors='ignore').replace('&nbsp;', '.')
				except: name = link[1].replace('&nbsp;', '.')
				if '<span' in name: name = name.split('<span')[0].rstrip(' [')
				name = source_utils.clean_name(name)

				if not self.search_series:
					if not self.bypass_filter:
						if not source_utils.filter_season_pack(self.title, self.aliases, self.year, self.season_x, name): continue
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

				if not url.startswith('http'): url = '%s%s' % (self.base_link, url)
				if self.search_series: self.items.append((name, name_info, url, package, last_season))
				else: self.items.append((name, name_info, url, package))
			except:
				source_utils.scraper_error('TORRENTFUNK')

	def get_pack_sources(self, items):
		try:
			link = client.request(items[2], timeout='5')
			if link is None: 	return
			hash = re.search(r'Infohash.*?>(?!<)(.+?)</', link, re.I).group(1)

			url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, items[0])
			if url in str(self.sources): return
			try:
				seeders = int(re.search(r'Swarm.*?>(?!<)([0-9]+)</', link, re.I).group(1).replace(',', ''))
				if self.min_seeders > seeders: return
			except: seeders = 0

			quality, info = source_utils.get_release_quality(items[1], url)
			try:
				size = re.search(r'<b>Size:</b>.*?((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', link).group(1)
				dsize, isize = source_utils._size(size)
				info.insert(0, isize)
			except: dsize = 0
			info = ' | '.join(info)

			item = {'provider': 'torrentfunk', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': items[0], 'name_info': items[1], 'quality': quality,
						'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'package': items[3]}
			if self.search_series: item.update({'last_season': items[4]})
			self.sources.append(item)
		except:
			source_utils.scraper_error('TORRENTFUNK')

	def resolve(self, url):
		return url