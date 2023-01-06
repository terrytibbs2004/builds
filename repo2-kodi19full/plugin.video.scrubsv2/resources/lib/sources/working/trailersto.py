# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import source_utils
#from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['trailers.to']
            self.base_link = 'https://trailers.to'
            self.search_link = '/en/popular/movies-tvshows-collections?q=%s'
            self.embed_search_link = '/player/embed/imdb/%s'
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
            imdb = data['imdb']
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            try: # works ok and finds what the embed doesnt alot but some items seem to fail on play. quality isnt really seen either.
                search_url = self.base_link + self.search_link % cleantitle.get_plus(title)
                r = client.scrapePage(search_url).text
                r = client.parseDOM(r, 'article', attrs={'class': 'tour-modern list-item'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt'), re.findall('-(\d{4})', i)) for i in r]
                r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
                url = [i[0] for i in r if cleantitle.match_alias(i[1], aliases) and cleantitle.match_year(i[2], year, data['year'])][0]
                url = self.base_link + url
                if 'tvshowtitle' in data:
                    sepi = '-season-%1d-episode-%1d-' % (int(season), int(episode))
                    r = client.scrapePage(url).text
                    r = client.parseDOM(r, 'a', attrs={'class': 'tour-modern-figure'}, ret='href')
                    url = [i for i in r if sepi in i][0]
                    url = self.base_link + url
                r = client.scrapePage(url).text
                links = client.parseDOM(r, 'a', attrs={'id': 'download-button'}, ret='href')
                for link in links:
                    link = client.replaceHTMLCodes(link)
                    link = "https:" + link if link.startswith('//') else link
                    quality, info = source_utils.get_release_quality(link, link)
                    link += '|Referer=%s' % self.base_link
                    self.results.append({'source': 'Direct', 'quality': quality, 'info': info, 'url': link, 'direct': True})
            except:
                #log_utils.log('sources', 1)
                pass
            try: # works good and easier but some items dont show a embed option from my tests.
                embed_search_term = '%s/S%1dE%1d' % (imdb, int(season), int(episode)) if 'tvshowtitle' in data else imdb
                embed_search_url = self.base_link + self.embed_search_link % embed_search_term
                r = client.scrapePage(embed_search_url).text
                try:
                    qual = client.parseDOM(r, 'div', attrs={'class': 'video-info'}, ret='title')[0]
                except:
                    qual = 'sd'
                links = client.parseDOM(r, 'source', ret='src')
                for link in links:
                    link = client.replaceHTMLCodes(link)
                    link = "https:" + link if link.startswith('//') else link
                    quality, info = source_utils.get_release_quality(qual, link)
                    link += '|Referer=%s' % self.base_link
                    self.results.append({'source': 'Direct', 'quality': quality, 'info': info, 'url': link, 'direct': True})
            except:
                #log_utils.log('sources', 1)
                pass
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


