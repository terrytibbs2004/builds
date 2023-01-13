# -*- coding: utf-8 -*-
"""
	LEscrapers Module
"""

from json import loads as jsloads
import re
from string import printable
from lescrapers.modules import cleantitle
from lescrapers.modules.control import homeWindow, setting as getSetting, setSetting


RES_4K = ['.4k', 'hd4k', '4khd', 'ultrahd', 'ultra.hd', '2160p', '216op', '2160i', 'hd2160', '2160hd'] # some idiots use "uhd.1080p" in their uploads, "uhd" now removed
RES_1080 = ['1080p', '1o8op', '1080i', 'hd1080', '1080hd'] # some idots using letter o vs. a zero
RES_720 = ['720p', '72op', '720i', 'hd720', '720hd']
SCR = ['dvdscr', 'screener', '.scr.', '.r5', '.r6']
CAM = ['1xbet', 'betwin', '.cam.', 'camrip', 'cam.rip', 'dvdcam', 'dvd.cam', 'dvdts', 'hdcam', '.hd.cam', '.hctc', '.hc.tc', '.hdtc',
			'.hd.tc', 'hdts', '.hd.ts', '.ts.', '.tc.', 'tsrip', 'telecine', 'telesync', 'tele.sync']

LANG = ['arabic', 'bgaudio', 'castellano', 'chinese', 'dutch', 'finnish', 'french', 'german', 'greek', 'italian', 'latino', 'polish', 'portuguese',
			  'russian', 'spanish', 'tamil', 'telugu', 'truefrench', 'truespanish', 'turkish', 'hebrew']
ABV_LANG = ['.zh.', '.zho.', '.chi.', '.chs.', '.nl.', '.nld.', '.dut,', '.fi.', '.fin.', '.fr.', '.fra.', '.fre.', '.de.', '.deu.', '.ger.', '.he.', '.heb.', '.hi.', '.hin.', '.it.', '.ita.',
						'.ja.', '.jpn.', '.ko.', '.kor.', '.pl.', '.pol.', '.pt.', '.por.', '.ru.', '.rus.', '.es.', '.spa.', '.sv.', '.swe.', '.tr.', '.tur.', '.uk.', '.ukr.', '.vi.', '.vie.']
DUBBED = ['dublado', 'dubbed', 'pldub']
SUBS = ['subita', 'subfrench', 'subspanish', 'subtitula', 'swesub', 'nl.subs']

UNDESIRABLES = ['400p.octopus', '720p.octopus', '1080p.octopus', 'alexfilm', 'amedia', 'baibako', 'bigsinema', 'bonus.disc', 'courage.bambey',
				'.cbr', '.cbz', 'coldfilm', 'dilnix', 'dutchreleaseteam', 'e.book.collection', 'empire.minutemen', 'eniahd', '.exe', 'exkinoray', 'extras.only',
				'gears.media', 'gearsmedia', 'gostfilm', 'hamsterstudio', 'hdrezka', 'hdtvrip', 'hurtom', 'idea.film', 'ideafilm', 'jaskier', 'kapatejl6', 'kb.1080p',
				'kb.720p', 'kb.400p', 'kerob', 'kinokopilka', 'kravec', 'kuraj.bambey', 'lakefilm', 'lostfilm', 'megapeer', 'minutemen.empire', 'newstudio',
				'omskbird', '.ost.', 'paravozik', 'profix.media', 'rifftrax', 'sample', 'soundtrack', 'subtitle.only', 'sunshinestudio', 'teaser', 'trailer', 'tumbler.studio',
				'tvshows', 'ultradox', 'viruseproject', 'vostfr', 'vo.stfr', 'web.dlrip', 'webdlrip', 'wish666', '.p.web.dl', '.d.web.dl']

season_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eigh', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
			'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twenty-one', 'twenty-two', 'twenty-three',
			'twenty-four', 'twenty-five']

season_ordinal_list = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth',
			'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth', 'twentieth', 'twenty-first',
			'twenty-second', 'twenty-third', 'twenty-fourth', 'twenty-fifth']

season_ordinal2_list = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th',
			'17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th']

season_dict = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eigh', '9': 'nine', '10': 'ten',
			'11': 'eleven', '12': 'twelve', '13': 'thirteen', '14': 'fourteen', '15': 'fifteen', '16': 'sixteen', '17': 'seventeen',
			'18': 'eighteen', '19': 'nineteen', '20': 'twenty', '21': 'twenty-one', '22': 'twenty-two', '23': 'twenty-three',
			'24': 'twenty-four', '25': 'twenty-five'}

