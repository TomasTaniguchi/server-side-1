from datetime import datetime
from graphene_sqlalchemy import SQLAlchemyObjectType
from database.base import db_session
from database.model_area import ModelArea
from database.model_code import ModelCode
from database.model_entity import ModelEntity
from database.model_subscriptions import ModelSubscriptions
from functions import random_code
import graphene
import utils


# Create a generic class to mutualize description of area attributes for both queries and mutations

class AreaAttribute:
    fk_id_entity = graphene.String(description="ForeignKey ")
    name_area = graphene.String(description="Name of the area max len 16.")
    code = graphene.String(description="Code of the area.")
    private = graphene.Boolean(description="Allow to establish private conversations")


class Area(SQLAlchemyObjectType):
    """Area node."""

    class Meta:
        model = ModelArea
        interfaces = (graphene.relay.Node,)


class CreateAreaInput(graphene.InputObjectType, AreaAttribute):
    """Arguments to create a area."""
    pass


class CreateArea(graphene.Mutation):
    """Mutation to create a area."""
    area = graphene.Field(lambda: Area, description="Area created by this mutation.")

    class Arguments:
        input = CreateAreaInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        now = datetime.utcnow()
        data['created'] = now
        data['edited'] = now
        area = ModelArea(**data)
        db_session.add(area)
        db_session.flush()
        name_area = data['name_area']
        entity_name_id  = data['fk_id_entity']
        account_id = db_session.query(ModelEntity.id_name_account).filter_by(id_name=entity_name_id).first()
        account_id = account_id.id_name_account
        source =  entity_name_id + name_area
        code = random_code.area()
        subscription = {'id_name_account': account_id, 'code': code, 'source': source, 'created': now, 'edited': now}
        subscription_model = ModelSubscriptions(**subscription)
        db_session.add(subscription_model)
        db_session.commit()
        return CreateArea(area=area)


class UpdateAreaInput(graphene.InputObjectType, AreaAttribute):
    """Arguments to update a area."""
    id = graphene.ID(required=True, description="Global Id of the area.")


class UpdateArea(graphene.Mutation):
    """Update a area."""
    area = graphene.Field(lambda: Area, description="Area updated by this mutation.")

    class Arguments:
        input = UpdateAreaInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        area = db_session.query(ModelArea).filter_by(id=data['id'])
        area.update(data)
        db_session.commit()
        area = db_session.query(ModelArea).filter_by(id=data['id']).first()
        print("mutate Update")
        return UpdateArea(area=area)


class DeleteAreaInput(graphene.InputObjectType):
    id = graphene.ID(required=True, description="Global Id of the area")


class DeleteArea(graphene.Mutation):
    """ Delete Area"""
    area = graphene.Field(lambda: Area, description="Area deleted by this mutation.")

    class Arguments:
        input = DeleteAreaInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        area = db_session.query(ModelArea).filter_by(id=data['id']).first()
        print("mutation Delete")
        db_session.delete(area)
        db_session.commit()
        area = db_session.query(ModelArea).filter_by(id=data['id']).first()
        return DeleteArea(area=area)
