# -*- coding: UTF-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import scrape_sources
from resources.lib.modules import source_utils
#from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['vumoo.to']
            self.base_link = 'https://vumoo.to'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            if tvshowtitle == 'House':
                tvshowtitle = 'House M.D.'
            url = {'imdb': imdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except Exception:
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
            year = data['year']
            search_title = cleantitle.geturl(title)
            se_check = 's%02de%02d' % (int(season), int(episode))
            if 'tvshowtitle' in data:
                search_link = self.base_link + '/tv-series/%s-season-%s/' % (search_title, season)
            else:
                search_link = self.base_link + '/movies/%s-%s/' % (search_title, year)
            html = client.request(search_link)
            links = zip(client.parseDOM(html, 'a', attrs={'class': 'play'}, ret='embedUrl'), client.parseDOM(html, 'a', attrs={'class': 'play'}))
            for link, sinfo in links:
                if 'tvshowtitle' in data:
                    if not se_check == sinfo:
                        continue
                    qual = 'HD'
                else:
                    qual = sinfo
                valid, host = source_utils.is_host_valid(link, hostDict)
                quality, info = source_utils.get_release_quality(link, qual)
                self.results.append({'source': host, 'quality': quality, 'url': link, 'info': info, 'direct': True})
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        try:
            html = client.request(url, referer=self.base_link)
            link = re.compile(client.regex_pattern6).findall(html)[0]
            link = "https:" + link if link.startswith('//') else link
            link += '|%s' % urlencode({'Referer': url})
            return link
        except Exception:
            #log_utils.log('resolve', 1)
            return url


