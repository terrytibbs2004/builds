# -*- coding: utf-8 -*-

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.results = []
        self.domains = ['dl3.vaiomusic.org']
        self.base_link = 'http://dl3.vaiomusic.org'
        self.search_link = ['/Movie/', '/Movie1/', '/Movies/1/', '/Animation/']


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['title']
            year = data['year']
            check_title = '%s %s' % (title, year)
            check_title = cleantitle.get(check_title)
            self.cookie = client.request(self.base_link, output='cookie', timeout='5')
            for i in self.search_link:
                try:
                    search_link = self.base_link + i
                    search_html = client.request(search_link, cookie=self.cookie)
                    results = client.parseDOM(search_html, 'tbody')[0]
                    results = client.parseDOM(results, 'td')
                    result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in results]
                    result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
                    page_link = [i[0] for i in result if check_title in cleantitle.get(i[1])][0]
                    link = search_link + page_link
                    quality, info = source_utils.get_release_quality(link, link)
                    link += '|%s' % urlencode({'Referer': search_link})
                    self.results.append({'source': 'Direct', 'quality': quality, 'info': info, 'url': link, 'direct': True})
                except:
                    pass
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


