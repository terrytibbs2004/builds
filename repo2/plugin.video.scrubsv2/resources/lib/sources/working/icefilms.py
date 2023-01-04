# -*- coding: utf-8 -*-

import re
import requests

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
            self.domains = ['icefilms.tv']
            self.base_link = 'https://icefilms.tv'
            #self.search_link = '/search/%s/1'
            self.search_link = 'https://www.google.com/search?q=%s+site:icefilms.tv'
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


    """ ### Removed for google search use since google search doesnt seem to find the shows.
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
    """


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
            imdb = data['imdb']
            #url = self.base_link + self.search_link % cleantitle.get_plus(title)
            ### Google search code start..
            check_title = '%s (%s)' % (title, year)
            check_title = cleantitle.get_plus(check_title)
            url = self.search_link % cleantitle.get_plus(title)
            html = client.scrapePage(url).text
            results = re.findall('<a href="(.+?)"><h3(.+?)</h3>', html)
            results = [(i[0], i[1]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i[0] for i in results if check_title in cleantitle.get_plus(i[1])][0]
            url = re.compile('q=(.+?)&amp', re.DOTALL).findall(result)[0]
            ### Google search code ends.
            self.cookie = client.request(self.base_link, output='cookie', timeout='5')
            #r = client.request(url, cookie=self.cookie)
            #r = client.parseDOM(r, 'div', attrs={'class': 'movie'})
            #r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'div', attrs={'class': 'title'}), client.parseDOM(r, 'div', attrs={'class': 'year'}))
            #r = [(i[0], i[1], i[2]) for i in r]
            #url = [i[0] for i in r if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year, data['year'])][0]
            #if url == None:
                #raise Exception()
            #if 'tvshowtitle' in data:
                #url = self.base_link + url + '/season/%s/episode/%s' % (season, episode)
            #else:
                #url = self.base_link + url
            r = client.request(url, cookie=self.cookie)
            customheaders = {'User-Agent': client.UserAgent, 'Referer': url, 'Cookie': self.cookie}
            streams = re.findall("get\('(.+?)', {(.+?)}, function", r)
            for stream, id in streams:
                try:
                    params = '{%s}' % id
                    html = requests.get(self.base_link + stream, headers=customheaders, params=params).text
                    link = client.parseDOM(html, 'iframe', ret='src')[0]
                    link = link + imdb if not imdb in link else link
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
                except:
                    pass
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


