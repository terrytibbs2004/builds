# -*- coding: utf-8 -*-

import re

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['imdbbox.com']
        self.base_link = 'https://imdbbox.com'
        self.search_link = '/search.html?keyword=%s'


# Sites Shitty So Ditched.


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            movie_link = self.base_link + self.search_link % movie_title
            r = client.request(movie_link, timeout='10')
            r = client.parseDOM(r, 'div', attrs={'class': 'card bg-default'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('(\d{4})', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            url = self.base_link + url
            return url
        except Exception:
            log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except Exception:
            log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            episode_title = cleantitle.geturl(title)
            url = self.base_link + '/videos/%s-season-%s-episode-%s-%s' % (url, season, episode, episode_title)
            return url
        except Exception:
            log_utils.log('episode', 1)
            return


#https://imdbbox.com/videos/seal-team-season-1-episode-22-the-cost-of-doing-business


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            page_html = client.request(url, timeout='10')
            results = client.parseDOM(page_html, 'iframe', ret='src')
            for result in results:
                result_url = self.base_link + result
                log_utils.log('Scraper Testing sources result_url: ' + repr(result_url))
                result_html = client.request(result_url, timeout='10')
                result_links = client.parseDOM(result_html, 'a', ret='href')
                for result_link in result_links:
                    if 'download.php' in result_link:
                        continue
                    link = self.base_link + result_link
                    log_utils.log('Scraper Testing sources link: ' + repr(link))
                    html = client.request(link, timeout='10')
                    links = client.parseDOM(html, 'iframe', ret='src')
                    for link in links:
                        log_utils.log('Scraper Testing sources iframe link: ' + repr(link))
                        links = self.scrape_proxy_sources(link)
                        for link in links:
                            log_utils.log('Scraper Testing sources final link: ' + repr(link))
                        #for source in scrape_sources.process(hostDict, link):
                            #self.results.append(source)
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def scrape_proxy_sources(self, url):
        try:
            results = []
            if url == None:
                return results
            log_utils.log('Scraper Testing scrape_proxy_sources starting url: ' + repr(url))
            if 'player.php' in url:
                link = self.base_link + url
                html = client.request(link, timeout='10')
                iframes = client.parseDOM(html, 'iframe', ret='src')
                for iframe in iframes:
                    #link = self.base_link + link if not link.startswith('http') else link
                    log_utils.log('Scraper Testing scrape_proxy_sources player.php iframe link: ' + repr(iframe))
                    results.append(iframe)
            if 'proxy.php' in url:
                link = self.base_link + url
                html = client.request(link, timeout='10')
                unpacked = client.unpacked(html)
                log_utils.log('Scraper Testing scrape_proxy_sources proxy.php unpacked: ' + repr(unpacked))
                regex = r'''\{\s*file:\s*"(.+?)",'''
                files = re.compile(regex).findall(unpacked)
                log_utils.log('Scraper Testing scrape_proxy_sources proxy.php links: ' + repr(files))
                for file in files:
                    #link = self.base_link + link if not link.startswith('http') else link
                    log_utils.log('Scraper Testing scrape_proxy_sources proxy.php file link: ' + repr(file))
                    results.append(file)
            return results
        except Exception:
            log_utils.log('scrape_proxy_sources', 1)
            return results


    def resolve(self, url):
        return url


"""
<a class="dropdown-item item-server" href="/proxy/player.php?id=MTgwNTY4">Main Server</a>
<a class="dropdown-item item-server" href="/proxy/player.php?id=MTgwNTY4&server=2">Mirror Server</a>
<a class="dropdown-item item-server" href="/proxy/download.php?id=MTgwNTY4" target="_blank">Downloads</a>
"""


