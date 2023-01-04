# -*- coding: utf-8 -*-

import re

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['yeshd.net']
            self.base_link = 'https://yeshd.net'
            self.search_link = '/?s=%s'
        except Exception:
            #log_utils.log('__init__', 1)
            return


# Might have blockage.


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_title = '%s (%s)' % (title, year)
            check_title = cleantitle.get(check_title)
            movie_link = self.base_link + self.search_link % movie_title
            r = client.request(movie_link)
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1])][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = tvshowtitle
            return url
        except Exception:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshow_title = cleantitle.get_plus(url)
            check_title = '%s Season %s' % (url, season)
            check_title = cleantitle.get(check_title)
            tvshow_link = self.base_link + self.search_link % tvshow_title
            r = client.request(tvshow_link)
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1])][0]
            url = url.replace('/series/', '/episode/')
            url = url[:-1] if url.endswith('/') else url
            url = url + '-episode-%s/' % episode
            return url
        except Exception:
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url)
            links = client.parseDOM(html, 'a', attrs={'target': '_blank'}, ret='href')
            for link in links:
                if 'facebook.com' in link or link == '#':
                    continue
                if 'getlinkstream.xyz' in link:
                    html = client.request(link)
                    vlinks = client.parseDOM(html, 'a', ret='href')
                    for vlink in vlinks:
                        for source in scrape_sources.process(hostDict, vlink):
                            self.results.append(source)
                else:
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


