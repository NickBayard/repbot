from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lib.db import create_db_session
from lib.utils import item_in_stock
from lib.models import Product


class RepBot:
    def __init__(self, db):
        self.db_file = db
        self._session = None
        self._driver = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._driver is not None:
            self.driver.close()

    @property
    def session(self):
        if self._session is None:
            self._session = create_db_session(self.db_file)
        return self._session

    @property
    def driver(self):
        if self._driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('disable-extensions')
            self._driver = webdriver.Chrome(options=options)
        return self._driver

    def run(self):
        for product in self.session.query(Product).all():
            print('{} {}in stock'.format(product.name,
                                         '' if item_in_stock(product) else 'not '))
