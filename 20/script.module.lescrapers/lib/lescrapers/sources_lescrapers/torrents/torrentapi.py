# -*- coding: utf-8 -*-
# modified by Venom for LEscrapers (updated 7-03-2021)
"""
	LEscrapers Project
"""

from json import loads as jsloads
import re
from time import sleep
try: #Py2
	from urlparse import parse_qs
	from urllib import urlencode, quote_plus, unquote_plus
except ImportError: #Py3
	from urllib.parse import parse_qs, urlencode, quote_plus, unquote_plus
from lescrapers.modules import cache
from lescrapers.modules import cfscrape
from lescrapers.modules import source_utils
from lescrapers.modules import workers


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.base_link = 'https://torrentapi.org' # just to satisfy scraper_test
		self.tvsearch = 'https://torrentapi.org/pubapi_v2.php?app_id=Torapi&token={0}&mode=search&search_string={1}&ranked=0&limit=100&format=json_extended' # string query
		self.tvshowsearch = 'https://torrentapi.org/pubapi_v2.php?app_id=Torapi&token={0}&mode=search&search_imdb={1}&search_string={2}&ranked=0&limit=100&format=json_extended' # imdb_id + string query
		self.msearch = 'https://torrentapi.org/pubapi_v2.php?app_id=Torapi&token={0}&mode=search&search_imdb={1}&ranked=0&limit=100&format=json_extended'
		self.token = 'https://torrentapi.org/pubapi_v2.php?app_id=Torapi&get_token=get_token'
		self.min_seeders = 0
		self.pack_capable = True

	def _get_token(self):
		try:
			token = self.scraper.get(self.token).content
			if not token: return '3qk6aj27ws'
			token = jsloads(token)["token"]
			return token
		except:
			source_utils.scraper_error('TORRENTAPI')

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
			self.scraper = cfscrape.create_scraper()
			self.key = cache.get(self._get_token, 0.2) # 800 secs token is valid for
			data = parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')
			aliases = data['aliases']
			episode_title = data['title'] if 'tvshowtitle' in data else None
			year = data['year']
			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else year

			query = '%s %s' % (title, hdlr)
			query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', query)
			if 'tvshowtitle' in data:
				search_link = self.tvshowsearch.format(self.key, data['imdb'], hdlr)
			else:
				search_link = self.msearch.format(self.key, data['imdb'])
			sleep(2.1)
			rjson = self.scraper.get(search_link).content
			if not rjson or 'torrent_results' not in str(rjson): return sources
			files = jsloads(rjson)['torrent_results']
		except:
			source_utils.scraper_error('TORRENTAPI')
			return sources
		for file in files:
			try:
				url = file["download"].split('&tr')[0]
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1)
				name = source_utils.clean_name(unquote_plus(file["title"]))

				if not source_utils.check_title(title, aliases, name, hdlr, year): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)
				if source_utils.remove_lang(name_info): continue

				if not episode_title: #filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
					ep_strings = [r'[.-]s\d{2}e\d{2}([.-]?)', r'[.-]s\d{2}([.-]?)', r'[.-]season[.-]?\d{1,2}[.-]?']
					if any(re.search(item, name.lower()) for item in ep_strings): continue
				try:
					seeders = int(file["seeders"])
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					dsize, isize = source_utils.convert_size(file["size"], to='GB')
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				sources.append({'provider': 'torrentapi', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info,
											'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('TORRENTAPI')
		return sources

	def sources_packs(self, url, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
		sources = []
		if not url: return sources
		if search_series: # torrentapi does not have showPacks
			return sources
		try:
			self.scraper = cfscrape.create_scraper()
			self.key = cache.get(self._get_token, 0.2) # 800 secs token is valid for

			self.bypass_filter = bypass_filter
			data = parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			self.title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU')
			self.aliases = data['aliases']
			self.year = data['year']
			self.season_x = data['season']
			self.season_xx = self.season_x.zfill(2)
			search_link = self.tvshowsearch.format(self.key, data['imdb'], 'S%s' % self.season_xx)
			# log_utils.log('search_link = %s' % str(search_link))
			sleep(2.1)
			rjson = self.scraper.get(search_link).content
			if not rjson or 'torrent_results' not in str(rjson): return sources
			files = jsloads(rjson)['torrent_results']
		except:
			source_utils.scraper_error('TORRENTAPI')
			return sources
		for file in files:
			try:
				url = file["download"].split('&tr')[0]
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1)
				name = source_utils.clean_name(unquote_plus(file["title"]))

				if not self.bypass_filter:
					if not source_utils.filter_season_pack(self.title, self.aliases, self.year, self.season_x, name):
						continue
				package = 'season'

				name_info = source_utils.info_from_name(name, self.title, self.year, season=self.season_x, pack=package)
				if source_utils.remove_lang(name_info): continue
				try:
					seeders = int(file["seeders"])
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					dsize, isize = source_utils.convert_size(file["size"], to='GB')
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				sources.append({'provider': 'torrentapi', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
										'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'package': package})
			except:
				source_utils.scraper_error('TORRENTAPI')
		return sources

	def resolve(self, url):
		return url