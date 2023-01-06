"""

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
"""

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import os, re, sys, string, json, random, base64
import shutil
import urllib
import time
#import urllib2

try:
    # Python 3
    from urllib.request import urlopen, Request
except ImportError:
    # Python 2
    from urllib2 import urlopen, Request

try:
    # Python 3
    from html.parser import HTMLParser
except ImportError:
    # Python 2
    from HTMLParser import HTMLParser

convert_special_characters = HTMLParser()
dlg = xbmcgui.Dialog()

from resources.lib.modules.common import *

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

art = 'special://home/addons/plugin.video.docula/resources/media/'

ytImage = 'https://i.ytimg.com/vi/URL/maxresdefault.jpg'
ytImage2 = 'https://i.ytimg.com/vi/URL/hqdefault.jpg'
ytImageHQ = 'https://i.ytimg.com/vi/URL/hqdefault.jpg'

#==========================================================================================================

class Listing:

    @staticmethod
    def Genres(type,list):

        #errorMsg="%s" % (type)
        #xbmcgui.Dialog().ok("type", errorMsg)

        if list is "History": eventsUrl = 'http://j1wizard.net/config/texts/historydocs.txt'
        if list is "Music": eventsUrl = 'http://j1wizard.net/config/texts/muzicdocs.txt'
        if list is "Sports": eventsUrl = 'http://j1wizard.net/config/texts/sportdocs.txt'
        if list is "Wrestling": eventsUrl = 'http://j1wizard.net/config/texts/docs.txt'
        #if list is "Events": eventsUrl = 'http://j1wizard.net/config/texts/events.txt'


        try: #Python 2
            link = OPEN_URL(eventsUrl).replace('\n','').replace('\r','').replace('\t','')
            #match = re.compile('item="(.+?)", "(.+?)", 801, "(.+?)", icon, fanart').findall(link)
        except: #Python 3
            link = OPEN_URL(eventsUrl)
            link = link.decode('ISO-8859-1')  # encoding may vary!

        match = re.compile('item="(.+?)", "(.+?)", 801, "(.+?)", .+?, fanart').findall(link)
		
        #errorMsg="%s" % (match)
        #xbmcgui.Dialog().ok("match", errorMsg)

        for name, url, genre in match:

            addIt=False

            if list is "History" and type is "All":
                icon=art+"History.png"
                addIt=True

            if list is "Music" and type is "All":
                icon=art+"Music.png"
                addIt=True

            if list is "Sports" and type is "All":
                icon=art+"Sports.png"
                addIt=True

            if list is "Wrestling" and type is "All":
                icon=art+"Wrestling.png"
                addIt=True
		
            if addIt==True:
                addLink(name,url,801,icon,fanart)

#=====================================
   
def OPEN_URL(url):

    try: #Python 2
        req = Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urlopen(req)
        link=response.read()
        response.close()
        return link
    except: #Python 3
        req = urllib.request.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib.request.urlopen(req)
        link=response.read()
        response.close()
        return link
	
#=====================================

def urlExists(url):

    request = Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        urlopen(request)
        return True
    except HTTPError:
        return False
	
#=====================================
