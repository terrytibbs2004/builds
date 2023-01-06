import xbmc
import xbmcvfs
import xbmcgui
import xbmcplugin
import sys
import json
from urllib.parse import quote
from .plugin2 import Myaddon, m

SEARCH_HISTORY = m.addon_data + 'search_history.json'
base_url = 'https://membed.net'
recently_added = base_url + '/index.php'
movies_url = base_url + '/movies'
featured_movies_url = base_url + '/cinema-movies'
series_url = base_url + '/series'
featured_series_url = base_url + '/recommended-series'
search_url = base_url + '/search.html?keyword='


class VC(Myaddon):

    def get_main(self, _url, content=None):
        soup = self.get_soup(_url)
        listings = soup.find(class_ = 'listing items')
        item_list = []
        for item in listings.find_all('a'):
            name = item.find(class_ = 'name').text.strip().replace('  ', ' ')
            url = base_url + item['href']
            icon = item.img['src']
            fanart = self.addon_fanart
            description = name
            item_list.append({'name': name, 'url': url, 'icon': icon, 'fanart': fanart, 'description': description})
        if content is not None:
            pagination = soup.find(class_ = 'pagination')
            page = pagination.find_all('a')[-1]['href']
            next_page = content + page    
            item_list.append(next_page)
        return item_list
    
    def get_season(self, url):
        soup = self.get_soup(url)
        episodes = soup.find(class_='video-info-left')
        episodes = episodes.find_all(class_='video-block')
        item_list = []
        for episode in episodes:
            title = episode.find('img')['alt'].strip().replace('  ', ' ').replace('Epiode', 'Episode')
            link = base_url + episode.a['href']
            icon = episode.find('img')['src']
            item_list.append([title, link, icon])
        return item_list

    def get_links(self, _url):
        soup = self.get_soup(_url)
        xbmc.log(f'soup= {soup.prettify}', xbmc.LOGINFO)
        description = soup.find(class_ = 'content-more-js')
        if description:
            description = description.text.strip()
        else:
            description = ''
        embed = 'https:' + soup.find('iframe')['src']
        soup = self.get_soup(embed)
        item_list = self.get_links_list(soup)
        item_list.append(description)
        return item_list
    
    #---Scraper---#

    def search_items(self, query, _type = 'Movies'):
        soup = self.get_soup(search_url + quote(query))
        items = soup.find_all(class_ = 'video-block')
        if len(items) > 0:
            if _type == 'Movies':
                for item in items:
                    if not 'season' in item.text.lower() and not 'episode' in item.text.lower():
                        return base_url + item.a['href']
        return xbmcgui.Dialog().ok('Gratis', 'Item Not Available')

    def get_link_page(self, _url):
        try:
            soup = self.get_soup(_url)
            return 'http:' + soup.find('iframe')['src']
        except Exception as e:
            xbmc.log(str(e), xbmc.LOGINFO)
    
    def get_links_list(self, _soup):
        try:
            links = _soup.find_all(class_ = 'linkserver')
        except AttributeError as e:
            return print(e)
        item_list = []
        for link in links:
            x = link.text.lower()
            if 'dood' in x or 'mixdrop' in x or 'streamsb' in x:
                links2 = []
                links2.append(link.text)
                links2.append(link['data-video'].split('?')[0])
                if links2 not in item_list:
                    item_list.append(links2)
        return item_list
    
    def get_scraper_links(self, query, _type='Movies'):
        _url = self.search_items(query, _type)
        soup = self.get_soup(self.get_link_page(_url))
        return self.get_links_list(soup)

#---VC Menus---#

vc = VC()

def latest_movies():
    xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Latest Movies')
    main = vc.get_main(movies_url, movies_url)
    for item in main[:-1]:
        vc.add_dir(item['name'],item['url'],'vc_links_page',item['icon'], item.get('fanart', vc.addon_fanart), item['description'], isFolder=False)
    vc.add_dir('Next Page', main[-1],'vc_latest_movies_nextpage','','','Open the Next Page')

