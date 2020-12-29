from datetime import datetime
from graphene_sqlalchemy import SQLAlchemyObjectType
from database import base
from database.model_code import ModelCode
from api_maytapi import phone_functions
import graphene
import utils


class CodeAttribute:
    id_name_entity = graphene.String(description="Id of the entity max len 10.")
    phone_number = graphene.String(description="Code number.")
    id_product = graphene.String(description="Identify of the product.")
    default_message = graphene.String(description="Default message for sent to number without sub_node")
    sent_area = graphene.Boolean(description="Sent list of areas")


class Code(SQLAlchemyObjectType):
    """Code node."""

    class Meta:
        model = ModelCode
        interfaces = (graphene.relay.Node,)


class CreateCodeInput(graphene.InputObjectType, CodeAttribute):
    """Arguments to create a code."""
    pass


class CreateCode(graphene.Mutation):
    """Mutation to create a account."""
    code = graphene.Field(lambda: Code, description="Code created by this mutation.")

    class Arguments:
        input = CreateCodeInput(required=True)

    def mutate(self, info, input):
        session = base.db_session()
        data = utils.input_to_dictionary(input)
        now = datetime.utcnow()
        data['created'] = now
        data['edited'] = now
        phone_number = data['phone_number']
        code_id = phone_functions.addPhone(phone_number)
        data['phone_id'] = code_id
        phone_id_str = str(code_id)
        data['qrcode_url'] = "http://localhost:5000/img_data/"+phone_id_str+".png"
        code = ModelCode(**data)
        session.add(code)
        entity = data['id_name_entity']
        if code_id != '0000':
            session.commit()
        session.close()

        return CreateCode(code=code)


class UpdateCodeInput(graphene.InputObjectType, CodeAttribute):
    """Arguments to update a code."""
    id = graphene.ID(required=True, description="Global Id of the code.")


class UpdateCode(graphene.Mutation):
    """Update a code."""
    code = graphene.Field(lambda: Code, description="Code updated by this mutation.")

    class Arguments:
        input = UpdateCodeInput(required=True)

    def mutate(self, info, input):

        session = base.db_session()

        data = utils.input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        code = session.query(ModelCode).filter_by(id=data['id'])
        code.update(data)
        session.commit()
        code = session.query(ModelCode).filter_by(id=data['id']).first()
        session.close()
        print("mutate Update")

        return UpdateCode(code=code)


class DeleteCodeInput(graphene.InputObjectType):
    id = graphene.ID(required=True, description="Global Id of the code")


class DeleteCode(graphene.Mutation):
    """ Delete Code"""
    code = graphene.Field(lambda: Code, description="Code deleted by this mutation.")

    class Arguments:
        input = DeleteCodeInput(required=True)

    def mutate(self, info, input):
        session = base.db_session()
        data = utils.input_to_dictionary(input)
        code = session.query(ModelCode).filter_by(id=data['id']).first()
        print("mutation Delete")
        session.delete(code)
        session.commit()
        code = session.query(ModelCode).filter_by(id=data['id']).first()
        session.close()
        return DeleteCode(code=code)
