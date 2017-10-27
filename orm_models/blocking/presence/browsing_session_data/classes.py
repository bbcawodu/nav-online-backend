from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from orm_models.base import PRESENCE_INTENT_KEYWORDS

from orm_models.blocking.base import DeclarativeBase
from orm_models.blocking.base import add_intent_keyword_fields_to_db_table
from orm_models.blocking.base import INTENT_KEYWORD_FIELD_NAMES_W_TYPES

from orm_models.blocking.presence.base import BaseClassForTableWithIntentFields


class PresenceBrowsingData(DeclarativeBase, BaseClassForTableWithIntentFields):
    __tablename__ = 'presencebrowsingdata'

    id = Column(Integer, primary_key=True)
    browsing_intent_snapshots = relationship("PresenceBrowsingIntentSnapshot", backref="presence_browsing_session_data_row")

    date_created = Column(DateTime)
    date_last_updated = Column(DateTime)

    def return_values_dict(self):
        values_dict = {
            "id": self.id,
            "current_intent": self.current_intent
        }

        if self.date_created:
            values_dict["date_created"] = self.date_created.isoformat()

        if self.date_last_updated:
            values_dict["date_last_updated"] = self.date_last_updated.isoformat()

        for intent_keyword in self.intent_keywords:
            for field_name, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
                keyword_field_name = "{}_{}".format(intent_keyword, field_name)
                values_dict[keyword_field_name] = getattr(self, keyword_field_name)

        return values_dict


PresenceBrowsingData = add_intent_keyword_fields_to_db_table(PresenceBrowsingData, PRESENCE_INTENT_KEYWORDS)
