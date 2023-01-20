import os, requests, json, time
import xbmcaddon
from xbmcvfs import translatePath
from base64 import b64encode, b64decode
from binascii import a2b_hex
from requests.sessions import HTTPAdapter

from ..models.Link import Link
from ..models.Extractor import Extractor
try:
    from Crypto.Cipher import DES, PKCS1_v1_5
    from Crypto.Util.Padding import unpad
    from Crypto.PublicKey import RSA
except:
    try:
        from Cryptodome.Cipher import DES, PKCS1_v1_5
        from Cryptodome.Util.Padding import unpad
        from Cryptodome.PublicKey import RSA
    except:
        pass






class UKTVNow(Extractor):
    base_url = "https://rocktalk.net/tv/index.php"
    user_agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)"
    player_user_agent = "mediaPlayerhttp/2.5 (Linux;Android 5.1) ExoPlayerLib/2.6.1"
    json_config = {}

    def __init__(self) -> None:
        self.domains = ["uktvnow.com"]
        self.name = "UKTVNow"
        self.short_name = "UKTVNow"

    def get_link(self, url):
        self.init_config()
        channel_id = url.replace("https://uktvnow.com/play/", "")
        stream = self.get_channel_links(channel_id)[0]
        return stream

    def init_config(self):
        if self.json_config != {}: return
        addon = xbmcaddon.Addon()
        USER_DATA_DIR = translatePath(addon.getAddonInfo("profile"))
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": "USER-AGENT-tvtap-APP-V2"})
        self.s.mount("https://", HTTPAdapter(max_retries=5))
        config = os.path.join(USER_DATA_DIR, "uktvnow_config.json")
        if not os.path.exists(config):
            self.update_channels()
            self.write_config()
        else:
            f = open(config)
            json_config = json.loads(f.read())
            f.close()
            self.json_config = json_config
            if time.time() - json_config["data_age"] > 8 * 60 * 60:
                self.update_channels()
                self.write_config()
    
    def write_config(self):
        addon = xbmcaddon.Addon()
        USER_DATA_DIR = translatePath(addon.getAddonInfo("profile"))
        if not os.path.exists(USER_DATA_DIR):
            os.makedirs(USER_DATA_DIR)
        config = os.path.join(USER_DATA_DIR, "uktvnow_config.json")
        self.json_config["data_age"] = time.time()
        f = open(config, "w")
        f.write(json.dumps(self.json_config))
        f.close()

    def payload(self):
        pub_key = RSA.importKey(
            a2b_hex(
                "30819f300d06092a864886f70d010101050003818d003081890281"
                "8100bfa5514aa0550688ffde568fd95ac9130fcdd8825bdecc46f1"
                "8f6c6b440c3685cc52ca03111509e262dba482d80e977a938493ae"
                "aa716818efe41b84e71a0d84cc64ad902e46dbea2ec61071958826"
                "4093e20afc589685c08f2d2ae70310b92c04f9b4c27d79c8b5dbb9"
                "bd8f2003ab6a251d25f40df08b1c1588a4380a1ce8030203010001"
            )
        )
        msg = a2b_hex(
            "7b224d4435223a22695757786f45684237686167747948392b58563052513d3d5c6e222c22534"
            "84131223a2242577761737941713841327678435c2f5450594a74434a4a544a66593d5c6e227d"
        )
        cipher = PKCS1_v1_5.new(pub_key)
        return b64encode(cipher.encrypt(msg))

    def api_request(self, case, channel_id=None):
        headers = {"app-token": "37a6259cc0c1dae299a7866489dff0bd"}
        data = {"payload": self.payload(), "username": "603803577"}
        if channel_id:
            data["channel_id"] = channel_id
        params = {"case": case}
        r = self.s.post(self.base_url, headers=headers, params=params, data=data, timeout=5)
        r.raise_for_status()
        resp = r.json()
        if resp["success"] == 1:
            return resp["msg"]
        else:
            raise ValueError(resp["msg"])

    def update_channels(self):
        channels = self.api_request("get_all_channels")["channels"]
        categories = []
        [categories.append(category) for category in [channel.get("cat_name") for channel in channels] if category not in categories]
        self.json_config["categories"] = sorted(categories)
        self.json_config["channels"] = channels

    def get_channel_links(self, pk_id):
        _channel = self.api_request("get_channel_link_with_token_latest", pk_id)["channel"][0]
        links = []
        for stream in _channel.keys():
            if "stream" in stream or "chrome_cast" in stream:
                _crypt_link = _channel[stream]
                if _crypt_link:
                    d = DES.new(b"98221122", DES.MODE_ECB)
                    link = unpad(d.decrypt(b64decode(_crypt_link)), 8).decode("utf-8")
                    if not link == "dummytext" and link not in links:
                        links.append(link)
        return [Link(l, headers={"User-Agent": self.player_user_agent} if l.startswith("http") else {}) for l in links]