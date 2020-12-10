from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lib.utils import build_logger
from lib.errors import BrowserError
from lib.constants import REPBASEURL, REPURL


class Browser:
    # FIXME For future release that will purchase new items
    def __init__(self, headless=True, logger=None):
        self._driver = None
        self.headless = headless
        self.log = logger if logger is not None else build_logger('repbot')

    @staticmethod
    def create(headless=True):
        with Browser(headless=headless) as b:
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
        self.driver.get(REPBASEURL)

    def logout(self):
        pass  # TODO

    def add_item_to_cart(self, product):
        pass  # TODO

    def checkout(self):
        pass  # TODO

    def purchase_items(self, items):
        self.log.info('Attempting to make purchases.')
        for item in items:
            self.add_item_to_cart(item)
        self.checkout()
