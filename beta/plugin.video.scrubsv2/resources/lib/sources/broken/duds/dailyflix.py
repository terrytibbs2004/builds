# -*- coding: UTF-8 -*-

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import log_utils
from resources.lib.modules import scrape_sources


class source:
    def __init__(self):
        self.results = []
        self.domains = ['main.dailyflix.stream', 'dailyflix.stream']
        self.base_link = 'https://main.dailyflix.stream'
        self.search_link = '/?s=%s'
        self.cookie = client.request(self.base_link, output='cookie', timeout='5')


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_title = cleantitle.get(title)
            movie_link = self.base_link + self.search_link % movie_title
            html = client.request(movie_link, cookie=self.cookie)
            tbody = client.parseDOM(html, 'tbody')[0]
            items = client.parseDOM(tbody, 'tr')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in items]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            url = [i[0] for i in r if check_title == cleantitle.get(i[1])][0]
            return url
        except Exception:
            log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url, cookie=self.cookie)
            links = client.parseDOM(html, 'iframe', ret='src')
            for link in links:
                log_utils.log('Scraper dailyflix sources link: ' + repr(link))
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except Exception:
            log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


"""


#https://watch.dailyflix.stream/

https://main.dailyflix.stream/?s=captain+marvel

<tbody>
                                                                <tr>
    <td>
        <span class="far fa-play-circle"></span>
        <a href="https://main.dailyflix.stream/captain-marvel/">Captain Marvel</a>
    </td>
    <td class="has-text-right is-size-7 is-hidden-mobile">0</td>
                                    <tr>
    
</tbody>



<tbody>
                                                                <tr>
    <td>
        <span class="far fa-play-circle"></span>
        <a href="https://main.dailyflix.stream/deadpool-2/">Deadpool 2</a>
    </td>
    <td class="has-text-right is-size-7 is-hidden-mobile">0</td>
                                    <tr>
                                    <tr>
    <td>
        <span class="far fa-play-circle"></span>
        <a href="https://main.dailyflix.stream/once-upon-a-deadpool/">Once Upon a Deadpool</a>
    </td>
    <td class="has-text-right is-size-7 is-hidden-mobile">0</td>
                                    <tr>
                                    <tr>
    <td>
        <span class="far fa-play-circle"></span>
        <a href="https://main.dailyflix.stream/deadpool/">Deadpool</a>
    </td>
    <td class="has-text-right is-size-7 is-hidden-mobile">0</td>
                                    <tr>
    
</tbody>






"""

