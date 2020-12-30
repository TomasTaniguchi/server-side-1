from database.model_enVaribles import  ModelEnvVariables
from database import base
session = base.db_session()

INSTANCE_URL = ""
PRODUCT_ID = ""
API_TOKEN = ""

def load_env_variables(id_env):
    env_variables = session.query(ModelEnvVariables).filter_by(ID=id_env).first()
    session.close()
    global INSTANCE_URL
    global PRODUCT_ID
    global API_TOKEN
    INSTANCE_URL = env_variables.INSTANCE_URL_WAPP
    PRODUCT_ID = env_variables.PRODUCT_ID_WAPP
    API_TOKEN = env_variables.API_TOKEN_WAPP


print(INSTANCE_URL)
print(PRODUCT_ID)
print(API_TOKEN)