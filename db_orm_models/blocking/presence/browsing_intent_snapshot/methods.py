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