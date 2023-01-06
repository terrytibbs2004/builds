# -*- coding: utf-8 -*-

import re
import base64

from six import ensure_text
from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['fsapi.xyz']
            self.base_link = 'https://fsapi.xyz'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except Exception:
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            if not data['imdb'] or data['imdb'] == '0':
                return self.results
            if 'tvshowtitle' in data:
                anime = source_utils.is_anime('show', 'tvdb', tvdb)
                if anime:
                    url = self.base_link + '/imdb-anime/%s-%s-%s' % (data['imdb'], data['season'], data['episode'])
                else:
                    url = self.base_link + '/tv-imdb/%s-%s-%s' % (data['imdb'], data['season'], data['episode'])
            else:
                url = self.base_link + '/movie/%s' % data['imdb']
            html = client.request(url)
            matchs = re.findall('''&url=(.+?)" target=''', html)
            for match in matchs:
                match = base64.b64decode(match)
                link = ensure_text(match, errors='ignore')
                if any(i in link for i in ['api.123movie.cc', 'vidsrc.me']):
                    continue
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


"""


Scraper Testing - fsapi sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt0021814'
Scraper Testing - fsapi sources link: 'https://www.2embed.ru/embed/imdb/movie?id=tt0052416'


"""


