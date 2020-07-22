from lib.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)
from lib import constants


class Product(Base):
    __tablename__ = 'products'

    _id = Column(Integer, primary_key=True)
    name = Column(String)
    endpoint = Column(String)
    description = Column(String)
    quantity = Column(Integer, default=1)
    nested = Column(Boolean, default=False)
    purchased = Column(Boolean, default=False)

    def __repr__(self):
        url = constants.REPURL.format(self.endpoint)
        return f'{self.__class__.__name__}(name={self.name}, endpoint={url}, ' \
               f'description={self.description}, quantity={self.quantity}, nested={self.nested}, ' \
               f'purchased={self.purchased})'
