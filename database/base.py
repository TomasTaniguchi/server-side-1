from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
db_name = 'entity_model_server_v_005_3'

# Create database engine

engine = create_engine("mysql+mysqlconnector://admin:Entity!123@localhost:12345/" + db_name, \
<<<<<<< HEAD
                       pool_size=10, max_overflow=-1, pool_recycle=100, echo=True)
=======
                       pool_size=10, max_overflow=-1, pool_recycle=100, echo=False)
>>>>>>> juan
# Engine connect

# Declarative base model to create database tables and classes
Base = declarative_base()
Base.metadata.bind = engine  # Bind engine to metadata of the base class

# Create database session object
db_session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))

Base.query = db_session.query_property()  # Used by graphql to execute queries
