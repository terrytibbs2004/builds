# Kodi 19 Matrix Version by Rock. 2021 #

import http.cookiejar
import gzip
import re
import io
import urllib.request, urllib.parse, urllib.error
import xbmcvfs
import socket

socket.setdefaulttimeout(60)

class HeadRequest(urllib.request.Request):
    def get_method(self):
        return 'HEAD'

class Net:  
    _cj = http.cookiejar.LWPCookieJar()
    _proxy = None
    _user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 ' + \
                  '(KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'
    _http_debug = False
    
    
    def __init__(self, cookie_file='', proxy='', user_agent='', 
                 http_debug=False):
        if cookie_file:
            self.set_cookies(cookie_file)
        if proxy:
            self.set_proxy(proxy)
        if user_agent:
            self.set_user_agent(user_agent)
        self._http_debug = http_debug
        self._update_opener()
        
    
    def set_cookies(self, cookie_file):
        try:
            self._cj.load(cookie_file, ignore_discard=True)
            self._update_opener()
            return True
        except:
            return False
        
    
    def get_cookies(self):
        return self._cj._cookies


    def save_cookies(self, cookie_file):
        self._cj.save(cookie_file, ignore_discard=True)        

        
    def set_proxy(self, proxy):
        self._proxy = proxy
        self._update_opener()

        
    def get_proxy(self):
        return self._proxy
        
        
    def set_user_agent(self, user_agent):
        self._user_agent = user_agent

        
    def get_user_agent(self):
        return self._user_agent


    def _update_opener(self):
        if self._http_debug:
            http = urllib.request.HTTPHandler(debuglevel=1)
        else:
            http = urllib.request.HTTPHandler()
            
        if self._proxy:
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self._cj),
                                          urllib.request.ProxyHandler({'http': 
                                                                self._proxy}), 
                                          urllib.request.HTTPBasicAuthHandler(),
                                          http)
        
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self._cj),
                                          urllib.request.HTTPBasicAuthHandler(),
                                          http)
        urllib.request.install_opener(opener)
        

    def http_GET(self, url, headers={}, compression=True):
        return self._fetch(url, headers=headers, compression=compression)
        

    def http_POST(self, url, form_data, headers={}, compression=True):
        return self._fetch(url, form_data, headers=headers,
                           compression=compression)

    
    def http_HEAD(self, url, headers={}):
        req = HeadRequest(url)
        req.add_header('User-Agent', self._user_agent)
        for k, v in list(headers.items()):
            req.add_header(k, v)
        response = urllib.request.urlopen(req)
        return HttpResponse(response)


    def _fetch(self, url, form_data={}, headers={}, compression=True):
        encoding = ''
        req = urllib.request.Request(url)
        if form_data:
            form_data = urllib.parse.urlencode(form_data)
            req = urllib.request.Request(url, form_data)
        req.add_header('User-Agent', self._user_agent)
        for k, v in list(headers.items()):
            req.add_header(k, v)
        if compression:
            req.add_header('Accept-Encoding', 'gzip')
        response = urllib.request.urlopen(req)
        return HttpResponse(response)



class HttpResponse:
    
    content = ''
    
    
    def __init__(self, response):
        self._response = response
        html = response.read()
        try:
            if response.headers['content-encoding'].lower() == 'gzip':
                html = gzip.GzipFile(fileobj=io.StringIO(html)).read()
        except:
            pass
        
        try:
            content_type = response.headers['content-type']
            if 'charset=' in content_type:
                encoding = content_type.split('charset=')[-1]
        except:
            pass

        r = re.search('<meta\s+http-equiv="Content-Type"\s+content="(?:.+?);' +
                      '\s+charset=(.+?)"', html, re.IGNORECASE)
        if r:
            encoding = r.group(1) 
                   
        try:
            html = str(html, encoding)
        except:
            pass
            
        self.content = html
    
    
    def get_headers(self):
        return self._response.info().headers
    
        
    def get_url(self):
        return self._response.geturl()
