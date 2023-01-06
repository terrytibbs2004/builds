# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['watchseries.cyou']
            self.base_link = 'https://www.watchseries.cyou'
            self.search_link = '/search/%s'
            self.cookie = client.request(self.base_link, output='cookie', timeout='5')
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
            search_title = cleantitle.get_dash(title)
            check_term = '%s (%s)' % (title, data['year'])
            check_title = cleantitle.get(title) if 'tvshowtitle' in data else cleantitle.get(check_term)
            check = 'TV' if 'tvshowtitle' in data else data['year']
            search_link = self.base_link + self.search_link % search_title
            html = client.request(search_link, cookie=self.cookie)
            results = client.parseDOM(html, 'div', attrs={'class': 'flw-item'})
            if 'tvshowtitle' in data:
                regex = '<span class="float-right fdi-type">(.+?)</span>'
            else:
                regex = '>(\d{4})</span>'
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall(regex, i)) for i in results]
            results = [(i[0][0], i[1][0], i[2][0]) for i in results if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            result_url = [i[0] for i in results if check_title == cleantitle.get(i[1]) and check == i[2]][0]
            if 'tvshowtitle' in data:
                season = data['season']
                episode = data['episode']
                result_url = result_url[:-1]
                result_url = result_url + '-season-%s-episode-%s/' % (season, episode)
            html = client.request(result_url, cookie=self.cookie)
            try:
                links = client.parseDOM(html, 'iframe', ret='src')
                for link in links:
                    if any(i in link for i in ['disableadblock.com', 'youtube.com']):
                        continue
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
            except:
                #log_utils.log('sources', 1)
                pass
            try:
                ext_links = client.parseDOM(html, 'ul', attrs={'id': 'videolinks'})[0]
                links = client.parseDOM(ext_links, 'a', ret='href')
                for link in links:
                    link = self.base_link + link
                    host = re.findall('/open/link/.+?/(.+?)/', link)[0]
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if valid:
                        self.results.append({'source': host, 'quality': 'SD', 'url': link, 'direct': False})
            except:
                #log_utils.log('sources', 1)
                pass
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        if any(x in url for x in self.domains):
            html = client.request(url, cookie=self.cookie)
            try:
                link = client.parseDOM(html, 'iframe', ret='src')[0]
                return link
            except:
                match = re.compile(r'href=(/open/site/.+?)>', re.I|re.S).findall(page)[0]
                link = self.base_link + match
                link = client.request(link, output='geturl')
                return link
        else:
            return url


