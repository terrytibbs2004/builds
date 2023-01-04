# -*- coding: utf-8 -*-

import re
import base64

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import source_utils
from resources.lib.modules import scrape_sources
#from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['moviesnipipay.me']
            self.base_link = 'https://moviesnipipay.me'
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


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('tvshow', 1)
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
            #log_utils.log('episode', 1)
            return


#https://moviesnipipay.me/batwoman-s01e11/
#https://moviesnipipay.me/turning-red-2022/


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            search_term = '%s %s' % (title, hdlr)
            search_title = cleantitle.geturl(search_term)
            search_link = self.base_link + '/%s/' % search_title
            html = client.scrapePage(search_link).text
            #try: all seem to be shrtlnkz.com trash
                #downloads = client.parseDOM(html, 'div', attrs={'class': 'dl-item'})[0]
                #downloads = re.compile('<a href="(.+?)".+?domain=(.+?)">').findall(downloads)
                #for dl_link, dl_host in downloads:
                    #if 'subscene.com' in dl_host:
                        #continue
                    #self.results.append({'source': dl_host, 'quality': 'SD', 'url': dl_link, 'direct': False})
            #except:
                #log_utils.log('sources', 1)
                #pass
            try:
                results = client.parseDOM(html, 'a', ret='data-em')
                for result in results:
                    b64 = base64.b64decode(result)
                    link = client.parseDOM(b64, 'iframe', ret='src')[0]
                    if any(i in link for i in ['youtube.com', 'short.ink']):
                        continue
                    if 'sharer.pw' in link:
                        try:
                            result_html = client.scrapePage(link).text
                            src = re.findall("Player\.src\({src: '(.+?)',", result_html)[0]
                            quality, info = source_utils.get_release_quality(src, src)
                            src += '|%s' % urlencode({'Referer': link})
                            self.results.append({'source': 'sharer', 'quality': quality, 'url': src, 'info': info, 'direct': True})
                        except:
                            #log_utils.log('sources', 1)
                            pass
                    else:
                        for source in scrape_sources.process(hostDict, link):
                            self.results.append(source)
            except:
                #log_utils.log('sources', 1)
                pass
            return self.results
        except Exception:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        if any(x in url for x in self.domains):
            try:
                link = client.request(url, output='geturl')
                return link
            except:
                return url
        else:
            return url


"""

# Some saved results that need resolved/looked at

https://embed4free.com/embed/G0U4Tb2jivO7tt7qA4
https://embed4free.com/embed/H6lhIfH44bVCicx7AX
https://embed4free.com/embed/qYVkDV8MQxFidYrZdR
https://embed4free.com/embed/XeY0H8qveTgnIqgtXj

https://gdrivestream.com/embed/cPg2OukSy5Ou
https://gdrivestream.com/embed/dCAQ2Zh9PCYg
https://gdrivestream.com/embed/kdvpcZ9eFK8q
https://gdrivestream.com/embed/q7BjxWm1NAOp

https://gdrvplayer.com/embed/0jFzEtFoZmRwePn
https://gdrvplayer.com/embed/9i4q9rgDIbpPXOM
https://gdrvplayer.com/embed/vBJIaQcp9el5E1d
https://gdrvplayer.com/embed/vWQvCqhoQMrtO4i


"""


