# -*- coding: utf-8 -*-
# created by Venom for Yourscrapers (updated 12-20-2021)
"""
	Yourscrapers Project
"""

import re
from urllib.parse import quote_plus, unquote_plus
from yourscrapers.modules import client
from yourscrapers.modules import source_utils


class source:
	priority = 5
	pack_capable = False
	hasMovies = True
	hasEpisodes = True
	def __init__(self):
		self.language = ['en']
		self.base_link = "http://topnow.se"
		self.search_link = '/index.php?search=%s'
		self.show_link = '/index.php?show=%s'

	def sources(self, data, hostDict):
		sources = []
		if not data: return sources
		append = sources.append
		try:
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ')
			aliases = data['aliases']
			episode_title = data['title'] if 'tvshowtitle' in data else None
			year = data['year']
			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else ('(' + year + ')')

			query = title
			query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', query)
			if 'tvshowtitle' in data: url = self.show_link % query.replace(' ', '-')
			else: url = self.search_link % quote_plus(query)
			url = '%s%s' % (self.base_link, url)
			# log_utils.log('url = %s' % url)
			results = client.request(url, timeout=5)
			if not results: return sources
			results = re.sub('[\r\n\t]', '', results)
			items = client.parseDOM(results, 'div', attrs={'class': 'card'})
			if not items: return sources
			undesirables = source_utils.get_undesirables()
			check_foreign_audio = source_utils.check_foreign_audio()
		except:
			source_utils.scraper_error('TOPNOW')
			return sources

		for item in items:
			try:
				if 'magnet:' not in item: continue
				name = client.parseDOM(item, 'img', attrs={'class': 'thumbnails'}, ret='alt')[0].replace(u'\xa0', u' ')
				if not source_utils.check_title(title, aliases, name, hdlr.replace('(', '').replace(')', ''), year): continue

				url = re.search(r'href\s*=\s*["\'](magnet:[^"\']+)["\']', item, re.DOTALL | re.I).group(1)
				try: url = unquote_plus(url).decode('utf8').replace('&amp;', '&').replace(' ', '.')
				except: url = unquote_plus(url).replace('&amp;', '&').replace(' ', '.')
				url = re.sub(r'(&tr=.+)&dn=', '&dn=', url) # some links on topnow &tr= before &dn=
				url = url.split('&tr=')[0].replace(' ', '.')
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1)
				release_name = source_utils.clean_name(url.split('&dn=')[1])
				name_info = source_utils.info_from_name(release_name, title, year, hdlr, episode_title)
				if source_utils.remove_lang(name_info, check_foreign_audio): continue
				if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue

				seeders = 0 # seeders not available on topnow
				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', item).group(0) # file size is no longer available on topnow's new site
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				append({'provider': 'topnow', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': release_name, 'name_info': name_info,
								'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('TOPNOW')
		return sources