from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lib.utils import build_logger


class Browser:
    def __init__(self, logger=None):
        self._driver = None
        self.log = logger if logger is not None else build_logger('repbot')

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
