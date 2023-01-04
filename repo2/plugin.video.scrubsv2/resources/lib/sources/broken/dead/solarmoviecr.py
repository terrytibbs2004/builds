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
            self.domains = ['solarmovie.cr']
            self.base_link = 'https://solarmovie.cr'
            self.search_link = 'https://www.google.com/search?q=%s+site:solarmovie.cr'
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


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['title']
            year = data['year']
            search_term = '%s %s' % (title, year)
            check_term = '%s (%s)' % (title, year)
            search_title = cleantitle.get_plus(search_term)
            check_title = cleantitle.get_dash(check_term)
            search_url = self.search_link % search_title
            html = client.scrapePage(search_url).text
            results = re.findall('<a href="(.+?)"><h3(.+?)</h3>', html)
            results = [(i[0], i[1]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i[0] for i in results if check_title in cleantitle.get_dash(i[1])][0]
            result_url = re.compile('q=(.+?)&amp', re.DOTALL).findall(result)[0]
            result_url = result_url + 'watching' if result_url.endswith('/') else '/watching'
            result_html = client.scrapePage(result_url).text
            links = client.parseDOM(result_html, 'a', ret='data-file')
            for link in links:
                if any(i in link for i in ['streamango.com', 'vcstream.to']):
                    continue
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


