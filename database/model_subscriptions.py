from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .model_tickets import ModelTickets


class ModelSubscriptions(Base):
    """Subscriptions model."""

    __tablename__ = 'Subscriptions'
    id = Column('id', Integer, primary_key=True, doc="Id of the subscription.")
    id_name_account = Column('id_name_account', String(10), ForeignKey('Account.id_name'), doc="id_name of the account")
    code = Column('code', String(10), doc="for index to be members")
    source = Column('source', String(100), nullable=False, doc="from where is subscrited .")
    created = Column('created', String(30), doc="Record created date.")
    edited = Column('edited', String(30), doc="Record last updated date.")

    #ticketsList = relationship(ModelTickets, backref='Subscriptions')
