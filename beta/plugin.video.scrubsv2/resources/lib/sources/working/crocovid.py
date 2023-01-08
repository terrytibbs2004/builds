# -*- coding: utf-8 -*-

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
            self.domains = ['crocovid.com']
            self.base_link = 'https://crocovid.com'
            self.search_link = '/search/?type=title&query=%s'
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
            url = {'imdb': imdb, 'tvshowtitle': tvshowtitle, 'year': year}
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
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            search_term = '%s %s' % (title, hdlr)
            check_term = cleantitle.get(search_term)
            search_url = self.base_link + self.search_link % cleantitle.get_plus(search_term)
            cookie = client.request(self.base_link, output='cookie')
            search_html = client.request(search_url, cookie=cookie)
            search_results = client.parseDOM(search_html, 'div', attrs={'class': 'search-row'})
            search_result = [(client.parseDOM(i, 'a', attrs={'class': 'videoLink'}, ret='href'), client.parseDOM(i, 'a', attrs={'class': 'videoLink'}, ret='title')) for i in search_results]
            search_result = [(i[0][0], i[1][0]) for i in search_result if len(i[0]) > 0 and len(i[1]) > 0]
            results_found = [(i[0], i[1]) for i in search_result if check_term in cleantitle.get(i[1])]
            for result_found in results_found:
                try:
                    result_url = self.base_link + result_found[0]
                    link = client.request(result_url, cookie=cookie, output='geturl')
                    if not link or 'mcafee.com' in link: # might be different elsewhere, could try to filter out that dead host sooner.
                        continue
                    for source in scrape_sources.process(hostDict, link, info=result_found[1]):
                        self.results.append(source)
                except:
                    #log_utils.log('sources', 1)
                    pass
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


