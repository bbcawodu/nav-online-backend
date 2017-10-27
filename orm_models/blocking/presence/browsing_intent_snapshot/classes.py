from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text

from orm_models.base import PRESENCE_INTENT_KEYWORDS

from orm_models.blocking.base import DeclarativeBase
from orm_models.blocking.base import add_intent_keyword_fields_to_db_table
from orm_models.blocking.base import INTENT_KEYWORD_FIELD_NAMES_W_TYPES
from orm_models.blocking.base import create_response_list_from_query_object

from orm_models.blocking.presence.base import BaseClassForTableWithIntentFields
from orm_models.blocking.presence.base import filter_query_obj_by_secondary_params

from methods import filter_query_obj_by_session_id
from methods import filter_query_obj_by_intent


class PresenceBrowsingIntentSnapshot(DeclarativeBase, BaseClassForTableWithIntentFields):
    __tablename__ = 'presence_browsing_intent_snapshot'

    id = Column(Integer, primary_key=True)
    presence_browsing_session_data_id = Column(Integer, ForeignKey('presencebrowsingdata.id'))

    date_created = Column(DateTime)
    calculated_intent = Column(Text)
    intent_formula_version = Column(Text)

    def return_values_dict(self):
        values_dict = {
            "id": self.id,
            "session_id": self.presence_browsing_session_data_id,
            "calculated_intent": self.calculated_intent,
            "intent_formula_version": self.intent_formula_version
        }

        if self.date_created:
            values_dict["date_created"] = self.date_created.isoformat()

        for intent_keyword in self.intent_keywords:
            for field_name, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
                keyword_field_name = "{}_{}".format(intent_keyword, field_name)
                values_dict[keyword_field_name] = getattr(self, keyword_field_name)

        return values_dict

    @classmethod
    def retrieve_table_data_by_session_id(cls, db_session, validated_GET_rqst_params, rqst_session_id, rqst_list_of_ids, rqst_errors):
        query_obj = filter_query_obj_by_session_id(db_session.query(cls), cls, rqst_session_id, rqst_list_of_ids)

        query_obj = filter_query_obj_by_secondary_params(validated_GET_rqst_params, query_obj, cls)

        response_list = create_response_list_from_query_object(query_obj)

        def check_query_obj_for_requested_data():
            if not response_list:
                rqst_errors.append("No {} rows in db for given browsing session data ids".format(cls.__tablename__))
            else:
                if rqst_list_of_ids:
                    for session_id in rqst_list_of_ids:
                        tuple_of_bools_if_id_in_data = (row_data['session_id'] == session_id for row_data in response_list)
                        if not any(tuple_of_bools_if_id_in_data):
                            rqst_errors.append('{} row with browsing session data id: {} not found in database'.format(cls.__tablename__, session_id))

        check_query_obj_for_requested_data()

        return response_list

    @classmethod
    def retrieve_table_data_by_intent(cls, db_session, validated_GET_rqst_params, rqst_intent, rqst_errors):
        query_obj = filter_query_obj_by_intent(db_session.query(cls), cls, rqst_intent)

        query_obj = filter_query_obj_by_secondary_params(validated_GET_rqst_params, query_obj, cls)

        response_list = create_response_list_from_query_object(query_obj)

        def check_response_data_for_requested_data():
            if not response_list:
                rqst_errors.append("No {} rows in db for given browsing session data intent".format(cls.__tablename__))

        check_response_data_for_requested_data()

        return response_list


PresenceBrowsingIntentSnapshot = add_intent_keyword_fields_to_db_table(PresenceBrowsingIntentSnapshot, PRESENCE_INTENT_KEYWORDS)
