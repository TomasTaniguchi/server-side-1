from datetime import datetime
from graphene_sqlalchemy import SQLAlchemyObjectType
from database.base import db_session
from database.model_contact import ModelContact
import graphene
import utils
# Create a generic class to mutualize description of contact attributes for both queries and mutations

class ContactAttribute:
    id_account = graphene.String(description="id a")
    id_contact = graphene.String(description="")
    type_contact = graphene.String(description="")
    name_contact = graphene.String(description="")
    image_contact = graphene.String(description="")
    phone_id = graphene.String(description="")
    node2 = graphene.String(description="")
    node3 = graphene.String(description="")
    node4 = graphene.String(description="")
    phone = graphene.String(description="")


class Contact(SQLAlchemyObjectType):
    """Contact node."""

    class Meta:
        model = ModelContact
        interfaces = (graphene.relay.Node,)


class CreateContactInput(graphene.InputObjectType, ContactAttribute):
    """Arguments to create a contact."""
    pass


class CreateContact(graphene.Mutation):
    """Mutation to create a contact."""
    contact = graphene.Field(lambda: Contact, description="Contact created by this mutation.")

    class Arguments:
        input = CreateContactInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        now = datetime.utcnow()
        data['created'] = now
        data['edited'] = now
        contact = ModelContact(**data)
        db_session.add(contact)
        db_session.commit()
        db_session.close()

        return CreateContact(contact=contact)


class UpdateContactInput(graphene.InputObjectType, ContactAttribute):
    """Arguments to update a contact."""
    id = graphene.ID(required=True, description="Global Id of the contact.")


class UpdateContact(graphene.Mutation):
    """Update a contact."""
    contact = graphene.Field(lambda: Contact, description="Contact updated by this mutation.")

    class Arguments:
        input = UpdateContactInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        contact = db_session.query(ModelContact).filter_by(id=data['id'])
        contact.update(data)
        db_session.commit()
        contact = db_session.query(ModelContact).filter_by(id=data['id']).first()
        print("mutate Update")
        return UpdateContact(contact=contact)


class DeleteContactInput(graphene.InputObjectType):
    id = graphene.ID(required=True, description="Global Id of the contact")


class DeleteContact(graphene.Mutation):
    """ Delete Contact"""
    contact = graphene.Field(lambda: Contact, description="Contact deleted by this mutation.")

    class Arguments:
        input = DeleteContactInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        contact = db_session.query(ModelContact).filter_by(id=data['id']).first()
        print("mutation Delete")
        db_session.delete(contact)
        db_session.commit()
        contact = db_session.query(ModelContact).filter_by(id=data['id']).first()
        return DeleteContact(contact=contact)