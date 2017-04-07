from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float

DeclarativeBase = declarative_base()

BROWSING_KEYWORDS = ['oncology']

BROWSING_DATA_FIELDS = {
                            "clicks": Column(Integer),
                            "hover_time": Column(Float)
                        }
