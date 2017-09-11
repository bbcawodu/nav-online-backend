from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy_blocking_orm_models import DeclarativeBase

from base import BaseClassForTableWithIntentFields
from base import add_intent_keyword_fields_to_db_table
from base import INTENT_KEYWORDS
from base import INTENT_KEYWORD_FIELD_NAMES_W_TYPES


class PresenceBrowsingIntentSnaphot(DeclarativeBase, BaseClassForTableWithIntentFields):
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

        for intent_keyword in INTENT_KEYWORDS:
            for field_name, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
                keyword_field_name = "{}_{}".format(intent_keyword, field_name)
                values_dict[keyword_field_name] = getattr(self, keyword_field_name)

        return values_dict


PresenceBrowsingIntentSnaphot = add_intent_keyword_fields_to_db_table(PresenceBrowsingIntentSnaphot)
