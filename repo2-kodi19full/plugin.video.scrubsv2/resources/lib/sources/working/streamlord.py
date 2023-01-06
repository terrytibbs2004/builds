# -*- coding: utf-8 -*-

import re

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import jsunpack
#from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['streamlord.com']
            self.base_link = 'http://www.streamlord.com'
            self.search_link = 'https://www.google.com/search?q=%s+%s+site:streamlord.com'
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
            if tvshowtitle == 'House':
                tvshowtitle = 'House M.D.'
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


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            search_title = cleantitle.get_plus(title)
            check_title = '%s+%s' % (search_title, year) if 'tvshowtitle' in data else '%s+(%s)' % (search_title, year)
            search_url = self.search_link % (search_title, year)
            html = client.scrapePage(search_url).text
            results = re.findall('<a href="(.+?)"><h3(.+?)</h3>', html)
            results = [(i[0], i[1]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i[0] for i in results if check_title in cleantitle.get_plus(i[1])][0]
            result_url = re.compile('q=(.+?)&amp', re.DOTALL).findall(result)[0]
            result_html = client.scrapePage(result_url).text
            try: # Havent seen this used.
                f = re.findall('''["']sources['"]\s*:\s*\[(.*?)\]''', result_html)[0]
                f = re.findall('''['"]*file['"]*\s*:\s*([^\(]+)''', f)[0]
                u = re.findall('function\s+%s[^{]+{\s*([^}]+)' % f, result_html)[0]
                u = re.findall('\[([^\]]+)[^+]+\+\s*([^.]+).*?getElementById\("([^"]+)', u)[0]
                a = re.findall('var\s+%s\s*=\s*\[([^\]]+)' % u[1], result_html)[0]
                b = client.parseDOM(result_html, 'span', attrs={'id': u[2]})[0]
                link = u[0] + a + b
                link = link.replace('"', '').replace(',', '').replace('\/', '/')
            except:
                pass
            try: # this seems to be used for shows.
                link = jsunpack.unpack(result_html)
                link = link.replace('"', '')
            except:
                pass
            try: # this seems to be used for movies.
                link = re.findall(r'sources[\'"]\s*:\s*\[.*?file[\'"]\s*:\s*(\w+)\(\).*function\s+\1\(\)\s*\{\s*return\([\'"]([^\'"]+)', result_html, re.DOTALL)[0][1]
            except:
                pass
            quality = '720p' if '-movie-' in result_html else 'SD'
            link += '|%s' % urlencode({'Referer': result_url})
            self.results.append({'source': 'Direct', 'quality': quality, 'url': link, 'direct': True})
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