season_ordinal_dict = {'1': 'first', '2': 'second', '3': 'third', '4': 'fourth', '5': 'fifth', '6': 'sixth', '7': 'seventh', '8': 'eighth', '9': 'ninth',
			'10': 'tenth', '11': 'eleventh', '12': 'twelfth', '13': 'thirteenth', '14': 'fourteenth', '15': 'fifteenth', '16': 'sixteenth',
			'17': 'seventeenth', '18': 'eighteenth', '19': 'nineteenth', '20': 'twentieth', '21': 'twenty-first', '22': 'twenty-second',
			'23': 'twenty-third', '24': 'twenty-fourth', '25': 'twenty-fifth'}

season_ordinal2_dict = {'1': '1st', '2': '2nd', '3': '3rd', '4': '4th', '5': '5th', '6': '6th', '7': '7th', '8': '8th', '9': '9th', '10': '10th',
			'11': '11th', '12': '12th', '13': '13th', '14': '14th', '15': '15th', '16': '16th', '17': '17th', '18': '18th', '19': '19th',
			'20': '20th', '21': '21st', '22': '22nd', '23': '23rd', '24': '24th', '25': '25th'}

def get_undesirables():
	undesirables = homeWindow.getProperty('le.undesirables')
	undesirables = list(set(undesirables.replace(' ', '').split(',')))
	return undesirables

def undesirablesSelect():
	from lescrapers.modules.control import multiselectDialog
	chosen = getSetting('undesirables.choice').replace(' ', '').split(',')
	try: preselect = [UNDESIRABLES.index(i) for i in chosen]
	except: preselect = [UNDESIRABLES.index(i) for i in UNDESIRABLES]
	choices = multiselectDialog(UNDESIRABLES, preselect=preselect)
	if not choices: return
	choices = [UNDESIRABLES[i] for i in choices]
	setSetting('undesirables.choice', ','.join(choices))

def get_qual(term):
	if any(i in term for i in SCR): return 'SCR'
	elif any(i in term for i in CAM): return 'CAM'
	elif any(i in term for i in RES_4K): return '4K'
	elif any(i in term for i in RES_1080): return '1080p'
	elif any(i in term for i in RES_720): return '720p'
	else: return 'SD'

def get_release_quality(release_info, release_link=None):
	try:
		quality = None ; info = []
		if release_info: quality = get_qual(release_info)
		if not quality:
			if release_link:
				release_link = release_link.lower()
				quality = get_qual(release_link)
				if not quality: quality = 'SD'
			else: quality = 'SD'
		return quality, info
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return 'SD', []

def aliases_to_array(aliases, filter=None):
	try:
		if all(isinstance(x, str) for x in aliases): return aliases
		if not filter: filter = []
		if isinstance(filter, str): filter = [filter]
		return [x.get('title') for x in aliases if not filter or x.get('country') in filter]
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return []

def check_title(title, aliases, release_title, hdlr, year, years=None):
	try: aliases = aliases_to_array(jsloads(aliases))
	except: aliases = None
	title_list = []
	if aliases:
		for item in aliases:
			try:
				alias = item.replace('!', '').replace('(', '').replace(')', '').replace('&', 'and').replace(year, '')
				# alias = re.sub(r'[^A-Za-z0-9\s\.-]+', '', alias)
				if years: # for movies only, scraper to pass None for episodes
					for i in years: alias = alias.replace(i, '')
				if alias in title_list: continue
				title_list.append(alias)
			except:
				from lescrapers.modules import log_utils
				log_utils.error()
	try:
		match = True
		title = title.replace('!', '').replace('(', '').replace(')', '').replace('&', 'and')
		# title = re.sub(r'[^A-Za-z0-9\s\.-]+', '', title)
		title_list.append(title)

		release_title = release_title_format(release_title) # converts to .lower()
		h = hdlr.lower()
		t = release_title.split(h)[0].replace(year, '').replace('(', '').replace(')', '').replace('&', 'and')
		if years:
			for i in years: t = t.split(i)[0]
		t = t.split('2160p')[0].split('4k')[0].split('1080p')[0].split('720p')[0]
		if all(cleantitle.get(i) != cleantitle.get(t) for i in title_list): match = False
		if years: # for movies only, scraper to pass None for episodes
				if not any(value in release_title for value in years): match = False
		else: 
			if h not in release_title: match = False
		return match
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return match

