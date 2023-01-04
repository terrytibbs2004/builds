# -*- coding: UTF-8 -*-

from six import ensure_text

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
            self.domains = ['flenix.plus']
            self.base_link = 'https://flenix.plus'
            self.search_link = '/index.php?do=search&filter=true'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            check_title = cleantitle.get_dash(title)
            search_url = self.base_link + self.search_link
            post = ('do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s' % (imdb))
            html = ensure_text(client.request(search_url, post=post), errors='replace')
            posts = client.parseDOM(html, 'div', attrs={'class': 'post'})
            post = [(client.parseDOM(i, 'div', attrs={'class': 'title'})) for i in posts]
            urls = [(client.parseDOM(i, 'a', ret='href')) for i in post]
            url = [i[0] for i in urls][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url)
            try:
                qual = client.parseDOM(html, 'div', attrs={'class': 'quality'})[0]
            except:
                qual = 'SD'
            links = client.parseDOM(html, 'iframe', ret='src')
            for link in links:
                if any(i in link for i in ['123files.club', 'api.hdv.fun', 'consistent.stream', 'dbgo.fun']):
                    continue
                for source in scrape_sources.process(hostDict, link, info=qual):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


