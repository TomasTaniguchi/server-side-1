from functions import random_code
from database.model_subscriptions import ModelSubscriptions

def createSubscription(**kwargs):
    """ update subscription s """
    now = kwargs.get('now')
    account_id = kwargs.get('id_name_account')
    id_name = (kwargs.get('entity'))
    db_session = kwargs.get('db_session')
    source = id_name
    code_random = random_code.code()
    subscription = {'id_name_account': account_id, 'code': code_random, 'source': source, 'created': now, 'edited': now}
    subscription_model = ModelSubscriptions(**subscription)
    db_session.add(subscription_model)
    return db_session