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
            self.genre_filter = ['animation', 'anime']
            self.domains = ['gogoanime.tel', 'gogoanime.gg', 'gogoanime.film', 'gogoanime.video', 'gogoanime.vc']
            self.base_link = 'https://gogoanime.tel'
            self.search_link = '/search.html?keyword=%s'
            self.episode_link = '/%s-episode-%s'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            q = self.base_link + self.search_link % cleantitle.get_plus(tvshowtitle)
            r = client.request(q)
            r = client.parseDOM(r, 'ul', attrs={'class': 'items'})
            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('\d{4}', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][-1]) for i in r if i[0] and i[1] and i[2]]
            r = [i for i in r if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year)]
            url = r[0][0]
            return url
        except Exception:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            url = [i for i in url.strip('/').split('/')][-1]
            url = self.base_link + self.episode_link % (url, int(episode))
            return url
        except Exception:
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url)
            r = client.parseDOM(html, 'a', ret='data-video')
            for u in r:
                for source in scrape_sources.process(hostDict, u):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


