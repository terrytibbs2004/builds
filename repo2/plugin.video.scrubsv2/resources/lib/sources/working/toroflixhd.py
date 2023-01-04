# -*- coding: utf-8 -*-

import re
import requests

from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
control.moderator()
from resources.lib.modules import scrape_sources
from resources.lib.modules import source_utils
#from resources.lib.modules import log_utils


class source:
    def __init__(self):
        try:
            self.results = []
            self.domains = ['toroflixhd.cf']
            self.base_link = 'https://toroflixhd.cf'
            self.search_link = '/search/%s/feed/rss2/'
            self.ajax_link = '/wp-admin/admin-ajax.php'
            self.session = requests.Session()
        except Exception:
            #log_utils.log('__init__', 1)
            return


# Needs more testing and maybe some changes.
# Has tv shows but not sure if its worth adding.


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movie_title = cleantitle.get_plus(title)
            check_term = '%s (%s)' % (title, year)
            check1 = cleantitle.get_plus(check_term)
            check2 = cleantitle.geturl(title)
            search_url = self.base_link + self.search_link % movie_title
            r = client.request(search_url)
            r = client.parseDOM(r, 'item')
            r = [(client.parseDOM(i, 'link'), client.parseDOM(i, 'title'), re.findall('/movies/(.+?)/</guid>', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in r if check1 in cleantitle.get_plus(i[1]) and check2 == i[2]][0]
            return url
        except Exception:
            #log_utils.log('movie', 1)
            return


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            html = client.request(url)
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
            results = re.compile("class='dooplay_player_option' data-type='(.+?)' data-post='(.+?)' data-nume='(\d+)'>", re.DOTALL).findall(html)
            for data_type, data_post, data_nume in results:
                try:
                    payload = {'action': 'doo_player_ajax', 'post': data_post, 'nume': data_nume, 'type': data_type}
                    r = self.session.post(post_link, headers=customheaders, data=payload)
                    i = r.json()
                    p = i['embed_url'].replace('\\', '')
                    link = client.parseDOM(p, 'iframe', ret='src')[0]
                    for source in scrape_sources.process(hostDict, link):
                        self.results.append(source)
                except:
                    pass
            downloads = client.parseDOM(html, 'a', attrs={'rel': 'noopener noreferrer'}, ret='href')
            for download in downloads:
                try:
                    if 'new.gdtot.cfd' in download:
                        continue
                    if 'torodrive.click' in download:
                        download = download.replace('/file/', '/play.php?id=')
                        html = client.scrapePage(download).text
                        download = re.findall('{"file":"(.+?)",', html)[0]
                    valid, host = source_utils.is_host_valid(download, hostDict)
                    quality, info = source_utils.get_release_quality(download, download)
                    download += '|Referer=%s' % url
                    self.results.append({'source': host, 'quality': quality, 'info': info, 'url': download, 'direct': True})
                except:
                    pass
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


"""


<li id='player-option-1' class='dooplay_player_option' data-type='movie' data-post='705' data-nume='1'>

https://sbspeed.com/e/n2bwdavydr1y.html
https://filepress.online/video/63022935ea302158d7a28470
https://filepress.online/video/6302293aea302158d7a284e9
https://filepress.online/video/63022940ea302158d7a2854f
https://short.ink/SK63uwqE5

https://filepress.online/video/63022e97ea302158d7a2d39c
https://filepress.online/video/63022e9dea302158d7a2d436
https://filepress.online/video/63022ea2ea302158d7a2d48a
https://short.ink/PE_sXFpeB


#####################################################################################


<a href="https://steep-star-e1a2.deadinside.workers.dev/0:/Hollywood/Bullet.Train.2022.1080p.Multi.Audio.AMZN.WEB-DL.x264.ESubs-TOROFlixHD.CF.mkv" target=" rel=" rel="noopener noreferrer">
<a href="https://steep-star-e1a2.deadinside.workers.dev/0:/Hollywood/Bullet.Train.2022.720p.Multi.Audio.AMZN.WEB-DL.x264.ESubs-TOROFlixHD.CF.mkv" target=" rel=" rel="noopener noreferrer">
<a href="https://steep-star-e1a2.deadinside.workers.dev/0:/Hollywood/Bullet.Train.2022.480p.Dual.Audio.Hin.Eng.AMZN.WEB-DL.x264.ESubs-TOROFlixHD.CF.mkv" target=" rel=" rel="noopener noreferrer">

<a href="https://new.gdtot.cfd/file/3972113336" target=" rel=" rel="noopener noreferrer">
<a href="https://new.gdtot.cfd/file/1692150312" target=" rel=" rel="noopener noreferrer">
<a href="https://new.gdtot.cfd/file/487855297" target=" rel=" rel="noopener noreferrer">

<a href="https://torodrive.click/file/3972113336" target=" rel=" rel="noopener noreferrer">
<a href="https://torodrive.click/file/1692150312" target=" rel=" rel="noopener noreferrer">
<a href="https://torodrive.click/file/487855297" target=" rel=" rel="noopener noreferrer">



https://torodrive.click/file/487855297

https://torodrive.click/stream/487855297

https://torodrive.click/play.php?id=487855297

{"file":"https://torodrive.click/drive-stream.php?download=487855297&label=0&idplay=1666320561",


"""



