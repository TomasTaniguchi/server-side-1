from .base import Base
from sqlalchemy import Column, String, Integer


class ModelEnvVariables(Base):
    """Environment variables model."""

    __tablename__ = 'EnVariables'
    ID = Column('ID', Integer, primary_key=True, doc="Id of the environment ")
    INSTANCE_URL_WAPP = Column('INSTANCE_URL_WAPP', String(50), doc="instance url api")
    PRODUCT_ID_WAPP = Column('PRODUCT_ID_WAPP', String(36), doc="product id api")
    API_TOKEN_WAPP = Column('API_TOKEN_WAPP', String(36), doc="api token")