from datetime import datetime
from graphene_sqlalchemy import SQLAlchemyObjectType
from database.model_entity import ModelEntity
from class_api.create_sub import createSubscription
import graphene
import utils
from database import base


class EntityAttribute:
    id_name = graphene.String(description="id name of the entity.")
    id_name_account = graphene.String(description="Id of the account")
    name = graphene.String(description="Name of the entity.")
    code = graphene.String(description="code of the entity")


class Entity(SQLAlchemyObjectType):
    """Entity node."""

    class Meta:
        model = ModelEntity
        interfaces = (graphene.relay.Node,)


class CreateEntityInput(graphene.InputObjectType, EntityAttribute):
    """Arguments to create a entity."""
    pass


class CreateEntity(graphene.Mutation):
    """Mutation to create a entity."""
    entity = graphene.Field(lambda: Entity, description="Entity created by this mutation.")

    class Arguments:
        input = CreateEntityInput(required=True)

    def mutate(self, info, input):
        session = base.db_session()
        data = utils.input_to_dictionary(input)
        now = datetime.utcnow()
        data['created'] = now
        data['edited'] = now
        entity = ModelEntity(**data)
        session.add(entity)
        session = createSubscription(db_session=session, entity=data['id_name'], id_name_account=data['id_name_account'], now=now)
        session.commit()
        session.close()
        return CreateEntity(entity=entity)


class UpdateEntityInput(graphene.InputObjectType, EntityAttribute):
    """Arguments to update a entity."""
    id = graphene.ID(required=True, description="Global Id of the entity.")


class UpdateEntity(graphene.Mutation):
    """Update a entity."""
    entity = graphene.Field(lambda: Entity, description="Entity updated by this mutation.")

    class Arguments:
        input = UpdateEntityInput(required=True)

    def mutate(self, info, input):
        session = base.db_session()

        data = utils.input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        entity = session.query(ModelEntity).filter_by(id=data['id'])
        entity.update(data)
        session.commit()
        entity = session.query(ModelEntity).filter_by(id=data['id']).first()
        print("mutate Update")
        session.close()
        return UpdateEntity(entity=entity)


class DeleteEntityInput(graphene.InputObjectType):
    id = graphene.ID(required=True, description="Global Id of the entity")


class DeleteEntity(graphene.Mutation):
    """ Delete Entity"""
    entity = graphene.Field(lambda: Entity, description="Entity deleted by this mutation.")

    class Arguments:
        input = DeleteEntityInput(required=True)

    def mutate(self, info, input):
        session = base.db_session()

        data = utils.input_to_dictionary(input)
        entity = session.query(ModelEntity).filter_by(id=data['id']).first()
        print("mutation Delete")
        session.delete(entity)
        session.commit()
        entity = session.query(ModelEntity).filter_by(id=data['id']).first()
        session.close()
        return DeleteEntity(entity=entity)
