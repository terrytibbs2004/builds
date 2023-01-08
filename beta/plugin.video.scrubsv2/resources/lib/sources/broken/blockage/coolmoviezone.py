# -*- coding: UTF-8 -*-

import re

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
            self.domains = ['coolmoviezone.show', 'coolmoviezone.studio', 'coolmoviezone.ninja', 'coolmoviezone.online',
                'coolmoviezone.io', 'coolmoviezone.biz', 'coolmoviezone.info'
            ]
            self.base_link = 'https://coolmoviezone.show'
            self.search_link = '/search/%s/feed/rss2/'
        except Exception:
            #log_utils.log('__init__', 1)
            return

#https://coolmoviezone.agency
#https://coolmoviezone.company/

#https://coolmoviezone.cfd/


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_term = '%s (%s)' % (title, year)
            check_title = cleantitle.get_plus(check_term)
            search_url = self.base_link + self.search_link % movie_title
            html = client.scrapePage(search_url).text
            items = client.parseDOM(html, 'item')
            r = [(client.parseDOM(i, 'title'), client.parseDOM(i, 'link')) for i in items]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            url = [i[1] for i in r if check_title == cleantitle.get_plus(i[0])][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            links = re.compile('<td align="center"><strong><a href="(.+?)">', re.DOTALL).findall(html)
            for link in links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


