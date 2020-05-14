from lib.db import create_db_session
from lib.utils import (
    item_in_stock,
    build_logger,
)
from lib.models import Product
from lib.browser import Browser


class RepBot:
    def __init__(self, db, logger=None):
        self.db_file = db
        self._session = None
        self.log = logger if logger is not None else build_logger('repbot')

    @property
    def session(self):
        if self._session is None:
            self._session = create_db_session(self.db_file)
        return self._session

    def products_to_purchase(self):
        return [p for p in self.session.query(Product).filter_by(purchased=False) if item_in_stock(p)]

    def run(self):
        products = self.products_to_purchase()
        if products:
            with Browser(logger=self.log) as browser:
                for product in products:
                    self.browser.add_item_to_cart(product)
                self.browser.checkout()
