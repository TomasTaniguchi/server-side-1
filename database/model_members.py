from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean


class ModelMembers(Base):
    """Members model."""

    __tablename__ = 'Members'

    id = Column('id', Integer, primary_key=True, doc="Id of the Member.")
    id_name_entity = Column('id_name_entity', String(15), ForeignKey('Entity.id_name'), doc="Id of the entity.")
    fk_id_area = Column('fk_id_area', Integer, ForeignKey('Area.id'), doc="Id of the area.")
    id_name_account_member = Column('id_name_account_member', String(15), ForeignKey('Account.id_name'), doc="id_name of the account member")
    subscriptions_id = Column('subscriptions_id', Integer, ForeignKey('Subscriptions.id'),doc="if of the Subscriptions")
    admin = Column('admin', Boolean, default=0, doc="If administrator of the Area.")
    active = Column('active', Boolean, default=0, doc=" if member active or not.")
    created = Column('created', String(30), doc="Record created date.")
    edited = Column('edited', String(30), doc="Record last updated date.")
