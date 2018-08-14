from twisted.trial import unittest
from twisted.enterprise import adbapi
from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue
from twistar.registry import Registry

from db_orm_models.non_blocking.presence_db_models.browsing_models import non_blocking_create_presence_browsing_session_data_row
from db_orm_models.non_blocking.presence_db_models.browsing_models import non_blocking_get_intent_snapshot_row_by_id
from db_orm_models.non_blocking.presence_db_models.browsing_models import non_blocking_get_intent_snapshot_rows_from_session_id
from db_orm_models.non_blocking.presence_db_models.browsing_models import non_blocking_update_presence_session_row_w_submitted_data

from os import environ
import urlparse

from sqlalchemy.engine import create_engine
from db_orm_models.blocking.base import DeclarativeBase


class DBModelTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(environ['TEST_DATABASE_URL'])
        DeclarativeBase.metadata.create_all(self.engine)

        # Get Database url from environment variables
        urlparse.uses_netloc.append("postgres")
        PARSED_DB_URL = urlparse.urlparse(environ['TEST_DATABASE_URL'])

        Registry.DBPOOL = adbapi.ConnectionPool("psycopg2",
                                                host=PARSED_DB_URL.hostname,
                                                port=PARSED_DB_URL.port,
                                                database=PARSED_DB_URL.path[1:],
                                                user=PARSED_DB_URL.username,
                                                password=PARSED_DB_URL.password,
                                                cp_min=3,
                                                cp_max=10,
                                                cp_noisy=True,
                                                cp_reconnect=True,
                                                cp_good_sql="SELECT 1")

    def tearDown(self):
        DeclarativeBase.metadata.drop_all(bind=self.engine)

    @inlineCallbacks
    def test_non_blocking_create(self):
        browsing_session_obj = yield non_blocking_create_presence_browsing_session_data_row()
        returnValue(self.assertNotEqual(browsing_session_obj.id, None))

    @inlineCallbacks
    def test_non_blocking_read(self):
        browsing_session_obj = yield non_blocking_create_presence_browsing_session_data_row()
        returnValue(self.assertNotEqual(browsing_session_obj.id, None))

    @inlineCallbacks
    def test_non_blocking_update(self):
        browsing_session_obj = yield non_blocking_create_presence_browsing_session_data_row()
        returnValue(self.assertNotEqual(browsing_session_obj.id, None))

    @inlineCallbacks
    def test_non_blocking_delete(self):
        browsing_session_obj = yield non_blocking_create_presence_browsing_session_data_row()
        returnValue(self.assertNotEqual(browsing_session_obj.id, None))
