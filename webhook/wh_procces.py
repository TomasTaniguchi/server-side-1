from database import base
from database.model_messages import ModelMessages
from webhook.functions_wh import get_node3, create_tickets, update_ticket, send_df_area, send_message_df
from webhook.functions_api_w import sent_payload
from webhook.get_from_db import get_id_name_entity, get_ticket
import sys, traceback
from functools import lru_cache
from eval_func_speed_copy import timerlog
session = base.db_session()



traceback_template = '''Traceback (most recent call last):
  File "%(filename)s", line %(lineno)s, in %(id_name)s
%(type)s: %(message)s\n''' # Skipping the "actual line" item

def message_sent(payload):
    message = payload['message']
    messages = ModelMessages(**message)
    session.add(messages)
    return

@timerlog
def message_received(payload):
    print("message_received")
    message = payload['message']
    phone_id = str(payload['phone_id'])
    id_message = message['id']
    node2 = get_id_name_entity(session, phone_id)
    user = payload['user']
    id_user = user['id']
    exists = get_ticket(session, id_user, node2)
    tickets_id = build_tickets(session=session, id_message=id_message, payload=payload, exists=exists, node2=node2, phone_id=phone_id)
    message['tickets_id'] = tickets_id
    messages = ModelMessages(**message)
    session.add(messages)
    session.commit()

    return


def act(payload):
    #print(payload)
    pass

def build_tickets(**kwargs):
    payload = kwargs.get('payload')
    node2 = kwargs.get('node2')
    session = kwargs.get('session')
    phone_id = kwargs.get('phone_id')
    payload['phone_id'] = phone_id
    exists = kwargs.get('exists')
    id_message = kwargs.get('id_message')
    try:
        user = payload['user']
        id_user = user['id']
        name = user['name']
        image = user['image']
        timestamp = int(payload['timestamp'])
        phone_destination = user['phone']
        last_id_msg = payload['message']['id']
        phone_num = user['phone']
        node3 = get_node3(session, payload, node2)

        tk = False
        for tk in exists:
            tk = tk.id
            break

        payload_tk = {'id_tk': id_user, 'phone_id': phone_id, 'phone': phone_num, \
                      'node2': node2, 'node3': "", 'node4': "", \
                      'timestamp': timestamp, 'last_id_msg': last_id_msg, 'id_name': name, 'image': image}

        if not tk:
            if node3:
                payload['user']['node3'] = node3
                payload_tk['node3'] = node3

            payload['user']['node2'] = node2

            new_tk = create_tickets(session, payload)
            session = new_tk[0]
            id = new_tk[1]
            payload_tk['id'] = id
            response = sent_payload(payload_tk)
            check_response(response)

            if node3:
                send_df_area(session, phone_id, phone_destination, node2, node3)
            else:
                send_message_df(session, phone_id, phone_destination, node2)

        else:
            node3_exist = False
            create_new_tk = True
            for tk in exists:
                if tk.node3 != "":
                    node3_exist = True
                if node3 and node3 == tk.node3:
                    #if node3 == tk.node3:
                    create_new_tk = False
            if node3_exist:
                for tk in exists:
                    if not node3 and tk.current:
                        tk.timestamp = timestamp
                        tk.last_id_msg = last_id_msg
                        session = update_ticket(session, tk)
                        id = tk.id
                        db_node3 = tk.node3
                        payload_tk['id'] = id
                        payload_tk['node3'] = db_node3
                        response = sent_payload(payload_tk)
                        check_response(response)
                        break

                    if node3 == tk.node3:
                        session = set_current_false(session, exists)
                        tk.timestamp = timestamp
                        tk.last_id_msg = last_id_msg
                        tk.current = 1
                        session = update_ticket(session, tk)
                        id = tk.id
                        payload_tk['id'] = id
                        payload_tk['node3'] = node3
                        response = sent_payload(payload_tk)
                        check_response(response)
                        send_df_area(session, phone_id, phone_destination, node2, node3)
                        break

            if not node3_exist:
                for tk in exists:
                    if not node3:
                        if tk.current:
                            session = update_ticket(session, tk)
                            id = tk.id
                            payload_tk['id'] = id
                            response = sent_payload(payload_tk)
                            check_response(response)
                            send_message_df(session, phone_id, phone_destination, node2)
                            break

            if create_new_tk and node3:
                payload['user']['node2'] = node2
                payload['user']['node3'] = node3
                session = set_current_false(session, exists)
                new_tk = create_tickets(session, payload)
                session = new_tk[0]
                id = new_tk[1]
                payload_tk['id'] = id
                payload_tk['node3'] = node3
                response = sent_payload(payload_tk)
                check_response(response)
                send_df_area(session, phone_id, phone_destination, node2, node3)


    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()  # most recent (if any) by default

        traceback_details = {
            'filename': exc_traceback.tb_frame.f_code.co_filename,
            'lineno': exc_traceback.tb_lineno,
            'id_name': exc_traceback.tb_frame.f_code.co_name,
            'type': exc_type.__name__,
            'message': str(exc_value),  # or see traceback._some_str()
        }

        del (exc_type, exc_value, exc_traceback)

        print(traceback.format_exc())
        print(traceback_template % traceback_details)


    finally:
        
        return payload_tk['id']


def set_current_false(session, tks):
    for tk in tks:
        tk.current = 0
        session.merge(tk)
    return session



def check_response(response):
    print(response)