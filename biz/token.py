import json

from core.cache import Cache
from util.config import Config
from util.http import HttpUtils


class Token:
    TOKEN_KEY = "wechat_token_key"
    URL_TEMPLATE = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"
    RESPONSE_KEY = "access_token"
    EXPIRE_KEY = "expires_in"

    cache = None

    def __init__(self):
        self.cache = Cache()

    def fetch(self):
        access_token = self.cache.get(self.TOKEN_KEY)
        if access_token is None or len(access_token) == 0:
            print("Token has been expired, try fetching new one.")
            # refresh token
            response = HttpUtils.get(url=self.URL_TEMPLATE.format(Config.get("app_id"), Config.get("app_secret")),
                                     return_raw=True)
            if response is not None:
                resp_json = json.loads(str(response.text))
                access_token = resp_json[self.RESPONSE_KEY]
                expire_time = resp_json[self.EXPIRE_KEY]
                print("Fetch done, " + access_token)
                self.cache.set_with_expire(self.TOKEN_KEY, access_token, expire_time)

        return access_token


if __name__ == "__main__":
    token = Token()
    token.fetch()
