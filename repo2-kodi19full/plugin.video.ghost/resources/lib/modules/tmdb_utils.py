# -*- coding: utf-8 -*-

import requests
from requests.compat import json, str

from resources.lib.modules import control
from resources.lib.modules import log_utils

USERNAME = control.setting('tmdb.user')
PASSWORD = control.setting('tmdb.pass')
SESSION_ID = control.setting('tmdb.session')
ACCOUNT_ID = control.setting('tmdb.id')

API_KEY = control.setting('tmdb.api')
if not API_KEY:
    API_KEY = 'c8b7db701bac0b26edfcc93b39858972'

API_URL = 'https://api.themoviedb.org/3/'
ART_URL = 'https://image.tmdb.org/t/p/original'
HEADERS = {'Content-Type': 'application/json;charset=utf-8'}


def getTMDbCredentialsInfo():
    if (USERNAME == '' or PASSWORD == '' or SESSION_ID == '' or ACCOUNT_ID == ''):
        return False
    return True


def authTMDb():
    try:
        if not SESSION_ID == '':
            if control.yesnoDialog('A Session Already Exists.' + '[CR]' + 'Delete Session?', heading='TMDB'):
                return delete_session()
            raise Exception()
        if USERNAME == '' or PASSWORD == '':
            control.infoDialog('Check Account Credentials.', sound=True)
            raise Exception()
        request_token = create_request_token()
        if not request_token:
            raise Exception()
        request_token = create_session_with_login(request_token)
        if not request_token:
            raise Exception()
        session_id = create_session(request_token)
        if not session_id:
            raise Exception()
        control.setSetting(id='tmdb.session', value=session_id)
        control.infoDialog('TMDb Auth Successful.', sound=True)
        return get_account_details(session_id)
    except:
        log_utils.log('authTMDb', 1)
        control.infoDialog('TMDb Auth Failed.', sound=True)
        return


