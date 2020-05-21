import re
import requests
import logging
import logging.handlers
from bs4 import BeautifulSoup as bs
from lib import constants
from lib.models import Product
from lib.errors import AvailabilityError


def item_in_stock(item: Product) -> bool:
    r = requests.get(constants.REPURL.format(item.endpoint))
    r.raise_for_status()
    soup = bs(r.text, 'lxml')
    in_stock = soup.find(class_=re.compile('availability in-stock')) is not None
    if item.nested and in_stock:
        table = soup.find(id='super-product-table')
        for row in table.tbody:
            if row.find(text=item.description):
                in_stock = row.find(class_='availability out-of-stock') is None
                break
        else:
            raise AvailabilityError(f'Product could not be found {item}')

    return in_stock


def build_logger(name=None, level=logging.DEBUG):
    log = logging.getLogger(name) if name else logging.getLogger()
    log.setLevel(level)

    formatter = logging.Formatter(fmt='{asctime} [{levelname}]({module}:{funcName}:{lineno}) {message}', style='{')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log
