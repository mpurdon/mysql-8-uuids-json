import uuid

from sqlalchemy import Column, BigInteger, Unicode
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_utils import UUIDType

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'guid_user'

    id = Column(BigInteger, primary_key=True, index=True)
    guid = Column(UUIDType(), unique=True, default=uuid.uuid4)
    name = Column(Unicode(255), nullable=False)
    address = Column(JSON)

    def __str__(self):
        return f'{self.name} [{self.guid}]'

    def __repr__(self):
        return f'<UserModel(id="{self.id}", guid="{self.guid}", name="{self.name}", address="{self.address}")>'