def remove_lang(release_info):
	if not release_info: return False
	try:
		if any(value in release_info for value in DUBBED): return True
		if any(value in release_info for value in SUBS): return True
		if homeWindow.getProperty('le.filter.undesirables') == 'true':
			undesirables = get_undesirables()
			if any(value in release_info for value in undesirables): return True
		if homeWindow.getProperty('le.filter.foreign.single.audio') == 'true':
			if any(value in release_info for value in LANG) and not any(value in release_info for value in ['.eng.', '.en.', 'english']): return True
			if any(value in release_info for value in ABV_LANG) and not any(value in release_info for value in ['.eng.', '.en.', 'english']): return True
		if release_info.endswith('.srt.') and not any(value in release_info for value in ['with.srt', '.avi', '.mkv', '.mp4']): return True
		return False
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return False

def single_checkPack(release_title, query):
	range_pattern = r'%s%s' % (query.lower(), '[-]\d{2}([-,.[({]|$)')
	if bool(re.search(range_pattern, release_title.lower())): return True
	else: return False

def filter_season_pack(show_title, aliases, year, season, release_title):
	try: aliases = aliases_to_array(jsloads(aliases))
	except: aliases = None
	title_list = []
	if aliases:
		for item in aliases:
			try:
				alias = item.replace('!', '').replace('(', '').replace(')', '').replace('&', 'and').replace(year, '')
				# alias = re.sub(r'[^A-Za-z0-9\s\.-]+', '', alias)
				if alias in title_list: continue
				title_list.append(alias)
			except:
				from lescrapers.modules import log_utils
				log_utils.error()
	try:
		show_title = show_title.replace('!', '').replace('(', '').replace(')', '').replace('&', 'and')
		# show_title = re.sub(r'[^A-Za-z0-9\s\.-]+', '', show_title)
		title_list.append(show_title)

		season_fill = season.zfill(2)
		season_check = '.s%s.' % season
		season_fill_check = '.s%s.' % season_fill
		season_full_check = '.season.%s.' % season
		season_full_check_ns = '.season%s.' % season
		season_full_fill_check = '.season.%s.' % season_fill
		season_full_fill_check_ns = '.season%s.' % season_fill

		string_list = [season_check, season_fill_check, season_full_check, season_full_check_ns, season_full_fill_check, season_full_fill_check_ns]
		split_list = [season_check, season_fill_check, '.' + season + '.season', 'total.season', 'season', 'the.complete', 'complete', year]

		release_title = release_title_format(release_title)
		t = release_title.replace('-', '.')
		for i in split_list:
			t = t.split(i)[0]
		if all(cleantitle.get(x) != cleantitle.get(t) for x in title_list):
			return False

# remove single episodes(returned in single ep scrape)
		episode_regex = [
				r's\d{1,3}e\d{1,3}',
				r's[0-3]{1}[0-9]{1}[.-]e\d{1,2}',
				r's\d{1,3}[.-]\d{1,3}e\d{1,3}',
				r'season[.-]?\d{1,3}[.-]?ep[.-]?\d{1,3}',
				r'season[.-]?\d{1,3}[.-]?episode[.-]?\d{1,3}']
		for item in episode_regex:
			if bool(re.search(item, release_title)):
				return False

# remove season ranges - returned in showPack scrape, plus non conforming season and specific crap
		rt = release_title.replace('-', '.')
		if any(i in rt for i in string_list):
			for item in [
				season_check.rstrip('.') + r'[.-]s([2-9]{1}|[1-3]{1}[0-9]{1})(?:[.-]|$)', # ex. ".s1-s9.", .s1-s39.
				season_fill_check.rstrip('.') + r'[.-]s\d{2}(?:[.-]|$)', # ".s01-s09.", .s01-s39.
				season_fill_check.rstrip('.') + r'[.-]\d{2}(?:[.-]|$)', # ".s01.09."
				r'\Ws\d{2}\W%s' % season_fill_check.lstrip('.'), # may need more reverse ranges
				season_full_check.rstrip('.') + r'[.-]to[.-]([2-9]{1}|[1-3]{1}[0-9]{1})(?:[.-]|$)', # ".season.1.to.9.", ".season.1.to.39"
				season_full_check.rstrip('.') + r'[.-]season[.-]([2-9]{1}|[1-3]{1}[0-9]{1})(?:[.-]|$)', # ".season.1.season.9.", ".season.1.season.39"
				season_full_check.rstrip('.') + r'[.-]([2-9]{1}|[1-3]{1}[0-9]{1})(?:[.-]|$)', # "season.1.9.", "season.1.39.
				season_full_check.rstrip('.') + r'[.-]\d{1}[.-]\d{1,2}(?:[.-]|$)', #  "season.1.9.09."
				season_full_check.rstrip('.') + r'[.-]\d{3}[.-](?:19|20)[0-9]{2}(?:[.-]|$)',# single season followed by 3 digit followed by 4 digit year ex."season.1.004.1971"
				season_full_fill_check.rstrip('.') + r'[.-]\d{3}[.-]\d{3}(?:[.-]|$)',# 2 digit season followed by 3 digit dash range ex."season.10.001-025."
				season_full_fill_check.rstrip('.') + r'[.-]season[.-]\d{2}(?:[.-]|$)' # 2 digit season followed by 2 digit season range ex."season.01-season.09."
					]:
				if bool(re.search(item, release_title)):
					return False
			return True
		return False
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return True

