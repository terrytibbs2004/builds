# -*- coding: utf-8 -*-
import re
import time

global global_var,stop_all#global
global_var=[]
stop_all=0
from  resources.modules.client import get_html
 
from resources.modules.general import clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,all_colors,base_header
from  resources.modules import cache
try:
    from resources.modules.general import Addon
except:
  import Addon
type=['movie','tv','torrent']

import urllib,logging,base64,json





color=all_colors[112]
def get_links(tv_movie,original_title,season_n,episode_n,season,episode,show_original_year,id):
    global global_var,stop_all
    all_links=[]
    
        

    if tv_movie=='movie':
        search_string=clean_name(original_title,1).replace(' ','+')+'+'+show_original_year
    else:
        search_string=clean_name(original_title,1).replace(' ','+')+'+s%se%s'%(season_n,episode_n)
        
    ur='https://torrz.techpeg.in/torrent?q=%s&cat=%s&inc_wout_cat=1'%(search_string,tv_movie)
    
    
   
    headers = {
    'User-Agent': 'okhttp/4.2.2',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    }
    if 1:
        
        y=get_html(ur,headers=headers,timeout=10).json()
        
        for results in y:
            
      
            
            if stop_all==1:
                break
            nam=results['name']
          
            o_size=results['size']
            try:
                size=float(o_size.replace('GB','').replace('MB','').replace(",",'').strip())
                if 'MB' in o_size:
                   size=size/1000
            except Exception as e:
                
                size=0
            lk=results['magnet']
            
            if '4k' in nam:
                  res='2160'
            elif '2160' in nam:
                  res='2160'
            elif '1080' in nam:
                      res='1080'
            elif '720' in nam:
                  res='720'
            elif '480' in nam:
                  res='480'
            elif '360' in nam:
                  res='360'
            else:
                  res='HD'
            max_size=int(Addon.getSetting("size_limit"))
            
            
            if (size)<max_size:
               
                all_links.append((nam,lk,str(size),res))

                global_var=all_links
    return global_var