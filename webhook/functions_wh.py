from database.model_code import ModelCode
from database.model_tickets import ModelTickets
from webhook.get_from_db import get_list_area_name, get_default_msg, get_default_msg_area, get_sent_list_area
from webhook.functions_api_w import sent_message


def check_area(session, msg_text, id_name_entity):
    msg_text += " " # para cuando la palabra esta al final de la cadena
    if "#" in msg_text:
        max_char_length = 18  # from model_area len(name_area) + 3 ("#"start, " "end, another space for the selection)
        char_start_position = msg_text.find("#")
        char_end_position = char_start_position + msg_text[char_start_position:char_start_position+max_char_length].find(" ")
        node3 = msg_text[char_start_position:char_end_position]
        areas = get_list_area_name(session, id_name_entity)[1]
        try:
            index = areas.index(node3)
            return areas[index]
        except ValueError:
            return False
    else:
        return False


def send_message_df(session, id_phone, phone_destination, id_name_entity):

    sent_list = get_list_area_name(session,id_phone)
    if sent_list:
        send_msg_areas_df(session, id_phone, phone_destination, id_name_entity)
    else:
        send_only_msg_df(session, id_phone, phone_destination)


def send_msg_areas_df(session, phone_id, phone_destination, id_name_entity):

    areas = get_list_area_name(session, id_name_entity)[0]
    print("2 phone_id: ", phone_id)
    default_msg = get_default_msg(session, phone_id)
    message = default_msg + "\n" + areas
    response = sent_message(phone_id, phone_destination, message)
    check_response(response)


def send_only_msg_df(session, phone_id, phone_destination):

    print("1 phone_id: ", phone_id)
    default_msg = get_default_msg(session, phone_id)
    response = sent_message(phone_id, phone_destination, default_msg)
    check_response(response)


def send_df_area(session, phone_id, phone_destination, id_name_entity, area):

    default_msg = get_default_msg_area(session, id_name_entity, area)
    print("3 phone_id: ", phone_id)
    response = sent_message(phone_id, phone_destination, default_msg)
    check_response(response)


def check_response(response):

    print(response)


def create_tickets(session, body):

    last_id_msg = body['message']['id']
    product_id_value = body['product_id']
    user = body['user']
    user['product_id'] = product_id_value
    user['phone_id'] = str(body['phone_id'])
    user['id_tk'] = body['user']['id']
    del user['id']
    user['timestamp'] = int(body['timestamp'])
    user['last_id_msg'] = last_id_msg
    tickets = ModelTickets(**user)
    session.add(tickets)
    session.flush()
    return session, tickets.id


def get_node3(session, body, id_name_entity):

    node3 = False
    if body['message']['type'] == 'text':
        chain = body['message']['text']
        area = check_area(session, chain, id_name_entity)
        if area:
            node3 = area
    return node3


def update_ticket(session, result):
    count = result.count
    count += 1
    result.count = count
    session.merge(result)
    return session
