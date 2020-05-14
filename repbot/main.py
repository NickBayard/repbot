#!/usr/bin/env python3
import argparse
import logging
from lib import RepBot, build_logger


def get_args():
    parser = argparse.ArgumentParser(description='Bot that will purchase a wishlist of items from RepFitness.com',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--db', dest='db_file', default='repbot.db', help='Location of the sqlite db to use')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    log = build_logger('main')
    bot = RepBot(args.db_file, logger=log)
    items_to_purchase = bot.products_to_purchase()
    if items_to_purchase:
        items = '\n   '.join([str(i) for i in items_to_purchase])
        log.info(f'Items are now available:\n   {items}')
