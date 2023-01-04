# -*- coding: utf-8 -*-

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
            self.domains = ['filmxy.pw', 'filmxy.me', 'filmxy.one', 'filmxy.tv', 'filmxy.live', 'filmxy.cc']
            self.base_link = 'https://www.filmxy.pw'
            self.search_link = 'https://www.google.com/search?q=%s+%s+site:filmxy.pw'
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
            search_title = cleantitle.get_plus(title)
            check_title = '%s+(%s)' % (search_title, year)
            search_url = self.search_link % (search_title, year)
            html = client.scrapePage(search_url).text
            results = re.findall('<a href="(.+?)"><h3(.+?)</h3>', html)
            results = [(i[0], i[1]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i[0] for i in results if check_title in cleantitle.get_plus(i[1])][0]
            result_url = re.compile('q=(.+?)&amp', re.DOTALL).findall(result)[0]
            result_html = client.scrapePage(result_url).text
            page_results = client.parseDOM(result_html, 'div', attrs={'class': 'video-section'})[0]
            page_urls = client.parseDOM(page_results, 'a', ret='data-player')
            for url in page_urls:
                url = client.replaceHTMLCodes(url)
                url = client.parseDOM(url, 'iframe', ret='src')[0]
                for source in scrape_sources.process(hostDict, url):
                    self.results.append(source)
            page_links = client.parseDOM(page_results, 'a', attrs={'target': '_blank'}, ret='href')
            for link in page_links:
                if any(i in link for i in ['vip-membership', 'rapidvideo.com', 'rapidvid.to', 'openload.co', 'streamango.com', 'streamcherry.com']):
                    continue
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


