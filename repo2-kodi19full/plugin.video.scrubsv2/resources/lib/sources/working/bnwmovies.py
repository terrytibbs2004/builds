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
            self.domains = ['bnwmovies.com']
            self.base_link = 'https://bnwmovies.com'
            self.search_link = '/?s=%s'
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


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            title = data['title']
            year = data['year']
            if int(year) > 1970:
                return self.results
            search_url = self.base_link + self.search_link % cleantitle.get_plus(title)
            search_html = client.scrapePage(search_url).text
            results = client.parseDOM(search_html, 'div', attrs={'class': 'post'})
            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in results]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            page_url = [i[0] for i in result if cleantitle.match_alias(i[1], aliases)][0]
            page_html = client.scrapePage(page_url).text
            links = client.parseDOM(page_html, 'source', ret='src')
            for link in links:
                valid, host = source_utils.is_host_valid(link, hostDict)
                quality, info = source_utils.get_release_quality(link, link)
                link += '|%s' % urlencode({'Referer': page_url})
                self.results.append({'source': host, 'quality': quality, 'url': link, 'info': info, 'direct': True})
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


