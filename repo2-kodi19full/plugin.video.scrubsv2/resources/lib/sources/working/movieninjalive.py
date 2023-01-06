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
        self.domains = ['movieninja.live']
        self.base_link = 'https://movieninja.live'
        self.search_link = '/search/%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('tvshow', 1)
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
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            check = 'TV' if 'tvshowtitle' in data else data['year']
            link = self.base_link + self.search_link % cleantitle.get_dash(title)
            html = client.scrapePage(link).text
            results = client.parseDOM(html, 'div', attrs={'class': 'flw-item'})
            if 'tvshowtitle' in data:
                regex = '<span class="float-right fdi-type">(.+?)</span>'
            else:
                regex = '<span class="fdi-item">(\d{4})</span>'
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall(regex, i)) for i in results]
            results = [(i[0][0], i[1][0], i[2][0]) for i in results if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            result = [i[0] for i in results if cleantitle.match_alias(i[1], aliases) and check == i[2]][0]
            link = self.base_link + result
            if 'tvshowtitle' in data:
                season = data['season']
                episode = data['episode']
                html = client.scrapePage(link).text
                regex = 'data-number="%s".+?data-s-number="%s".+?href="(.+?)"' % (episode, season)
                result = re.compile(regex, re.DOTALL).findall(html)[0]
                link = self.base_link + result
            html = client.scrapePage(link).text
            links = client.parseDOM(html, 'iframe', ret='src')
            for link in links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


