from flask import Flask, request, abort

from database import base
from database.model_messages import ModelMessages
from database.model_tickets import ModelTickets
from database.model_code import ModelCode
from database.model_activity import ModelActivity
import multiprocessing
from utils.rx_test import Observable
from utils.rx_test import ThreadPoolScheduler

optimal_thread_count = multiprocessing.cpu_count() + 1
poo_scheduler = ThreadPoolScheduler(optimal_thread_count)
print(optimal_thread_count)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print("webhook")
    if request.method == 'POST':
        def is_activity():
            return Observable.of(request.json).map(lambda i: (i['type']))

        is_activity().take_while(lambda i: i == "ack") \
            .map(lambda i: act()).subscribe()
        is_activity().take_while(lambda i: i == "message") \
            .map(lambda i: messenger()).subscribe()

        return '', 200

        abort(400)


def build_tickets(id_message):
    body = request.json
    user = request.json['user']
    id_user = user['id']
    exists = base.db_session.query(ModelTickets.id).filter_by(id=id_user).scalar() is not None
    base.db_session.remove()
    if not exists:
        print('new entry')
        product_id_value = body['product_id']
        phone_id_value = body['phone_id']
        user['product_id'] = product_id_value
        user['phone_id'] = phone_id_value
        get_entity = base.db_session.query(ModelCode.id_name_entity).filter_by(phone_id=phone_id_value).first()
        get_entity = get_entity.id_name_entity
        user['node2'] = get_entity
        #sent_list = base.db_session.query(ModelCode.id_name_entity).filter_by(phone_id=phone_id_value).first()
        tickets = ModelTickets(**user)
        base.db_session.add(tickets)
        base.db_session.commit()
        build_activity(id_user, id_message, 'new_message', 1)
    else:
        print('Edit entry')
        result = base.db_session.query(ModelTickets).get(id_user)
        base.db_session.remove()
        count = result.count
        count += 1
        result.count = count
        base.db_session.merge(result)

        base.db_session.commit()
        build_activity(result.id, id_message, 'new_message', 1)
        # base.db_session.flush()
        # es importante borrar esto en algun momento
        result = base.db_session.query(ModelTickets).get(id_user)
        base.db_session.remove()
        print(result.count)
    return

def build_activity(id_ticket, id_message, type_act, count):
    activity = {'tickets_id': id_ticket, 'message_id': id_message, 'type': type_act, 'count': count}
    print(activity)
    activity_model = ModelActivity(**activity)
    base.db_session.add(activity_model)
    base.db_session.commit()


def message_sent():
    print("es un mensaje enviado")
    print(request.json)
    message = request.json['message']
    messages = ModelMessages(**message)
    base.db_session.add(messages)
    base.db_session.commit()


def message_received():
    print(request.json)
    print("es un mensaje recibido")
    message = request.json['message']
    id_message = message['id']
    messages = ModelMessages(**message)
    base.db_session.add(messages)
    base.db_session.commit()
    build_tickets(id_message)


def act():
    print("es actividad")
    print(request.json)


def messenger():
    source = Observable.of(request.json).map(lambda i: (i['message']['fromMe'] == True))
    source.take_while(lambda i: i == True) \
        .map(lambda i: message_sent()).subscribe()
    source.take_while(lambda i: i == False) \
        .map(lambda i: message_received()).subscribe()

app.run(host='127.0.0.1', port=8000)
