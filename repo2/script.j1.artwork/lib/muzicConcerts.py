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

mediapath = 'special://home/addons/script.j1.artwork/lib/resources/images/genres/'

channellist=[
        ("[B]Dirty Honey Live at the Viper Room (2020)[/B]", "w2lro88_-kM", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Michael Jackson - Live At Wembley (July 16, 1988)[/B]", "9shByOh8fVE", 801, "POP", mediapath+'Concert.png', fanart),
        ("[B]Greta Van Fleet Live: Red Rocks Amphitheater Act 1 (2019)[/B]", "FcpFCZgTu7I", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Greta Van Fleet Live: Red Rocks Amphitheater Act 2 (2019)[/B]", "ENfETz7RCwo", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Greta Van Fleet Live: Red Rocks Amphitheater Act 3 (2019)[/B]", "_CXk6gUfTcg", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Janis Joplin: Live (1969-1970)[/B]", "Fm81oN5m-Qk", 801, "Rock, Blues", mediapath+'Concert.png', fanart),
        ("[B]Janis Joplin: Live in Frankfurt, Germany[/B]", "5NuZxUxHN0o", 801, "Rock, Blues", mediapath+'Concert.png', fanart),
        ("[B]Black Sabbath: Live At Ozzfest 2005[/B]", "D9yawWUIit0", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Black Sabbath: Wells Fargo Center, PA 2013[/B]", "yHPNEr3CWuA", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Justin Moore: Off The Beaten Path[/B]", "t0mryb76L9M", 801, "Country", mediapath+'Concert.png', fanart),
        ("[B]Willie Nelson: Live At Woodstock 1999[/B]", "VqGeDnXmB6I", 801, "Country", mediapath+'Concert.png', fanart),
        ("[B]Willie Nelson: Live At Beach Life 2019[/B]", "SSApQVLsErw", 801, "Country", mediapath+'Concert.png', fanart),
        ("[B]Heart Of Country - Legends In Concert[/B]", "2vyP2pUMgpU", 801, "Country", mediapath+'Concert.png', fanart),
        ("[B]Brooks n Dunn: Cains Ballroom 2005[/B]", "trXPUI6eqLo", 801, "Country", mediapath+'Concert.png', fanart),
        ("[B]The Women Of Country: CBS Special 1993[/B]", "vP1LJ5XwWVw", 801, "Country", mediapath+'Concert.png', fanart),
        ("[B]Brad Paisley Live Country Concert 2018[/B]", "df_hfptZKHU", 801, "Country", mediapath+'Concert.png', fanart),
        ("[B]Johnny Cash: Live In Austin, Tx 1987[/B]", "b2h_elvIYXI", 801, "Country", mediapath+'Concert.png', fanart),
        ("[B]Legends Of Country Guitar In Concert[/B]", "m82SBydm_7c", 801, "Country", mediapath+'Concert.png', fanart),
        ("[B]Maroon 5: Rock At Rio Live 2017[/B]", "6KwKDFKfhxc", 801, "Pop, Alternative", mediapath+'Concert.png', fanart),
        ("[B]Judas Priest: Seminole Hard Rock 2019[/B]", "ChZ3iHZgUIQ", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Travis Tritt: Live Country Concert[/B]", "vFTaoTVrEwk", 801, "Country, Rock", mediapath+'Concert.png', fanart),
        ("[B]Evanescence: Rock Am Ring 2003[/B]", "ufy7hNJzmik", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Incubus: Live At Rock Am Ring 2008[/B]", "pjx37Fofjr4", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Foo Fighters: Rock Am Ring 2015[/B]", "pnrx1UV6mdQ", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Iron Maiden: Legacy Of The Beast 2019[/B]", "6KdN6_4a8IY", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]System Of A Down: Rock In Rio 2011[/B]", "n1gzz0Hnor0", 801, "Rock, Alternative", mediapath+'Concert.png', fanart),
        ("[B]Billie Eilish: Reading Festival 2019[/B]", "miM5tubtvfA", 801, "Pop, Alternative", mediapath+'Concert.png', fanart),
        ("[B]Godsmack: Rock On The Range 2018[/B]", "OxoiPKol3co", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Linkin Park: Rock Am Ring 2004[/B]", "5BMe_UP5R9I", 801, "Rock, Metal, Alternative", mediapath+'Concert.png', fanart),
        ("[B]Shakira: Rock In Rio Concert[/B]", "g-p4-WSdAqA", 801, "Rock, Pop", mediapath+'Concert.png', fanart),
        ("[B]AC/DC: Live In Toronto 2003[/B]", "tHbCTqP5rYo", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Journey: Journeys Best Live 2018[/B]", "ezCouyLd4S4", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]The Who: Live At Rio 2017[/B]", "iOs0QsB_X8Q", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]George Thorogood: Capitol Theatre 07/05/84[/B]", "KDd7wBXTIRc", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Gun n Roses: Arena Londres 2012[/B]", "1tNaYFZT-Rk", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]The Ramones: Live At Theatre de l Empire 1980[/B]", "qwg0VPJSAaE", 801, "Rock, Punk", mediapath+'Concert.png', fanart),
        ("[B]Huey Lewis & the News: Live 05/23/89[/B]", "IwztgcEPnoE", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Stone Temple Pilots: Bizarre Fest 2001[/B]", "MrLzCepgXjc", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Green Day: Reading Festival 2013[/B]", "ZNLXO9Mw6NQ", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Traffic: Live At Woodstock 1994[/B]", "N0tf8FIPZsw", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Moody Blues: Live at the Royal Albert Hall[/B]", "q8474UHL-dk", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Chicago: Live at Tanglewood 07/21/1970[/B]", "_oAoSZ2y1cw", 801, "Rock, Jazz, Blues", mediapath+'Concert.png', fanart),
        ("[B]Greta Van Fleet: Live At ACL 2018[/B]", "WgPVKIIGymQ", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]B52s: With The Wild Crowd Live 2011[/B]", "NBpYsS5V35o", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Jethro Tull Live at the Capital Centre 1977[/B]", "QByXiqkECKQ", 801, "Rock, Alternative, Jazz", mediapath+'Concert.png', fanart),
        ("[B]Pearl Jam: Live At Lollapalooza 2018[/B]", "pZtx9ba_bWc", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Joe Satriani Satchurated Live 2012[/B]", "L0rpgwJnd-k", 801, "Rock, Metal, Blues", mediapath+'Concert.png', fanart),
        ("[B]Soundgarden: Hard Rock Calling 2012[/B]", "IN3CBIV79ug", 801, "Rock, Metal, Blues", mediapath+'Concert.png', fanart),
        ("[B]Genesis: Live At Wembley Stadium 1987[/B]", "A3Q8KOkimE0", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]R.E.M. Live At The Rockpalast 2005[/B]", "rD9BSKNcn0g", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Stone Temple Pilots SWU Festival 2011[/B]", "IN3CBIV79ug", 801, "Rock, Metal, Blues", mediapath+'Concert.png', fanart),
        ("[B]The Cure: Live At Lollapalooza 2008[/B]", "ckdHyuPZY8s", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]The Doors: Live At Isle of Wight 1970[/B]", "51SAvWieaNc", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Black Sabbath, Deep Purple, Led Zeppelin[/B]", "uOSS3v1O61w", 801, "Rock, Metal, Blues", mediapath+'Concert.png', fanart),
        ("[B]Robert Plant & Jimmy Page Live 1995[/B]", "lTaLMkwgem4", 801, "Rock, Metal, Blues", mediapath+'Concert.png', fanart),
        ("[B]Tom Petty & The Heartbreakers 2006[/B]", "tw_-wYgFlbE", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]The Police: The Tokyo Dome 2008[/B]", "tuBhwEgi8qU", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]National Lampoon Lemmings 1973[/B]", "tuBhwEgi8qU", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Alice Cooper: Live In Sydney[/B]", "j7NVzpY7jkU", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Motley Crue: Carnival Of Sins[/B]", "EnZKhKSLqRk", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Boston @ The Forum[/B]", "G0UU4yyKmyI", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Def Leppard Viva Hysteria[/B]", "3zzvM6s0lmA", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Led Zeppelin Celebration Day[/B]", "ZPeUzqSyHeI", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Elton John Live In Hyde Park[/B]", "YLQXvLPe2yU", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Red Hot Chili Peppers At Slane Castle[/B]", "FmrGz8qSyrk", 801, "Rock, Alternative", mediapath+'Concert.png', fanart),
        ("[B]Lynyrd Skynyrd 07/13/77 Convention Hall[/B]", "FbMVdXLDRWQ", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Aerosmith: Woodstock 1994[/B]", "Gerf9gHEJoY", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Queen: Hammersmith Odeon (12/24/75)[/B]", "ETn5XZDaT60", 801, "Alternative", mediapath+'Concert.png', fanart),
        ("[B]Beatles, Stones, Kinks, Animals & More[/B]", "93HYF8uuT3s", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Monsters Of Rock Moscow 1991[/B]", "3Mtilj2gKz0", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Slipknot Live At Knotfest 2012[/B]", "5T0RS6bkOAg", 801, "Metal", mediapath+'Concert.png', fanart),
        ("[B]Metalica Freeze Em All Live In Antartica[/B]", "2Hi2u98VKxc", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Little River Band Houston, Tx 1981[/B]", "7qMy-dfO-sU", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Foo Fighters Hyde Park 2006[/B]", "P8fA4RRYmUQ", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]AC/DC Oakland Coliseum Stadium 1979[/B]", "epSe9V5ngeo", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Skillet Live At Pinkpop 2016[/B]", "NdboG7BJtHo", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Grateful Dead Roosevelt Stadium 1976[/B]", "G1yLgdzAbXQ", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Grateful Dead San Francisco 1983[/B]", "C9AQiF5fFFI", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Joe Bonamassa Live Concert 2017[/B]", "6Yht1A-8Q8w", 801, "Rock, Metal, Blues", mediapath+'Concert.png', fanart),
        ("[B]Fab Four Beatles Tribute Band[/B]", "4rHiDArtjuM", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Bob Marley Rockpalast, Dortmund 1980[/B]", "XspU6g9m2Fs", 801, "Reggae", mediapath+'Concert.png', fanart),
        ("[B]Van Halen Oakland Coliseum 1981[/B]", "VQgHvOvujNE", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Nirvana Reading Festival 1992[/B]", "RYAIQRPPu5w", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Stevie Ray Vaughan Live at Montreux 1985[/B]", "S2uMYyAKFvU", 801, "Rock, Metal, Blues", mediapath+'Concert.png', fanart),
        ("[B]Styx Return To Paradise 1997[/B]", "Sg6ccWZJo4I", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]David Bowie: Go Bang Fest 1997[/B]", "benRujPzThQ", 801, "Rock, Alternative", mediapath+'Concert.png', fanart),
        ("[B]Uriah Heep Live in London 2019[/B]", "SuieQnKcT14", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Journey live in Tokyo - 07/31/81[/B]", "AZfVJdVzvpg", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Bon Jovi: A Night With Bon Jovi[/B]", "4yocblnuvnk", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Deep Purple Live at Montreux 2011[/B]", "avG1a36FaqM", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Journey Live Concert 2018[/B]", "ezCouyLd4S4", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Santana Live In Tanglewood 1970[/B]", "b3_TQKdksyc", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]My Chemical Romance - Black Parade Is Dead[/B]", "Ud2eziOjjTo", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Allman Brothers Band University Of Florida 1982[/B]", "F78XV6fjxCE", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Van Halen Toronto 8/19/1995[/B]", "WFgkhz3-Dp0", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Pantera Killing In Korea[/B]", "6-Jvkf9jlNw", 801, "Metal", mediapath+'Concert.png', fanart),
        ("[B]Linkin Park Live Roxy Theatre 2000[/B]", "MzCPdJQ3EvQ", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]The Who Live In Glastonbury 2007[/B]", "HbRbk_RZRRI", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]ZZ Top Live Concert[/B]", "dNgPfkayAlw", 801, "Rock, Metal, Blues", mediapath+'Concert.png', fanart),
        ("[B]ZZ Top Live at Bonnaroo 2013[/B]", "-uZinAmZtJg", 801, "Rock, Metal, Blues", mediapath+'Concert.png', fanart),
        ("[B]ZZ TOP Live at Rockpalast 1980[/B]", "xpxFzLg1Vi8", 801, "Rock, Metak, Blues", mediapath+'Concert.png', fanart),
        ("[B]Jimi Hendrix Live Full Concert 1969[/B]", "qPrAg3sXIAM", 801, "Rock, Metal, Blues", mediapath+'Concert.png', fanart),
        ("[B]Foghat: Live Two Centuries of Boogie 1998[/B]", "Z5sHdkHb-2U", 801, "Rock, Blues", mediapath+'Concert.png', fanart),
        ("[B]Bachman Turner Overdrive Live[/B]", "YukhsMPHvvo", 801, "Rock, Blues", mediapath+'Concert.png', fanart),
        ("[B]Janis Joplin: Big Brother & Holding Co.[/B]", "Fm81oN5m-Qk", 801, "Rock, Blues", mediapath+'Concert.png', fanart),
        ("[B]Styx Live In Los Angeles 2014[/B]", "pZThG_d4lyc", 801, "Rock", mediapath+'Concert.png', fanart),
        ("[B]Toto 35 Anniversary Tour 2013[/B]", "s021m2C7-aI", 801, "Rock, Metal", mediapath+'Concert.png', fanart),
        ("[B]Foreigner Live In New York 2015[/B]", "kF_copPwqkA", 801, "Rock", mediapath+'Concert.png', fanart),
]

#=====================================

class concertListing:

    @staticmethod
    def Genres(type):
		
        #errorMsg="%s" % (type)
        #xbmcgui.Dialog().ok("type", errorMsg)

        for name, url, zmode, genre, icon, fanart in sorted(channellist, reverse=False):
	        addLink(name,url,zmode,icon,fanart)

#=====================================

