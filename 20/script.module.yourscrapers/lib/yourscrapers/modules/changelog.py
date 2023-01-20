# -*- coding: utf-8 -*-
"""
	Yourscrapers Module
"""

from yourscrapers.modules.control import addonPath, addonVersion, joinPath
from yourscrapers.windows.textviewer import TextViewerXML


def get():
	yourscrapers_path = addonPath()
	yourscrapers_version = addonVersion()
	changelogfile = joinPath(yourscrapers_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]YourScrapers -  v%s - ChangeLog[/B]' % yourscrapers_version
	windows = TextViewerXML('textviewer.xml', yourscrapers_path, heading=heading, text=text)
	windows.run()
	del windows