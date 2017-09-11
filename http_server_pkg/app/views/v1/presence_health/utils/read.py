from sqlalchemy_blocking_orm_models.presence_db_models import PresenceBrowsingData
from sqlalchemy_blocking_orm_models.presence_db_models import PresenceBrowsingIntentSnaphot
from sqlalchemy_blocking_orm_models.presence_db_models import INTENT_KEYWORDS
from sqlalchemy_blocking_orm_models.presence_db_models import INTENT_KEYWORD_FIELD_NAMES_W_TYPES


def filter_query_obj_by_id(query_obj, obj_model, rqst_id, list_of_ids):
    if isinstance(rqst_id, unicode) and rqst_id.lower() == "all":
        query_obj = query_obj.order_by(obj_model.id)
    else:
        query_obj = query_obj.filter(obj_model.id.in_(list_of_ids)).order_by(obj_model.id)

    return query_obj


def filter_query_obj_by_session_id(query_obj, obj_model, rqst_session_id, list_of_ids):
    if isinstance(rqst_session_id, unicode) and rqst_session_id.lower() == "all":
        query_obj = query_obj.order_by(obj_model.presence_browsing_session_data_id)
    else:
        query_obj = query_obj.filter(obj_model.presence_browsing_session_data_id.in_(list_of_ids)).\
            order_by(obj_model.presence_browsing_session_data_id)

    return query_obj


def filter_query_obj_by_intent(query_obj, obj_model, rqst_intent):
    query_obj = query_obj.filter(obj_model.calculated_intent == rqst_intent).order_by(obj_model.presence_browsing_session_data_id)

    return query_obj


def filter_query_obj_by_secondary_params(validated_GET_rqst_params, query_obj, obj_model):
    if 'min_date' in validated_GET_rqst_params:
        rqst_min_date = validated_GET_rqst_params['min_date'].replace(hour=23, minute=59)

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

    for intent_keyword in INTENT_KEYWORDS:
        for field_name, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
            keyword_field_name = "{}_{}".format(intent_keyword, field_name)

            if keyword_field_name in validated_GET_rqst_params:
                rqst_keyword_value = validated_GET_rqst_params[keyword_field_name]

                query_obj = query_obj.filter(getattr(obj_model, keyword_field_name) >= rqst_keyword_value)

    return query_obj


def create_response_list_from_query_object(query_obj):
    return_list = []

    for db_instance in query_obj:
        return_list.append(db_instance.return_values_dict())

    return return_list


def retrieve_browsing_session_data_by_id(db_session, validated_GET_rqst_params, rqst_id, rqst_list_of_ids, rqst_errors):
    browsing_session_query_obj = filter_query_obj_by_id(db_session.query(PresenceBrowsingData), PresenceBrowsingData, rqst_id, rqst_list_of_ids)

    browsing_session_query_obj = filter_query_obj_by_secondary_params(validated_GET_rqst_params, browsing_session_query_obj, PresenceBrowsingData)

    response_list = create_response_list_from_query_object(browsing_session_query_obj)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No browsing session data rows in db for given ids")
        else:
            if rqst_list_of_ids:
                for db_id in rqst_list_of_ids:
                    tuple_of_bools_if_id_in_data = (row_data['id'] == db_id for row_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Browsing session data row with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def retrieve_browsing_session_intent_snapshot_data_by_id(db_session, validated_GET_rqst_params, rqst_id, rqst_list_of_ids, rqst_errors):
    intent_snapshot_query_obj = filter_query_obj_by_id(db_session.query(PresenceBrowsingIntentSnaphot), PresenceBrowsingIntentSnaphot, rqst_id, rqst_list_of_ids)

    intent_snapshot_query_obj = filter_query_obj_by_secondary_params(validated_GET_rqst_params, intent_snapshot_query_obj, PresenceBrowsingIntentSnaphot)

    response_list = create_response_list_from_query_object(intent_snapshot_query_obj)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No intent snapshot rows in db for given ids")
        else:
            if rqst_list_of_ids:
                for db_id in rqst_list_of_ids:
                    tuple_of_bools_if_id_in_data = (row_data['id'] == db_id for row_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Intent snapshot row with id: {} not found in database'.format(db_id))

    check_response_data_for_requested_data()

    return response_list


def retrieve_browsing_session_intent_snapshot_data_by_session_id(db_session, validated_GET_rqst_params, rqst_session_id, rqst_list_of_ids, rqst_errors):
    intent_snapshot_query_obj = filter_query_obj_by_session_id(db_session.query(PresenceBrowsingIntentSnaphot), PresenceBrowsingIntentSnaphot, rqst_session_id, rqst_list_of_ids)

    intent_snapshot_query_obj = filter_query_obj_by_secondary_params(validated_GET_rqst_params, intent_snapshot_query_obj, PresenceBrowsingIntentSnaphot)

    response_list = create_response_list_from_query_object(intent_snapshot_query_obj)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No intent snapshot rows in db for given browsing session data ids")
        else:
            if rqst_list_of_ids:
                for session_id in rqst_list_of_ids:
                    tuple_of_bools_if_id_in_data = (row_data['session_id'] == session_id for row_data in response_list)
                    if not any(tuple_of_bools_if_id_in_data):
                        rqst_errors.append('Intent snapshot row with browsing session data id: {} not found in database'.format(session_id))

    check_response_data_for_requested_data()

    return response_list


def retrieve_browsing_session_intent_snapshot_data_by_intent(db_session, validated_GET_rqst_params, rqst_intent, rqst_errors):
    intent_snapshot_query_obj = filter_query_obj_by_intent(db_session.query(PresenceBrowsingIntentSnaphot), PresenceBrowsingIntentSnaphot, rqst_intent)

    intent_snapshot_query_obj = filter_query_obj_by_secondary_params(validated_GET_rqst_params, intent_snapshot_query_obj, PresenceBrowsingIntentSnaphot)

    response_list = create_response_list_from_query_object(intent_snapshot_query_obj)

    def check_response_data_for_requested_data():
        if not response_list:
            rqst_errors.append("No intent snapshot rows in db for given browsing session data intent")

    check_response_data_for_requested_data()

    return response_list
