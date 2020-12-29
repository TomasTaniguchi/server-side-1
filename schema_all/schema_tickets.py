from class_api.data_subcription_tk import PayloadSubTk
from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model_tickets import ModelTickets
from rx import Observable
import graphene

ObsInterval = Observable.interval(1000).share()


def get_tk(node2, node3, node4, id_tk, timestamp):
    obs = Observable.from_(PayloadSubTk.payload_tickets)\
        .filter(lambda i: i['node2'] == node2
                and i['node3'] == node3
                and i['node4'] == node4
                and i['timestamp'] >= timestamp
                or (i['id_tk'] == id_tk
                and i['timestamp'] >= timestamp))
    return obs


class Subscription(graphene.ObjectType):
    get_tk = graphene.String(node2=graphene.String(), node3=graphene.String(),
                             node4=graphene.String(), id_tk=graphene.String(),
                             timestamp=graphene.Int())

    def resolve_get_tk(info, node2, node3, node4, id_tk, timestamp):
        obs = get_tk(node2, node3, node4, id_tk, timestamp)
        return ObsInterval.flat_map(lambda i: obs.map(lambda tk: tk)).distinct()


class TicketsAttribute:
    id = graphene.Int(description="unique id of the ticket")
    id_tk = graphene.String(description="id of the ticket")
    product_id = graphene.String(description="Product id identity")
    phone_id = graphene.String(description="Id of the destination phone.")
    node2 = graphene.String(description="node2 of subscriptions")
    node3 = graphene.String(description="node3 of subscriptions")
    node4 = graphene.String(description="node4 of subscriptions")
    phone = graphene.Int(description="Code number of the contact what do some entry")
    name = graphene.String(description="id_name of the contact.")
    image = graphene.String(description="Link of the contact profile picture ")
    count = graphene.Int(description="keep te count of activity")
    last_id_msg = graphene.String(descripton="Id of the last message")
    timestamp = graphene.Int(description="Record timestamp")


class Tickets(SQLAlchemyObjectType):
    """Tickets node."""

    class Meta:
        model = ModelTickets
        interfaces = (graphene.relay.Node,)
