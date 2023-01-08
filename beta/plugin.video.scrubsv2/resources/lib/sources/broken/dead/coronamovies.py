# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import googlestream
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['coronamovies.net']
            self.base_link = 'https://coronamovies.net'
            self.search_link = '/?s=%s'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            movie_link = self.base_link + self.search_link % movie_title
            r = client.scrapePage(movie_link).text
            r = client.parseDOM(r, 'strong', attrs={'class': 'mr-auto'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a'), re.findall('(\d{4})', i)) for i in r]
            r = [(i[0][0], i[1][0].split('<span')[0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.scrapePage(url).text
            links = re.compile("setMp4Source\(\'(.+?)\',", re.DOTALL).findall(html)
            for link in links:
                if 'googleusercontent' in link:
                    try:
                        quality = googlestream.googletag(link)[0]['quality']
                    except:
                        quality = 'SD'
                    link += '|%s' % urlencode({'Referer': url})
                    self.results.append({'source': 'gvideo', 'quality': quality, 'url': link, 'direct': True})
                else:
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


