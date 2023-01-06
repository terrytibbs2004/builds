# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import jsunpack
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.results = []
        self.domains = ['goojara.to', 'supernova.to']
        self.base_link = 'https://goojara.to'
        self.search_link = 'https://www.google.com/search?q=%s+%s+site:goojara.to'
        self.cookie = client.request(self.base_link, output='cookie', timeout='5')


#https://www.goojara.to/

# final links seem to resolve to a 404 page
# should be a simple .url to get the real final link but always fails.


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('tvshow', 1)
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
            log_utils.log('episode', 1)
            return



    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            search_title = cleantitle.get_plus(title)
            if 'tvshowtitle' in data:
                check_title = 'Watch+%s+Season+%s+Episode+%s' % (search_title, data['season'], data['episode'])
            else:
                check_title = '%s+(%s)' % (search_title, year)
            check_title = cleantitle.get_plus(check_title)
            search_url = self.search_link % (search_title, year)
            html = client.scrapePage(search_url).text
            results = re.findall('<a href="(.+?)"><h3(.+?)</h3>', html)
            results = [(i[0], i[1]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i[0] for i in results if check_title in cleantitle.get_plus(i[1])][0]
            result_url = re.compile('q=(.+?)&amp', re.DOTALL).findall(result)[0]
            result_html = client.request(result_url, cookie=self.cookie)
            result_links = re.compile('<a class="bcg" href="(.+?)">(.+?)<span>', re.DOTALL).findall(result_html)
            for link, hoster in result_links:
                valid, host = source_utils.is_host_valid(hoster, hostDict)
                log_utils.log('Scraper Testing sources link: ' + repr(link))
                self.results.append({'source': host, 'quality': 'SD', 'url': link, 'direct': False})
            return self.results
        except:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        try:
            link = client.request(url, output='geturl')
            log_utils.log('Scraper Testing resolve link: ' + repr(link))
            return link
        except:
            log_utils.log('resolve', 1)
            return url