def trending_movies():
    xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Trending Movies')
    main = vc.get_main(featured_movies_url, featured_movies_url)
    for item in main[:-1]:
        vc.add_dir(item['name'],item['url'],'vc_links_page',item['icon'],item.get('fanart', vc.addon_fanart), item['description'], isFolder=False)
    vc.add_dir('Next Page', main[-1],'trending_movies_nextpage','','','Open the Next Page')

def latest_episodes(_type=None):
    if _type == 'season':
        xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Latest Series Seasons')
    else:
        xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Latest Episodes')
    main = vc.get_main(series_url, series_url)
    for item in main[:-1]:
        if _type == 'season':
            if ' episode ' in item['name'].lower() and ' season ' in item['name'].lower():
                name = item['name'].split(' Episode')[0].strip(':').strip('-')
                vc.add_dir(name, item['url'], 'vc_season_menu', item['icon'], item.get('fanart', vc.addon_fanart), item['description'])
        else:
            vc.add_dir(item['name'],item['url'],'vc_links_page',item['icon'],item.get('fanart', vc.addon_fanart), item['description'], isFolder=False)
    if _type == 'season':
        vc.add_dir('Next Page', main[-1],'vc_season_nextpage','','','Open the Next Page')
    else:
        vc.add_dir('Next Page', main[-1],'latest_series_nextpage','','','Open the Next Page')

def featured_series(_type=None):
    if _type == 'season':
        xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Featured Series Seasons')
    else:
        xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Featured Series Episodes')
    main = vc.get_main(featured_series_url, featured_series_url)
    for item in main[:-1]:
        if _type == 'season':
            if ' episode ' in item['name'].lower() and ' season ' in item['name'].lower():
                name = item['name'].split(' Episode')[0].strip(':').strip('-')
                vc.add_dir(name, item['url'], 'vc_season_menu', item['icon'], vc.addon_fanart, name)
        else:
            vc.add_dir(item['name'],item['url'],'vc_links_page',item['icon'], vc.addon_fanart,item['name'], isFolder=False)
    if _type == 'season':
        vc.add_dir('Next Page', main[-1],'vc_featured_season_nextpage','','','Open the Next Page')
    else:
        vc.add_dir('Next Page', main[-1],'featured_series_nextpage','','','Open the Next Page')

def latest_movies_nextpage(_url):
    xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Latest Movies')
    main = vc.get_main(_url, movies_url)
    for item in main[:-1]:
        vc.add_dir(item['name'],item['url'],'vc_links_page',item['icon'],item.get('fanart', vc.addon_fanart), item['description'], isFolder=False)
    vc.add_dir('Next Page', main[-1],'vc_latest_movies_nextpage','','','Open the Next Page')

def trending_movies_nextpage(_url):
    xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Trending Movies')
    main = vc.get_main(_url, featured_movies_url)
    for item in main[:-1]:
        vc.add_dir(item['name'], item['url'],'vc_links_page',item['icon'],item.get('fanart', vc.addon_fanart), item['description'], isFolder=False)
    vc.add_dir('Next Page', main[-1],'trending_movies_nextpage','','','Open the Next Page')

def latest_series_nextpage(_url, _type=None):
    if _type == 'season':
        xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Latest Series Seasons')
    else:
        xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Latest Series Episodes')
    main = vc.get_main(_url, series_url)
    for item in main[:-1]:
        if _type == 'season':
            if ' episode ' in item['name'].lower() and ' season ' in item['name'].lower():
                name = item['name'].split(' Episode')[0].strip(':').strip('-')
                vc.add_dir(name, item['url'], 'vc_season_menu', item['icon'], item.get('fanart', vc.addon_fanart), item['description'])
        else:
            vc.add_dir(item['name'],item['url'],'vc_links_page',item['icon'],item.get('fanart', vc.addon_fanart), item['description'], isFolder=False)
    if _type == 'season':
        vc.add_dir('Next Page', main[-1],'vc_season_nextpage','','','Open the Next Page')
    else:
        vc.add_dir('Next Page', main[-1],'latest_series_nextpage','','','Open the Next Page')

