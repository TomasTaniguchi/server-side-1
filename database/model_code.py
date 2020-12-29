from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship



class ModelCode(Base):
    """Code model."""

    __tablename__ = 'Code'
    id = Column('id', Integer, primary_key=True, doc="Id of code is auto_increment.")
    phone_id = Column('phone_id', String(50), unique=True, doc="Id of code is not auto_increment.")
    id_name_entity = Column('id_name_entity', String(15), ForeignKey('Entity.id_name'), doc="Id of the entity.")
    phone_number = Column('phone_number', String(15), doc="Code number of the entity.")
    code_entity = Column('code_entity', Boolean, default=0, doc="if is code of entity = True, default ")
    qrcode_url = Column('qrcode_url', String(50), doc="url the img_data")
    status = Column('status', Boolean, doc="status the number in the api external")
    status_login = Column('status_login', Boolean, doc="status login in api external")
    id_product = Column('id_product', String(60), doc= "id of the product")
    default_message = Column('default_message', String(1000), default= "Para redirigir sus mensajes al area correspondiente envie un mensaje con #nombre del area: ", doc="MessageSent default to sent automatically.")
    sent_area = Column('sent_area', Boolean, default=1, doc="Sent list of areas available")
    created = Column('created', String(30), doc="Record created date.")
    edited = Column('edited', String(30), doc="Record last updated date.")

