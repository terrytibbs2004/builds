# Kodi 19 Matrix Version by Rock. 2021 #

import cgi
import re
import os
try:
   import pickle as pickle
except:
   import pickle
import unicodedata
import urllib.request, urllib.parse, urllib.error
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
from urllib.parse import urlparse
    
class Addon:       
    def __init__(self, addon_id, argv=None):
        self.addon = xbmcaddon.Addon(id=addon_id)
        if argv:
            self.url = argv[0]
            self.handle = int(argv[1])
            self.queries = self.parse_query(argv[2][1:])
        

    def get_author(self):
        return self.addon.getAddonInfo('author')
            

    def get_changelog(self):    
        return self.addon.getAddonInfo('changelog')
            

    def get_description(self):
        return self.addon.getAddonInfo('description')
            

    def get_disclaimer(self):    
        return self.addon.getAddonInfo('disclaimer')
            

    def get_fanart(self):
        return self.addon.getAddonInfo('fanart')
            

    def get_icon(self):
        return self.addon.getAddonInfo('icon')
            

    def get_id(self):
        return self.addon.getAddonInfo('id')
            

    def get_name(self):    
        return self.addon.getAddonInfo('name')
            

    def get_path(self):
        return self.addon.getAddonInfo('path')
            

    def get_profile(self):    
        return xbmcvfs.translatePath(self.addon.getAddonInfo('profile'))
            

    def get_stars(self):    
        return self.addon.getAddonInfo('stars')
            

    def get_summary(self):    
        return self.addon.getAddonInfo('summary')
            

    def get_type(self):   
        return self.addon.getAddonInfo('type')
            

    def get_version(self):    
        return self.addon.getAddonInfo('version')
            

    def get_setting(self, setting):
        return self.addon.getSetting(setting)


    def set_setting(self, setting, value):
        self.addon.setSetting(id=setting, value=value)


    def get_string(self, string_id):
        return self.addon.getLocalizedString(string_id)   


    def parse_query(self, query, defaults={'mode': 'main'}):
        queries = urllib.parse.parse_qs(query)
        q = defaults
        for key, value in list(queries.items()):
            if len(value) == 1:
                q[key] = value[0]
            else:
                q[key] = value
        return q


    def build_plugin_url(self, queries):
        out_dict = {}
        for k, v in list(queries.items()):
            if isinstance(v, str):
                v = v.encode('utf8')
            elif isinstance(v, str):
                # Must be encoded in UTF-8
                v.decode('utf8')
            out_dict[k] = v
        return self.url + '?' + urllib.parse.urlencode(out_dict)


    def log(self, msg, level=xbmc.LOGINFO):
        #msg = unicodedata.normalize('NFKD', unicode(msg)).encode('ascii',
        #                                                         'ignore')
        xbmc.log('%s: %s' % (self.get_name(), msg), level)
        

    def log_error(self, msg):
        self.log(msg, xbmc.LOGERROR)    
        

    def log_debug(self, msg):
        self.log(msg, xbmc.LOGDEBUG)    


    def log_notice(self, msg):
        self.log(msg, xbmc.LOGNOTICE)    


    def show_ok_dialog(self, msg, title=None, is_error=False):
        if not title:
            title = self.get_name()
        log_msg = ' '.join(msg)
        
        while len(msg) < 3:
            msg.append('')
        
        if is_error:
            self.log_error(log_msg)
        else:
            self.log_notice(log_msg)
        
        xbmcgui.Dialog().ok(title, msg[0], msg[1], msg[2])


    def show_error_dialog(self, msg):
        self.show_ok_dialog(msg, 'Error: %s' % self.get_name(), True)


    def show_small_popup(self, title='', msg='', delay=5000, image=''):
        xbmc.executebuiltin('XBMC.Notification("%s","%s",%d,"%s")' %
                            (title, msg, delay, image))


    def show_countdown(self, time_to_wait, title='', text=''):
        
        dialog = xbmcgui.DialogProgress()
        ret = dialog.create(title)

        self.log_notice('waiting %d secs' % time_to_wait)
        
        secs = 0
        increment = 100 / time_to_wait

        cancelled = False
        while secs <= time_to_wait:

            if (dialog.iscanceled()):
                cancelled = True
                break

            if secs != 0: 
                xbmc.sleep(1000)

            secs_left = time_to_wait - secs
            if secs_left == 0: 
                percent = 100
            else: 
                percent = increment * secs
            
            remaining_display = ('Wait %d seconds for the ' +
                    'video stream to activate...') % secs_left
            dialog.update(percent, text, remaining_display)

            secs += 1

        if cancelled == True:     
            self.log_notice('countdown cancelled')
            return False
        else:
            self.log_debug('countdown finished waiting')
            return True        


    def show_settings(self):
        self.addon.openSettings()


    def resolve_url(self, stream_url):
        if stream_url:
            self.log_debug('resolved to: %s' % stream_url)
            xbmcplugin.setResolvedUrl(self.handle, True, 
                                      xbmcgui.ListItem(path=stream_url))
        else:
            self.show_error_dialog(['sorry, failed to resolve URL :('])
            xbmcplugin.setResolvedUrl(self.handle, False, xbmcgui.ListItem())

    
    def get_playlist(self, pl_type, new=False):
        pl = xbmc.PlayList(pl_type)
        if new:
            pl.clear()
        return pl
    
    
    def get_music_playlist(self, new=False):
        self.get_playlist(xbmc.PLAYLIST_MUSIC, new)
    

    def get_video_playlist(self, new=False):
        self.get_playlist(xbmc.PLAYLIST_VIDEO, new)


    def add_item(self, queries, infolabels, properties=None, contextmenu_items='', context_replace=False, img='',
                 fanart='', resolved=False, total_items=0, playlist=False, item_type='video', 
                 is_folder=False):
        infolabels = self.unescape_dict(infolabels)
        if not resolved:
            if not is_folder:
                queries['play'] = 'True'
            play = self.build_plugin_url(queries)
        else: 
            play = resolved
        listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, 
                                    thumbnailImage=img)
        listitem.setInfo(item_type, infolabels)
        listitem.setProperty('IsPlayable', 'true')
        listitem.setProperty('fanart_image', fanart)
        
        if properties:
            for prop in list(properties.items()):
                listitem.setProperty(prop[0], prop[1])

        if contextmenu_items:
            listitem.addContextMenuItems(contextmenu_items, replaceItems=context_replace)        
        if playlist is not False:
            self.log_debug('adding item: %s - %s to playlist' % \
                                                    (infolabels['title'], play))
            playlist.add(play, listitem)
        else:
            self.log_debug('adding item: %s - %s' % (infolabels['title'], play))
            xbmcplugin.addDirectoryItem(self.handle, play, listitem, 
                                        isFolder=is_folder, 
                                        totalItems=total_items)


    def add_video_item(self, queries, infolabels, properties=None, contextmenu_items='', context_replace=False,
                       img='', fanart='', resolved=False, total_items=0, playlist=False):
        self.add_item(queries, infolabels, properties, contextmenu_items, context_replace, img, fanart,
                      resolved, total_items, playlist, item_type='video')


    def add_music_item(self, queries, infolabels, properties=None, contextmenu_items='', context_replace=False,
                        img='', fanart='', resolved=False, total_items=0, playlist=False):
        self.add_item(queries, infolabels, properties, contextmenu_items, img, context_replace, fanart,
                      resolved, total_items, playlist, item_type='music')


    def add_directory(self, queries, infolabels, properties=None, contextmenu_items='', context_replace=False,
                       img='', fanart='', total_items=0, is_folder=True):
        self.add_item(queries, infolabels, properties, contextmenu_items, context_replace, img, fanart,
                      total_items=total_items, resolved=self.build_plugin_url(queries), 
                      is_folder=is_folder)

    def end_of_directory(self):
        xbmcplugin.endOfDirectory(self.handle)
        

    def _decode_callback(self, matches):
        id = matches.group(1)
        try:
            return chr(int(id))
        except:
            return id


    def decode(self, data):
        return re.sub("&#(\d+)(;|(?=\s))", self._decode_callback, data).strip()


    def unescape(self, text):
        try:
            text = self.decode(text)
            rep = {'&lt;': '<',
                   '&gt;': '>',
                   '&quot': '"',
                   '&rsquo;': '\'',
                   '&acute;': '\'',
                   }
            for s, r in list(rep.items()):
                text = text.replace(s, r)
            # this has to be last:
            text = text.replace("&amp;", "&")
        
        #we don't want to fiddle with non-string types
        except TypeError:
            pass

        return text
        

    def unescape_dict(self, d):
        out = {}
        for key, value in list(d.items()):
            out[key] = self.unescape(value)
        return out
    
    def save_data(self, filename, data):
        profile_path = self.get_profile()
        try:
            os.makedirs(profile_path)
        except:
            pass
        save_path = os.path.join(profile_path, filename)
        try:
            pickle.dump(data, open(save_path, 'wb'))
            return True
        except pickle.PickleError:
            return False
        
    def load_data(self,filename):
        profile_path = self.get_profile()
        load_path = os.path.join(profile_path, filename)
        print(profile_path)
        if not os.path.isfile(load_path):
            self.log_debug('%s does not exist' % load_path)
            return False
        try:
            data = pickle.load(open(load_path))
        except:
            return False
        return data
            
        