def filter_show_pack(show_title, aliases, imdb, year, season, release_title, total_seasons):
	try: aliases = aliases_to_array(jsloads(aliases))
	except: aliases = None
	title_list = []
	if aliases:
		for item in aliases:
			try:
				alias = item.replace('!', '').replace('(', '').replace(')', '').replace('&', 'and').replace(year, '')
				# alias = re.sub(r'[^A-Za-z0-9\s\.-]+', '', alias)
				if alias in title_list: continue
				title_list.append(alias)
			except:
				from lescrapers.modules import log_utils
				log_utils.error()
	try:
		show_title = show_title.replace('!', '').replace('(', '').replace(')', '').replace('&', 'and')
		# show_title = re.sub(r'[^A-Za-z0-9\s\.-]+', '', show_title)
		title_list.append(show_title)

		split_list = ['.all.seasons', 'seasons', 'season', 'the.complete', 'complete', 'all.torrent', 'total.series', 'tv.series', 'series', 'edited', 's1', 's01', year] #s1 or s01 used so show pack only kept that begin with 1
		release_title = release_title_format(release_title)
		t = release_title.replace('-', '.')
		for i in split_list:
			t = t.split(i)[0]
		if all(cleantitle.get(x) != cleantitle.get(t) for x in title_list):
			return False, 0

# remove single episodes(returned in single ep scrape)
		episode_regex = [
				r's\d{1,3}e\d{1,3}',
				r's[0-3]{1}[0-9]{1}[.-]e\d{1,2}',
				r's\d{1,3}[.-]\d{1,3}e\d{1,3}',
				r'season[.-]?\d{1,3}[.-]?ep[.-]?\d{1,3}',
				r'season[.-]?\d{1,3}[.-]?episode[.-]?\d{1,3}']
		for item in episode_regex:
			if bool(re.search(item, release_title)):
				return False, 0

# remove season ranges that do not begin at 1
		season_range_regex = [
				r'(?:season|seasons|s)[.-]?(?:0?[2-9]{1}|[1-3]{1}[0-9]{1})(?:[.-]?to[.-]?|[.-]?thru[.-]?|[.-])(?:season|seasons|s|)[.-]?(?:0?[3-9]{1}(?!\d{2}p)|[1-3]{1}[0-9]{1}(?!\d{2}p))'] # seasons.5-6, seasons5.to.6, seasons.5.thru.6, season.2-9.s02-s09.1080p
		for item in season_range_regex:
			if bool(re.search(item, release_title)):
				return False, 0

# remove single seasons - returned in seasonPack scrape
		season_regex = [
				r'season[.-]?([1-9]{1})[.-]0{1}\1[.-]?complete', # "season.1.01.complete" when 2nd number matches the fiirst group with leading 0
				r'season[.-]?([2-9]{1})[.-](?:[0-9]+)[.-]?complete', # "season.9.10.complete" when first number is >1 followed by 2 digit number
				r'season[.-]?\d{1,2}[.-]s\d{1,2}', # season.02.s02
				r'season[.-]?\d{1,2}[.-]complete', # season.02.complete
				r'season[.-]?\d{1,2}[.-]\d{3,4}p{0,1}', # "season.02.1080p" and no seperator "season02.1080p"
				r'season[.-]?\d{1,2}[.-](?!thru|to|\d{1,2}[.-])', # "season.02." or "season.1" not followed by "to", "thru", or another single or 2 digit number then a dot(which would be a range)
				r'season[.-]?\d{1,2}[.]?$', # end of line ex."season.1", "season.01", "season01" can also have trailing dot or end of line(dash would be a range)
				r'season[.-]?\d{1,2}[.-](?:19|20)[0-9]{2}', # single season followed by 4 digit year ex."season.1.1971", "season.01.1971", or "season01.1971"
				r'season[.-]?\d{1,2}[.-]\d{3}[.-]{1,2}(?:19|20)[0-9]{2}', # single season followed by 3 digits then 4 digit year ex."season.1.004.1971" or "season.01.004.1971" (comic book format)
				r'(?<!thru)(?<!to)(?<!\d{2})[.-]s\d{2}[.-]complete', # ".s01.complete" not preceded by "thru", "to", or 2 digit number
				r'(?<!thru)(?<!to)(?<!s\d{2})[.-]s\d{2}(?![.-]thru)(?![.-]to)(?![.-]s\d{2})(?![.-]\d{2})' # .s02. not preceded by "thru", "to", or "s01". Not followed by ".thru", ".to", ".s02", "-s02", ".02.", or "-02."
				]
		for item in season_regex:
			if bool(re.search(item, release_title)):
				return False, 0

