from sqlalchemy import Sequence
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy.sql import func
from patient_assist_db_models import DeclarativeBase
from patient_assist_db_models import BROWSING_KEYWORDS


def add_browsing_data_fields(browsing_data_table_class):
    browsing_data_table_fields = {
        "clicks": Column(Integer),
        "hover_time": Column(Float)
    }

    for browsing_keword in BROWSING_KEYWORDS:
        for field, field_type in browsing_data_table_fields.items():
            setattr(browsing_data_table_class, "{}_{}".format(browsing_keword, field), field_type)

    return browsing_data_table_class


class PresenceBrowsingData(DeclarativeBase):
    __tablename__ = 'presencebrowsingdata'

    id = Column(Integer, Sequence('presencebrowsingdata_id_seq'), primary_key=True)
    cookie_id = Column(String(10000))
    send_cta_updates = Column(Boolean)


PresenceBrowsingData = add_browsing_data_fields(PresenceBrowsingData)
