from .base import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .model_messages import ModelMessages

def node_default(context):
    return context.get_current_parameters()['phone_id']


class ModelTickets(Base):
    """Tickets model."""

    __tablename__ = 'Tickets'

    id = Column('id', Integer, primary_key=True, doc=" unique Id of the ticket.")
    id_tk = Column('id_tk', String(50), doc="Id of the ticket")
    product_id = Column('product_id', String(50), doc="Product id identity")
    phone_id = Column('phone_id', String(50), default='', doc="Id of the destination code.")
    node2 = Column('node2', String(30), default='', doc="@Entity")
    node3 = Column('node3', String(30), default='', doc="#area")
    node4 = Column('node4', String(30), default='', doc=".account")
    current = Column('current', Boolean, default=True, doc="")
    phone = Column('phone', String(15), doc="phone number if the code have one")
    name = Column('name', String(30), doc="id_name of the contact what doing the entry")
    image = Column('image', String(200), doc="Link of the contact profile picture ")
    count = Column('count', Integer, default=1, doc="keep te count of activity")
    last_id_msg = Column('last_id_msg', String(100), doc="last message id")
    timestamp = Column('timestamp', Integer, doc="Record timestamp.")

    listMessage = relationship(ModelMessages, backref="Tickets")