# remove spelled out single seasons
		season_regex = []
		[season_regex.append(r'(complete[.-]%s[.-]season)' % x) for x in season_ordinal_list]
		[season_regex.append(r'(complete[.-]%s[.-]season)' % x) for x in season_ordinal2_list]
		[season_regex.append(r'(season[.-]%s)' % x) for x in season_list] 
		for item in season_regex:
			if bool(re.search(item, release_title)):
				return False, 0


# from here down we don't filter out, we set and pass "last_season" it covers for the range and addon can filter it so the db will have full valid showPacks.
# set last_season for range type ex "1.2.3.4" or "1.2.3.and.4" (dots or dashes)
		dot_release_title = release_title.replace('-', '.')
		dot_season_ranges = []
		all_seasons = '1'
		season_count = 2
		while season_count <= int(total_seasons):
			dot_season_ranges.append(all_seasons + '.and.%s' % str(season_count))
			all_seasons += '.%s' % str(season_count)
			dot_season_ranges.append(all_seasons)
			season_count += 1
		if any(i in dot_release_title for i in dot_season_ranges):
			keys = [i for i in dot_season_ranges if i in dot_release_title]
			last_season = int(keys[-1].split('.')[-1])
			return True, last_season



# "1.to.9" type range filter (dots or dashes)
		to_season_ranges = []
		start_season = '1'
		season_count = 2
		while season_count <= int(total_seasons):
			to_season_ranges.append(start_season + '.to.%s' % str(season_count))
			season_count += 1
		if any(i in dot_release_title for i in to_season_ranges):
			keys = [i for i in to_season_ranges if i in dot_release_title]
			last_season = int(keys[0].split('to.')[1])
			return True, last_season

# "1.thru.9" range filter (dots or dashes)
		thru_ranges = [i.replace('to', 'thru') for i in to_season_ranges]
		if any(i in dot_release_title for i in thru_ranges):
			keys = [i for i in thru_ranges if i in dot_release_title]
			last_season = int(keys[0].split('thru.')[1])
			return True, last_season

# "1-9" range filter
		dash_ranges = [i.replace('.to.', '-') for i in to_season_ranges]
		if any(i in release_title for i in dash_ranges):
			keys = [i for i in dash_ranges if i in release_title]
			last_season = int(keys[0].split('-')[1])
			return True, last_season

# "1~9" range filter
		tilde_ranges = [i.replace('.to.', '~') for i in to_season_ranges]
		if any(i in release_title for i in tilde_ranges):
			keys = [i for i in tilde_ranges if i in release_title]
			last_season = int(keys[0].split('~')[1])
			return True, last_season



# "01.to.09" 2 digit range filter (dots or dashes)
		to_season_ranges = []
		start_season = '01'
		season_count = 2
		while season_count <= int(total_seasons):
			to_season_ranges.append(start_season + '.to.%s' % '0' + str(season_count) if int(season_count) < 10 else start_season + '.to.%s' % str(season_count))
			season_count += 1
		if any(i in dot_release_title for i in to_season_ranges):
			keys = [i for i in to_season_ranges if i in dot_release_title]
			last_season = int(keys[0].split('to.')[1])
			return True, last_season

# "01.thru.09" 2 digit range filter (dots or dashes)
		thru_ranges = [i.replace('to', 'thru') for i in to_season_ranges]
		if any(i in dot_release_title for i in thru_ranges):
			keys = [i for i in thru_ranges if i in dot_release_title]
			last_season = int(keys[0].split('thru.')[1])
			return True, last_season

# "01-09" 2 digit range filtering
		dash_ranges = [i.replace('.to.', '-') for i in to_season_ranges]
		if any(i in release_title for i in dash_ranges):
			keys = [i for i in dash_ranges if i in release_title]
			last_season = int(keys[0].split('-')[1])
			return True, last_season

