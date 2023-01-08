# -*- coding: utf-8 -*-

import re
import requests

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
            self.domains = ['bluray7.com']
            self.base_link = 'https://bluray7.com'
            self.search_link = '/search/%s/feed/rss2/'
            self.ajax_link = '/wp-admin/admin-ajax.php'
            self.session = requests.Session()
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
            search_url = self.base_link + self.search_link % cleantitle.get_plus(title)
            html = client.request(search_url)
            items = client.parseDOM(html, 'item')
            r = [(client.parseDOM(i, 'link'), client.parseDOM(i, 'title')) for i in items]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], re.findall('(.+?)(?:\((\d{4}))', i[1])) for i in r]
            r = [(i[0], i[1][0]) for i in r if len(i[1]) > 0]
            url = [i[0] for i in r if cleantitle.match_alias(i[1][0], aliases) and cleantitle.match_year(i[1][1], year)][0]
            html = client.request(url)
            try:
                qual = client.parseDOM(html, 'strong', attrs={'class': 'quality'})[0]
            except:
                qual = 'SD'
            customheaders = {
                'Host': self.domains[0],
                'Accept': '*/*',
                'Origin': self.base_link,
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': client.UserAgent,
                'Referer': url,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            post_link = self.base_link + self.ajax_link
            results = re.compile("data-type='(.+?)' data-post='(.+?)' data-nume='(\d+)'>", re.DOTALL).findall(html)
            for data_type, data_post, data_nume in results:
                try:
                    payload = {'action': 'doo_player_ajax', 'post': data_post, 'nume': data_nume, 'type': data_type}
                    r = self.session.post(post_link, headers=customheaders, data=payload)
                    i = r.json()
                    if not i['type'] == 'iframe':
                        continue
                    p = i['embed_url'].replace('\\', '')
                    for source in scrape_sources.process(hostDict, p, info=qual):
                        self.results.append(source)
                except:
                    pass
            tbody = client.parseDOM(html, 'tbody')
            downloads = client.parseDOM(tbody, 'a', ret='href')
            for download in downloads:
                try:
                    html = client.request(download)
                    link = client.parseDOM(html, 'a', attrs={'id': 'link'}, ret='href')[0]
                    for source in scrape_sources.process(hostDict, link, info=qual):
                        self.results.append(source)
                except:
                    pass
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


