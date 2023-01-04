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
            self.domains = ['putlocker.unblockit.page', 'putlocker.unblockit.nz']
            self.base_link = 'https://putlocker.unblockit.page'
            self.search_link = '/search/%s/'
        except Exception:
            #log_utils.log('__init__', 1)
            return


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
            if url is None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.geturl(title)
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            query1 = '%s-season-%s' % (title, season) if 'tvshowtitle' in data else title
            query2 = '%s-%s-season-%s' % (title, year, season) if 'tvshowtitle' in data else '%s-%s' % (title, year)
            check1 = cleantitle.get(query1)
            check2 = cleantitle.get(query2)
            url = self.base_link + self.search_link % (query1.replace('-', '+'))
            self.cookie = client.request(self.base_link, output='cookie', timeout='5')
            html = client.request(url, cookie=self.cookie)
            results = client.parseDOM(html, 'div', attrs={'class': 'ml-item'})
            results = [(client.parseDOM(i, 'a', ret='cid')[0], client.parseDOM(i, 'a', ret='title')[0]) for i in results]
            try:
                url = [i[0] for i in results if check1 == cleantitle.get(i[1])][0]
            except:
                url = [i[0] for i in results if check2 == cleantitle.get(i[1])][0]
            url = self.base_link + url
            r = client.request(url, cookie=self.cookie)
            check_year = re.findall('Release:</strong>.+?/released/(\d+)/', r)[0]
            check_year = cleantitle.match_year(check_year, year, data['year'])
            if not check_year:
                return self.results
            r = client.parseDOM(r, 'div', attrs={'class': 'les-content'})
            if 'tvshowtitle' in data:
                check_epi1 = 'Episode %s' % episode
                check_epi2 = 'Episode %s:' % episode
                try:
                    results = zip(client.parseDOM(r, 'a', ret='title'), client.parseDOM(r, 'a', ret='data-file'))
                    links = [i[1] for i in results if (check_epi1 == i[0] or check_epi2 in i[0])]
                except:
                    links = client.parseDOM(r, 'a', attrs={'title': check_epi1}, ret='data-file')
            else:
                links = client.parseDOM(r, 'a', ret='data-file')
            for link in links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


