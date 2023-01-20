# -*- coding: utf-8 -*-
"""
	LEscrapers Module
"""

from lescrapers.modules.control import addonPath, addonVersion, joinPath
from lescrapers.windows.textviewer import TextViewerXML
from lescrapers.modules import py_tools

if py_tools.isPY2:
	from io import open #py2 open() does not support encoding param

def get(file):
	lescrapers_path = addonPath()
	lescrapers_version = addonVersion()
	helpFile = joinPath(lescrapers_path, 'lib', 'lescrapers', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]LEScrapers -  v%s - %s[/B]' % (lescrapers_version, file)
	windows = TextViewerXML('textviewer.xml', lescrapers_path, heading=heading, text=text)
	windows.run()
	del windows