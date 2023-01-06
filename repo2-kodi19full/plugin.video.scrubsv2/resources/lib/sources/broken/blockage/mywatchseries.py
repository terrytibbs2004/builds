# -*- coding: UTF-8 -*-

import re

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['mywatchseries.stream', 'get.mywatchseries.stream', 'go.mywatchseries.stream', 'on.mywatchseries.stream']
            self.base_link = 'https://mywatchseries.stream'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except Exception:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshowTitle = url
            season = '%s' % int(season)
            episode = '%02d' % int(episode)
            episodeTitle = cleantitle.geturl(title)
            url = self.base_link + '/%s-%sx%s-%s' % (tvshowTitle, str(season), str(episode), episodeTitle)
            return url
        except Exception:
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            item_page = client.scrapePage(url).text
            item_results = client.parseDOM(item_page, 'tr')
            item_results = [(client.parseDOM(i, 'a', attrs={'target': '_blank'}, ret='href')[0], client.parseDOM(i, 'a', attrs={'target': '_blank'}, ret='title')[0]) for i in item_results]
            for item in item_results:
                valid, host = source_utils.is_host_valid(item[1], hostDict)
                if host in str(self.results):
                    continue
                if valid:
                    link = self.base_link + item[0]
                    self.results.append({'source': host, 'quality': 'SD', 'url': link, 'direct': False})
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        try:
            item_page = client.scrapePage(url).text
            item_link = client.parseDOM(item_page, 'a', attrs={'rel': 'external nofollow'}, ret='href')[0]
            if item_link.startswith('/play/'):
                link = self.base_link + item_link
            else:
                link = item_link
            link = client.scrapePage(link).url
            return link
        except Exception:
            #log_utils.log('resolve', 1)
            return url


