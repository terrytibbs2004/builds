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
            self.domains = ['losmovies.online', 'losmovies.website', 'losmovies.click', 'losmovies.today', 'losmovies.life']
            self.base_link = 'https://losmovies.online'
            self.search_link = '/display-results?type=movies&q=%s'
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
            if url == None:
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
            search_title = cleantitle.get_plus(title)
            check_title = cleantitle.get_under(title)
            check = '%s_%s' % (check_title, data['year'])
            link = self.base_link + self.search_link % search_title
            html = client.scrapePage(link).text
            results = client.parseDOM(html, 'div', attrs={'class': 'showRow showRowImage showRowImage'})
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='src')) for i in results]
            results = [(i[0][0], i[1][0]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i[0] for i in results if check in i[1]][0]
            link = self.base_link + result
            html = client.scrapePage(link).text
            if 'tvshowtitle' in data:
                season = data['season']
                episode = data['episode']
                regex = '<td class="linkHidden linkHiddenUrl" data-width="700" data-height="460" data-season="%s" data-serie="%s">(.+?)</td>' % (season, episode)
                links = re.compile(regex, re.DOTALL).findall(html)
            else:
                #regex = '<td class="linkHidden linkHiddenUrl" data-width="700" data-height="460" data-season=".+?" data-serie=".+?">(.+?)</td>'
                links = client.parseDOM(html, 'td', attrs={'class': 'linkHidden linkHiddenUrl'})
            for link in links:
                if 'https://eplayvid.com/watch/%s' in link:
                    continue # this was add imdb but fails. and the sites dead with .net not working with this link either.
                if any(i in link for i in ['1movietv.com', '123files.club', 'dbgo.fun', 'vidsrc.me', '2embed.ru']):
                    continue
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


