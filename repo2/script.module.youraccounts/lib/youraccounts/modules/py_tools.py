# -*- coding: utf-8 -*-
"""
	Your Accounts
"""

from sys import version_info
# import types

isPY2 = version_info[0] == 2
isPY3 = version_info[0] == 3

if isPY2:
	class _C:
		def _m(self): pass
	ClassType = type(_C)
	range = xrange
	string_types = basestring,
	integer_types = (int, long)
	# class_types = (type, types.ClassType)
	class_types = (type, ClassType)
	text_type = unicode
	binary_type = str
	def iteritems(d, **kw):
		return d.iteritems(**kw)

elif isPY3:
	string_types = str,
	integer_types = int,
	class_types = type,
	text_type = str
	binary_type = bytes
	def iteritems(d, **kw):
		return iter(d.items(**kw))

def ensure_text(s, encoding='utf-8', errors='strict'):
	try:
		if isinstance(s, binary_type):
			return s.decode(encoding, errors)
		elif isinstance(s, text_type):
			return s
	except:
		from youraccounts.modules import log_utils
		log_utils.error()
		return s

def ensure_str(s, encoding='utf-8', errors='strict'):
	from youraccounts.modules import log_utils
	try:
		if not isinstance(s, (text_type, binary_type)):
			return log_utils.log("not expecting type '%s'" % type(s), __name__, log_utils.LOGDEBUG)
		if isPY2 and isinstance(s, text_type):
			s = s.encode(encoding, errors)
		elif isPY3 and isinstance(s, binary_type):
			s = s.decode(encoding, errors)
		return s
	except:
		log_utils.error()
		return s

def six_encode(txt, char='utf-8'):
	try:
		if isPY2 and isinstance(txt, text_type):
			txt = txt.encode(char)
		return txt
	except:
		from youraccounts.modules import log_utils
		log_utils.error()
		return txt

def six_decode(txt, char='utf-8'):
	try:
		if isPY3 and isinstance(txt, binary_type):
			txt = txt.decode(char)
		return txt
	except:
		from youraccounts.modules import log_utils
		log_utils.error()
		return txt