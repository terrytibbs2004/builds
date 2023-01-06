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
    from urllib.request import urlopen, Request, HTTPError
except ImportError:
    # Python 2
    from urllib2 import urlopen, Request, HTTPError

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

art = 'special://home/addons/script.j1.artwork/lib/resources/art/'
eventsUrl = 'http://j1wizard.net/config/texts/events.txt'
ytImage = 'https://i.ytimg.com/vi/URL/maxresdefault.jpg'
ytImage2 = 'https://i.ytimg.com/vi/URL/hqdefault.jpg'

class eventListing:

    @staticmethod
    def Genres(type):
		
        #errorMsg="%s" % (type)
        #xbmcgui.Dialog().ok("type", errorMsg)

        try: #Python 2
            link = OPEN_URL(eventsUrl).replace('\n','').replace('\r','').replace('\t','')
            #match = re.compile('item="(.+?)", "(.+?)", 801, "(.+?)", icon, fanart').findall(link)
        except: #Python 3
            link = OPEN_URL(eventsUrl)
            link = link.decode('ISO-8859-1')  # encoding may vary!

        match = re.compile('item="(.+?)", "(.+?)", 801, "(.+?)", icon, fanart').findall(link)
		
        #errorMsg="%s" % (match)
        #xbmcgui.Dialog().ok("match", errorMsg)

        for name, url, genre in match:

            addIt=False
            if type is "All":
                icon=art+"events.jpg"
                addIt=True

            elif type is "1pw" and '1PW' in genre:
                icon=art+"1pw.jpg"
                addIt=True

            elif type is "aaw" and 'AAW' in genre:
                icon=art+"aaw.jpg"
                addIt=True

            elif type is "bwf" and 'BRONX' in genre:
                icon=art+"bwf.jpg"
                addIt=True

            elif type is "ccw" and 'CCW' in genre:
                icon=art+"cascade.jpg"
                addIt=True

            elif type is "wwa" and 'WWA' in genre:
                icon=art+"wwa.jpg"
                addIt=True

            elif type is "defiant" and 'DEFIANT' in genre:
                icon=art+"defiant.jpg"
                addIt=True

            elif type is "evolve" and 'EVOLVE' in genre:
                icon=art+"evolve.jpg"
                addIt=True

            elif type is "ewf" and 'EMPIRE' in genre:
                icon=art+"ewf.jpg"
                addIt=True
				
            elif type is "roh" and 'ROH' in genre:
                icon=art+"aew.jpg"
                addIt=True
				
            elif type is "brit" and 'BRIT' in genre:
                icon=art+"brit.jpg"
                addIt=True
				
            elif type is "capitol" and 'CAPITOL' in genre:
                icon=art+"capitol.jpg"
                addIt=True

            elif type is "ipw" and 'IPW' in genre:
                icon=art+"ipw.jpg"
                addIt=True

            elif type is "mlw" and 'MLW' in genre:
                icon=art+"mlw.jpg"
                addIt=True

            elif type is "row" and 'ROW' in genre:
                icon=art+"row.jpg"
                addIt=True

            elif type is "pcw" and 'PCW' in genre:
                icon=art+"pcw.jpg"
                addIt=True

            elif type is "hob" and 'HOB' in genre:
                icon=art+"hob.jpg"
                addIt=True

            elif type is "hog" and 'HOG' in genre:
                icon=art+"hog.jpg"
                addIt=True

            elif type is "misc" and 'MISC' in genre:
                icon=art+"misc.jpg"
                addIt=True

            elif type is "nwa" and 'NWA' in genre:
                icon=art+"nwa.jpg"
                addIt=True

            elif type is "owe" and 'OWE' in genre:
                icon=art+"owe.jpg"
                addIt=True

            elif type is "champ" and 'CHAMP' in genre:
                icon=art+"champ.jpg"
                addIt=True

            elif type is "pwa" and 'PWA' in genre:
                icon=art+"pwa.jpg"
                addIt=True

            elif type is "pwl" and 'PWL' in genre:
                icon=art+"pwl.jpg"
                addIt=True

            elif type is "wlw" and 'WLW' in genre:
                icon=art+"wlw.jpg"
                addIt=True

            elif type is "fwa" and 'FWA' in genre:
                icon=art+"fwa.jpg"
                addIt=True

            elif type is "progress" and 'PROGRESS' in genre:
                icon=art+"progress.jpg"
                addIt=True

            elif type is "rise" and 'RISE' in genre:
                icon=art+"rise.jpg"
                addIt=True

            elif type is "smash" and 'SMASH' in genre:
                icon=art+"smash.jpg"
                addIt=True

            elif type is "ovw" and 'OVW' in genre:
                icon=art+"ovw.jpg"
                addIt=True

            elif type is "tna" and 'TNA' in genre:
                icon=art+"impact.jpg"
                addIt=True

            elif type is "women" and 'WOMEN' in genre:
                icon=art+"wow.jpg"
                addIt=True

            elif type is "wwe" and 'WWE' in genre:
                icon=art+"wwe.jpg"
                addIt=True
		
            if addIt==True:

                theImage = ytImage.replace('URL',url)
                exists = urlExists(theImage)
                if exists is True:
	                addLink(name,url,801,theImage,fanart)
                else:
	                theImage = ytImage2.replace('URL',url)                    				
	                exists = urlExists(theImage)
	                if exists is True:
	                    addLink(name,url,801,theImage,fanart)
                if exists is False:
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
		