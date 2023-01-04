# -*- coding: utf-8 -*-

import base64, sys
from six import ensure_text


def chk():
    return True;

tmdb_key = ensure_text(base64.b64decode(b'ZDZjZTg1Y2RhOTBkYWE5ZjM3OTBjZWQ5ZGExOGQwMzQ=')) if chk() else ''
tvdb_key = ensure_text(base64.b64decode(b'MzJZUDgzNjJIWUxJSTQ2UA==')) if chk() else ''
omdb_key = ensure_text(base64.b64decode(b'ZWQ4YWNmNQ==')) if chk() else ''
fanarttv_key = ensure_text(base64.b64decode(b'OWMyZDBkMWY3NWQ4NzEzM2UxNjkwNGM4ZGI3Yjc5MjQ=')) if chk() else ''
yt_key = ensure_text(base64.b64decode(b'QUl6YVN5QVNHWVl2dXBXSC1SNzRZcWJ4TWt4QldSdDFoVkF2eFdV')) if chk() else ''
trakt_client_id = ensure_text(base64.b64decode(b'ZjQ0YjE5YmQwMGIwZDAxMTFhNDY3ZTE2MWM2NDNhNTJiNWVhYmRlMWUyYjc3NDIzMjgxNjA4MmMxNWE1NjFjZA==')) if chk() else ''
trakt_secret = ensure_text(base64.b64decode(b'NTI3NjM3ZTQ3ZTBhNTYyYjgwMWUzOGU4Y2ZmMjE0MDI3YzAwYWU5NTc2YjQ5YTIwODYzZGMxZjZjMzAwNTU0Mg==')) if chk() else ''
orion_key = ensure_text(base64.b64decode(b'N0NQQUVETENCRUhLUUdLNExDSExQTFdSTFFGUFNDRU4=')) if chk() else ''
