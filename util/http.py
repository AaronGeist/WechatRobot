import json
import os

import requests

from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from util.config import Config

# disable warning for skip check SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class HttpUtils:
    session = None
    cookie = None

    KEY_COOKIE_LOCATION = "cookie_location"
    DEFAULT_HEADER = {
        "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
    }

    @classmethod
    def create_session_if_absent(cls):
        try:
            if cls.session is None:
                cls.session = requests.Session()
        except Exception as e:
            print(e)
            return None

    @classmethod
    def load_cookie(cls):
        if cls.session is not None:
            cookie_file = Config.get(cls.KEY_COOKIE_LOCATION)
            if os.path.exists(cookie_file):
                with open(cookie_file, "r") as f:
                    try:
                        data = f.read()
                        if data != "":
                            cls.session.cookies = requests.utils.cookiejar_from_dict(json.loads(data),
                                                                                     cookiejar=None,
                                                                                     overwrite=True)
                    except Exception as e:
                        pass

    @classmethod
    def save_cookie(cls):
        if cls.session is not None:
            with open(Config.get(cls.KEY_COOKIE_LOCATION), "w") as f:
                f.write(json.dumps(requests.utils.dict_from_cookiejar(cls.session.cookies)))

    @classmethod
    def clear_cookie(cls):
        if cls.session is not None:
            cls.session.cookies.clear()

        with open(Config.get(cls.KEY_COOKIE_LOCATION), "w") as f:
            f.write("")

    @classmethod
    def get(cls, url, session=None, headers=None, proxy=None, timeout=60, return_raw=False, allow_redirects=True):
        if session is not None:
            cls.session = session
        cls.create_session_if_absent()

        if headers is None:
            headers = cls.DEFAULT_HEADER

        try:
            response = cls.session.get(url, timeout=timeout, headers=headers, proxies=proxy, verify=False,
                                       allow_redirects=allow_redirects)
            if response.status_code != 200 and response.status_code != 301:
                # print("Wrong response status: " + str(response.status_code))
                return None

            if return_raw:
                return response
            else:
                return BeautifulSoup(response.text.encode(response.encoding, 'ignore'), 'html.parser')
        except Exception as e:
            print(e)
            return None

    @classmethod
    def post(cls, url, session=None, data=None, headers=None, proxy=None, returnRaw=False):
        if session is not None:
            cls.session = session
        cls.create_session_if_absent()

        try:
            response = cls.session.post(url, headers=headers, proxies=proxy, verify=False, data=data)
            if response.status_code != 200:
                print("Wrong response status: " + str(response.status_code))
            if returnRaw:
                return response
            else:
                return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_attr(cls, soup_obj, match_exp, attr):
        assert soup_obj is not None
        assert match_exp is not None

        tags = soup_obj.select(match_exp)
        if tags is not None and len(tags) > 0:
            return tags[0][attr]
        else:
            return None

    @classmethod
    def get_attrs(cls, soupObj, matchExp, attr):
        assert (soupObj is not None)
        assert (matchExp is not None)

        tags = soupObj.select(matchExp)

        attrs = list()
        for tag in tags:
            attrs.append(tag[attr])

        return attrs

    @classmethod
    def get_content(cls, soupObj, matchExp, index=0):
        assert (soupObj is not None)
        assert (matchExp is not None)

        items = soupObj.select(matchExp)
        if items is None or len(items) <= 0:
            return None
        else:
            if len(items[0].contents) > index:
                return items[0].contents[index]
            else:
                return None

    @classmethod
    def get_contents(cls, soupObj, matchExp, index=0):
        assert (soupObj is not None)
        assert (matchExp is not None)

        items = soupObj.select(matchExp)

        contents = list()
        for item in items:
            contents.append(item.contents[index])

        return contents


if __name__ == "__main__":
    print(HttpUtils.get("https://www.jd.com"))
