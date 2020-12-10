import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader as Loader

from pathlib import Path
from dataclasses import dataclass
from typing import List

from lib.errors import NotifyError


@dataclass
class Notification:
    api_account: str
    emails: List[str]

    def __repr__(self):
        return f'{self.__class__.__name__}(api_account={self.api_account}, emails={self.emails})'

    @staticmethod
    def create(user_yaml):
        p = Path(user_yaml)
        if not p.is_file():
            raise NotifyError(f'User info file is invalid: {user_yaml}')

        with p.open() as f:
            data = yaml.load(f, Loader=Loader)

        return Notification(**data.get('notification'))
