import xbmcvfs
import xbmcplugin
import sys
from urllib.parse import parse_qsl
from .replays import replays
from . import vc, bst, sc
from .plugin import m

def main_menu():
    xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Main Menu')
    
    m.add_dir('Latest Movies','','vc_latest_movies',m.addon_icon, m.addon_fanart,'Watch the Latest Movies')

    m.add_dir('Trending Movies','','vc_trending_movies',m.addon_icon, m.addon_fanart,'Watch the Latest Trending Movies')

    m.add_dir('Latest Episodes','','vc_latest_episodes',m.addon_icon, m.addon_fanart,'Watch the Latest Series Episodes')

    m.add_dir('Latest Seasons', vc.series_url, 'vc_latest_season', m.addon_icon, m.addon_fanart, 'Watch the Latest Series Seasons')

    m.add_dir('BS Latest', bst.new_shows, 'bst_new_shows', m.addon_icon, m.addon_fanart,'Watch the Latest Episodes')
    
    m.add_dir('BS Popular Series', bst.most_popular, 'bst_series', m.addon_icon, m.addon_fanart,'Popular Series')

    m.add_dir('Search','','vc_search_history', m.addon_icon, m.addon_fanart,'Search Movies and Series')
    
    m.add_dir('Vids', '', 'vid_main', m.addon_icon, m.addon_fanart, 'Vids')
    
    m.add_dir('Sports Replays', '', 'replays_main', m.addon_icon, m.addon_fanart, 'Sports Replays')

    
def router(paramstring):
    p = dict(parse_qsl(paramstring))
    name = p.get('name', '')
    name2 = p.get('name2', '')
    url = p.get('url', '')
    mode = p.get('mode')
    icon = p.get('icon', m.addon_icon)
    fanart = p.get('fanart', m.addon_fanart)
    description = p.get('description', '')
    if p.get('page') is None: page = ''
    else: page = int(p.get('page'))
    
    #import json
    #m.textview(json.dumps(p, indent=4))
    
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    
    if mode is None:
        if not xbmcvfs.exists(m.addon_data):
            xbmcvfs.mkdirs(m.addon_data)
        main_menu()
    
    #---VC Modes---#    
    elif mode == 'play_video':
        from .player import Player
        p = Player()
        p.play_video(name, url, icon, description,name2)
        
    elif mode == 'vc_latest_movies':
        vc.latest_movies()
        
    elif mode == 'vc_trending_movies':
        vc.trending_movies()
        
    elif mode == 'vc_latest_episodes':
        vc.latest_episodes()
        
    elif mode == 'vc_trending_series':
        vc.featured_series()
        
    elif mode == 'vc_latest_movies_nextpage':
        vc.latest_movies_nextpage(url)
        
    elif mode == 'trending_movies_nextpage':
        vc.trending_movies_nextpage(url)
        
    elif mode == 'latest_series_nextpage':
        vc.latest_series_nextpage(url)
        
    elif mode == 'featured_series_nextpage':
        vc.featured_series_nextpage(url)
        
    elif mode == 'vc_search_history':
        vc.search_history()
    
    elif mode == 'vc_search':
        vc.search(url, page, icon, description)
        
    elif mode == 'vc_links_page':
        vc.links_page(name, url, icon)
        
    elif mode == 'vc_season_menu':
        vc.season_menu(url)
        
    elif mode == 'vc_latest_season':
        vc.latest_episodes(_type='season')
        
    elif mode == 'vc_featured_season':
        vc.featured_series(_type='season')
        
    elif mode == 'vc_season_nextpage':
        vc.latest_series_nextpage(url, _type = 'season')
        
    elif mode == 'vc_featured_season_nextpage':
        vc.featured_series_nextpage(url, _type = 'season')
    
    #---BST Modes---#    
    elif mode == 'bst_new_shows':
        bst.bshows1(url)
        
    elif mode == 'bst_get_links':
        bst1 = bst.bst
        bst1.get_links(name2, url, icon)
        
    elif mode == 'bst_browse_shows':
        bst.bshows_series(url)
        
    elif mode == 'bst_episodes':
        bst.bshows_episodes(name, url)
        
    elif mode == 'bst_new_shows':
        bst.bshows1(url)
        
    elif mode == 'bst_series':
        bst.bshows_series(bst.most_popular)
        
    elif mode == 'play_video2':
        from .player import Player
        p = Player()
        p.play_video(name, url, icon, description, name2)
    
    #---Replays Modes---#
    elif mode == 'replays_main':
        replays.main_menu()
    
    elif mode == 'replays_cat':
        replays.sub_menu(name, url)
    
    elif mode == 'replays_links':
        replays.get_replays_links(name, url, icon)
    
    elif mode == 'replays_archives':
        replays.archives_main()
    
    elif mode == 'replays_date':
        replays.by_date(url, icon)

    elif mode == 'replays_search':
        replays.search(url, icon)
    
    elif mode == 'soccer_main':
        sc.main(icon)

    elif mode == 'soccer_matches':
        sc.matches(url)

    elif mode == 'soccer_get_links':
        sc.get_links(name, url, icon, fanart)
    
    elif mode == 'vid_main':
        from .myvideo import main
        main()
    
    elif mode == 'vid_sub':
        from .myvideo import sub_menu
        sub_menu(url)
    
    elif mode == 'vid_search_history':
        from .myvideo import search_history
        search_history()
    
    elif mode == 'vid_search':
        from .myvideo import search
        search(query = name)
    
    elif mode == 'vid_player':
        from .myvideo import get_links
        get_links(name, url, icon, description)
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))