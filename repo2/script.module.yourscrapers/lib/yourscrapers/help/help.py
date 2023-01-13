# -*- coding: utf-8 -*-
"""
	Yourscrapers Module
"""

from yourscrapers.modules.control import addonPath, addonVersion, joinPath
from yourscrapers.windows.textviewer import TextViewerXML


def get(file):
	yourscrapers_path = addonPath()
	yourscrapers_version = addonVersion()
	helpFile = joinPath(yourscrapers_path, 'lib', 'yourscrapers', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]YourScrapers -  v%s - %s[/B]' % (yourscrapers_version, file)
	windows = TextViewerXML('textviewer.xml', yourscrapers_path, heading=heading, text=text)
	windows.run()
	del windows