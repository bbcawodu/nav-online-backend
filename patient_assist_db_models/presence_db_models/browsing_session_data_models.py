from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from patient_assist_db_models import DeclarativeBase
from .base import BaseClassForTableWithIntentFields
from .base import add_intent_keyword_fields_to_db_table


class PresenceBrowsingData(DeclarativeBase, BaseClassForTableWithIntentFields):
    __tablename__ = 'presencebrowsingdata'

    id = Column(Integer, primary_key=True)
    cookie_id = Column(String(10000))
    send_cta_updates = Column(Boolean)


PresenceBrowsingData = add_intent_keyword_fields_to_db_table(PresenceBrowsingData)
