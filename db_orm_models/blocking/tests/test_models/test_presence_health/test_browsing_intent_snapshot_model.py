import unittest

from conftest import TEST_BROWSING_DATA_VALUES

from db_orm_models.blocking.presence import PresenceBrowsingIntentSnapshot
from db_orm_models.blocking.tests.test_models.base import BlockingDBObjectsBaseTestCase


class BrowsingIntentSnapshotORMModelTestCase(BlockingDBObjectsBaseTestCase, unittest.TestCase):
    db_model = PresenceBrowsingIntentSnapshot

    def test_retrieve_table_data_by_session_id(self):
        session_ids_to_get = [
            1
        ]
        session_ids_to_get_string = u"1"
        test_validated_get_rqst_params = {

        }
        test_errors = []

        retrieved_test_table_data = self.db_model.retrieve_table_data_by_session_id(self.test_session,
                                                                                    test_validated_get_rqst_params,
                                                                                    session_ids_to_get_string,
                                                                                    session_ids_to_get,
                                                                                    test_errors)

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(retrieved_test_table_data), 0, "{}".format([retrieved_test_table_data]))

    def test_retrieve_table_data_by_intent(self):
        test_intent_value = u"oncology"
        test_validated_get_rqst_params = {

        }
        test_errors = []

        retrieved_test_table_data = self.db_model.retrieve_table_data_by_intent(self.test_session,
                                                                                test_validated_get_rqst_params,
                                                                                test_intent_value,
                                                                                test_errors)

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(retrieved_test_table_data), 0, "{}".format([retrieved_test_table_data]))
