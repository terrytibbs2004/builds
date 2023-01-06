# -*- coding: UTF-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

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
            self.domains = ['vexmovies.space']
            self.base_link = 'https://vexmovies.space'
            self.search_link = '/search/%s/feed/rss2/'
        except Exception:
            #log_utils.log('__init__', 1)
            return


# Could most likely scrape the iframe from the search items instead of loading the movie page but it would take away the item check.


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            title = data['title']
            imdb = data['imdb']
            search_url = self.base_link + self.search_link % cleantitle.get_plus(title)
            html = client.scrapePage(search_url).text
            items = client.parseDOM(html, 'item')
            r = [(client.parseDOM(i, 'title'), client.parseDOM(i, 'link')) for i in items]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            url = [i[1] for i in r if cleantitle.match_alias(i[0], aliases)][0]
            html = client.scrapePage(url).text
            imdb_check = re.findall(r'imdb.com/title/(.+?)/"', html)[0]
            if not imdb_check == imdb:
                return self.results
            links = client.parseDOM(html, 'iframe', ret='src')
            for link in links:
                if 'youtube.com' in link:
                    continue
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


