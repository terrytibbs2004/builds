# -*- coding: utf-8 -*-

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import scrape_sources
#from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['go.myvideolinks.net', 'to.myvideolinks.net', 'forums.myvideolinks.net', 'myvideolinks.net']
            self.base_link = 'https://go.myvideolinks.net'
            self.search_link = '/search/%s/feed/rss2/'
        except Exception:
            #log_utils.log('__init__', 1)
            return


# Reworked the old scraper to this new url then ditched the tv show bit for now till i get the urge to fuck with it.
# This simple ghetto rig seems to be working fine besides some results failing. Might need a bit more testing.


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            year = data['year']
            search_url = self.base_link + self.search_link % data['imdb']
            search_html = client.scrapePage(search_url).text
            posts = client.parseDOM(search_html, 'item')
            for post in posts:
                post_title = client.parseDOM(post, 'title')[0]
                if not year in post_title:
                    continue
                links = client.parseDOM(post, 'a', attrs={'class': 'autohyperlink'}, ret='href')
                links += client.parseDOM(post, 'iframe', ret='src')
                for link in links:
                    for source in scrape_sources.process(hostDict, link, info=post_title):
                        self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


