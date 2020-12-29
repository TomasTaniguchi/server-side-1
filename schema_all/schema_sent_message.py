import graphene
import time
import multiprocessing
from rx import Observable
from rx.concurrency import ThreadPoolScheduler
from webhook import wh_procces
optimal_thread_count = multiprocessing.cpu_count() + 1
poo_scheduler = ThreadPoolScheduler(optimal_thread_count)
from graphene_sqlalchemy import SQLAlchemyObjectType
from functions.general_purpose import create_unique_id
from database import base
from database.model_messages import ModelMessages
from database.model_tickets import ModelTickets
from database.model_account import ModelAccount
import utils
from class_api.data_subcription_tk import PayloadSubTk

class NewMessageAttribute:
    tickets_id = graphene.String(description="id of the ticket")
    type = graphene.String(required=True, description="type of message")
    text = graphene.String( description=" text of message")
    fromMe = graphene.Boolean(description="source of the msg")
    mime = graphene.String(description="format of the media data")
    url = graphene.String(description="url of file or media msg")
    caption = graphene.String(description="caption of message")
    filename = graphene.String(description="file id_name")
    payload = graphene.String(description="Latitude and longitude")
    vcardList = graphene.String(description="List of the vcard")
    timestamp = graphene.Int(description="Record timestamp.")


class NewTicketAttribute:
    id = graphene.Int(description="unique Id of the ticket.")
    id_tk = graphene.String(required=True, description="Id of the ticket")
    phone_id = graphene.String(description="Id of the destination code.")
    node2 = graphene.String(description="@Entity")
    node3 = graphene.String(description="#Area")
    node4 = graphene.String(description=".account")
    phone = graphene.String(description="phone number if the code have one")
    name = graphene.String(description="id_name of the contact what doing the entry")
    image = graphene.String(description="Link of the contact profile picture")
    last_id_msg = graphene.String(description="last message id")
    timestamp = graphene.Int(description="Record timestamp.")


class NewMessage(SQLAlchemyObjectType):
    """Message node."""

    class Meta:
        model = ModelMessages
        interfaces = (graphene.relay.Node,)


class NewTicket(SQLAlchemyObjectType):
    """Ticket node."""

    class Meta:
        model = ModelTickets
        interfaces = (graphene.relay.Node,)


class IdAccountInput(graphene.InputObjectType):
    id = graphene.String(required=True, description="id of the account")
    pass


class BuildTicketInput(graphene.InputObjectType, NewTicketAttribute):
    """Arguments to create a tickets."""
    pass


class BuildMessageInput(graphene.InputObjectType, NewMessageAttribute):
    """Arguments to create a message."""
    pass


class SentMessage(graphene.Mutation):
    message = graphene.Field(lambda: NewMessage, description="Message created by this mutation.")
    ticket = graphene.Field(lambda: NewTicket, description="Ticket created by this mutation.")

    class Arguments:
        message_data = BuildMessageInput(required=True)
        ticket_data = BuildTicketInput(required=True)
        id_account = IdAccountInput(required=True)

    def mutate(self, info, message_data=None, ticket_data=None, id_account=None):
        session = base.db_session()
        print("id accound: ", id_account['id'])
        id_account = utils.input_to_dictionary(id_account)
        print(id_account)
        print("ticket_data: ", ticket_data)

        def try_to_get_id(session, **kwargs):
            tks_column  = {'id_tk': '', 'node2': '', 'node3': '', 'node4': ''}
            for tk in tks_column:
                tks_column[tk] = kwargs.get(tk)

            id_in_tk = session.query(ModelTickets.id).filter_by(id_tk = tks_column['id_tk'],\
                                                                node2 = tks_column['node2'],\
                                                                node3 = tks_column['node3'],
                                                                node4 = tks_column['node4']).first()

            if not id_in_tk:
                print("we don't get the id")
                return None

            return id_in_tk.id

        if 'id' not in ticket_data:
            id = try_to_get_id(session, **payload_tk)
            ticket_data['id'] = id

        print("id in tk : ", ticket_data['id'])

        current_time = round(time.time())
        type_msg = message_data['type']
        id_tk = ticket_data['id_tk']
        id_msg = create_unique_id(id_tk)
        message_data['id'] = id_msg

        ticket_data['timestamp'] = current_time
        ticket_data['last_id_msg'] = id_msg
        if ticket_data['id'] == None:
            if 'phone' != ticket_data:
                account_data = session.query(ModelAccount).filter_by(id=id_account['id']).first()
            ticket_data['name'] = account_data.name
            ticket_data['image'] = account_data.profile_img

            ticket = ModelTickets(**ticket_data)
            session.add(ticket)
            session.flush()
            id_from_tk = ticket.id
        else:
            print("we are in update")
            del ticket_data['id_tk']
            ticket = ModelTickets(**ticket_data)
            session.merge(ticket)
            id_from_tk = ticket.id

        ticket_data['id'] = id_from_tk

        payload_tk = {'id_tk': "", 'phone_id': "", 'phone': "",\
                      'node2': "", 'node3': "", 'node4': "",\
                      'timestamp': "", 'last_id_msg': "",\
                      'id_name': "", 'image': "", 'id': "" }

        for key in ticket_data:
            if ticket_data[key] != None:
                payload_tk[key] = ticket_data[key]

        PayloadSubTk.received_data(ticket_data['id'], payload_tk)
        message_data['timestamp'] = ticket_data['timestamp']
        message_data['tickets_id'] = ticket_data['id']
        message = ModelMessages(**message_data)
        session.add(message)

        session.commit()

        if 'phone' == ticket_data:
            print("sent Message whatsapp")
            #Observable.of().map(lambda i: (i['type'])) \
            #    .map(lambda i: ).subscribe_on(poo_scheduler).subscribe()

        return SentMessage(message=message, ticket= ticket)

