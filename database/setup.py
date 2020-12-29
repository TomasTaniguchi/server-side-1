from database import base

from database.model_account import ModelAccount
from database.model_entity import ModelEntity
from database.model_code import ModelCode
from database.model_area import ModelArea
from database.model_contact import ModelContact
from database.model_members import ModelMembers
from database.model_subscriptions import ModelSubscriptions
from database.model_tickets import ModelTickets
from database.model_messages import ModelMessages

import logging
import sys

# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    log.info('Create database {}'.format(base.db_name))
    base.Base.metadata.drop_all(base.engine)
    base.Base.metadata.create_all(base.engine)
