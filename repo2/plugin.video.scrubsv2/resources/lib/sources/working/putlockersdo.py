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
            self.domains = ['putlockers.do']
            self.base_link = 'https://www.putlockers.do'
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
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            episode_check = 'Episode %s' % episode
            episode_check = cleantitle.get_plus(episode_check)
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            search = '%s Season %s' % (title, season) if 'tvshowtitle' in data else title
            url = self.base_link + self.search_link % cleantitle.get_utf8(search)
            r = client.scrapePage(url).text
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='cid'), client.parseDOM(r, 'a', ret='title'))
            if 'tvshowtitle' in data:
                r = [(i[0], i[1], re.findall('(.*?)\s+-\s+Season\s+(\d)', i[1])) for i in r]
                r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
                url = [i[0] for i in r if cleantitle.match_alias(i[2][0], aliases) and i[2][1] == season][0]
            else:
                r = [(i[0], i[1]) for i in r]
                url = [i[0] for i in r if cleantitle.match_alias(i[1], aliases)][0]
            if url == None:
                raise Exception()
            url = self.base_link + url
            r = client.scrapePage(url).text
            r = client.parseDOM(r, 'div', attrs={'class': 'les-content'})
            if 'tvshowtitle' in data:
                r = zip(client.parseDOM(r, 'a', ret='data-file'), client.parseDOM(r, 'a', ret='title'))
                r = [(i[0], i[1]) for i in r]
                links = [i[0] for i in r if (episode_check == cleantitle.get_plus(i[1]) or cleantitle.get_plus(i[1]).startswith(episode_check+'+'))]
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


