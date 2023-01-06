# -*- coding: utf-8 -*-

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
            self.domains = ['realtalksociety.com']
            self.base_link = 'https://realtalksociety.com'
            self.search_link = '/?search=%s'
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
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            check1 = '%s s%02de%02d' % (title, int(season), int(episode)) if 'tvshowtitle' in data else '%s %s' % (title, year)
            check2 = '%s Season %s Episode %s' % (title, season, episode) if 'tvshowtitle' in data else '%s %s' % (title, year)
            search_term = '%s s%02de%02d' % (title, int(season), int(episode)) if 'tvshowtitle' in data else title
            search_url = self.base_link + self.search_link % cleantitle.get_plus(search_term)
            r = client.scrapePage(search_url).text
            r = client.parseDOM(r, 'div', attrs={'class': 'gallerySectionContent'})[0]
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            results = [(i[0], i[1]) for i in r]
            try:
                url = [i[0] for i in results if cleantitle.get(check1) in cleantitle.get(i[1])][0]
            except:
                url = [i[0] for i in results if cleantitle.get(check2) in cleantitle.get(i[1])][0]
            r = client.scrapePage(url).text
            links = client.parseDOM(r, 'source', ret='src')
            for link in links:
                link = "https:" + link if link.startswith('//') else link
                quality, info = source_utils.get_release_quality(link, link)
                link += '|Referer=%s/&User-Agent=iPad' % self.base_link
                self.results.append({'source': 'Direct', 'quality': quality, 'info': info, 'url': link, 'direct': True})
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


