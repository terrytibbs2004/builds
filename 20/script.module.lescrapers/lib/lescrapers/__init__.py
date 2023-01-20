# -*- coding: UTF-8 -*-

import os
from pkgutil import walk_packages
from lescrapers.modules.control import setting as getSetting

debug = getSetting('debug.enabled') == 'true'

def sources(specified_folders=None, ret_all=False):
	try:
		sourceDict = []
		sourceFolder = getScraperFolder()
		sourceFolderLocation = os.path.join(os.path.dirname(__file__), sourceFolder)
		sourceSubFolders = [x[1] for x in os.walk(sourceFolderLocation)][0]
		sourceSubFolders = [x for x in sourceSubFolders if  '__pycache__' not in x]
		if specified_folders:
			sourceSubFolders = specified_folders
		for i in sourceSubFolders:
			for loader, module_name, is_pkg in walk_packages([os.path.join(sourceFolderLocation, i)]):
				if is_pkg: continue
				if ret_all or enabledCheck(module_name):
					try:
						module = loader.find_module(module_name).load_module(module_name)
						sourceDict.append((module_name, module.source()))
					except Exception as e:
						if debug:
							from lescrapers.modules import log_utils
							log_utils.log('Error: Loading module: "%s": %s' % (module_name, e), level=log_utils.LOGWARNING)
		return sourceDict
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return []

def getScraperFolder():
	try:
		sourceSubFolders = [x[1] for x in os.walk(os.path.dirname(__file__))][0]
		return [i for i in sourceSubFolders if 'lescrapers' in i.lower()][0]
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return 'sources_lescrapers'

def enabledCheck(module_name):
	try:
		if getSetting('provider.' + module_name) == 'true': return True
		else: return False
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return True

def pack_sources():
	return ['7torrents', 'bitcq', 'bitlord', 'bt4g', 'btscene', 'extratorrent', 'glodls', 'idope', 'kickass2', 'limetorrents', 'magnetdl', 'piratebay', 'solidtorrents',
				'torrentapi', 'torrentdownload', 'torrentfunk', 'torrentgalaxy', 'torrentparadise', 'torrentproject2', 'torrentz2', 'yourbittorrent', 'zooqle']
# btdb removed 7-3-21
# glodls added 7-3-21
# extratorrent new proxy 11-4-21
# bitcq added 11-2-21