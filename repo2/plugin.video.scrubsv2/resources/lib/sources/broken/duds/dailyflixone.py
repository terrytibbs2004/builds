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
            self.domains = ['main.dailyflix.one']
            self.base_link = 'https://main.dailyflix.one'
            self.search_link = '/?search=%s'
        except Exception:
            #log_utils.log('__init__', 1)
            return


# Could use some more work since results vary due to final page layout.


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
            year = data['year']
            check_item = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else year
            check_term = '%s (%s)' % (title, year)
            search_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title) if 'tvshowtitle' in data else cleantitle.get(check_term)
            search_url = self.base_link + self.search_link % search_title
            search_html = client.scrapePage(search_url).text
            results = re.findall('<a class="link" href="(.+?)">(.+?)</a>', search_html)
            result = [(i[0], i[1]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result_url = [i[0] for i in result if check_title in cleantitle.get(i[1]) and year in i[1]][0]
            html = client.scrapePage(result_url).text
            if 'tvshowtitle' in data:
                posts = client.parseDOM(html, 'div', attrs={'class': 'postlinks'})
                lhtml = [i for i in posts if check_item in i][0]
            links = client.parseDOM(lhtml, 'a', attrs={'class': 'latestnews'}, ret='href')
            if 'tvshowtitle' in data and ('S%02dE%02d' % (int(data['season']), int(data['episode'])-1) or 'S%02dE%02d' % (int(data['season']), int(data['episode'])+1) in lhtml):
                links = [i for i in links if check_item.lower() in i.lower()]
            for link in links:
                if any(i in link for i in [self.domains[0], 'imdb.com', 'javascript', '?t=tv&id=', 'vidlox.me', 'vshare.eu', 'mystream.to']):
                    continue
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


"""


Scraper Testing - dailyflixone sources link: 'https://tor.dailyflix.one/?file=magnet:?xt=urn:btih:f2dc7e714b53bde62069e2b7c8cc6c7cb4d6ce97&amp;dn=The.Batman.2022.HDTS.850MB.c1nem4.x264-SUNSCREEN%5BTGx%5D'
# temp save to show this scraper has a torr result.


"""


