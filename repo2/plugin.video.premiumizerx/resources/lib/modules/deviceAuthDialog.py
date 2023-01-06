import xbmcgui
import time
import xbmcaddon
import logging

__addon__ = xbmcaddon.Addon("plugin.video.premiumizerx")

addon = xbmcaddon.Addon()


LATER_BUTTON = 201
NEVER_BUTTON = 202
ACTION_PREVIOUS_MENU = 10
ACTION_BACK = 92
INSTRUCTION_LABEL = 203
AUTHCODE_LABEL = 204
WARNING_LABEL = 205
CENTER_Y = 6
CENTER_X = 2

logger = logging.getLogger(__name__)

def setSetting(setting, value):
    __addon__.setSetting(setting, str(value))
    
def getString(string_id):
    return __addon__.getLocalizedString(string_id).encode('utf-8', 'ignore')

def notification(header, message, time=5000, icon=__addon__.getAddonInfo('icon')):
    xbmc.executebuiltin("XBMC.Notification(%s,%s,%i,%s)" % (header, message, time, icon))

class DeviceAuthDialog(xbmcgui.WindowXMLDialog):

    def __init__(self, xmlFile, resourcePath, code, url):
        self.code = code
        self.url = url

    def onInit(self):
        instuction = self.getControl(INSTRUCTION_LABEL)
        authcode = self.getControl(AUTHCODE_LABEL)
        warning = self.getControl(WARNING_LABEL)
        instuction.setLabel(addon.getLocalizedString(32159).format("[COLOR red]" + self.url + "[/COLOR]"))
        authcode.setLabel(self.code)
        warning.setLabel(addon.getLocalizedString(32162))

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
            self.close()

    def onControl(self, control):
        pass

    def onFocus(self, control):
        pass

    def onClick(self, control):
        logger.debug('onClick: %s' % (control))

        if control == LATER_BUTTON:
            import webbrowser
            link = 'https://www.premiumize.me/ref/947927388'
            webbrowser.open(link, autoraise = True, new = 2)            

        if control == NEVER_BUTTON:
            from resources.lib.modules import control as AddonControl
            AddonControl.openSettings('0.0')

        if control in [LATER_BUTTON, NEVER_BUTTON]:
            self.close()
            
class DonationDialog(xbmcgui.WindowXMLDialog):

    def __init__(self, xmlFile, resourcePath, code, url):
        self.code = code
        self.url = url

    def onInit(self):
        warning = self.getControl(WARNING_LABEL)

    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
            self.close()

    def onControl(self, control):
        pass

    def onFocus(self, control):
        pass

    def onClick(self, control):
        logger.debug('onClick: %s' % (control))

        if control == LATER_BUTTON:
            import webbrowser
            link = ''
            webbrowser.open(link, autoraise = True, new = 2)            

        if control in [LATER_BUTTON, NEVER_BUTTON]:
            self.close()
