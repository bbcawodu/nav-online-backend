from datetime import datetime

from flask.views import MethodView
from orm_models.base import KEYWORD_RECORDING_TYPES

from http_server_pkg.app import app
from http_server_pkg.app import db
from http_server_pkg.app.views.v1.utils import JSONGETRspMixin
from orm_models.blocking.presence import PRESENCE_INTENT_KEYWORDS
from orm_models.blocking.presence import PresenceBrowsingData
from orm_models.blocking.presence import PresenceBrowsingIntentSnapshot


def set_intent_keyword_accepted_http_get_params_for_class_view(class_based_view):
    for intent_keyword in PRESENCE_INTENT_KEYWORDS:
        for field_type in KEYWORD_RECORDING_TYPES:
            keyword_field_name = "{}_{}".format(intent_keyword, field_type)
            class_based_view.accepted_GET_request_parameters.append(keyword_field_name)


class PresenceBrowsingSessionDataGETEndpoint(MethodView, JSONGETRspMixin):
    def parse_get_params_logic(self, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []
            db_session = db.session()

            if 'id' in validated_GET_rqst_params:
                rqst_id = validated_GET_rqst_params['id']
                rqst_list_of_ids = None

                if rqst_id != 'all':
                    rqst_list_of_ids = validated_GET_rqst_params['id_list']

                data_list = PresenceBrowsingData.retrieve_table_data_by_id(db_session, validated_GET_rqst_params, rqst_id, rqst_list_of_ids, rqst_errors)
            else:
                rqst_errors.append('No valid primary parameters')

            db_session.close()

            for rqst_param, param_value in validated_GET_rqst_params.items():
                if isinstance(param_value, datetime):
                    param_value = param_value.isoformat()

                response_raw_data[rqst_param] = param_value

            # for accepted_param in self.accepted_GET_request_parameters:
            #     response_raw_data[accepted_param] = accepted_param

            # for key, value in GET_PARAMETER_VALIDATION_FUNCTIONS.items():
            #     response_raw_data[key] = key

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    accepted_GET_request_parameters = [
        "id",
        "min_date",
        "max_date",
    ]
    parse_GET_request_and_add_response = parse_get_params_logic


set_intent_keyword_accepted_http_get_params_for_class_view(PresenceBrowsingSessionDataGETEndpoint)


class PresenceBrowsingIntentSnapshotGETEndpoint(MethodView, JSONGETRspMixin):
    def parse_get_params_logic(self, validated_GET_rqst_params, response_raw_data, rqst_errors):
        def retrieve_data_by_primary_params_and_add_to_response():
            data_list = []
            db_session = db.session()

            if 'id' in validated_GET_rqst_params:
                rqst_id = validated_GET_rqst_params['id']
                rqst_list_of_ids = None

                if rqst_id != 'all':
                    rqst_list_of_ids = validated_GET_rqst_params['id_list']

                data_list = PresenceBrowsingIntentSnapshot.retrieve_table_data_by_id(db_session, validated_GET_rqst_params, rqst_id, rqst_list_of_ids, rqst_errors)
            elif 'session_id' in validated_GET_rqst_params:
                rqst_session_id = validated_GET_rqst_params['session_id']
                rqst_list_of_ids = None

                if rqst_session_id != 'all':
                    rqst_list_of_ids = validated_GET_rqst_params['session_id_list']

                data_list = PresenceBrowsingIntentSnapshot.retrieve_table_data_by_session_id(db_session,
                                                                                         validated_GET_rqst_params,
                                                                                         rqst_session_id,
                                                                                         rqst_list_of_ids,
                                                                                         rqst_errors)
            elif 'intent' in validated_GET_rqst_params:
                rqst_intent = validated_GET_rqst_params['intent']

                data_list = PresenceBrowsingIntentSnapshot.retrieve_table_data_by_intent(db_session,
                                                                                     validated_GET_rqst_params,
                                                                                     rqst_intent,
                                                                                     rqst_errors)
            else:
                rqst_errors.append('No valid primary parameters')

            db_session.close()

            response_raw_data['Data'] = data_list

        retrieve_data_by_primary_params_and_add_to_response()

    accepted_GET_request_parameters = [
        "id",
        'session_id',
        'intent',
        "min_date",
        "max_date",
    ]
    parse_GET_request_and_add_response = parse_get_params_logic


set_intent_keyword_accepted_http_get_params_for_class_view(PresenceBrowsingIntentSnapshotGETEndpoint)

app.add_url_rule('/v1/presence_health/browsing_session_data/', view_func=PresenceBrowsingSessionDataGETEndpoint.as_view('presence_browsing_session_data'))
app.add_url_rule('/v1/presence_health/browsing_intent_snapshot/', view_func=PresenceBrowsingIntentSnapshotGETEndpoint.as_view('presence_browsing_intent_snapshot'))