def featured_series_nextpage(_url, _type=None):
    if _type == 'season':
        xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Featured Series Seasons')
    else:
        xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Featured Series Episodes')
    main = vc.get_main(_url, featured_series_url)
    for item in main[:-1]:
        if _type == 'season':
            if ' episode ' in item['name'].lower() and ' season ' in item['name'].lower():
                name = item['name'].split(' Episode')[0].strip(':').strip('-')
                vc.add_dir(name, item['url'], 'vc_season_menu', item['icon'], vc.addon_fanart, name)
        else:
            vc.add_dir(item['name'],item['url'],'vc_links_page',item['icon'], vc.addon_fanart,item['name'], isFolder=False)
    if _type == 'season':
        vc.add_dir('Next Page', main[-1],'vc_featured_season_nextpage','','','Open the Next Page')
    else:
        vc.add_dir('Next Page', main[-1],'featured_series_nextpage','','','Open the Next Page')

def search(_url, page, icon, description):
    history = []
    if page == '':
        page = 2
        query = m.from_keyboard()
        if not query: quit()
        if not xbmcvfs.exists(SEARCH_HISTORY):
            with open(SEARCH_HISTORY, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(json.dumps(history))
        with open(SEARCH_HISTORY, 'r', encoding='utf-8', errors='ignore') as f:
            history = json.load(f)
        if not query in history:
            history.append(query)
        with open(SEARCH_HISTORY, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(json.dumps(history))
            _url = search_url + quote(query)
    else:
        page = int(page) + 1
    main = vc.get_main(_url)
    if len(main) >= 1:
        for item in main:
            if ' episode ' in item['name'].lower() and ' season ' in item['name'].lower():
                name = item['name'].split(' Episode')[0].strip(':').strip('-')
                vc.add_dir(name, item['url'], 'vc_season_menu', item['icon'], vc.addon_fanart, name)
            else:
                name = item['name']
                vc.add_dir(name, item['url'], 'vc_links_page', item['icon'], vc.addon_fanart, name, isFolder=False)
        vc.add_dir('Next Page', _url + f'&page={str(page)}', 'vc_search', icon,  vc.addon_fanart, description, page=page)
    else:
        vc.add_dir('No More Items to Display', '', '', '',  vc.addon_fanart, 'No More Items to Display', isFolder=False)

def search_history():
    m.add_dir('New Search', '', 'vc_search', m.addon_icon, m.addon_fanart, 'New Search')
    if xbmcvfs.exists(SEARCH_HISTORY):
        with open(SEARCH_HISTORY, 'r', encoding='utf-8', errors='ignore') as f:
            history = json.load(f)
        if history:
            history.reverse()
        for query in history:
            m.add_dir(query, search_url + quote(query), 'vc_search', m.addon_icon, m.addon_fanart, '', page=1)

def season_menu(url):
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
    for title, link, icon in vc.get_season(url):
        vc.add_dir(title, link, 'vc_links_page', icon, vc.addon_fanart, title, isFolder=False)

def links_page(title, _url, iconimage):
    xbmcplugin.setPluginCategory(int(sys.argv[1]), title)
    xbmc.log(f'_url= {_url}', xbmc.LOGINFO)
    links = vc.get_links(_url)
    desc = links[-1]
    from .player2 import Player
    p = Player()
    p.play_video(title, vc.get_multilink(links[:-1]), iconimage, desc)
    #counter = 1
    #for link in links[:-1]:
        #vc.add_dir('Link ' + str(counter) + ': ' + link[0],link[1], 'play_video', iconimage, fanart, title + ':\n\n' + desc,name2=title,isFolder=False)
        #counter+=1