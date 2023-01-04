# -*- coding: UTF-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import scrape_sources
from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['xxiku.com']
            self.base_link = 'https://xxiku.com'
            self.search_link = '/search/%s/feed/rss2/'
        except Exception:
            #log_utils.log('__init__', 1)
            return


# Site crashed during my update to the "new" search code lol, gonna have to try again later. Plus FINISH!!!


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
            search_url = self.base_link + self.search_link % cleantitle.get_plus(title)
            self.cookie = client.request(self.base_link, output='cookie', timeout='5')
            r = client.request(search_url, cookie=self.cookie)
            r = client.parseDOM(r, 'item')
            r = [(client.parseDOM(i, 'link'), client.parseDOM(i, 'title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            log_utils.log('Scraper Testing starting r1: \n' + repr(r))
            r = [(i[0], re.findall('(.+?)(?:\((\d{4})\))', i[1])) for i in r]
            log_utils.log('Scraper Testing starting r2: \n' + repr(r))
            r = [(i[0], i[1][0]) for i in r if len(i[1]) > 0]
            log_utils.log('Scraper Testing starting r3: \n' + repr(r))
            url = [i[0] for i in r if cleantitle.match_alias(i[1][0], aliases) and cleantitle.match_year(i[1][1], year)][0]
            log_utils.log('Scraper Testing starting url: \n' + repr(url))
            html = client.request(url, cookie=self.cookie)
            try:
                qual = re.findall('Quality: .+?/quality/.+? rel="tag">(.+?)</a></div>', r)[0]
            except:
                qual = 'SD'
            links = client.parseDOM(html, 'iframe', ret='src')
            for link in links:
                for source in scrape_sources.process(hostDict, link, info=qual):
                    self.results.append(source)
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


