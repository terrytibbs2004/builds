# -*- coding: UTF-8 -*-

import re

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import source_utils
from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['telepisodes.org']
            self.base_link = 'https://telepisodes.org'
            self.cookie = client.request(self.base_link, output='cookie', timeout='5')
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = self.base_link + '/tv-series/%s/season-%s/episode-%s/' % (url, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            page = client.request(url, cookie=self.cookie)
            items = client.parseDOM(page, 'td', attrs={'class': 'linkdom w3-center'})
            for item in items:
                try:
                    hoster = client.parseDOM(item, 'a', attrs={'rel': 'nofollow ugc'}, ret='title')[0]
                    valid, host = source_utils.is_host_valid(hoster, hostDict)
                    if valid:
                        link = client.parseDOM(item, 'a', attrs={'rel': 'nofollow ugc'}, ret='href')[0]
                        link = self.base_link + link
                        self.results.append({'source': host, 'quality': 'SD', 'url': link, 'direct': False})
                except:
                    log_utils.log('sources', 1)
                    pass
            return self.results
        except:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        if any(x in url for x in self.domains):
            html = client.request(url, cookie=self.cookie)
            try:
                link = client.parseDOM(html, 'iframe', ret='src')[0]
                return link
            except:
                match = re.compile(r'href=(/open/site/.+?)>', re.I|re.S).findall(html)[0]
                link = self.base_link + match
                link = client.request(link, cookie=self.cookie, output='geturl')
                return link
        else:
            return url


