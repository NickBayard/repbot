#!/usr/bin/env python3

import argparse
from lib import RepBot, Browser


def get_args():
    parser = argparse.ArgumentParser(description='Bot that will purchase a wishlist of items from RepFitness.com',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--db', dest='db_file', default='repbot.db', help='Location of the sqlite db to use')
    parser.add_argument('--headed', action='store_true', help='Browser should not run headless.')
    parser.add_argument('--purchase', action='store_true', help='Available items should be purchased')
    parser.add_argument('--user-info', help='YAML file with private user info.')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    bot = RepBot(db=args.db_file,
                 browser=Browser.create(args.user_info, headless=not args.headed) if args.purchase else None)

    bot.run()
