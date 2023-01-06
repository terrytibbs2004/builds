# -*- coding: utf-8 -*-
import glob, os, sys, sqlite3
import xbmc, xbmcaddon, xbmcvfs
from xbmc import log
from datetime import datetime
from xml.dom.minidom import parse

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
getsetting = addon.getSetting
setsetting = addon.setSetting
addoninfo = addon.getAddonInfo
addon_name = addoninfo('name')
addon_icon = addoninfo("icon")
translatePath = xbmcvfs.translatePath
home = translatePath('special://home/')
addons_path = os.path.join(home, 'addons/')
user_path = os.path.join(home, 'userdata/')
db_path = os.path.join(user_path, 'Database/')
addons_db = os.path.join(db_path,'Addons33.db')
installed_date = str(datetime.now())[:-7]

addon_xmls = []

def enable_addons():
	for name in glob.glob(os.path.join(addons_path,'*/addon.xml')):
		addon_xmls.append(name)
	addon_xmls.sort()
	addon_ids =[]
	for xml in addon_xmls:
		root = parse(xml)
		tag = root.documentElement
		_id = tag.getAttribute('id')
		addon_ids.append(_id)
	enabled=[]
	disabled=[]
	for x in addon_ids:
		try:
			xbmcaddon.Addon(id = x)
			enabled.append(x)
		except:
			disabled.append(x)
	for y in disabled:
		try:
			enable_db(y)
		except Exception as e:
			log('Failed to enable %s. Reason: %s' % (y, e), xbmc.LOGINFO)
		
	
def enable_db(d_addon):
    """ create a database connection to a SQLite database """
    conn = None
    conn = sqlite3.connect(addons_db)
    c = conn.cursor()
    try:
    	c.execute("SELECT id, addonID, enabled FROM installed WHERE addonID = ?", (d_addon,))
    	found = c.fetchone()
    	if found == None:
    		# Insert a row of data
    		c.execute('INSERT INTO installed (addonID , enabled, installDate) VALUES (?,?,?)', (d_addon, '1', installed_date,))
    	else:
    		c.execute('UPDATE installed SET enabled = ? WHERE addonID = ? ', (1, d_addon,))
    except Exception as e:
    	log('Failed to enable %s. Reason: %s' % (d_addon, e), xbmc.LOGINFO)
    conn.commit()
    conn.close()