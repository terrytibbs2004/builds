# -*- coding: UTF-8 -*-
# modified by Venom for LEscrapers  (updated 2-26-2021)
'''
	LEscrapers Project
'''

import re
import time
try: #Py2
	from urlparse import parse_qs, urljoin
	from urllib import urlencode, quote_plus
except: #Py3
	from urllib.parse import parse_qs, urljoin, urlencode, quote_plus
from lescrapers.modules import cfscrape
from lescrapers.modules import cleantitle
from lescrapers.modules import client
from lescrapers.modules import dom_parser  # switch to client.parseDOM() to rid import
from lescrapers.modules import py_tools
from lescrapers.modules import source_utils
from lescrapers.modules import workers


class source:
	def __init__(self):
		self.priority = 24
		self.language = ['en']
		self.domains = ['rmz.cr', 'rapidmoviez.site']
		self.base_link = 'http://rmz.cr/'
		self.search_link = 'search/%s'
		# self.base_link = 'http://rapidmoviez.cr/' # cloudflare IUAM challenge failure
		self.scraper = cfscrape.create_scraper()
		self.headers = {'User-Agent': client.agent()}

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

	def search(self, title, year):
		try:
			url = urljoin(self.base_link, self.search_link % (quote_plus(title)))
			# r = self.scraper.get(url, headers=self.headers).content
			r = py_tools.ensure_str(self.scraper.get(url, headers=self.headers).content, errors='replace')
				# switch to client.parseDOM() to rid import
			if not r: return None
			r = dom_parser.parse_dom(r, 'div', {'class': 'list_items'})[0]
			r = dom_parser.parse_dom(r.content, 'li')
			r = [(dom_parser.parse_dom(i, 'a', {'class': 'title'})) for i in r]
			r = [(i[0].attrs['href'], i[0].content) for i in r]
			r = [(urljoin(self.base_link, i[0])) for i in r if cleantitle.get(title) in cleantitle.get(i[1]) and year in i[1]]
			if r: return r[0]
			else: return None
		except:
			return None

	def sources(self, url, hostDict):
		self.sources = []
		if not url: return self.sources
		try:
			self.hostDict = hostDict
			data = parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			self.title = self.title.replace('&', 'and').replace('Special Victims Unit', 'SVU')
			self.aliases = data['aliases']
			self.episode_title = data['title'] if 'tvshowtitle' in data else None
			self.year = data['year']
			self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else self.year
			imdb = data['imdb']

			url = self.search(self.title, self.year)
			# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
			if not url: return self.sources

			# result = self.scraper.get(url, headers=self.headers).content
			result = py_tools.ensure_str(self.scraper.get(url, headers=self.headers).content, errors='replace')
			if not result: return self.sources
			r_pack = None
			if 'tvshowtitle' in data:
				r = dom_parser.parse_dom(result, 'ul', {'id': 'episodes'})
				# r_pack = dom_parser.parse_dom(result, 'ul', {'id': 'packs'}) # Rapidmoviez has pack files, needs more work
			else:
				r = dom_parser.parse_dom(result, 'ul', {'id': 'releases'})

			if not r and not r_pack: return self.sources
			if r:
				r = dom_parser.parse_dom(r[0].content, 'a', req=['href'])
				r = [(i.content, urljoin(self.base_link, i.attrs['href'])) for i in r if i and i.content != 'Watch']
				r = [(i[0], i[1]) for i in r if self.hdlr in i[0].upper()]

			# if r_pack:
				# r_pack = dom_parser.parse_dom(r_pack[0].content, 'a', req=['href'])
				# r_pack = [(i.content, urljoin(self.base_link, i.attrs['href'])) for i in r_pack if i and i.content != 'Watch']
				# r += [(i[0], i[1]) for i in r_pack if 'S%02d' % int(data['season']) in i[0].upper()]
				# r += [(i[0], i[1]) for i in r_pack if 'SEASON %02d' % int(data['season']) in i[0].upper()]

			# log_utils.log('r = %s' % r, log_utils.LOGDEBUG)
			threads = []
			for i in r:
				threads.append(workers.Thread(self.get_sources, i[0], i[1]))
			[i.start() for i in threads]
			alive = [x for x in threads if x.is_alive() is True]
			while alive:
				alive = [x for x in threads if x.is_alive() is True]
				time.sleep(0.1)
			return self.sources
		except:
			source_utils.scraper_error('RAPIDMOVIEZ')
			return self.sources

	def get_sources(self, name, url):
		try:
			# r = self.scraper.get(url, headers=self.headers).content
			r = py_tools.ensure_str(self.scraper.get(url, headers=self.headers).content, errors='replace')
			name = client.replaceHTMLCodes(name)
			if name.startswith('['): name = name.split(']')[1]
			name = name.strip().replace(' ', '.')
			name_info = source_utils.info_from_name(name, self.title, self.year, self.hdlr, self.episode_title)
			if source_utils.remove_lang(name_info): return self.sources

			l = dom_parser.parse_dom(r, 'pre', {'class': 'links'})
			if l == []: return
			s = ''
			for i in l:
				s += i.content

			urls = re.findall(r'''((?:http|ftp|https)://[\w_-]+(?:(?:\.[\w_-]+)+)[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])''', i.content, flags=re.M | re.S)
			urls = [i for i in urls if not i.endswith(('.rar', '.zip', '.iso', '.idx', '.sub', '.srt'))]
			for link in urls:
				url = py_tools.ensure_text(client.replaceHTMLCodes(str(link)), errors='replace')
				if url in str(self.sources): continue

				valid, host = source_utils.is_host_valid(url, self.hostDict)
				if not valid: continue

				quality, info = source_utils.get_release_quality(name, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', name).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except:
					dsize = 0
				info = ' | '.join(info)

				self.sources.append({'provider': 'rapidmoviez', 'source': host, 'name': name, 'name_info': name_info, 'quality': quality, 'language': 'en', 'url': url,
													'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
		except:
			source_utils.scraper_error('RAPIDMOVIEZ')

	def resolve(self, url):
		return url