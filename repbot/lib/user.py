import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader as Loader

from pathlib import Path
from dataclasses import dataclass
from datetime import date
from typing import List

from lib.errors import UserError


@dataclass
class Login:
    username: str
    password: str

    def __repr__(self):
        return f'{self.__class__.__name__}(username={self.username})'


@dataclass
class CreditCard:
    type: str
    number: int
    expiration: date
    verification: int

    def __repr__(self):
        return f'{self.__class__.__name__}(type={self.type})'


@dataclass
class Notification:
    api_account: str
    emails: List[str]

    def __repr__(self):
        return f'{self.__class__.__name__}(api_account={self.api_account}, emails={self.emails})'


@dataclass
class User:
    login: Login
    credit_card: CreditCard
    notification: Notification

    def __repr__(self):
        return f'{self.__class__.__name__}(login={self.login}, credit_card={self.credit_card}, '\
               f'notification={self.notification})'

    @staticmethod
    def create(user_yaml):
        p = Path(user_yaml)
        if not p.is_file():
            raise UserError(f'User info file is invalid: {user_yaml}')

        with p.open() as f:
            data = yaml.load(f, Loader=Loader)

        return User(login=Login(**data.get('login', {})),
                    credit_card=CreditCard(**data.get('credit_card')),
                    notification=Notification(**data.get('notification')))
