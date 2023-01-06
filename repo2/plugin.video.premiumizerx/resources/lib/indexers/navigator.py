# -*- coding: utf-8 -*-

'''
    premiumizer Add-on
    Copyright (C) 2016 premiumizer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import os
import sys
import xbmcaddon
import urllib.parse as urlparse
import webbrowser
from resources.lib.modules import control, deviceAuthDialog
from resources.lib.api import trakt

import datetime
sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
control.moderator()

artPath = control.artPath()
addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065)

__addon__ = xbmcaddon.Addon("plugin.video.premiumizerx")

timeNow = datetime.datetime.now().strftime('%Y%m%d')
popup      = control.setting('popup.date')

class navigator:
    def root(self):
        from resources.lib.api import premiumize
        validAccount = premiumize.validAccount()
        if not validAccount:
            from resources.lib.modules import deviceAuthDialog
            authDialog = deviceAuthDialog.DonationDialog('firstrun.xml', xbmcaddon.Addon().getAddonInfo('path'), code='', url='')
            authDialog.doModal()
            del authDialog	
            control.openSettings('0.0')
            sys.exit()
        elif (popup == '0' or ((int(timeNow) - int(popup)) > 30)):
            from resources.lib.modules import deviceAuthDialog
            authDialog = deviceAuthDialog.DonationDialog('donations.xml', xbmcaddon.Addon().getAddonInfo('path'), code='', url='')
            authDialog.doModal()
            del authDialog	
            control.setSetting(id='popup.date', value=timeNow) 
        #self.addDirectoryItem('TEST', 'testItem', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(
            'Search Cloud', 'premiumizeSearch', 'cloud.png', 'DefaultMovies.png')
        self.addDirectoryItem('Meta Cloud', 'meta_cloud',
                              'cloud.png', 'DefaultTVShows.png')
#        self.addDirectoryItem('Meta Library', 'libraryNavigator',
#                              'cloud.png', 'DefaultMovies.png', isFolder=True)
        self.addDirectoryItem(50001, 'premiumizeNavigator',
                              'cloud.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Lists', 'browse_nav',
                              'cloud.png', 'DefaultTVShows.png')

        downloads = True if control.setting('downloads') == 'true' else False
        if downloads == True:
            self.addDirectoryItem(
                'Download Manager', 'download_manager', 'cloud.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32008, 'toolNavigator',
                              'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[I]Support and Donations[/I]', 'donations',
                              'support.png', 'DefaultAddonProgram.png', isFolder=False)
        self.endDirectory()

    def download_manager(self):
        self.addDirectoryItem(
            'Downloading', 'download_manager_list', 'cloud.png', 'DefaultFolder.png')
        downloads = True if control.setting('downloads') == 'true' else False
        if downloads == True:
            download_path = control.setting('download.path')
            dest = control.transPath(download_path)
            if len(control.listDir(dest)[0]) > 0:
                self.addDirectoryItem(
                    32009, dest, 'cloud.png', 'DefaultFolder.png', isAction=False)
        self.endDirectory()

    def browse_nav(self, lite=False):
        self.addDirectoryItem(32001, 'movieNavigator',
                              'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator',
                              'tv.png', 'DefaultTVShows.png')
        self.endDirectory()

    def meta_cloud(self):
        self.addDirectoryItem(
            'Movies', 'meta_folder&content=movie', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem('Tv', 'meta_folder&content=tv',
                              'tv.png', 'DefaultTVShows.png')
        self.endDirectory()

    def movies(self, lite=False):
        self.addDirectoryItem(40000, 'moviesInProgress',
                              'movies.png', 'DefaultRecentlyAddedMovies.png')
        #self.addDirectoryItem('New HD Releases', 'movies&url=newreleases',
        #                      'movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32017, 'movies&url=trending',
                              'movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(40009, 'movieFavourites',
                              'mymovies.png', 'DefaultMovies.png')
        if traktCredentials == True:
            self.addDirectoryItem('Trakt on Deck', 'traktOnDeck&content=movies',
                                  'trakt.png', 'DefaultMovies.png', queue=True)
        if traktCredentials == True and imdbCredentials == True:

            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(
                32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(
                32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(
                32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(
                32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(
                32035, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(
                32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists',
                              'mymovies.png', 'DefaultMovies.png')

        self.addDirectoryItem(32010, 'movieSearch',
                              'search.png', 'DefaultMovies.png')
        self.endDirectory()

    def premiumizeNav(self):
        from resources.lib.api import premiumize
        try:
            accountStatus = premiumize.info()
            self.addDirectoryItem(accountStatus, '0',
                                  'search.png', 'DefaultMovies.png')
        except:
            pass


        self.addDirectoryItem(
                50002, 'premiumizerootFolder', 'cloud.png', 'DefaultMovies.png')
        self.addDirectoryItem(
                50003, 'premiumizeTransfers', 'cloud.png', 'DefaultMovies.png')
        self.addDirectoryItem(50004, 'premiumizeAdd',
                                  'cloud.png', 'DefaultMovies.png')
        self.endDirectory()

    def library(self):
        self.addDirectoryItem('[B]LIBRARY[/B]: Update Library',
                              'update_meta_library', 'cloud.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]LIBRARY[/B]: Movies Library Path', control.setting(
            'meta.library.movies'), 'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem('[B]LIBRARY[/B]: TV Library Path', control.setting(
            'meta.library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)
        self.addDirectoryItem('[B]LIBRARY[/B]: Auto Setup Library Paths',
                              'setup_library_paths', 'cloud.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def mymovies(self, lite=False):
        self.addDirectoryItem(40009, 'movieFavourites',
                              'mymovies.png', 'DefaultMovies.png')

        if traktCredentials == True and imdbCredentials == True:

            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(
                32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem('Trakt on Deck', 'traktOnDeck&content=movies',
                                  'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(
                32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(
                32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem('Trakt on Deck', 'traktOnDeck&content=movies',
                                  'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(
                32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(
                32035, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(
                32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists',
                              'mymovies.png', 'DefaultMovies.png')

        self.endDirectory()

    def tvshows(self, lite=False):

        self.addDirectoryItem(32017, 'tvshows&url=trending',
                              'tv.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem('MY Watchlist', 'tvFavourites',
                              'mymovies.png', 'DefaultMovies.png')
        if traktCredentials == True:

            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(
                32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(
                32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(
                32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

        elif imdbCredentials == True:
            self.addDirectoryItem(
                32035, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(
                32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png',
                                  'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar',
                                  'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists',
                              'mytv.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists',
                                  'trakt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32010, 'tvSearch',
                              'search.png', 'DefaultTVShows.png')
        self.endDirectory()

    def mytvshows(self, lite=False):
        # self.accountCheck()
        self.addDirectoryItem('MY Watchlist', 'tvFavourites',
                              'mymovies.png', 'DefaultMovies.png')
        if traktCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(
                32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(
                32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(
                32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

        elif imdbCredentials == True:
            self.addDirectoryItem(
                32035, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(
                32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png',
                                  'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar',
                                  'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists',
                              'mytv.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists',
                                  'trakt.png', 'DefaultTVShows.png')

        # if lite == False:
            # self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
            # self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            # self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()

    def tools(self):

        self.addDirectoryItem(32043, 'openSettings&query=0.0',
                              'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32044, 'openSettings&query=1.0',
                              'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32048, 'openSettings&query=2.0',
                              'settings.png', 'DefaultAddonProgram.png')


        #self.addDirectoryItem(32052, 'clearCache', 'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]SETTINGS:[/B] Clear Cache/Meta',
                              'clearMeta', 'settings.png', 'DefaultAddonProgram.png')

        #self.addDirectoryItem(40006, 'backupSettings',
       #                       'settings.png', 'DefaultAddonProgram.png')
        #self.addDirectoryItem(40007, 'restoreSettings',
        #                      'settings.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]HELP[/B]', 'helpNavigator',
                              'help.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(
            '[B]CHANGELOG[/B]', 'changelogNavigator', 'help.png', 'DefaultAddonProgram.png')
        self.endDirectory()

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(
                32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(
                32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()

    def search(self):
        self.addDirectoryItem(32001, 'movieSearch',
                              'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(
            32002, 'tvSearch', 'search.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson',
                              'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(
            32030, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')

        self.endDirectory()

    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode(
                'utf-8'), sound=True, icon='WARNING')
            sys.exit()

    def clearCache(self):
        control.idle()
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057).encode(
            'utf-8'), sound=True, icon='INFO')

    def help(self):
        import xbmc
        import xbmcgui
        import xbmcaddon
        import xbmcvfs
        import os
        addonInfo = xbmcaddon.Addon().getAddonInfo
        addonPath = xbmc.translatePath(addonInfo('path'))
        changelogfile = os.path.join(addonPath, 'help.txt')
        r = open(changelogfile)
        text = r.read()

        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(500)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                retry -= 1
                win.getControl(1).setLabel('Version: %s' %
                                           (xbmcaddon.Addon().getAddonInfo('version')))
                win.getControl(5).setText(text)
                return
            except:
                pass

    def changelog(self):
        import xbmc
        import xbmcgui
        import xbmcaddon
        import xbmcvfs
        import os
        addonInfo = xbmcaddon.Addon().getAddonInfo
        addonPath = xbmc.translatePath(addonInfo('path'))
        changelogfile = os.path.join(addonPath, 'changelog.txt')
        r = open(changelogfile)
        text = r.read()

        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(500)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                retry -= 1
                win.getControl(1).setLabel('Version: %s' %
                                           (xbmcaddon.Addon().getAddonInfo('version')))
                win.getControl(5).setText(text)
                return
            except:
                pass

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name)
        except:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query

        thumb = control.getIcon(thumb)

        cm = []
        if queue == True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None:
            cm.append((control.lang(context[0]).encode(
                'utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url,
                        listitem=item, isFolder=isFolder)

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
