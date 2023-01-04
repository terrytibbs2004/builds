# -*- coding: utf-8 -*-

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
        self.domains = ['forums.myvideolinks.net', 'myvideolinks.net']
        self.base_link = 'http://forums.myvideolinks.net'
        self.search_link = '/search.php?keywords=%s&terms=all&author=&sc=1&sf=all&sr=topics&sk=t&sd=d&st=0&ch=0&t=0&submit=Search'


#https://to.myvideolinks.net/
#https://to.myvideolinks.net/?s=hocus+pocus


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
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
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
            season, episode = (data['season'], data['episode']) if 'tvshowtitle' in data else ('0', '0')
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            search = '%s %s' % (title, hdlr) if 'tvshowtitle' in data else data['imdb']
            search_url = self.base_link + self.search_link % cleantitle.get_plus(search)
            search_html = client.scrapePage(search_url).text
            search_result = client.parseDOM(search_html, 'ul', attrs={'class': 'topiclist topics'})[0]
            search_result = client.parseDOM(search_result, 'li')
            search_result = [(client.parseDOM(i, 'a', attrs={'class': 'topictitle'}, ret='href'), client.parseDOM(i, 'a', attrs={'class': 'topictitle'})) for i in search_result]
            search_result = [(i[0][0], i[1][0]) for i in search_result if len(i[0]) > 0 and len(i[1]) > 0]
            result_urls = [i[0] for i in search_result if hdlr in i[1]]
            for result_url in result_urls:
                try:
                    result_url = result_url.replace('./viewtopic.php', '/viewtopic.php')
                    result_url = self.base_link + client.replaceHTMLCodes(result_url)
                    page_html = client.scrapePage(result_url).text
                    page_links = client.parseDOM(page_html, 'a', attrs={'class': 'postlink'}, ret='href')
                    for link in page_links:
                        if any(i in link for i in ['imdb.com', 'youtube.com', 'turbobit.net', 'streamzz.to']):
                            continue
                        for source in scrape_sources.process(hostDict, link):
                            if source['source'] in str(self.results):
                                continue
                            self.results.append(source)
                except:
                    #log_utils.log('sources', 1)
                    pass
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


