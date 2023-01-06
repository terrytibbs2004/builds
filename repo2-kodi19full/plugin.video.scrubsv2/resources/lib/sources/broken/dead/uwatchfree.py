# -*- coding: UTF-8 -*-

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
            self.domains = ['uwatchfree.fo', 'uwatchfree.as']
            self.base_link = 'https://www.uwatchfree.fo'
            self.search_link = '/search/%s/feed/rss2/'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            check_term = '%s (%s)' % (title, year)
            check_title = cleantitle.get_plus(check_term)
            movie_link = self.base_link + self.search_link % imdb
            html = client.scrapePage(movie_link).text
            posts = client.parseDOM(html, 'item')
            for post in posts:
                if not imdb in post:
                    continue
                post_title = client.parseDOM(post, 'title')[0]
                if not check_title == cleantitle.get_plus(post_title):
                    continue
                url = client.parseDOM(post, 'link')[0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            body = client.parseDOM(html, 'tbody')[0]
            links = client.parseDOM(body, 'a', ret='href')
            for link in links:
                html = client.scrapePage(link).text
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


