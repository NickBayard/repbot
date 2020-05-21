from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lib.utils import build_logger
from lib.errors import BrowserError
from lib.user import User


class Browser:
    def __init__(self, user_info, headless=True, logger=None):
        self.user = User.create(user_info)
        self._driver = None
        self.headless = headless
        self.log = logger if logger is not None else build_logger('repbot')

    @staticmethod
    def create(user_info, headless=True):
        if not user_info:
            raise BrowserError('User info must be provided to make purchases.')
        else:
            with Browser(user_info, headless=headless) as b:
                yield b

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._driver is not None:
            self.logout()
            # TODO log off of session
            self.driver.close()

    @property
    def driver(self):
        if self._driver is None:
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('headless')
            options.add_argument('disable-extensions')
            self._driver = webdriver.Chrome(options=options)
        return self._driver

    def login(self):
        pass  # TODO

    def logout(self):
        pass  # TODO

    def add_item_to_cart(self, product):
        pass  # TODO

    def checkout(self):
        pass  # TODO
