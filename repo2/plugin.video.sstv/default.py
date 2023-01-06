 #############Imports#############
import base64,os,re,unicodedata,requests,time,string,sys,json,datetime,zipfile,shutil
from resources.modules import client,control,tools,shortlinks
from resources.ivue import ivuesetup
from kodi_six import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
from datetime import date
import xml.etree.ElementTree as ElementTree
import six
from six.moves import urllib_parse, urllib_request

def getKodiVersion():
    return int(xbmc.getInfoLabel("System.BuildVersion").split(".")[0])
transPath = xbmc.translatePath if getKodiVersion() < 19 else xbmcvfs.translatePath
#################################

#############Defined Strings#############
addon_id     = 'plugin.video.sstv'
selfAddon    = xbmcaddon.Addon(id=addon_id)
icon         = transPath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart       = transPath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

username     = control.setting('Username')
password     = control.setting('Password')
host         = control.setting('Host')

port         = '81'

live_url     = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories'%(host,port,username,password)
vod_url      = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
series_url   = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(host,port,username,password)
panel_api    = '%s:%s/panel_api.php?username=%s&password=%s'%(host,port,username,password)
play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
all_series_url   = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series&cat_id=0'%(host,port,username,password)

Guide = transPath(os.path.join('special://home/addons/plugin.video.sstv/resources/catchup', 'guide.xml'))
GuideLoc = transPath(os.path.join('special://home/addons/plugin.video.sstv/resources/catchup', 'g'))

advanced_settings           =  transPath('special://home/addons/'+addon_id+'/resources/advanced_settings')
advanced_settings_target    =  transPath(os.path.join('special://home/userdata','advancedsettings.xml'))
#########################################


def start():
    if username=="":
        user = userpopup()
        passw= passpopup()
        control.setSetting('Username',user)
        control.setSetting('Password',passw)
        xbmc.executebuiltin('Container.Refresh')
        auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,user,passw)
        auth = tools.OPEN_URL(auth)
        auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(host,port,user,passw)
        auth = tools.OPEN_URL(auth)
        if auth == "":
            line1 = "Login Details Incorrect"
            line2 = "Please Try Again" 
            line3 = "" 
            xbmcgui.Dialog().ok('Attention', line1 + '\n' + line2 + '\n' + line3)
            start()
        else:
            line1 = "Login Successful"
            line2 = "Welcome to [B]SS TV[/B]!" 
            line3 = ('[B][COLOR white]%s[/COLOR][/B]'%user)
            xbmcgui.Dialog().ok('SS TV', line1 + '\n' + line2 + '\n' + line3)
            addonsettings('ADS2','')
            xbmc.executebuiltin('Container.Refresh')
            home()
    else:
        auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
        auth = tools.OPEN_URL(auth)
        auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(host,port,username,password)
        auth = tools.OPEN_URL(auth)
        if not auth=="":
            tools.addDir('[B][COLOR white]Account Details[/COLOR][/B]','url',6,icon,fanart,'')
            tools.addDir('[B][COLOR white]Live Channels[/COLOR][/B]','live',1,icon,fanart,'')
            tools.addDir('[B][COLOR white]Movies[/COLOR][/B]','url',11,icon,fanart,'')
            tools.addDir('[B][COLOR white]TV Shows[/COLOR][/B]','url',12,icon,fanart,'')
            tools.addDir('[B][COLOR white]TV Guide[/COLOR][/B]','url',122,icon,fanart,'')
            tools.addDir('[B][COLOR white]Tools[/COLOR][/B]','url',16,icon,fanart,'')
            tools.addDir('[B][COLOR white]Settings[/COLOR][/B]','AS',10,icon,fanart,'')
            tools.addDir('[B][COLOR white]Log Out[/COLOR][/B]','LO',10,icon,fanart,'')
            
            
def home():
    tools.addDir('Account Details','url',6,icon,fanart,'')
    tools.addDir('Live Channels','live',1,icon,fanart,'')
    tools.addDir('Movies','url',11,icon,fanart,'')
    tools.addDir('TV Shows','url',12,icon,fanart,'')
    tools.addDir('Catchup TV','url',13,icon,fanart,'')
    tools.addDir('Tools','url',16,icon,fanart,'')
    tools.addDir('Settings','AS',10,icon,fanart,'')
    tools.addDir('Log Out','LO',10,icon,fanart,'')
    

def livecategory(url):
    
    open = tools.OPEN_URL(live_url)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        name = tools.regex_from_to(a,'<title>','</title>')
        name = base64.b64decode(name)
        url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
        tools.addDir(name,url1,2,icon,fanart,'')

