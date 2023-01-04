# -*- coding: utf-8 -*-

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
            self.domains = ['gomoviz.top', 'gomoviz.uno', 'gomoviz.cyou', 'gomoviz.online', 'gomoviz.us', 'gomoviz.xyz', 'gomoviz.org']
            self.base_link = 'https://gomoviz.top'
            self.search_link = '/?s=%s'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            search_url = self.base_link + self.search_link % cleantitle.get_plus(title)
            r = client.scrapePage(search_url).text
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), re.findall('(\d{4})', i), client.parseDOM(i, 'a', ret='oldtitle')) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [(i[0], i[1], re.findall('(.+?)(?:\(|$)', i[2])) for i in r]
            r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
            url = [i[0] for i in r if cleantitle.match_alias(i[2], aliases) and cleantitle.match_year(i[1], year)][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            try:
                qual = client.parseDOM(html, 'span', attrs={'class': 'quality'})[0]
            except:
                qual = 'SD'
            links = client.parseDOM(html, 'iframe', ret='src')
            links += client.parseDOM(html, 'a', attrs={'class': 'su-button su-button-style-flat'}, ret='href')
            for link in links:
                if any(i in link for i in ['youtube.com', 'abcvideo.cc']):
                    continue
                for source in scrape_sources.process(hostDict, link, info=qual):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


