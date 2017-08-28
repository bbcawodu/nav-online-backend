from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sys import maxint

INTENT_KEYWORDS = ['oncology']

INTENT_KEYWORD_FIELD_NAMES_W_TYPES = {
                            "clicks": Column(Integer),
                            "hover_time": Column(Float)
                        }


class BaseClassForTableWithIntentFields(object):
    @property
    def current_intent(self):
        max_intent_index_entry = {"keyword": None,
                                  "clicks": -maxint - 1,
                                  "hover_time": -maxint - 1,
                                  "intent_index": -maxint - 1}

        for keyword in INTENT_KEYWORDS:
            keyword_clicks = getattr(self, "{}_{}".format(keyword, "clicks"))
            keyword_hover_time = getattr(self, "{}_{}".format(keyword, "hover_time"))
            keyword_data_list_entry = {"keyword": keyword,
                                       "clicks": keyword_clicks,
                                       "hover_time": keyword_hover_time,
                                       "intent_index": 10 * keyword_clicks + keyword_hover_time}

            max_intent_index_entry = max(max_intent_index_entry, keyword_data_list_entry,
                                         key=lambda entry: entry['intent_index'])

        return max_intent_index_entry["keyword"]


def add_intent_keyword_fields_to_db_table(class_for_table):
    for intent_keyword in INTENT_KEYWORDS:
        for field_name, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
            setattr(class_for_table, "{}_{}".format(intent_keyword, field_name), field_type)

    return class_for_table
