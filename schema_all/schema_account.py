from datetime import datetime
from graphene_sqlalchemy import SQLAlchemyObjectType
from database.base import db_session
from database.model_account import ModelAccount
from database.model_subscriptions import ModelSubscriptions
from functions import random_code
import graphene
import utils


# Create a generic class to mutualize description of account attributes for both queries and mutations

class AccountAttribute:
    id_name = graphene.String(description="id max len 15 string")
    name = graphene.String(description="Name of the account max len 30.")
    password = graphene.String(description="Password of the account.")
    email = graphene.String(description="Email of the account.")


class Account(SQLAlchemyObjectType):
    """Account node."""

    class Meta:
        model = ModelAccount
        interfaces = (graphene.relay.Node,)


class CreateAccountInput(graphene.InputObjectType, AccountAttribute):
    """Arguments to create a account."""
    pass


class CreateAccount(graphene.Mutation):
    """Mutation to create a account."""
    account = graphene.Field(lambda: Account, description="Account created by this mutation.")

    class Arguments:
        input = CreateAccountInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        now = datetime.utcnow()
        data['created'] = now
        data['edited'] = now
        account = ModelAccount(**data)
        db_session.add(account)
        db_session.flush()
        id_name = data['id_name']

        """ update subscriptions """
        code = random_code.account()
        subscription = {'id_name_account': id_name, 'code': code, 'source': id_name, 'created': now, 'edited': now}
        subscription_model = ModelSubscriptions(**subscription)
        db_session.add(subscription_model)

        db_session.commit()
        db_session.close()

        return CreateAccount(account=account)


class UpdateAccountInput(graphene.InputObjectType, AccountAttribute):
    """Arguments to update a account."""
    id = graphene.ID(required=True, description="Global Id of the account.")


class UpdateAccount(graphene.Mutation):
    """Update a account."""
    account = graphene.Field(lambda: Account, description="Account updated by this mutation.")

    class Arguments:
        input = UpdateAccountInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        data['edited'] = datetime.utcnow()
        account = db_session.query(ModelAccount).filter_by(id=data['id'])
        account.update(data)
        db_session.commit()
        account = db_session.query(ModelAccount).filter_by(id=data['id']).first()
        print("mutate Update")
        return UpdateAccount(account=account)


class DeleteAccountInput(graphene.InputObjectType):
    id = graphene.ID(required=True, description="Global Id of the account")


class DeleteAccount(graphene.Mutation):
    """ Delete Account"""
    account = graphene.Field(lambda: Account, description="Account deleted by this mutation.")

    class Arguments:
        input = DeleteAccountInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        account = db_session.query(ModelAccount).filter_by(id=data['id']).first()
        print("mutation Delete")
        db_session.delete(account)
        db_session.commit()
        account = db_session.query(ModelAccount).filter_by(id=data['id']).first()
        return DeleteAccount(account=account)

