from datetime import datetime
from graphene_sqlalchemy import SQLAlchemyObjectType
from database.base import db_session
from database.model_area import ModelArea
from database.model_members import ModelMembers
from database.model_subscriptions import ModelSubscriptions
from functions.general_purpose import get_nodes
import graphene

import utils


class MembersAttribute:
    id_name_account_member = graphene.String(required=True, description="Id name account member.")
    code_sub = graphene.String(required=True, description="Subscription code.")
    source_sub = graphene.String(required=True, description="Subscription source.")
    active = graphene.Boolean(description="true if is member active")


class MemberNode(SQLAlchemyObjectType):
    """Member node."""

    class Meta:
        model = ModelMembers
        interfaces = (graphene.relay.Node,)


class CreateMembersInput(graphene.InputObjectType, MembersAttribute):
    """Arguments to create a member."""
    pass

class CreateMember(graphene.Mutation):
    """Mutation to create a member."""
    member_n = graphene.Field(lambda: MemberNode, description="Member created by this mutation.")

    class Arguments:
        input = CreateMembersInput(required=True)

    def mutate(self, info, input):
        session = db_session()
        data = utils.input_to_dictionary(input)
        result_ms = session.query(ModelSubscriptions.id).filter_by(code=data['code_sub'], source=data['source_sub']).first()
        member_n = None
        if result_ms.id:
            data_member = {'id_name_account_member': data['id_name_account_member'], 'subscriptions_id': result_ms.id,
                           'created': datetime.utcnow(), 'edited': datetime.utcnow()}
            nodes = get_nodes(data['source_sub'])
            for n in nodes:
                if nodes[n] != '':
                    if n == 'node2':
                        key = 'id_name_entity'
                        data_member[key] = nodes[n]
                    if n == 'node3':
                        key = 'fk_id_area'
                        result_ma = session.query(ModelArea.id).filter_by(fk_id_entity= nodes['node2'],
                                                                          name_area=nodes['node3']).first()
                        data_member[key] = result_ma.id
            member_n = ModelMembers(**data_member)
            db_session.add(member_n)
            db_session.commit()
            db_session.close()

        return CreateMember(member_n=member_n)


class DeleteMemberInput(graphene.InputObjectType):
    id = graphene.ID(required=True, description="Global Id of the member")


class DeleteMember(graphene.Mutation):
    """ Delete Member"""
    member_n = graphene.Field(lambda: MemberNode, description="Members deleted by this mutation.")

    class Arguments:
        input = DeleteMemberInput(required=True)

    def mutate(self, info, input):
        session = db_session()
        data = utils.input_to_dictionary(input)
        member_n = session.query(ModelMembers).filter_by(id=data['id']).first()
        print("mutation Delete")
        db_session.delete(member_n)
        db_session.commit()
        member_n = session.query(ModelMembers).filter_by(id=data['id']).first()
        session.close()
        return DeleteMember(member_n=member_n)
