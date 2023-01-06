# -*- coding: UTF-8 -*-

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
            self.genre_filter = ['animation', 'anime']
            self.domains = ['animeshow.tv']
            self.base_link = 'https://animeshow.tv'
            self.search_link = '/find.html?key=%s'
        except Exception:
            #log_utils.log('__init__', 1)
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
            search_url = self.base_link + self.search_link % cleantitle.get_plus(title)
            r = client.request(search_url)
            r = client.parseDOM(r, 'div', attrs={'class': 'genres_result'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'div', attrs={'class': 'genres_result_title'}), client.parseDOM(i, 'div', attrs={'class': 'genres_result_dates'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year, data['year'])][0]
            if 'tvshowtitle' in data:
                url = url[:-1]
                url = url + '-episode-%s' % int(episode)
            mirrors = ['/', '-mirror-2/', '-mirror-3/', '-mirror-4/']
            for mirror in mirrors:
                try:
                    vurl = url + mirror
                    html = client.scrapePage(vurl).text
                    links = client.parseDOM(html, 'iframe', ret='src')
                    for link in links:
                        if not 'http' in link:
                            continue
                        if 'mycrazygifts.com' in link:
                            continue
                        for source in scrape_sources.process(hostDict, link):
                            self.results.append(source)
                except:
                    pass
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


