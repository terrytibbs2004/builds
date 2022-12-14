"""
    Plugin for ResolveUrl
    Copyright (C) 2020 cywteow

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import requests
from resolveurl.lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError
from resolveurl.plugins.__resolve_generic__ import ResolveGeneric
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from Cryptodome.Util.Padding import pad
from base64 import b64decode, b64encode
from urllib.parse import urlsplit, parse_qs, urlparse
from bs4 import BeautifulSoup
import json


class GogoCdnResolver(ResolveGeneric):
    name = "GoGoCdn"
    domains = ['goload.io']
    pattern = r'(?://|\.)(goload\.io)/(?:streaming\.php|embedplus)\?id=([a-zA-Z0-9-]+)'
    key1 = '37911490979715163134003223491201'
    key2 = '54674138327930866480207815084989'
    iv = '3134003223491201'

    def get_media_url(self, host, media_id):
        encryptedParams = self._getEncryptedParams(f'https://{host}/streaming.php?id={media_id}')
        web_url = self.get_url(host, encryptedParams)
        response = requests.get(web_url, headers={"X-Requested-With":"XMLHttpRequest"})
        if response.status_code == 200:
            sources = []
            encryptedResult = response.json()
            result = self._decrypt(encryptedResult['data'], self.key2)
            result = result.decode('UTF-8')
            result = json.loads(result)
            for source in result['source']:
                if source['file'].endswith('.m3u8') and 'gogocdn' in source['file']:
                    sources.append(source['file'])
            for source in result['source_bk']:
                if source['file'].endswith('.m3u8') and 'gogocdn' in source['file']:
                    sources.append(source['file'])
            if len(sources) > 0:
                return urlparse(sources[0])._replace(scheme='http').geturl()

        raise ResolverError('Video cannot be located.')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/encrypt-ajax.php?{media_id}')

    def _encrypt(self,msg):
        try:        
            cipher = AES.new(self.key1.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
            ct_bytes = cipher.encrypt(pad(msg.encode("utf8"), AES.block_size))
            ct = b64encode(ct_bytes).decode("utf8")
            return ct
        except ValueError as e:
            return e

    def _decrypt(self, msg, key):
        try:
            iv = self.iv.encode("utf8")
            ct = b64decode(msg)
            cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt
        except ValueError as e:
            print (str(e))
            return ValueError
    
    def _getEncryptedParams(self, url):
        params = parse_qs(urlsplit(url).query)
        encryptedKey = self._encrypt(params['id'][0])
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        result = soup.find('script', {"data-name": "episode"})
        decryptedToken = self._decrypt(result['data-value'], self.key1).decode("UTF-8")
        return f'id={encryptedKey}&alias={decryptedToken}'

    @classmethod
    def _is_enabled(cls):
        return True
