# -*- coding: utf-8 -*-
# modified by Venom for LEscrapers (updated 11-05-2021)
'''
	LEscrapers Project
'''

import re
try: #Py2
	from urlparse import parse_qs
	from urllib import urlencode, quote_plus
except ImportError: #Py3
	from urllib.parse import parse_qs, urlencode, quote_plus
from lescrapers.modules import cfscrape
from lescrapers.modules import client
from lescrapers.modules import py_tools
from lescrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 21
		self.language = ['en']
		self.domains = ['scene-rls.com', 'scene-rls.net']
		self.base_link = 'http://scene-rls.net'
		self.search_link = '/?s=%s'

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
			scraper = cfscrape.create_scraper()
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
			url = self.search_link % quote_plus(query)
			url = '%s%s' % (self.base_link, url)
			# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
			# r = scraper.get(url).content
			r = py_tools.ensure_str(scraper.get(url).content, errors='replace')
			posts = client.parseDOM(r, 'div', attrs={'class': 'post'})
			if not posts: return sources
		except:
			source_utils.scraper_error('SCENERLS')
			return sources
		items = []
		for post in posts:
			try:
				content = client.parseDOM(post, "div", attrs={"class": "postContent"})
				size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', content[0]).group(0)
				u = client.parseDOM(content, "h2")
				u = client.parseDOM(u, 'a', ret='href')
				u = [(i.strip('/').split('/')[-1], i, size) for i in u]
				items += u
			except:
				source_utils.scraper_error('SCENERLS')
				return sources
		for item in items:
			try:
				name = item[0]
				name = client.replaceHTMLCodes(name)
				if not source_utils.check_title(title, aliases, name, hdlr, year): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)
				if source_utils.remove_lang(name_info): continue
				# check year for reboot/remake show issues if year is available-crap shoot
				# if 'tvshowtitle' in data:
					# if re.search(r'([1-3][0-9]{3})', name):
						# if not any(value in name for value in [year, str(int(year)+1), str(int(year)-1)]):
							# continue

				url = py_tools.ensure_text(client.replaceHTMLCodes(str(item[1])), errors='replace')
				if url in str(sources): continue

				valid, host = source_utils.is_host_valid(url, hostDict)
				if not valid: continue

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					dsize, isize = source_utils._size(item[2])
					info.insert(0, isize)
				except:
					dsize = 0
				info = ' | '.join(info)

				sources.append({'provider': 'scenerls', 'source': host, 'name': name, 'name_info': name_info, 'quality': quality, 'language': 'en', 'url': url,
											'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('SCENERLS')
		return sources

	def resolve(self, url):
		return url