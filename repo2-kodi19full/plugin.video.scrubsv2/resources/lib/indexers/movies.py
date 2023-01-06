# -*- coding: utf-8 -*-

import re
import os
import sys
import datetime

import simplejson as json
import six
from six.moves import range, urllib_parse, zip

from resources.lib.indexers import navigator

from resources.lib.modules import tmdb_utils
from resources.lib.modules import trakt
from resources.lib.modules import bookmarks
from resources.lib.modules import cleantitle
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views
from resources.lib.modules import utils
from resources.lib.modules import log_utils

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

params = dict(urllib_parse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

action = params.get('action')


class movies:
    def __init__(self):
        self.list = []
        self.datetime = datetime.datetime.utcnow()
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.year_date = (self.datetime - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        self.month_date = (self.datetime - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tmdb_key = control.setting('tmdb.api')
        if self.tmdb_key == '' or self.tmdb_key == None:
            self.tmdb_key = 'c8b7db701bac0b26edfcc93b39858972'
        self.fanart_tv_headers = {'api-key': 'cb2f78390c6f7cbc5d1c9a257e013e5c'}
        self.fanart_tv_user = control.setting('fanart.api')
        if not self.fanart_tv_user == '' or self.fanart_tv_user == None:
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})
        self.user = str(control.setting('fanart.api')) + str(control.setting('tmdb.api'))
        self.shownoyear = control.setting('show.noyear') or 'false'
        self.unairedcolor = control.setting('unaired.color')
        if self.unairedcolor == '':
            self.unairedcolor = 'darkred'
        self.lang = control.apiLanguage()['tmdb'] or 'en'
        self.items_per_page = str(control.setting('items.per.page')) or '20'
        self.settingFanart = control.setting('fanart') or 'false'
        self.hq_artwork = control.setting('hq.artwork') or 'false'
        self.trailer_source = control.setting('trailer.source') or '2'
        self.studio_artwork = control.setting('studio.artwork') or 'false'
        self.trakt_link = 'https://api.trakt.tv'
        self.imdb_link = 'https://www.imdb.com'
        self.tmdb_link = 'https://api.themoviedb.org'
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/movies/%s'
        self.fanart_tv_level_link = 'http://webservice.fanart.tv/v3/level'
        #self.tmdb_image_link = 'https://image.tmdb.org/t/p/original'
        self.tmdb_image_link = 'https://image.tmdb.org/t/p/w%s%s'
        self.tmdb_info_link = self.tmdb_link + '/3/movie/%s?api_key=%s&language=en-US&append_to_response=credits,releases' % ('%s', self.tmdb_key)

        self.tmdb_search_link = self.tmdb_link + '/3/search/movie?api_key=%s&query=%s&language=en-US&include_adult=false&page=1' % (self.tmdb_key, '%s')
        self.tmdb_popular_link = self.tmdb_link + '/3/movie/popular?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_now_playing_link = self.tmdb_link + '/3/movie/now_playing?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_toprated_link = self.tmdb_link + '/3/movie/top_rated?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_upcoming_link = self.tmdb_link + '/3/movie/upcoming?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_trending_day_link = self.tmdb_link + '/3/trending/movie/day?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_trending_week_link = self.tmdb_link + '/3/trending/movie/week?api_key=%s&language=en-US&page=1' % self.tmdb_key
        self.tmdb_featured_link = self.tmdb_link + '/3/discover/movie?api_key=%s&vote_count.gte=100&sort_by=first_air_date.desc&language=en-US&include_adult=false&page=1' % self.tmdb_key
        self.tmdb_premiere_link = self.tmdb_link + '/3/discover/movie?api_key=%s&first_air_date.gte=%s&first_air_date.lte=%s&language=en-US&include_adult=false&page=1' % (self.tmdb_key, self.year_date, self.today_date)
        self.tmdb_views_link = self.tmdb_link + '/3/discover/movie?api_key=%s&vote_count.gte=100&sort_by=vote_average.desc&language=en-US&include_adult=false&page=1' % self.tmdb_key
        self.tmdb_in_theatres_link = self.tmdb_link + '/3/discover/movie?api_key=%s&release_date.gte=date[90]&release_date.lte=date[0]&language=en-US&include_adult=false&page=1' % self.tmdb_key
        self.tmdb_year_link = self.tmdb_link + '/3/discover/movie?api_key=%s&primary_release_year=%s&language=en-US&include_adult=false&page=1' % (self.tmdb_key, '%s')
        self.tmdb_decade_link = self.tmdb_link + '/3/discover/movie?api_key=%s&primary_release_date.gte=%s&primary_release_date.lte=%s&language=en-US&include_adult=false&page=1' % (self.tmdb_key, '%s', '%s')
        self.tmdb_language_link = self.tmdb_link + '/3/discover/movie?api_key=%s&with_original_language=%s&language=en-US&include_adult=false&page=1' % (self.tmdb_key, '%s')
        self.tmdb_certification_link = self.tmdb_link + '/3/discover/movie?api_key=%s&certification_country=US&certification=%s&language=en-US&include_adult=false&page=1' % (self.tmdb_key, '%s')
        self.tmdb_genre_link = self.tmdb_link + '/3/discover/movie?api_key=%s&with_genres=%s&language=en-US&include_adult=false&page=1' % (self.tmdb_key, '%s')
        self.tmdb_collections_link = self.tmdb_link + '/3/collection/%s?api_key=%s&language=en-US&page=1' % ('%s', self.tmdb_key)
        self.tmdb_userlists_link = self.tmdb_link + '/3/list/%s?api_key=%s&language=en-US&page=1' % ('%s', self.tmdb_key)
        self.tmdb_jewtestmovies_link = self.tmdb_userlists_link % ('97123')
        self.tmdb_jewmovies_link = self.tmdb_userlists_link % ('86696')
        self.tmdb_favorites_link = tmdb_utils.get_movie_favorites()
        self.tmdb_watchlist_link = tmdb_utils.get_movie_watchlist()

        self.imdb_search_link = self.imdb_link + '/find?q=%s&s=tt&ttype=ft'
        self.imdb_person_link = self.imdb_link + '/search/title?title_type=movie,short,tvMovie&production_status=released&role=%s&sort=year,desc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_persons_link = self.imdb_link + '/search/name?count=100&name='
        self.imdb_personlist_link = self.imdb_link + '/search/name?count=100&gender=male,female'
        self.imdb_year_link = self.imdb_link + '/search/title?title_type=movie,tvMovie&production_status=released&year=%s,%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', '%s', self.items_per_page)
        self.imdb_added_link  = self.imdb_link + '/search/title?title_type=movie,tvMovie&languages=en&num_votes=500,&production_status=released&release_date=%s,%s&sort=release_date,desc&count=%s&start=1' % (self.year_date, self.today_date, self.items_per_page)
        self.imdb_theaters_link = self.imdb_link + '/search/title?title_type=feature&release_date=date[120],date[0]&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page
        self.imdb_theaters1_link = self.imdb_link + '/search/title?title_type=feature&num_votes=1000,&countries=us&languages=en&release_date=date[90],date[0]&sort=release_date,desc&count=%s&start=1' % self.items_per_page
        self.imdb_theaters2_link = self.imdb_link + '/showtimes/location?ref_=inth_ov_sh_sm'
        self.imdb_coming_soon_link = self.imdb_link + '/coming-soon/?ref_=hm_cs_sm'
        self.imdb_boxoffice_link = self.imdb_link + '/search/title?title_type=movie,tvMovie&production_status=released&sort=boxoffice_gross_us,desc&count=%s&start=1' % self.items_per_page
        self.imdb_featured_link = self.imdb_link + '/search/title?title_type=movie,tvMovie&production_status=released&release_date=date[365],date[60]&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page
        self.imdb_popular_link = self.imdb_link + '/search/title?title_type=movie,tvMovie&production_status=released&groups=top_1000&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page
        self.imdb_oscars_link = self.imdb_link + '/search/title?title_type=movie,tvMovie&production_status=released&groups=oscar_best_picture_winners&sort=year,desc&count=%s&start=1' % self.items_per_page
        self.imdb_rating_link = self.imdb_link + '/search/title?title_type=movie,tvMovie&num_votes=5000,&release_date=,date[0]&sort=user_rating,desc&count=%s&start=1' % self.items_per_page
        self.imdb_views_link = self.imdb_link + '/search/title?title_type=movie,tvMovie&production_status=released&sort=num_votes,desc&count=%s&start=1' % self.items_per_page
        self.imdb_genre_link = self.imdb_link + '/search/title?title_type=feature,tv_movie,documentary&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_language_link = self.imdb_link + '/search/title?title_type=movie,tvMovie&production_status=released&primary_language=%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_certification_link = self.imdb_link + '/search/title?title_type=movie,tvMovie&production_status=released&certificates=us:%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_list_link = self.imdb_link + '/list/%s/?view=simple&sort=date_added,desc&title_type=movie,short,tvMovie,video&start=1'
        self.imdb_list2_link = self.imdb_link + '/list/%s/?view=simple&sort=alpha,asc&title_type=movie,short,tvMovie,video&start=1'
        self.imdb_lists_link = self.imdb_link + '/user/ur%s/lists?tab=all&sort=modified&order=desc&filter=titles' % self.imdb_user
        self.imdb_watchlist_link = self.imdb_link + '/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user
        self.imdb_watchlist2_link = self.imdb_link + '/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdb_keyword_link = self.imdb_link + '/search/title?title_type=movie,short,tvMovie&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_keywords_link = self.imdb_link + '/search/keyword?keywords=%s&title_type=movie,tvMovie&sort=moviemeter,asc&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_userlists_link = self.imdb_link + '/list/%s/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&count=%s&start=1' % ('%s', self.items_per_page)
        self.imdb_top1000y20to29_link = self.imdb_link + '/search/title/?groups=top_1000&release_date=2020,2029&title_type=movie,tvMovie&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page
        self.imdb_top1000y10to19_link = self.imdb_link + '/search/title/?groups=top_1000&release_date=2010,2019&title_type=movie,tvMovie&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page
        self.imdb_top1000y00to09_link = self.imdb_link + '/search/title/?groups=top_1000&release_date=2000,2009&title_type=movie,tvMovie&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page
        self.imdb_top1000y90to99_link = self.imdb_link + '/search/title/?groups=top_1000&release_date=1990,1999&title_type=movie,tvMovie&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page
        self.imdb_top1000y80to89_link = self.imdb_link + '/search/title/?groups=top_1000&release_date=1980,1989&title_type=movie,tvMovie&sort=moviemeter,asc&count=%s&start=1' % self.items_per_page

        self.trakt_search_link = self.trakt_link + '/search/movie?query=%s&limit=%s&page=1' % ('%s', self.items_per_page)
        self.trakt_anticipated_link = self.trakt_link + '/movies/anticipated?limit=%s&page=1' % self.items_per_page
        self.trakt_boxoffice_link = self.trakt_link + '/movies/boxoffice?limit=%s&page=1' % self.items_per_page
        self.trakt_popular_link = self.trakt_link + '/movies/popular?limit=%s&page=1' % self.items_per_page
        self.trakt_trending_link = self.trakt_link + '/movies/trending?limit=%s&page=1' % self.items_per_page
        self.trakt_featured_link = self.trakt_link + '/recommendations/movies?limit=%s&page=1' % self.items_per_page
        self.trakt_list_link = self.trakt_link + '/users/%s/lists/%s/items'
        self.trakt_lists_link = self.trakt_link + '/users/me/lists'
        self.trakt_likedlists_link = self.trakt_link + '/users/likes/lists?limit=1000000'
        self.trakt_collection_link = self.trakt_link + '/users/me/collection/movies'
        self.trakt_watchlist_link = self.trakt_link + '/users/me/watchlist/movies'
        self.trakt_history_link = self.trakt_link + '/users/me/history/movies?limit=%s&page=1' % self.items_per_page
        self.trakt_ondeck_link = self.trakt_link + '/sync/playback/movies?limit=%s&page=1' % self.items_per_page
        self.trakt_related_link = self.trakt_link + '/movies/%s/related'
        self.trakt_update_link = self.trakt_link + '/movies/updates/%s?limit=%s&page=1' % ('%s', self.items_per_page)
        self.trakt_played1_link = self.trakt_link + '/movies/played/weekly?limit=%s&page=1' % self.items_per_page
        self.trakt_played2_link = self.trakt_link + '/movies/played/monthly?limit=%s&page=1' % self.items_per_page
        self.trakt_played3_link = self.trakt_link + '/movies/played/yearly?limit=%s&page=1' % self.items_per_page
        self.trakt_played4_link = self.trakt_link + '/movies/played/all?limit=%s&page=1' % self.items_per_page
        self.trakt_collected1_link = self.trakt_link + '/movies/collected/weekly?limit=%s&page=1' % self.items_per_page
        self.trakt_collected2_link = self.trakt_link + '/movies/collected/monthly?limit=%s&page=1' % self.items_per_page
        self.trakt_collected3_link = self.trakt_link + '/movies/collected/yearly?limit=%s&page=1' % self.items_per_page
        self.trakt_collected4_link = self.trakt_link + '/movies/collected/all?limit=%s&page=1' % self.items_per_page
        self.trakt_watched1_link = self.trakt_link + '/movies/watched/weekly?limit=%s&page=1' % self.items_per_page
        self.trakt_watched2_link = self.trakt_link + '/movies/watched/monthly?limit=%s&page=1' % self.items_per_page
        self.trakt_watched3_link = self.trakt_link + '/movies/watched/yearly?limit=%s&page=1' % self.items_per_page
        self.trakt_watched4_link = self.trakt_link + '/movies/watched/all?limit=%s&page=1' % self.items_per_page


    def search_term_menu(self, select):
        navigator.navigator().addDirectoryItem('New Search...', 'movies_searchterm&select=%s' % select, 'search.png', 'DefaultMovies.png')
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
            navigator.navigator().addDirectoryItem(term.title(), 'movies_searchterm&select=%s&name=%s' % (select, term), 'search.png', 'DefaultMovies.png')
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
        if select == 'movies':
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


    def search_imdb_movie(self, url):
        try:
            result = client.scrapePage(url).text
            result = client.parseDOM(result, 'table', attrs={'class': 'findList'})[0]
            items = client.parseDOM(result, 'td', attrs={'class': 'result_text'})
            for item in items:
                try:
                    title = client.parseDOM(item, 'a')[0]
                    title = client.replaceHTMLCodes(title)
                    try:
                        year = re.compile(r'\((\d{4})\)').findall(item)[0]
                    except:
                        year = '0'
                    imdb = client.parseDOM(item, 'a', ret='href')[0]
                    imdb = re.findall(r'(tt\d*)', imdb)[0]
                    self.list.append({'title': title, 'originaltitle': title, 'year': year, 'imdb': imdb, 'tmdb': '0', 'tvdb': '0'})
                except:
                    pass
        except:
            pass
        return self.list


    def search_imdb_persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.imdb_personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def imdb_keywords(self):
        from resources.lib.indexers.metadata.imdb import imdb_various
        keywords = imdb_various.keywords_list
        for keyword in keywords:
            self.list.append({'name': keyword.replace('-', ' '), 'url': self.imdb_keywords_link % keyword, 'image': 'imdb.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def imdb_years(self):
        year = (self.datetime.strftime('%Y'))
        for i in range(int(year)-0, 1900, -1):
            self.list.append({'name': str(i), 'url': self.imdb_year_link % (str(i), str(i)), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def imdb_decades(self):
        year = (self.datetime.strftime('%Y'))
        dec = int(year[:3]) * 10
        for i in range(dec, 1890, -10):
            self.list.append({'name': str(i) + 's', 'url': self.imdb_year_link % (str(i), str(i+9)), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def imdb_genres(self):
        from resources.lib.indexers.metadata.imdb import imdb_various
        genres = imdb_various.genre_list
        for genre in genres:
            self.list.append({'name': genre[0], 'url': self.imdb_genre_link % genre[1] if genre[2] else self.imdb_keyword_link % genre[1], 'image': 'genres.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def imdb_languages(self):
        from resources.lib.indexers.metadata.imdb import imdb_various
        languages = imdb_various.languages_list
        for language in languages:
            self.list.append({'name': language[0], 'url': self.imdb_language_link % language[1], 'image': 'languages.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def imdb_certifications(self):
        certificates = ['G', 'PG', 'PG-13', 'R', 'NC-17']
        for certificate in certificates:
            self.list.append({'name': str(certificate), 'url': self.imdb_certification_link % str(certificate), 'image': 'certificates.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def hellaLifeTimeHallMark(self):
        from resources.lib.indexers.metadata.imdb import imdb_userlists
        userlists = imdb_userlists.imdb_hellaLifeTimeHallMark
        for item in userlists:
            self.list.append({'name': item[0], 'url': self.imdb_userlists_link % item[1], 'image': 'imdb.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def imdbUserLists(self):
        self.list.append({'name': 'IMDb Top1000 (2020 - 2029)', 'url': self.imdb_top1000y20to29_link, 'image': 'imdb.png', 'action': 'movies'})
        self.list.append({'name': 'IMDb Top1000 (2010 - 2019)', 'url': self.imdb_top1000y10to19_link, 'image': 'imdb.png', 'action': 'movies'})
        self.list.append({'name': 'IMDb Top1000 (2000 - 2009)', 'url': self.imdb_top1000y00to09_link, 'image': 'imdb.png', 'action': 'movies'})
        self.list.append({'name': 'IMDb Top1000 (1990 - 1999)', 'url': self.imdb_top1000y90to99_link, 'image': 'imdb.png', 'action': 'movies'})
        self.list.append({'name': 'IMDb Top1000 (1980 - 1989)', 'url': self.imdb_top1000y80to89_link, 'image': 'imdb.png', 'action': 'movies'})
        from resources.lib.indexers.metadata.imdb import imdb_userlists
        userlists = imdb_userlists.imdb_imdbUserLists
        for item in userlists:
            self.list.append({'name': item[0], 'url': self.imdb_userlists_link % item[1], 'image': 'imdb.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def search_tmdb_people(self, q=None):
        query = urllib_parse.quote_plus(q)
        self.list = tmdb_utils.find_people(None, query, 'movie')
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def search_tmdb_keyword(self, q=None):
        query = urllib_parse.quote_plus(q)
        self.list = tmdb_utils.find_keyword(None, query, 'movie')
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def search_tmdb_companies(self, q=None):
        query = urllib_parse.quote_plus(q)
        self.list = tmdb_utils.find_companies(query, 'movie')
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def search_tmdb_collection(self, q=None):
        query = urllib_parse.quote_plus(q)
        self.list = tmdb_utils.find_collection(query)
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_years(self):
        year = (self.datetime.strftime('%Y'))
        for i in range(int(year)+1, 1900, -1):
            self.list.append({'name': str(i), 'url': self.tmdb_year_link % str(i), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_decades(self):
        year = (self.datetime.strftime('%Y'))
        dec = int(year[:3]) * 10
        for i in range(dec, 1890, -10):
            self.list.append({'name': str(i) + 's', 'url': self.tmdb_decade_link % (str(i) + '-01-01', str(i+9) + '-01-01'), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_genres(self):
        from resources.lib.indexers.metadata.tmdb import tmdb_various
        genres = tmdb_various.genre_list
        for item in genres:
            self.list.append({'name': item[0], 'url': self.tmdb_genre_link % item[1], 'image': 'genres.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_languages(self):
        from resources.lib.indexers.metadata.tmdb import tmdb_various
        languages = tmdb_various.language_list
        for item in languages:
            self.list.append({'name': item[0], 'url': self.tmdb_language_link % item[1], 'image': 'languages.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_certifications(self):
        certificates = ['G', 'PG', 'PG-13', 'R', 'NC-17', 'NR']
        for item in certificates:
            self.list.append({'name': item, 'url': self.tmdb_certification_link % item, 'image': 'certificates.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_popular_companies(self):
        from resources.lib.indexers.metadata.tmdb import tmdb_production_companies
        companies = tmdb_production_companies.companies
        for item in companies:
            item_url = self.tmdb_link + '/3/discover/movie?api_key=%s&with_companies=%s&language=en-US&page=1' % (self.tmdb_key, '%s')
            #item_art = self.tmdb_image_link + item['image'] if 'image' in item and not item['image'] == None else 'tmdb.png'
            item_art = self.tmdb_image_link % ('300', item['image']) if 'image' in item and not item['image'] == None else 'tmdb.png'
            self.list.append({'name': item['name'], 'url': item_url % item['id'], 'image': item_art, 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_popular_keywords(self):
        from resources.lib.indexers.metadata.tmdb import tmdb_keywords
        keywords = tmdb_keywords.keywords_list
        for item in keywords:
            item_url = self.tmdb_link + '/3/discover/movie?api_key=%s&with_keywords=%s&language=en-US&page=1' % (self.tmdb_key, '%s')
            self.list.append({'name': item['name'], 'url': item_url % item['id'], 'image': 'tmdb.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_popular_people(self):
        self.list = tmdb_utils.get_popular_people(None, 'movie')
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_collections(self, url):
        from resources.lib.indexers.metadata.tmdb import tmdb_collections
        if url == 'page1':
            collections = tmdb_collections.tmdb_collections_page1
        elif url == 'page2':
            collections = tmdb_collections.tmdb_collections_page2
        elif url == 'page3':
            collections = tmdb_collections.tmdb_collections_page3
        elif url == 'page4':
            collections = tmdb_collections.tmdb_collections_page4
        elif url == 'page5':
            collections = tmdb_collections.tmdb_collections_page5
        elif url == 'page6':
            collections = tmdb_collections.tmdb_collections_page6
        elif url == 'page7':
            collections = tmdb_collections.tmdb_collections_page7
        elif url == 'page8':
            collections = tmdb_collections.tmdb_collections_page8
        elif url == 'page9':
            collections = tmdb_collections.tmdb_collections_page9
        elif url == 'page10':
            collections = tmdb_collections.tmdb_collections_page10
        elif url == 'page11':
            collections = tmdb_collections.tmdb_collections_page11
        for item in collections:
            #item_poster = self.tmdb_image_link + item['poster'] if 'poster' in item and not item['poster'] == None else '0'
            item_poster = self.tmdb_image_link % ('500', item['poster']) if 'poster' in item and not item['poster'] == None else '0'
            #item_fanart = self.tmdb_image_link + item['fanart'] if 'fanart' in item and not item['fanart'] == None else '0'
            item_fanart = self.tmdb_image_link % ('1280', item['fanart']) if 'fanart' in item and not item['fanart'] == None else '0'
            self.list.append({'name': item['name'], 'url': self.tmdb_collections_link % item['id'], 'poster': item_poster, 'fanart': item_fanart, 'image': 'tmdb.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_userlists_list(self, url):
        from resources.lib.indexers.metadata.tmdb import tmdb_userlists
        if url == 'tmdbActorCollections':
            userlists = tmdb_userlists.tmdb_ActorCollections
        elif url == 'tmdbDCvsMarvel':
            userlists = tmdb_userlists.tmdb_DCvsMarvel
        elif url == 'tmdbHolidays':
            userlists = tmdb_userlists.tmdb_Holidays
        elif url == 'tmdbAssortment':
            userlists = tmdb_userlists.tmdb_Assortment
        elif url == 'tmdbCollections':
            userlists = tmdb_userlists.tmdb_Collections
        elif url == 'tmdbCollectionsDupes':
            userlists = tmdb_userlists.tmdb_CollectionsDupes
        for item in userlists:
            self.list.append({'name': item[0], 'url': self.tmdb_userlists_link % item[1], 'image': 'tmdb.png', 'action': 'movies'})
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
            self.list[i].update({'action': 'movies'})
        self.list = sorted(self.list, key=lambda k: (k['image'], k['name'].lower()))
        self.addDirectory(self.list, queue=True)
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
            self.list[i].update({'action': 'movies'})
        self.list = sorted(self.list, key=lambda k: (k['image'], k['name'].lower()))
        self.addDirectory(self.list, queue=True)
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
            self.list[i].update({'action': 'movies'})
        self.list = sorted(self.list, key=lambda k: (k['image'], k['name'].lower()))
        self.addDirectory(self.list, queue=True)
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
            self.list[i].update({'action': 'movies'})
        self.list = sorted(self.list, key=lambda k: (k['image'], k['name'].lower()))
        self.addDirectory(self.list, queue=True)
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
                    items.append(i['movie'])
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
                paused_at = item.get('paused_at', '0')
                if not paused_at:
                    paused_at == '0'
                else:
                    paused_at = re.sub('[^0-9]+', '', paused_at)
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'next': next, 'paused_at': paused_at})
            except:
                #log_utils.log('trakt_list', 1)
                pass
        return self.list


    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
            for item in items:
                try:
                    try:
                        name = item['list']['name']
                    except:
                        name = item['name']
                    name = client.replaceHTMLCodes(name)
                    try:
                        url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                    except:
                        url = ('me', item['ids']['slug'])
                    url = self.trakt_list_link % url
                    self.list.append({'name': name, 'url': url, 'context': url, 'image': 'trakt.png'})
                except:
                    #log_utils.log('trakt_user_list', 1)
                    pass
        except:
            #log_utils.log('trakt_user_list', 1)
            pass
        return self.list


    def imdb_list(self, url):
        try:
            for i in re.findall(r'date\[(\d+)\]', url):
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
            result = result.replace('\n', ' ')
            try:
                result = result.replace(r'"class=".*?ister-page-nex', '" class="lister-page-nex')
                next = client.parseDOM(result, 'a', ret='href', attrs={'class': r'.*?ister-page-nex.*?'})
                if len(next) == 0:
                    next = client.parseDOM(result, 'div', attrs={'class': u'pagination'})[0]
                    next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
                    next = [i[0] for i in next if 'Next' in i[1]]
                next = url.replace(urllib_parse.urlparse(url).query, urllib_parse.urlparse(next[0]).query)
                next = client.replaceHTMLCodes(next)
            except:
                next = ''
            items = client.parseDOM(result, 'div', attrs={'class': r'lister-item .*?'})
            items += client.parseDOM(result, 'div', attrs={'class': r'list_item.*?'})
            for item in items:
                try:
                    title = client.parseDOM(item, 'a')[1]
                    title = client.replaceHTMLCodes(title)
                    year = client.parseDOM(item, 'span', attrs={'class': r'lister-item-year.*?'})
                    year += client.parseDOM(item, 'span', attrs={'class': 'year_type'})
                    try:
                        year = re.compile(r'(\d{4})').findall(str(year))[0]
                    except:
                        year = '0'
                    if int(year) > int((self.datetime).strftime('%Y')):
                        if self.shownoyear != 'true':
                            raise Exception()
                    imdb = client.parseDOM(item, 'a', ret='href')[0]
                    imdb = re.findall(r'(tt\d*)', imdb)[0]
                    self.list.append({'title': title, 'originaltitle': title, 'year': year, 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'next': next})
                except:
                    #log_utils.log('imdb_list', 1)
                    pass
        except:
            #log_utils.log('imdb_list', 1)
            pass
        return self.list


    def imdb_user_list(self, url):
        try:
            if control.setting('imdb.sort.order') == '1':
                list_url = self.imdb_list2_link
            else:
                list_url = self.imdb_list_link
            result = client.scrapePage(url).text
            items = client.parseDOM(result, 'li', attrs={'class': 'ipl-zebra-list__item user-list'})
            for item in items:
                try:
                    name = client.parseDOM(item, 'a')[0]
                    name = client.replaceHTMLCodes(name)
                    url = client.parseDOM(item, 'a', ret='href')[0]
                    url = url.split('/list/', 1)[-1].strip('/')
                    url = list_url % url
                    url = client.replaceHTMLCodes(url)
                    self.list.append({'name': name, 'url': url, 'context': url, 'image': 'imdb.png'})
                except:
                    #log_utils.log('imdb_user_list', 1)
                    pass
        except:
            #log_utils.log('imdb_user_list', 1)
            pass
        return self.list


    def imdb_person_list(self, url):
        try:
            result = client.scrapePage(url).text
            items = client.parseDOM(result, 'div', attrs={'class': '.+?etail'})
            for item in items:
                try:
                    name = client.parseDOM(item, 'img', ret='alt')[0]
                    name = client.replaceHTMLCodes(name)
                    url = client.parseDOM(item, 'a', ret='href')[0]
                    url = re.findall(r'(nm\d*)', url, re.I)[0]
                    url = self.imdb_person_link % url
                    url = client.replaceHTMLCodes(url)
                    image = client.parseDOM(item, 'img', ret='src')[0]
                    image = re.sub(r'(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                    image = client.replaceHTMLCodes(image)
                    self.list.append({'name': name, 'url': url, 'image': image})
                except:
                    #log_utils.log('imdb_person_list', 1)
                    pass
        except:
            #log_utils.log('imdb_person_list', 1)
            pass
        return self.list


    def tmdb_list(self, url):
        try:
            next = url
            if 'date[' in url:
                for i in re.findall('date\[(\d+)\]', url):
                    url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days=int(i))).strftime('%Y-%m-%d'))
            result = client.scrapePage(url).json()
            try:
                page = int(result['page'])
                total = int(result['total_pages'])
                if page >= total:
                    raise Exception()
                if not 'page=' in url:
                    raise Exception()
                next = '%s&page=%s' % (next.split('&page=', 1)[0], str(page+1))
            except:
                next = ''
            if 'results' in result:
                items = result['results']
            elif 'items' in result:
                items = result['items']
            elif 'parts' in result:
                items = result['parts']
            elif 'cast' in result:
                items = result['cast']
            for item in items:
                try:
                    if 'media_type' in item and not item['media_type'] == 'movie':
                        raise Exception()
                    title = item['title']
                    title = client.replaceHTMLCodes(title)
                    originaltitle = item['original_title']
                    originaltitle = client.replaceHTMLCodes(originaltitle)
                    year = item['release_date']
                    year = re.compile('(\d{4})').findall(year)[0]
                    if int(year) > int((self.datetime).strftime('%Y')):
                        if self.shownoyear != 'true':
                            raise Exception()
                    tmdb = item['id']
                    tmdb = re.sub('[^0-9]', '', str(tmdb))
                    self.list.append({'title': title, 'originaltitle': originaltitle, 'year': year, 'imdb': '0', 'tmdb': tmdb, 'tvdb': '0', 'next': next})
                except:
                    #log_utils.log('tmdb_list', 1)
                    pass
        except:
            #log_utils.log('tmdb_list', 1)
            pass
        return self.list


    def get_fanart_tv_artwork(self, id):
        try:
            art = client.scrapePage(self.fanart_tv_art_link % id, headers=self.fanart_tv_headers).json()
            try:
                poster = art['movieposter']
                poster = [x for x in poster if x.get('lang') == 'en'][::-1] + [x for x in poster if x.get('lang') in ['00', '']][::-1]
                poster = poster[0]['url']
                if poster == '' or poster == None or poster == []:
                    poster = '0'
            except:
                poster = '0'
            try:
                if 'moviebackground' in art:
                    fanart = art['moviebackground']
                else:
                    fanart = art['moviethumb']
                fanart = [x for x in fanart if x.get('lang') == 'en'][::-1] + [x for x in fanart if x.get('lang') in ['00', '']][::-1]
                fanart = fanart[0]['url']
                if fanart == '' or fanart == None or fanart == []:
                    fanart = '0'
            except:
                fanart = '0'
            try:
                banner = art['moviebanner']
                banner = [x for x in banner if x.get('lang') == 'en'][::-1] + [x for x in banner if x.get('lang') in ['00', '']][::-1]
                banner = banner[0]['url']
                if banner == '' or banner == None or banner == []:
                    banner = '0'
            except:
                banner = '0'
            try:
                if 'hdmovielogo' in art:
                    clearlogo = art['hdmovielogo']
                else:
                    clearlogo = art['clearlogo']
                clearlogo = [x for x in clearlogo if x.get('lang') == 'en'][::-1] + [x for x in clearlogo if x.get('lang') in ['00', '']][::-1]
                clearlogo = clearlogo[0]['url']
                if clearlogo == '' or clearlogo == None or clearlogo == []:
                    clearlogo = '0'
            except:
                clearlogo = '0'
            try:
                if 'hdmovieclearart' in art:
                    clearart = art['hdmovieclearart']
                else:
                    clearart = art['clearart']
                clearart = [x for x in clearart if x.get('lang') == 'en'][::-1] + [x for x in clearart if x.get('lang') in ['00', '']][::-1]
                clearart = clearart[0]['url']
                if clearart == '' or clearart == None or clearart == []:
                    clearart = '0'
            except:
                clearart = '0'
            try:
                if 'moviethumb' in art:
                    landscape = art['moviethumb']
                else:
                    landscape = art['moviebackground']
                landscape = [x for x in landscape if x.get('lang') == 'en'][::-1] + [x for x in landscape if x.get('lang') in ['00', '']][::-1]
                landscape = landscape[0]['url']
                if landscape == '' or landscape == None or landscape == []:
                    landscape = '0'
            except:
                landscape = '0'
            try:
                discart = art['moviedisc']
                discart = [x for x in discart if x.get('lang') == 'en'][::-1] + [x for x in discart if x.get('lang') in ['00', '']][::-1]
                discart = discart[0]['url']
                if discart == '' or discart == None or discart == []:
                    discart = '0'
            except:
                discart = '0'
        except:
            poster = fanart = banner = clearlogo = clearart = landscape = discart = '0'
        return poster, fanart, banner, clearlogo, clearart, landscape, discart


    def final_info(self, i):
        try:
            if self.list[i]['metacache'] == True:
                return
            try:
                imdb = self.list[i]['imdb']
            except:
                imdb = '0'
            try:
                tmdb = self.list[i]['tmdb']
            except:
                tmdb = '0'
            if tmdb == '0' and not imdb == '0':
                try:
                    temp_item = tmdb_utils.find_movie_by_external_source(imdb=imdb)
                    tmdb = temp_item['id']
                except:
                    temp_item = trakt.getMovieSummary(imdb)
                    tmdb = temp_item.get('ids', {}).get('tmdb')
            url = self.tmdb_info_link % tmdb
            item = client.scrapePage(url).json()
            if imdb == '0':
                try:
                    imdb = item['imdb_id']
                except:
                    temp_item = trakt.getMovieSummary(tmdb)
                    imdb = temp_item.get('ids', {}).get('imdb')
            title = self.list[i]['title'] or item['title']
            title = client.replaceHTMLCodes(title)
            originaltitle = self.list[i]['originaltitle'] or item['original_title']
            originaltitle = client.replaceHTMLCodes(originaltitle)
            year = self.list[i]['year']
            if year == '' or year == '0' or year == None or year == []:
                year = item['release_date']
                if year:
                    year = re.compile('(\d{4})').findall(year)[0]
                    if year == '' or year == None:
                        year = '0'
                else:
                    year = '0'
            premiered = item['release_date']
            if premiered:
                premiered = re.compile(r'(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                if premiered == '' or premiered == None:
                    premiered = '0'
            else:
                premiered = '0'
            if self.studio_artwork == 'true':
                studio = item['production_companies']
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
            duration = str(item['runtime'])
            if duration == '' or duration == '0' or duration == None or duration == []:
                duration = '0'
            rating = str(item['vote_average'])
            if rating == '' or rating == '0' or rating == '0.0' or rating == None or rating == []:
                rating = '0'
            votes = str(item['vote_count'])
            try:
                votes = str(format(int(votes), ',d'))
            except:
                votes = '0'
            if votes == '' or votes == '0' or votes == None or votes == []:
                votes = '0'
            tagline = item['tagline']
            if not tagline:
                tagline = '0'
            plot = item['overview']
            if not plot:
                plot = '0'
            mpaa = item['releases']['countries']
            try:
                mpaa = [x for x in mpaa if not x['certification'] == '']
                mpaa = [x for x in mpaa if str(x['iso_3166_1']) == 'US'][0]['certification']
            except:
                mpaa = '0'
            director = item['credits']['crew']
            try:
                director = [x['name'] for x in director if str(x['job']) == 'Director']
                director = ' / '.join(director).strip()
            except:
                director = '0'
            writer = item['credits']['crew']
            try:
                writer = [x['name'] for x in writer if str(x['job']) in ['Writer', 'Screenplay']]
                writer = [x for n,x in enumerate(writer) if x not in writer[:n]]
                writer = ' / '.join(writer).strip()
            except:
                writer = '0'
        
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

            poster = item['poster_path']
            if not (poster == '' or poster == None):
                #poster = self.tmdb_image_link + poster
                poster = self.tmdb_image_link % ('500', poster)
            else:
                poster = '0'
            fanart = item['backdrop_path']
            if not (fanart == '' or fanart == None):
                #fanart = self.tmdb_image_link + fanart
                fanart = self.tmdb_image_link % ('1280', fanart)
            else:
                fanart = '0'
            if self.hq_artwork == 'true':
                poster2, fanart2, banner, clearlogo, clearart, landscape, discart = self.get_fanart_tv_artwork(imdb)
            else:
                poster2 = fanart2 = banner = clearlogo = clearart = landscape = discart = '0'
            poster = poster2 if not poster2 == '0' else poster
            fanart = fanart2 if not fanart2 == '0' else fanart
            item = {'title': title, 'originaltitle': originaltitle, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster, 'banner': banner, 'fanart': fanart, 'clearlogo': clearlogo, 'clearart': clearart, 'landscape': landscape,
                'discart': discart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'mpaa': mpaa, 'director': director, 'writer': writer, 'castwiththumb': castwiththumb, 'plot': plot, 'tagline': tagline
            }
            item = dict((k,v) for k, v in six.iteritems(item) if not v == '0')
            self.list[i].update(item)
            meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.lang, 'user': self.user, 'item': item}
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
                    self.list = cache.get(self.trakt_list, 720, url, self.trakt_user)
                except:
                    self.list = self.trakt_list(url, self.trakt_user)
                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: k['title'])
                if idx == True:
                    self.worker()
            elif u in self.trakt_link and '/sync/playback/' in url:
                self.list = self.trakt_list(url, self.trakt_user)
                self.list = sorted(self.list, key=lambda k: int(k['paused_at']), reverse=True)
                if idx == True:
                    self.worker()
            elif u in self.trakt_link and self.trakt_search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx == True:
                    self.worker()
            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx == True:
                    self.worker()
            elif u in self.imdb_link and '/find?' in url:
                self.list = cache.get(self.search_imdb_movie, 1, url)
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
            if idx == True and create_directory == True:
                self.movieDirectory(self.list)
            return self.list
        except:
            #log_utils.log('get', 1)
            pass


    def movieDirectory(self, items):
        if items == None or len(items) == 0:
            control.idle()
            #sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart = control.addonFanart()
        traktCredentials = trakt.getTraktCredentialsInfo()
        tmdbCredentials = tmdb_utils.getTMDbCredentialsInfo()
        try:
            isOld = False ; control.item().getArt('type')
        except:
            isOld = True
        isPlayable = True if not 'plugin' in control.infoLabel('Container.PluginName') else False
        indicators = playcount.getMovieIndicators()#refresh=True) if action == 'movies' else playcount.getMovieIndicators()
        playbackMenu = 'Select Source' if control.setting('hosts.mode') == '2' else 'Auto Play'
        watchedMenu = 'Watched in Trakt' if trakt.getTraktIndicatorsInfo() == True else 'Watched in Scrubs'
        unwatchedMenu = 'Unwatched in Trakt' if trakt.getTraktIndicatorsInfo() == True else 'Unwatched in Scrubs'
        if self.trailer_source == '0':
            trailerAction = 'tmdb_trailer'
        elif self.trailer_source == '1':
            trailerAction = 'yt_trailer'
        else:
            trailerAction = 'imdb_trailer'
        nextMenu = '[I]Next Page[/I]'
        for i in items:
            try:
                if 'channel' in i:
                    label = '%s : %s (%s)' % (i['channel'], i['title'], i['year'])
                else:
                    label = '%s (%s)' % (i['title'], i['year'])
                imdb, tmdb, title, year = i['imdb'], i['tmdb'], i['originaltitle'], i['year']
                try:
                    premiered = i['premiered']
                    if premiered == '0' or (int(re.sub('[^0-9]', '', premiered)) > int(re.sub('[^0-9]', '', str(self.today_date)))):
                        label = '[COLOR %s][I]%s[/I][/COLOR]' % (self.unairedcolor, label)
                except:
                    pass
                sysname = urllib_parse.quote_plus('%s (%s)' % (title, year))
                systitle = urllib_parse.quote_plus(title)
                meta = dict((k,v) for k, v in six.iteritems(i) if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb, 'tmdb_id': tmdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=%s&name=%s&tmdb=%s&imdb=%s' % (sysaddon, trailerAction, systitle, tmdb, imdb)})
                if not 'duration' in i:
                    meta.update({'duration': '120'})
                elif i['duration'] == '0':
                    meta.update({'duration': '120'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                poster = i['poster'] if 'poster' in i and not i['poster'] == '0' else addonPoster
                meta.update({'poster': poster})
                sysmeta = urllib_parse.quote_plus(json.dumps(meta))
                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib_parse.quote_plus(url)
                path = '%s?action=play&title=%s&year=%s&imdb=%s' % (sysaddon, systitle, year, imdb)
                cm = []
                cm.append(('Clean Tools Widget', 'RunPlugin(%s?action=cleantools_widget)' % sysaddon))
                cm.append(('Clear Providers', 'RunPlugin(%s?action=clear_sources)' % sysaddon))
                cm.append(('Find Similar', 'Container.Update(%s?action=movies&url=%s)' % (sysaddon, self.trakt_related_link % imdb)))
                cm.append(('Queue Item', 'RunPlugin(%s?action=queue_item)' % sysaddon))
                if traktCredentials == True:
                    cm.append(('Trakt Manager', 'RunPlugin(%s?action=trakt_manager&name=%s&imdb=%s&content=movie)' % (sysaddon, sysname, imdb)))
                if tmdbCredentials == True:
                    cm.append(('TMDb Manager', 'RunPlugin(%s?action=tmdb_manager&name=%s&tmdb=%s&content=movie)' % (sysaddon, sysname, tmdb)))
                cm.append(('Add to Library', 'RunPlugin(%s?action=movie_to_library&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, sysname, systitle, year, imdb, tmdb)))
                
                if isOld == True:
                    cm.append(('Information', 'Action(Info)'))
                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=movies_playcount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=movies_playcount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                cm.append((playbackMenu, 'RunPlugin(%s?action=alter_sources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))
                try:
                    item = control.item(label=label, offscreen=True)
                except:
                    item = control.item(label=label)
                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster})
                fanart = i['fanart'] if 'fanart' in i and not i['fanart'] == '0' else addonFanart
                if self.settingFanart == 'true':
                    art.update({'fanart': fanart})
                else:
                    art.update({'fanart': addonFanart})
                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                else:
                    art.update({'banner': addonBanner})
                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})
                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})
                if 'landscape' in i and not i['landscape'] == '0':
                    landscape = i['landscape']
                else:
                    landscape = fanart
                art.update({'landscape': landscape})
                if 'discart' in i and not i['discart'] == '0':
                    art.update({'discart': i['discart']})
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
                if isPlayable:
                    item.setProperty('IsPlayable', 'true')
                offset = bookmarks.get('movie', imdb, '', '', True)
                if float(offset) > 120:
                    percentPlayed = int(float(offset) / float(meta['duration']) * 100)
                    item.setProperty('resumetime', str(offset))
                    item.setProperty('percentplayed', str(percentPlayed))
                item.setInfo(type='Video', infoLabels = control.metadataClean(meta))
                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                #log_utils.log('movieDirectory', 1)
                pass
        try:
            url = items[0]['next']
            if url == '':
                raise Exception()
            icon = control.addonNext()
            url = '%s?action=movies&url=%s' % (sysaddon, urllib_parse.quote_plus(url))
            try:
                item = control.item(label=nextMenu, offscreen=True)
            except:
                item = control.item(label=nextMenu)
            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon, 'fanart': addonFanart})
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass
        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        control.sleep(1000)
        views.setView('movies', {'skin.aeon.nox.silvo' : 50, 'skin.estuary': 55, 'skin.confluence': 500}) #View 50 List #View 501 LowList


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
                    cm.append(('Add to Library', 'RunPlugin(%s?action=movies_to_library&url=%s)' % (sysaddon, urllib_parse.quote_plus(i['context']))))
                except:
                    pass
                try:
                    item = control.item(label=name, offscreen=True)
                except:
                    item = control.item(label=name)
                poster = i['poster'] if 'poster' in i and not (i['poster'] == '0' or i['poster'] == None) else thumb
                fanart = i['fanart'] if 'fanart' in i and not (i['fanart'] == '0' or i['fanart'] == None) else addonFanart
                item.setArt({'icon': thumb, 'thumb': poster, 'fanart': fanart})
                item.addContextMenuItems(cm)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                #log_utils.log('addDirectory', 1)
                pass
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


