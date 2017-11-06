import os

from flask_sqlalchemy import SQLAlchemy

import http_server_pkg


class BlockingDBObjectsBaseTestCase(object):
    def setUp(self, *args, **kwargs):
        http_server_pkg.app.testing = True
        http_server_pkg.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TEST_DATABASE_URL']

        self.test_db_obj = SQLAlchemy(http_server_pkg.app)
        self.test_session = self.test_db_obj.session()

    def tearDown(self):
        self.test_session.rollback()

    def test_retrieve_table_data_by_id(self):
        ids_to_get = [

        ]
        ids_to_get_string = u"all"
        test_validated_get_rqst_params = {

        }
        test_errors = []

        retrieved_test_table_data = self.db_model.retrieve_table_data_by_id(
            self.test_session,
            test_validated_get_rqst_params,
            ids_to_get_string,
            ids_to_get,
            test_errors
                                                                            )

        self.assertEqual(len(test_errors), 0, "{}".format(test_errors))
        self.assertNotEqual(len(retrieved_test_table_data), 0, "{}".format([retrieved_test_table_data]))
