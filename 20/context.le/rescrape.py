# -*- coding: utf-8 -*-

from json import dumps as jsdumps, loads as jsloads
import sys
import xbmc
try: #Py2
	from urlparse import parse_qsl
	from urllib import quote_plus
except ImportError: #Py3
	from urllib.parse import parse_qsl, quote_plus

if __name__ == '__main__':
	item = sys.listitem
	# message = item.getLabel()
	path = item.getPath()
	plugin = 'plugin://plugin.video.le/'
	args = path.split(plugin, 1)
	params = dict(parse_qsl(args[1].replace('?', '')))

	title = params['title']
	systitle = quote_plus(title)
	year = params.get('year', '')

	if 'meta' in params:
		meta = jsloads(params['meta'])
		imdb = meta.get('imdb', '')
		tmdb = meta.get('tmdb', '')
		tvdb = meta.get('tvdb', '')
		season = meta.get('season', '')
		episode = meta.get('episode', '')
		tvshowtitle = meta.get('tvshowtitle', '')
		systvshowtitle = quote_plus(tvshowtitle)
		premiered = ''
		if tvshowtitle: premiered = meta.get('premiered', '')
	else:
		imdb = params.get('imdb', '')
		tmdb = params.get('tmdb', '')
		tvdb = params.get('tvdb', '')
		season = params.get('season', '')
		episode = params.get('episode', '')
		tvshowtitle = params.get('tvshowtitle', '')
		systvshowtitle = quote_plus(tvshowtitle)
		premiered = ''
		if tvshowtitle: premiered = params.get('premiered', '')

	sysmeta = quote_plus(jsdumps(meta))
	path = 'PlayMedia(%s?action=play_Item&title=%s&year=%s&imdb=%s&tmdb=%s&tvdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=%s&meta=%s&rescrape=true)' % (
									plugin, systitle, year, imdb, tmdb, tvdb, season, episode, systvshowtitle, premiered, sysmeta)
	xbmc.executebuiltin(path)