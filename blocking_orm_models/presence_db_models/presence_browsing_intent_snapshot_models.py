from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text

from blocking_orm_models import DeclarativeBase
from .base import BaseClassForTableWithIntentFields
from .base import add_intent_keyword_fields_to_db_table


class PresenceBrowsingIntentSnaphot(DeclarativeBase, BaseClassForTableWithIntentFields):
    __tablename__ = 'presence_browsing_intent_snapshot'

    id = Column(Integer, primary_key=True)
    presence_browsing_session_data_id = Column(Integer, ForeignKey('presencebrowsingdata.id'))

    date_created = Column(DateTime)
    calculated_intent = Column(Text)
    intent_formula_version = Column(Text)


PresenceBrowsingIntentSnaphot = add_intent_keyword_fields_to_db_table(PresenceBrowsingIntentSnaphot)
