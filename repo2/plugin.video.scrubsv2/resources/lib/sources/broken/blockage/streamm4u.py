# -*- coding: utf-8 -*-

import requests

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
            self.domains = ['streamm4u.com']
            self.base_link = 'https://streamm4u.com'
            self.search_link = '/search/%s'
            self.ajax_link = '/anhjax'
            self.session = requests.Session()
            self.cookie = client.request(self.base_link, output='cookie', timeout='5')
        except Exception:
            log_utils.log('__init__', 1)
            return


# Has Shows but havent taken the time to code it in.


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.geturl(title)
            check_term = '%s (%s) StreamM4u M4uFree' % (title, year)
            check_title = cleantitle.get_plus(check_term)
            search_url = self.base_link + self.search_link % movie_title
            html = client.request(search_url, cookie=self.cookie)
            r = client.parseDOM(html, 'div', attrs={'class': 'col-xl-2 col-lg-3 col-md-4 col-sm-4 col-6'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get_plus(i[1])][0]
            return url
        except Exception:
            log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url, cookie=self.cookie)
            post_link = self.base_link + self.ajax_link
            token = client.parseDOM(html, 'meta', attrs={'name': 'csrf-token'}, ret='content')[0]
            results = client.parseDOM(html, 'span', ret='data')
            for result in results:
                payload = {'url': post_link, '_token': token, 'm4u': result}
                r = self.session.post(post_link, data=payload)
                i = client.replaceHTMLCodes(r.text)
                p = client.parseDOM(i, 'iframe', ret='src')[0]
                for source in scrape_sources.process(hostDict, p):
                    self.results.append(source)
            return self.results
        except:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


"""


Scraper Testing - streamm4u sources link: 'https://play.playm4u.xyz/play/v1/5f3b10264d6f1d25eb2ccd1e?caption=http://subsubforme.xyz/sub/sub/d6b91d11b8c89d18cec23ab0f6a3c660.srt'
Scraper Testing - streamm4u sources link: 'https://play.playm4u.xyz/play/v1/5f34fa6a1a8d091d9d6cc7b9?caption=http://subsubforme.xyz/sub/sub/356ad156b098113385104f205672d72a.srt'
# gets blocked for me but maybe someone else can scrape it?


"""


