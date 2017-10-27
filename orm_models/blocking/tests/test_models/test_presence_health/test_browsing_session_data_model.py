import unittest

from orm_models.blocking import PresenceBrowsingData

from conftest import TEST_BROWSING_DATA_VALUES
from orm_models.blocking.tests.test_models.base import BlockingDBObjectsBaseTestCase


class BrowsingSessionORMModelTestCase(BlockingDBObjectsBaseTestCase, unittest.TestCase):
    db_model = PresenceBrowsingData
