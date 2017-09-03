from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from blocking_orm_models import DeclarativeBase
from .base import BaseClassForTableWithIntentFields
from .base import add_intent_keyword_fields_to_db_table


class PresenceBrowsingData(DeclarativeBase, BaseClassForTableWithIntentFields):
    __tablename__ = 'presencebrowsingdata'

    id = Column(Integer, primary_key=True)
    browsing_intent_snapshots = relationship("PresenceBrowsingIntentSnaphot", backref="presence_browsing_session_data_row")

    date_created = Column(DateTime)
    date_last_updated = Column(DateTime)


PresenceBrowsingData = add_intent_keyword_fields_to_db_table(PresenceBrowsingData)
