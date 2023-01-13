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
		self.priority = 22
		self.language = ['en']
		self.domains = ['new.myvideolinks.net']
		self.base_link = 'http://new.myvideolinks.net'
		self.search_link = '/?s=%s'
		# http://new.myvideolinks.net/search/%s/feed/rss2/

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
			query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)
			url = '%s%s' % (self.base_link, self.search_link % quote_plus(query))
			# log_utils.log('url = %s' % url, __name__, log_utils.LOGDEBUG)
			r = client.request(url, timeout='5')
			if not r or 'Error 404' in r: return sources
			r = client.parseDOM(r, 'div', attrs={'id': 'content'})
			r1= client.parseDOM(r, 'h2')
			posts = zip(client.parseDOM(r1, 'a', ret='href'), client.parseDOM(r1, 'a'))
		except:
			source_utils.scraper_error('MYVIDEOLINK')
			return sources
		items = []
		for post in posts:
			try:
				name = source_utils.strip_non_ascii_and_unprintable(post[1])
				if '<' in name: name = re.sub(r'<.*?>', '', name)
				name = client.replaceHTMLCodes(name)
				name = source_utils.clean_name(name)

				if 'tvshowtitle' in data:
					if not source_utils.check_title(title, aliases, name, hdlr, year):
						if not source_utils.check_title(title, aliases, name, 'S%02d' % int(data['season']), year):
							if not source_utils.check_title(title, aliases, name, 'Season.%d' % int(data['season']), year):
								if not source_utils.check_title(title, aliases, name, 'S%d' % int(data['season']), year): continue
				else:
					if not source_utils.check_title(title, aliases, name, hdlr, year): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)

				link = post[0]
				results = client.request(link, timeout='5')
				results = client.parseDOM(results, 'div', attrs={'class': 'entry-content cf'})[0]

				if 'tvshowtitle' in data:
					isSeasonList = False
					if 'Season' in name or 'S%02d' % int(data['season']) in name:
						isSeasonList = True
					results = re.sub(r'\n', '', results)
					results = re.sub(r'\t', '', results).replace('> <', '><')
					test = re.findall(r'<p><b>(.*?)</ul>', results, re.DOTALL) # parsing this site for episodes is a bitch, fuck it this is close as I'm doing
					for x in test:
						test2 = re.search(r'(.*?)</b>', x).group(1)
						if hdlr in test2:
							if isSeasonList:
								name = re.sub(r'\.Season\.\d+', '.%s.' % test2.replace(' ', '.'), name)
								name = re.sub(r'\.S\d+', '.%s' % test2.replace(' ', '.'), name)
							else: name = test2
							links = client.parseDOM(x, 'a', ret='href')
							break
						else:
							try: test3 = re.search(r'<p><b>(.*?)</b></p>', x).group(1)
							except: continue
							if hdlr in test3:
								if isSeasonList:
									name = re.sub(r'\.Season\.\d+', '.%s.' % test3.replace(' ', '.'), name)
									name = re.sub(r'\.S\d+', '.%s' % test3.replace(' ', '.'), name)
								else: name = test3
								links = client.parseDOM(x, 'a', ret='href')
								break
				else:
					links = client.parseDOM(results, 'a', attrs={'class': 'autohyperlink'}, ret='href')

				for link in links:
					try:
						url = py_tools.ensure_text(client.replaceHTMLCodes(str(link)), errors='replace')
						if url.endswith(('.rar', '.zip', '.iso', '.part', '.png', '.jpg', '.bmp', '.gif')): continue
						if url in str(sources): continue

						valid, host = source_utils.is_host_valid(url, hostDict)
						if not valid: continue

						quality, info = source_utils.get_release_quality(name_info, url)
						try:
							size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', results).group(0)
							dsize, isize = source_utils._size(size)
							info.insert(0, isize)
						except:
							dsize = 0
						info = ' | '.join(info)

						sources.append({'provider': 'myvideolink', 'source': host, 'name': name, 'name_info': name_info, 'quality': quality, 'language': 'en', 'url': url,
													'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
					except:
						source_utils.scraper_error('MYVIDEOLINK')
			except:
				source_utils.scraper_error('MYVIDEOLINK')
		return sources

	def resolve(self, url):
		return url