# "01~09" 2 digit range filtering
		tilde_ranges = [i.replace('.to.', '~') for i in to_season_ranges]
		if any(i in release_title for i in tilde_ranges):
			keys = [i for i in tilde_ranges if i in release_title]
			last_season = int(keys[0].split('~')[1])
			return True, last_season



# "s1.to.s9" single digit range filter (dots or dashes)
		to_season_ranges = []
		start_season = 's1'
		season_count = 2
		while season_count <= int(total_seasons):
			to_season_ranges.append(start_season + '.to.s%s' % str(season_count))
			season_count += 1
		if any(i in dot_release_title for i in to_season_ranges):
			keys = [i for i in to_season_ranges if i in dot_release_title]
			last_season = int(keys[0].split('to.s')[1])
			return True, last_season

# "s1.thru.s9" single digit range filter (dots or dashes)
		thru_ranges = [i.replace('to', 'thru') for i in to_season_ranges]
		if any(i in dot_release_title for i in thru_ranges):
			keys = [i for i in thru_ranges if i in dot_release_title]
			last_season = int(keys[0].split('thru.s')[1])
			return True, last_season

# "s1-s9" single digit range filtering (dashes)
		dash_ranges = [i.replace('.to.', '-') for i in to_season_ranges]
		if any(i in release_title for i in dash_ranges):
			keys = [i for i in dash_ranges if i in release_title]
			last_season = int(keys[0].split('-s')[1])
			return True, last_season

# "s1~s9" single digit range filtering (dashes)
		tilde_ranges = [i.replace('.to.', '~') for i in to_season_ranges]
		if any(i in release_title for i in tilde_ranges):
			keys = [i for i in tilde_ranges if i in release_title]
			last_season = int(keys[0].split('~s')[1])
			return True, last_season



# "s01.to.s09"  2 digit range filter (dots or dash)
		to_season_ranges = []
		start_season = 's01'
		season_count = 2
		while season_count <= int(total_seasons):
			to_season_ranges.append(start_season + '.to.s%s' % '0' + str(season_count) if int(season_count) < 10 else start_season + '.to.s%s' % str(season_count))
			season_count += 1
		if any(i in dot_release_title for i in to_season_ranges):
			keys = [i for i in to_season_ranges if i in dot_release_title]
			last_season = int(keys[0].split('to.s')[1])
			return True, last_season

# "s01.thru.s09" 2 digit  range filter (dots or dashes)
		thru_ranges = [i.replace('to', 'thru') for i in to_season_ranges]
		if any(i in dot_release_title for i in thru_ranges):
			keys = [i for i in thru_ranges if i in dot_release_title]
			last_season = int(keys[0].split('thru.s')[1])
			return True, last_season

# "s01-s09" 2 digit  range filtering (dashes)
		dash_ranges = [i.replace('.to.', '-') for i in to_season_ranges]
		if any(i in release_title for i in dash_ranges):
			keys = [i for i in dash_ranges if i in release_title]
			last_season = int(keys[0].split('-s')[1])
			return True, last_season

# "s01~s09" 2 digit  range filtering (dashes)
		tilde_ranges = [i.replace('.to.', '~') for i in to_season_ranges]
		if any(i in release_title for i in tilde_ranges):
			keys = [i for i in tilde_ranges if i in release_title]
			last_season = int(keys[0].split('~s')[1])
			return True, last_season

# "s01.s09" 2 digit  range filtering (dots)
		dot_ranges = [i.replace('.to.', '.') for i in to_season_ranges]
		if any(i in release_title for i in dot_ranges):
			keys = [i for i in dot_ranges if i in release_title]
			last_season = int(keys[0].split('.s')[1])
			return True, last_season

		return True, total_seasons
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		# return True, total_seasons

def info_from_name(release_title, title, year, hdlr=None, episode_title=None, season=None, pack=None):
	try:
		release_title = release_title.lower().replace('&', 'and').replace("'", "")
		release_title = re.sub(r'[^a-z0-9]+', '.', release_title)
		title = title.lower().replace('&', 'and').replace("'", "")
		title = re.sub(r'[^a-z0-9]+', '.', title)
		name_info = release_title.replace(title, '').replace(year, '')
		if hdlr: name_info = name_info.replace(hdlr.lower(), '')
		if episode_title:
			episode_title = episode_title.lower().replace('&', 'and').replace("'", "")
			episode_title = re.sub(r'[^a-z0-9]+', '.', episode_title)
			name_info = name_info.replace(episode_title, '')
		if pack:
			if pack == 'season':
				season_fill = season.zfill(2)
				str1_replace = ['.s%s' % season, '.s%s' % season_fill, '.season.%s' % season, '.season%s' % season, '.season.%s' % season_fill, '.season%s' % season_fill, 'complete']
				for i in str1_replace: name_info = name_info.replace(i, '')
			elif pack == 'show':
				str2_replace = ['.all.seasons', 'seasons', 'season', 'the.complete', 'complete', 'all.torrent', 'total.series', 'tv.series', 'series', 'edited', 's1', 's01']
				for i in str2_replace: name_info = name_info.replace(i, '')
		name_info = name_info.lstrip('.').rstrip('.')
		name_info = '.%s.' % name_info
		return name_info
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return release_title

