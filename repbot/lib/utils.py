import re
import requests
from bs4 import BeautifulSoup as bs
from lib import constants
from lib.models import Product


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
            raise Exception(f'Product could not be found {item}')

    return in_stock
