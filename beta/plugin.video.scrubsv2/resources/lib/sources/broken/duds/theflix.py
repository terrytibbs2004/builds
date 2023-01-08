# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils
from resources.lib.modules import tmdb_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['theflix.to']
            self.base_link = 'https://theflix.to'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.geturl(title)
            tmdb_id = tmdb_utils.find_movie_by_external_source(imdb=imdb)
            url = self.base_link + '/movie/%s-%s' % (tmdb_id['id'], movie_title)
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshow_title = cleantitle.geturl(tvshowtitle)
            tmdb_id = tmdb_utils.find_tvshow_by_external_source(imdb=imdb)
            url = self.base_link + '/tv-show/%s-%s' % (tmdb_id['id'], tvshow_title)
            return url
        except Exception:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url + '/season-%s/episode-%s' % (season, episode)
            return url
        except Exception:
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url)
            links = re.compile('"videoUrl":"(.+?)",', re.DOTALL).findall(html)
            for link in links:
                link = link.replace('\\u0026', '&')
                quality, info = source_utils.get_release_quality(link, link)
                link += '|%s' % urlencode({'Referer': url})
                self.results.append({'source': 'Direct', 'quality': quality, 'url': link, 'info': info, 'direct': True})
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