def livelist(url):
    open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        name = tools.regex_from_to(a,'<title>','</title>')
        name = base64.b64decode(name)
        xbmc.log(str(name))
        try:
            name = re.sub('\[.*?min ','-',name)
        except:
            pass
        thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
        url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
        desc = tools.regex_from_to(a,'<description>','</description>')
        tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))

def vod(url):
    if url =="vod":
        open = tools.OPEN_URL(vod_url)
    else:
        open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(base64.b64decode(name),url1,3,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(name,url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                if xbmcaddon.Addon().getSetting('hidexxx')=='true':
                    tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
                else:
                    if not 'XXX' in name:
                        if not 'Adult' in name:
                            tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)  
        
##########################################
def catchup():
    listcatchup()
        
def listcatchup():
    open = tools.OPEN_URL(panel_api)
    all  = tools.regex_get_all(open,'{"num','direct')
    for a in all:
        if '"tv_archive":1' in a:
            name = tools.regex_from_to(a,'"epg_channel_id":"','"').replace('\/','/')
            thumb= tools.regex_from_to(a,'"stream_icon":"','"').replace('\/','/')
            id   = tools.regex_from_to(a,'stream_id":"','"')
            if not name=="":
                tools.addDir(name,'url',14,thumb,fanart,id)
            

def tvarchive(name,description):
    days = 7
    
    now = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','')
    date3 = datetime.datetime.now() - datetime.timedelta(days)
    date = str(date3)
    date = str(date).replace('-','').replace(':','').replace(' ','')
    APIv2 = base64.b64decode("JXM6JXMvcGxheWVyX2FwaS5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmYWN0aW9uPWdldF9zaW1wbGVfZGF0YV90YWJsZSZzdHJlYW1faWQ9JXM=")%(host,port,username,password,description)
    link=tools.OPEN_URL(APIv2)
    match = re.compile('"title":"(.+?)".+?"start":"(.+?)","end":"(.+?)","description":"(.+?)"').findall(link)
    for ShowTitle,start,end,DesC in match:
        ShowTitle = base64.b64decode(ShowTitle)
        DesC = base64.b64decode(DesC)
        format = '%Y-%m-%d %H:%M:%S'
        try:
            modend = dtdeep.strptime(end, format)
            modstart = dtdeep.strptime(start, format)
        except:
            modend = datetime.datetime(*(time.strptime(end, format)[0:6]))
            modstart = datetime.datetime(*(time.strptime(start, format)[0:6]))
        StreamDuration = modend - modstart
        modend_ts = time.mktime(modend.timetuple())
        modstart_ts = time.mktime(modstart.timetuple())
        FinalDuration = int(modend_ts-modstart_ts) / 60
        strstart = start
        Realstart = str(strstart).replace('-','').replace(':','').replace(' ','')
        start2 = start[:-3]
        editstart = start2
        start2 = str(start2).replace(' ',' - ')
        start = str(editstart).replace(' ',':')
        Editstart = start[:13] + '-' + start[13:]
        Finalstart = Editstart.replace('-:','-')
        if Realstart > date:
            if Realstart < now:
                catchupURL = base64.b64decode("JXM6JXMvc3RyZWFtaW5nL3RpbWVzaGlmdC5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmc3RyZWFtPSVzJnN0YXJ0PQ==")%(host,port,username,password,description)
                ResultURL = catchupURL + str(Finalstart) + "&duration=%s"%(FinalDuration)
                kanalinimi = "[B][COLOR white]%s[/COLOR][/B] - %s"%(start2,ShowTitle)
                tools.addDir(kanalinimi,ResultURL,4,icon,fanart,DesC)


def DownloaderClass(url, dest):
    dp = xbmcgui.DialogProgress()
    dp.create('Fetching latest Catch Up',"Fetching latest Catch Up...",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib_request.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[COLOR white]%.02f MB of less than 5MB[/COLOR]' % (currently_downloaded)
            e = '[COLOR white]Speed:  %.02f Mb/s ' % mbps_speed  + '[/COLOR]'
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled():
            dialog = xbmcgui.Dialog()
            dialog.ok("SS TV", 'The download was cancelled.')
                
            sys.exit()
            dp.close()
##########################################

def search_scat(url):
    text = searchdialog()
    if not text:
        xbmc.executebuiltin("XBMC.Notification([COLOR white][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
        return
    return scat(url,text)

def scat(url,search=None):
    open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(base64.b64decode(name),url1,24,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)

##########################################

def seasons(url):
    if url =="seasons":
        open = tools.OPEN_URL(seasons_url)
    else:
        open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(base64.b64decode(name).replace('?',''),url1,21,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)

##########################################

def eps(url):
    open = tools.OPEN_URL(url)
    #print open
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(base64.b64decode(name).replace('?',''),url1,22,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)

##########################################
def series(url):
    log(url)
    if url =="vod":
        open = tools.OPEN_URL(vod_url)
    else:
        open = tools.OPEN_URL(url)
    log(open)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(base64.b64decode(name).replace('?',''),url1,20,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc)) 
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        
#####################################################################

def tvguide():
    if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)') and xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
        dialog = xbmcgui.Dialog().select('Select a TV Guide', ['PVR TV Guide','iVue TV Guide'])
        if dialog==0:
            xbmc.executebuiltin('ActivateWindow(TVGuide)')
        elif dialog==1:
            xbmc.executebuiltin('RunAddon(script.ivueguide)')
    elif not xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)') and xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
        xbmc.executebuiltin('RunAddon(script.ivueguide)')
    elif xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)') and not xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
        xbmc.executebuiltin('ActivateWindow(TVGuide)')

