# -*- coding: UTF-8 -*-

from resources.lib.modules import client
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources
from resources.lib.modules import tmdb_utils


class source:
    def __init__(self):
        self.results = []
        self.domains = ['1movietv.com']
        self.base_link = 'https://1movietv.com'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + '/playstream/' + imdb
            return url
        except Exception:
            log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tmdb_id = tmdb_utils.find_tvshow_by_external_source(imdb=imdb)
            url = '/playstream/' + tmdb_id['id']
            return url
        except Exception:
            log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = self.base_link + url + '-' + season + '-' + episode
            return url
        except Exception:
            log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            links = client.parseDOM(html, 'iframe', ret='src')
            for link in links:
                if any(i in link for i in ['1movietv.xyz', 'vido.fun']):
                    continue
                log_utils.log('Scraper onemovietv sources link: ' + repr(link))
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


