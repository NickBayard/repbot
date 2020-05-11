from lib.base import Base
from sqlalchemy import Column, Integer, String


class Product(Base):
    __tablename__ = 'products'

    _id = Column(Integer, primary_key=True)
    name = Column(String)
    endpoint = Column(String)
    quantity = Column(Integer)
    options = Column(String)

    def __repr__(self):
        return f'{self.__class__.__name__(name={self.name}, endpoint={self.endpoint}, ' \
               f'quantity={self.quantity}, options={self.options})'