def stream_video(url):
    url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
    liz = xbmcgui.ListItem('')
    liz.setArt({ 'thumb': iconimage, 'icon': iconimage, 'fanart': fanart}) 
    liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
    liz.setProperty('IsPlayable','true')
    liz.setPath(str(url))
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    
    
def subm():
    tools.addDir('[COLOR white]All Movies[/COLOR]','vod',333,icon,fanart,'')
    tools.addDir('[COLOR white]Movie Categories[/COLOR]','vod',3,icon,fanart,'')
    tools.addDir('[COLOR white]Search Movies[/COLOR]','url',5,icon,fanart,'')

def subt():
    tools.addDir('[COLOR white]TV Show Categories[/COLOR]',series_url,24,icon,fanart,'')
    tools.addDir('[COLOR white]Search TV Shows[/COLOR]',all_series_url,2424,icon,fanart,'')

def subg():
    if xbmc.getCondVisibility('System.HasAddon(script.ivueguide)'):
        tools.addDir('[COLOR white]Launch iVue[/COLOR]','pvr',7,icon,fanart,'')
    tools.addDir('[COLOR white]Configure iVue[/COLOR]','pvr',75,icon,fanart,'')
    
def tvguide():
    xbmc.executebuiltin('RunAddon(script.ivueguide)')

def guideconf():
    xbmc.executebuiltin('RunAddon(plugin.video.IVUEcreator)')


def searchdialog():
    search = control.inputDialog(heading='Search SS TV:')
    if search=="":
        return
    else:
        return search

    
