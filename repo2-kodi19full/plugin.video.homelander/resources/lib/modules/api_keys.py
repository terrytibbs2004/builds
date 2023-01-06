# -*- coding: utf-8 -*-

import base64, sys
from six import ensure_text


def chk():
    return True;

tmdb_key = ensure_text(base64.b64decode(b'NzRmM2NlOTMxZDY1ZWJkYTFmNzdlZjI0ZWFjMjYyNWY=')) if chk() else ''
tvdb_key = ensure_text(base64.b64decode(b'UVkzTUVUMU1UU0ZBTkJYVw==')) if chk() else ''
omdb_key = ensure_text(base64.b64decode(b'OGI1Mjg3ODM=')) if chk() else ''
fanarttv_key = ensure_text(base64.b64decode(b'YzM0NjljMWNjOTQ2NWI5ZjFhMWE4NjJmZWVhOGI3NmI=')) if chk() else ''
yt_key = ensure_text(base64.b64decode(b'QUl6YVN5QllQTHFOYjlVb29EdnhFS2poRTFRelhZQzY5OHpFeWg0')) if chk() else ''
trakt_client_id = ensure_text(base64.b64decode(b'NzQyOTAyN2Q4MTkzNDk2NzdkYjY2YzQ5ZTdmMzdmNThlNmQ1N2Q0MjEyMDRiMjA3NDhlOWY1NmE4YTNmMDYwMw==')) if chk() else ''
trakt_secret = ensure_text(base64.b64decode(b'MDY3Zjg3NTBjZGE2YmY1MDI3MzRlMWNiZjRlYzA3MmUzOTc1MWJiYmFiOTgzOTQzY2Q0ZWNjNzQ4YzA4ODBkNQ==')) if chk() else ''
orion_key = ensure_text(base64.b64decode(b'VFVKUERHTENFQkJSQUdSSlJQVkhNNk1DSFNGM1IyRjQ=')) if chk() else ''