def release_title_format(release_title):
	try:
		release_title = release_title.lower().replace("'", "").lstrip('.').rstrip('.')
		fmt = '.%s.' % re.sub(r'[^a-z0-9-~]+', '.', release_title).replace('.-.', '-').replace('-.', '-').replace('.-', '-').replace('--', '-')
		return fmt
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return release_title

def clean_name(release_title):
	try:
		unwanted = [
							'[.www.tamilrockers.com.]', 'tamilrockers.com', 'www.tamilrockers.com', 'www.tamilrockers.ws', 'www.tamilrockers.pl', 'www.tamilrockerrs.pl',
							'[.www.torrenting.com.]', 'www.torrenting.com', 'www.torrenting.org', 'www-torrenting-com', 'www-torrenting-org',
							'[katmoviehd.eu]', '[katmoviehd.to]', '[katmoviehd.tv]', '+katmoviehd.pw+', 'katmoviehd-pw',
							'[.www.torrent9.uno.]', '[www.torrent9.ph.]', 'www.torrent9.nz', '[.torrent9.tv.]', '[.torrent9.cz.]', '[ torrent9.cz ]', 'torrent9-cz-.-', 'torrent9.cz.].', 'torrent9-cz-]-',
							'[agusiq.torrents.pl]', '[agusiq-torrents.pl]', 'agusiq-torrents-pl',
							'[.oxtorrent.com.]', '[oxtorrent-com]', 'oxtorrent-com',
							'[movcr.com]', 'www.movcr.tv', 'movcr-com', 'www.movcr.to',
							'[ex-torrenty.org]', '[xtorrenty.org]', 'xtorrenty.org',
							'[acesse.]', '[acesse-hd-elite-me]', '[acesse.hd-elite.me].',
							'[torrentcouch.net]', '[torrentcouch-net]',
							'[.www.cpasbien.cm.]', '[.www.cpasbien.pw.]',
							'[auratorrent.pl].nastoletni.wilkoak', '[auratorrent.pl]',
							'[.www.nextorrent.site.]', '[nextorrent.net]',
							'[www.scenetime.com]', 'www.scenetime.com',
							'[kst.vn]', 'kst-vn',
							'[itfriend]', '[itf]',
							'(imax)', '.imax.',
							'www.2movierulz.ac', 'www.2movierulz.ms',
							'www.3movierulz.com', 'www.3movierulz.tv', 'www.8movierulz.ws',
							'[zooqle.com]', '[horriblesubs]', '[gktorrent.com]', '[.www.omgtorrent.com.]', '[3d.hentai]', '[dark.media]', '[devil-torrents.pl]', 'mkvcinemas.live',
							'[filetracker.pl]', 'www.bludv.tv', 'ramin.djawadi', '[prof]', '[reup]', '[.www.speed.cd.]', '[-bde4.com]', 'extramovies.casa',
							'[ah]', '[ul]', '+13.+', 'taht.oyunlar', 'crazy4tv.com', '[tv]', '[noobsubs]', '[.freecourseweb.com.]', 'karibu', '989pa.com', '[aletorrenty.pl]',
							'best-torrents-net', '[.www.torrentday.com.]', '1-3-3-8.com', 'ssrmovies.club', 'www.tamilmv.bid', 'www.1tamilmv.org', '[h3h2.com]']
		if release_title.lower().startswith('rifftrax'): return release_title # removed by "undesirables" anyway so exit
		release_title = strip_non_ascii_and_unprintable(release_title).lstrip('/ ').replace(' ', '.')
		for i in unwanted:
			if release_title.lower().startswith(i):
				pattern = r'\%s' % i if i.startswith('[') or i.startswith('+') else r'%s' % i
				release_title = re.sub(r'^%s' % pattern, '', release_title, 1, re.I)
		release_title = release_title.lstrip(' 4.-[](){}:/')
		return release_title
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return release_title

