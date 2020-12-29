from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String


class ModelContact(Base):
    """Contact Model."""
    __tablename__ = 'Contact'
    id = Column('id', Integer, primary_key=True, doc="Id of the area.")
    id_account = Column('id_account', ForeignKey('Account.id'), doc="Id of the account")
    id_contact = Column('id_contact', String(50), doc="Id of the account contact")
    type_contact = Column('type_contact', String(10))
    image_contact = Column('image_contact', String(200))
    name_contact = Column('name_contact', String(30))
    node2 = Column('node2', String(15), doc="")
    node3 = Column('node3', String(15), doc="")
    node4 = Column('node4', String(15), doc="")
    phone = Column('phone', String(15), nullable=False, doc="phone number.")
    created = Column('created', String(30), doc="Record created date.")
    edited = Column('edited', String(30), doc="Record last updated date.")

