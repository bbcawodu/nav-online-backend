import unittest
import datetime

from conftest import TEST_BROWSING_DATA_VALUES
from conftest import combinations
from http_server_pkg.tests.test_views.base import HTTPServerViewsBaseTestCase


class BrowsingSessionDataAPITestCase(HTTPServerViewsBaseTestCase, unittest.TestCase):
    base_url = 'v1/presence_health/browsing_session_data/'

    def test_retrieve_all_entries_get_request(self):
        self.base_url += "?id=all"

        response_data = self.make_test_rqst()

        returned_entries = response_data['Data']

        self.assertNotEqual(len(returned_entries), 0, "{}".format(returned_entries))

    def test_min_date_get_request(self):
        self.base_url += "?id=all&min_date={}".format(datetime.datetime.utcnow().date().isoformat())

        response_data = self.make_test_rqst()

        returned_entries = response_data['Data']

        self.assertNotEqual(len(returned_entries), 0, "{}".format(returned_entries))

    def test_max_date_get_request(self):
        self.base_url += "?id=all&max_date={}".format(datetime.datetime.utcnow().date().isoformat())

        response_data = self.make_test_rqst()

        returned_entries = response_data['Data']

        self.assertNotEqual(len(returned_entries), 0, "{}".format(returned_entries))

    def test_min_oncology_clicks_get_request(self):
        self.base_url += "?id=all&oncology_clicks=4"

        response_data = self.make_test_rqst()

        returned_entries = response_data['Data']

        self.assertNotEqual(len(returned_entries), 0, "{}".format(returned_entries))

    def test_min_oncology_hover_time_get_request(self):
        self.base_url += "?id=all&oncology_hover_time=9.1"

        response_data = self.make_test_rqst()

        returned_entries = response_data['Data']

        self.assertNotEqual(len(returned_entries), 0, "{}".format(returned_entries))

    def test_multiple_params_get_request(self):
        base_url = self.base_url + "?id=all"
        params_to_test = [
            "oncology_hover_time=9.1",
            "oncology_clicks=4",
            "min_date={}".format(datetime.datetime.utcnow().date().isoformat()),
            "max_date={}".format(datetime.datetime.utcnow().date().isoformat()),
        ]

        combos_of_test_params = combinations(params_to_test)

        for param_combo in combos_of_test_params:
            self.base_url = base_url
            for param in param_combo:
                self.base_url += "&{}".format(param)

            response_data = self.make_test_rqst()
            returned_entries = response_data['Data']
            self.assertNotEqual(len(returned_entries), 0, "{}".format(returned_entries))
