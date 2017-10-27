from sys import maxint


CURRENT_INTENT_FORMULA_VERSION = "1.0"

KEYWORD_RECORDING_TYPES = [
    "clicks",
    "hover_time"
]

PRESENCE_INTENT_KEYWORDS = [
    'oncology'
]


def current_intent_formula(self):
    max_intent_index_entry = {
        "keyword": None,
        "clicks": -maxint - 1,
        "hover_time": -maxint - 1,
        "intent_index": -maxint - 1
    }

    for keyword in self.intent_keywords:
        keyword_clicks = getattr(self, "{}_{}".format(keyword, "clicks"))
        keyword_hover_time = getattr(self, "{}_{}".format(keyword, "hover_time"))
        keyword_data_list_entry = {"keyword": keyword,
                                   "clicks": keyword_clicks,
                                   "hover_time": keyword_hover_time,
                                   "intent_index": 10 * keyword_clicks + keyword_hover_time}

        max_intent_index_entry = max(max_intent_index_entry, keyword_data_list_entry,
                                     key=lambda entry: entry['intent_index'])

    return max_intent_index_entry["keyword"]