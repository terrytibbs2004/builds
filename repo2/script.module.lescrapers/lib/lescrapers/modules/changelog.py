# -*- coding: utf-8 -*-
"""
	LEscrapers Module
"""

from lescrapers.modules.control import addonPath, addonVersion, joinPath
from lescrapers.windows.textviewer import TextViewerXML
from lescrapers.modules import py_tools

if py_tools.isPY2:
	from io import open #py2 open() does not support encoding param

def get():
	lescrapers_path = addonPath()
	lescrapers_version = addonVersion()
	changelogfile = joinPath(lescrapers_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]LEScrapers -  v%s - ChangeLog[/B]' % lescrapers_version
	windows = TextViewerXML('textviewer.xml', lescrapers_path, heading=heading, text=text)
	windows.run()
	del windows