from database import base
from database.model_tickets import ModelTickets
from database.model_area import ModelArea
from database.model_code import ModelCode
from functools import lru_cache
from eval_func_speed import runtime_log

@runtime_log
#@lru_cache()
def get_list_area_name(session, id_name_entity):
    get_list = session.query(ModelArea.name_area).filter_by(fk_id_entity=id_name_entity)
    areas = ""
    list_area = []
    for i in get_list:
        area = i.name_area
        list_area.append(area)
        area = area + "\n"
        areas += area
    return areas, list_area

@runtime_log
#@lru_cache()
def get_id_name_entity(session, phone_id):
    get_entity = session.query(ModelCode.id_name_entity).filter_by(phone_id=phone_id).first()
    return get_entity.id_name_entity

@runtime_log
#@lru_cache()
def get_default_msg(session, phone_id):
    default_msg = session.query(ModelCode.default_message).filter_by(phone_id=phone_id).first()
    return default_msg.default_message

@runtime_log
#@lru_cache()
def get_default_msg_area(session, id_name_entity, area):
    default_msg = session.query(ModelArea.default_message).filter_by(fk_id_entity=id_name_entity,
                                                                     name_area=area).first()
    return default_msg.default_message
@runtime_log
#@lru_cache()
def get_sent_list_area(session, phone_id):
    sent_msg_df_list = session.query(ModelCode.sent_area).filter_by(phone_id=phone_id).first()
    return sent_msg_df_list.sent_area

@runtime_log
def get_ticket(session, id_user, node2):
    exists = session.query(ModelTickets).filter_by(id_tk=id_user, node2=node2)
    return exists
