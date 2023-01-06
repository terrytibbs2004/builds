# -*- coding: UTF-8 -*-

import re

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
        self.domains = ['movie4u.live', 'movies4u.co']
        self.base_link = 'https://www1.movie4u.live'


# Ditched for bad results instead of quality links.


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
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            search_title = cleantitle.geturl(title)
            if 'tvshowtitle' in data:
                search_url = self.base_link + '/episodes/%s-%sx%s/' % (search_title, season, episode)
            else:
                search_url = self.base_link + '/movies/%s' % search_title
            item_url = client.scrapePage(search_url).url
            item_html = client.scrapePage(item_url).text
            
            item_date = client.parseDOM(item_html, 'span', attrs={'class': 'date'})[0]
            if not (year in item_date or data['year'] in item_date):
                return self.results
            item_holder = client.parseDOM(item_html, 'div', attrs={'class':'bwa-content'})[0]
            item_holder = client.parseDOM(item_holder, 'a', ret='href')[0]
            page_html = client.scrapePage(item_holder).text
            page_links = client.parseDOM(page_html, 'iframe', ret='src', attrs={'class': 'metaframe rptss'})
            for link in page_links:
                #log_utils.log('link: \n' + repr(link))
                try:
                    link = url = client.request(link, timeout='10', output='geturl') if 'player.php' in link else link
                    for source in scrape_sources.process(hostDict, link):
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


# Link 1 is before ...
#link = client.scrapePage(link).url if 'player.php' in link else link
# Link 2 is after that.  Seems to need a bit more work or maybe just ditch the shows.

Scraper Testing - movie4u sources link1: 'https://movie4u.live/dl/1/player.php?id=f1afc5b2-7050-4684-ab03-e7eaf407b051'
Scraper Testing - movie4u sources link1: 'https://movie4u.live/dl/2/player.php?id=45c1e4a5-f012-4128-8d53-37361bfccfdf'
Scraper Testing - movie4u sources link1: 'https://openload.co/embed/0EZJRQL8APE/Deadwood.S03E03.720p.Bluray.x264.anoXmous_.mp4'
Scraper Testing - movie4u sources link1: 'https://streamango.com/embed/mmdqrepbbnqbbcfk/Deadwood_S03E03_720p_Bluray_x264_anoXmous_mp4'

Scraper Testing - movie4u sources link2: 'https://1movietv.com/playmotv/videoplayback.php?id=FypEo9w+lJpT3Zczo8kZiOzNLZeK6PC4vfTwUHMj+pYMaaEwu5l/8ETJEyzZUEOTFxk0GJvs8Zqtzj2XcHvB170lrXYVx34Ck6TUIBs864GoAEXvGzO+E5me+Ffq/qBDrcPx8gSz9WSib5LMfBfmyQu8LJzCfyJ7Tla6pMxVGkHgRPqWeSsEuxlCizFxQO5e8T8udqpcD28jJ1POSoRmO+OrNjW67v6vd8132KwEKLLq26tfUHGnU5b1/bPTUKnJPHumQ1F/dIQP94r05jDQvVGTl4R5ULTm2B5f3gNl5LZrvh0KMJulDWtyBFQx/CWhirBXxOJFS1iAdzP3iok0kToGahgBzKnaMOEp0mi3p10='
Scraper Testing - movie4u sources link2: 'https://openload.co/embed/0EZJRQL8APE/Deadwood.S03E03.720p.Bluray.x264.anoXmous_.mp4'
Scraper Testing - movie4u sources link2: 'https://streamango.com/embed/mmdqrepbbnqbbcfk/Deadwood_S03E03_720p_Bluray_x264_anoXmous_mp4'
Scraper Testing - movie4u sources link2: 'https://vidsrc.me/embed/tt2231461/'
Scraper Testing - movie4u sources link2: 'https://vidsrc.me/embed/tt3861390/'
Scraper Testing - movie4u sources link2: 'https://vidsrc.me/embed/tt4154664/'


"""


