from __future__ import annotations

import enum
import logging
import random
import requests
import urllib

from typing import Dict

logger = logging.getLogger(__name__)


class PKUWebApp:

    def __init__(self, app_id: str, url: str, route: str, host: str | None = None) -> None:
        """这个 route 据 [这里](https://github.com/PkuRH/PKURunningHelper/blob/b549a1f91257ebab75cad7ab5359b0fafc575a6c/PKURunner/iaaa.py#L60) 说是 salt"""

        self.app_id: str = app_id
        """应用 ID"""

        self.url: str = url
        """应用 URL"""

        self.route: str = route
        """据 [这里](https://github.com/PkuRH/PKURunningHelper/blob/b549a1f91257ebab75cad7ab5359b0fafc575a6c/PKURunner/iaaa.py#L60) 说是 salt"""

        self.host: str = urllib.parse.urlparse(url).hostname
        """应用 host"""
        if host != None:
            self.host = host

    @property
    def data(self) -> dict:
        """returns data for authorization"""

        return {
            "appid": self.app_id,
            "redirUrl": self.url
        }

    @property
    def target_url(self) -> str:
        """remove port from url"""

        url = urllib.parse.urlparse(self.url)
        url._replace(netloc=url.hostname)
        return url.geturl()


APPS: Dict[str, PKUWebApp] = {
    "syllabus": PKUWebApp(
        "syllabus",
        "http://elective.pku.edu.cn:80/elective2008/ssoLogin.do",
        "ba917d327a9bfb3c695ce9c36a37098c",
    ),

    "portal": PKUWebApp(
        "portal2017",
        "https://portal.pku.edu.cn/portal2017/ssoLogin.do",
        "88413b23c55e32efc0b27ec26ba8b90e",
    ),
}


class PKULogin:
    """不写文档注释哈哈"""

    def __init__(self, student_id: int, password: str) -> None:

        self.session: requests.Session = requests.Session()
        """会话"""

        # Set headers
        self.init_headers()

        self.student_id: int = student_id
        """学号"""

        self.password: str = password
        """密码"""

        self.token: str = ""
        """令牌, 用于登录后的请求"""

        logger.info("PKULogin initialized.",
                    extra={"student_id": self.student_id})

    def init_headers(self) -> None:
        """初始化 headers"""

        self.session.headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
        self.session.headers["Accept-Encoding"] = "gzip, deflate, br"
        self.session.headers["Accept-Language"] = "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
        self.session.headers["Connection"] = "keep-alive"
        self.session.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        self.session.headers["Host"] = "iaaa.pku.edu.cn"
        self.session.headers["Origin"] = "https://iaaa.pku.edu.cn"
        self.session.headers["Sec-Fetch-Dest"] = "empty"
        self.session.headers["Sec-Fetch-Mode"] = "cors"
        self.session.headers["Sec-Fetch-Site"] = "same-origin"
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0"
        self.session.headers["X-Requested-With"] = "XMLHttpRequest"
        self.session.headers["Upgrade-Insecure-Requests"] = "1"

    def login(self, app: PKUWebApp) -> None:
        """登录"""

        logger.info(f"Logging in... App: {app.app_id}",
                    extra={
                        "student_id": self.student_id,
                        "app_id": app.app_id,
                    })

        data: dict = {
            "userName": self.student_id,
            "password": self.password,
            "randCode": "",
            "smsCode": "",
            "otpCode": "",
        }
        data.update(app.data)

        # Login
        res = self.session.post(
            "https://iaaa.pku.edu.cn/iaaa/oauthlogin.do",
            data=data,
            cookies={
                'username': self.student_id,
            }
        )
        assert res.json()
        if res.json().get("success"):
            self.token = res.json()["token"]
            logger.info("Token acquired.", extra={
                "student_id": self.student_id,
                "app_id": app.app_id,
            })

            # Get JSESSIONID
            self.session.cookies.set(
                'route', app.route, domain=app.host, path='/')
            params = {
                "_rand": '%.10f' % random.random(),
                "token": self.token,
            }
            login_res = self.session.get(
                app.target_url,
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Host": app.host,
                },
                params=params
            )
            if login_res.status_code == 200:
                logger.info("Login success.",
                            extra={
                                "student_id": self.student_id,
                                "app_id": app.app_id,
                            })
            else:
                logger.error(f"Login failed. Code: {login_res.status_code}",
                             extra={
                                 "student_id": self.student_id,
                                 "app_id": app.app_id,
                                 "status_code": login_res.status_code,
                             })
                logger.debug(login_res.text)
        else:
            logger.error(f"Token acquisition failed. Error: {res.json().get('message')}",
                         extra={
                             "student_id": self.student_id,
                             "app_id": app.app_id,
                         })
            logger.error("Login failed.",
                         extra={
                             "student_id": self.student_id,
                             "app_id": app.app_id,
                         })
            logger.error(res.json())
