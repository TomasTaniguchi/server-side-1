from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from .model_code import ModelCode
from sqlalchemy.orm import relationship
from .model_members import ModelMembers
from .model_area import ModelArea


class ModelEntity(Base):
    """Entity model."""
    __tablename__ = 'Entity'

    id = Column('id', Integer, primary_key=True, doc="id of the entity.")
    id_name = Column('id_name', String(15), unique=True, doc="Id id_name of the entity")
    id_name_account = Column('id_name_account', String(15), ForeignKey('Account.id_name'), doc="id_name of the account")
    profile_img = Column('profile_img', String(50))
    name = Column('name', String(30), doc="Name of the entity")
    created = Column('created', String(30), doc="Record created date.")
    edited = Column('edited', String(30), doc="Record last updated date.")
    memberList = relationship(ModelMembers, backref='Entity')
    codeList = relationship(ModelCode, backref='Entity')
    areaList = relationship(ModelArea, backref='Enity')