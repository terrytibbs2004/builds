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
            self.domains = ['hollymoviehd.cc']
            self.base_link = 'https://hollymoviehd.cc'
            self.search_link = '/?s=%s'
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
            search = '%s Season %s' % (title, season) if 'tvshowtitle' in data else title
            search_url = self.base_link + self.search_link % cleantitle.get_plus(search)
            r = client.request(search_url)
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            if 'tvshowtitle' in data:
                r = [(i[0], re.findall('(.+?) Season (\d+)', i[1])) for i in r]
                r = [(i[0], i[1][0]) for i in r if len(i[1]) > 0]
                url = [i[0] for i in r if cleantitle.match_alias(i[1][0], aliases) and i[1][1] == season][0]
                url = url.replace('/series/', '/episode/')
                url = url[:-1] if url.endswith('/') else url
                url = url + '-episode-%s/' % episode
            else:
                results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
                try:
                    r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
                    url = [i[0] for i in r if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year)][0]
                except:
                    url = [i[0] for i in results if cleantitle.match_alias(i[1], aliases)][0]
            html = client.request(url)
            links = client.parseDOM(html, 'a', attrs={'target': '_blank'}, ret='href')
            for link in links:
                if 'facebook.com' in link or 'imdb.com' in link or link == '#':
                    continue
                elif 'getlinkstream.xyz' in link or 'novastream.cloud' in link:
                    html = client.request(link)
                    vlinks = client.parseDOM(html, 'a', ret='href')
                    for vlink in vlinks:
                        for source in scrape_sources.process(hostDict, vlink):
                            self.results.append(source)
                else:
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


