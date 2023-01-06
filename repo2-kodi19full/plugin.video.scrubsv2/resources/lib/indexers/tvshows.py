# -*- coding: utf-8 -*-

import re
import os
import sys
import datetime

import simplejson as json
import six
from six.moves import range, urllib_parse, zip

from resources.lib.indexers import navigator

from resources.lib.modules import cleantitle
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import tmdb_utils
from resources.lib.modules import trakt
from resources.lib.modules import utils
from resources.lib.modules import views
from resources.lib.modules import workers
from resources.lib.modules import log_utils

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

params = dict(urllib_parse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

action = params.get('action')


class tvshows:
    def __init__(self):
        self.list = []
        self.datetime = datetime.datetime.utcnow()
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.year_date = (self.datetime - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        self.month_date = (self.datetime - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.specials = control.setting('tv.specials') or 'true'
        self.shownoyear = control.setting('show.noyear') or 'false'
        self.showunaired = control.setting('showunaired') or 'true'
        self.unairedcolor = control.setting('unaired.color')
        if self.unairedcolor == '':
            self.unairedcolor = 'darkred'
        self.hq_artwork = control.setting('hq.artwork') or 'false'
        self.trailer_source = control.setting('trailer.source') or '2'
        self.studio_artwork = control.setting('studio.artwork') or 'false'
        self.items_per_page = str(control.setting('items.per.page')) or '20'
        self.lang = control.apiLanguage()['tmdb'] or 'en'
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tmdb_key = control.setting('tmdb.api')
        if self.tmdb_key == '' or self.tmdb_key == None:
            self.tmdb_key = 'c8b7db701bac0b26edfcc93b39858972'
        self.fanart_tv_headers = {'api-key': 'cb2f78390c6f7cbc5d1c9a257e013e5c'}
        self.fanart_tv_user = control.setting('fanart.api')
        if not self.fanart_tv_user == '' or self.fanart_tv_user == None:
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})
        self.user = control.setting('fanart.api') + str('')
        self.imdb_link = 'https://www.imdb.com'
        self.trakt_link = 'https://api.trakt.tv'
        self.tvmaze_link = 'https://www.tvmaze.com'
        self.tmdb_link = 'https://api.themoviedb.org'
        self.tvmaze_info_link = 'https://api.tvmaze.com/shows/%s'
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/tv/%s'
        #self.tmdb_image_link = 'https://image.tmdb.org/t/p/original'
        self.tmdb_image_link = 'https://image.tmdb.org/t/p/w%s%s'
        self.tmdb_info_link = self.tmdb_link + '/3/tv/%s?api_key=%s&language=en-US&append_to_response=credits,content_ratings,external_ids' % ('%s', self.tmdb_key)

        self.tmdb_search_link = self.tmdb_link + '/3/search/tv?api_key=%s&query=%s&language=en-US&page=1' % (self.tmdb_key, '%s')
        self.tmdb_popular_link = self.tmdb_link + '/3/tv/popular?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_featured_link = self.tmdb_link + '/3/discover/tv?api_key=%s&vote_count.gte=100&sort_by=first_air_date.desc&language=en-US&page=1' % self.tmdb_key
        self.tmdb_toprated_link = self.tmdb_link + '/3/tv/top_rated?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_views_link = self.tmdb_link + '/3/discover/tv?api_key=%s&vote_count.gte=100&sort_by=vote_average.desc&language=en-US&page=1' % self.tmdb_key
        self.tmdb_airing_link = self.tmdb_link + '/3/tv/airing_today?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_active_link = self.tmdb_link + '/3/tv/on_the_air?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_premiere_link = self.tmdb_link + '/3/discover/tv?api_key=%s&first_air_date.gte=%s&first_air_date.lte=%s&language=en-US&page=1' % (self.tmdb_key, self.year_date, self.today_date)
        self.tmdb_trending_day_link = self.tmdb_link + '/3/trending/tv/day?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_trending_week_link = self.tmdb_link + '/3/trending/tv/week?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_genre_link = self.tmdb_link + '/3/discover/tv?api_key=%s&with_genres=%s&language=en-US&page=1' % (self.tmdb_key, '%s')
        self.tmdb_networks_link = self.tmdb_link + '/3/discover/tv?api_key=%s&with_networks=%s&language=en-US&page=1' % (self.tmdb_key, '%s')
        self.tmdb_year_link = self.tmdb_link + '/3/discover/tv?api_key=%s&first_air_date_year=%s&language=en-US&page=1' % (self.tmdb_key, '%s')
        self.tmdb_decade_link = self.tmdb_link + '/3/discover/tv?api_key=%s&first_air_date.gte=%s&first_air_date.lte=%s&language=en-US&page=1' % (self.tmdb_key, '%s', '%s')
        self.tmdb_language_link = self.tmdb_link + '/3/discover/tv?api_key=%s&with_original_language=%s&language=en-US&page=1' % (self.tmdb_key, '%s')
        self.tmdb_collections_link = self.tmdb_link + '/3/collection/%s?api_key=%s&language=en-US&page=1' % ('%s', self.tmdb_key)
        self.tmdb_userlists_link = self.tmdb_link + '/3/list/%s?api_key=%s&language=en-US&page=1' % ('%s', self.tmdb_key)
        self.tmdb_jew250tv_link = self.tmdb_userlists_link % ('86660')
        self.tmdb_jewtestshows_link = self.tmdb_userlists_link % ('97124')
        self.tmdb_huluorig_link = self.tmdb_userlists_link % ('47716')
        self.tmdb_netflixorig_link = self.tmdb_userlists_link % ('47713')
        self.tmdb_amazonorig_link = self.tmdb_userlists_link % ('47714')
        self.tmdb_favorites_link = tmdb_utils.get_tvshow_favorites()
        self.tmdb_watchlist_link = tmdb_utils.get_tvshow_watchlist()

        self.imdb_person_link = self.imdb_link + '/search/title?title_type=tvSeries,tvMiniSeries&release_date=,date[0]&role=%s&sort=year,desc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_persons_link = self.imdb_link + '/search/name?count=100&name='
        self.imdb_personlist_link = self.imdb_link + '/search/name?count=100&gender=male,female'
        self.imdb_popular_link = self.imdb_link + '/search/title?title_type=tvSeries,tvMiniSeries&num_votes=100,&release_date=,date[0]&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page
        self.imdb_premiere_link = self.imdb_link + '/search/title?title_type=tvSeries,tvMiniSeries&languages=en&num_votes=10,&release_date=date[60],date[0]&sort=release_date,desc&count=%s&start=1' % self.items_per_page
        self.imdb_airing_link = self.imdb_link + '/search/title?title_type=tv_episode&release_date=date[1],date[0]&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page
        self.imdb_active_link = self.imdb_link + '/search/title?title_type=tvSeries,tvMiniSeries&num_votes=10,&production_status=active&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page
        self.imdb_views_link = self.imdb_link + '/search/title?title_type=tvSeries,tvMiniSeries&num_votes=100,&release_date=,date[0]&sort=num_votes,desc&count=%s&start=1' % self.items_per_page
        self.imdb_rating_link = self.imdb_link + '/search/title?title_type=tvSeries,tvMiniSeries&num_votes=5000,&release_date=,date[0]&sort=user_rating,desc&count=%s&start=1' % self.items_per_page
        self.imdb_genre_link = self.imdb_link + '/search/title?title_type=tvSeries,tvMiniSeries&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_language_link = self.imdb_link + '/search/title?title_type=tvSeries,tvMiniSeries&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_certification_link = self.imdb_link + '/search/title?title_type=tvSeries,tvMiniSeries&release_date=,date[0]&certificates=us:%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_year_link = self.imdb_link + '/search/title?title_type=tv_series,mini_series&num_votes=100,&production_status=released&year=%s,%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', '%s', self.items_per_page)
        self.imdb_decade_link = self.imdb_link + '/search/title?title_type=tv_series,mini_series&num_votes=100,&production_status=released&year=%s,%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', '%s', self.items_per_page)
        self.imdb_keyword_link = self.imdb_link + '/search/title?title_type=tvSeries,tvMiniSeries&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_keywords_link = self.imdb_link + '/search/keyword?keywords=%s&title_type=tvSeries,miniSeries&sort=moviemeter,asc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_userlists_link = self.imdb_link + '/list/%s/?view=detail&sort=alpha,asc&title_type=tvSeries,miniSeries&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_lists_link = self.imdb_link + '/user/ur%s/lists?tab=all&sort=modified&order=desc&filter=titles' % self.imdb_user
        self.imdb_list_link = self.imdb_link + '/list/%s/?view=simple&sort=date_added,desc&title_type=tvSeries,tvMiniSeries&start=1'
        self.imdb_list2_link = self.imdb_link + '/list/%s/?view=simple&sort=alpha,asc&title_type=tvSeries,tvMiniSeries&start=1'
        self.imdb_watchlist_link = self.imdb_link + '/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user
        self.imdb_watchlist2_link = self.imdb_link + '/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user

        #self.trakt_search_link = self.trakt_link + '/search/show?limit=%s&page=1&query=' % self.items_per_page
        self.trakt_history_link = self.trakt_link + '/users/me/history/shows?limit=%s&page=1' % self.items_per_page
        self.trakt_popular_link = self.trakt_link + '/shows/popular?limit=%s&page=1' % self.items_per_page
        self.trakt_featured_link = self.trakt_link + '/recommendations/shows?limit=%s&page=1' % self.items_per_page
        self.trakt_trending_link = self.trakt_link + '/shows/trending?limit=%s&page=1' % self.items_per_page
        self.trakt_anticipated_link = self.trakt_link + '/shows/anticipated?limit=%s&page=1' % self.items_per_page
        self.trakt_premieres_link = self.trakt_link + '/calendars/all/shows/premieres?limit=%s&page=1' % self.items_per_page
        self.trakt_update_link = self.trakt_link + '/shows/updates/%s?limit=%s&page=1' % ('%s', self.items_per_page)
        self.trakt_related_link = self.trakt_link + '/shows/%s/related'
        self.trakt_list_link = self.trakt_link + '/users/%s/lists/%s/items'
        self.trakt_lists_link = self.trakt_link + '/users/me/lists'
        self.trakt_likedlists_link = self.trakt_link + '/users/likes/lists?limit=1000000'
        self.trakt_collection_link = self.trakt_link + '/users/me/collection/shows'
        self.trakt_watchlist_link = self.trakt_link + '/users/me/watchlist/shows'
        self.trakt_played1_link = self.trakt_link + '/shows/played/weekly?limit=%s&page=1' % self.items_per_page
        self.trakt_played2_link = self.trakt_link + '/shows/played/monthly?limit=%s&page=1' % self.items_per_page
        self.trakt_played3_link = self.trakt_link + '/shows/played/yearly?limit=%s&page=1' % self.items_per_page
        self.trakt_played4_link = self.trakt_link + '/shows/played/all?limit=%s&page=1' % self.items_per_page
        self.trakt_collected1_link = self.trakt_link + '/shows/collected/weekly?limit=%s&page=1' % self.items_per_page
        self.trakt_collected2_link = self.trakt_link + '/shows/collected/monthly?limit=%s&page=1' % self.items_per_page
        self.trakt_collected3_link = self.trakt_link + '/shows/collected/yearly?limit=%s&page=1' % self.items_per_page
        self.trakt_collected4_link = self.trakt_link + '/shows/collected/all?limit=%s&page=1' % self.items_per_page
        self.trakt_watched1_link = self.trakt_link + '/shows/watched/weekly?limit=%s&page=1' % self.items_per_page
        self.trakt_watched2_link = self.trakt_link + '/shows/watched/monthly?limit=%s&page=1' % self.items_per_page
        self.trakt_watched3_link = self.trakt_link + '/shows/watched/yearly?limit=%s&page=1' % self.items_per_page
        self.trakt_watched4_link = self.trakt_link + '/shows/watched/all?limit=%s&page=1' % self.items_per_page


    def search_term_menu(self, select):
        navigator.navigator().addDirectoryItem('New Search...', 'tvshows_searchterm&select=%s' % select, 'search.png', 'DefaultTVShows.png')
        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS %s (ID Integer PRIMARY KEY AUTOINCREMENT, term);" % select)
        except:
            pass
        dbcur.execute("SELECT * FROM %s ORDER BY ID DESC" % select)
        delete_option = False
        for (id, term) in dbcur.fetchall():
            delete_option = True
            navigator.navigator().addDirectoryItem(term.title(), 'tvshows_searchterm&select=%s&name=%s' % (select, term), 'search.png', 'DefaultTVShows.png')
        dbcur.close()
        if delete_option:
            navigator.navigator().addDirectoryItem('Clear Search History', 'clear_search_cache&select=%s' % select, 'tools.png', 'DefaultAddonProgram.png')
        navigator.navigator().endDirectory(cached=False)


    def search_term(self, select, q=None):
        control.idle()
        if (q == None or q == ''):
            k = control.keyboard('', 'Search') ; k.doModal()
            q = k.getText() if k.isConfirmed() else None
        if (q == None or q == ''):
            return
        q = q.lower()
        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM %s WHERE term = ?" % select, (q,))
        dbcur.execute("INSERT INTO %s VALUES (?, ?)" % select, (None, q))
        dbcon.commit()
        dbcur.close()
        if select == 'tvshow':
            #url = self.trakt_search_link % urllib_parse.quote_plus(q)
            #url = self.imdb_search_link % urllib_parse.quote_plus(q)
            url = self.tmdb_search_link % urllib_parse.quote_plus(q)
            self.get(url)
        elif select == 'people':
            #url = self.imdb_persons_link + urllib_parse.quote_plus(q)
            #self.search_imdb_persons(url)
            self.search_tmdb_people(q)
        elif select == 'keywords':
            self.search_tmdb_keyword(q)
        elif select == 'companies':
            self.search_tmdb_companies(q)
        elif select == 'collections':
            self.search_tmdb_collection(q)


    def search_tmdb_people(self, q=None):
        query = urllib_parse.quote_plus(q)
        self.list = tmdb_utils.find_people(None, query, 'tv')
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def search_tmdb_keyword(self, q=None):
        query = urllib_parse.quote_plus(q)
        self.list = tmdb_utils.find_keyword(None, query, 'tv')
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def search_tmdb_companies(self, q=None):
        query = urllib_parse.quote_plus(q)
        self.list = tmdb_utils.find_companies(query, 'tv')
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def search_tmdb_collection(self, q=None):
        query = urllib_parse.quote_plus(q)
        self.list = tmdb_utils.find_collection(query)
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_genres(self):
        from resources.lib.indexers.metadata.tmdb import tmdb_various
        genres = tmdb_various.tv_genre_list
        for item in genres:
            self.list.append({'name': item[0], 'url': self.tmdb_genre_link % item[1], 'image': 'genres.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_languages(self):
        from resources.lib.indexers.metadata.tmdb import tmdb_various
        languages = tmdb_various.language_list
        for item in languages:
            self.list.append({'name': item[0], 'url': self.tmdb_language_link % item[1], 'image': 'languages.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_popular_companies(self):
        from resources.lib.indexers.metadata.tmdb import tmdb_production_companies
        companies = tmdb_production_companies.companies
        for item in companies:
            item_url = self.tmdb_link + '/3/discover/tv?api_key=%s&with_companies=%s&language=en-US&page=1' % (self.tmdb_key, '%s')
            #item_art = self.tmdb_image_link + item['image'] if 'image' in item and not item['image'] == None else 'tmdb.png'
            item_art = self.tmdb_image_link % ('300', item['image']) if 'image' in item and not item['image'] == None else 'tmdb.png'
            self.list.append({'name': item['name'], 'url': item_url % item['id'], 'image': item_art, 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_popular_keywords(self):
        from resources.lib.indexers.metadata.tmdb import tmdb_keywords
        keywords = tmdb_keywords.keywords_list
        for item in keywords:
            item_url = self.tmdb_link + '/3/discover/tv?api_key=%s&with_keywords=%s&language=en-US&page=1' % (self.tmdb_key, '%s')
            self.list.append({'name': item['name'], 'url': item_url % item['id'], 'image': 'tmdb.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_popular_people(self):
        self.list = tmdb_utils.get_popular_people(None, 'tv')
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_years(self):
        year = (self.datetime.strftime('%Y'))
        for i in range(int(year)+1, 1900, -1):
            self.list.append({'name': str(i), 'url': self.tmdb_year_link % str(i), 'image': 'years.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_decades(self):
        year = (self.datetime.strftime('%Y'))
        dec = int(year[:3]) * 10
        for i in range(dec, 1890, -10):
            self.list.append({'name': str(i) + 's', 'url': self.tmdb_decade_link % (str(i) + '-01-01', str(i+9) + '-01-01'), 'image': 'years.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_networks(self):
        from resources.lib.indexers.metadata.tmdb import tmdb_networks
        networks = tmdb_networks.networks
        for network in networks:
            network_name = network['name']
            network_id = network['id']
            network_origin_country = network['origin_country']
            network_url = self.tmdb_networks_link % network_id
            network_label = '%s (%s)' % (network_name, network_origin_country) if network_origin_country else network_name
            self.list.append({'name': network_label, 'url': network_url, 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def imdb_genres(self):
        from resources.lib.indexers.metadata.imdb import imdb_various
        genres = imdb_various.genre_list
        for genre in genres:
            self.list.append({'name': genre[0], 'url': self.imdb_genre_link % genre[1] if genre[2] else self.imdb_keyword_link % genre[1], 'image': 'genres.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def imdb_years(self):
        year = (self.datetime.strftime('%Y'))
        for i in range(int(year)-0, 1900, -1):
            self.list.append({'name': str(i), 'url': self.imdb_year_link % (str(i), str(i)), 'image': 'years.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def imdb_decades(self):
        year = (self.datetime.strftime('%Y'))
        dec = int(year[:3]) * 10
        for i in range(dec, 1890, -10):
            self.list.append({'name': str(i) + 's', 'url': self.imdb_decade_link % (str(i), str(i+9)), 'image': 'years.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def imdb_keywords(self):
        from resources.lib.indexers.metadata.imdb import imdb_various
        keywords = imdb_various.keywords_list
        for keyword in keywords:
            self.list.append({'name': keyword.replace('-', ' '), 'url': self.imdb_keywords_link % keyword, 'image': 'imdb.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def imdb_languages(self):
        from resources.lib.indexers.metadata.imdb import imdb_various
        languages = imdb_various.languages_list
        for language in languages:
            self.list.append({'name': language[0], 'url': self.imdb_language_link % language[1], 'image': 'languages.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def imdb_certifications(self):
        certificates = ['TV-G', 'TV-PG', 'TV-14', 'TV-MA']
        for i in certificates:
            self.list.append({'name': str(i), 'url': self.imdb_certification_link % str(i), 'image': 'certificates.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def search_imdb_persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.imdb_personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tvmaze_networks(self):
        from resources.lib.indexers.metadata.tvmaze import tvmaze_networks
        networks = tvmaze_networks.networks
        for i in networks:
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def webchannels(self):
        from resources.lib.indexers.metadata.tvmaze import tvmaze_networks
        webchannels = tvmaze_networks.webchannels
        for i in webchannels:
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tmdbTvLists(self):
        from resources.lib.indexers.metadata.tmdb import tmdb_userlists
        userlists = tmdb_userlists.tmdb_TvLists
        for i in userlists:
            self.list.append({'name': i[0], 'url': self.tmdb_userlists_link % i[1], 'image': 'tmdb.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def imdbUserLists(self):
        from resources.lib.indexers.metadata.imdb import imdb_userlists
        userlists = imdb_userlists.imdb_TvLists
        for i in userlists:
            self.list.append({'name': i[0], 'url': self.imdb_userlists_link % i[1], 'image': 'imdb.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def userlists_trakt(self):
        userlists = []
        try:
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            activity = trakt.getActivity()
            userlists += self.trakt_user_list(self.trakt_lists_link, self.trakt_user)
        except:
            #log_utils.log('userlists', 1)
            pass
        self.list = userlists
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.list = sorted(self.list, key=lambda k: (k['image'], k['name'].lower()))
        self.addDirectory(self.list)
        return self.list


    def userlists_trakt_liked(self):
        userlists = []
        try:
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            activity = trakt.getActivity()
            userlists += self.trakt_user_list(self.trakt_likedlists_link, self.trakt_user)
        except:
            #log_utils.log('userlists', 1)
            pass
        self.list = userlists
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.list = sorted(self.list, key=lambda k: (k['image'], k['name'].lower()))
        self.addDirectory(self.list)
        return self.list


    def userlists_imdb(self):
        userlists = []
        try:
            if self.imdb_user == '':
                raise Exception()
            userlists += self.imdb_user_list(self.imdb_lists_link)
        except:
            #log_utils.log('userlists', 1)
            pass
        self.list = userlists
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.list = sorted(self.list, key=lambda k: (k['image'], k['name'].lower()))
        self.addDirectory(self.list)
        return self.list


    def userlists_tmdb(self):
        userlists = []
        try:
            if tmdb_utils.getTMDbCredentialsInfo() == False:
                raise Exception()
            userlists += tmdb_utils.get_created_lists(self.tmdb_userlists_link)
        except:
            #log_utils.log('userlists', 1)
            pass
        self.list = userlists
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.list = sorted(self.list, key=lambda k: (k['image'], k['name'].lower()))
        self.addDirectory(self.list)
        return self.list


    def trakt_list(self, url, user):
        try:
            q = dict(urllib_parse.parse_qsl(urllib_parse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib_parse.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urllib_parse.urlparse(url).query, '') + '?' + q
            result = trakt.getTraktAsJson(u)
            items = []
            for i in result:
                try:
                    items.append(i['show'])
                except:
                    pass
            if len(items) == 0:
                items = result
        except:
            #log_utils.log('trakt_list', 1)
            return
        try:
            q = dict(urllib_parse.parse_qsl(urllib_parse.urlsplit(url).query))
            if not int(q['limit']) == len(items):
                raise Exception()
            q.update({'page': str(int(q['page']) + 1)})
            q = (urllib_parse.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urllib_parse.urlparse(url).query, '') + '?' + q
            next = six.ensure_str(next)
        except:
            next = ''
        for item in items:
            try:
                title = item['title']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(title)
                year = item.get('year')
                if year:
                    year = re.sub(r'[^0-9]', '', str(year))
                else:
                    year = '0'
                if int(year) > int((self.datetime).strftime('%Y')):
                    if self.shownoyear != 'true':
                        raise Exception()
                imdb = item.get('ids', {}).get('imdb')
                if not imdb:
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub(r'[^0-9]', '', str(imdb))
                tmdb = item.get('ids', {}).get('tmdb')
                if not tmdb:
                    tmdb == '0'
                else:
                    tmdb = str(tmdb)
                tvdb = item.get('ids', {}).get('tvdb')
                if not tvdb:
                    tvdb = '0'
                else:
                    tvdb = re.sub('[^0-9]', '', str(tvdb))
                paused_at = item.get('paused_at', '0') or '0'
                paused_at = re.sub('[^0-9]+', '', paused_at)
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'next': next, 'paused_at': paused_at})
            except:
                #log_utils.log('trakt_list', 1)
                pass
        return self.list


    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
        except:
            #log_utils.log('trakt_user_list', 1)
            pass
        for item in items:
            try:
                try:
                    name = item['list']['name']
                except:
                    name = item['name']
                name = client.replaceHTMLCodes(six.ensure_str(name))
                try:
                    url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except:
                    url = ('me', item['ids']['slug'])
                url = self.trakt_list_link % url
                url = six.ensure_str(url)
                self.list.append({'name': name, 'url': url, 'context': url, 'image': 'trakt.png'})
            except:
                #log_utils.log('trakt_user_list', 1)
                pass
        return self.list


    def imdb_list(self, url):
        try:
            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days=int(i))).strftime('%Y-%m-%d'))
            def imdb_watchlist_id(url):
                result = client.scrapePage(url).text
                return client.parseDOM(result, 'meta', ret='content', attrs={'property': 'pageId'})[0]
            if url == self.imdb_watchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdb_list_link % url
            elif url == self.imdb_watchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdb_list2_link % url
            result = client.scrapePage(url).text
            result = control.six_decode(result)
            result = result.replace('\n', ' ')
            items = client.parseDOM(result, 'div', attrs = {'class': 'lister-item .*?'})
            items += client.parseDOM(result, 'div', attrs = {'class': 'list_item.*?'})
        except:
            #log_utils.log('imdb_list', 1)
            return
        try:
            result = result.replace(r'"class=".*?ister-page-nex', '" class="lister-page-nex')
            next = client.parseDOM(result, 'a', ret='href', attrs = {'class': r'.*?ister-page-nex.*?'})
            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs = {'class': u'pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]
            next = url.replace(urllib_parse.urlparse(url).query, urllib_parse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(six.ensure_str(next))
        except:
            next = ''
        for item in items:
            try:
                title = client.parseDOM(item, 'a')[1]
                title = client.replaceHTMLCodes(six.ensure_str(title))
                year = client.parseDOM(item, 'span', attrs = {'class': r'lister-item-year.*?'})
                year += client.parseDOM(item, 'span', attrs = {'class': r'year_type'})
                try:
                    year = re.findall(r'(\d{4})', str(year)[0])[0]
                except:
                    year = '0'
                year = six.ensure_str(year)
                if int(year) > int(self.datetime.strftime('%Y')):
                    if self.shownoyear != 'true':
                        raise Exception()
                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = six.ensure_str(imdb)
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'next': next})
            except:
                #log_utils.log('imdb_list', 1)
                pass
        return self.list


    def imdb_person_list(self, url):
        try:
            result = client.scrapePage(url).text
            items = client.parseDOM(result, 'div', attrs = {'class': '.+? mode-detail'})
        except:
            #log_utils.log('imdb_person_list', 1)
            return
        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
                name = client.replaceHTMLCodes(six.ensure_str(name))
                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.imdb_person_link % url
                url = client.replaceHTMLCodes(six.ensure_str(url))
                image = client.parseDOM(item, 'img', ret='src')[0]
                image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(six.ensure_str(image))
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                #log_utils.log('imdb_person_list', 1)
                pass
        return self.list


    def imdb_user_list(self, url):
        try:
            result = client.scrapePage(url).text
            items = client.parseDOM(result, 'li', attrs = {'class': 'ipl-zebra-list__item user-list'})
        except:
            #log_utils.log('imdb_user_list', 1)
            pass
        if control.setting('imdb.sort.order') == '1':
            list = self.imdb_list2_link
        else:
            list = self.imdb_list_link
        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(six.ensure_str(name))
                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url = url.split('/list/', 1)[-1].strip('/')
                url = list % url
                url = client.replaceHTMLCodes(six.ensure_str(url))
                self.list.append({'name': name, 'url': url, 'context': url, 'image': 'imdb.png'})
            except:
                #log_utils.log('imdb_user_list', 1)
                pass
        return self.list


    def tvmaze_list(self, url):
        try:
            result = client.scrapePage(url).text
            result = client.parseDOM(result, 'div', attrs = {'id': 'w1'})
            items = client.parseDOM(result, 'span', attrs = {'class': 'title'})
            items = [client.parseDOM(i, 'a', ret='href') for i in items]
            items = [i[0] for i in items if len(i) > 0]
            items = [re.findall('/(\d+)/', i) for i in items]
            items = [i[0] for i in items if len(i) > 0]
            next = ''; last = []; nextp = []
            page = int(str(url.split('&page=', 1)[1]))
            next = '%s&page=%s' % (url.split('&page=', 1)[0], page+1)
            last = client.parseDOM(result, 'li', attrs = {'class': 'last disabled'})
            nextp = client.parseDOM(result, 'li', attrs = {'class': 'next'})
            if last != [] or nextp == []:
                next = ''
        except:
            #log_utils.log('tvmaze_list', 1)
            return
        def items_list(i):
            try:
                url = self.tvmaze_info_link % i
                item = client.scrapePage(url).json()
                title = item['name']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(six.ensure_str(title))
                premiered = item['premiered']
                try:
                    premiered = re.findall('(\d{4}-\d{2}-\d{2})', premiered)[0]
                except:
                    premiered = '0'
                premiered = six.ensure_str(premiered)
                year = item['premiered']
                try:
                    year = re.findall('(\d{4})', year)[0]
                except:
                    year = '0'
                year = six.ensure_str(year)
                if int(year) > int(self.datetime.strftime('%Y')):
                    if self.shownoyear != 'true':
                        raise Exception()
                imdb = item['externals']['imdb']
                if imdb == None or imdb == '':
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = six.ensure_str(imdb)
                tvdb = item['externals']['thetvdb']
                if tvdb == None or tvdb == '':
                    tvdb = '0'
                else:
                    tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = six.ensure_str(tvdb)
                try:
                    content = item['type'].lower()
                except:
                    content = '0'
                if content == None or content == '':
                    content = '0'
                content = six.ensure_str(content)
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'imdb': imdb, 'tvdb': tvdb, 'tmdb': '0', 'content': content, 'next': next})
            except:
                #log_utils.log('tvmaze_list', 1)
                pass
        try:
            threads = []
            for i in items:
                threads.append(workers.Thread(items_list, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self.list
        except:
            #log_utils.log('tvmaze_list', 1)
            return


    def tmdb_list(self, url):
        try:
            result = client.scrapePage(url).json()
            if 'results' in result:
                items = result['results']
            elif 'items' in result:
                items = result['items']
            elif 'parts' in result:
                items = result['parts']
            elif 'cast' in result:
                items = result['cast']
        except:
            #log_utils.log('tmdb_list', 1)
            return
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            if 'page=' not in url:
                raise Exception()
            next = '%s&page=%s' % (url.split('&page=', 1)[0], page+1)
        except:
            next = ''
        for item in items:
            try:
                if 'media_type' in item and not item['media_type'] == 'tv':
                    raise Exception()
                tmdb = str(item.get('id'))
                try:
                    title = item['name']
                except:
                    title = ''
                title = six.ensure_str(title)
                try:
                    originaltitle = item['original_name']
                except:
                    originaltitle = ''
                originaltitle = six.ensure_str(originaltitle)
                if not originaltitle:
                    originaltitle = title
                try:
                    premiered = item['first_air_date']
                except:
                    premiered = ''
                if not premiered:
                    premiered = '0'
                try:
                    year = re.findall('(\d{4})', premiered)[0]
                except:
                    year = ''
                if not year:
                    year = '0'
                self.list.append({'title': title, 'originaltitle': originaltitle, 'premiered': premiered, 'year': year, 'imdb': '0', 'tmdb': tmdb, 'tvdb': '0', 'next': next})
            except:
                #log_utils.log('tmdb_list', 1)
                pass
        return self.list


    def get_fanart_tv_artwork(self, id):
        try:
            art = client.scrapePage(self.fanart_tv_art_link % id, headers=self.fanart_tv_headers).json()
            try:
                poster = art['tvposter']
                poster = [x for x in poster if x.get('lang') == 'en'][::-1] + [x for x in poster if x.get('lang') in ['00', '']][::-1]
                poster = poster[0]['url']
                if poster == '' or poster == None or poster == []:
                    poster = '0'
            except:
                poster = '0'
            try:
                if 'showbackground' in art:
                    fanart = art['showbackground']
                else:
                    fanart = art['tvthumb']
                fanart = [x for x in fanart if x.get('lang') == 'en'][::-1] + [x for x in fanart if x.get('lang') in ['00', '']][::-1]
                fanart = fanart[0]['url']
                if fanart == '' or fanart == None or fanart == []:
                    fanart = '0'
            except:
                fanart = '0'
            try:
                banner = art['tvbanner']
                banner = [x for x in banner if x.get('lang') == 'en'][::-1] + [x for x in banner if x.get('lang') in ['00', '']][::-1]
                banner = banner[0]['url']
                if banner == '' or banner == None or banner == []:
                    banner = '0'
            except:
                banner = '0'
            try:
                if 'hdtvlogo' in art:
                    clearlogo = art['hdtvlogo']
                else:
                    clearlogo = art['clearlogo']
                clearlogo = [x for x in clearlogo if x.get('lang') == 'en'][::-1] + [x for x in clearlogo if x.get('lang') in ['00', '']][::-1]
                clearlogo = clearlogo[0]['url']
                if clearlogo == '' or clearlogo == None or clearlogo == []:
                    clearlogo = '0'
            except:
                clearlogo = '0'
            try:
                if 'hdclearart' in art:
                    clearart = art['hdclearart']
                else:
                    clearart = art['clearart']
                clearart = [x for x in clearart if x.get('lang') == 'en'][::-1] + [x for x in clearart if x.get('lang') in ['00', '']][::-1]
                clearart = clearart[0]['url']
                if clearart == '' or clearart == None or clearart == []:
                    clearart = '0'
            except:
                clearart = '0'
            try:
                if 'tvthumb' in art:
                    landscape = art['tvthumb']
                else:
                    landscape = art['showbackground']
                landscape = [x for x in landscape if x.get('lang') == 'en'][::-1] + [x for x in landscape if x.get('lang') in ['00', '']][::-1]
                landscape = landscape[0]['url']
                if landscape == '' or landscape == None or landscape == []:
                    landscape = '0'
            except:
                landscape = '0'
        except:
            poster = fanart = banner = clearlogo = clearart = landscape = '0'
        return poster, fanart, banner, clearlogo, clearart, landscape


    def final_info(self, i):
        try:
            if self.list[i]['metacache'] == True:
                return
            imdb = self.list[i]['imdb'] if 'imdb' in self.list[i] else '0'
            tmdb = self.list[i]['tmdb'] if 'tmdb' in self.list[i] else '0'
            tvdb = self.list[i]['tvdb'] if 'tvdb' in self.list[i] else '0'
            if tmdb == '0' and not imdb == '0':
                try:
                    temp_item = tmdb_utils.find_tvshow_by_external_source(imdb=imdb)
                    tmdb = temp_item['id']
                except:
                    tmdb = ''
                if not tmdb:
                    try:
                        temp_item = trakt.getTVShowSummary(imdb)
                        tmdb = temp_item.get('ids', {}).get('tmdb')
                    except:
                        tmdb = '0'
            url = self.tmdb_info_link % tmdb
            item = client.scrapePage(url).json()
            if item == None:
                raise Exception()
            if imdb == '0':
                try:
                    imdb = item['external_ids']['imdb_id']
                except:
                    imdb = ''
                if not imdb:
                    try:
                        temp_item = trakt.getTVShowSummary(tmdb)
                        imdb = temp_item.get('ids', {}).get('imdb')
                    except:
                        imdb = '0'
            if tvdb == '0':
                try:
                    tvdb = item['external_ids']['tvdb_id']
                except:
                    tvdb = ''
                if not tvdb:
                    try:
                        temp_item = trakt.getTVShowSummary(tmdb)
                        tvdb = temp_item.get('ids', {}).get('tvdb')
                    except:
                        tvdb = '0'
            
            title = self.list[i]['title'] or item['name']
            title = client.replaceHTMLCodes(title)
            originaltitle = self.list[i]['originaltitle'] or item['original_name']
            originaltitle = client.replaceHTMLCodes(originaltitle)
            premiered = item['first_air_date'] or self.list[i]['premiered']
            if premiered:
                premiered = re.compile(r'(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                if premiered == '' or premiered == None:
                    premiered = '0'
            year = self.list[i]['year']
            if year == '' or year == '0' or year == None or year == []:
                year = re.compile('(\d{4})').findall(premiered)[0]
                if year == '' or year == None:
                    year = '0'
            if self.studio_artwork == 'true':
                #studio = item['production_companies']
                studio = item['networks']
                if studio:
                    studio = [x['name'] for x in studio][0]
                    if studio == '' or studio == None or studio == []:
                        studio = '0'
                else:
                    studio = '0'
            else:
                studio = '0'
            genre = item['genres']
            if genre:
                genre = [x['name'] for x in genre]
                genre = ' / '.join(genre).strip()
                if genre == '' or genre == None or genre == []:
                    genre = '0'
            else:
                genre = '0'
            try:
                duration = item['episode_run_time'][0]
                duration = str(duration)
            except:
                duration = ''
            if not duration:
                duration = '0'
            try:
                status = item['status']
            except:
                status = ''
            if not status:
                status = '0'
            rating = str(item['vote_average'])
            if rating == '' or rating == '0' or rating == '0.0' or rating == None or rating == []:
                rating = '0'
            votes = str(item['vote_count'])
            votes = str(format(int(votes), ',d'))
            if votes == '' or votes == '0' or votes == None or votes == []:
                votes = '0'
            tagline = item['tagline']
            if not tagline:
                tagline = '0'
            
            plot = item['overview']
            if not plot:
                try:
                    plot = self.list[i]['plot']
                except:
                    plot = '0'
            try:
                mpaa = item['content_ratings']['results']
                mpaa = [x['rating'] for x in mpaa if x['iso_3166_1'] == 'US'][0]
            except:
                mpaa = ''
            if not mpaa:
                mpaa = '0'
        
            castwiththumb = []
            try:
                r_cast = item['credits']['cast'][:30]
                for person in r_cast:
                    _icon = person['profile_path']
                    #icon = self.tmdb_image_link + _icon if _icon else ''
                    icon = self.tmdb_image_link % ('185', _icon) if _icon else ''
                    castwiththumb.append({'name': person['name'], 'role': person['character'], 'thumbnail': icon})
            except:
                pass
            if not castwiththumb:
                castwiththumb = '0'

            poster1 = item['poster_path']
            if not (poster1 == '' or poster1 == None):
                #poster1 = self.tmdb_image_link + poster1
                poster1 = self.tmdb_image_link % ('500', poster1)
            else:
                poster1 = '0'
            fanart1 = item['backdrop_path']
            if not (fanart1 == '' or fanart1 == None):
                #fanart1 = self.tmdb_image_link + fanart1
                fanart1 = self.tmdb_image_link % ('1280', fanart1)
            else:
                fanart1 = '0'
            if self.hq_artwork == 'true':
                poster2, fanart2, banner, clearlogo, clearart, landscape, discart = self.get_fanart_tv_artwork(imdb)
            else:
                poster2 = fanart2 = banner = clearlogo = clearart = landscape = discart = '0'
            poster = poster2 if not poster2 == '0' else poster1
            fanart = fanart2 if not fanart2 == '0' else fanart1
            item = {'title': title, 'originaltitle': originaltitle, 'premiered': premiered, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'status': status,
                'poster': poster, 'fanart': fanart, 'banner': banner, 'clearlogo': clearlogo, 'clearart': clearart, 'landscape': landscape, 'discart': discart,
                'studio': studio, 'genre': genre, 'duration': duration, 'mpaa': mpaa, 'castwiththumb': castwiththumb, 'plot': plot, 'tagline': tagline
            }
            item = dict((k,v) for k, v in six.iteritems(item) if not v == '0')
            self.list[i].update(item)
            meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)
        except:
            #log_utils.log('final_info', 1)
            pass


    def worker(self):
        self.meta = []
        total = len(self.list)
        for i in range(0, total):
            self.list[i].update({'metacache': False})
        self.list = metacache.fetch(self.list, self.lang, self.user)
        for r in range(0, total, 40):
            threads = []
            for i in range(r, r+40):
                if i < total:
                    threads.append(workers.Thread(self.final_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
        if self.meta:
            metacache.insert(self.meta)
        self.list = [i for i in self.list]


    def get(self, url, idx=True, create_directory=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass
            try:
                u = urllib_parse.urlparse(url).netloc.lower()
            except:
                pass
            if u in self.tmdb_link and ('/list/' in url or '/collection/' in url):
                self.list = cache.get(self.tmdb_list, 24, url)
                self.list = sorted(self.list, key=lambda k: k['year'])
                if idx == True:
                    self.worker()
            elif u in self.tmdb_link and self.tmdb_search_link in url:
                self.list = cache.get(self.tmdb_list, 1, url)
                if idx == True:
                    self.worker()
            elif u in self.tmdb_link:
                self.list = cache.get(self.tmdb_list, 24, url)
                if idx == True:
                    self.worker()
            elif u in self.trakt_link and '/users/' in url:
                try:
                    if url == self.trakt_history_link:
                        raise Exception()
                    if not '/users/me/' in url:
                        raise Exception()
                    #if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user):
                        #raise Exception()
                    self.list = cache.get(self.trakt_list, 720, url, self.trakt_user)
                except:
                    self.list = self.trakt_list(url, self.trakt_user)
                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: k['title'])
                if idx == True:
                    self.worker()
            #elif u in self.trakt_link and self.trakt_search_link in url:
                #self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                #if idx == True:
                    #self.worker()
            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx == True:
                    self.worker()
            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 1, url)
                if idx == True:
                    self.worker()
            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 24, url)
                if idx == True:
                    self.worker()
            elif u in self.tvmaze_link:
                self.list = cache.get(self.tvmaze_list, 24, url)
                if idx == True:
                    self.worker()
            if idx == True and create_directory == True:
                self.tvshowDirectory(self.list)
            return self.list
        except:
            #log_utils.log('get', 1)
            pass


    def tvshowDirectory(self, items):
        if items == None or len(items) == 0:
            control.idle()
            #sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        traktCredentials = trakt.getTraktCredentialsInfo()
        tmdbCredentials = tmdb_utils.getTMDbCredentialsInfo()
        try:
            isOld = False
            control.item().getArt('type')
        except:
            isOld = True
        indicators = playcount.getTVShowIndicators()#refresh=True) if action == 'tvshows' else playcount.getTVShowIndicators()
        watchedMenu = '[I]Watched in Trakt[/I]' if trakt.getTraktIndicatorsInfo() == True else '[I]Watched in Scrubs[/I]'
        unwatchedMenu = '[I]Unwatched in Trakt[/I]' if trakt.getTraktIndicatorsInfo() == True else '[I]Unwatched in Scrubs[/I]'
        if self.trailer_source == '0':
            trailerAction = 'tmdb_trailer'
        elif self.trailer_source == '1':
            trailerAction = 'yt_trailer'
        else:
            trailerAction = 'imdb_trailer'
        nextMenu = '[I]Next Page[/I]'
        for i in items:
            try:
                label = i['title']
                status =  i['status']
                try:
                    label = '%s (%s)' % (label, status)
                    premiered = i['premiered']
                    if (premiered == '0' and status in ['Upcoming', 'In Production', 'Planned']) or (int(re.sub('[^0-9]', '', premiered)) > int(re.sub('[^0-9]', '', str(self.today_date)))):
                        label = '[COLOR %s][I]%s[/I][/COLOR]' % (self.unairedcolor, label)
                except:
                    pass
                poster = i['poster'] if 'poster' in i and not i['poster'] == '0' else addonPoster
                fanart = i['fanart'] if 'fanart' in i and not i['fanart'] == '0' else addonFanart
                banner1 = i.get('banner', '')
                banner = banner1 or fanart or addonBanner
                if 'landscape' in i and not i['landscape'] == '0':
                    landscape = i['landscape']
                else:
                    landscape = fanart
                systitle = sysname = urllib_parse.quote_plus(i['title'])
                sysimage = urllib_parse.quote_plus(poster)
                seasons_meta = {'poster': poster, 'fanart': fanart, 'banner': banner, 'clearlogo': i.get('clearlogo', '0'), 'clearart': i.get('clearart', '0'), 'landscape': landscape}
                sysmeta = urllib_parse.quote_plus(json.dumps(seasons_meta))
                imdb, tvdb, tmdb, year = i.get('imdb', ''), i.get('tvdb', ''), i.get('tmdb', ''), i.get('year', '')
                meta = dict((k,v) for k, v in six.iteritems(i) if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tvdb_id': tvdb})
                meta.update({'tmdb_id': tmdb})
                meta.update({'mediatype': 'tvshow'})
                meta.update({'tvshowtitle': i['title']})
                meta.update({'trailer': '%s?action=%s&name=%s&tmdb=%s&imdb=%s' % (sysaddon, trailerAction, systitle, tmdb, imdb)})
                if not 'duration' in i:
                    meta.update({'duration': '60'})
                elif i['duration'] == '0':
                    meta.update({'duration': '60'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                cm = []
                cm.append(('Clean Tools Widget', 'RunPlugin(%s?action=cleantools_widget)' % sysaddon))
                cm.append(('Clear Providers', 'RunPlugin(%s?action=clear_sources)' % sysaddon))
                cm.append(('Find Similar', 'Container.Update(%s?action=tvshows&url=%s)' % (sysaddon, self.trakt_related_link % imdb)))
                cm.append(('Queue Item', 'RunPlugin(%s?action=queue_item)' % sysaddon))
                if traktCredentials == True:
                    cm.append(('Trakt Manager', 'RunPlugin(%s?action=trakt_manager&name=%s&tmdb=%s&content=tvshow)' % (sysaddon, sysname, tmdb)))
                if tmdbCredentials == True:
                    cm.append(('TMDb Manager', 'RunPlugin(%s?action=tmdb_manager&name=%s&tmdb=%s&content=tvshow)' % (sysaddon, sysname, tmdb)))
                cm.append(('Add to Library', 'RunPlugin(%s?action=tvshow_to_library&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, systitle, year, imdb, tmdb)))
                if isOld == True:
                    cm.append(('Information', 'Action(Info)'))
                try:
                    overlay = int(playcount.getTVShowOverlay(indicators, imdb, tmdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=tvshows_playcount&name=%s&imdb=%s&tmdb=%s&query=6)' % (sysaddon, systitle, imdb, tmdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=tvshows_playcount&name=%s&imdb=%s&tmdb=%s&query=7)' % (sysaddon, systitle, imdb, tmdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                try:
                    item = control.item(label=label, offscreen=True)
                except:
                    item = control.item(label=label)
                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'landscape': landscape})
                if settingFanart == 'true':
                    art.update({'fanart': fanart})
                else:
                    art.update({'fanart': addonFanart})
                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})
                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})
                try:
                    castwiththumb = i.get('castwiththumb')
                    if castwiththumb and not castwiththumb == '0':
                        if control.getKodiVersion() >= 18:
                            item.setCast(castwiththumb)
                        else:
                            cast = [(p['name'], p['role']) for p in castwiththumb]
                            meta.update({'cast': cast})
                except:
                    pass
                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels=control.metadataClean(meta))
                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)
                url = '%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&meta=%s' % (sysaddon, systitle, year, imdb, tmdb, sysmeta)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                #log_utils.log('tvshowDirectory', 1)
                pass
        try:
            url = items[0]['next']
            if url == '':
                raise Exception()
            icon = control.addonNext()
            url = '%s?action=tvshows&url=%s' % (sysaddon, urllib_parse.quote_plus(url))
            try:
                item = control.item(label=nextMenu, offscreen=True)
            except:
                item = control.item(label=nextMenu)
            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon, 'fanart': addonFanart})
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            #log_utils.log('tvshowDirectory', 1)
            pass
        control.content(syshandle, 'tvshows')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('tvshows', {'skin.aeon.nox.silvo' : 50, 'skin.estuary': 55, 'skin.confluence': 500}) #View 50 List #View 501 LowList


    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0:
            control.idle()
            #sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonFanart = control.addonFanart()
        addonThumb = control.addonThumb()
        artPath = control.artPath()
        for i in items:
            try:
                name = i['name']
                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath == None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb
                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib_parse.quote_plus(i['url'])
                except:
                    pass
                cm = []
                cm.append(('Clean Tools Widget', 'RunPlugin(%s?action=cleantools_widget)' % sysaddon))
                if queue == True:
                    cm.append(('Queue Item', 'RunPlugin(%s?action=queue_item)' % sysaddon))
                try:
                    cm.append(('Add to Library', 'RunPlugin(%s?action=tvshows_to_library&url=%s)' % (sysaddon, urllib_parse.quote_plus(i['context']))))
                except:
                    pass
                try:
                    item = control.item(label=name, offscreen=True)
                except:
                    item = control.item(label=name)
                item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': addonFanart})
                item.addContextMenuItems(cm)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                #log_utils.log('addDirectory', 1)
                pass
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


