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
        try:
            self.results = []
            self.domains = ['123moviesfree.so', '123movie.movie']
            self.base_link = 'https://123moviesfree.so'
            self.search_link = '/movie/search/%s'
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
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            search_term = '%s Season %s' % (title, season) if 'tvshowtitle' in data else title
            search_url = self.base_link + self.search_link % cleantitle.geturl(search_term)
            r = client.scrapePage(search_url).text
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            if 'tvshowtitle' in data:
                r = [(i[0], re.findall('(.+?) Season (\d+)$', i[1])) for i in r]
                r = [(i[0], i[1][0]) for i in r if len(i[1]) > 0]
                url = [i[0] for i in r if cleantitle.match_alias(i[1][0], aliases) and i[1][1] == season][0]
                url = self.base_link + '%s/watching.html?ep=%s' % (url, episode)
            else:
                results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
                try:
                    r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
                    url = [i[0] for i in r if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year)][0]
                except:
                    url = [i[0] for i in results if cleantitle.match_alias(i[1], aliases)][0]
                url = self.base_link + '%s/watching.html' % url
            r = client.scrapePage(url).text
            check_year = re.findall('Release:.+?(\d{4})', r)[0]
            check_year = cleantitle.match_year(check_year, year, data['year'])
            if not check_year:
                return self.results
            try:
                qual = client.parseDOM(r, 'span', attrs={'class': 'quality'})[0]
            except:
                qual = 'SD'
            r = client.parseDOM(r, 'div', attrs={'class': 'les-content'})
            if 'tvshowtitle' in data:
                check_epi1 = 'Episode %s ' % episode
                check_epi2 = 'Episode %s:' % episode
                try:
                    results = zip(client.parseDOM(r, 'a', ret='title'), client.parseDOM(r, 'a', ret='player-data'))
                    links = [i[1] for i in results if (check_epi1 in i[0] or check_epi2 in i[0])]
                except:
                    links = client.parseDOM(r, 'a', attrs={'episode-data': episode}, ret='player-data')
            else:
                links = client.parseDOM(r, 'a', ret='player-data')
            for link in links:
                for source in scrape_sources.process(hostDict, link, info=qual):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


