# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 RACC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals, absolute_import

import os
import time
import requests

from .peewee import SqliteDatabase, Model, IntegerField, TextField, ForeignKeyField, chunked
from uuid import uuid4
from pyamf import remoting, AMF3
from pyamf.flex import messaging
from base64 import b64decode
from itertools import chain
from datetime import datetime
import warnings

warnings.simplefilter("ignore")
db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Config(BaseModel):
    data_age = IntegerField(default=time.time)
    api_url = TextField()
    api_referer = TextField()
    api_authorization = TextField()
    token_url_21 = TextField()
    token_auth_21 = TextField()
    token_url_38 = TextField()
    token_auth_38 = TextField()
    token_url_48 = TextField()
    token_auth_48 = TextField()
    mod_value = TextField()


class User(BaseModel):
    user_id = TextField(unique=True)
    check = IntegerField()


class Category(BaseModel):
    category_id = IntegerField(primary_key=True)
    title = TextField()


class Country(BaseModel):
    country_id = IntegerField(primary_key=True)
    title = TextField()


class Video(BaseModel):
    video_id = IntegerField(primary_key=True)
    category = ForeignKeyField(Category, backref="videos")
    country = ForeignKeyField(Country, backref="videos")
    title = TextField()
    logo_url = TextField()


class Stream(BaseModel):
    stream_id = IntegerField(primary_key=True)
    video_id = ForeignKeyField(Video, backref="streams")
    token = IntegerField()
    stream_url = TextField()


