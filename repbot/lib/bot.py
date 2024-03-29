from lib.db import create_db_session
from lib.utils import (
    item_in_stock,
    build_logger,
)
from lib.models import Product


class RepBot:
    def __init__(self, db, email=None, browser=None, logger=None):
        self.db_file = db
        self.email = email
        self.browser = browser
        self._session = None
        self.log = logger if logger is not None else build_logger('repbot')

    @property
    def session(self):
        if self._session is None:
            self._session = create_db_session(self.db_file)
        return self._session

    def products_to_purchase(self):
        unpurchased = self.session.query(Product).filter_by(purchased=False)

        errors = []
        available = []

        for p in unpurchased:
            try:
                if item_in_stock(p):
                    available.append(p)
            except Exception as ex:
                errors.append(ex)

        if errors:  # Don't fail on the remaining purchases.  Just log the issues.
            errors = '\n'.join([repr(e) for e in errors])
            self.log.error(f'Unable to gather some in stock statuses:\n{errors}')

        return available

    def run(self):
        products = self.products_to_purchase()
        if products:
            items = '\n   '.join([str(i) for i in products])
            msg = f'Items are now available:\n   {items}'

            self.log.info(msg)

            if self.email is not None:
                self.email.send('RepBot - In stock notice', msg)

            if self.browser is not None:
                self.browser.purchase_items(items)
