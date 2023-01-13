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
from lescrapers.modules import client
from lescrapers.modules import py_tools
from lescrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 29
		self.language = ['en']
		self.domains = ['300mbfilms.io', '300mbfilms.co']
		self.base_link = 'https://www.300mbfilms.io'
		self.search_link = '/?s=%s'

	def movie(self, imdb, title, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('300MBFILMS')
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('300MBFILMS')
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
			source_utils.scraper_error('300MBFILMS')
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
			query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)
			url = '%s%s' % (self.base_link, self.search_link % quote_plus(query))
			# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)
			r = client.request(url)
			if not r: return sources
			posts = client.parseDOM(r, 'h2')
			urls = []
			for item in posts:
				if not item.startswith('<a href'): continue
				try:
					name = client.parseDOM(item, "a")[0]
					if not source_utils.check_title(title, aliases, name, hdlr, year): continue
					name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)
					if source_utils.remove_lang(name_info): continue

					quality, info = source_utils.get_release_quality(name_info, item[0])
					try:
						size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', item).group(0)
						dsize, isize = source_utils._size(size)
						info.insert(0, isize)
					except:
						dsize = 0
					info = ' | '.join(info)

					item = client.parseDOM(item, 'a', ret='href')
					url = item
					links = self.links(url)
					if links is None: continue
					urls += [(i, name, name_info, quality, info, dsize) for i in links]
				except:
					source_utils.scraper_error('300MBFILMS')

			for item in urls:
				if 'earn-money' in item[0]: continue
				url = py_tools.ensure_text(client.replaceHTMLCodes(item[0]), errors='replace')
				valid, host = source_utils.is_host_valid(url, hostDict)
				if not valid: continue

				sources.append({'provider': '300mbfilms', 'source': host, 'name': item[1], 'name_info': item[2], 'quality': item[3], 'language': 'en', 'url': url,
											'info': item[4], 'direct': False, 'debridonly': True, 'size': item[5]})
			return sources
		except:
			source_utils.scraper_error('300MBFILMS')
			return sources

	def links(self, url):
		urls = []
		try:
			if not url: return
			for url in url:
				r = client.request(url)
				r = client.parseDOM(r, 'div', attrs={'class': 'entry'})
				r = client.parseDOM(r, 'a', ret='href')
				if 'money' not in str(r): continue

				r1 = [i for i in r if 'money' in i][0]
				r = client.request(r1)
				r = client.parseDOM(r, 'div', attrs={'id': 'post-\d+'})[0]

				if 'enter the password' in r:
					plink= client.parseDOM(r, 'form', ret='action')[0]
					post = {'post_password': '300mbfilms', 'Submit': 'Submit'}
					send_post = client.request(plink, post=post, output='cookie')
					link = client.request(r1, cookie=send_post)
				else:
					link = client.request(r1)
				if '<strong>Single' not in link: continue
				link = re.findall(r'<strong>Single(.+?)</tr', link, re.DOTALL | re.I)[0]
				link = client.parseDOM(link, 'a', ret='href')
				link = [(i.split('=')[-1]) for i in link]
				for i in link: urls.append(i)
				return urls
		except:
			source_utils.scraper_error('300MBFILMS')

	def resolve(self, url):
		return url