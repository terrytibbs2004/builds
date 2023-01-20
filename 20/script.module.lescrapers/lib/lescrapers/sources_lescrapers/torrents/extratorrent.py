# -*- coding: utf-8 -*-
# created by Venom for LEscrapers (added cfscrape 4-20-2020)(updated 11-05-2021)
"""
	LEscrapers Project
"""

import re
try: #Py2
	from urlparse import parse_qs
	from urllib import urlencode, quote_plus, unquote_plus
except ImportError: #Py3
	from urllib.parse import parse_qs, urlencode, quote_plus, unquote_plus
from lescrapers.modules import cfscrape
from lescrapers.modules import client
from lescrapers.modules import py_tools
from lescrapers.modules import source_utils
from lescrapers.modules import workers


class source:
	def __init__(self):
		self.priority = 4
		self.language = ['en']
		self.domains = ['extratorrent.proxyninja.org']
		# self.base_link = 'https://extratorrent.si' # dead
		self.base_link = 'https://extratorrent.proxyninja.org'
		self.msearch_link = '/search/?new=1&search=%s&s_cat=1'
		self.tvsearch_link = '/search/?new=1&search=%s&s_cat=2'
		# new proxy site does not have page issue ".si" use to have and pack file category no longer exists
		# self.packsearch_link = '/search/?page=2&new=1&search=%s&s_cat=2' # page1 appears broken, scrape page2 only for packs
		self.min_seeders = 1
		self.pack_capable = True

	def movie(self, imdb, title, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('EXTRATORRENT')
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
			source_utils.scraper_error('EXTRATORRENT')
			return

	def sources(self, url, hostDict):
		self.sources = []
		if not url: return self.sources
		try:
			self.scraper = cfscrape.create_scraper()
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
			urls = []
			url = self.tvsearch_link % quote_plus(query) if 'tvshowtitle' in data else self.msearch_link % quote_plus(query)
			url = '%s%s' % (self.base_link, url)
			urls.append(url)
			urls.append('%s%s' % (url, '&page=2')) # next page seems to be working once again
			# urls.append('%s%s' % (url, '&page=3'))
			# log_utils.log('urls = %s' % urls)

			threads = []
			for url in urls:
				threads.append(workers.Thread(self.get_sources, url))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.sources
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return self.sources

	def get_sources(self, url):
		try:
			r = py_tools.ensure_str(self.scraper.get(url).content, errors='replace')
			if not r: return
			rows = client.parseDOM(r, 'tr', attrs={'class': 'tlr'})
			rows += client.parseDOM(r, 'tr', attrs={'class': 'tlz'})
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return

		for row in rows:
			try:
				url = re.search(r'href\s*=\s*["\'](magnet:[^"\']+)["\']', row, re.I).group(1)
				url = unquote_plus(url).replace('&amp;', '&').replace(' ', '.').split('&tr')[0]
				url = source_utils.strip_non_ascii_and_unprintable(url)
				if url in str(self.sources): continue
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1)

				name = url.split('&dn=')[1]
				name = source_utils.clean_name(name)
				if not source_utils.check_title(self.title, self.aliases, name, self.hdlr, self.year): continue
				name_info = source_utils.info_from_name(name, self.title, self.year, self.hdlr, self.episode_title)
				if source_utils.remove_lang(name_info): continue

				if not self.episode_title: #filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
					ep_strings = [r'(?:\.|\-)s\d{2}e\d{2}(?:\.|\-|$)', r'(?:\.|\-)s\d{2}(?:\.|\-|$)', r'(?:\.|\-)season(?:\.|\-)\d{1,2}(?:\.|\-|$)']
					if any(re.search(item, name.lower()) for item in ep_strings): continue
				try:
					seeders = int(client.parseDOM(row, 'td', attrs={'class': 'sn'})[0].replace(',', ''))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', row).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				self.sources.append({'provider': 'extratorrent', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info,
												'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('EXTRATORRENT')

	def sources_packs(self, url, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
		self.sources = []
		if not url: return self.sources
		try:
			self.scraper = cfscrape.create_scraper()
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
						self.tvsearch_link % quote_plus(query + ' S%s' % self.season_xx),
						self.tvsearch_link % quote_plus(query + ' Season %s' % self.season_x)]
			if self.search_series:
				queries = [
						self.tvsearch_link % quote_plus(query + ' Season'),
						self.tvsearch_link % quote_plus(query + ' Complete')]

			threads = []
			for url in queries:
				link = '%s%s' % (self.base_link, url)
				threads.append(workers.Thread(self.get_sources_packs, link))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.sources
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return self.sources

	def get_sources_packs(self, link):
		try:
			# log_utils.log('link = %s' % link)
			r = py_tools.ensure_str(self.scraper.get(link).content, errors='replace')
			if not r: return
			posts = client.parseDOM(r, 'tr', attrs={'class': 'tlr'})
			posts += client.parseDOM(r, 'tr', attrs={'class': 'tlz'})
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return
		for post in posts:
			try:
				post = re.sub(r'\n', '', post)
				post = re.sub(r'\t', '', post)
				url = re.search(r'href\s*=\s*["\'](magnet:[^"\']+)["\']', post, re.I).group(1)
				url = unquote_plus(url).replace('&amp;', '&').replace(' ', '.').split('&tr')[0]
				url = source_utils.strip_non_ascii_and_unprintable(url)
				if url in str(self.sources): continue
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1)
				name = url.split('&dn=')[1]
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
					seeders = int(client.parseDOM(post, 'td', attrs={'class': 'sn'})[0].replace(',', ''))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', post).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				item = {'provider': 'extratorrent', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
							'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'package': package}
				if self.search_series: item.update({'last_season': last_season})
				self.sources.append(item)
			except:
				source_utils.scraper_error('EXTRATORRENT')

	def resolve(self, url):
		return url