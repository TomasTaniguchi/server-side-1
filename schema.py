from graphene_sqlalchemy import SQLAlchemyConnectionField
from database.model_tickets import ModelTickets
from database.model_messages import ModelMessages
from database.model_members import ModelMembers
from schema_all.schema_tickets import Subscription


from schema_all import schema_account, schema_entity, \
    schema_subscriptions, schema_contact, \
    schema_code, schema_members, schema_area, \
    schema_tickets, schema_sent_message, schema_message
import graphene
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s-%(thread)d')
logging.debug(msg="start")


class Query(graphene.ObjectType):
    """Nodes which can be queried by this API."""
    node = graphene.relay.Node.Field()

    # Account
    account = graphene.relay.Node.Field(schema_account.Account)
    account_list = SQLAlchemyConnectionField(schema_account.Account)

    validate_account = graphene.Field(lambda: schema_account.Account,
                                      id_name=graphene.String(),
                                      password=graphene.String())
    check_id_name_account = graphene.Field(lambda: schema_account.Account,
                                           id_name=graphene.String())
    check_email_account = graphene.Field(lambda: schema_account.Account,
                                         email=graphene.String())
    # Area
    check_name_area = graphene.Field(lambda: schema_area.Area,
                                     name_area=graphene.String(),
                                     fk_id_entity=graphene.String())

    # Contact
    contact = graphene.relay.Node.Field(schema_contact.Contact)
    contact_list = SQLAlchemyConnectionField(schema_contact.Contact)

    # Entity
    entity = graphene.relay.Node.Field(schema_entity.Entity)
    entity_list = SQLAlchemyConnectionField(schema_entity.Entity)
    check_entity_id_name = graphene.Field(lambda: schema_entity.Entity,
                                          id_name=graphene.String())

    # Subscriptions
    subscription = graphene.relay.Node.Field(schema_subscriptions.Subscriptions)
    subscription_list = SQLAlchemyConnectionField(lambda: schema_subscriptions.Subscriptions,
                                                  id_name_account=graphene.String())

    # Code
    code = graphene.relay.Node.Field(schema_code.Code)
    code_list = SQLAlchemyConnectionField(schema_code.Code)

    # Members
    member = graphene.relay.Node.Field(schema_members.MemberNode)
    member_list = SQLAlchemyConnectionField(schema_members.MemberNode)

    check_member_in_entity = SQLAlchemyConnectionField(lambda: schema_members.MemberNode,
                                                       id_name_entity=graphene.String(),
                                                       id_name_account_member=graphene.String())

    check_member_in_area = SQLAlchemyConnectionField(lambda: schema_members.MemberNode,
                                                     fk_id_area=graphene.String(),
                                                     id_name_account_member=graphene.String())

    # Area
    area = graphene.relay.Node.Field(schema_area.Area)
    area_list = SQLAlchemyConnectionField(schema_area.Area)

    # Tickets
    ticket = graphene.relay.Node.Field(schema_tickets.Tickets)
    ticket_list = SQLAlchemyConnectionField(lambda: schema_tickets.Tickets,
                                            phone_id=graphene.String(),
                                            node2=graphene.String(),
                                            node3=graphene.String(),
                                            node4=graphene.String(),
                                            timestamp=graphene.String())

    # MessageSent
    getMessage = graphene.Field(lambda: schema_message.Message, id=graphene.String())
    list_message = SQLAlchemyConnectionField(lambda: schema_message.Message,
                                             tickets_id=graphene.String(),
                                             timestamp=graphene.String())

    def resolve_list_message(self, context, tickets_id, timestamp):
        query = schema_message.Message.get_query(context)
        timestamp = int(timestamp)
        tickets_id = int(tickets_id)
        query_result = query.filter(
            (ModelMessages.tickets_id == tickets_id)
            & (ModelMessages.timestamp >= timestamp))
        return query_result

    def resolve_validate_account(self, context, id_name, password):
        query = schema_account.Account.get_query(context)
        logging.debug(msg='resolve_validate_account, received param: ' + id_name + ' and ' + password)
        query_result = query.filter_by(id_name=id_name,
                                       password=password).first()
        return query_result

    def resolve_check_id_name_account(self, context, id_name):
        query = schema_account.Account.get_query(context)
        logging.debug(msg='resolve_validate_account, received param: ' + id_name)
        query_result = query.filter_by(id_name=id_name).first()
        return query_result

    def resolve_check_email_account(self, context, email):
        query = schema_account.Account.get_query(context)
        logging.debug(msg='resolve_check_email_account, received param: ' + email)
        query_result = query.filter_by(email=email).first()
        return query_result

    def resolve_check_entity_id_name(self, context, id_name):
        query = schema_entity.Entity.get_query(context)
        logging.debug(msg='resolve_check_entity_id_name, received param: ' + id_name)
        query_result = query.filter_by(id_name=id_name).first()
        return query_result

    def resolve_check_name_area(self, context, name_area, fk_id_entity):
        query = schema_area.Area.get_query(context)
        logging.debug(msg='resolve_check_name_area, received param: ' + name_area + ' ' + fk_id_entity)
        query_result = query.filter_by(fk_id_entity=fk_id_entity,
                                       name_area=name_area).first()

        return query_result

    def resolve_check_member_in_area(self, context, fk_id_area, id_name_account_member):
        query = schema_members.MemberNode.get_query(context)
        logging.debug(msg='resolve_check_member_in_area, received param: ' + fk_id_area + ' ' + id_name_account_member)
        print('received param: ' + fk_id_area, ' ', id_name_account_member)
        query_result = query.filter((ModelMembers.fk_id_area == fk_id_area) &\
                       (ModelMembers.id_name_account_member == id_name_account_member))
        return query_result

    def resolve_check_member_in_entity(self, context, id_name_entity, id_name_account_member):
        query = schema_members.MemberNode.get_query(context)
        logging.info(msg='resolve_check_member_in_entity, received param: '
                          + id_name_entity + ' ' + id_name_account_member)
        query_result = query.filter((ModelMembers.id_name_entity == id_name_entity) &\
                       (ModelMembers.id_name_account_member == id_name_account_member))

        return query_result

    def resolve_ticket_list(self, context, node2, node3, node4, timestamp):
        logging.debug(msg='resolve_ticket_list, received param: '
                          + node2 + ' ' + node3 + node4 + ' ' + timestamp)
        timestamp = int(timestamp)
        query = schema_tickets.Tickets.get_query(context)
        query_result = query.filter(
            (ModelTickets.timestamp >= timestamp) | (ModelTickets.node2 == node2)
            & (ModelTickets.node3 == node3) & (ModelTickets.node4 == node4) & (ModelTickets.timestamp >= timestamp))

        return query_result

    def resolve_subscription_list(self, context, id_name_account):
        query = schema_subscriptions.Subscriptions.get_query(context)
        logging.debug(msg='resolve_subscription_list, received param: ' + id_name_account)
        query_result = query.filter_by(id_name_account=id_name_account)
        return query_result

    def resolve_getMessage(self, context, id):
        query = schema_message.Message.get_query(context)
        logging.debug(msg='resolve_getMessage, received param: ' + id)
        query_result = query.filter_by(id=id).first()
        return query_result


class Mutation(graphene.ObjectType):
    """Mutations which can be performed by this API."""
    # Account mutation
    createAccount = schema_account.CreateAccount.Field()
    updateAccount = schema_account.UpdateAccount.Field()
    deleteAccount = schema_account.DeleteAccount.Field()
    # Contact mutation
    createContact = schema_contact.CreateContact.Field()
    updateContact = schema_contact.UpdateContact.Field()
    deleteContact = schema_contact.DeleteContact.Field()
    # Entity mutation
    createEntity = schema_entity.CreateEntity.Field()
    updateEntity = schema_entity.UpdateEntity.Field()
    deleteEntity = schema_entity.DeleteEntity.Field()
    # Code mutation
    createCode = schema_code.CreateCode.Field()
    updateCode = schema_code.UpdateCode.Field()
    deleteCode = schema_code.DeleteCode.Field()
    # Member mutation
    createMember = schema_members.CreateMember.Field()
    deleteMember = schema_members.DeleteMember.Field()
    # Area mutation
    createArea = schema_area.CreateArea.Field()
    updateArea = schema_area.UpdateArea.Field()
    deleteArea = schema_area.DeleteArea.Field()

    # Create MessageSent
    CreateMessage = schema_sent_message.SentMessage.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
# temporal
