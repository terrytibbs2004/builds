# -*- coding: utf-8 -*-

import re

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['my.go123movies.io']
        self.base_link = 'https://my.go123movies.io'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            movie_link = self.base_link + self.search_link % movie_title
            r = client.scrapePage(movie_link).text
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='oldtitle'), re.findall('(\d{4})', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshow_title = cleantitle.get_plus(tvshowtitle)
            check_title = cleantitle.get(tvshowtitle)
            tvshow_link = self.base_link + self.search_link % tvshow_title
            r = client.scrapePage(tvshow_link).text
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='oldtitle'), re.findall('(\d{4})', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            return url
        except Exception:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url[:-1]
            url = url.replace('/series/', '/episode/')
            url = url + '-season-%s-episode-%s/' % (season, episode)
            return url
        except Exception:
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            links = client.parseDOM(html, 'iframe', ret='src')
            for link in links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


