# -*- coding: utf-8 -*-

import re
import sys

import requests

from six.moves import reduce

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import sources
from resources.lib.modules import scrape_sources
#from resources.lib.modules import log_utils


class doctorwho:
    def __init__(self):
        self.base_link = 'https://watchdoctorwhoonline.com'
        self.ajax_link = '/wp-admin/admin-ajax.php'
        self.session = requests.Session()
        self.hostDict = sources.sources().getHostDict()
        self.categories = [
            {'title': 'Random Episode', 'url': '/?redirect_to', 'image': '/wp-content/uploads/2021/05/new.png'},
            {'title': 'Doctor Who: Specials', 'url': '/season-watch/doctor-who-specials/', 'image': '/wp-content/uploads/2021/08/special-poster.jpg'},
            {'title': 'Doctor Who: Season 1', 'url': '/season-watch/doctor-who-season-1/', 'image': '/wp-content/uploads/2018/01/9Jt2FFCAME7eHDC28r4qCHErhhF-185x278.jpg'},
            {'title': 'Doctor Who: Season 2', 'url': '/season-watch/doctor-who-season-2/', 'image': '/wp-content/uploads/2018/01/oXVmsIkZCgJDNcZJJxzvV7zwyb1-185x278.jpg'},
            {'title': 'Doctor Who: Season 3', 'url': '/season-watch/doctor-who-season-3/', 'image': '/wp-content/uploads/2018/01/67xbjSv353G2rqQIs6dnDKc6P11-185x278.jpg'},
            {'title': 'Doctor Who: Season 4', 'url': '/season-watch/doctor-who-season-4/', 'image': '/wp-content/uploads/2018/01/h6hogh9U371q87XLhvrJbczg8lm-185x278.jpg'},
            {'title': 'Doctor Who: Season 5', 'url': '/season-watch/doctor-who-season-5/', 'image': '/wp-content/uploads/2018/01/hUsQerEeMqsu9cVYzMEB2OGJjrw-185x278.jpg'},
            {'title': 'Doctor Who: Season 6', 'url': '/season-watch/doctor-who-season-6/', 'image': '/wp-content/uploads/2018/01/xmfMcVkVer5r33QhA4e2DpIR78B-185x278.jpg'},
            {'title': 'Doctor Who: Season 7', 'url': '/season-watch/doctor-who-season-7/', 'image': '/wp-content/uploads/2018/01/ciWPkTULcVkgJ56RkTo2NsOYCs9-185x278.jpg'},
            {'title': 'Doctor Who: Season 8', 'url': '/season-watch/doctor-who-season-8/', 'image': '/wp-content/uploads/2018/01/nMxeLkOF9DzbqJdSx7gzmbFvPGK-185x278.jpg'},
            {'title': 'Doctor Who: Season 9', 'url': '/season-watch/doctor-who-season-9/', 'image': '/wp-content/uploads/2018/01/uidaCdI0hKiZGfMzWHNMYeNZyV7-185x278.jpg'},
            {'title': 'Doctor Who: Season 10', 'url': '/season-watch/doctor-who-season-10/', 'image': '/wp-content/uploads/2018/01/8HPLQQqTPfy7Oiligw9FXcfig9w-185x278.jpg'},
            {'title': 'Doctor Who: Season 11', 'url': '/season-watch/doctor-who-season-11/', 'image': '/wp-content/uploads/2018/10/3EcYZhBMAvVw4czcDLg9Sd0FuzQ-185x278.jpg'},
            {'title': 'Doctor Who: Season 12', 'url': '/season-watch/doctor-who-season-12/', 'image': '/wp-content/uploads/2020/01/cDDb7WA2i7cENhkEEjXEDrXGyNL-185x278.jpg'},
            {'title': 'Doctor Who: Season 13', 'url': '/season-watch/doctor-who-season-13/', 'image': '/wp-content/uploads/2022/04/hnAwYE6NvC4UVdMRPd7FOX52PQy-185x278.jpg'}
        ]
        self.list = []


    def root(self):
        try:
            for i in self.categories:
                title = client.replaceHTMLCodes(i['title'])
                url = self.base_link + i['url']
                image = self.base_link + i['image']
                if i['title'] == 'Random Episode':
                    action = 'doctorwho_scrape_episode'
                else:
                    action = 'doctorwho_scrape_season'
                self.list.append({'title': title, 'url': url, 'image': image, 'action': action})
            addDirectory(self.list)
            return self.list
        except:
            #log_utils.log('root', 1)
            return self.list


    def scrape_season(self, url):
        try:
            html = client.scrapePage(url).text
            episodes = client.parseDOM(html, 'li', attrs={'class': r'mark-.*?'})
            for i in episodes:
                title1 = client.parseDOM(i, 'div', attrs={'class': 'numerando'})[0]
                title2 = re.findall("<div class='episodiotitle'>.+?'>(.+?)</a>", i)[0]
                title_layout = '[B]%s[/B] (%s)' % (title1, title2)
                title = client.replaceHTMLCodes(title_layout)
                link = client.parseDOM(i, 'a', ret='href')[0]
                image = client.parseDOM(i, 'img', ret='src')[0]
                self.list.append({'title': title, 'url': link, 'image': image, 'action': 'doctorwho_scrape_episode'})
            addDirectory(self.list)
            return self.list
        except:
            #log_utils.log('scrape_season', 1)
            return self.list


    def scrape_episode(self, url):
        try:
            if not url.startswith('http'):
                url = self.base_link + url
            if '/?redirect_to' in url:
                url += '=random&post_type=episodes'
            html = client.scrapePage(url).text
            customheaders = {
                'Host': 'watchdoctorwhoonline.com',
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
                    i = r.text
                    p = i.replace('\\', '')
                    link = client.parseDOM(p, 'iframe', ret='src')[0]
                    for source in scrape_sources.process(self.hostDict, link):
                        title = '%s ( %s %s)' % (source['source'], source['quality'], source['info'])
                        link = source['url']
                        self.list.append({'title': title, 'url': link, 'image': None, 'action': 'alt_play'})
                except:
                    #log_utils.log('scrape_episode', 1)
                    pass
            addDirectory(self.list)
            return self.list
        except:
            #log_utils.log('scrape_episode', 1)
            control.infoDialog('Error : No Stream Available.', sound=False, icon='INFO')
            return self.list


def addDirectory(items, queue=False, isFolder=True):
    if items == None or len(items) == 0:
        control.idle()
    sysaddon = sys.argv[0]
    syshandle = int(sys.argv[1])
    addonFanart = control.addonFanart()
    for i in items:
        try:
            url = '%s?action=%s&url=%s' % (sysaddon, i['action'], i['url'])
            title = i['title']
            thumb = i['image'] if not i['image'] == (None or 'None') else 'DefaultVideo.png'
            item = control.item(label=title)
            item.setProperty('IsPlayable', 'true')
            item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': addonFanart})
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
        except Exception:
            #log_utils.log('addDirectory', 1)
            pass
    control.content(syshandle, 'addons')
    control.directory(syshandle, cacheToDisc=True)


