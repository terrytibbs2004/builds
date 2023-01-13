# -*- coding: utf-8 -*-
"""
	Your Accounts
"""

from youraccounts.modules.control import addonPath, addonVersion, joinPath
from youraccounts.windows.textviewer import TextViewerXML
from youraccounts.modules import py_tools

if py_tools.isPY2:
	from io import open #py2 open() does not support encoding param

def get():
	youraccounts_path = addonPath()
	youraccounts_version = addonVersion()
	changelogfile = joinPath(youraccounts_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Your Accounts -  v%s - ChangeLog[/B]' % youraccounts_version
	windows = TextViewerXML('textviewer.xml', youraccounts_path, heading=heading, text=text)
	windows.run()
	del windows