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
            self.domains = ['rarefilmm.com']
            self.base_link = 'https://rarefilmm.com'
            self.search_link = '/?s=%s+%s'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_plus(title)
            check_term = '%s (%s)' % (title, year)
            url = self.base_link + self.search_link % (title, year)
            searchPage = client.scrapePage(url).text
            section = client.parseDOM(searchPage, "h2", attrs={"class": "excerpt-title"})
            for item in section:
                results = re.compile('<a href="(.+?)">(.+?)</a>').findall(item)
                for url, checkit in results:
                    if cleantitle.get_plus(check_term) == cleantitle.get_plus(checkit):
                        return url
            return
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            results = client.parseDOM(html, 'iframe', ret='src')
            results += re.compile('href="(.+?)"><strong>').findall(html)
            for link in results:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


