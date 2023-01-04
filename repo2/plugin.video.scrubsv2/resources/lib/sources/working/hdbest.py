# -*- coding: utf-8 -*-

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
        self.results = []
        self.domains = ['hdbest.net']
        self.base_link = 'https://hdbest.net'
        self.search_link = '/search/%s/feed/rss2/'


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
            year = data['year']
            imdb = data['imdb']
            search_url = self.base_link + self.search_link % cleantitle.get_plus(title)
            html = client.request(search_url)
            r = client.parseDOM(html, 'item')
            r = zip(client.parseDOM(r, 'link'), client.parseDOM(r, 'title'))
            results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
            try:
                r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
                url = [i[0] for i in r if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year)][0]
            except:
                url = [i[0] for i in results if cleantitle.match_alias(i[1], aliases)][0]
            result_html = client.scrapePage(url).text
            result_links = client.parseDOM(result_html, 'iframe', ret='src')
            for link in result_links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


