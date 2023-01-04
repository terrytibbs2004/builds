# -*- coding: UTF-8 -*-

import re
import base64

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
            self.domains = ['putlockerfun.com']
            self.base_link = 'https://putlockerfun.com'
            self.search_link = '/search/%s.html'
            self.cookie = client.request(self.base_link, output='cookie', timeout='5')
        except Exception:
            log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            search_url = self.base_link + self.search_link % search_title
            search_html = client.request(search_url, cookie=self.cookie)
            r = client.parseDOM(search_html, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'h2')[0], re.findall('<b>Release:\s*(\d+)</b>', i)[0]) for i in r]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            url = self.base_link + url
            return url
        except Exception:
            log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            search_title = cleantitle.get_plus(tvshowtitle)
            check_title = cleantitle.get(tvshowtitle)
            search_url = self.base_link + self.search_link % search_title
            search_html = client.request(search_url, cookie=self.cookie)
            r = client.parseDOM(search_html, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'h2')[0], re.findall('<b>Release:\s*(\d+)</b>', i)[0]) for i in r]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            url = self.base_link + url
            return url
        except Exception:
            log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            check_url1 = '-season-%s-episode-%s-' % (season, episode)
            check_url2 = '-season-%s-episode-%s' % (season, episode)
            html = client.request(url, cookie=self.cookie)
            details = client.parseDOM(html, 'div', attrs={'id': 'details'})
            episodes = zip(client.parseDOM(details, 'a', ret='href'))
            try:
                url = [(i[0]) for i in episodes if check_url1 in i[0]]
            except:
                url = [(i[0]) for i in episodes if i[0].endswith(check_url2)]
            url = self.base_link + url[0]
            return url
        except Exception:
            log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url, cookie=self.cookie)
            player = re.findall(r'document.write\(Base64.decode\("(.+?)"\)', html)[0]
            b64 = base64.b64decode(player)
            link = client.parseDOM(b64, 'iframe', ret='src')[0]
            link = self.base_link + link.replace('\/', '/')
            link = client.request(link, cookie=self.cookie, output='geturl')
            for source in scrape_sources.process(hostDict, link):
                self.results.append(source)
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


