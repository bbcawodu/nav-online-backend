from orm_models.base import current_intent_formula
from orm_models.base import PRESENCE_INTENT_KEYWORDS

from orm_models.blocking.base import filter_query_obj_by_id
from orm_models.blocking.base import create_response_list_from_query_object
from orm_models.blocking.base import INTENT_KEYWORD_FIELD_NAMES_W_TYPES


class BaseClassForTableWithIntentFields(object):
    intent_keywords = PRESENCE_INTENT_KEYWORDS

    @classmethod
    def retrieve_table_data_by_id(cls, db_session, validated_GET_rqst_params, rqst_id, rqst_list_of_ids, rqst_errors):
        query_obj = filter_query_obj_by_id(db_session.query(cls), cls, rqst_id, rqst_list_of_ids)

        query_obj = filter_query_obj_by_secondary_params(validated_GET_rqst_params, query_obj, cls)

        response_list = create_response_list_from_query_object(query_obj)

        def check_query_obj_for_requested_data():
            if not response_list:
                rqst_errors.append("No {} rows in db for given ids".format(cls.__tablename__))
            else:
                if rqst_list_of_ids:
                    for db_id in rqst_list_of_ids:
                        tuple_of_bools_if_id_in_data = (row_data['id'] == db_id for row_data in response_list)
                        if not any(tuple_of_bools_if_id_in_data):
                            rqst_errors.append('{} row with id: {} not found in database'.format(cls.__tablename__, db_id))

        check_query_obj_for_requested_data()

        return response_list


BaseClassForTableWithIntentFields.current_intent = property(current_intent_formula)


def filter_query_obj_by_secondary_params(validated_GET_rqst_params, query_obj, obj_model):
    if 'min_date' in validated_GET_rqst_params:
        rqst_min_date = validated_GET_rqst_params['min_date'].replace(hour=0, minute=0)

        if hasattr(obj_model, 'date_last_updated'):
            query_obj = query_obj.filter(obj_model.date_last_updated >= rqst_min_date)
        elif hasattr(obj_model, 'date_created'):
            query_obj = query_obj.filter(obj_model.date_created >= rqst_min_date)
    if 'max_date' in validated_GET_rqst_params:
        rqst_max_date = validated_GET_rqst_params['max_date'].replace(hour=23, minute=59)

        if hasattr(obj_model, 'date_last_updated'):
            query_obj = query_obj.filter(obj_model.date_last_updated <= rqst_max_date)
        elif hasattr(obj_model, 'date_created'):
            query_obj = query_obj.filter(obj_model.date_created <= rqst_max_date)

    for intent_keyword in PRESENCE_INTENT_KEYWORDS:
        for field_name, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
            keyword_field_name = "{}_{}".format(intent_keyword, field_name)

            if keyword_field_name in validated_GET_rqst_params:
                rqst_keyword_value = validated_GET_rqst_params[keyword_field_name]

                query_obj = query_obj.filter(getattr(obj_model, keyword_field_name) >= rqst_keyword_value)

    return query_obj
