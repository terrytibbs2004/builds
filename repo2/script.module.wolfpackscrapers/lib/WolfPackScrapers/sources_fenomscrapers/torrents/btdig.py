# -*- coding: utf-8 -*-
# created by Venom for Fenomscrapers (1-28-2021)
'''
	Fenomscrapers Project
'''

import re
try: #Py2
	from urlparse import parse_qs, urljoin
	from urllib import urlencode, quote_plus, unquote_plus
except ImportError: #Py3
	from urllib.parse import parse_qs, urljoin, urlencode, quote_plus, unquote_plus

from WolfPackScrapers.modules import cfscrape # client.request causes strange 429 error
from WolfPackScrapers.modules import client
from WolfPackScrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 3
		self.language = ['en']
		self.domains = ['www.digbt.org']
		self.base_link = 'https://www.btdig.com'
		self.search_link = '/search?q=%s'
		self.scraper = cfscrape.create_scraper()
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
			query = re.sub('[^A-Za-z0-9\s\.-]+', '', query)
			url = self.search_link % quote_plus(query)
			url = urljoin(self.base_link, url)
			# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
			r = self.scraper.get(url).content
			# r = client.request(url)
			if not r: return sources
			rows = client.parseDOM(r, "div", attrs={"class": "one_result"})
			if not rows: return sources
		except:
			source_utils.scraper_error('BTDIG')
			return sources

		for row in rows:
			try:
				url = re.findall(r'href\s*=\s*["\'](magnet:[^"\']+)["\']', row, re.DOTALL | re.I)[0]
				url = unquote_plus(url).replace('&amp;', '&').replace(' ', '.').split('&tr')[0]
				hash = re.compile(r'btih:(.*?)&', re.I).findall(url)[0]
				name = url.split('&dn=')[1]
				name = source_utils.clean_name(name)

				if not source_utils.check_title(title, aliases, name, hdlr, year): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)
				if source_utils.remove_lang(name_info): continue

				if not episode_title: #filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
					ep_strings = [r'(?:\.|\-)s\d{2}e\d{2}(?:\.|\-|$)', r'(?:\.|\-)s\d{2}(?:\.|\-|$)', r'(?:\.|\-)season(?:\.|\-)\d{1,2}(?:\.|\-|$)']
					if any(re.search(item, name.lower()) for item in ep_strings): continue

				try:
					seeders = 1 # seeders not available on "btdig", set to 1 to satisfy addon caching of torrent
					if self.min_seeders > seeders: return
				except: seeders = 0

				quality, info = source_utils.get_release_quality(url)
				try:
					size = client.parseDOM(row, "span", attrs={"class": "torrent_size"})[0]
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				sources.append({'provider': 'btdig', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info,
											'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('BTDIG')
		return sources


	def resolve(self, url):
		return url