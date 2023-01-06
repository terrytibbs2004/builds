# -*- coding: utf-8 -*-

import re
import requests

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['spacemov.site']
        self.base_link = 'https://spacemov.site'
        self.search_link = '/?s=%s'
        self.ajax_link = '/wp-admin/admin-ajax.php'
        self.session = requests.Session()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('tvshow', 1)
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
            log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['year']
            search_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            search_url = self.base_link + self.search_link % search_title
            html = client.scrapePage(search_url).text
            results = client.parseDOM(html, 'div', attrs={'class': 'result-item'})
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'img', ret='alt'), client.parseDOM(i, 'span', attrs={'class': 'year'})) for i in results]
            results = [(i[0][0], i[1][0], i[2][0]) for i in results if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            result_url = [i[0] for i in results if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            if 'tvshowtitle' in data:
                check = '-%sx%s' % (season, episode)
                html = client.scrapePage(result_url).text
                results = client.parseDOM(html, 'div', attrs={'class': 'episodiotitle'})
                results = [(client.parseDOM(i, 'a', ret='href')) for i in results]
                result_url = [i[0] for i in results if check in i[0]][0]
            html = client.scrapePage(result_url).text
            #try: # returns youtube and hlspanel sources.
                #links = client.parseDOM(html, 'iframe', ret='src')
                #for link in links:
                    #if 'youtube.com' in link:
                        #continue
                    #for source in scrape_sources.process(hostDict, link):
                        #self.results.append(source)
            #except:
                #log_utils.log('sources', 1)
                #pass
            try:
                customheaders = {
                    'Host': self.domains[0],
                    'Accept': '*/*',
                    'Origin': self.base_link,
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': client.UserAgent,
                    'Referer': result_url,
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9'
                }
                post_link = self.base_link + self.ajax_link
                results = re.compile("data-type='(.+?)' data-post='(.+?)' data-nume='(.+?)'>", re.DOTALL).findall(html)
                for data_type, data_post, data_nume in results:
                    payload = {'action': 'doo_player_ajax', 'post': data_post, 'nume': data_nume, 'type': data_type}
                    r = self.session.post(post_link, headers=customheaders, data=payload)
                    i = r.json()
                    log_utils.log('Scraper spacemov sources i: ' + repr(i))
                    if not i['type'] == 'iframe':
                        continue
                    p = i['embed_url'].replace('\\', '')
                    for source in scrape_sources.process(hostDict, p):
                        self.results.append(source)
            except:
                log_utils.log('sources', 1)
                pass
            return self.results
        except:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


"""


Scraper Testing - spacemov sources link: 'https://hlspanel.xyz/video/e7e284c40b9e4218421b65d3bf7e47b9'
Scraper Testing - spacemov sources link: 'https://hlspanel.xyz/video/c5d590683c0fa48aee0f85cd43261d8a'
# found with the normal iframe try.

"""


