import copy

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy.ext.declarative import declarative_base


# Use this object to define database schema
# docs: http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
DeclarativeBase = declarative_base()

INTENT_KEYWORD_FIELD_NAMES_W_TYPES = {
    "clicks": Column(Integer),
    "hover_time": Column(Float)
}


def add_intent_keyword_fields_to_db_table(class_for_table, intent_keywords):
    for intent_keyword in intent_keywords:
        for field_name, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
            setattr(class_for_table, "{}_{}".format(intent_keyword, field_name), copy.deepcopy(field_type))

    return class_for_table


def filter_query_obj_by_id(query_obj, obj_model, rqst_id, list_of_ids):
    if isinstance(rqst_id, unicode) and rqst_id.lower() == "all":
        query_obj = query_obj.order_by(obj_model.id)
    else:
        query_obj = query_obj.filter(obj_model.id.in_(list_of_ids)).order_by(obj_model.id)

    return query_obj


def create_response_list_from_query_object(query_obj):
    return_list = []

    for db_instance in query_obj:
        return_list.append(db_instance.return_values_dict())

    return return_list
