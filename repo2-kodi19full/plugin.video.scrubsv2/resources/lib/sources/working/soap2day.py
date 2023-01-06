# -*- coding: UTF-8 -*-

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
            self.domains = ['soap2day.app']
            self.base_link = 'https://ww1.soap2day.app'
            self.search_link = '/search?term=%s'
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
            if url is None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            url = self.base_link + self.search_link % cleantitle.get_utf8(title)
            html = client.scrapePage(url).text
            results = client.parseDOM(html, 'li', attrs={'rel': 'tooltip'})
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt'), re.findall('-\s*(\d{4})\s*</h4>', i)) for i in results]
            results = [(i[0][0], client.replaceHTMLCodes(i[1][0]), i[2][0]) for i in results if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in results if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year, data['year'])][0]
            if 'tvshowtitle' in data:
                check_season = 'season-%s' % season
                html = client.scrapePage(url).text
                results = client.parseDOM(html, 'li', attrs={'class': 'child_season'})
                seasons = client.parseDOM(html, 'a', ret='href')
                url = [i for i in seasons if i.endswith(check_season)][0]
                check_episode = 'episode-%s' % episode
                html = client.scrapePage(url).text
                results = client.parseDOM(html, 'li', attrs={'class': 'child_episode'})
                episodes = client.parseDOM(html, 'a', ret='href')
                url = [i for i in episodes if i.endswith(check_episode)][0]
            html = client.scrapePage(url).text
            links = client.parseDOM(html, 'div', ret='data-link')
            for link in links:
                html = client.scrapePage(link).text
                link = client.parseDOM(html, 'iframe', ret='src')[0]
                link = client.replaceHTMLCodes(link)
                if '/play/' in link:
                    html = client.scrapePage(link).text
                    link = client.parseDOM(html, 'source', ret='src')[0]
                    link = client.replaceHTMLCodes(link)
                link = client.request(link, timeout='6', output='geturl')
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


