import xbmc
import xbmcvfs
import xbmcgui
import xbmcaddon
import json
import time

ADDON_DATA = xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo("profile"))
PROGRESS_FILE = ADDON_DATA + "progress.json"


class Player(xbmc.Player):
    
    def __init__(self):
        xbmc.Player.__init__(self)
        self.progress = None
        self.info_tag = None
        self.title = None
        self.total_time = None
        
        if not xbmcvfs.exists(ADDON_DATA):
            xbmcvfs.mkdirs(ADDON_DATA)
        if not xbmcvfs.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "w", encoding="utf-8", errors="ignore") as f:
                json.dump({}, f)
        
    def onPlayBackStarted(self):
        pass
    
    def onPlayBackStopped(self):
        pass
    
    def onPlayBackEnded(self):
        pass
    
    def resume(self):
        xbmc.log("Player Resume Started", xbmc.LOGINFO)
        if self.await_video_playback():
            xbmc.log("Gratis Player: Video Playback Started", xbmc.LOGINFO)
        else:
            return
        self.set_attributes()
        if self.title is None:
            return
        try:
            if self.progress > 10:
                formatted_time = time.strftime('%H:%M:%S', time.gmtime(self.progress))
                self.pause()
                play_resume = xbmcgui.Dialog().yesno(xbmcaddon.Addon().getAddonInfo('name'), f"Would You Like to Resume Where You Left Off?\n{formatted_time}", nolabel="Start Over", yeslabel="Resume")
                if play_resume:
                    self.seekTime(self.progress - 5)
                xbmc.sleep(100)
                self.pause()
            self.track_progress()
            ended = False
            
            if self.total_time - 60 < self.progress:
                ended = True
            self.set_progress(ended)
        except RuntimeError as e:
            xbmc.log(f"Gratis Player Error: {e}", xbmc.LOGINFO)
            return
    
    def set_attributes(self):
        try:
            if self.isPlayingVideo():
                self.info_tag = self.getVideoInfoTag()
                self.title = self.info_tag.getTitle()
                self.progress = self.get_progress()
                self.total_time = self.getTotalTime()
        except RuntimeError as e:
            xbmc.log(f"Gratis Player Error: {e}", xbmc.LOGINFO)   
    
    def await_video_playback(self):
        for _ in range(1, 100):
            if not self.isPlayingVideo():
                xbmc.sleep(100)
            else:
                return True
        return False
    
    def track_progress(self):
        try:
            while self.isPlayingVideo():
                xbmc.sleep(1000)
                self.progress = self.getTime()   
        except RuntimeError:
            xbmc.log("Gratis Player: Playback has ended.", xbmc.LOGINFO)
    
    def get_progress(self):
        with open(PROGRESS_FILE, "r", encoding="utf-8", errors="ignore") as f:
            progress_json = json.load(f)
        if self.title in progress_json:
            return progress_json.get(self.title)
        return 0
    
    def set_progress(self, ended: bool = False):
        if ended:
            self.progress = 0
        with open (PROGRESS_FILE, "r", encoding="utf-8", errors="ignore") as f:
            progress_json = json.load(f)
        progress_json[f"{self.title}"] = self.progress
        with open(PROGRESS_FILE, "w", encoding="utf-8", errors="ignore") as f:
            json.dump(progress_json, f, indent=4)
    
    def play_video(self, title, link, iconimage, desc, title2):
        import resolveurl
        liz = xbmcgui.ListItem(title)
        liz.setInfo('video', {'title': title2, 'plot':desc})
        liz.setArt({'thumb': iconimage, 'icon': iconimage})
        if resolveurl.HostedMediaFile(link).valid_url():
            link = resolveurl.HostedMediaFile(link).resolve()
        self.play(link,liz)
        self.resume()