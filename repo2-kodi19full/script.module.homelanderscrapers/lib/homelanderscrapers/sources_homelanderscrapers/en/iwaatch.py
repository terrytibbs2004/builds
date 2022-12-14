# -*- coding: utf-8 -*-

import re

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, quote, quote_plus
except ImportError: from urllib.parse import urlencode, quote, quote_plus

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import dom_parser as dom
from resources.lib.modules import source_utils


class source:
	def __init__(self):
		self.priority = 32
		self.language = ['en']
		self.domains = ['iwaatch.com']
		self.base_link = 'https://iwaatch.com/'
		self.search_link = 'api/api.php?page=moviesearch&q={0}'


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'year': year}
			url = urlencode(url)
			return url
		except BaseException:
			source_utils.scraper_error('IWAATCH')
			return


	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			if not url:
				return sources

			data = parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
			title = data['title']
			year = data['year']
			t = title + year

			query = '%s' % data['title']
			query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

			url = self.search_link.format(quote_plus(query))
			url = urljoin(self.base_link, url)
			# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)

			r = client.request(url)
			if r is None:
				return sources
			if 'Not Found' in r:
				return sources
			items = client.parseDOM(r, 'li')
			items = [(dom.parse_dom(i, 'a', req='href')[0]) for i in items if year in i]
			items = [(i.attrs['href'], re.sub('<.+?>|\n', '', i.content).strip()) for i in items]
			item = [i[0].replace('movie', 'view') for i in items if cleantitle.get(t) == cleantitle.get(i[1])][0]

			html = client.request(item)
			streams = re.findall('sources\:\s*\[(.+?)\]\,', html, re.DOTALL)[0]
			streams = re.findall('src:\s*[\'"](.+?)[\'"].+?size:\s*[\'"](.+?)[\'"]', streams, re.DOTALL)

			for link, label in streams:
				quality = source_utils.get_release_quality(label, label)[0]
				link += '|User-Agent=%s&Referer=%s' % (quote(client.agent()), item)
				sources.append({'source': 'direct', 'quality': quality, 'info': '', 'language': 'en', 'url': link,
				                'direct': True, 'debridonly': False})

			return sources
		except:
			source_utils.scraper_error('IWAATCH')
			return sources


	def resolve(self, url):
		return url