class RBTV:
    def __init__(self, cache_dir):
        DB = os.path.join(cache_dir, "rbtv2.db")
        db.init(DB)
        db.connect()
        db.create_tables([Config, User, Category, Country, Video, Stream], safe=True)
        self.config_url = "https://api.backendless.com/A73E1615-C86F-F0EF-FFDC-58ED0DFC6B00/7B3DFBA7-F6CE-EDB8-FF0F-45195CF5CA00/binary"
        self.user_agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTT Build/LVY48F)"
        self.player_user_agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTT Build/LVY48F)"
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": self.user_agent})

        config = Config.select()
        if config.count() == 0:
            self.fetch_config()
            self.config = Config.select()[0]
            self.fetch_videos()
        else:
            self.config = Config.select()[0]

        if time.time() - self.config.data_age > 8 * 60 * 60:
            self.fetch_config()
            self.config = Config.select()[0]
            self.fetch_videos()

    def __del__(self):
        db.close()
        self.s.close()

    @staticmethod
    def decode_value(v):
        return b64decode(v[1:]).decode("utf-8")

    @staticmethod
    def decode_value2(v):
        return b64decode(v[:-1]).decode("utf-8")

    def api_request(self, url, data):
        headers = {
            "Referer": self.config.api_referer,
            "Authorization": self.config.api_authorization,
        }
        r = self.s.post(url, headers=headers, data=data, timeout=5, verify=False)
        r.raise_for_status()
        return r.json()

    def fetch_config(self):
        data = {
            "clientId": None,
            "destination": "GenericDestination",
            "correlationId": None,
            "source": "com.backendless.services.persistence.PersistenceService",
            "operation": "first",
            "messageRefType": None,
            "headers": {"application-type": "ANDROID", "api-version": "1.0"},
            "timestamp": 0,
            "body": ["AppConfigGolfNew"],
            "timeToLive": 0,
            "messageId": None,
        }
        req = remoting.Request(target="null", body=[messaging.RemotingMessage(**data)])
        ev = remoting.Envelope(AMF3)
        ev["null"] = req
        resp = self.s.post(
            self.config_url,
            data=remoting.encode(ev).getvalue(),
            headers={"Content-Type": "application/x-amf"},
            timeout=5,
            verify=False,
        )
        resp.raise_for_status()
        amf_data = remoting.decode(resp.content).bodies[0][1].body.body
        if amf_data:
            with db.atomic():
                Config.delete().execute()
                Config.insert(
                    api_url=self.decode_value(amf_data["YmFzZXVybG5ld3gw"]),
                    api_referer=self.decode_value(amf_data["SXNpc2VrZWxvX3Nlc2lzdGltdV95ZXppbm9tYm9sbzAw"]),
                    api_authorization=self.decode_value(amf_data["amFnX3Ryb3JfYXR0X2Vu"]),
                    token_url_21=self.decode_value(amf_data["Y2FsYWFtb19pa3Mw"]),
                    token_auth_21=self.decode_value(amf_data["WXJfd3lmX3luX2JhaXMw"]),
                    token_url_38=self.decode_value(amf_data["YmVsZ2lfMzgw"]),
                    token_auth_38=self.decode_value(amf_data["Z2Vsb29mc2JyaWVm"]),
                    token_url_48=self.decode_value(amf_data["Ym9ya3lsd3VyXzQ4"]),
                    token_auth_48=self.decode_value(amf_data["dGVydHRleWFj"]),
                    mod_value=self.decode_value(amf_data["TW9vbl9oaWsx"]),
                ).execute()

    def register_user(self):
        data = {
            "gmail": "",
            "api_level": "19",
            "android_id": uuid4().hex[:16],
            "device_id": "unknown",
            "device_name": "AFTT",
            "version": "2.1 (39)",
        }
        user_id = self.api_request(self.config.api_url + "adduserinfo.nettv/", data).get("user_id")
        if user_id:
            with db.atomic():
                User.delete().execute()
                User.insert(user_id=user_id, check=8).execute()

    def fetch_videos(self):
        user = User.select()
        if user.count() == 0:
            self.register_user()
        user = User.select()[0]
        data = {"check": user.check, "user_id": user.user_id, "version": "37"}
        user.check = 1
        user.save()
        res = self.api_request(self.config.api_url + "redbox.tv/", data)

        def categories(res):
            for item in res["categories_list"]:
                yield {"category_id": item["cat_id"], "title": item["cat_name"]}

        def countries(res):
            for item in res["countries_list"]:
                yield {"country_id": item["country_id"], "title": item["country_name"]}

        def videos(res):
            for item in res["eY2hhbm5lbHNfbGlzdA=="]:
                yield {
                    "video_id": self.decode_value2(item["rY19pZA=="]),
                    "category": item["cat_id"],
                    "country": item["country_id"],
                    "title": self.decode_value2(item["ZY19uYW1l"]),
                    "logo_url": self.decode_value(item["abG9nb191cmw="]),
                }

        def streams(res):
            for item in res["eY2hhbm5lbHNfbGlzdA=="]:
                video_id = self.decode_value2(item["rY19pZA=="])
                for stream in item["Qc3RyZWFtX2xpc3Q="]:
                    yield {
                        "stream_id": self.decode_value2(stream["cc3RyZWFtX2lk"]),
                        "video_id": video_id,
                        "token": self.decode_value2(stream["AdG9rZW4="]),
                        "stream_url": self.decode_value(stream["Bc3RyZWFtX3VybA=="]),
                    }

        with db.atomic():
            Stream.delete().execute()
            Video.delete().execute()
            Country.delete().execute()
            Category.delete().execute()
            for batch in chunked(categories(res), 100):
                Category.replace_many(batch).execute()
            for batch in chunked(countries(res), 100):
                Country.replace_many(batch).execute()
            for batch in chunked(videos(res), 100):
                Video.replace_many(batch).execute()
            for batch in chunked(streams(res), 100):
                Stream.replace_many(batch).execute()

    def get_categories(self):
        return Category.select().order_by(Category.category_id)

    def get_category_by_id(self, category_id):
        return Category.get(Category.category_id == category_id)

    def get_video_by_id(self, video_id):
        return Video.get(Video.video_id == video_id)

    def resolve_logo(self, logo_url):
        return (logo_url, {"User-Agent": self.user_agent})

    def resolve_stream(self, stream):
        def modified_header():
            value = int(self.config.mod_value)
            return "".join(list(chain(*zip(str(int(time.time()) ^ value), "0123456789"))))

        if stream.token == 21:
            url = self.config.token_url_21
            auth = self.config.token_auth_21
        elif stream.token == 38:
            url = self.config.token_url_38
            auth = self.config.token_auth_38
        elif stream.token == 48:
            url = self.config.token_url_48
            auth = self.config.token_auth_48
        else:
            return (stream.stream_url, {"User-Agent": self.player_user_agent})

        headers = {
            "User-Agent": self.user_agent,
            "Accept-Encoding": "gzip",
            "Modified": modified_header(),
            "Authorization": auth,
        }

        req = requests.Request("GET", url)
        prepped = req.prepare()
        prepped.headers = headers
        r = self.s.send(prepped, timeout=5, verify=False)
        r.raise_for_status()
        _token = r.text

        if stream.token == 21:
            token = _token
        elif stream.token == 38:
            token = "".join([_token[:-59], _token[-58:-52], _token[-51:-43], _token[-42:-34], _token[-33:]])
        elif stream.token == 48:
            now = datetime.utcnow()
            _in = list(_token)
            _in.pop(len(_in) + 2 - 3 - int(str(now.year)[:2]))
            _in.pop(len(_in) + 3 - 4 - int(str(now.year)[2:]))
            # java January = 0
            _in.pop(len(_in) + 4 - 5 - (now.month - 1 + 1 + 10))
            _in.pop(len(_in) + 5 - 6 - now.day)
            token = "".join(_in)

        return (
            stream.stream_url + token,
            {
                "User-Agent": self.player_user_agent,
            },
        )
