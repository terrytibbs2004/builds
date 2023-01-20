# -*- coding: utf-8 -*-
"""
	LEscrapers Module
"""

import re
from lescrapers.modules import py_tools


def get(title):
	try:
		if not title: return
		try: title = py_tools.ensure_str(title)
		except: pass
		title = re.sub(r'&#(\d+);', '', title).lower()
		title = re.sub(r'(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
		title = title.replace('&quot;', '\"').replace('&amp;', '&')
		title = re.sub(r'\n|([\[({].+?[})\]])|([:;–\-"\',!_.?~$@])|\s', '', title) # stop trying to remove alpha characters "vs" or "v", they're part of a title
		return title
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return title

def get_simple(title):
	try:
		if not title: return
		try: title = py_tools.ensure_str(title)
		except: pass
		title = re.sub(r'(\d{4})', '', title).lower()
		title = re.sub(r'&#(\d+);', '', title)
		title = re.sub(r'(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
		title = title.replace('&quot;', '\"').replace('&amp;', '&')
		title = re.sub(r'\n|[()[\]{}]|[:;–\-",\'!_.?~$@]|\s', '', title) # stop trying to remove alpha characters "vs" or "v", they're part of a title
		title = re.sub(r'<.*?>', '', title) # removes tags
		return title
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return title

def geturl(title):
	if not title: return
	try:
		try: title = py_tools.ensure_str(title)
		except: pass
		title = title.lower().rstrip()
		try: title = title.translate(None, ':*?"\'\.<>|&!,')
		except:
			try: title = title.translate(title.maketrans('', '', ':*?"\'\.<>|&!,'))
			except:
				for c in ':*?"\'\.<>|&!,': title = title.replace(c, '')
		title = title.replace('/', '-').replace(' ', '-').replace('--', '-').replace('–', '-').replace('!', '')
		return title
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return title

def normalize(title):
	try:
		import unicodedata
		title = ''.join(c for c in unicodedata.normalize('NFKD', py_tools.ensure_text(py_tools.ensure_str(title))) if unicodedata.category(c) != 'Mn')
		return str(title)
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return title