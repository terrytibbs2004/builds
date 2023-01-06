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
        ("[B]Sweet Emotion: Aerosmith Live[/B]", "33ClrPlzuVQ", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]The Story Of Aerosmith[/B]", "Ik0a409bNRA", 801, "Docs", mediapath+'Music.png', fanart),
        ("[B]The Story Of Lynyrd Skynyrd[/B]", "AePnPCSFCfI", 801, "Docs", mediapath+'Music.png', fanart),
        ("[B]Pour Some Sugar On It: Def Leppard[/B]", "l9NP8jaOxf0", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Foolin: Def Leppard Live 2012[/B]", "zz8UYM9MFpg", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Rock Of Ages + Photograph: Def Leppard[/B]", "BMC77fgiJEA", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Smokin In The Boys Room: Motley Crue[/B]", "5oVBvxA0mm0", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Every Rose Has Its Thorn: Poison[/B]", "LGVuqf6_rcI", 801, "Anthem", mediapath+'Music.png', fanart),
        ("[B]Schools Out: Alice Cooper Live[/B]", "LVwslrvZnz0", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Aqualung: Jethro Tull Live 1980[/B]", "8I58oeTvgNU", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Rollin On Down The Highway: Bachman Turner[/B]", "OAQdbYX5oeo", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Born To Be Wild: Steppenwolf 1968[/B]", "mLhpXUtxS1c", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Holy Water: Bad Company[/B]", "4wGkZJ9JFII", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]If You Needed Somebody: Bad Company[/B]", "_AMKtiS6UEQ", 801, "Anthem", mediapath+'Music.png', fanart),
        ("[B]Locomotive Breath: Jethro Tull[/B]", "eSUdlUmtg3Q", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Sweet Home Alabama: Lynyrd Skynyrd[/B]", "Zup5Pg98m5U", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]More Than A Feeling: Boston Live[/B]", "YOPnzvSrZd4", 801, "Rock, Anthem", mediapath+'Music.png', fanart),
        ("[B]Bad Company: Bad Company Live[/B]", "af4NuB3j7BA", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Go Your Own Way: Fleetwood Mac[/B]", "kFNKhNLUS9s", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]I Wanna Know What Love Is: Foreigner[/B]", "NVFfjWqfui8", 801, "Rock, Anthem", mediapath+'Music.png', fanart),
        ("[B]Devil Went Down To Georgia: Charlie Daniels[/B]", "yLIqvYHcv48", 801, "Country", mediapath+'Music.png', fanart),
        ("[B]Smoke On The Water: Deep Purple[/B]", "_rSrrgwYGjo", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Inside Looking Out: Grand Funk Railroad[/B]", "9U8socv_seg", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]King Of Dreams: Deep Purple 1990[/B]", "i5WoLKFPhY8", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Dont Want To Miss A Thing: Aerosmith[/B]", "C_2dXspJe_Y", 801, "Rock, Anthem", mediapath+'Music.png', fanart),
        ("[B]Shooting Star: Bad Company Live[/B]", "w4iGKjO9A-g", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]King Of Dreams: Deep Purple 1990[/B]", "i5WoLKFPhY8", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Hold On Loosely: 38 Special[/B]", "vJtf7R_oVaw", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Stairway To Heaven: Led Zeppelin[/B]", "6hBLHkmBKDg", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Dream On: Aerosmith 2014[/B]", "MqZcg68QfE4", 801, "Rock, Anthem", mediapath+'Music.png', fanart),
        ("[B]Save All Your: Great White[/B]", "kBY31lCXimo", 801, "Rock, Anthem", mediapath+'Music.png', fanart),
        ("[B]Never Been Any Reason: Head East[/B]", "VgvL6aqJxMA", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Shes A Beauty: The Tubes[/B]", "mQ_k_VG6Syc", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Lay It On The Line: Triumph[/B]", "gCWj8Nz5DUg", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Slaughter: Fly To The Angels[/B]", "ukmobha2krY", 801, "Rock, Metal, Anthem", mediapath+'Music.png', fanart),
        ("[B]Great White: Rock Me[/B]", "yg06B46VVys", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Lola: The Kinks Rock & Roll Hall Of Fame Benefit[/B]", "wbX2aQQ4uog", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Little Help From My Friends: Joe Cocker[/B]", "NR-H2uFCQls", 801, "Rock, Anthem", mediapath+'Music.png', fanart),
        ("[B]Heartbreaker: Grand Funk Railroad[/B]", "uW3nPqPPBDw", 801, "Rock, Metal, Blues", mediapath+'Music.png', fanart),
        ("[B]Suzy Q: Johnny Winter Live At Rockpalast[/B]", "QII1YfFVhNU", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Im Your Captain: Grand Funk Railroad[/B]", "g8MYsii4DZY", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Heart: Barracuda (1977)[/B]", "PeMvMNpvB5M", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Going Home: Ten Years After Woodstock 69[/B]", "_m7Q_rGLS_Q", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]A Man Ill Never Be: Boston[/B]", "gZxP3bMn0as", 801, "Rock, Metal, Anthem", mediapath+'Music.png', fanart),
        ("[B]Feeling Stronger Every Day: Chicago[/B]", "e-wHixgp2RE", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Blinded By The Light: Manfred Mann[/B]", "lcWVL4B-4pI", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Plush: Stone Temple Pilots[/B]", "3hCnZ4WNug4", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Alive: Pearl Jam On Countdown[/B]", "gb9uQJYNybU", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Better Man: Pearl Jam Rock Hall 2017[/B]", "84zCxQYTMy0", 801, "Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]Im A Man: Spencer Davis Group[/B]", "4_gFF-z9OS8", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Stealin: Uriah Heep Live[/B]", "CiRFW8QSQYY", 801, "Rock, Anthem", mediapath+'Music.png', fanart),
        ("[B]Dead Or Alive: Bon Jovi Madison Square Garden 2012[/B]", "Zdnhx-p-n5k", 801, "Rock, Blues Anthem", mediapath+'Music.png', fanart),
        ("[B]Dead Or Alive: Bon Jovi[/B]", "Mqyrt7RCgsg", 801, "Rock, Blues, Anthem", mediapath+'Music.png', fanart),
        ("[B]Best Rock Ballads[/B]", "9MLgnD13aZc", 801, "Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]Def Leppard Story[/B]", "Dj7BHCpX4Ho", 801, "Docs, Rock", mediapath+'Music.png', fanart),
        ("[B]Jefferson Airplane Story[/B]", "9hrfujWd1WA", 801, "Docs, Rock", mediapath+'Music.png', fanart),
        ("[B]Bohenian Rhapsody: Queen[/B]", "3p4MZJsexEs", 801, "Rock, Anthem", mediapath+'Music.png', fanart),
        ("[B]Muppets Bohemian Rhapsody[/B]", "tgbNymZ7vqY", 801, "Rock, TV", mediapath+'Music.png', fanart),
        ("[B]The Foreigner Story[/B]", "uRBNhZUujVY", 801, "Docs, Rock", mediapath+'Music.png', fanart),
        ("[B]Happy Day: Sister Act II[/B]", "SLY7yI1xV-M", 801, "Movie", mediapath+'Music.png', fanart),
        ("[B]Guns n Roses: Band That Time Forgot[/B]", "lhLVTnzqJj4", 801, "Docs, Rock", mediapath+'Music.png', fanart),
        ("[B]Bon Jovi: When We Were Beautiful[/B]", "pmmN7_gH9vc", 801, "Docs, Rock", mediapath+'Music.png', fanart),
        ("[B]Betty Davis Eyes[/B]", "EPOIS5taqA8", 801, "Rock, Pop, Alternative", mediapath+'Music.png', fanart),
        ("[B]Hold Your Head Up: Argent[/B]", "o-6v4H4BtWI", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Deep Purple The History[/B]", "nOcoGotfabc", 801, "Docs, Rock", mediapath+'Music.png', fanart),
        ("[B]The Blues Story Doc[/B]", "5qq_qnLHf74", 801, "Docs, Blues, Soul", mediapath+'Music.png', fanart),
        ("[B]Grand Funk Railroad Doc[/B]", "yhOeTZIyZqI", 801, "Docs, Rock", mediapath+'Music.png', fanart),
        ("[B]Girl Groups Documentary[/B]", "jyzL6D-5znY", 801, "Docs, Pop, RnB, Soul", mediapath+'Music.png', fanart),
        ("[B]Wanna Know What Love Is: Foreigner[/B]", "dWwEi4SNf1M", 801, "Rock, Anthem, Blues", mediapath+'Music.png', fanart),
        ("[B]Livin On A Prayer[/B]", "ekomXrzOF3A", 801, "Rock, Anthem", mediapath+'Music.png', fanart),
        ("[B]Cant Fight This Feeling: Reo Speedwagon[/B]", "-10Gy6xc-WM", 801, "Anthem, Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]Alone: Heart[/B]", "rtopccRfyUU", 801, "Anthem, Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]With Or Without You: U2[/B]", "6DeDzsCGbsQ", 801, "Anthem, Rock, Blues, Alternative", mediapath+'Music.png', fanart),
        ("[B]Comfortably Numb: Pink Floyd[/B]", "LTseTg48568", 801, "Anthem, Rock, Blues, Metal", mediapath+'Music.png', fanart),
        ("[B]Final Countdown: Europe[/B]", "HyWajWueH2w", 801, "Anthem, Rock", mediapath+'Music.png', fanart),
        ("[B]Dream On: Aerosmith[/B]", "zthQPe41w24", 801, "Anthem, Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]Keep On Lovin You: Reo Speedwagon[/B]", "7tvhmq6_IKs", 801, "Anthem, Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]Money For Nothing: Dire Straits[/B]", "JcqhvPNiJzo", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Highway Star: Deep Purple[/B]", "VmAeuJ_gW1Q", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Dont You (Forget About Me): Simple Minds[/B]", "T-dRPKC_7-Y", 801, "Alternative", mediapath+'Music.png', fanart),
        ("[B]Since You Been Gone: Rainbow[/B]", "sKW9kWAIdI0", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Hysteria: Def Leppard[/B]", "5HSP2JnAvb0", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Dont Want To Miss A Thing: Aerosmith[/B]", "9o4kvBI5A98", 801, "Anthem, Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]Home Sweet Home: Motley Crue[/B]", "C9U5HGYe0Mk", 801, "Anthem, Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]Separate Ways: Journey[/B]", "j-eVamWhUBw", 801, "Anthem, Blues", mediapath+'Music.png', fanart),
        ("[B]Dont Stop Believin (Dan Lucus) The Voice[/B]", "Ozmoe6hSBzo", 801, "Anthem, Rock, TV", mediapath+'Music.png', fanart),
        ("[B]Crazy On You: Heart[/B]", "RBq_THTWNM4", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Try (Truth About Love): Pink[/B]", "ivPEKaBHjYA", 801, "Pop, RnB", mediapath+'Music.png', fanart),
        ("[B]Say You Will: Foreigner[/B]", "rqOwtJqaxfw", 801, "Anthem, Rock", mediapath+'Music.png', fanart),
        ("[B]You Give Love A Bad Name: Bon Jovi[/B]", "pxAveEQOoNQ", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Alone (Dan Lucas) The Voice[/B]", "nxiOBhaGWMo", 801, "Rock, Blues, TV", mediapath+'Music.png', fanart),
        ("[B]Whiter Shade Of Pale: Geff Harrison The Voice[/B]", "9oG8faoL-Zk", 801, "Blues, TV", mediapath+'Music.png', fanart),
        ("[B]Thrill Is Gone: BB King[/B]", "HzTlB-TjAzM", 801, "Blues, Rock, Soul, RnB", mediapath+'Music.png', fanart),
        ("[B]Smoke On The Water: The Voice[/B]", "treNBRm1Ruc", 801, "Rock, Metal, TV", mediapath+'Music.png', fanart),
        ("[B]Still Lovin You: The Voice[/B]", "QTxrwYzl6f8", 801, "Anthem, Blues, TV", mediapath+'Music.png', fanart),
        ("[B]Without You: Mariah Carey[/B]", "H6oGuXenlNo", 801, "Pop", mediapath+'Music.png', fanart),
        ("[B]Alone: Floortje Smit The Voice[/B]", "uVx9CaavEPA", 801, "Anthem, Blues, Rock, TV", mediapath+'Music.png', fanart),
        ("[B]Simple Man: Lynyrd Skynyrd[/B]", "Mqfwbf3X8SA", 801, "Rock, Blues, Anthem", mediapath+'Music.png', fanart),
        ("[B]I Will Always Love You: Whitney Houston[/B]", "XKRI8CcpC9M", 801, "RnB", mediapath+'Music.png', fanart),
        ("[B]Feels Like The Firt Time: Foreigner[/B]", "z2WDDxFXJ9s", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Dust In The Wind: Kansas[/B]", "4XvI__yHNow", 801, "Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]Time: Pink Floyd[/B]", "oEGL7j2LN84", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Purple Rain: Prince[/B]", "TvnYmWpD_T8", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Sweet Child O Mine: Guns N Roses[/B]", "HlEuo9aR7Qo", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Hotel California: Eagles[/B]", "yYkL5igsG4k", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]What About Love: Heart[/B]", "APznhptgsb8", 801, "Rock, Anthem", mediapath+'Music.png', fanart),
        ("[B]Go Your Own Way: Fleetwood Mac[/B]", "nZt49yGvdeY", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Little Help From My Friends: Joe Cocker[/B]", "oL1JyDTq3Qc", 801, "Rock, Metal, Anthem", mediapath+'Music.png', fanart),
        ("[B]Cant You See: Marshall Tucker Band[/B]", "dlc6xCPx60U", 801, "Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]How Many More Times: Led Zeppelin[/B]", "qSIS0o7vtPE", 801, "Rock, Blues, Metal", mediapath+'Music.png', fanart),
        ("[B]Bohemian Rhaposy: The Voice[/B]", "jZ6DBG54c3Y", 801, "Blues, Rock, TV", mediapath+'Music.png', fanart),
        ("[B]Dont Look Back: Boston[/B]", "2HuiH-0R6a0", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Lady: Styx[/B]", "uR4if4ble1A", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Pitch Perfect 1: Finale[/B]", "mAVPYq8fc3k", 801, "Movie, Alternative", mediapath+'Music.png', fanart),
        ("[B]Pitch Perfect 2: Finale[/B]", "6RsgmjeAQ14", 801, "Movie", mediapath+'Music.png', fanart),
        ("[B]Pitch Perfect 3: Freedom[/B]", "foV6LGohzBI", 801, "Movie", mediapath+'Music.png', fanart),
        ("[B]Tumblin Dice: Linda Ronstadt[/B]", "yBg5cnoNyAE", 801, "Rock, Movie", mediapath+'Music.png', fanart),
        ("[B]School Of Rock[/B]", "oP7kExN8LFA", 801, "Rock, Movie", mediapath+'Music.png', fanart),
        ("[B]Once Bitten: 3 Speed[/B]", "NqqyWI9LDeY", 801, "Movie", mediapath+'Music.png', fanart),
        ("[B]Staying Alive: Airplane[/B]", "ar3wkC8U6LA", 801, "Movie", mediapath+'Music.png', fanart),
        ("[B]Rocket Man: Elton John[/B]", "DtVBCG6ThDk", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Tiny Dancer: Elton John[/B]", "XujEruAWcR4", 801, "Blues", mediapath+'Music.png', fanart),
        ("[B]The Chain: Fleetwood Mac[/B]", "kBYHwH1Vb-c", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Verace On The Floor: Bruno Mars[/B]", "-FyjEnoIgTM", 801, "Pop", mediapath+'Music.png', fanart),
        ("[B]Love On Top: Beyonce[/B]", "Ob7vObnFUJc", 801, "RnB", mediapath+'Music.png', fanart),
        ("[B]Drunk In Love: Explicit Beyonce[/B]", "p1JPKLa-Ofc", 801, "Pop", mediapath+'Music.png', fanart),
        ("[B]Crazy In Love: Beyonce[/B]", "ViwtNLUqkMY", 801, "RnB, Pop", mediapath+'Music.png', fanart),
        ("[B]Run The World: Beyonce[/B]", "VBmMU_iwe6U", 801, "RnB", mediapath+'Music.png', fanart),
        ("[B]Love On The Brain: Rhianna[/B]", "0RyInjfgNc4", 801, "Pop, HipHop, Rap", mediapath+'Music.png', fanart),
        ("[B]Diamonds: Rhianna[/B]", "lWA2pjMjpBs", 801, "Pop", mediapath+'Music.png', fanart),
        ("[B]Beautiful Trauma: Pink[/B]", "EBt_88nxG4c", 801, "Pop", mediapath+'Music.png', fanart),
        ("[B]Please Dont Leave Me: Pink[/B]", "eocCPDxKq1o", 801, "Pop", mediapath+'Music.png', fanart),
        ("[B]Lose Yourself:Eminem[/B]", "_Yhyp-_hX2s", 801, "Rap", mediapath+'Music.png', fanart),
        ("[B]In The Club: 50 Cents[/B]", "OUeaAOIAbXs", 801, "Rap", mediapath+'Music.png', fanart),
        ("[B]Hells Bells AC/DC[/B]", "3tOKYFR4Rzg", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]You Shook Me All Night Long: AC/DC[/B]", "zakKvbIQ28o", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Highway To Hell: AC/DC[/B]", "gEPmA3USJdI", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Shadows Of The Night: Pat Benatar[/B]", "Qccnc693ETw", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Best Of The Worst: Charm City Devils[/B]", "h7XhpOrrkAM", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]The Man Ill Never Be: Boston[/B]", "gZxP3bMn0as", 801, "Rock, Metal, Blues", mediapath+'Music.png', fanart),
        ("[B]Dreams: Van Halen[/B]", "d5PqVeex4QU", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Money For Nothing: Classic Rock Show[/B]", "0Q50DXNWU2Q", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]When Its Love: Van Halen[/B]", "kIPWrpD1OWc", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Wang Dang Doodle: Grateful Dead[/B]", "Afv-C7j73pM", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Black Oak Arkansas Rockumentary[/B]", "WHuCfG5mXNk", 801, "Rock, Docs", mediapath+'Music.png', fanart),
        ("[B]Sugar Magnolia: Grateful Dead[/B]", "V70MrjzLFyo", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Uncle Johns Band: Grateful Dead[/B]", "vvxtly3o3OI", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Photograph: Def Leppard[/B]", "_kVYAkK0bkY", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Why Cant This Be Love: Van Halen[/B]", "wB7cYGokbx0", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Best Of Both Worlds: Van Halen[/B]", "X6x0NWRh7WQ", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Hunger City: Cherry Bombs[/B]", "x5_yOzK8T5Q", 801, "Rock", mediapath+'Music.png', fanart),
        ("[B]Second Chance: Shinedown[/B]", "WbsDPbr8qoM", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]45: Shinedown[/B]", "MLeIyy2ipps", 801, "Rock, Metal, Blues", mediapath+'Music.png', fanart),
        ("[B]Remember When: Alan Jackson[/B]", "TTA2buWlNyM", 801, "Country", mediapath+'Music.png', fanart),
        ("[B]Craving You: Thomas Rhett[/B]", "VGWZrO5U9ek", 801, "Country", mediapath+'Music.png', fanart),
        ("[B]Tennessee Whiskey Chris Stapleton[/B]", "4zAThXFOy2c", 801, "Country, Blues", mediapath+'Music.png', fanart),
        ("[B]Alone With You: Jake Owen[/B]", "Y3EpArAtGJQ", 801, "Country", mediapath+'Music.png', fanart),
        ("[B]Country Girl: Luke Bryan[/B]", "7HX4SfnVlP4", 801, "Country", mediapath+'Music.png', fanart),
        ("[B]Where I Come From: Montgomery Gentry[/B]", "7iDwzIB6Pn0", 801, "Country", mediapath+'Music.png', fanart),
        ("[B]Whiskey River: Willie Nelson[/B]", "LxQBMxvGJVA", 801, "Country, Rock", mediapath+'Music.png', fanart),
        ("[B]We Wont Be Fooled Again: Classic Rock Show[/B]", "Vm0Pw8aPpKg", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Comfortably Numb: David Gilmour Pompeii 2016[/B]", "LTseTg48568", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Run Like Hell: David Gilmour Pompeii 2016[/B]", "El4AEHR1ANw", 801, "Country", mediapath+'Music.png', fanart),
        ("[B]Wish You Were Here: Gilmour Pompeii 2016[/B]", "WaEKXGlfYj8", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]One Of These Days: Gilmour Pompeii 2016[/B]", "nXaXKfyI7tQ", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Shine On You Crazy Diamond: Gilmour Pompeii 2016[/B]", "CiXNIjGX1hY", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Time/Breathe: David Gilmour Pompeii 2016[/B]", "sogFyPrAY5E", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Simple Man: Lynyrd Skynyrd Florida Theatre 2015[/B]", "Mqfwbf3X8SA", 801, "Rock, Blues", mediapath+'Music.png', fanart),
        ("[B]Coming Back To Life: Gilmour Pompeii 2016[/B]", "YTaYw6V5HP4", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]High Hopes: David Gilmour Pompeii 2016[/B]", "-xveqYrKJTE", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]5AM: David Gilmour Live At Pompeii 2016[/B]", "Gxg58Tegflg", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Rattle That Lock: Gilmour Pompeii 2016[/B]", "HHfkMg0ZrU4", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Faces Of Stone: David Gilmour Pompeii 2016[/B]", "xFai4z9Z5bU", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]What Do You Want From Me: Gilmour Pompeii 2016[/B]", "bKJqJt5RLrs", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]The Blue: David Gilmour Live At Pompeii 2016[/B]", "sztwFEFYpqs", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Great Gig In The Sky: Gilmour Pompeii 2016[/B]", "jXRJSyHuG2I", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]A Boat Lies Waiting: Gilmour Pompeii 2016[/B]", "z3GNlRDWupc", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Money: David Gilmour Live At Pompeii 2016[/B]", "26nZZSLs65o", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]In Any Tongue: David Gilmour Pompeii 2016[/B]", "iOACn7v-_VI", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Purple Haze: Jimi Hendrix Atlanta Pop[/B]", "cJunCsrhJjg", 801, "Rock, Metal", mediapath+'Music.png', fanart),
        ("[B]Red House: Jimi Hendrix Experience Live[/B]", "JzUiGuQKrRE", 801, "Rock, Metal, Blues", mediapath+'Music.png', fanart),
        ("[B]Freedom: Jimi Hendrix Experience Live[/B]", "wDvlErh5zcc", 801, "Rock, Metal, Blues", mediapath+'Music.png', fanart),
        ("[B]Hey Joe: Jimi Hendrix Monterey Pop 1967[/B]", "fe82eYRjiBU", 801, "Rock, Metal, Blues", mediapath+'Music.png', fanart),
        ("[B]Like A Rolling Stone: Jimi Hendrix[/B]", "ktjpxrIFOx8", 801, "Rock, Metal, Blues", mediapath+'Music.png', fanart),
        ("[B]Foxey Lady: Jimi Hendrix Miami Pop 1968[/B]", "_PVjcIO4MT4", 801, "Rock, Metal, Blues", mediapath+'Music.png', fanart),
]

#=====================================

class MuzicListing:

    @staticmethod
    def Genres(type):
		
        #errorMsg="%s" % (type)
        #xbmcgui.Dialog().ok("type", errorMsg)

        for name, url, zmode, genre, icon, fanart in sorted(channellist, reverse=False):

            addIt=False
            if type is "All":
                icon=mediapath+"All-muzic.png"
                addIt=True

            elif type is "Alternative" and "Alternative" in genre:
                icon=mediapath+"Alternative.png"
                addIt=True

            elif type is "Anthem" and "Anthem" in genre:
                icon=mediapath+"Anthem.png"
                addIt=True

            elif type is "Blues" and "Blues" in genre:
                icon=mediapath+"Blues.png"
                addIt=True

            elif type is "Country" and "Country" in genre:
                icon=mediapath+"Country.png"
                addIt=True

            elif type is "Docs" and "Docs" in genre:
                icon=mediapath+"Docs.png"
                addIt=True

            elif type is "HipHop" and "HipHop" in genre:
                icon=mediapath+"Hip Hop.png"
                addIt=True

            elif type is "Jazz" and "Jazz" in genre:
                icon=mediapath+"Jazz.png"
                addIt=True

            elif type is "Metal" and "Metal" in genre:
                icon=mediapath+"Metal.png"
                addIt=True

            elif type is "Movie" and "Movie" in genre:
                icon=mediapath+"Movie.png"
                addIt=True

            elif type is "Pop" and "Pop" in genre:
                icon=mediapath+"Pop.png"
                addIt=True

            elif type is "Punk" and "Punk" in genre:
                icon=mediapath+"Punk.png"
                addIt=True

            elif type is "RnB" and "RnB" in genre:
                icon=mediapath+"RnB.png"
                addIt=True

            elif type is "Rock" and "Rock" in genre:
                icon=mediapath+"Rock.png"
                addIt=True

            elif type is "Rap" and "Rap" in genre:
                icon=mediapath+"Rap.png"
                addIt=True

            elif type is "Soul" and "Soul" in genre:
                icon=mediapath+"Soul.png"
                addIt=True

            elif type is "TV" and "TV" in genre:
                icon=mediapath+"TV.png"
                addIt=True
		
            if addIt==True:
	            addLink(name,url,zmode,icon,fanart)

#=====================================

