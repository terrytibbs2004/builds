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

art = 'special://home/addons/script.j1.artwork/lib/resources/art/'
ytImageHQ = 'https://i.ytimg.com/vi/URL/hqdefault.jpg'

#==========================================================================================================

channellist=[
        ("[B]OVW: One Night Special Womens Championship 8/26/2017[/B]", "-0Fu_yCU2jA", 801, "OVW, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN: Womens Wrestling 4/1/21[/B]", "KeHCBbdCvpE", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN: Womens Wrestling 4/1/21[/B]", "ePxygtUwDKY", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN: Womens Wrestling 3/6/21[/B]", "AIbzMY8VWzc", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN: Womens Wrestling 2/5/21[/B]", "64Ibiuf3lNk", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]Best of Womens Wrestling in ECCW 1/21/21[/B]", "0B5wdy4dTdA", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN: Womens Wrestling 2/1/21[/B]", "6nZs1lDg1-A", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN: Womens Wrestling 1/22/21[/B]", "gmbs0ISUIBk", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN: Womens Wrestling 1/13/21[/B]", "HHNL2r8Rios", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN: Womens Wrestling 1/11/21[/B]", "wYusLHr3F3M", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 1/8/21[/B]", "oFfcrCUh3tA", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN: Womens Wrestling 1/4/21[/B]", "AC435ZuQhHk", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 1/3/21[/B]", "mnm7QfJ_PGM", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN: 50 Most Watched Ladies Night Out Matches 12/31/20[/B]", "rBsYQpobqQI", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Pro Wrestling Livestream - Lindsay Snow, Annie Social, Scott Steiner, Jordynne Grace, AJ Styles 12/25/20[/B]", "KnfVSrDoFZQ", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Pro Wrestling Livestream - Angelina Love, Thunder Rosa, Mia Yim, La Rosa Negra, Holidead 12/19/20[/B]", "bMOtVaOUSVE", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 12/17/20[/B]", "HrTRweSDHMI", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 12/13/20[/B]", "fxal-uNWvUw", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 12/11/20[/B]", "ZKg2nSefzR4", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 12/10/20[/B]", "JCNnYzSIbGE", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]EVE Womens Wrestling: 12/6/20[/B]", "35MH371p_tg", 801, "EVE, WOMEN", art+'eve.jpg', fanart),    
        ("[B]EVE Womens Wrestling: 12/8/20[/B]", "Tm44WFV2kXE", 801, "EVE, WOMEN", art+'eve.jpg', fanart),    
        ("[B]WWE: Hell in a Cell full matches (10/25/20)[/B]", "1M9rue59HWo", 801, "WWE", art+'wwe.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 11/27/20[/B]", "bMOtVaOUSVE", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]ROW: Best of Hyan (4/12/20)[/B]", "t7p5DaG7VxQ", 801, "ROW", art+'row.jpg', fanart),    
        ("[B]ROW: Best of Alex Gracia (5/12/20)[/B]", "VILXL1N6u-o", 801, "ROW", art+'row.jpg', fanart),    
        ("[B]TMN Best of Wrestlecade Night I - Showcase of Champions (11/27/20)[/B]", "be0ADLrlbD0", 801, "TMN", art+'tmn.jpg', fanart),    
        ("[B]TMN Best of Wrestlecade Night II (11/28/20)[/B]", "DvDcRq96BNQ", 801, "TMN", art+'tmn.jpg', fanart),    
        ("[B]TMN Best of Wrestlecade Night III (11/29/20)[/B]", "7tOl0sMasPU", 801, "TMN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 11/28/20[/B]", "qWOOdLMkrUs", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 11/21/20[/B]", "E0fbyMwIBgg", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 11/20/20[/B]", "PfDuC9PA_M4", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 11/15/20[/B]", "wqjsvop5Yv0", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TNA: Before The Glory 2010[/B]", "9ck4wfTrtmk", 801, "TNA", art+'impact.jpg', fanart),
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 11/13/20[/B]", "XS2MwTy-ebE", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]AOW-UK: Golden Chance 2018[/B]", "6cONitfXy0Y", 801, "MISC", art+'misc3.jpg', fanart),    
        ("[B]Wildkat Sports Revolution Rumble (2019)[/B]", "QkLtKBxvYtI", 801, "MISC", art+'misc2.jpg', fanart),    
        ("[B]Women Extreme Wrestling Booty Whipping 10/29/20[/B]", "7qXIOAyles4", 801, "WOMEN", art+'wew.jpg', fanart),    
        ("[B]Women Extreme Wrestling Get Me Bail 10/28/20[/B]", "zePC6ohOSS0", 801, "WOMEN", art+'wew.jpg', fanart),    
        ("[B]Women Extreme Wrestling Criminal Battery 9/15/20[/B]", "Ht80mx1xEvc", 801, "WOMEN", art+'wew.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 11/1/20[/B]", "LgKVmiVI-3E", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]ECWA: Super 8 ChickFight Tournament 10/25/20[/B]", "6dH6SYG5FYA", 801, "MISC, WOMEN", art+'misc2.jpg', fanart),    
        ("[B]TMN: Intergender Wrestling, Penelope Ford, Maria Manic, Kris Statlander 10/7/20[/B]", "tYGqU9UBw0A", 801, "MISC, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/30/20[/B]", "XdPOnthaL_g", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]USA vs Canada - Midget Wrestling 2015[/B]", "8Mw9D34LP58", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]WAW: Straight Out Of WAW Academy (10/3/20)[/B]", "aW3CZHU4pJ4", 801, "WAW", art+'waw.jpg', fanart),
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/24/20[/B]", "tenBWm_or5c", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/23/20[/B]", "5M01R-1anf4", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]WWA Hysteria 106 Danger At The Door 10/18/2020[/B]", "bas-eIB_TeE", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/19/20[/B]", "PJJ0ZjaQyPg", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/18/20[/B]", "Xhh2O7hUHw4", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]AEW Dynamite Episode #1 (10/2/2019)[/B]", "Soy9DqsTTco", 801, "AEW", art+'aew.jpg', fanart),
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/16/20[/B]", "m2vtQyYfVLM", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/13/20[/B]", "6IXdpyYH5hI", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/11/20[/B]", "-U6XUd24Fyg", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/9/20[/B]", "obVLGAOyYx8", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/4/20[/B]", "gv08Po7VtVE", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 10/2/20[/B]", "ShIJDN8Mpis", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Best of Alex Gracia in Ladies Night Out[/B]", "LW0tp5kr2SI", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling N Intergender Wrestling: 9/24/20[/B]", "N77xswqkJ9g", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]WWA Hysteria 105 To The Extreme 9/12/2020[/B]", "sqHPcx5KSVs", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WAW: Straight Out Of WAW Academy Pt2 (9/12/20)[/B]", "IbQ-LV-Lly8", 801, "WAW", art+'waw.jpg', fanart),
        ("[B]TMN Womens Wrestling: 8/14/20[/B]", "m-ryKxdZ1g0", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]EVE: Classic Womens Wrestling Stream[/B]", "V82Wqgqg6_0", 801, "EVE, WOMEN", art+'eve.jpg', fanart),
        ("[B]WAW: Straight Out Of WAW Academy 9/12/20[/B]", "8ue4si967Pc", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]Rise: Point At The Sign II 2019[/B]", "mf4ZIS2pJOo", 801, "RISE, WOMEN", art+'rise.jpg', fanart),
        ("[B]WWA One Night Only 2017[/B]", "EEgOuUejvTk", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]Midget Madness Comedy (1989)[/B]", "wM41rQZUEiU", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Real Canadian Wrestling: Midget Wrestling Warriors 2016[/B]", "TzGj-_T3x6o", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Midget Wrestling Show Project 2015[/B]", "63f1L6Gpjq0", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Midget Wrestling Warriors present Apocalypse 2016[/B]", "J646vNP5h-A", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Micro Wrestling Pigeon Forge, TN 2019[/B]", "lHUJ_Kf4Gsc", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Extreme Midget Wrestling: Tilted Kilt Skokie, IL 2018[/B]", "Ri__tBZ5Rf4", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Midget Wrestling: Elwood Opera House - Elwood Indiana 2013[/B]", "kE_RmLAXsKA", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Midget Wrestling: The Cellar Door Visalia 2017[/B]", "QkKH_6CmMGk", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Midget Wrestling Show hosted by WWE Legend Capt Lou Albano[/B]", "crjS7YJxEGM", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Midget Wrestling: Florida State Fair 2017[/B]", "0Lco0ApJ76Y", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Midget Mania: Bancroft, Ontario Canada August 20, 1992[/B]", "NBcHAJb1XAA", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Extreme Midget Wrestling: Volume 1 2016[/B]", "N0bwYYK2hK0", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Extreme Midget Wrestling: Volume 2 2017[/B]", "GCkyBcb1pHg", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Extreme Midget Wrestling: 03/19/19[/B]", "EvkEQ8toFzM", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]Midget Mania From Philadelfia 2017[/B]", "lBbsPZCHLNY", 801, "MIDGET, MISC", art+'midget.jpg', fanart),    
        ("[B]TMN Womens Wrestling Showcase: 9/3/20[/B]", "bqaRNS0Csmg", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 8/30/20[/B]", "OJh2B4UL8Uc", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]Womens Wrestling: SEAdLINNNG5 (8/26/20)[/B]", "Syz0aWktbeM", 801, "WOMEN", art+'misc2.jpg', fanart),    
        ("[B]Stardom: Cinderella Tournament 2019[/B]", "Jc3gvzgY1o8", 801, "WOMEN", art+'stardom.jpg', fanart),    
        ("[B]WWE: The Best Of Summerslam (8/23/20)[/B]", "vOx3oj-VzQA", 801, "WWE", art+'wwe.jpg', fanart),    
        ("[B]WWE: The Best NXT TakeOver Title Matches (8/22/20)[/B]", "hu52ZF9kXa8", 801, "WWE", art+'wwe.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 8/21/20[/B]", "amJH93LU6Iw", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]Queens Of Combat: Season 1 Ep 1[/B]", "YVy9oWW7zq0", 801, "WOMEN", art+'tmn.jpg', fanart),    
        ("[B]WAW TV featuring Bellatrix S01 E20: 8/16/20[/B]", "wmlbU09eho4", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]TMN Womens Wrestling: 8/14/20[/B]", "m-ryKxdZ1g0", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: Best of Su Yung 8/12/20[/B]", "Tn3oXYgeVBo", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 8/6/20[/B]", "JXNu03RI_jI", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 8/2/20[/B]", "o7X3_wVjzi4", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 7/31/20[/B]", "sDTVeaY-0A8", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 3/14/20[/B]", "iLyIzMp3w1Y", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]AEW Womens Tag Team Cup: Night #2[/B]", "a-a8umBNnIA", 801, "AEW, WOMEN", art+'aew.jpg', fanart),
        ("[B]AEW Womens Tag Team Cup: Night #1[/B]", "iXcCQ9mhODc", 801, "AEW, WOMEN", art+'aew.jpg', fanart),
        ("[B]WAW TV featuring Bellatrix S01 E19: 8/2/20[/B]", "4JVfLwX08bM", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]WWA Hysteria 104 War Games 8/15/2020[/B]", "sieO5_N5xlw", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]TMN Pro Wrestling: 8/8/20[/B]", "YY52NHBQZtg", 801, "TMN", art+'tmn.jpg', fanart),    
        ("[B]VCW: Frank The Flame Barnhill Memorial Part 2 (8/6/20)[/B]", "y6qiXCAhbuI", 801, "MISC", art+'victory.jpg', fanart),
        ("[B]VCW: Frank The Flame Barnhill Memorial Part 1 (7/30/20)[/B]", "MSd4yWEH9Z8", 801, "MISC", art+'victory.jpg', fanart),
        ("[B]VCW: Lethal Leap Year (2/29/20)[/B]", "uOilJf8HIbA", 801, "MISC", art+'victory.jpg', fanart),
        ("[B]FWA: Road To Glory 2020[/B]", "khyZX4_9ctk", 801, "FWA", art+'fwa.jpg', fanart),    
        ("[B]WAW TV featuring Bellatrix S01 E18: 8/2/20[/B]", "AMVRnjbWAfY", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]TMN Womens Wrestling: 7/26/20[/B]", "TGPpcyDzoOA", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]WAW TV featuring Bellatrix S01 E17: 7/26/20[/B]", "YbYcYkt99tk", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]The Undertaker: The Complete 90s Collection 2020[/B]", "nXfr42ZAPGE", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]TMN Womens Wrestling: 7/25/20[/B]", "24XtJLLfmas", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 7/24/20[/B]", "pDqlN9biR-c", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: Best of Diamante 2020[/B]", "vvH1zfGPa4w", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]Rise: Tessa Blanchard vs. Mercedes Martinez 2018[/B]", "apoJgbkKRb0", 801, "RISE, WOMEN", art+'rise.jpg', fanart),
        ("[B]ROH: CM Punk Vs Samoa Joe 2019[/B]", "BpC7byrTu6I", 801, "ROH", art+'roh.jpg', fanart),
        ("[B]Rockstar Pro: Armageddon Games 2020[/B]", "_1dihlD0BBs", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]WAW TV featuring Bellatrix S01 E16: 7/19/20[/B]", "BgGOPAevc_Y", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]TMN Womens Wrestling: 7/17/20[/B]", "aLK6XGHHNK8", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]WWE Wrestling November 1994[/B]", "7NMg2IbcP30", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]TMN Womens Wrestling: 7/10/20[/B]", "jdqP6sYlNBQ", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]AWL Openweight Title Trilogy: Sullivan vs Matters[/B]", "oEJLE_xxPs8", 801, "AWL", art+'awl.jpg', fanart),
        ("[B]WAW TV featuring Bellatrix S01 E15: 7/12/20[/B]", "fTYSieeHipU", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]WAW TV featuring Bellatrix S01 E14: 7/5/20[/B]", "gR-Q_EDqrj4", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]TMN Womens Wrestling: Best of Annie Social 7/4/20[/B]", "P5qQWzzpr1g", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]Wrestling GO: You Go Girl 3/2/2019[/B]", "yOH40HAfDCQ", 801, "WOMEN", art+'misc2.jpg', fanart),    
        ("[B]Best of the West presents: Quarantine 2020[/B]", "S2N_7s0WqZ0", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]Discovery Wrestling: The 2019 Disco Derby[/B]", "8YTQ48ZyspM", 801, "WOMEN", art+'discovery.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 7/3/20[/B]", "csXwEfeDSTc", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]WAW Presents Hard Times 3/22/20[/B]", "l4rUAeitwfo", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]WAW TV featuring Bellatrix S01 E13: 6/28/20[/B]", "d3COmMCBT_I", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]WAW TV featuring Bellatrix S01 E12: 6/21/20[/B]", "qfIBSrtv_iw", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]ROW: Lucha Libre in Texas City[/B]", "DzUQ39ljoPc", 801, "ROW", art+'row.jpg', fanart),
        ("[B]Inspire Pro Wrestling: Quick & The Dead 10/13/13[/B]", "CXTB9seUkdI", 801, "MISC", art+'ipw.jpg', fanart),
        ("[B]TMN Womens Wrestling: 6/26/20[/B]", "3uDj7m0heJE", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 6/25/20[/B]", "HeACVi4--nA", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]FWA: Femme Fatales Vol. 1 | 1/19/20[/B]", "PbOCMzvnkzg", 801, "WOMEN", art+'fwa.jpg', fanart),    
        ("[B]Bellatrix Female Warriors: Season 01 - Episode 09[/B]", "jphqV5-u-G0", 801, "WAW, WOMEN", art+'waw.jpg', fanart),    
        ("[B]WAW TV featuring Bellatrix S01 E11: 6/14/20[/B]", "dRb1GNNswYY", 801, "MISC, WAW", art+'waw.jpg', fanart),
        ("[B]WAW Fightmare TV S01 E08: 6/16/20[/B]", "Kqk47I7QeHo", 801, "WAW", art+'waw.jpg', fanart),
        ("[B]WAW Fightmare TV S01 E07: 6/2/20[/B]", "TjAeg8hAbgc", 801, "WAW", art+'waw.jpg', fanart),
        ("[B]WAW Fightmare TV S01 E05: 5/5/20[/B]", "XN-Q5xOoeps", 801, "WAW", art+'waw.jpg', fanart),
        ("[B]WAW Fightmare TV S01 E04: 4/21/20[/B]", "OWkiUgihjUg", 801, "WAW", art+'waw.jpg', fanart),
        ("[B]WAW Fightmare TV S01 E03: 4/14/20[/B]", "jHfTPOKq1cI", 801, "WAW", art+'waw.jpg', fanart),
        ("[B]WAW Fightmare TV S01 E02: 4/7/20[/B]", "fxF3X4Mg_4o", 801, "WAW", art+'waw.jpg', fanart),
        ("[B]WAW Fightmare TV S01 E01: 3/31/20[/B]", "WK0kEl1T25w", 801, "WAW", art+'waw.jpg', fanart),
        ("[B]Bellatrix Female Warriors: Season 01 - Episode 08[/B]", "OigT30Cu6ik", 801, "WAW, WOMEN", art+'waw.jpg', fanart),    
        ("[B]TMN Ladies Night Out: Underground Ep1 2019[/B]", "ZGXOVjUmJGI", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),
        ("[B]Best of Alex Gracia in Reality of Wrestling[/B]", "VILXL1N6u-o", 801, "ROW, WOMEN", art+'row.jpg', fanart),
        ("[B]WWE Vengeance 2001 FULL MATCH[/B]", "WNqIHDI5zfY", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]TMN Tessa Blanchard, Su Yung, Jordynne Grace, Mia Yim, Kylie Rae 6/14/20[/B]", "2PiR7ibO3bA", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),
        ("[B]TMN Womens Wrestling: 6/12/20[/B]", "esHzCAd1xAk", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]Thunder Queens Battle 7-31-1993[/B]", "ErOo1EruC1M", 801, "WOMEN", art+'tmn.jpg', fanart),    
        ("[B]Battle Club Pro & Tier 1 Present: The One Who Knocks 2017[/B]", "3Mqzs6WMknE", 801, "MISC", art+'misc2.jpg', fanart),
        ("[B]Night Of The Legends: 8/5/1994[/B]", "8tRalabmsk0", 801, "MISC", art+'misc3.jpg', fanart),    
        ("[B]TMN Best of Kylie Rae in Ladies Night Out[/B]", "KLFqJmVGi94", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]River City Wrestling Event: September 8, 2017 in San Antonio, TX[/B]", "cKu_qih6bZI", 801, "MISC", art+'misc2.jpg', fanart),    
        ("[B]Phoenix Pro Wrestling: The Debut 11/14/14[/B]", "a0Ql8s0_-_Q", 801, "MISC", art+'misc3.jpg', fanart),    
        ("[B]Warriors of Wrestling presents 12 Year Anniversary[/B]", "vhAM4qtKzug", 801, "MISC", art+'warriors.jpg', fanart),    
        ("[B]W.O.W No-Limits #1 contender tournament 2/8/20[/B]", "_F2borkbwTw", 801, "MISC", art+'warriors.jpg', fanart),    
        ("[B]Warriors of Wrestling presents Frankie Getz Memorial show[/B]", "vZmyUgbdnv0", 801, "MISC", art+'warriors.jpg', fanart),    
        ("[B]SOUL 9: In The Air Tonight (One Year Anniversary Show)[/B]", "RQhjiFv8tTc", 801, "MISC", art+'misc2.jpg', fanart),    
        ("[B]Warriors of Wrestling presents Women of Warriors III 10/7/2017[/B]", "oAorg3rIHb8", 801, "WOMEN", art+'warriors.jpg', fanart),    
        ("[B]Bellatrix Female Warriors: Season 01 - Episode 01[/B]", "7z-QPwi7EcI", 801, "WAW, WOMEN", art+'waw.jpg', fanart),    
        ("[B]Bellatrix Female Warriors: Season 01 - Episode 02[/B]", "pHv2UQZwKkY", 801, "WAW, WOMEN", art+'waw.jpg', fanart),    
        ("[B]Bellatrix Female Warriors: Season 01 - Episode 03[/B]", "1MVZG2RhoWI", 801, "WAW, WOMEN", art+'waw.jpg', fanart),    
        ("[B]Bellatrix Female Warriors: Season 01 - Episode 04[/B]", "dW-cY5yifHc", 801, "WAW, WOMEN", art+'waw.jpg', fanart),    
        ("[B]Bellatrix Female Warriors: Season 01 - Episode 05[/B]", "zE0EW52hVjc", 801, "WAW, WOMEN", art+'waw.jpg', fanart),    
        ("[B]Bellatrix Female Warriors: Season 01 - Episode 06[/B]", "9qhBHfvWG8g", 801, "WAW, WOMEN", art+'waw.jpg', fanart),    
        ("[B]Bellatrix Female Warriors: Season 01 - Episode 07[/B]", "GxbGBUr4ALU", 801, "WAW, WOMEN", art+'waw.jpg', fanart),    
        ("[B]Straight Outta Bellatrix Academy 19/01/20[/B]", "o38Vx25QvmM", 801, "WOMEN", art+'waw.jpg', fanart),    
        ("[B]Straight Outta Bellatrix Academy 16/02/20[/B]", "JUsumZI3aig", 801, "WOMEN", art+'waw.jpg', fanart),    
        ("[B]Warriors of Wrestling presents Brooklyn Beatdown 3/6/20[/B]", "8BSK7m0m7EU", 801, "MISC", art+'warriors.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 6/05/20[/B]", "83gPNXODlzM", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 6/04/20[/B]", "7ymqVPl-G6Q", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]3-2-1 BATTLE! Close Encounters Of The Furred Kind 2020[/B]", "WRjjRbMnfes", 801, "MISC", art+'321.jpg', fanart),
        ("[B]3-2-1 BATTLE! Finding Emo 2020[/B]", "acfkm-dKzFU", 801, "MISC", art+'321.jpg', fanart),
        ("[B]3-2-1 BATTLE! The Notebooking 2020[/B]", "mC9JfG6Tse0", 801, "MISC", art+'321.jpg', fanart),
        ("[B]3-2-1 BATTLE! Battle Rumble 2020[/B]", "YnHcRDMtmLE", 801, "MISC", art+'321.jpg', fanart),
        ("[B]3-2-1 BATTLE! Finding Emo 2020[/B]", "acfkm-dKzFU", 801, "MISC", art+'321.jpg', fanart),
        ("[B]3-2-1 BATTLE! Battle of the Sexes 2019[/B]", "TEOu7occkJE", 801, "MISC", art+'321.jpg', fanart),
        ("[B]GNW Lady Yasmine: 17 Matches 2020[/B]", "rMDG0aFq37Y", 801, "WOMEN", art+'misc2.jpg', fanart),    
        ("[B]RCW Re-Animated XV 2020[/B]", "-jTEROS-AjU", 801, "MISC, RCW", art+'riot.jpg', fanart),   
        ("[B]GWF Courage: Episode VI 2016[/B]", "OnEtG1tjNfY", 801, "MISC", art+'gwf.jpg', fanart),
        ("[B]GWF Courage: Episode V 2016[/B]", "l0vc6q-FuDA", 801, "MISC", art+'gwf.jpg', fanart),
        ("[B]GWF Courage: Episode IV 2016[/B]", "gU4q-rJMqW4", 801, "MISC", art+'gwf.jpg', fanart),
        ("[B]GWF Courage: Episode III 2016[/B]", "gN_7QhVtoZU", 801, "MISC", art+'gwf.jpg', fanart),
        ("[B]GWF Courage: Episode II 2016[/B]", "9Drp-IoA-qM", 801, "MISC", art+'gwf.jpg', fanart),
        ("[B]GWF Courage: Episode I 2016[/B]", "HjOUtmtHYO4", 801, "MISC", art+'gwf.jpg', fanart),
        ("[B]RCW Glutton For Punishment 2020[/B]", "6XPVpf3B6D4", 801, "MISC", art+'riot.jpg', fanart),   
        ("[B]The Smokeshow: Australian 2019[/B]", "8RcTM9NEnok", 801, "MISC", art+'misc2.jpg', fanart),
        ("[B]RoE WrestleClash XX 2019[/B]", "JhV9K8PigXU", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]OTT Wrestling: Presents National Showcase[/B]", "3bBQ9F0C00I", 801, "MISC", art+'ott.jpg', fanart),
        ("[B]OTT Wrestling: Presents Gems From The Tivoli p2[/B]", "AyglhZhoGqI", 801, "MISC", art+'ott.jpg', fanart),
        ("[B]OTT Wrestling: Presents Gems From The Tivoli p1[/B]", "-nsdGeHBCio", 801, "MISC", art+'ott.jpg', fanart),
        ("[B]Club WWN Greatest Hit #9[/B]", "IR8QnPCXm-I", 801, "MISC", art+'wwn.jpg', fanart),
        ("[B]TMN Womens Wrestling: 5/28/20[/B]", "M9h9XGV51o4", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 5/20/20[/B]", "wiK_mGxNcWE", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 5/19/20[/B]", "h1t-aF8mnrk", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Wrestling Event: 5/3/20[/B]", "RWoUm_gHO6g", 801, "TMN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 4/25/20[/B]", "QoONxwDI8EU", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 4/16/20[/B]", "0D54gA6-XrQ", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 3/29/20[/B]", "KpOZyP7DWYY", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 3/26/20[/B]", "h6uR7gocY0I", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Battle Club Pro Wrestling: 3/18/20[/B]", "0BdKl2J-wGY", 801, "TMN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: Best of Barbi Hayden 3/17/20[/B]", "vJPCbC86W0I", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 3/14/20[/B]", "wS3uLkGpplg", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]TMN Womens Wrestling: 3/13/20[/B]", "iLyIzMp3w1Y", 801, "TMN, WOMEN", art+'tmn.jpg', fanart),    
        ("[B]All Ladies Pro Wrestling - Jan. 24th, 2015[/B]", "pWcxOq_xwcU", 801, "WOMEN", art+'misc2.jpg', fanart),    
        ("[B]Club WWN Greatest Hit #8[/B]", "mEF_H10TVdk", 801, "MISC", art+'wwn.jpg', fanart),
        ("[B]Club WWN Greatest Hit #7[/B]", "Mhq963O9qvc", 801, "MISC", art+'wwn.jpg', fanart),
        ("[B]Club WWN Greatest Hit #6[/B]", "8Z50H3WMRiI", 801, "MISC", art+'wwn.jpg', fanart),
        ("[B]Club WWN Greatest Hit #5[/B]", "OLlzKPfcGn4", 801, "MISC", art+'wwn.jpg', fanart),
        ("[B]Club WWN Greatest Hit #4[/B]", "aOETxpohMm0", 801, "MISC", art+'wwn.jpg', fanart),
        ("[B]Club WWN Greatest Hit #3[/B]", "jkmxNok_yfE", 801, "MISC", art+'wwn.jpg', fanart),
        ("[B]Trinity Brawl II 2019[/B]", "Pmjj1APRSPs", 801, "MISC", art+'misc2.jpg', fanart),
        ("[B]Fight Factory Pro Wrestling IX 2020[/B]", "UjqAtrGZvVc", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]DOA Pro Wrestling: Burning Bridges 2019[/B]", "iG2fGyzhpDI", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]DNA Wrestling: Its in Our Blood II 2020[/B]", "bo3zt9gDYOg", 801, "MISC", art+'dna.jpg', fanart),
        ("[B]Respect Womens Wrestling: Volumn VI 2019[/B]", "Qg-zmS8BSvY", 801, "WOMEN", art+'respect.jpg', fanart),    
        ("[B]NWA Crocket Cup 2019[/B]", "bPtXBGYXAlQ", 801, "NWA, MISC", art+'nwa.jpg', fanart),
        ("[B]OCW One Night Special Womens Championship 2020[/B]", "-0Fu_yCU2jA", 801, "WOMEN", art+'misc2.jpg', fanart),    
        ("[B]3-2-1 Battle! Gone With The Weird 2019[/B]", "QneGXuEaoq0", 801, "MISC", art+'321.jpg', fanart),    
        ("[B]LPWA Wrestling - Prime Time 2012[/B]", "fBzEZNMptzA", 801, "WOMEN", art+'lpwa.jpg', fanart),    
        ("[B]3-2-1 Battle! Rebel Girls 2019[/B]", "mtrdrLWL4V0", 801, "WOMEN", art+'321.jpg', fanart),    
        ("[B]Gold Rush Pro: Lady Luck Tournment 2015[/B]", "4V4te3exehM", 801, "WOMEN, GOLD", art+'misc2.jpg', fanart),    
        ("[B]EVE Womens Wrestling: War Games 2020[/B]", "QEU96ldJdKM", 801, "WOMEN", art+'eve.jpg', fanart),    
        ("[B]EVE Womens Wrestling: War Games 2018[/B]", "ETBcUtaO7uY", 801, "WOMEN", art+'eve.jpg', fanart),    
        ("[B]STARDOM: No People Gate 3/8/20[/B]", "2uXoAZ2lEMA", 801, "WOMEN", art+'stardom.jpg', fanart), 
        ("[B]Tofu Pro Wrestling The Real WIP Queendom 2018[/B]", "ArLFl0_aQhg", 801, "WOMEN", art+'misc2.jpg', fanart), 
        ("[B]Britannia BWP Lockdown 2020[/B]", "0cYPLPO8eTM", 801, "BRIT", art+'brit.jpg', fanart),
        ("[B]IPW NOAH JR. Heavyweight Tournament 2019[/B]", "I3_zIB_KXwc", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW UK Extreme Measures 2006[/B]", "_js6LcC8byo", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW Live at Unit 9 IV 2018[/B]", "Lt81A6k-fnk", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW Live at Unit 9 V 2018[/B]", "JL3cG-UtPEg", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW Magnifient 7even 2018[/B]", "eJuNsJQV3eE", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW This is IPW 2018[/B]", "NtCzhFeykFM", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW Womens Showcase 2016[/B]", "xQLL3vN5Xuc", 801, "IPW, WOMEN", art+'ipw.jpg', fanart),   
        ("[B]IPW UK Supershow VIII 2017[/B]", "9uCsBD5D8Rk", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]FWA: Hotwired 2005[/B]", "3M7OTTonwWs", 801, "FWA", art+'fwa.jpg', fanart),
        ("[B]HOB Womens Championship 2018[/B]", "G3YkoRVdEX8", 801, "HOB, WOMEN", art+'hob.jpg', fanart),
        ("[B]HOB Tag Team Championship 2018[/B]", "BBxo6I1YDMo", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Heavyweight Championship 2018[/B]", "GMZdLrimRws", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Southern NE Championship 2018[/B]", "W2HBnu9SmeI", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]Discovery Wrestling November 2015[/B]", "Op-s_sT4s30", 801, "MISC", art+'discovery.jpg', fanart),   
        ("[B]Britannia Wrestling ScouseDown 2017[/B]", "qMtCtF1fCGs", 801, "BRIT", art+'brit.jpg', fanart),
        ("[B]Defiant Wrestling #10 2018[/B]", "7iDwFSewd-s", 801, "DEFIANT", art+'defiant.jpg', fanart),
        ("[B]Defiant Wrestling #9 2018[/B]", "KnBZeRzb-Yw", 801, "DEFIANT", art+'defiant.jpg', fanart),
        ("[B]Defiant Wrestling #8 2018[/B]", "asPRBPxkMiE", 801, "DEFIANT", art+'defiant.jpg', fanart),
        ("[B]Defiant Wrestling #7 2018[/B]", "sADkh5Uzptc", 801, "DEFIANT", art+'defiant.jpg', fanart),
        ("[B]Defiant Wrestling #6 2018[/B]", "x36AABa0usw", 801, "DEFIANT", art+'defiant.jpg', fanart),
        ("[B]CCW Wrestling Celtic Rumble 2016[/B]", "mz5Cim9j8xM", 801, "CCW", art+'ccw.jpg', fanart),
        ("[B]Ultimate Championship Wrestling August 27th 2016[/B]", "yoOjVEC0s4Y", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]Inspire Pro Wrestling Ecstasy of Gold 2014[/B]", "cbekomngnm8", 801, "MISC", art+'ipw.jpg', fanart),
        ("[B]Pro Wrestling Clash: Ignition 2018[/B]", "onPjcxP5iiY", 801, "MISC", art+'misc2.jpg', fanart),
        ("[B]UK Wrestling December Bash 09-12-17[/B]", "4yQnISVRugw", 801, "MISC", art+'ukw.jpg', fanart),
        ("[B]Discovery Wrestling March 2017[/B]", "5upguxLU2DE", 801, "MISC", art+'discovery.jpg', fanart),
        ("[B]Futureshock Wrestling 11th Anniversity 2016[/B]", "RMcJg9FkbKg", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]Revolt Pro Wrestling December 2018[/B]", "W2ZURBQo9Mg", 801, "MISC", art+'rpw.jpg', fanart),    
        ("[B]Defiant Wrestling #5 2018[/B]", "bi0pj0MuTmg", 801, "DEFIANT", art+'defiant.jpg', fanart),
        ("[B]Defiant Wrestling #4 2018[/B]", "kErVMN98R_c", 801, "DEFIANT", art+'defiant.jpg', fanart),
        ("[B]Defiant Wrestling #2 2017[/B]", "EnsHdnSRboE", 801, "DEFIANT", art+'defiant.jpg', fanart),
        ("[B]TNA Wrestling Christmas Episode 2007[/B]", "aaPQSr_fxe0", 801, "TNA", art+'impact.jpg', fanart),
        ("[B]TNA Impact Wrestling 7/25/2013[/B]", "gB3bA4C9gxo", 801, "TNA", art+'impact.jpg', fanart),
        ("[B]RoE March Madness 2019[/B]", "VVG8IXTKUvk", 801, "MISC", art+'misc2.jpg', fanart),
        ("[B]RoE WrestleClash XXI 2019[/B]", "prY5yRJQ71M", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]CCW Wrestling Revolution 2013[/B]", "ZiAsqHd6UTI", 801, "CCW", art+'ccw.jpg', fanart),
        ("[B]CCW Wrestling Revolution II 2015[/B]", "k9Abzo3ex5w", 801, "CCW", art+'ccw.jpg', fanart),
        ("[B]One Pro Wrestling: No Turning Back 1/06/06[/B]", "WtH1ik67IzI", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: A Cruel Twist Of Fate 10/01/05[/B]", "cc2h_g8L0RA", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: All or Nothing Night I 8/04/06[/B]", "9u9vDbJHpww", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: All or Nothing Night II 8/05/06[/B]", "sSpkHGWd9RM", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Know Your Enemy Night I 5/26/06[/B]", "D0QWkp7qFig", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Know Your Enemy Night II 5/27/06[/B]", "UcsmapHYtrc", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Fight Club 5/27/06[/B]", "hSohUzrD2Ns", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Fight Club II 5/27/06[/B]", "S-sc3af8rj0", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Fight Club III 10/14/06[/B]", "mIQ9S1GkXPg", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Fight Club IV 11/26/06[/B]", "ACA6PAImOxE", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: 1st Anniversary Show 10/14/06[/B]", "iEfdl0K-nM4", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Know Your Enemy Night I 6/30/07[/B]", "PL7QeUCfCzw", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Know Your Enemy Night II 7/01/07[/B]", "cXeOHB8sDqs", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Will Not Die 01/13/07[/B]", "nVgAUc8qqDE", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Devils Due 7/01/07[/B]", "9ZpbD4JNNf0", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Invincible 08/18/07[/B]", "5nWVUNoU7cQ", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: The Underground II 09/22/07[/B]", "ZVI0Y33zLA4", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: The Underground III 10/26/07[/B]", "EDFiIeOBJZA", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: The Underground IV 11/10/07[/B]", "xAG3iHxvyXM", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: 2nd Anniversary Show 10/13/07[/B]", "JsrY1aCLhKk", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: Fully Charged 3/16/08[/B]", "W7O3S8qSjls", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: 3rd Anniversary Show 10/08/08[/B]", "yDg0BzAmkMA", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]One Pro Wrestling: 4th Anniversary Show 11/15/09[/B]", "GhcJc-kbiYI", 801, "1PW", art+'1pw.jpg', fanart),
        ("[B]Welcome To The Proving Grounds Burlington 2019[/B]", "gbWk_ikTOHY", 801, "SMASH", art+'smash.jpg', fanart),
        ("[B]Smash Super Showdown VI 2018[/B]", "fRQrRd5NlME", 801, "SMASH", art+'smash.jpg', fanart),
        ("[B]GCW VS FIST COMBAT, WEST VS. EAST, 8/8/2019[/B]", "c1zz588vEso", 801, "MISC", art+'gcw.jpg', fanart),
        ("[B]Wrestle Rampage - Ground Zero 2019[/B]", "qwQpsUgy_ow", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]AWF Supershow Adelaide 2018[/B]", "hp2Q5poRYiY", 801, "MISC", art+'misc.jpg', fanart),
        ("[B]Wrestling League: Live in London 2019[/B]", "cP8gctTyri4", 801, "MISC", art+'misc2.jpg', fanart),   
        ("[B]Breed Pro: My childhood was small, but Im gonna be BIG 2019[/B]", "ATMZzf4qjdM", 801, "MISC, BREED", art+'breed.jpg', fanart),   
        ("[B]Breed Pro: Because Words Matter 2019[/B]", "JtWIPlQl5u4", 801, "MISC, BREED", art+'breed.jpg', fanart),   
        ("[B]Breed Pro Wrestling: Out Of The Box 2019[/B]", "kr1T74_JGEs", 801, "MISC, BREED", art+'breed.jpg', fanart),   
        ("[B]Breed Pro Wrestling: This House Is A Circus 2019[/B]", "yBbC8BFxNn4", 801, "MISC, BREED", art+'breed.jpg', fanart),   
        ("[B]Breed Pro Wrestling: Sunday Night YEET 2019[/B]", "ZDXH-bo50h4", 801, "MISC, BREED", art+'breed.jpg', fanart),   
        ("[B]Rev Pro: Its All Legal 2018[/B]", "Ufgncg8LZ_o", 801, "MISC", art+'rpw.jpg', fanart),
        ("[B]Pro Wrestling Darwin: Evolve or Dissolve 2019[/B]", "6QIu4oDJc7s", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]Pro Wrestling Darwin: Top End Hostility 2019[/B]", "iNjQlamToaM", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]DNA Wrestling: Project 4 2019[/B]", "sXPWn5dRNsM", 801, "MISC, DNA", art+'dna.jpg', fanart),
        ("[B]DNA Wrestling: Battle Zone 2019[/B]", "0xAwEJRvQOc", 801, "MISC, DNA", art+'dna.jpg', fanart),
        ("[B]DNA Wrestling: Go Big or Go Home 2019[/B]", "_dATw38e8as", 801, "MISC, DNA", art+'dna.jpg', fanart),
        ("[B]Chaotic Wrestling: Summer Chaos 2018[/B]", "i0q31q7FAUA", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]Battle Arts Rising Stars March 17, 2018[/B]", "qQ6rPsu9_bw", 801, "MISC", art+'misc2.jpg', fanart),
        ("[B]SENDAI GIRLS Niigata 10/18/14[/B]", "DMDA2sxiGgc", 801, "WOMEN", art+'iceribbon.jpg', fanart),
        ("[B]STARDOM: GODDESSES OF STARDOM 10/26/14[/B]", "CSsfpTZmTWk", 801, "WOMEN", art+'stardom.jpg', fanart), 
        ("[B]UWF-TNA Norfolk, VA 3/03/06[/B]", "7n3jeYAvTxg", 801, "TNA", art+'impact.jpg', fanart),   
        ("[B]UWF-TNA Fort Lee, VA 3/04/06[/B]", "dknia2CxJxM", 801, "TNA", art+'impact.jpg', fanart),   
        ("[B]UWF-TNA Danville, VA 3/31/06[/B]", "WhiB1iZkbvY", 801, "TNA", art+'impact.jpg', fanart),   
        ("[B]UWF-TNA Mooreville, NC 5/26/06[/B]", "J8SEO-WvRv0", 801, "TNA", art+'impact.jpg', fanart),   
        ("[B]UWF-TNA Greensboro, NC 5/27/06[/B]", "6f5LDgOh3Tc", 801, "TNA", art+'impact.jpg', fanart),   
        ("[B]UWF-TNA Harrisonburg, VA 2/10/06[/B]", "qNMh6zpTKUQ", 801, "TNA", art+'impact.jpg', fanart),   
        ("[B]UWF-TNA Hardcore War II[/B]", "wF0OvAPQxQI", 801, "TNA", art+'impact.jpg', fanart),   
        ("[B]International Pro Wrestling Magnificent 7even 2018[/B]", "eJuNsJQV3eE", 801, "MISC", art+'ipw.jpg', fanart),   
        ("[B]International Pro Wrestling This Is IPW 2018[/B]", "NtCzhFeykFM", 801, "MISC", art+'ipw.jpg', fanart),   
        ("[B]International Pro Wrestling Run The Gauntlet 2018[/B]", "JL3cG-UtPEg", 801, "MISC", art+'ipw.jpg', fanart),   
        ("[B]International Pro Wrestling #8 2019[/B]", "kYOnms8gWmU", 801, "MISC", art+'ipw.jpg', fanart),   
        ("[B]International Pro Wrestling #6 2019[/B]", "BsQ8AuTS3lo", 801, "MISC", art+'ipw.jpg', fanart),   
        ("[B]Beyond Wrestling: IWTV Caffeine 2019[/B]", "Sucin4_S3ec", 801, "MISC", art+'beyond.jpg', fanart),   
        ("[B]Mayhem Pro Wrestling #1 2019[/B]", "H3t8hj0Ov3o", 801, "MISC", art+'misc2.jpg', fanart),   
        ("[B]Breed Pro Wrestling Colossal Tussle 2019[/B]", "Mzcfyx6ctUU", 801, "MISC, BREED", art+'breed.jpg', fanart),   
        ("[B]Frontline Wrestling NEXTGEN #1 2019[/B]", "KiXl1rXEewU", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]Beauty In Combat 11/20/15[/B]", "wWu1jNofNUY", 801, "MISC", art+'misc2.jpg', fanart),   
        ("[B]Beauty In Combat 9/2/18[/B]", "7x1hoixjE5k", 801, "MISC", art+'misc2.jpg', fanart),   
        ("[B]Riptide Wrestling Black Water 2017[/B]", "BD6HBrvmZwY", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]ECW Wrestling (WWE) 2/9/10[/B]", "aOKu-AO_Mjo", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]ECW Wrestling (WWE) 11/17/09[/B]", "Nm-EXQEvjJo", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]ECW Wrestling (WWE) 10/20/09[/B]", "ZYpzaRoZqTE", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]Defy Wrestling Throwback 2019[/B]", "46Q95nbdIMM", 801, "MISC", art+'defy.jpg', fanart),   
        ("[B]Defy Wrestling Defy1 Legacy 2017[/B]", "N1r1gqTBDgs", 801, "MISC", art+'defy.jpg', fanart),   
        ("[B]Beyond Wrestling Americanrana 2018[/B]", "DPATu1NNTDY", 801, "MISC", art+'beyond.jpg', fanart),   
        ("[B]Beyond Wrestling TFT Night I 2018[/B]", "Y0xE1ghqIjQ", 801, "MISC", art+'beyond.jpg', fanart),   
        ("[B]Beyond Wrestling N NWA Smokey Mountain 2014[/B]", "dSf9qjTOR9A", 801, "MISC", art+'beyond.jpg', fanart),   
        ("[B]Heavy On Wrestling: Black Sunday 2018[/B]", "cbibPppE4ME", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]PWA Diegos Last Show ft Jimmy Havoc 2018[/B]", "e6Gb508hYMM", 801, "MISC", art+'misc.jpg', fanart),   
        ("[B]JCW Wrestling: St. Andrews Brawl 2011[/B]", "l7x4tVMMtQE", 801, "MISC", art+'misc2.jpg', fanart),   
        ("[B]Hope Wrestling: Hope N Glory 2016[/B]", "oV8UYYkb3F4", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]IWC Wrestling Sixteen 2019[/B]", "dLpaz9vxzhI", 801, "MISC", art+'misc2.jpg', fanart),   
        ("[B]ROH: Jay Lethal vs Matt Taven - 60 Minute Classic 2019[/B]", "-EuoGmfEls0", 801, "WWE, WOMEN", art+'roh.jpg', fanart),
        ("[B]WWE Superstars Thu, June 3, 2010[/B]", "3Sf58J0xrdk", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE NXT - June 13, 2012[/B]", "ijybO3A61Ws", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE NXT - October 26, 2010[/B]", "cAJnhzydPa0", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE NXT - November 2, 2010[/B]", "cgJoczGrBTU", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE NXT - February 22, 2012[/B]", "OVGxjC_qWuk", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE Superstars Thu, April 22, 2010[/B]", "BpxJJ8sl-qo", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE NXT - May 24, 2011[/B]", "AQ-q7_34PhI", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE Superstars - August 19, 2010[/B]", "lDVqyH6pbYk", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE Superstars: September 06, 2012[/B]", "m_EAsyWrLzo", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE NXT - February 22, 2011[/B]", "KiH6jbzMfVA", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE NXT - September 13, 2011[/B]", "_J1xnMLazYI", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE NXT - January 11, 2012[/B]", "HEWec3jp6Ns", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE Superstars - February 16, 2012[/B]", "RYZc1rjqBfw", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE NXT - October 26, 2011[/B]", "AdMoCMEV8xA", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]WWE Superstars Thu, May 27, 2010[/B]", "Yi4371jVc0E", 801, "WWE", art+'wwe.jpg', fanart),
        ("[B]ROH 60 Minute Match Taven VS Lethal 2019[/B]", "-EuoGmfEls0", 801, "ROH", art+'roh.jpg', fanart),
        ("[B]Progress Natural Progression T6 2019[/B]", "D-wt0WzHgTA", 801, "PROGRESS", art+'progress.jpg', fanart),
        ("[B]Progress x APC Catch 2019[/B]", "6BntNm_gsUU", 801, "PROGRESS", art+'progress.jpg', fanart),
        ("[B]Progress Chapter 76 2018[/B]", "25W3JISrSY4", 801, "PROGRESS", art+'progress.jpg', fanart),  
        ("[B]Progress Chapter 55 2018[/B]", "aEHsTXH4azY", 801, "PROGRESS", art+'progress.jpg', fanart),   
        ("[B]Progress Chapter 36 2016[/B]", "l-iAhlPte3o", 801, "PROGRESS", art+'progress.jpg', fanart),  
        ("[B]Progress Chapter 13 2014[/B]", "it2coTptmlM", 801, "PROGRESS", art+'progress.jpg', fanart),  
        ("[B]Progress ENDVR:7 2014[/B]", "vo5OHAqd9uc", 801, "PROGRESS", art+'progress.jpg', fanart),   
        ("[B]Mid-West Entertainment Wrestling 2017[/B]", "Bf9Igsn5mxg", 801, "MISC", art+'misc2.jpg', fanart),   
        ("[B]MLW Fury Road 2019[/B]", "mAC2-aWe-s8", 801, "MLW", art+'mlw.jpg', fanart),
        ("[B]MLW Kings of Colosseum 2019[/B]", "KK8i9WC4KP8", 801, "MLW", art+'mlw.jpg', fanart),  
        ("[B]MLW Battle Riot 2019[/B]", "k1j8A8GxvCw", 801, "MLW", art+'mlw.jpg', fanart),   
        ("[B]MLW War Chamber 2019[/B]", "opaBZaH4Wyc", 801, "MLW", art+'mlw.jpg', fanart), 
        ("[B]MLW Superfight 2019[/B]", "4QQaqJbZoxk", 801, "MLW", art+'mlw.jpg', fanart),   
        ("[B]MLW Never Say Never 2017[/B]", "cHvgV4HhVuU", 801, "MLW", art+'mlw.jpg', fanart),   
        ("[B]Unlimited Wrestling Icebreaker 2019[/B]", "dqyaVWQIiGQ", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]Unlimited Wrestling New Dawn 2020[/B]", "MqAdh8ufrkY", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]Defiant Wrestling Built to Destroy 2019[/B]", "y6R2bJqsEh8", 801, "DEFIANT", art+'defiant.jpg', fanart),  
        ("[B]WCPW Wrestling: Exit Wounds 2017[/B]", "jTeoxnDjQek", 801, "DEFIANT", art+'defiant.jpg', fanart),   
        ("[B]WCPW Wrestling: Fight Back 2017[/B]", "MumdQnkd4bE", 801, "DEFIANT", art+'defiant.jpg', fanart),   
        ("[B]WCPW Loaded: The Penultimate Episode 2017[/B]", "8Pa-nPhJewk", 801, "DEFIANT", art+'defiant.jpg', fanart),   
        ("[B]Pro Wrestling World Cup Qualifier 2017[/B]", "eLx6lyDMG24", 801, "DEFIANT", art+'defiant.jpg', fanart),   
        ("[B]Pro Wrestling World Cup Finals 2017[/B]", "WwQtY5xm4v0", 801, "DEFIANT", art+'defiant.jpg', fanart),   
        ("[B]AAW Pro Wrestling: Destination Milwaukee 2019[/B]", "zLxiR6oSbJg", 801, "AAW", art+'aaw.jpg', fanart),   
        ("[B]AAW Pro Wrestling: Defining Moment 2017[/B]", "JGqoN0kE4y0", 801, "AAW", art+'aaw.jpg', fanart),   
        ("[B]AAW Pro Wrestling: Epic 2017[/B]", "zLxiR6oSbJg", 801, "AAW", art+'aaw.jpg', fanart),   
        ("[B]AAW Pro Wrestling: Never Say Die 2016[/B]", "FbYDzIULDts", 801, "AAW", art+'aaw.jpg', fanart),  
        ("[B]AAW Pro Wrestling: Windy City Classic XI 2015[/B]", "ZNzp9PaOquU", 801, "AAW", art+'aaw.jpg', fanart),   
        ("[B]AAW Pro Wrestling: Hell Hath No Fury 2015[/B]", "2-9JbenT6Ow", 801, "AAW", art+'aaw.jpg', fanart),   
        ("[B]AAW Pro Wrestling: Day of Defiance 2013[/B]", "1zNqNkcUWLQ", 801, "AAW", art+'aaw.jpg', fanart),   
        ("[B]AAW Pro Wrestling: Point of No Return 2012[/B]", "6qXOu9XzDrA", 801, "AAW", art+'aaw.jpg', fanart),   
        ("[B]Legendary Action Wrestling: Legendary 2019[/B]", "bD0nn83dTAw", 801, "MISC", art+'misc2.jpg', fanart),    
        ("[B]ACE: Crossroads XIII 2017[/B]", "vdHyrhfFh9o", 801, "MISC", art+'misc.jpg', fanart),   
        ("[B]PAPW: Never Give Up 2018[/B]", "E054zFaKkDE", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]PAPW: The Beginning 2018[/B]", "VUWHqgjsH6s", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]PAPW: Thrill-o at Melillo 2018[/B]", "lMIa88SrO3U", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]WrestlePro Brooklyn 2018[/B]", "mB9h8QAIDLg", 801, "MISC", art+'misc2.jpg', fanart),
        ("[B]WrestlePro Brace For Impact 2018[/B]", "4tGRsh7mJx0", 801, "MISC", art+'misc2.jpg', fanart),
        ("[B]SPRY Wrestling Setting the Pace 2008[/B]", "T1h8gPzCCPM", 801, "MISC", art+'misc.jpg', fanart),
        ("[B]RCW Battle For Supremacy 2019[/B]", "x8NoB-Nrl_Q", 801, "MISC", art+'riot.jpg', fanart),   
        ("[B]RCW Rites of Passage 2011[/B]", "MbRLSh4tJog", 801, "MISC", art+'riot.jpg', fanart),   
        ("[B]Wrestling For A Cause (National Leiomyosarcoma Foundation) 2019[/B]", "vNKYnPxJ0co", 801, "MISC", art+'misc2.jpg', fanart),   
        ("[B]Go Pro Wrestling Go Big or Go Home 2019[/B]", "bOnaO_42_oA", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]Hurricane Pro Wrestling 2019[/B]", "dRyt2wsuas4", 801, "MISC", art+'misc2.jpg', fanart),   
        ("[B]Hurricane Pro Wrestling (Intergender)[/B]", "jgPUILMwhyw", 801, "WOMEN, MISC", art+'misc2.jpg', fanart),   
        ("[B]GNW Wrestling in Pembroke 2018[/B]", "OqvPEL3QTIM", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]Discovery Wrestling Year III 2018[/B]", "xuj1p50lHac", 801, "MISC", art+'discovery.jpg', fanart),   
        ("[B]UK Wrestling December Bash 2017[/B]", "4yQnISVRugw", 801, "MISC", art+'ukw.jpg', fanart),   
        ("[B]Lone Star Championship Wrestling 2015[/B]", "BMrSEMu1V-4", 801, "MISC", art+'misc.jpg', fanart),   
        ("[B]Midget Wrestling Warriors Game Over 2020[/B]", "wF3XtyRqAHc", 801, "MIDGET, MISC", art+'midget.jpg', fanart),   
        ("[B]Ironfist Wrestling: Supremacy 2020[/B]", "DUoIOWdxUIw", 801, "MISC", art+'misc2.jpg', fanart),   
        ("[B]Courage Pro: Lifts, Locks, N Leg Drops 2020[/B]", "BqUyn6IfVps", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]Courage Pro: Hamilton Heritage Rumble 2019[/B]", "jwUUhXfSl4A", 801, "MISC", art+'misc3.jpg', fanart),   
        ("[B]Women of Warriors Championship Lineage[/B]", "fevCBuelhlI", 801, "WOMEN", art+'warriors.jpg', fanart),
        ("[B]Women of Warriors Wrestling VII 2019[/B]", "2tOgTpc9Wks", 801, "WOMEN", art+'warriors.jpg', fanart),
        ("[B]Women of Warriors Wrestling Debut 2017[/B]", "PaLz_moU-2w", 801, "WOMEN", art+'warriors.jpg', fanart),
        ("[B]TMN Womens Wrestling Streamed 4/25/20[/B]", "QoONxwDI8EU", 801, "WOMEN", art+'tmn.jpg', fanart),
        ("[B]Wrestling Go - You Go Girls II 2019[/B]", "cpEdu9UGFDI", 801, "WOMEN", art+'tmn.jpg', fanart),
        ("[B]Womens Wrestling Queen of the North II[/B]", "yEvKyx0u4Uc", 801, "WOMEN", art+'tmn.jpg', fanart),
        ("[B]WOW Womens Wrestling 2001[/B]", "lTptnyvJYZA", 801, "WOMEN", art+'wow.jpg', fanart),
        ("[B]Warriors Of Wrestling (Intergender) 2019[/B]", "yfsB4A9eLUM", 801, "WOMEN", art+'warriors.jpg', fanart),
        ("[B]Sparkle Ladies Wrestling 2017[/B]", "CayVlnhwAz0", 801, "WOMEN", art+'tmn.jpg', fanart),
        ("[B]LPWA Womens Wrestling Best Of Vol II 2013[/B]", "e1pjDBnJOM4", 801, "WOMEN", art+'lpwa.jpg', fanart),
        ("[B]LPWA Womens Wrestling Prime Time 2012[/B]", "fBzEZNMptzA", 801, "WOMEN", art+'lpwa.jpg', fanart),
        ("[B]3-2-1 Battle Rebel Girls 2019[/B]", "mtrdrLWL4V0", 801, "WOMEN", art+'tmn.jpg', fanart),
        ("[B]EVE Womens Wrestling: #SHE-1[/B]", "g2WXlT6Nswk", 801, "WOMEN", art+'eve.jpg', fanart),    
        ("[B]Ladies Night Out IX Matinee[/B]", "0D54gA6-XrQ", 801, "WOMEN", art+'row.jpg', fanart),    
        ("[B]Ladies Night Out IX[/B]", "DGfBACSUMus", 801, "WOMEN", art+'row.jpg', fanart),    
        ("[B]Ladies Night Out VIII[/B]", "p91fSCxdLWU", 801, "WOMEN", art+'row.jpg', fanart),    
        ("[B]Ladies Night Out VII[/B]", "up_Pmw0s9XI", 801, "WOMEN", art+'row.jpg', fanart),    
        ("[B]Ladies Night Out VI[/B]", "CLFZJAlZRvI", 801, "WOMEN", art+'row.jpg', fanart),    
        ("[B]Queens of the Ring 4/3/20[/B]", "jgPUILMwhyw", 801, "WOMEN", art+'tmn.jpg', fanart),   
        ("[B]Queens of the Ring 9/13/19[/B]", "0LOqsYd0lkA", 801, "WOMEN", art+'tmn.jpg', fanart),   
        ("[B]Queens of the Ring II 1/18/2020[/B]", "5F3chfqR-20", 801, "WOMEN", art+'tmn.jpg', fanart),   
        ("[B]Womens Pro Wrestling 2019[/B]", "6YIeJ_YhyWM", 801, "WOMEN", art+'tmn.jpg', fanart),
        ("[B]JCPW Girls Night Out 2017[/B]", "ZosrFju3rUg", 801, "WOMEN", art+'iceribbon.jpg', fanart),
        ("[B]Glam! #1 Womens Wrestling 2019[/B]", "F6eic6l0Ecg", 801, "WOMEN", art+'glam.jpg', fanart),
        ("[B]Glam! #2 Womens Wrestling 2019[/B]", "eR3NtzztznE", 801, "WOMEN", art+'glam.jpg', fanart),   
        ("[B]Glam! #3 Womens Wrestling 2019[/B]", "i85cc-qK_G4", 801, "WOMEN", art+'glam.jpg', fanart),   
        ("[B]Bronx Wrestling Federation A Bronx Tale 2020[/B]", "zO3oQUBpw3c", 801, "BRONX", art+'bwf.jpg', fanart),
        ("[B]Bronx Wrestling Federation Once Upon A Time 2020[/B]", "lGw51Z4IgGQ", 801, "BRONX", art+'bwf.jpg', fanart),   
        ("[B]Bronx Wrestling Federation 100 Event[/B]", "MyrDqsfsKPc", 801, "BRONX", art+'bwf.jpg', fanart),   
        ("[B]Bronx Wrestling Federation A New Hope 2019[/B]", "v2RBg60Jr6Y;", 801, "BRONX", art+'bwf.jpg', fanart),   
        ("[B]Bronx Wrestling Federation Welcome to Terrodome 2019[/B]", "1FlnWwOYZFk", 801, "BRONX", art+'bwf.jpg', fanart),   
        ("[B]Bronx Wrestling Federation 9th Anniversity 2019[/B]", "hFr3qsnOHgk", 801, "BRONX", art+'bwf.jpg', fanart),   
        ("[B]Bronx Wrestling Federation Escape From NY 2019[/B]", "Hin7X2ZjQdM", 801, "BRONX", art+'bwf.jpg', fanart),   
        ("[B]Empire Wrestling Federation 9/06/19[/B]", "j1ITeTRuqfo", 801, "EMPIRE", art+'ewf.jpg', fanart),   
        ("[B]Empire Wrestling Federation 8/02/19[/B]", "XCqiSN7phaY", 801, "EMPIRE", art+'ewf.jpg', fanart),   
        ("[B]Empire Wrestling Federation 7/05/19[/B]", "fR5Jhwi6kWQ", 801, "EMPIRE", art+'ewf.jpg', fanart),   
        ("[B]Empire Wrestling Federation 6/14/19[/B]", "TEvJ48paQI4", 801, "EMPIRE", art+'ewf.jpg', fanart),   
        ("[B]Empire Wrestling Federation 6/07/19[/B]", "8miDQZl0pU4", 801, "EMPIRE", art+'ewf.jpg', fanart),   
        ("[B]Empire Wrestling Federation 5/03/19[/B]", "4kioE7sVuEo", 801, "EMPIRE", art+'ewf.jpg', fanart),   
        ("[B]Empire Wrestling Federation 3/01/19[/B]", "0zyCKvOFMJs", 801, "EMPIRE", art+'ewf.jpg', fanart),   
        ("[B]Empire Wrestling Federation 2/16/19[/B]", "OdfbSLgfYDc", 801, "EMPIRE", art+'ewf.jpg', fanart),   
        ("[B]Empire Wrestling Federation 1/12/19[/B]", "HlBlViR6eWw", 801, "EMPIRE", art+'ewf.jpg', fanart),   
        ("[B]Empire Wrestling Federation 12/17/18[/B]", "3g8G5PvlLsA", 801, "EMPIRE", art+'ewf.jpg', fanart),   
        ("[B]IPW Retaliation 2017[/B]", "s63lMqyv5W8", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW 2 Hott 2 Handle 2017[/B]", "lAA4fIlyLqk", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW WrestleRave XI 2017[/B]", "WQa5QT2oJ3M", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW The Memorial Show 2017[/B]", "1k6mQLEwRi4", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW Proving Grounds 2017[/B]", "onGAJJl3cn8", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW Threshold 2017[/B]", "_FzF4E4Cp1s", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW Seasons Bleedings 2016[/B]", "Y3NasOcbwoI", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW Chaos Theory 2016[/B]", "xcPrJZn-6yY", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW Backdrop 2016[/B]", "VWuN3wQf2tE", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW Ringside Rush 2016[/B]", "00mybaLICgU", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]IPW End of Days 2016[/B]", "OoIClFPYEdM", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]Spokane Anarchy WrestleRave X 2016[/B]", "idNhezE6Gpc", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]Spokane Anarchy Final Encounter 2016[/B]", "77maTUDsVK0", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]Spokane Anarchy Memorial Show 2016[/B]", "lm-AXMl-xRI", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]Spokane Anarchy Proving Grounds 2016[/B]", "3IIU_edQGAU", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]Spokane Anarchy War of Washington 2 2016[/B]", "BvC9k9k-Wdo", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]Spokane Anarchy Redemption 2016[/B]", "m1uqtxsO8EU", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]Spokane Anarchy Threshold 2016[/B]", "ypjgBBTaOvM", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]Spokane Anarchy Seasons Bleedings 2015[/B]", "ftOAVXknSYE", 801, "IPW", art+'ipw.jpg', fanart),   
        ("[B]Cascade Championship Wrestling Christmas 2019[/B]", "h2p-ye-ZCaU", 801, "CCW", art+'ccw.jpg', fanart),   
        ("[B]Cascade Championship Wrestling Classic 3 2019[/B]", "2XYbU44zoeE", 801, "CCW", art+'ccw.jpg', fanart),   
        ("[B]Cascade Championship Wrestling Merica 2019[/B]", "foOHRAuOfOY", 801, "CCW", art+'ccw.jpg', fanart),   
        ("[B]Cascade Wrestling Queen of the Ring 2019[/B]", "0LOqsYd0lkA", 801, "CCW", art+'ccw.jpg', fanart),   
        ("[B]Cascade Championship Wrestling Forever 2019[/B]", "ueMCF5Wcl40", 801, "CCW", art+'ccw.jpg', fanart),   
        ("[B]Alpha-1 Wrestling The Purge 2016[/B]", "hUEwJnVCFzI", 801, "MISC", art+'alpha1.jpg', fanart),   
        ("[B]Alpha-1 Wrestling Final Act 2016[/B]", "pU3erw2Mmls", 801, "MISC", art+'alpha1.jpg', fanart),   
        ("[B]Alpha-1 Wrestling Intoxicated 2013[/B]", "0Y3pLvf5jnA", 801, "MISC", art+'alpha1.jpg', fanart),   
        ("[B]Revolt Pro Wrestling Rise Up 2018[/B]", "Qv5DHgPJVO0", 801, "MISC", art+'rpw.jpg', fanart),    
        ("[B]Revolt Pro Wrestling 2018[/B]", "W2ZURBQo9Mg", 801, "MISC", art+'rpw.jpg', fanart),   
        ("[B]Revolt Pro Wrestling Next Chapter 2019[/B]", "vVmYMQmvvdo", 801, "MISC", art+'rpw.jpg', fanart),   
        ("[B]Reactivate Professional Wrestling Recharged 2020[/B]", "QQkGipG7edc", 801, "MISC", art+'episodes.jpg', fanart),   
        ("[B]WWA Hysteria 103 The Reunion 2020[/B]", "kmxcsHMgDwA", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 102 The War 2020[/B]", "EZ90mJ8kdgU", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 101 Reloaded 2018[/B]", "kQOc16lGM7g", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 100 Curtain Call 2019[/B]", "LNC7umlG-5k", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 99 November Reign 2019[/B]", "8Yul1DVGFQs", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 98 Halloween Hell 2019[/B]", "LLBfGp6BSYA", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 97 One Night Only 2019[/B]", "vrnJjgzGsmM", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 96 Two Hundred 2019[/B]", "tvR6MBkciyI", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 95 Showdown 2019[/B]", "nujFQub3ufQ", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 94 Danger At The Door 2019[/B]", "OQOwniGuS_M", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 93 Grave Consequences 2019[/B]", "Hnr_pl_XxUw", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 92 Last Man Standing 2019[/B]", "xOjFSwsw5iU", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 91 Wont Be Back 2019[/B]", "XVnyYWbBl0Y", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 90 We Are Now 2019[/B]", "DeI3L5Qokoo", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 89 Back To The Extreme 2019[/B]", "_-kKWYs-tSg", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 88 All Bad Things 2019[/B]", "Vd1kAr7Kgfg", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 87 Fandemonium 2019[/B]", "QVQ2KSN4xLM", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 86 First Blood 2019[/B]", "m2VKdJxOg2k", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 85 War Games 2019[/B]", "lebNXCAZddU", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 84 The War Part 2 2019[/B]", "vlfqCIEngck", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 83 The War Part 1 2019[/B]", "z29X2DeHz5Y", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 82 Mad World 2019[/B]", "3oj3xcyWpzY", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 81 Lawless 2019[/B]", "Bp59cV7nP4Q", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 80 Night of the Misfits 2019[/B]", "EenqzQXeYfo", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 79 Curtain Call 2019[/B]", "WvdrGmya28c", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 78 High Risk 2019[/B]", "Db6_E48QUuo", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 77 November Reign 2018[/B]", "2l9wnyYoy88", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 76 Halloween Hell 2018[/B]", "1jpbqob8G-c", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 75 Brace For Impact 2018[/B]", "a7rLBGAcAwk", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 74 Deception 2018[/B]", "QYeXhGKvU6s", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 73 One Night Only 2018[/B]", "KloW2wTj8Ng", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 72 Showdown 2018[/B]", "uXwbos7TMi4", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 71 Grave Consequences 2018[/B]", "RFbb87i_V-s", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 70 Independence Day 2018[/B]", "lptRXdQ00XY", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 69 Final Countdown 2018[/B]", "irdGpmtJ_Qg", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 68 Wont Back Down 2018[/B]", "8iDVGbZugGE", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 67 One Fifty 2018[/B]", "ZdU76DfSkyw", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 66 To The Extreme 2018[/B]", "cgDuFxd4cQE", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 65 Relentless 2018[/B]", "r6ng7Bz7ji4", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA vs. UCW: When Worlds Collide 2018[/B]", "yaTJy20MDA8", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 64 Fandemonium 2018[/B]", "-w8L9DkNBYM", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 63 Rock N Roll Forever 2018[/B]", "8AenSLiHUq8", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 62 The War 2018[/B]", "GBo3K3kCBIc", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 61 Madtown Madness 2018[/B]", "45sJG9JIHzg", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 60 Return To Evansville 2018[/B]", "MrVHTNgLus8", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 59 Ultimate X 2018[/B]", "EPznDAI-wy4", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 58 Relapse 2018[/B]", "NepbxJxgB3k", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 57 Season 3 Premiere 2018[/B]", "a5lQbuKUFW4", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 56 Curtain Call 2018[/B]", "USAO2bs93eg", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 55 High Risk 2018[/B]", "7iYADgeHjRE", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 54 End Game 2017[/B]", "C9RZRp110L4", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 53 November Reign 2017[/B]", "8WMZFXJOboU", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 52 Halloween Hell 2017[/B]", "1nA8SboqPcA", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 51 Battle Lines 2017[/B]", "S-fnkNrlnJU", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 50 Kentucky Classic 2017[/B]", "iM6agFpXbp8", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 49 Deception 2017[/B]", "Vz0kXs1XL40", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 48 Showdown 2017[/B]", "5pYjR6Wc2BU", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 47 Independence Day 2017[/B]", "YWxSMh4sAPw", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 46 Final Countdown 2017[/B]", "O0lhbDe_rJw", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 45 Hardwired to Self-Destruct 2017[/B]", "S6J2s6NSY_0", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 44 System Rulez 2017[/B]", "xY-rwNzJNwI", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 43 War Games 2017[/B]", "Dro20R7jZiI", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 42 Collision Course 2017[/B]", "cmhJBYdDvGA", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 41 Relentless 2017[/B]", "LuvfdFryfgg", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 40 Fandemonium 2017[/B]", "8gftLjeYOaM", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 39 Wrestle Roulette 2017[/B]", "Oju2mF7mdzY", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 38 Z3ro Hour 2017[/B]", "szgvkFitHsg", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 37 The War 2017[/B]", "uym8iNg9Q0o", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 36 Ultimate X 2017[/B]", "Fic6xZROJnA", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 35 Disarray Hell 2017[/B]", "2n5YaqSonV4", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 34 Relapse 2017[/B]", "HR0gB_XLI7I", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 33 Season 2 Debut 2017[/B]", "ODPOoCK65hI", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 32 Curtain Call 2017[/B]", "lEgwm_dvoNQ", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 31 New Divide 2017[/B]", "uTNxalCuVXc", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 30 Revolution 2017[/B]", "nvq8NrSAk1E", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 29 One Hundred 2016[/B]", "eiHyMrgU5eo", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 28 Boundless 2016[/B]", "V52ZTHpmECc", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 27 November Reign 2016[/B]", "CyfmUp8pJag", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 26 Halloween Hell 2016[/B]", "BQMBbfNTAYc", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA One Night Only 2016[/B]", "zRQOdchbtLI", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 25 Kentucky Classic Stage 2 2016[/B]", "YjiI-3kaG-A", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 24 Kentucky Classic Stage 1 2016[/B]", "g1jVjkYcJbg", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 23 Battle Lines 2016[/B]", "2Tqr1ohpS2o", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 22 High Risk 2016[/B]", "fB1vT4mS-gU", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 21 Deception 2016[/B]", "bvAsHOWFuNA", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 20 Relentless 2016[/B]", "W1l82n8vpQ8", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 19 Showdown 2016[/B]", "GHB76N6xDOs", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 18 Endgame 2016[/B]", "vjSsAUmdkzw", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 17 Independence Day 2016[/B]", "OH9wiIjDT2A", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 16 Final Countdown 2016[/B]", "8wzUT8PdSBU", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 15 Street Fight 2016[/B]", "QW5ope1Y_7o", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 14 Pick Your Poison 2016[/B]", "QNG-fA0IHHM", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 13 TLC 2016[/B]", "uyy7ddHGjUU", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 12 Collision Course 2016[/B]", "j_LwlQ8FHzI", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 11 Monsters Ball 2016[/B]", "H2iVSdf1rSg", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 10 Ultimate X 2016[/B]", "VUSpsaFI7vI", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 09 The Next Level 2016[/B]", "klxAQJ_Ws8o", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 08 Fandemonium 2016[/B]", "eEYD3JwYHdM", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 07 Fatal Four Way 2016[/B]", "zo1-yNRorf0", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 06 Last Man Standing 2016[/B]", "bC2GMhG3Rug", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 05 Wrestle Roulette 2016[/B]", "bQ78SqvClFQ", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 04 The War 2016[/B]", "SxPnpnv72iw", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]WWA Hysteria 01 The Beginning 2016[/B]", "9F3CMnU4FYM", 801, "WWA", art+'wwa.jpg', fanart),
        ("[B]GWF Light Heavyweight Tournament 2020[/B]", "XxXq5kl8sq0", 801, "MISC", art+'gwf.jpg', fanart),
        ("[B]GWF Chaos City Berlin 2019[/B]", "SbgbQ2SF3MY", 801, "MISC", art+'gwf.jpg', fanart),
        ("[B]GWF Womens Wrestling Revolution X[/B]", "itlSjG-aFyM", 801, "WOMEN", art+'gwf.jpg', fanart),
        ("[B]GWF Mystery Mayhem 2017[/B]", "__TjSllCLx4", 801, "MISC", art+'gwf.jpg', fanart),
        ("[B]GWF Womens Wrestling Revolution 2016[/B]", "B8qn5OnxrEE", 801, "WOMEN", art+'gwf.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling Lockdown Special 2020[/B]", "e2oyri0p1AY", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling Rumble 2019[/B]", "duhlQwQoGTw", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling Summersesh 2019[/B]", "4i5tEecC6rk", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling ASCENT Tournament Day 2 2019[/B]", "8jd-dz4Migs", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling ASCENT Tournament Day 1 2019[/B]", "bIKE6FZo5q4", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling Welcome to Paradise 2019[/B]", "sGF9MF8mRE4", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling Games of Death 2019[/B]", "hZ4-seV89yg", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling Extreme Rumble 2019[/B]", "lhDTle3TPn0", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling Big Fn Joes Xmas Bash 2018[/B]", "iwnZYL6gdTg", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling Rumble 2018[/B]", "Q6NFcV4v5HA", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Rise Underground Pro Wrestling 18+ Summersesh 2018[/B]", "w4HZ64f3rrw", 801, "RISE", art+'rise.jpg', fanart),
        ("[B]Progress Chapter 55 2018[/B]", "aEHsTXH4azY", 801, "MISC", art+'progress.jpg', fanart),
        ("[B]IPW 2 Hott 2 Handle 2016[/B]", "jwJr4TAFwYo", 801, "IPW", art+'ipw.jpg', fanart),
        ("[B]Warrior Wrestling 4 2019[/B]", "zmeFCzXf7q0", 801, "MISC", art+'warriors.jpg', fanart),
        ("[B]TNA Bound For Glory 2012[/B]", "ImQtBbxv4gg", 801, "TNA", art+'impact.jpg', fanart),
        ("[B]TNA Destination X 2012[/B]", "2Ub1m0HAPzQ", 801, "TNA", art+'impact.jpg', fanart),
        ("[B]TNA Very 1st Pay Per View 2002[/B]", "EAmbK135FVw", 801, "TNA", art+'impact.jpg', fanart),
        ("[B]TNA Slammiversity 2005[/B]", "T0KRvLwrnww", 801, "TNA", art+'impact.jpg', fanart),
        ("[B]TNA Lockdown 2005[/B]", "xiZq-OaSuVM", 801, "TNA", art+'impact.jpg', fanart),
        ("[B]TNA Lockdown 2009[/B]", "b9ayCBzwlnQ", 801, "TNA", art+'impact.jpg', fanart),
        ("[B]ROW vs Impact Wrestling[/B]", "T_Ujax_9yOo", 801, "ROW, TNA", art+'roh.jpg', fanart),
        ("[B]NWA Crocket Cup 2019[/B]", "bPtXBGYXAlQ", 801, "NWA", art+'nwa.jpg', fanart),
        ("[B]NWA Pop Up Wrestling[/B]", "encEBRB12Xs", 801, "NWA", art+'nwa.jpg', fanart),
        ("[B]NWA 70 Wrestling[/B]", "PfVB5aQlPV0", 801, "NWA", art+'nwa.jpg', fanart),
        ("[B]NWA Houston Wrestling[/B]", "rA_n-CpjUek", 801, "NWA", art+'nwa.jpg', fanart),
        ("[B]ROH: 3 Wild Kevin Steen Matches[/B]", "S_YydsYvoJ0", 801, "ROH", art+'roh.jpg', fanart),
        ("[B]ROH: 3 Wild Samoa Joe Matches[/B]", "Whi7usNNd6s", 801, "ROH", art+'roh.jpg', fanart),
        ("[B]ROH: 3 Wild AJ Styles Matches[/B]", "5WxzFMqWVe0", 801, "ROH", art+'roh.jpg', fanart),
        ("[B]ROH: 3 Wild CM Punk Matches[/B]", "d3NJyWauUE0", 801, "ROH", art+'roh.jpg', fanart),
        ("[B]ROH: 3 Wild Bryan Danielson[/B]", "7-tcrmjagG0", 801, "ROH", art+'roh.jpg', fanart),
        ("[B]ROH: 3 Wild Tyler Black[/B]", "0AbgdrZ2lMw", 801, "ROH", art+'roh.jpg', fanart),
        ("[B]ROH: 3 Wild El Generico[/B]", "W6qM_KS4iMQ", 801, "ROH", art+'roh.jpg', fanart),
        ("[B]Club WWN Greatest Hits #1[/B]", "ke6KeTb3rDw", 801, "MISC", art+'wwn.jpg', fanart),
        ("[B]Club WWN Greatest Hits #2[/B]", "GpKOKBGusk4", 801, "MISC", art+'wwn.jpg', fanart),
        ("[B]Evolve 146 Wrestling[/B]", "C-DUSDlgTwQ", 801, "MISC", art+'evolve.jpg', fanart),
        ("[B]Full Impact Pro In Full Force 2019[/B]", "ruWqODKuU5c", 801, "MISC", art+'misc3.jpg', fanart),
        ("[B]Evolve 142 Wrestling[/B]", "3l19dnc18N4", 801, "MISC", art+'evolve.jpg', fanart),
        ("[B]Evolve 141 Wrestling[/B]", "u22iWh5BtNk", 801, "MISC", art+'evolve.jpg', fanart),
        ("[B]Evolve 134 Wrestling[/B]", "Wv3Ncm8MK8I", 801, "MISC", art+'evolve.jpg', fanart),
        ("[B]ROH/NJPW G1 Supercard 2019[/B]", "tnjcUTJpJqc", 801, "ROH", art+'roh.jpg', fanart),
        ("[B]ROW Best of Hyan Collection #1[/B]", "t7p5DaG7VxQ", 801, "ROW", art+'row.jpg', fanart),
        ("[B]Evolve 125 Show of 2019 Canidate[/B]", "I286EvEMUtM", 801, "MISC", art+'evolve.jpg', fanart),
        ("[B]ROW Best of Steel Cage Matches[/B]", "jVPDCp-w7vs", 801, "ROW", art+'row.jpg', fanart),
        ("[B]ICW Shugs Hoose Party 6 Pt2[/B]", "fzYQVwXQreg", 801, "MISC", art+'misc2.jpg', fanart),
        ("[B]ROW Best of Series P1[/B]", "EAcKUkX4RoE", 801, "ROW", art+'row.jpg', fanart),
        ("[B]ICW Shugs Hoose Party 6 Pt1[/B]", "Li9bukqn9sY", 801, "MISC", art+'misc2.jpg', fanart),
        ("[B]AWL Australia Enter Phase 1[/B]", "p_lEblYWuZM", 801, "AWL", art+'awl.jpg', fanart),
        ("[B]AWL Australia: Purge New Dawn[/B]", "zlfIXWErUWI", 801, "AWL", art+'awl.jpg', fanart),
        ("[B]PWL Australia: Day Reckoning[/B]", "u2kpX8HckVU", 801, "AWL", art+'awl.jpg', fanart),
        ("[B]PWL Australia: Revolution 2[/B]", "hsp8CX5AmoE", 801, "AWL", art+'awl.jpg', fanart),
        ("[B]Britannia Royally Rumbled 2020[/B]", "NpUjUF8Nyv4", 801, "BRIT", art+'brit.jpg', fanart),
        ("[B]Smash Wrestling New Beginnings[/B]", "HfX3jB2hWiY", 801, "SMASH", art+'smash.jpg', fanart),
        ("[B]House of Glory 9th Anniversary[/B]", "nf6Qf8KSRh8", 801, "HOG", art+'hog.jpg', fanart),
        ("[B]House of Glory 8th Anniversary[/B]", "2YDcGmHNJe4", 801, "HOG", art+'hog.jpg', fanart),
        ("[B]Britannia Wrestling Road to the Rumble[/B]", "yTy8n_P1Imo", 801, "BRIT", art+'brit.jpg', fanart),
        ("[B]ROW Wrestling Christmas Chaos[/B]", "gqc4extPB64", 801, "ROW", art+'row.jpg', fanart),
        ("[B]Britannia Wrestling 2020 Vision[/B]", "yTy8n_P1Imo", 801, "BRIT", art+'brit.jpg', fanart),
        ("[B]AWA Holiday Hell 18+[/B]", "-f3BS8wrAsU", 801, "AWL", art+'awl.jpg', fanart),
        ("[B]Smash Christmas Show[/B]", "CjW9jzd5qb4", 801, "SMASH", art+'smash.jpg', fanart),
        ("[B]Britannia Wrestling Against the Odds[/B]", "wZLjYHovzh0", 801, "BRIT", art+'brit.jpg', fanart),
        ("[B]FWA: Civil War Show[/B]", "lTwkKopPOdg", 801, "FWA", art+'fwa.jpg', fanart),
        ("[B]Britannia Wrestling Summer Break[/B]", "TX36n0Wmj88", 801, "BRIT", art+'brit.jpg', fanart),
        ("[B]FWA: Battle For Destiny 3[/B]", "QLKbnjddkXE", 801, "FWA", art+'fwa.jpg', fanart),
        ("[B]CW Red Carpet Rumble III #26[/B]", "pKkeNb2w_kI", 801, "CHAMP", art+'misc3.jpg', fanart),
        ("[B]CW Red Carpet Rumble II #25[/B]", "brgtMaTten0", 801, "CHAMP", art+'misc3.jpg', fanart),
        ("[B]AWL Australia: Fire Rises[/B]", "rbIlDsQcY-g", 801, "AWL", art+'awl.jpg', fanart),
        ("[B]CW Red Carpet Rumble I #24[/B]", "Qzh4ibtJCHQ", 801, "CHAMP", art+'misc3.jpg', fanart),
        ("[B]FWA: Rated S Show[/B]", "Ji6Yy_IKu88", 801, "FWA", art+'fwa.jpg', fanart),
        ("[B]AWL Australia: Rise Rapscallion[/B]", "shBHO8HnT-4", 801, "AWL", art+'awl.jpg', fanart),
        ("[B]ROW Rise to Wrestling Royalty[/B]", "do4I7nNpEW4", 801, "ROW", art+'row.jpg', fanart),
        ("[B]ROW Summer of Champions VI[/B]", "T_Ujax_9yOo", 801, "ROW", art+'row.jpg', fanart),
        ("[B]ROW Summer of Champions V[/B]", "Td1yjcFU7kY", 801, "ROW", art+'row.jpg', fanart),
        ("[B]ROW iPPV No Limits[/B]", "V3rr5bQHWnU", 801, "ROW", art+'row.jpg', fanart),
        ("[B]AWL Australia: Revolution[/B]", "gTMn0viP2UI", 801, "AWL", art+'awl.jpg', fanart),
        ("[B]FWA: Resolution II[/B]", "-TsGbOrBH58", 801, "FWA", art+'fwa.jpg', fanart),
        ("[B]FWA: Fear Of The Dark[/B]", "GR5hzXxjbIc", 801, "FWA", art+'fwa.jpg', fanart),
        ("[B]FWA: Rise Of The Future[/B]", "D2CW8WOHjbQ", 801, "FWA", art+'fwa.jpg', fanart),
        ("[B]House of Glory High Intensity 7[/B]", "ydjAfJ7Djxc", 801, "HOG", art+'hog.jpg', fanart),
        ("[B]Capitol Wrestling Episode #159[/B]", "geomLUuSWCE", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #158[/B]", "C5ZQrrheew0", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #157[/B]", "gged1-LTEPI", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #156[/B]", "DlaReX0atkM", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #155[/B]", "yPmiC_PCijE", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #154[/B]", "AD7eQW1ManY", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #153[/B]", "feSxmCVSIYQ", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #152[/B]", "r1Odt0LEiH4", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #151[/B]", "c5b1Kp3k5K4", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #150[/B]", "E2mrJ1YTn6g", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #149[/B]", "LwBQN4EnPE4", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #148[/B]", "0QpUKqntLkg", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #147[/B]", "M0KIDjGSD-k", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #146[/B]", "DVgpJzpN6qQ", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #145[/B]", "S_tZ2aqtUE0", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #144[/B]", "SpChCKX_HIs", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #143[/B]", "xtRHoQenOf4", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #142[/B]", "eEu25ytLtuI", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #141[/B]", "qsvBQ92-C2U", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]Capitol Wrestling Episode #140[/B]", "ZqzIbFTB_Jk", 801, "CAPITOL", art+'capitol.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e40[/B]", "VAteMWVvn_M", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e39[/B]", "k2uJvLMlqAU", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e38[/B]", "GwhhP5XNoNk", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e37[/B]", "sIkEU_ri2dA", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e36[/B]", "jxbXmdDLXUw", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e35[/B]", "1oOOJZl7P8w", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e34[/B]", "KpycOb72d8w", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e33[/B]", "S4GVgsD8kZU", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e32[/B]", "-2XIe1yLz5c", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e31[/B]", "fb0ps-sGnyY", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e30[/B]", "kHsg-vGgXqw", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e29[/B]", "xbculei-s74", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e28[/B]", "_Y1nqQy0ZSY", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e27[/B]", "8ciLlzm6ZGs", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e26[/B]", "WaWHefAeSUM", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e25[/B]", "sIWKy79hpwg", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e24[/B]", "Ss3GyCN8tAM", 801, "HOB", art+'hob.jpg', fanart),
        ("[B]HOB Turnbuckle s4 e23[/B]", "HmHLArrUbew", 801, "HOB", art+'hob.jpg', fanart),
]

#=====================================

class archiveListing:

    @staticmethod
    def Genres(type):
		
        #errorMsg="%s" % (type)
        #xbmcgui.Dialog().ok("type", errorMsg)

        for name, url, zmode, genre, theImage, fanart in channellist:

            addIt=False
            if type is "All":
                icon=art+"archive.jpg"
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

            elif type is "midget" and 'MIDGET' in genre:
                icon=art+"midget.jpg"
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

            elif type is "lucha" and 'LUCHA' in genre:
                icon=art+"lucha.jpg"
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

            elif type is "awl" and 'AWL' in genre:
                icon=art+"awl.jpg"
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

            elif type is "tmn" and 'TMN' in genre:
                icon=art+"tmn.jpg"
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

            elif type is "waw" and 'WAW' in genre:
                icon=art+"waw.jpg"
                addIt=True
		
            if addIt==True:
	            #theImage = ytImageHQ.replace('URL',url)
	            addLink(name,url,zmode,theImage,fanart)
	            #addLink(name,url,zmode,icon,fanart)

#=====================================

