from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model_subscriptions import ModelSubscriptions
import graphene
import utils


class SubscriptionsAttribute:

    id = graphene.Int(description="id max len 15 string")
    id_name_account = graphene.String(description="Name of the account max len 10.")
    code = graphene.String(description="code of node")
    source = graphene.String(description="node of subscription")


class Subscriptions(SQLAlchemyObjectType):
    """Subscriptions node."""

    class Meta:
        model = ModelSubscriptions
        interfaces = (graphene.relay.Node,)