def strip_non_ascii_and_unprintable(text):
	try:
		result = ''.join(char for char in text if char in printable)
		return result.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return text

def _size(siz):
	try:
		if siz in ['0', 0, '', None]: return 0, ''
		div = 1 if siz.lower().endswith(('gb', 'gib')) else 1024
		# if ',' in siz and siz.lower().endswith(('mb', 'mib')): siz = size.replace(',', '')
		# elif ',' in siz and siz.lower().endswith(('gb', 'gib')): siz = size.replace(',', '.')
		dec_count = len(re.findall(r'[.]', siz))
		if dec_count == 2: siz = siz.replace('.', ',', 1) # torrentproject2 likes to randomly use 2 decimals vs. a comma then a decimal
		float_size = float(re.sub(r'[^0-9|/.|/,]', '', siz.replace(',', ''))) / div #comma issue where 2,750 MB or 2,75 GB (sometimes replace with "." and sometimes not)
		str_size = '%.2f GB' % float_size
		return float_size, str_size
	except:
		from lescrapers.modules import log_utils
		log_utils.error('failed on siz=%s' % siz)
		return 0, ''

def convert_size(size_bytes, to='GB'):
	try:
		import math
		if size_bytes == 0: return 0, ''
		power = {'B' : 0, 'KB': 1, 'MB' : 2, 'GB': 3, 'TB' : 4, 'EB' : 5, 'ZB' : 6, 'YB': 7}
		i = power[to]
		p = math.pow(1024, i)
		float_size = round(size_bytes / p, 2)
		# if to == 'B' or to  == 'KB': return 0, ''
		str_size = "%s %s" % (float_size, to)
		return float_size, str_size
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return 0, ''

def scraper_error(provider):
	import traceback
	from lescrapers.modules import log_utils
	failure = traceback.format_exc()
	log_utils.log(provider.upper() + ' - Exception: \n' + str(failure), caller='scraper_error', level=log_utils.LOGERROR)

def is_host_valid(url, domains):
	try:
		# ('.rar', '.zip', '.iso', '.part', '.png', '.jpg', '.bmp', '.gif') # possibly consider adding
		if any(x in url.lower() for x in ['.rar.', '.zip.', '.iso.', '.sample.']) or any(url.lower().endswith(x) for x in ['.rar', '.zip', '.iso', '.sample']):
			return False, ''
		host = __top_domain(url)
		hosts = [domain.lower() for domain in domains if host and host in domain.lower()]
		if hosts and '.' not in host: host = hosts[0]
		if hosts and any([h for h in ['google', 'picasa', 'blogspot'] if h in host]): host = 'gvideo'
		if hosts and any([h for h in ['akamaized', 'ocloud'] if h in host]): host = 'CDN'
		return any(hosts), host
	except:
		from lescrapers.modules import log_utils
		log_utils.error()
		return False, ''

def __top_domain(url):
	try: #Py2
		from urlparse import urlparse
	except ImportError: #Py3
		from urllib.parse import urlparse
	try:
		elements = urlparse(url)
		domain = elements.netloc or elements.path
		domain = domain.split('@')[-1].split(':')[0]
		regex = r"(?:www\.)?([\w\-]*\.[\w\-]{2,3}(?:\.[\w\-]{2,3})?)$"
		res = re.search(regex, domain)
		if res: domain = res.group(1)
		domain = domain.lower()
		return domain
	except:
		from lescrapers.modules import log_utils
		log_utils.error()

def copy2clip(txt):
	from sys import platform as sys_platform
	platform = sys_platform
	if platform == "win32":
		try:
			from subprocess import check_call
			# cmd = "echo " + txt.strip() + "|clip"
			cmd = "echo " + txt.replace('&', '^&').strip() + "|clip" # "&" is a command seperator
			return check_call(cmd, shell=True)
		except:
			from lescrapers.modules import log_utils
			log_utils.error('Windows: Failure to copy to clipboard')
	elif platform == "darwin":
		try:
			from subprocess import check_call
			cmd = "echo " + txt.strip() + "|pbcopy"
			return check_call(cmd, shell=True)
		except:
			from lescrapers.modules import log_utils
			log_utils.error('Mac: Failure to copy to clipboard')
	elif platform == "linux":
		try:
			from subprocess import Popen, PIPE
			p = Popen(["xsel", "-pi"], stdin=PIPE)
			p.communicate(input=txt)
		except:
			from lescrapers.modules import log_utils
			log_utils.error('Linux: Failure to copy to clipboard')