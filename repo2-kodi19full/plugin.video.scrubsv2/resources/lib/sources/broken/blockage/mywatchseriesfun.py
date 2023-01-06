# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['mywatchseries.fun']
            self.base_link = 'https://mywatchseries.fun'
            self.search_link = '/search/%s'
        except Exception:
            #log_utils.log('__init__', 1)
            return

https://www.watchseriesz.com/movies
https://www.mywatchseries.fun/tv-series


# Might have blockage.

# Might be buggy or needing more work, getting sleepy and sloppy lol.


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            search_title = cleantitle.get_dash(tvshowtitle)
            check1_title = '%s (%s)' % (tvshowtitle, year)
            check1_title = cleantitle.get_dash(check1_title)
            check2_title = cleantitle.get_dash(tvshowtitle)
            link = self.base_link + self.search_link % search_title
            html = client.request(link)
            regex = 'class="film-poster-img lazyload"> <a href=(.+?) title="(.+?)" class="film-poster-ahref flw-item-tip">'
            results = re.compile(regex).findall(html)
            for result_url, result_title in results:
                if check1_title == cleantitle.get_dash(result_title):
                    return result_url
                elif check2_title == cleantitle.get_dash(result_title):
                    return result_url
            return
        except:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            #log_utils.log('Scraper episode starting url: \n' + repr(url))
            result_html = client.request(url)
            search_url = '-season-%s-episode-%s/' % (season, episode)
            results = client.parseDOM(result_html, 'a', ret='href')
            result_url = [i for i in results if search_url in i][0]
            return result_url
        except:
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            #log_utils.log('Scraper sources starting url: \n' + repr(url))
            html = client.request(url)
            try:
                links = client.parseDOM(html, 'iframe', ret='src')
                for link in links:
                    if 'disableadblock.com' in link:
                        continue
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
            except:
                #log_utils.log('sources', 1)
                pass
            try:
                try:
                    ext_links = client.parseDOM(html, 'ul', attrs={'id': 'video-links'})[0]
                except:
                    ext_links = client.parseDOM(html, 'ul', attrs={'id': 'videolinks'})[0]
                links = client.parseDOM(ext_links, 'a', ret='href')
                for link in links:
                    host = re.findall('/open/link/.+?/(.+?)/', link)[0]
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if valid:
                        link = self.base_link + link
                        self.results.append({'source': host, 'quality': 'SD', 'url': link, 'direct': False})
            except:
                #log_utils.log('sources', 1)
                pass
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        if any(x in url for x in self.domains):
            html = client.request(url)
            try:
                link = client.parseDOM(html, 'iframe', ret='src')[0]
                return link
            except:
                match = re.compile(r'href=(/open/site/.+?)>', re.I|re.S).findall(page)[0]
                link = self.base_link + match
                link = client.request(link, output='geturl')
                return link
        else:
            return url