def create_request_token():
    try:
        url = API_URL + 'authentication/token/new?api_key=%s' % API_KEY
        result = requests.get(url, headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        request_token = result['request_token']
        return request_token
    except:
        log_utils.log('create_request_token', 1)
        return None


def create_session_with_login(request_token):
    try:
        url = API_URL + 'authentication/token/validate_with_login?api_key=%s' % API_KEY
        post = {"username": "%s" % str(USERNAME), "password": "%s" % str(PASSWORD), "request_token": "%s" % str(request_token)}
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        request_token = result['request_token']
        return request_token
    except:
        log_utils.log('create_session_with_login', 1)
        return None


def create_session(request_token):
    try:
        url = API_URL + 'authentication/session/new?api_key=%s' % API_KEY
        post = {"request_token": "%s" % str(request_token)}
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        session_id = result['session_id']
        return session_id
    except:
        log_utils.log('create_session', 1)
        return None


def delete_session():
    try:
        if SESSION_ID == '':
            raise Exception()
        url = API_URL + 'authentication/session?api_key=%s' % API_KEY
        post = {"session_id": "%s" % str(SESSION_ID)}
        result = requests.delete(url, data=json.dumps(post), headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        control.setSetting(id='tmdb.session', value='')
        if not ACCOUNT_ID == '':
            control.setSetting(id='tmdb.id', value='')
        control.infoDialog('TMDb delete_session Successful', sound=True)
    except:
        control.infoDialog('TMDb delete_session Failed', sound=True)
        log_utils.log('delete_session', 1)
        pass


def get_account_details(session_id):
    try:
        url = API_URL + 'account?api_key=%s&session_id=%s' % (API_KEY, session_id)
        result = requests.get(url, headers=HEADERS).json()
        account_username = result['username']
        account_name = result['name']
        account_id = result['id']
        account_include_adult = result['include_adult']
        account_iso_639_1 = result['iso_639_1']
        account_iso_3166_1 = result['iso_3166_1']
        control.setSetting(id='tmdb.id', value=str(account_id))
        message = ('username: %s' % str(account_username) + '[CR]' + 'name: %s' % str(account_name) + '[CR]' + 'id: %s' % str(account_id) + '[CR]' + 'include_adult: %s' % str(account_include_adult) + '[CR]' + 'iso_639_1: %s' % str(account_iso_639_1) + '[CR]' + 'iso_3166_1: %s' % str(account_iso_3166_1))
        return control.okDialog(message, heading='TMDB Account Details')
    except:
        log_utils.log('get_account_details', 1)
        pass


def get_created_lists(url=None):
    try:
        if not url:
            url = API_URL + 'list/%s?api_key=%s&language=en-US&page=1' % ('%s', API_KEY)
        lists_url = API_URL + 'account/%s/lists?api_key=%s&language=en-US&session_id=%s&page=1' % (ACCOUNT_ID, API_KEY, SESSION_ID)
        result = requests.get(lists_url, headers=HEADERS).json()
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            if not 'page=' in lists_url:
                raise Exception()
            next = '%s&page=%s' % (lists_url.split('&page=', 1)[0], str(page+1))
        except:
            next = ''
        items = []
        lists = result['results']
        for list in lists:
            list_name = list['name']
            list_id = list['id']
            list_url = url % list_id
            items.append({'name': list_name, 'url': list_url, 'context': list_url, 'list_id': list_id, 'image': 'tmdb.png', 'next': next})
        return items
    except:
        log_utils.log('get_created_lists', 1)
        return items


def create_list(name):
    try:
        url = API_URL + 'list?api_key=%s&session_id=%s' % (API_KEY, SESSION_ID)
        post = {"name": "%s" % str(name), "description": "created_userlist", "language": "en"}
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        list_id = result['list_id']
        return list_id
    except:
        log_utils.log('add_to_watchlist', 1)
        return


def add_to_list(tmdb, list_id):
    try:
        url = API_URL + 'list/%s/add_item?api_key=%s&session_id=%s' % (list_id, API_KEY, SESSION_ID)
        post = {"media_id": "%s" % str(tmdb)}
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        return True
    except:
        log_utils.log('add_to_list', 1)
        return False


def remove_from_list(tmdb, list_id):
    try:
        url = API_URL + 'list/%s/remove_item?api_key=%s&session_id=%s' % (list_id, API_KEY, SESSION_ID)
        post = {"media_id": "%s" % str(tmdb)}
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        return True
    except:
        log_utils.log('remove_from_list', 1)
        return False


def get_movie_favorites():
    try:
        url = API_URL + 'account/%s/favorite/movies?api_key=%s&session_id=%s&language=en-US&page=1' % (ACCOUNT_ID, API_KEY, SESSION_ID)
        return url
    except:
        log_utils.log('get_movie_favorites', 1)
        return


def get_tvshow_favorites():
    try:
        url = API_URL + 'account/%s/favorite/tv?api_key=%s&session_id=%s&language=en-US&page=1' % (ACCOUNT_ID, API_KEY, SESSION_ID)
        return url
    except:
        log_utils.log('get_tvshow_favorites', 1)
        return


def add_to_favorites(tmdb, media_type):
    try:
        url = API_URL + 'account/%s/favorite?api_key=%s&session_id=%s' % (ACCOUNT_ID, API_KEY, SESSION_ID)
        post = {"media_type": "%s" % str(media_type), "media_id": "%s" % str(tmdb), "favorite": True}
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        return True
    except:
        log_utils.log('add_to_favorites', 1)
        return False


def remove_from_favorites(tmdb, media_type):
    try:
        url = API_URL + 'account/%s/favorite?api_key=%s&session_id=%s' % (ACCOUNT_ID, API_KEY, SESSION_ID)
        post = {"media_type": "%s" % str(media_type), "media_id": "%s" % str(tmdb), "favorite": False}
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        return True
    except:
        log_utils.log('remove_from_favorites', 1)
        return False


def get_movie_watchlist():
    try:
        url = API_URL + 'account/%s/watchlist/movies?api_key=%s&session_id=%s&language=en-US&page=1' % (ACCOUNT_ID, API_KEY, SESSION_ID)
        return url
    except:
        log_utils.log('get_movie_watchlist', 1)
        return


def get_tvshow_watchlist():
    try:
        url = API_URL + 'account/%s/watchlist/tv?api_key=%s&session_id=%s&language=en-US&page=1' % (ACCOUNT_ID, API_KEY, SESSION_ID)
        return url
    except:
        log_utils.log('get_tvshow_watchlist', 1)
        return


def add_to_watchlist(tmdb, media_type):
    try:
        url = API_URL + 'account/%s/watchlist?api_key=%s&session_id=%s' % (ACCOUNT_ID, API_KEY, SESSION_ID)
        post = {"media_type": "%s" % str(media_type), "media_id": "%s" % str(tmdb), "watchlist": True}
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        return True
    except:
        log_utils.log('add_to_watchlist', 1)
        return False


def remove_from_watchlist(tmdb, media_type):
    try:
        url = API_URL + 'account/%s/watchlist?api_key=%s&session_id=%s' % (ACCOUNT_ID, API_KEY, SESSION_ID)
        post = {"media_type": "%s" % str(media_type), "media_id": "%s" % str(tmdb), "watchlist": False}
        result = requests.post(url, data=json.dumps(post), headers=HEADERS).json()
        if not result.get('success') is True:
            raise Exception()
        return True
    except:
        log_utils.log('remove_from_watchlist', 1)
        return False


def manager(name, imdb, tmdb, content):
    try:
        media_type = "movie" if content == "movie" else "tv"
        items = [('Add to [B]Favorites[/B]', 'add_to_favorites')]
        items += [('Remove from [B]Favorites[/B]', 'remove_from_favorites')]
        items += [('Add to [B]Watchlist[/B]', 'add_to_watchlist')]
        items += [('Remove from [B]Watchlist[/B]', 'remove_from_watchlist')]
        items += [('Add to [B]new List[/B]', '%s')]
        result = get_created_lists()
        lists = [(i['name'], i['list_id']) for i in result]
        lists = [lists[i//2] for i in range(len(lists)*2)]
        for i in range(0, len(lists), 2):
            lists[i] = (('Add to [B]%s[/B]' % lists[i][0]), '%s' % lists[i][1])
        for i in range(1, len(lists), 2):
            lists[i] = (('Remove from [B]%s[/B]' % lists[i][0]), '%s' % lists[i][1])
        items += lists
        select = control.selectDialog([i[0] for i in items], 'TMDb Manager')
        if select == -1:
            return
        elif select == 0:
            add_to_favorites(tmdb, media_type)
        elif select == 1:
            remove_from_favorites(tmdb, media_type)
        elif select == 2:
            add_to_watchlist(tmdb, media_type)
        elif select == 3:
            remove_from_watchlist(tmdb, media_type)
        elif select == 4:
            t = 'Add to [B]new List[/B]'
            k = control.keyboard('', t) ; k.doModal()
            new = k.getText() if k.isConfirmed() else None
            if (new == None or new == ''):
                return
            try:
                list_id = create_list(new)
                if not list_id:
                    raise Exception()
                result = add_to_list(tmdb, list_id)
            except:
                return control.infoDialog('TMDb Manager: ' + repr(items[select][0]), heading=str(name), sound=True, icon='ERROR')
        else:
            if items[select][0].startswith('Add'):
                result = add_to_list(tmdb, items[select][1])
            elif items[select][0].startswith('Remove'):
                result = remove_from_list(tmdb, items[select][1])
        icon = control.infoLabel('ListItem.Icon') if not result == None else 'ERROR'
        control.infoDialog('TMDb Manager: ' + repr(items[select][0]), heading=str(name), sound=True, icon=icon)
    except:
        log_utils.log('manager', 1)
        return


def get_movie_account_states(tmdb):
    try:
        url = API_URL + 'movie/%s/account_states?api_key=%s&session_id=%s' % (tmdb, API_KEY, SESSION_ID)
        result = requests.get(url, headers=HEADERS)
        return result.json()
    except:
        log_utils.log('get_movie_account_states', 1)
        return


def get_tvshow_account_states(tmdb):
    try:
        url = API_URL + 'tv/%s/account_states?api_key=%s&session_id=%s' % (tmdb, API_KEY, SESSION_ID)
        result = requests.get(url, headers=HEADERS)
        return result.json()
    except:
        log_utils.log('get_tvshow_account_states', 1)
        return


def get_movie_alternative_titles(tmdb):
    try:
        url = API_URL + 'movie/%s/alternative_titles?api_key=%s&country=US&language=en-US' % (tmdb, API_KEY)
        result = requests.get(url, headers=HEADERS).json()
        results = result['titles']
        return results
    except:
        log_utils.log('get_movie_alternative_titles', 1)
        return


def get_tvshow_alternative_titles(tmdb):
    try:
        url = API_URL + 'tv/%s/alternative_titles?api_key=%s&country=US&language=en-US' % (tmdb, API_KEY)
        result = requests.get(url, headers=HEADERS).json()
        results = result['results']
        return results
    except:
        log_utils.log('get_tvshow_alternative_titles', 1)
        return


def get_movie_external_ids(tmdb):
    try:
        url = API_URL + 'movie/%s/external_ids?api_key=%s&language=en-US' % (tmdb, API_KEY)
        result = requests.get(url, headers=HEADERS)
        return result.json()
    except:
        log_utils.log('get_movie_external_ids', 1)
        return


def get_tvshow_external_ids(tmdb):
    try:
        url = API_URL + 'tv/%s/external_ids?api_key=%s&language=en-US' % (tmdb, API_KEY)
        result = requests.get(url, headers=HEADERS)
        return result.json()
    except:
        log_utils.log('get_tvshow_external_ids', 1)
        return


def get_season_external_ids(tmdb, season):
    try:
        url = API_URL + 'tv/%s/season/%s/external_ids?api_key=%s&language=en-US' % (tmdb, season, API_KEY)
        result = requests.get(url, headers=HEADERS)
        return result.json()
    except:
        log_utils.log('get_season_external_ids', 1)
        return


def get_episode_external_ids(tmdb, season, episode):
    try:
        url = API_URL + 'tv/%s/season/%s/episode/%s/external_ids?api_key=%s&language=en-US' % (tmdb, season, episode, API_KEY)
        result = requests.get(url, headers=HEADERS)
        return result.json()
    except:
        log_utils.log('get_episode_external_ids', 1)
        return


def find_movie_by_external_source(imdb):
    try:
        url = API_URL + 'find/%s?api_key=%s&language=en-US&external_source=imdb_id' % (imdb, API_KEY)
        result = requests.get(url, headers=HEADERS).json()
        item = result['movie_results'][0]
        return item
    except:
        log_utils.log('find_movie_by_external_source', 1)
        return


def find_tvshow_by_external_source(imdb=None, tvdb=None):
    try:
        if imdb:
            url = API_URL + 'find/%s?api_key=%s&language=en-US&external_source=imdb_id' % (imdb, API_KEY)
        elif tvdb:
            url = API_URL + 'find/%s?api_key=%s&language=en-US&external_source=tvdb_id' % (tvdb, API_KEY)
        result = requests.get(url, headers=HEADERS).json()
        item = result['tv_results'][0]
        return item
    except:
        log_utils.log('find_tvshow_by_external_source', 1)
        return


def get_movie_trailers(tmdb):
    try:
        url = API_URL + 'movie/%s/videos?api_key=%s&language=en-US' % (tmdb, API_KEY)
        result = requests.get(url, headers=HEADERS).json()
        items = result['results']
        return items
    except:
        log_utils.log('get_movie_trailers', 1)
        return


def get_tvshow_trailers(tmdb):
    try:
        url = API_URL + 'tv/%s/videos?api_key=%s&language=en-US' % (tmdb, API_KEY)
        result = requests.get(url, headers=HEADERS).json()
        items = result['results']
        return items
    except:
        log_utils.log('get_tvshow_trailers', 1)
        return


def get_season_trailers(tmdb, season):
    try:
        url = API_URL + 'tv/%s/season/%s/videos?api_key=%s&language=en-US' % (tmdb, season, API_KEY)
        result = requests.get(url, headers=HEADERS).json()
        items = result['results']
        return items
    except:
        log_utils.log('get_season_trailers', 1)
        return


def get_episode_trailers(tmdb, season, episode):
    try:
        url = API_URL + 'tv/%s/season/%s/episode/%s/videos?api_key=%s&language=en-US' % (tmdb, season, episode, API_KEY)
        result = requests.get(url, headers=HEADERS).json()
        items = result['results']
        return items
    except:
        log_utils.log('get_episode_trailers', 1)
        return


###################################################
###################################################


# https://api.themoviedb.org/3/person/{person_id}/combined_credits?api_key=<<api_key>>&language=en-US
# https://api.themoviedb.org/3/person/{person_id}/tv_credits?api_key=<<api_key>>&language=en-US
# https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key=<<api_key>>&language=en-US


def get_popular_people(url, content):
    try:
        list = []
        media_type = "movie" if content == "movie" else "tv"
        if not url:
            #url = API_URL + 'discover/%s?api_key=%s&with_people=%s&language=en-US&page=1' % (media_type, API_KEY, '%s')
            url = API_URL + 'person/%s/%s_credits?api_key=%s&language=en-US' % ('%s', media_type, API_KEY)
        list_url = API_URL + 'person/popular?api_key=%s&language=en-US&page=1' % API_KEY
        result = requests.get(list_url, headers=HEADERS).json()
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            if not 'page=' in list_url:
                raise Exception()
            next = '%s&page=%s' % (list_url.split('&page=', 1)[0], str(page+1))
        except:
            next = ''
        items = result['results']
        for item in items:
            person_name = item['name']
            person_id = item['id']
            person_url = url % person_id
            try:
                person_art = ART_URL + item['profile_path']
            except:
                person_art = 'tmdb.png'
            list.append({'name': person_name, 'url': person_url, 'person_id': person_id, 'image': person_art, 'next': next})
        return list
    except:
        log_utils.log('get_popular_people', 1)
        return list


def find_people(url, query, content):
    try:
        list = []
        media_type = "movie" if content == "movie" else "tv"
        if not url:
            #url = API_URL + 'discover/%s?api_key=%s&with_people=%s&language=en-US&page=1' % (media_type, API_KEY, '%s')
            url = API_URL + 'person/%s/%s_credits?api_key=%s&language=en-US' % ('%s', media_type, API_KEY)
        list_url = API_URL + 'search/person?api_key=%s&query=%s&language=en-US&page=1' % (API_KEY, query)
        result = requests.get(list_url, headers=HEADERS).json()
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            if not 'page=' in list_url:
                raise Exception()
            next = '%s&page=%s' % (list_url.split('&page=', 1)[0], str(page+1))
        except:
            next = ''
        items = result['results']
        for item in items:
            person_name = item['name']
            person_id = item['id']
            person_url = url % person_id
            try:
                person_art = ART_URL + item['profile_path']
            except:
                person_art = 'tmdb.png'
            list.append({'name': person_name, 'url': person_url, 'person_id': person_id, 'image': person_art, 'next': next})
        return list
    except:
        log_utils.log('find_people', 1)
        return list


def find_keyword(url, query, content):
    try:
        list = []
        media_type = "movie" if content == "movie" else "tv"
        if not url:
            url = API_URL + 'discover/%s?api_key=%s&with_keywords=%s&language=en-US&page=1' % (media_type, API_KEY, '%s')
        list_url = API_URL + 'search/keyword?api_key=%s&query=%s&language=en-US&page=1' % (API_KEY, query)
        result = requests.get(list_url, headers=HEADERS).json()
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            if not 'page=' in list_url:
                raise Exception()
            next = '%s&page=%s' % (list_url.split('&page=', 1)[0], str(page+1))
        except:
            next = ''
        items = result['results']
        for item in items:
            keyword_name = item['name']
            keyword_id = item['id']
            keyword_url = url % keyword_id
            list.append({'name': keyword_name, 'url': keyword_url, 'keyword_id': keyword_id, 'image': 'tmdb.png', 'next': next})
        return list
    except:
        log_utils.log('find_keyword', 1)
        return list


def find_companies(query, content):
    try:
        list = []
        media_type = "movie" if content == "movie" else "tv"
        list_url = API_URL + 'search/company?api_key=%s&query=%s&page=1' % (API_KEY, query)
        result = requests.get(list_url, headers=HEADERS).json()
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            if not 'page=' in list_url:
                raise Exception()
            next = '%s&page=%s' % (list_url.split('&page=', 1)[0], str(page+1))
        except:
            next = ''
        items = result['results']
        for item in items:
            company_name = item['name']
            company_id = item['id']
            try:
                company_art = ART_URL + item['logo_path']
            except:
                company_art = 'tmdb.png'
            company_url = API_URL + 'discover/%s?api_key=%s&with_companies=%s&language=en-US&page=1' % (media_type, API_KEY, company_id)
            list.append({'name': company_name, 'url': company_url, 'company_id': company_id, 'image': company_art, 'next': next})
        return list
    except:
        log_utils.log('find_companies', 1)
        return list


def find_collection(query):
    try:
        list = []
        list_url = API_URL + 'search/collection?api_key=%s&query=%s&page=1' % (API_KEY, query)
        result = requests.get(list_url, headers=HEADERS).json()
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            if not 'page=' in list_url:
                raise Exception()
            next = '%s&page=%s' % (list_url.split('&page=', 1)[0], str(page+1))
        except:
            next = ''
        items = result['results']
        for item in items:
            try:
                collection_name = item['name']
                collection_id = item['id']
                try:
                    collection_poster = ART_URL + item['poster_path']
                    collection_fanart = ART_URL + item['backdrop_path']
                except:
                    collection_poster = 'tmdb.png'
                    collection_fanart = None
                collection_url = API_URL + 'collection/%s?api_key=%s&language=en-US&page=1' % (collection_id, API_KEY)
                list.append({'name': collection_name, 'url': collection_url, 'collection_id': collection_id, 'poster': collection_poster, 'fanart': collection_fanart, 'image': 'tmdb.png', 'next': next})
            except:
                log_utils.log('find_collection', 1)
                pass
            
        return list
    except:
        log_utils.log('find_collection', 1)
        return list


