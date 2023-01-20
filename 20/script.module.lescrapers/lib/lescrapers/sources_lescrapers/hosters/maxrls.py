# -*- coding: UTF-8 -*-
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
from lescrapers.modules import workers


class source:
	def __init__(self):
		self.priority = 21
		self.language = ['en']
		self.domains = ['max-rls.com']
		self.base_link = 'http://max-rls.com'
		self.search_link = '/?s=%s&submit=Find'

	def movie(self, imdb, title, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('MAXRLS')
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('MAXRLS')
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
			source_utils.scraper_error('MAXRLS')
			return

	def sources(self, url, hostDict):
		sources = []
		if not url: return sources
		try:
			scraper = cfscrape.create_scraper(delay=5)
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
			url = ('%s%s' % (self.base_link, self.search_link % quote_plus(query))).replace('%3A+', '+')
			# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
			# result = scraper.get(url).content
			result = py_tools.ensure_str(scraper.get(url).content, errors='replace')

			if not result or "Sorry, but you are looking for something that isn't here" in str(result):
				return sources
			posts = client.parseDOM(result, "div", attrs={"class": "post"})
			if not posts: return sources
		except:
			source_utils.scraper_error('MAXRLS')
			return sources
		for post in posts:
			try:
				post_title = client.parseDOM(post, "h2", attrs={"class": "postTitle"})
				post_title = client.parseDOM(post_title, 'a')[0]
				if not source_utils.check_title(title, aliases, post_title, hdlr, year): continue
				content = client.parseDOM(post, "div", attrs={"class": "postContent"})
				ltr = client.parseDOM(content, "p", attrs={"dir": "ltr"})
				if not ltr: continue

				for i in ltr:
					if '<strong>' not in i or 'imdb.com' in i: continue
					name = re.search(r'<strong>(.*?)<', i).group(1)
					name = re.sub(r'(<span.*?>)', '', name).replace('</span>', '')
					if title not in name: continue # IMDB and Links: can be in name so check for title match
					name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)
					if source_utils.remove_lang(name_info): continue

					links = client.parseDOM(i, "a", ret="href")
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', i).group(0)

					for link in links:
						url = link
						if url in str(sources): continue
						valid, host = source_utils.is_host_valid(url, hostDict)
						if not valid: continue

						quality, info = source_utils.get_release_quality(name_info, url)
						try:
							dsize, isize = source_utils._size(size)
							info.insert(0, isize)
						except:
							dsize = 0
						info = ' | '.join(info)

						sources.append({'provider': 'maxrls', 'source': host, 'name': name, 'name_info': name_info, 'quality': quality, 'language': 'en',
															'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('MAXRLS')
		return sources

	def resolve(self, url):
		return url