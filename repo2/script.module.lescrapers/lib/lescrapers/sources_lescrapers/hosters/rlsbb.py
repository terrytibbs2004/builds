# -*- coding: utf-8 -*-
# modified by Venom for LEscrapers (updated 11-05-2021)
'''
	LEscrapers Project
'''

import re
try: #Py2
	from urlparse import parse_qs
	from urllib import urlencode
except ImportError: #Py3
	from urllib.parse import parse_qs, urlencode
from lescrapers.modules import cfscrape
from lescrapers.modules import client
from lescrapers.modules import py_tools
from lescrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 26
		self.language = ['en']
		self.domains = ['proxybb.com', 'rlsbb.ru', 'rlsbb.to']
		self.base_new = 'http://proxybb.com'
		self.base_old = 'http://old3.proxybb.com'
		self.search_link = 'http://search.proxybb.com/?s=%s' #may use in future but adds a request to do so.

	def movie(self, imdb, title, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('RLSBB')
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
			url = urlencode(url)
			return url
		except:
			source_utils.scraper_error('RLSBB')
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
			source_utils.scraper_error('RLSBB')
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

			isSeasonQuery = False
			query = '%s %s' % (title, hdlr)
			query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)
			# query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', query)
			query = re.sub(r'\s', '-', query)

			if int(year) >= 2021: self.base_link = self.base_new
			else: self.base_link = self.base_old

			url = '%s%s' % (self.base_link, query)
			# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)

			# r = scraper.get(url).content
			r = py_tools.ensure_str(scraper.get(url).content, errors='replace')
			if not r or 'nothing was found' in r:
				if 'tvshowtitle' in data:
					season = re.search(r'S(.*?)E', hdlr).group(1)
					query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', title)
					# query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', title)
					query = re.sub(r'\s', '-', query)
					query = query + "-S" + season
					url = '%s%s' % (self.base_link, query)
					# r = scraper.get(url).content
					r = py_tools.ensure_str(scraper.get(url).content, errors='replace')
					isSeasonQuery = True
				else: return sources 
			if not r or 'nothing was found' in r: return sources
			# may need to add fallback to use self.search_link if nothing found
			posts = client.parseDOM(r, "div", attrs={"class": "content"})
			if not posts: return sources
		except:
			source_utils.scraper_error('RLSBB')
			return sources

		release_title = re.sub(r'[^A-Za-z0-9\s\.-]+', '', title).replace(' ', '.')
		items = [] ; count = 0
		for post in posts:
			if count >= 300: break # to limit large link list and slow scrape time
			try:
				post_titles = re.findall(r'(?:.*>|>\sRelease Name.*|\s)(%s.*?)<' % release_title, post, re.I) #parse all matching release_titles in each post(content) group
				items = []
				if len(post_titles) >1:
					index = 0
					for name in post_titles:
						start = post_titles[index].replace('[', '\\[').replace('(', '\\(').replace(')', '\\)').replace('+', '\\+').replace(' \\ ', ' \\\\ ')
						end = (post_titles[index + 1].replace('[', '\\[').replace('(', '\\(').replace(')', '\\)').replace('+', '\\+')).replace(' \\ ', ' \\\\ ') if index + 1 < len(post_titles) else ''
						try: container = re.findall(r'(?:%s)([\S\s]+)(?:%s)' % (start, end), post, re.I)[0] #parse all data between release_titles in multi post(content) group
						except:
							source_utils.scraper_error('RLSBB')
							continue
						try: size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', container).group(0).replace(',', '.')
						except: size = '0'
						container = client.parseDOM(container, 'a', ret='href')
						items.append((name, size, container))
						index += 1
				elif len(post_titles) == 1:
					name = post_titles[0]
					container = client.parseDOM(post, 'a', ret='href') #parse all links in a single post(content) group
					try: size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', post).group(0).replace(',', '.')
					except: size = '0'
					items.append((name, size, container))
				else: continue

				for group_name, size, links in items:
					for i in links:
						name = group_name
						# if isSeasonQuery and hdlr not in name.upper():
							# name = i.rsplit("/", 1)[-1]
							# if hdlr not in name.upper(): continue
						if hdlr not in name.upper():
							name = i.rsplit("/", 1)[-1]
							if hdlr not in name.upper(): continue

						name = client.replaceHTMLCodes(name)
						name = source_utils.strip_non_ascii_and_unprintable(name)
						name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)

						url = py_tools.ensure_text(client.replaceHTMLCodes(str(i)), errors='replace')
						if url in str(sources): continue
						if url.endswith(('.rar', '.zip', '.iso', '.part', '.png', '.jpg', '.bmp', '.gif')): continue

						valid, host = source_utils.is_host_valid(url, hostDict)
						if not valid: continue

						quality, info = source_utils.get_release_quality(name, url)
						try:
							if size == '0':
								try: size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', name).group(0).replace(',', '.')
								except: raise Exception()
							dsize, isize = source_utils._size(size)
							info.insert(0, isize)
						except:
							dsize = 0
						info = ' | '.join(info)

						sources.append({'provider': 'rlsbb','source': host, 'name': name, 'name_info': name_info, 'quality': quality, 'language': 'en', 'url': url,
													'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
						count += 1
			except:
				source_utils.scraper_error('RLSBB')
		return sources

	def resolve(self, url):
		return url