# -*- coding: UTF-8 -*-
# (updated 9-20-2021)
'''
	LEscrapers Project
'''

from base64 import b64encode
import re
import requests
try: #Py2
	from urllib import urlencode, quote
	from urlparse import parse_qs
except ImportError: #Py3
	from urllib.parse import urlencode, quote, parse_qs
from lescrapers.modules.control import setting as getSetting
from lescrapers.modules import source_utils

SORT = {'s1': 'relevance', 's1d': '-', 's2': 'dsize', 's2d': '-', 's3': 'dtime', 's3d': '-'}
SEARCH_PARAMS = {'st': 'adv', 'sb': 1, 'fex': 'm4v,3gp,mov,divx,xvid,wmv,avi,mpg,mpeg,mp4,mkv,avc,flv,webm', 'fty[]': 'VIDEO', 'spamf': 1, 'u': '1', 'gx': 1, 'pno': 1, 'sS': 3}
SEARCH_PARAMS.update(SORT)


class source:
	def __init__(self):
		self.priority = 21
		self.language = ['en']
		self.domain = 'easynews.com'
		self.base_link = 'https://members.easynews.com'
		self.search_link = '/2.0/search/solr-search/advanced'

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
		auth = self._get_auth()
		if not auth: return sources
		try:
			title_chk = getSetting('easynews.title.chk') == 'true'
			data = parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')
			aliases = data['aliases']

			episode_title = data['title'] if 'tvshowtitle' in data else None
			year = data['year']
			years = [str(year), str(int(year)+1), str(int(year)-1)] if 'tvshowtitle' not in data else None
			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else year

			query = self._query(data)
			url, params = self._translate_search(query)
			headers = {'Authorization': auth}
			results = requests.get(url, params=params, headers=headers, timeout=15).json()
			down_url = results.get('downURL')
			dl_farm = results.get('dlFarm')
			dl_port = results.get('dlPort')
			files = results.get('data', [])
		except:
			source_utils.scraper_error('EASYNEWS')
			return sources
		for item in files:
			try:
				post_hash, post_title, ext, duration = item['0'], item['10'], item['11'], item['14']
				# log_utils.log('post_title = %s' % post_title, __name__, log_utils.LOGDEBUG)
				checks = [False] * 5
				if 'alangs' in item and item['alangs'] and 'eng' not in item['alangs']: checks[1] = True
				if re.match('^\d+s', duration) or re.match('^[0-5]m', duration): checks[2] = True
				if 'passwd' in item and item['passwd']: checks[3] = True
				if 'virus' in item and item['virus']: checks[4] = True
				if 'type' in item and item['type'].upper() != 'VIDEO': checks[5] = True
				if any(checks): continue

				stream_url = down_url + quote('/%s/%s/%s%s/%s%s' % (dl_farm, dl_port, post_hash, ext, post_title, ext))
				name = source_utils.clean_name(post_title)
				# log_utils.log('name = %s' % name, __name__, log_utils.LOGDEBUG)
				name_chk = name
				if 'tvshowtitle' in data:
					name_chk = re.sub(r'S\d+([.-])E\d+', hdlr, name_chk, 1, re.I)
					name_chk = re.sub(r'^tvp[.-]', '', name_chk, 1, re.I)
				name_chk = re.sub(r'disney[.-]gallery[.-]star[.-]wars[.-]', '', name_chk, 0, re.I)
				name_chk = re.sub(r'marvels[.-]', '', name_chk, 0, re.I)
				if title_chk:
					if not source_utils.check_title(title, aliases, name_chk, hdlr, year, years): continue

				name_info = source_utils.info_from_name(name_chk, title, year, hdlr, episode_title)
				if source_utils.remove_lang(name_info): continue

				file_dl = stream_url + '|Authorization=%s' % (quote(auth))

				quality, info = source_utils.get_release_quality(name_info, file_dl)
				try:
					size = float(int(item['rawSize']))
					dsize, isize = source_utils.convert_size(size, to='GB')
					if isize: info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				sources.append({'provider': 'easynews', 'source': 'direct', 'name': name, 'name_info': name_info, 'quality': quality, 'language': "en", 'url': file_dl,
											'info': info, 'direct': True, 'debridonly': False, 'size': dsize})
			except:
				source_utils.scraper_error('EASYNEWS')
		return sources

	def resolve(self, url):
		return url

	def _get_auth(self):
		auth = None
		username = getSetting('easynews.user')
		password = getSetting('easynews.password')
		if username == '' or password == '': return auth
		try: # Python 2
			user_info = '%s:%s' % (username, password)
			auth = 'Basic ' + b64encode(user_info)
		except: # Python 3
			user_info = '%s:%s' % (username, password)
			user_info = user_info.encode('utf-8')
			auth = 'Basic ' + b64encode(user_info).decode('utf-8')
		return auth

	def _query(self, data):
		if 'tvshowtitle' not in data:
			title = re.sub(r'[^A-Za-z0-9\s\.-]+', '', data.get('title'))
			year = int(data.get('year'))
			years = '%s,%s,%s' % (str(year - 1), year, str(year + 1))
			query = '"%s" %s' % (title, years)
		else:
			title = re.sub(r'[^A-Za-z0-9\s\.-]+', '', data.get('tvshowtitle'))
			season = int(data.get('season'))
			episode = int(data.get('episode'))
			query = '%s S%02dE%02d' % (title, season, episode)
		return query

	def _translate_search(self, query):
		params = SEARCH_PARAMS
		params['pby'] = 350
		params['safeO'] = 1 # 1 is the moderation (adult filter) ON, 0 is OFF.
		# params['gps'] = params['sbj'] = query # gps stands for "group search" and does so by keywords, sbj=subject and can limit results, use gps only
		params['gps'] = query
		url = self.base_link + self.search_link
		return url, params