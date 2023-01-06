"""
    Returns the temp4late Movie list-

    <dir>
    <title>Star Wars Movies</title>
    <temp4_movie>movies</temp4_movie>
	<fanart></fanart>
	<thumbnail></thumbnail>
    </dir>


    ---------------------

    Possible Genre's are:
    Documentary
    Extras
	Movie
    Audio Books
    -----------------------

    Genre tag examples

    <dir>
    <title>Star Wars Movies</title>
    <temp4_movie>genre/Movie</temp4_movie>
	<fanart>http://ukodi1.com/images/G4xUAWx.jpg</fanart>
	<thumbnail>http://uk1.site/images/movie.png</thumbnail>
	<summary>All Star Wars Movies</summary>
    </dir>

    <dir>
    <title>Star Wars Documentaries</title>
    <temp4_movie>genre/Documentary</temp4_movie>
	<fanart>http://ukodi1.com/images/G4xUAWx.jpg</fanart>
	<thumbnail>http://uk1.site/images/doc's.png</thumbnail>
	<summary>Star Wars Docs</summary>
    </dir>    
	
	<dir>
    <title>Star Wars Extras</title>
    <temp4_movie>genre/Extras</temp4_movie>
	<fanart>http://ukodi1.com/images/G4xUAWx.jpg</fanart>
	<thumbnail>http://uk1.site/images/EXTRA.png</thumbnail>
	<summary>Extras & Fan Made</summary>
    </dir> 
	
	<dir>
    <title>Star Wars Audio Books</title>
    <temp4_movie>genre/Audio Books</temp4_movie>
	<fanart>http://ukodi1.com/images/G4xUAWx.jpg</fanart>
	<thumbnail>http://uk1.site/images/AUDIO.png</thumbnail>
	<summary>Audio Books</summary>
    </dir> 

    --------------------------------------------------------------

"""
from resources.modules import public
import logging,xbmcplugin,sys,base64,json
addDir3=public.addDir3
addLink=public.addLink
from  resources.modules.client import get_html
def run(url,lang,icon,fanart,plot,name):
    return addDir3(name,'temp4_movie',193,icon,fanart,plot,id=url)
        
def next_level(url,icon,fanart,plot,name,id):
    table_id = "apppxFvFzSNbUjBJn"
    table_name = "Star%20Wars"
    api_key = "keyFw4tAzBr8ximp0"
    
    genre = id.split("/")[-1]

    
    # App ID, Table ID, Max Results, Sort ID, View Mode, API Key
    headers={'Authorization': 'Bearer {}'.format(api_key)}
    import posixpath
    ur=posixpath.join('https://api.airtable.com/','v0', table_id,table_name)

    x=get_html(ur,headers=headers,verify=False).json()
    
    
    all_d=[]
    
    for field in x['records']:
        links=[]
        res = field['fields']   
        if genre.lower() not in res['type'].lower() and 'movies' not in id:
            continue
        name = res['name']
        name = (name).encode('ascii', errors='ignore').decode('ascii', errors='ignore')
        summary = res['summary']
        summary = (summary).encode('ascii', errors='ignore').decode('ascii', errors='ignore')
        fanart = res['fanart']
        thumbnail = res['thumbnail']
        
        if len(thumbnail)<2:
            thumbnail=icon
        if len(res['link1'])>2:
            links .append( res['link1'])
        if len(res['link2'])>2:
            links .append( res['link2'])
        if len(res['link3'])>2:
            links .append( res['link3'])
        if len(res['link4'])>2:
            links .append( res['link4'])
        if len(res['link5'])>2:
            links .append( res['link5'])
        if len(links)==0:
            continue
        if len(links)>1:
            f_link='$$$$'.join(links)
        else:
            f_link=links[0]
        
        aa=addLink(name,f_link,6,False,thumbnail,fanart,summary,original_title=name,place_control=True)
        all_d.append(aa)
    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_d,len(all_d))
    