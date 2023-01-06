# -*- coding: UTF-8 -*-

import re

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import scrape_sources
#from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['putlockers.net']
            self.base_link = 'https://wwv.putlockers.net'
            self.search_link = '/search/?s=%s'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            search_url = self.base_link + self.search_link % cleantitle.get_plus(title)
            r = client.scrapePage(search_url).text
            r = client.parseDOM(r, 'div', attrs={'class': 'featuredItems singleVideo'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='oldtitle'), client.parseDOM(i, 'div', attrs={'class': 'jt-info'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            link = [i[0] for i in r if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year)][0]
            page = client.scrapePage(link).text
            videoArea = client.parseDOM(page, 'div', attrs={'class': 'videoArea'})
            url = client.parseDOM(videoArea, 'a', ret='href')[0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            search_url = self.base_link + self.search_link % cleantitle.get_plus(tvshowtitle)
            r = client.scrapePage(search_url).text
            r = client.parseDOM(r, 'div', attrs={'class': 'featuredItems singleVideo'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='oldtitle'), client.parseDOM(i, 'div', attrs={'class': 'jt-info'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            link = [i[0] for i in r if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year) and '/series/' in i[0]][0]
            url = re.findall('(?://.+?|)(/.+)', link)[0]
            return url
        except Exception:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshowtitle = re.findall('/series/(.+?)/', url)[0]
            link = self.base_link + '/episode/%s-%sx%s/' % (tvshowtitle, season, episode)
            episodePage = client.scrapePage(link).text
            videoArea = client.parseDOM(episodePage, 'div', attrs={'class': 'videoArea'})
            url = client.parseDOM(videoArea, 'a', ret='href')[0]
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