def search():
    if mode==([3, 4, 20, 21]):
        return False
    #text = searchdialog()
    text = xbmcgui.Dialog().input("Search for a Movie ?")
    xbmc.log(repr(text),xbmc.LOGERROR)
    if not text:
        xbmc.executebuiltin("XBMC.Notification([COLOR white][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
        return
    xbmc.log(str(text))
    open = tools.OPEN_URL(panel_api)
    import json
    j = json.loads(open)
    available_channels = j["available_channels"]
    for id,channel in list(available_channels.items()):
        name = channel["name"] or ''
        type = channel["stream_type"] or ''
        ext = channel["container_extension"] or ''
        thumb = channel["stream_icon"] or ''
        fanart = ''
        liz=xbmcgui.ListItem(name)
        liz.setArt({ 'thumb': iconimage, 'icon': iconimage, 'fanart': fanart})
        liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":'',})
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
        xbmc.log(repr(name))
        if text in name.lower():
            #tools.addDir(name,play_url+id+'.'+ext,4,thumb,fanart,'')
            play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
        elif text not in name.lower() and text in name:
            #tools.addDir(name,play_url+id+'.'+ext,4,thumb,fanart,'')
            play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
    
def addonsettings(url,description):
    if   url =="CC":
        tools.clear_cache()
    elif url =="AS":
        xbmc.executebuiltin('Addon.OpenSettings(%s)'%addon_id)
    elif url =="ADS":
        dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','Enable Nvidia Shield AS','Disable AS'])
        if dialog==0:
            advancedsettings('stick')
            xbmcgui.Dialog().ok('SS TV', 'Set Advanced Settings')
        elif dialog==1:
            advancedsettings('firetv')
            xbmcgui.Dialog().ok('SS TV', 'Set Advanced Settings')
        elif dialog==2:
            advancedsettings('lessthan')
            xbmcgui.Dialog().ok('SS TV', 'Set Advanced Settings')
        elif dialog==3:
            advancedsettings('morethan')
            xbmcgui.Dialog().ok('SS TV', 'Set Advanced Settings')
        elif dialog==4:
            advancedsettings('shield')
            xbmcgui.Dialog().ok('SS TV', 'Set Advanced Settings')
        elif dialog==5:
            advancedsettings('remove')
            xbmcgui.Dialog().ok('SS TV', 'Advanced Settings Removed')
    elif url =="ADS2":
        dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','Nvidia Shield'])
        if dialog==0:
            advancedsettings('stick')
            xbmcgui.Dialog().ok('SS TV', 'Set Advanced Settings')
        elif dialog==1:
            advancedsettings('firetv')
            xbmcgui.Dialog().ok('SS TV', 'Set Advanced Settings')
        elif dialog==2:
            advancedsettings('lessthan')
            xbmcgui.Dialog().ok('SS TV', 'Set Advanced Settings')
        elif dialog==3:
            advancedsettings('morethan')
            xbmcgui.Dialog().ok('SS TV', 'Set Advanced Settings')
        elif dialog==4:
            advancedsettings('shield')
            xbmcgui.Dialog().ok('SS TV', 'Set Advanced Settings')
    elif url =="ST":
        try:
            xbmcaddon.Addon(id = 'script.speedtester')
            xbmc.executebuiltin('RunAddon("script.speedtester")')
        except:
            xbmc.executebuiltin('InstallAddon("script.speedtester")')
            xbmc.executebuiltin('RunAddon("script.speedtester")')
    elif url =="META":
        if 'ON' in description:
            xbmcaddon.Addon().setSetting('meta','false')
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmcaddon.Addon().setSetting('meta','true')
            xbmc.executebuiltin('Container.Refresh')
    elif url =="XXX":
        if 'ON' in description:
            xbmcaddon.Addon().setSetting('hidexxx','false')
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmcaddon.Addon().setSetting('hidexxx','true')
            xbmc.executebuiltin('Container.Refresh')
    elif url =="LO":
        xbmcaddon.Addon().setSetting('Username','')
        xbmcaddon.Addon().setSetting('Password','')
        xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)')
        xbmc.executebuiltin('Container.Refresh')
    elif url =="UPDATE":
        if 'ON' in description:
            xbmcaddon.Addon().setSetting('update','false')
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmcaddon.Addon().setSetting('update','true')
            xbmc.executebuiltin('Container.Refresh')
    
def all_movies():
    open = tools.OPEN_URL(panel_api)
    import json
    j = json.loads(open)
    available_channels = j["available_channels"]
    for id,channel in list(available_channels.items()):
        name = channel["name"] or ''
        type = channel["stream_type"] or ''
        ext = channel["container_extension"] or ''
        thumb = channel["stream_icon"] or ''
        fanart = ''
        liz=xbmcgui.ListItem(name)
        liz.setArt({ 'thumb': thumb, 'icon': thumb, 'fanart': ''}) 
        liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":'',})
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)

def advancedsettings(device):
    if device == 'stick':
        file = open(os.path.join(advanced_settings, 'stick.xml'))
    elif device == 'firetv':
        file = open(os.path.join(advanced_settings, 'firetv.xml'))
    elif device == 'lessthan':
        file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
    elif device == 'morethan':
        file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
    elif device == 'shield':
        file = open(os.path.join(advanced_settings, 'shield.xml'))
    elif device == 'remove':
        os.remove(advanced_settings_target)
    
    try:
        read = file.read()
        f = open(advanced_settings_target, mode='w+')
        f.write(read)
        f.close()
    except:
        pass
        
    
def asettings():
    choice = xbmcgui.Dialog().yesno('SS TV', 'Please Select The RAM Size of Your Device', yeslabel='Less than 1GB RAM', nolabel='More than 1GB RAM')
    if choice:
        lessthan()
    else:
        morethan()
    

def morethan():
        file = open(os.path.join(advanced_settings, 'morethan.xml'))
        a = file.read()
        f = open(advanced_settings_target, mode='w+')
        f.write(a)
        f.close()

        
def lessthan():
        file = open(os.path.join(advanced_settings, 'lessthan.xml'))
        a = file.read()
        f = open(advanced_settings_target, mode='w+')
        f.write(a)
        f.close()
        
        
