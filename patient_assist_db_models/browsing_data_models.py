from sqlalchemy import Sequence
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy.sql import func
from patient_assist_db_models import DeclarativeBase


class PresenceBrowsingData(DeclarativeBase):
    __tablename__ = 'presencebrowsingdata'

    id = Column(Integer, Sequence('presencebrowsingdata_id_seq'), primary_key=True)
    cookie_id = Column(String(10000))
    send_cta_updates = Column(Boolean)
    oncology_clicks = Column(Integer)
    oncology_hover_time = Column(Float)
