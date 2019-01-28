from core.cache import Cache
from util.config import Config
from util.http import HttpUtils


class Token:
    TOKEN_KEY = "wechat_token_key"
    EXPIRE_TIME = 7200
    URL_TEMPLATE = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"

    cache = None

    def __init__(self):
        self.cache = Cache()

    def fetch(self):
        token = self.cache.get(self.TOKEN_KEY)
        if token is None:
            # refresh token
            response = HttpUtils.get(url=self.URL_TEMPLATE.format(Config.get("app_id"), Config.get("app_secret")),
                                     return_raw=True)
            print(response.text)
            self.cache.set_with_expire(self.TOKEN_KEY, token, self.EXPIRE_TIME)

        return token

if __name__ == "__main__":
    token = Token()
    token.fetch()