def userpopup():
    kb =xbmc.Keyboard ('', 'heading', True)
    kb.setHeading('Enter Username')
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        text = kb.getText()
        return text
    else:
        return False

        
def passpopup():
    kb =xbmc.Keyboard ('', 'heading', True)
    kb.setHeading('Enter Password')
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        text = kb.getText()
        return text
    else:
        return False
        
        
def accountinfo():
    open = tools.OPEN_URL(panel_api)
    try:
        username   = tools.regex_from_to(open,'"username":"','"')
        password   = tools.regex_from_to(open,'"password":"','"')
        status     = tools.regex_from_to(open,'"status":"','"')
        connects   = tools.regex_from_to(open,'"max_connections":"','"')
        active     = tools.regex_from_to(open,'"active_cons":"','"')
        expiry     = tools.regex_from_to(open,'"exp_date":"','"')
        url        = tools.regex_from_to(open,'"url":"','"')
        expiry     = datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
        expreg     = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
        for day,month,year in expreg:
            month     = tools.MonthNumToName(month)
            year      = re.sub(' -.*?$','',year)
            expiry    = month+' '+day+' - '+year
            tools.addDir('[B][COLOR white]Account Status :[/COLOR][/B] %s'%status,'','',icon,fanart,'')
            tools.addDir('[B][COLOR white]Expiry Date:[/COLOR][/B] '+expiry,'','',icon,fanart,'')
            tools.addDir('[B][COLOR white]Username :[/COLOR][/B] '+username,'','',icon,fanart,'')
            tools.addDir('[B][COLOR white]Password :[/COLOR][/B] '+password,'','',icon,fanart,'')
            tools.addDir('[B][COLOR white]Allowed Connections:[/COLOR][/B] '+connects,'','',icon,fanart,'')
            tools.addDir('[B][COLOR white]Current Connections:[/COLOR][/B] '+ active,'','',icon,fanart,'')
            tools.addDir('[B][COLOR white]Current DNS:[/COLOR][/B] '+url,'','',icon,fanart,'')
    except:pass
        
    
def extras():
    if xbmcaddon.Addon().getSetting('meta')=='true':
        META = '[B][COLOR lime]ON[/COLOR][/B]'
    else:
        META = '[B][COLOR white]OFF[/COLOR][/B]'
    if xbmcaddon.Addon().getSetting('hidexxx')=='true':
        XXX = '[B][COLOR lime]ON[/COLOR][/B]'
    else:
        XXX = '[B][COLOR white]OFF[/COLOR][/B]'
    tools.addDir('Metadata is %s'%META,'META',10,icon,fanart,META)
    tools.addDir('Clear Cache','CC',10,icon,fanart,'')
    tools.addDir('Edit Advanced Settings','ADS',10,icon,fanart,'')
    tools.addDir('Run a Speed Test','ST',10,icon,fanart,'')    
    
params=tools.get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None

try:
    url=urllib_parse.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib_parse.unquote_plus(params["name"])
except:
    pass
try:
    iconimage=urllib_parse.unquote_plus(params["iconimage"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    description=urllib_parse.unquote_plus(params["description"])
except:
    pass
try:
    query=urllib_parse.unquote_plus(params["query"])
except:
    pass
try:
    type=urllib_parse.unquote_plus(params["type"])
except:
    pass

if mode==None or url==None or len(url)<1:
    start()

elif mode==1:
    livecategory(url)

elif mode==2:
    livelist(url)

elif mode==3:
    vod(url)
    
elif mode==333:
    all_movies()
    
elif mode==4:
    stream_video(url)

elif mode==5:
    search()

elif mode==6:
    accountinfo()

elif mode==7:
    tvguide()

elif mode==75:
    guideconf()

elif mode==9:
    xbmc.executebuiltin('ActivateWindow(busydialog)')
    tools.Trailer().play(url) 
    xbmc.executebuiltin('Dialog.Close(busydialog)')

elif mode==10:
    addonsettings(url,description)
    
elif mode==11:
    subm()

elif mode==12:
    subt()

elif mode==122:
    subg()

elif mode==13:
    catchup()

elif mode==14:
    tvarchive(name,description)
    
elif mode==15:
    listcatchup2()
    
elif mode==16:
    extras()

elif mode==17:
    shortlinks.Get()

elif mode==19:
    get()

elif mode==20:
    series(url)

elif mode==21:
    seasons(url)

elif mode==22:
    eps(url)

elif mode==24:
    scat(url)

elif mode==2424:
    search_scat(url)

elif mode==25:
    AS(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
