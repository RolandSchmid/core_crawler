import logging
from abc import ABC
from time import sleep

from fake_useragent import UserAgent
from requests import Session

from core.tools.Logger import get_logger_main

logger: logging.Logger = get_logger_main()


class WebReader:
    ua: UserAgent = UserAgent()
    session: Session = Session()

    def __init__(self, base_url: str, headers: dict[str, str] = None, cookies: dict = None) -> None:
        super().__init__()
        self.cookies: dict | None = cookies
        self.session.headers['User-Agent'] = self.ua.random
        self.session.headers['Accept'] = '*/*'
        self.session.headers['Origin'] = base_url
        self.session.headers['Referer'] = base_url
        if headers is not None:
            for name, value in headers.items():
                self.session.headers[name] = value

    def get_content(self, url, retry: bool = True) -> str or None:

        while True:
            resp = self.session.get(url, cookies=self.cookies)

            if resp is not None and resp.status_code == 200:
                return resp.text

            if not retry:
                break
            if resp is not None and resp.status_code == 404:
                logger.error(f'URL not found: {url}')
                break
            sleep(2)
            continue

        return None


class AbstractSpider(ABC):

    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url
        self.reader: WebReader = WebReader(base_url, self.get_cookies())

    def get_cookies(self) -> dict | None:
        return None
