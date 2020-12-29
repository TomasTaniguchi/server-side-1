from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model_messages import ModelMessages
import graphene


class MessageAttribute:
    tickets_id = graphene.Int(description= "Id unique tks")
    id = graphene.String(description="Id of the message")
    type = graphene.String(description="type of message")
    text = graphene.String(description=" text of message")
    url = graphene.String(description="url of file or media msg")
    filename = graphene.String(description="file id_name")
    fromMe = graphene.Boolean(description= "source of the msg")
    caption = graphene.String(description="caption of message")
    timestamp = graphene.Int(description= "Timestamp message")


class Message(SQLAlchemyObjectType):
    """MessageSent node."""

    class Meta:
        model = ModelMessages
        interfaces = (graphene.relay.Node,)