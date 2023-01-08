# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
#from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['tubitv.com']
            self.base_link = 'https://tubitv.com'
            self.search_link = 'https://www.google.com/search?q=%s+%s+site:tubitv.com'
        except Exception:
            #log_utils.log('__init__', 1)
            return


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
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
            html = client.request(search_url)
            results = re.findall('<a href="(.+?)"><h3(.+?)</h3>', html)
            results = [(i[0], i[1]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i[0] for i in results if check_title in cleantitle.get_plus(i[1])][0]
            result_url = re.compile('q=(.+?)&amp', re.DOTALL).findall(result)[0]
            result_url = result_url.replace('/movies/', '/embed/')
            result_html = client.request(result_url)
            video_resources = re.compile('"video_resources":\[(.+?)\],', re.DOTALL).findall(result_html)[0]
            video_links = re.compile('{"url":"(.+?)",', re.DOTALL).findall(video_resources)
            for link in video_links:
                if 'adrise.tv' in link:
                    continue
                link = link.replace('\\u002F', '/')
                link += '|%s' % urlencode({'Referer': result_url})
                self.results.append({'source': 'Direct', 'quality': '720p', 'url': link, 'direct': True})
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


