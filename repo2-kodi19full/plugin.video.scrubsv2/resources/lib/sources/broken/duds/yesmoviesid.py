# -*- coding: utf-8 -*-

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
        try:
            self.results = []
            self.domains = ['yesmovies.id']
            self.base_link = 'https://yesmovies.id'
            self.search_link = 'https://www.google.com/search?q=%s+site:yesmovies.id'
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
            if tvshowtitle == 'House':
                tvshowtitle = 'House M.D.'
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
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
            search_term = '%s season %s' % (title, data['season']) if 'tvshowtitle' in data else '%s %s' % (title, data['year'])
            check_term = '%s season %s' % (title, data['season']) if 'tvshowtitle' in data else '%s (%s)' % (title, data['year'])
            search_title = cleantitle.get_plus(search_term)
            check_title = cleantitle.get_dash(check_term)
            search_url = self.search_link % search_title
            html = client.scrapePage(search_url).text
            results = re.findall('<a href="(.+?)"><h3(.+?)</h3>', html)
            results = [(i[0], i[1]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i[0] for i in results if check_title in cleantitle.get_dash(i[1])][0]
            result_url = re.compile('q=(.+?)&amp', re.DOTALL).findall(result)[0]
            if 'tvshowtitle' in data:
                result_url = result_url + '/watching.html?ep=%s' % data['episode']
            else:
                result_url = result_url + '/watching.html?ep=0'
            result_html = client.scrapePage(result_url).text
            links = client.parseDOM(result_html, 'li', ret='data-video')
            for link in links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


