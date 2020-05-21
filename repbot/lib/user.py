import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader as Loader

from pathlib import Path
from dataclasses import dataclass
from datetime import date
from lib.errors import UserError


@dataclass
class User:
    username: str
    password: str
    cc_type: str
    cc_number: int
    cc_expiration: date
    ccv: int

    def __repr__(self):
        return f'{self.__class__.__name__}(username={self.username})'

    @staticmethod
    def create(user_yaml):
        p = Path(user_yaml)
        if not p.is_file():
            raise UserError(f'User info file is invalid: {user_yaml}')

        with p.open() as f:
            data = yaml.load(f, Loader=Loader)

        return User(**data)
