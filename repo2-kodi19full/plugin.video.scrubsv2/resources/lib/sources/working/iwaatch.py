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
        self.results = []
        self.domains = ['iwaatch.com']
        self.base_link = 'https://iwaatch.com'
        self.search_link = '/?q=%s'


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
            if url is None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            title = data['title']
            year = data['year']
            search_url = self.base_link + self.search_link % cleantitle.get_plus(title)
            html = client.scrapePage(search_url).text
            r = client.parseDOM(html, 'div', attrs={'class': 'col-xs-12 col-sm-6 col-md-3 '})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'div', attrs={'class': 'post-title'})) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i[0] for i in r if cleantitle.match_alias(i[1], aliases)][0]
            url = result.replace('/movie/', '/view/')
            html = client.scrapePage(url).text
            sources = re.findall(r'sources:.+?\[(.+?)\]', html, re.S)[0]
            links = re.findall(r'(?:file|src)\s*(?:\:)\s*(?:\"|\')(.+?)(?:\"|\')', sources)
            for link in links:
                link = "https:" + link if link.startswith('//') else link
                quality, info = source_utils.get_release_quality(link, link)
                link = link + '|Referer=%s' % url
                self.results.append({'source': 'Direct', 'quality': quality, 'info': info, 'url': link, 'direct': True})
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


