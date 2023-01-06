# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
from xbmcgui import ListItem
from kodi_six import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from routing import Plugin

import os
import time
from requests.exceptions import RequestException
from resources.lib.uktvnow import UKTVNow

try:
    from xbmcvfs import translatePath
except ImportError:
    from kodi_six.xbmc import translatePath

addon = xbmcaddon.Addon()
plugin = Plugin()
plugin.name = addon.getAddonInfo("name")
USER_DATA_DIR = translatePath(addon.getAddonInfo("profile"))
data_time = int(addon.getSetting("data_time") or "0")
cache_time = int(addon.getSetting("cache_time") or "0")
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)


def log(msg, level=xbmc.LOGDEBUG):
    xbmc.log("[{0}] {1}".format(plugin.name, msg), level=level)


TV = UKTVNow(USER_DATA_DIR)
current_time = int(time.time())
if current_time - data_time > cache_time * 60 * 60:
    try:
        TV.update_channels()
        addon.setSetting("data_time", str(current_time))
        log("[{0}] Channels updated".format(current_time))
    except (ValueError, RequestException) as e:
        if data_time == 0:
            """ No data """
            log(e.message)
            dialog = xbmcgui.Dialog()
            dialog.notification(plugin.name, repr(e.message), xbmcgui.NOTIFICATION_ERROR)
            xbmcplugin.endOfDirectory(plugin.handle, False)
        else:
            """ Data update failed """
            log("[{0}] Channels update fail, data age: {1}".format(current_time, data_time))
            log(e.message)


@plugin.route("/")
def root():
    list_items = []
    for cat in TV.get_categories():
        li = ListItem(cat.cat_name, offscreen=True)
        url = plugin.url_for(list_channels, cat_id=cat.cat_id)
        list_items.append((url, li, True))
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route("/list_channels/<cat_id>")
def list_channels(cat_id=None):
    list_items = []
    for channel in TV.get_channels_by_category(cat_id):
        title = "{0} - {1}".format(channel.country, channel.channel_name.rstrip(".,-"))
        image = TV.image_url(channel.img)
        li = ListItem(title, offscreen=True)
        li.setProperty("IsPlayable", "true")
        li.setArt({"thumb": image, "icon": image})
        li.setInfo(type="Video", infoLabels={"Title": title, "mediatype": "video"})
        url = plugin.url_for(play, pk_id=channel.pk_id)
        list_items.append((url, li, False))
    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.setContent(plugin.handle, "videos")
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route("/play/<pk_id>/play.pvr")
def play(pk_id):
    channel = TV.get_channel_by_id(pk_id)
    title = "{0} - {1}".format(channel.country, channel.channel_name.rstrip(".,-"))
    image = TV.image_url(channel.img)
    try:
        links = TV.get_channel_links(pk_id)
        if addon.getSetting("autoplay") == "true":
            link = links[0]
        elif len(links) > 1:
            dialog = xbmcgui.Dialog()
            ret = dialog.select("Choose Stream", links)
            link = links[ret]
        else:
            link = links[0]

        li = ListItem(title, path=link)
        li.setArt({"thumb": image, "icon": image})
        if "playlist.m3u8" in link:
            li.setContentLookup(False)
            li.setMimeType("application/vnd.apple.mpegurl")
            if addon.getSetting("inputstream") == "true":
                if sys.version_info[0] == 2:
                    li.setProperty("inputstreamaddon", "inputstream.adaptive")
                else:
                    li.setProperty("inputstream", "inputstream.adaptive")
                li.setProperty("inputstream.adaptive.manifest_type", "hls")
                li.setProperty("inputstream.adaptive.stream_headers", link.split("|")[-1])

        xbmcplugin.setResolvedUrl(plugin.handle, True, li)
    except (ValueError, RequestException) as e:
        log(e.message)
        dialog = xbmcgui.Dialog()
        dialog.notification(plugin.name, repr(e.message), xbmcgui.NOTIFICATION_ERROR)
        xbmcplugin.setResolvedUrl(plugin.handle, False, ListItem())


if __name__ == "__main__":
    plugin.run(sys.argv)
    del TV