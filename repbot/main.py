#!/usr/bin/env python3

import argparse
from lib import RepBot, Gmail, Notification


def get_args():
    parser = argparse.ArgumentParser(description='Bot that will purchase a wishlist of items from RepFitness.com',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--db', dest='db_file', default='repfit.db', help='Location of the sqlite db to use')
    parser.add_argument('--headed', action='store_true', help='Browser should not run headless.')
    parser.add_argument('--notification-info', default='user_info.yaml', type=Notification.create,
                        help='YAML file with private user info.')
    parser.add_argument('--credentials', default='credentials.json',
                        help='JSON file containing Google API credentials')
    parser.add_argument('--token', default='token.pickle',
                        help='YAML file with private user info.')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    bot = RepBot(db=args.db_file,
                 email=Gmail(args.notification_info, args.credentials, args.token),
                 browser=None)

    bot.run()
