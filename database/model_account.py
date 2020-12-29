from .base import Base
from sqlalchemy import Column, String, Boolean, Integer
from .model_subscriptions import ModelSubscriptions
from .model_entity import ModelEntity

from sqlalchemy.orm import relationship


class ModelAccount(Base):
    """Account model."""

    __tablename__ = 'Account'
    id = Column('id', Integer, primary_key=True, doc="Id of the account id_name ")
    id_name = Column('id_name', String(15), unique=True, doc = "Id_name of the account ")
    profile_img = Column('profile_img', String(50))
    name = Column('name', String(30), nullable=True, doc="Name of the person.")
    password = Column('password', String(16), nullable=False, doc="Password of the account.")
    email = Column('email', String(40), nullable=False, doc="EMail of the account.")
    state_account = Column('state_account', Boolean, default=0, doc="Estate of the account")
    entity = Column('entity', Boolean, default=0, doc = "if the account have some entity")
    created = Column('created', String(30), doc="Record created date.")
    edited = Column('edited', String(30), doc="Record last updated date.")

    subscriptionsList = relationship(ModelSubscriptions, backref='Account')
    entityList = relationship(ModelEntity, backref='Account')

