import logging
import random
import requests
import urllib

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)


class PKUWebApp:

    def __init__(self, app_id: str, url: str) -> None:
        """..."""

        self.app_id: str = app_id
        """应用 ID"""

        self.url: str = url
        """应用 URL"""

    @property
    def data(self) -> dict:
        """returns data for authorization"""

        return {
            "appid": self.app_id,
            "redirUrl": self.url
        }


class PKUWebApps:

    syllabus: PKUWebApp = PKUWebApp(
        app_id="syllabus",
        url="http://elective.pku.edu.cn:80/elective2008/ssoLogin.do"
    )
    """选课系统"""

    portal: PKUWebApp = PKUWebApp(
        app_id="portal2017",
        url="https://portal.pku.edu.cn/portal2017/ssoLogin.do"
    )
    """信息门户"""


class PKULogin:
    """不写文档注释哈哈"""

    def __init__(self, student_id: int, password: str) -> None:

        self.session: requests.Session = requests.Session()
        """会话"""

        # Set headers
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

        self.student_id: int = student_id
        """学号"""

        self.password: str = password
        """密码"""

        self.token: str = ""
        """令牌, 用于登录后的请求"""

        logger.info("PKULogin initialized.",
                    extra={"student_id": self.student_id})

    def login(self, app: PKUWebApp) -> None:
        """登录"""

        data: dict = {
            "username": self.student_id,
            "password": self.password,
            "randCode": "",
            "smsCode": "",
            "otpCode": "",
        }
        data.update(app.data)

        # Login
        res = self.session.post(
            "https://iaaa.pku.edu.cn/iaaa/oauthlogin.do",
            data=data
        )
        assert res.json()
        if res.json()["success"]:
            self.token = res.json()["token"]
            logger.info("Token acquired.", extra={
                "student_id": self.student_id,
                "app_id": app.app_id,
            })
            params = {
                "_rand": random.random,
                "token": self.token
            }
            login_res = self.session.get(
                app.url,
                params=params
            )
            if login_res.status_code == 200:
                logger.info("Login success.",
                            extra={
                                "student_id": self.student_id,
                                "app_id": app.app_id,
                            })
            else:
                logger.error("Login failed.",
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
            logger.debug(res.text)
