from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .model_members import ModelMembers


class ModelArea(Base):
    """Area Model."""
    __tablename__ = 'Area'
    id = Column('id', Integer, primary_key=True, doc="Id of the area.")
    fk_id_entity = Column('fk_id_entity', ForeignKey('Entity.id_name'), doc="Id of the Entity")
    name_area = Column('name_area', String(15), doc="Name of the area.")
    default_message = Column('default_message', String(1000), default= "Bienvenidos al area #nombre del area, todos sus mensajes serán redirijidos a esta area", doc="MessageSent default to sent automatically.")
    code = Column('code', String(25), doc="code of the area")
    private = Column('private', Boolean, default=0, doc="Allow to establish private conversations")
    created = Column('created', String(30))
    edited = Column('edited', String(30))

    memberList = relationship(ModelMembers, backref='Area')
