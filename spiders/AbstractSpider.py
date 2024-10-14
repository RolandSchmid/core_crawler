import logging
from abc import ABC
from collections.abc import Callable
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

    def __try(self, function: Callable, url: str, data, retry: bool) -> str or None:

        tries: int = 0
        while True:
            resp = function(url, json=data, cookies=self.cookies)

            if resp is not None and resp.status_code == 200:
                return resp.text

            if not retry:
                break
            if resp is not None and resp.status_code == 404:
                logger.error(f'URL not found: {url}')
                break
            if tries == 3:
                logger.error(f'Could not get: {url}')
                break
            tries += 1
            sleep(2)
            continue

        return None

    def get(self, url: str, retry: bool = True) -> str or None:
        return self.__try(self.session.get, url, None, retry)

    def post(self, url: str, data, retry: bool = True) -> str or None:
        return self.__try(self.session.post, url, data, retry)


class AbstractSpider(ABC):

    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url
        self.reader: WebReader = WebReader(base_url, cookies=self.get_cookies())

    def get_cookies(self) -> dict | None:
        return None
