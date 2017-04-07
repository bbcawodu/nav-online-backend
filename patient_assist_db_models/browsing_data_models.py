from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from patient_assist_db_models import DeclarativeBase
from patient_assist_db_models import BROWSING_KEYWORDS
from patient_assist_db_models import BROWSING_DATA_FIELDS
from sys import maxint


class BaseBrowsingDataClass(object):
    @property
    def current_intent(self):
        max_intent_index_entry = {"keyword": None,
                                  "clicks": -maxint - 1,
                                  "hover_time": -maxint - 1,
                                  "intent_index": -maxint - 1}

        for keyword in BROWSING_KEYWORDS:
            keyword_clicks = getattr(self, "{}_{}".format(keyword, "clicks"))
            keyword_hover_time = getattr(self, "{}_{}".format(keyword, "hover_time"))
            keyword_data_list_entry = {"keyword": keyword,
                                       "clicks": keyword_clicks,
                                       "hover_time": keyword_hover_time,
                                       "intent_index": 10 * keyword_clicks + keyword_hover_time}

            max_intent_index_entry = max(max_intent_index_entry, keyword_data_list_entry,
                                         key=lambda entry: entry['intent_index'])

        return max_intent_index_entry["keyword"]


def add_browsing_data_fields(browsing_data_table_class):
    for browsing_keword in BROWSING_KEYWORDS:
        for field, field_type in BROWSING_DATA_FIELDS.items():
            setattr(browsing_data_table_class, "{}_{}".format(browsing_keword, field), field_type)

    return browsing_data_table_class


class PresenceBrowsingData(DeclarativeBase, BaseBrowsingDataClass):
    __tablename__ = 'presencebrowsingdata'

    id = Column(Integer, primary_key=True)
    cookie_id = Column(String(10000))
    send_cta_updates = Column(Boolean)


PresenceBrowsingData = add_browsing_data_fields(PresenceBrowsingData)
