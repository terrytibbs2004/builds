# -*- coding: UTF-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['projecfreetv.co']
        self.base_link = 'https://projecfreetv.co'
        self.search_link = '/episode/%s-s%02de%02d/'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            search_title = cleantitle.get_dash(title)
            url = self.base_link + self.search_link % (search_title, int(season), int(episode))
            html = client.scrapePage(url).text
            try: # tvshow year check?
                check_year = client.parseDOM(html, 'div', attrs={'itemprop': 'datePublished'})[0]
            except: # movie year check?
                check_year = client.parseDOM(html, 'span', attrs={'itemprop': 'datePublished'})[0]
            check_year = re.findall('(\d{4})', check_year)[0]
            check_year = cleantitle.match_year(check_year, year, data['year'])
            if not check_year:
                return self.results
            links = re.compile('<a href="(.+?)" .+?>(.+?)<br></a>').findall(html)
            for link1, link2 in links:
                for source in scrape_sources.process(hostDict, link1):
                    self.results.append(source)
                for source in scrape_sources.process(hostDict, link2):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


