#!/usr/bin/env python3
import argparse
from lib import create_db_session, RepBot


def get_args():
    parser = argparse.ArgumentParser(description='Bot that will purchase a wishlist of items from RepFitness.com',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--db', dest='db_file', default='repbot.db', help='Location of the sqlite db to use')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    session = create_db_session(args.db_file)
    bot = RepBot(session)
    bot.run()
