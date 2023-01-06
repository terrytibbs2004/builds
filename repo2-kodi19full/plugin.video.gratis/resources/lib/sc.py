import requests
import datetime
import re
from bs4 import BeautifulSoup as bs
from base64 import b64decode
from .plugin import Myaddon


base_url = 'https://soccercatch.com'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
headers = {"User-Agent":user_agent, "Connection":'keep-alive', 'Accept':'audio/webm,audio/ogg,udio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5', 'Referer': base_url}

homepage = requests.get(base_url, headers=headers).text
p = Myaddon()

def date_url(date):
    return f'{base_url}/api/matches/date?date={date}'

def date_post(url):
    return requests.post(url, headers=headers).text

def get_dates():
    dates = []
    d = datetime.date(2021,1,18)
    while d <= datetime.date.today():
        dates.append([datetime.datetime.strftime(d,'%A, %B %d, %Y'), datetime.datetime.strftime(d,'%d-%m-%Y')])
        d += datetime.timedelta(days=1)
    return list(reversed(dates))

def main(icon):
    dates = get_dates()
    for name, number in dates:
        url = date_url(number)
        p.add_dir(name, url, 'soccer_matches', icon, p.addon_fanart, '')

def matches(url):
    r = date_post(url)
    soup = (bs(r, 'html.parser'))
    matches = soup.find_all('a', class_='match-list-content')
    for match in matches:
        url = f"{base_url}{match['href']}"
        home = match.find(class_='match-list-home')
        away = match.find(class_='match-list-away')
        home_name = home.img['alt']
        home_icon = home.img['src']
        away_name = away.img['alt']
        away_icon = away.img['src']
        name = f'{home_name} vs {away_name}'
        p.add_dir(name, url, 'soccer_get_links', home_icon, away_icon, name)

def get_links(name, url, icon, fanart):
    r = requests.get(url, headers=headers).text
    soup = bs(r, 'html.parser')
    highlights = soup.find_all(class_='iframe-responsive')
    url = re.findall(' src="(.+?)"| src=\'(.+?)\'', str(highlights))
    highlight_links = []
    for url1, url2 in url:
        if url1 != '':
            highlight_links.append(url1)
        if url2 != '':
            highlight_links.append(url2)
    if len(highlight_links) > 0:
        for link in highlight_links:
            index = 0
            if 'youtube' in link:
                yt_id = link.split('/')[-1]
                yt_link = f'plugin://plugin.video.youtube/play/?video_id={yt_id}'
                p.add_dir(f'{name} - Highlights', yt_link, 'play_video2', icon, fanart, f'{name} - Highlights', isFolder=False)
            if 'fmatchsand' in link:
                r = requests.get(link, headers=headers).text
                hls = re.findall("src:{hls:'(.+?)'}", r)[0]
                m3u = f'http:{hls}'
                p.add_dir(f'{name} - Highlights', m3u, 'play_video', icon, fanart, f'{name} - Highlights', name2=name, hls=True, isFolder=False)
            index += 1
    fullmatch = soup.find_all(class_='code-block')
    links = []
    for match in fullmatch:
        if 'Pre-Match'.lower() in str(match).lower():
            title = f'{name} - Pre Match'
        elif 'First-Half'.lower() in str(match).lower():
            title = f'{name} - First Half'
        elif 'Second-Half'.lower() in str(match).lower():
            title = f'{name} - Second Half'
        elif 'Post-Match'.lower() in str(match).lower():
            title = f'{name} - Post Match'
        else:
            title = f'{name} - Full Match'
        url = re.findall('data-url="(.+?)"', str(match))[0]
        url = b64decode(url).decode('utf-8').rstrip('.html')
        if not url in links:
            links.append([title, url])
    if len(links) > 0:
        for title, link in links:
            p.add_dir(f"{title} - {link.split('/')[2]}", link, 'play_video', icon, fanart, f"{title} - {link.split('/')[2]}", name2=title, isFolder=False)