# -*- coding: utf-8 -*-

import re

import simplejson as json
from six import ensure_text
from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import googlestream
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['0123movies.li']
        self.base_link = 'https://0123movies.li'
        self.search_link = '/search/%s.html'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            movie_link = self.base_link + self.search_link % movie_title
            r = client.scrapePage(movie_link).text
            r = client.parseDOM(r, 'div', attrs={'class': 'flw-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('>(\d{4})</span>', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1]) and year == i[2]][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            #log_utils.log('tvshow', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            tvshow_title = cleantitle.get_plus(data['tvshowtitle'])
            check_title = cleantitle.get(data['tvshowtitle'])
            tvshow_link = self.base_link + self.search_link % tvshow_title
            r = client.scrapePage(tvshow_link).text
            r = client.parseDOM(r, 'div', attrs={'class': 'flw-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('>(\d{4})</span>', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check_title in cleantitle.get(i[1]) and ('Season %s' % season) in i[1]][0]
            url += '?episode=%01d' % int(episode)
            return url
        except Exception:
            #log_utils.log('episode', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            try:
                url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except:
                episode = None
            ref = url
            result = client.scrapePage(url).text
            if episode:
                result = client.parseDOM(result, 'div', attrs={'id': 'ip_episode'})[0]
                ep_url = client.parseDOM(result, 'a', attrs={'data-name': str(episode)}, ret='href')[0]
                result = client.scrapePage(ep_url).text
            r = client.parseDOM(result, 'div', attrs={'id': 'servers-list'})[0]
            r = client.parseDOM(r, 'li')
            for u in r:
                try:
                    url = self.base_link + '/ip.file/swf/plugins/ipplugins.php'
                    p1 = client.parseDOM(u, 'a', ret='data-film')[0]
                    p2 = client.parseDOM(u, 'a', ret='data-server')[0]
                    p3 = client.parseDOM(u, 'a', ret='data-name')[0]
                    post = {'ipplugins': 1, 'ip_film': p1, 'ip_server': p2, 'ip_name': p3, 'fix': "0"}
                    post = urlencode(post)
                    for i in range(3):
                        result = ensure_text(client.request(url, post=post, XHR=True, referer=ref, timeout='5'), errors='replace')
                        if not result == None:
                            break
                    result = json.loads(result)
                    u = result['s']
                    try:
                        s = result['v']
                    except:
                        s = result['c']
                    url = self.base_link + '/ip.file/swf/ipplayer/ipplayer.php'
                    for n in range(3):
                        try:
                            post = {'u': u, 'w': '100%', 'h': '420', 's': s, 'n': n}
                            post = urlencode(post)
                            result = ensure_text(client.request(url, post=post, XHR=True, referer=ref, timeout='5'), errors='replace')
                            src = json.loads(result)['data']
                            if not src or src == 'hash':
                                continue
                            if type(src) is list:
                                src = [i['files'] for i in src]
                                for i in src:
                                    for source in scrape_sources.process(hostDict, i):
                                        self.results.append(source)
                            else:
                                for source in scrape_sources.process(hostDict, src):
                                    self.results.append(source)
                        except:
                            #log_utils.log('sources', 1)
                            pass
                except:
                    #log_utils.log('sources', 1)
                    pass
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        if 'google' in url:
            url = googlestream.googlepass(url)
        return url


"""


https://streambox.one/embed/?hash=835d39c63aa1050b707c522981c59fb8
can be...
https://streambox.one/embed-Jw4xBFZ.html
# Cant be resolved without alot of work lol.


"""


