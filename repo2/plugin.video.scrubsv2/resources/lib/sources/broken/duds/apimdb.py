# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urljoin, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['openvids.io', 'v2.apimdb.net', 'apimdb.net']
            self.base_link = 'https://openvids.io'
        except Exception:
            log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('tvshow', 1)
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
        except:
            log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            if 'tvshowtitle' in data:
                url = self.base_link + '/episode/%s-%s-%s' % (data['imdb'], data['season'], data['episode'])
                check = '/%s-%s-%s/' % (data['imdb'], data['season'], data['episode'])
            else:
                url = self.base_link + '/movie/%s' % data['imdb']
                check = '/%s/' % data['imdb']
            html = client.request(url)
            if not check in html:
                return self.results
            results = client.parseDOM(html, 'div', attrs={'class': 'server'}, ret='data-src')
            for result in results:
                try:
                    result_url = self.base_link + result
                    result_html = client.request(result_url)
                    link = client.parseDOM(result_html, 'iframe', ret='src')[0]
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
                except:
                    log_utils.log('sources', 1)
                    pass
            return self.results
        except:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


