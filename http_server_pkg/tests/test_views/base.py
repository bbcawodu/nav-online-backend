import os
import json

import http_server_pkg


class HTTPServerViewsBaseTestCase(object):
    def setUp(self, *args, **kwargs):
        http_server_pkg.app.testing = True
        http_server_pkg.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['TEST_DATABASE_URL']
        self.app = http_server_pkg.app.test_client()

    def make_test_rqst(self):
        response = self.app.get(self.base_url)

        response_json = response.data.decode('utf-8')
        response_data = json.loads(response_json)

        return response_data

    def test_base_get_api_rqst(self):
        response = self.app.get(self.base_url)

        # Test for a valid reponse code (200)
        self.assertEqual(response.status_code, 200)

    def test_decode_get_api_json_response(self):
        response_data = self.make_test_rqst()

        # Test for valid decoded json data from response body
        self.assertIsNotNone(response_data)

    def test_get_api_response_data_status(self):
        response_data = self.make_test_rqst()

        # Test decoded JSON data for "Status" key
        self.assertIsNotNone(response_data["Status"])

    def test_get_api_response_data_version(self):
        response_data = self.make_test_rqst()

        # Test decoded JSON data for correct API version
        self.assertEqual(response_data["Status"]["Version"], 1.0)
