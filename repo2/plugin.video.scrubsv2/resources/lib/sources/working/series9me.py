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
            self.domains = ['series9.la', 'series9.me']
            self.base_link = 'https://series9.la'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvshowtitle': tvshowtitle, 'year': year}
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
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            search_title = cleantitle.geturl(title)
            if 'tvshowtitle' in data:
                search_link = self.base_link + '/film/%s-season-%s/watching.html?ep=%s' % (search_title, season, episode)
            else:
                search_link = self.base_link + '/film/%s/watching.html?ep=0' % search_title
            result_html = client.scrapePage(search_link).text
            check_year = re.findall('Release:</strong>\s*(\d+)</p>', result_html)[0]
            check_year = cleantitle.match_year(check_year, year, data['year'])
            if not check_year:
                return self.results
            check_epi1 = 'Episode %s ' % episode
            check_epi2 = 'Episode %s:' % episode
            if 'tvshowtitle' in data:
                try:
                    results = zip(client.parseDOM(result_html, 'a', ret='title'), client.parseDOM(result_html, 'a', ret='player-data'))
                    links = [i[1] for i in results if (check_epi1 in i[0] or check_epi2 in i[0])]
                except:
                    links = client.parseDOM(result_html, 'a', attrs={'episode-data': episode}, ret='player-data')
            else:
                links = client.parseDOM(result_html, 'a', ret='player-data')
            for link in links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


