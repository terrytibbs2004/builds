# -*- coding: UTF-8 -*-

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import source_utils
#from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.base_link = 'https://filepursuit.p.rapidapi.com'
            self.search_link = '/?type=video&q=%s'
            self.api_key = control.setting('filepursuit.api') or ''
        except Exception:
            log_utils.log('__init__', 1)
            return


#https://rapidapi.com/azharxes/api/filepursuit
# my key saved for testing and base64'd for a giggle lol.
#IyJYLVJhcGlkQVBJLUtleSI6ICIzOTc2MjgwYjY4bXNoODQ5NzZlZjcxYzJmMTg0cDEwMDZkNmpzbjQ2ZWZlNDk2YmIwNyIs


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urlencode(url)
            return url
        except:
            #log_utils.log('movie', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
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
            if url is None:
                return self.results
            if self.api_key == '':
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            hdlr = 'S%02dE%02d' % (int(season), int(episode)) if 'tvshowtitle' in data else year
            search_term = '%s %s' % (title, hdlr)
            search_url = self.base_link + self.search_link % cleantitle.get_plus(search_term)
            headers = {'X-RapidAPI-Key': self.api_key, 'X-RapidAPI-Host': 'filepursuit.p.rapidapi.com'}
            r = client.scrapePage(search_url, headers=headers).json()
            if 'not_found' in r['status']:
                return self.results
            results = r['files_found']
            for item in results:
                try:
                    name = item['file_name']
                except:
                    name = url.split('/')[-1]
                for alias in aliases:
                    if not cleantitle.get(alias['title']) in cleantitle.get(name):
                        continue
                if any(x in name.lower() for x in ['trailer', 'promo']):
                    continue
                link = item['file_link']
                try:
                    size = float(item['file_size_bytes']) / 1073741824
                    size = '%.2f GB' % size
                except:
                    size = ''
                quality, info = source_utils.get_release_quality(link, name)
                self.results.append({'source': 'Direct', 'quality': quality, 'info': info+size, 'url': link, 'direct': True})
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


