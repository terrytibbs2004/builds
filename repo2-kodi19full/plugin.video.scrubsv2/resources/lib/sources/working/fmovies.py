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
            self.domains = ['fmovies.vision', 'gostream.cool']
            self.base_link = 'https://fmovies.vision'
            self.search_link = '/index.php?do=search&filter=true'
        except Exception:
            #log_utils.log('__init__', 1)
            return


#https://123movies-free.live/
# possible sister site.


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            search_url = self.base_link + self.search_link
            post = ('do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s' % cleantitle.get_utf8(title))
            html = client.request(search_url, post=post).replace('\n', '')
            r = client.parseDOM(html, 'div', attrs={'class': 'item'})
            r = [(client.parseDOM(i, 'a', attrs={'class': 'poster'}, ret='href'), client.parseDOM(i, 'img', ret='alt'), re.findall('<div class="meta">(\d{4}) <i class="dot">', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year)][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url)
            links = []
            try:
                links += client.parseDOM(html, 'div', ret='data-link')
            except:
                #log_utils.log('sources', 1)
                pass
            try:
                iframe_url = client.parseDOM(html, 'iframe', ret='src')[0]
                iframe_html = client.request(iframe_url)
                links += client.parseDOM(iframe_html, 'li', ret='data-link')
            except:
                #log_utils.log('sources', 1)
                pass
            try:
                script_url = re.compile('<script src="(https://simplemovie.xyz/.+?)"').findall(html)[0]
                script_html = client.request(script_url).replace("\\", "")
                links += re.compile('''<tr onclick="window\.open\( \\'(.+?)\\' \)">''').findall(script_html)
            except:
                #log_utils.log('sources', 1)
                pass
            for link in links:
                try:
                    if link.endswith('voe.sx/e/') or link.endswith('voe.sx/'):
                        continue
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
                except:
                    #log_utils.log('sources', 1)
                    pass
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


