from __future__ import print_function

import json

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import CallResult
from twistar.registry import Registry
from twisted.enterprise import adbapi
from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue

from db_orm_models.base import PRESENCE_INTENT_KEYWORDS
from db_orm_models.non_blocking.presence_db_models import non_blocking_create_presence_browsing_session_data_row
from db_orm_models.non_blocking.presence_db_models import non_blocking_get_browsing_session_data_row_by_id
from db_orm_models.non_blocking.presence_db_models import non_blocking_update_presence_session_row_w_submitted_data

from wamp_server_pkg.base import PARSED_DB_URL


class PresenceBrowsingSessionDataComponent(ApplicationSession):
    """
    An application component that collects browsing data for users of the Presence Health Website.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("PresenceBrowsingSessionDataComponent attached")

        # create a new database connection pool. connections are created lazy (as needed)
        def onPoolConnectionCreated(conn):
            # callback fired when Twisted adds a new database connection to the pool.
            # use this to do any app specific configuration / setup on the connection
            pid = conn.get_backend_pid()
            print("New DB connection created (backend PID {})".format(pid))

        @inlineCallbacks
        def register_rpcs_with_component():
            create_browsing_session_data_row_procedure_uri = u'create_browsing_session_data_row'
            try:
                yield self.register(self.create_browsing_session_data_row,
                                    create_browsing_session_data_row_procedure_uri)
            except Exception as e:
                print("failed to register '{}' procedure: {}".format(create_browsing_session_data_row_procedure_uri, e))
            else:
                print("'{}' procedure registered".format(create_browsing_session_data_row_procedure_uri))

            submit_browsing_data_procedure_uri = u'submit_browsing_data'
            try:
                yield self.register(self.submit_browsing_data, submit_browsing_data_procedure_uri)
            except Exception as e:
                print("failed to register '{}' procedure: {}".format(submit_browsing_data_procedure_uri, e))
            else:
                print("'{}' procedure registered".format(submit_browsing_data_procedure_uri))

            read_browsing_session_data_row_procedure_uri = u'read_browsing_session_data_row'
            try:
                yield self.register(self.read_browsing_session_data_row, read_browsing_session_data_row_procedure_uri)
            except Exception as e:
                print("failed to register '{}' procedure: {}".format(read_browsing_session_data_row_procedure_uri, e))
            else:
                print("'{}' procedure registered".format(read_browsing_session_data_row_procedure_uri))

            read_current_browsing_intent_procedure_uri = u'read_current_browsing_intent'
            try:
                yield self.register(self.read_current_browsing_intent, read_current_browsing_intent_procedure_uri)
            except Exception as e:
                print("failed to register '{}' procedure: {}".format(read_current_browsing_intent_procedure_uri, e))
            else:
                print("'{}' procedure registered".format(read_current_browsing_intent_procedure_uri))

        Registry.DBPOOL = adbapi.ConnectionPool("psycopg2",
                                                host=PARSED_DB_URL.hostname,
                                                port=PARSED_DB_URL.port,
                                                database=PARSED_DB_URL.path[1:],
                                                user=PARSED_DB_URL.username,
                                                password=PARSED_DB_URL.password,
                                                cp_min=3,
                                                cp_max=10,
                                                cp_noisy=True,
                                                cp_openfun=onPoolConnectionCreated,
                                                cp_reconnect=True,
                                                cp_good_sql="SELECT 1")

        yield register_rpcs_with_component()

    @inlineCallbacks
    def create_browsing_session_data_row(self):
        presence_data_instance = yield non_blocking_create_presence_browsing_session_data_row()

        returnValue(CallResult(**presence_data_instance.return_values_dict()))

    @inlineCallbacks
    def submit_browsing_data(self, *args):
        """
        This procedure takes a given id corresponding to a presence health browsing data db row along with client
        browsing data information, updates the db record, and returns relevant updated info about the entry.

        :param args: Argument list. Accepts only one argument.
                 [browsing_data_json]
                 browsing_data_json: A JSON formatted object that has the following mandatory keys.
                                     id: (type: String) Cookie id of presence health browsing data row.
                                     keyword: (type: String) keyword corresponding the given browsing data.
                                     keyword_clicks: (type: Integer) number of clicks corresponding to given keyword.
                                     keyword_hover_time: (type: Float) length of hover time corresponding to given keyword.

        :return: Returns keywords results that are accessible through the results' kwargs property.
            id: (type: Integer) Database id of newly created presence health browsing data row.
            oncology_clicks: (type: Integer) Total number of clicks corresponding to the 'oncology' keyword.
            oncology_hover_time: (type: Float) Total amount of time corresponding to the 'oncology' keyword.
        """

        def check_args_for_browsing_data(argument_list):
            """
            This function takes an argument list containing one argument, browsing_data, parses it for errors, and returns the
            JSON object retrieved from the argument list.

            :param argument_list: Argument list. Accepts only one argument.
                         [browsing_data]
                         browsing_data: (type: Unicode or String) JSON object that contains submitted browsing data.
            :return: (type: Unicode or String) JSON object that contains submitted browsing data.
            """

            if len(argument_list) != 1:
                raise Exception(
                    "'patient_assist_backend.submit_browsing_data_presence_health' accepts exactly 1 argument, browsing data.")
            browsing_data_json = argument_list[0]
            # parse arguments for validity before processing
            if not isinstance(browsing_data_json, unicode) and not isinstance(browsing_data_json, str):
                raise Exception(
                    "browsing data must be a unicode or string object. It is {}".format(type(browsing_data_json)))

            return browsing_data_json

        def decode_json_arg(json_arg):
            """
            This function takes a JSON formatted String or Unicode object, parses it for errors, transforms it into a python
            object, and finally returns the decoded object.

            :param json_arg: (type: Unicode or String) JSON object for decoding.
            :return: (type: Dictionary) Dictionary object that contains submitted browsing data.
            """

            try:
                return json.loads(json_arg)
            except ValueError:
                print("Decoding JSON argument has failed")
                raise Exception("Decoding JSON argument has failed")

        def check_browsing_data_for_args(browsing_data):
            """
            This function takes a dictionary, parses it for parameters that are used for submitting browsing data and returns
            any errors. Finally, the function returns an argument list containing any relevant browsing data.

            :param browsing_data: (type: Dictionary) Dictionary object that contains submitted browsing data.
            :return: Argument List: [browsing_session_data_row_id, browsing_keyword, keyword_clicks, keyword_hover_time]
                     browsing_session_data_row_id: (type: String or Unicode) Cookie id of presence health browsing data instance.
                     browsing_keyword: (type: String or Unicode) Browsing data keyword to update.
                     keyword_clicks: (type: Integer) Number of clicks for corresponding keyword.
                     keyword_hover_time: (type: Float) Amount of time, in seconds, of hover time for corresponding keyword.
            """

            try:
                browsing_session_data_row_id = browsing_data['id']
                if not isinstance(browsing_session_data_row_id, unicode) and not isinstance(
                        browsing_session_data_row_id, str):
                    raise Exception("'id' must be a unicode or string object.")
                browsing_session_data_row_id = int(browsing_session_data_row_id)
            except KeyError:
                raise Exception("id' key is not present in browsing data JSON object.")

            try:
                browsing_keyword = browsing_data['keyword']
                if not isinstance(browsing_keyword, unicode) and not isinstance(browsing_keyword, str):
                    raise Exception("'keyword' must be a unicode or string object.")
                if browsing_keyword not in PRESENCE_INTENT_KEYWORDS:
                    raise Exception("'keyword' must be in the following list of accepted keywords: {}.".format(
                        json.dumps(PRESENCE_INTENT_KEYWORDS)))
            except KeyError:
                raise Exception("'keyword' key is not present in browsing data JSON object.")

            try:
                keyword_clicks = browsing_data['keyword_clicks']
                if not isinstance(keyword_clicks, int):
                    raise Exception("'keyword_clicks' must be an integer.")
                if keyword_clicks < 0:
                    raise Exception("'keyword_clicks' must be an positive.")
            except KeyError:
                raise Exception("'keyword_clicks' key is not present in browsing data JSON object.")
            try:
                keyword_hover_time = browsing_data['keyword_hover_time']
                if not isinstance(keyword_hover_time, float):
                    raise Exception("'keyword_hover_time' must be a floating point.")
                if keyword_hover_time < 0:
                    raise Exception("'keyword_hover_time' must be positive")
            except KeyError:
                raise Exception("'keyword_hover_time' key is not present in browsing data JSON object.")

            return browsing_session_data_row_id, browsing_keyword, keyword_clicks, keyword_hover_time

        browsing_data_json = check_args_for_browsing_data(args)

        browsing_data_raw = decode_json_arg(browsing_data_json)

        browsing_session_data_row_id, browsing_keyword, keyword_clicks, keyword_hover_time = check_browsing_data_for_args(browsing_data_raw)

        presence_browsing_session_data_row = yield non_blocking_get_browsing_session_data_row_by_id(browsing_session_data_row_id)

        presence_browsing_session_data_row = yield non_blocking_update_presence_session_row_w_submitted_data(presence_browsing_session_data_row, browsing_keyword, keyword_clicks, keyword_hover_time)

        returnValue(CallResult(**presence_browsing_session_data_row.return_values_dict()))

    @inlineCallbacks
    def read_browsing_session_data_row(self, *args):
        def get_and_decode_json_arg(argument_list):
            if len(argument_list) != 1:
                raise Exception(
                    "'read_browsing_sesion_data_row' accepts exactly 1 argument, browsing_session_id_obj.")
            browsing_session_id_json = argument_list[0]

            # parse arguments for validity before processing
            if not isinstance(browsing_session_id_json, unicode) and not isinstance(browsing_session_id_json, str):
                raise Exception(
                    "browsing_session_id_obj must be a unicode or string object. It is {}".format(type(browsing_session_id_json)))

            try:
                return json.loads(browsing_session_id_json)
            except ValueError:
                print("Decoding JSON argument has failed")
                raise Exception("Decoding JSON argument has failed")

        def check_input_dict_for_id(browsing_data):
            try:
                db_id = browsing_data['id']
                if not isinstance(db_id, unicode) and not isinstance(db_id, str):
                    raise Exception("'id' must be a unicode or string object.")
                db_id = int(db_id)
            except KeyError:
                raise Exception("id' key is not present in browsing data JSON object.")

            return db_id

        browsing_session_id_dict = get_and_decode_json_arg(args)

        browsing_session_data_row_id = check_input_dict_for_id( browsing_session_id_dict)

        browsing_data_row = yield non_blocking_get_browsing_session_data_row_by_id(browsing_session_data_row_id)

        returnValue(CallResult(**browsing_data_row.return_values_dict()))

    @inlineCallbacks
    def read_current_browsing_intent(self, *args):
        def get_and_decode_json_arg(argument_list):
            if len(argument_list) != 1:
                raise Exception(
                    "'read_current_browsing_intent' accepts exactly 1 argument, browsing_session_id_obj.")
            browsing_session_id_json = argument_list[0]

            # parse arguments for validity before processing
            if not isinstance(browsing_session_id_json, unicode) and not isinstance(browsing_session_id_json, str):
                raise Exception(
                    "browsing_session_id_obj must be a unicode or string object. It is {}".format(type(browsing_session_id_json)))

            try:
                return json.loads(browsing_session_id_json)
            except ValueError:
                print("Decoding JSON argument has failed")
                raise Exception("Decoding JSON argument has failed")

        def check_input_dict_for_id(browsing_data):
            try:
                db_id = browsing_data['id']
                if not isinstance(db_id, unicode) and not isinstance(db_id, str):
                    raise Exception("'id' must be a unicode or string object.")
                db_id = int(db_id)
            except KeyError:
                raise Exception("id' key is not present in browsing data JSON object.")

            return db_id

        def make_return_dictionary():
            current_intent = browsing_data_row.current_intent
            cta_url = "https://picbackend.herokuapp.com/v2/cta/?intent=" + current_intent
            return_value = {
                'current_intent': current_intent,
                'cta_url': cta_url,
            }

            return return_value

        browsing_session_id_dict = get_and_decode_json_arg(args)

        browsing_session_data_row_id = check_input_dict_for_id( browsing_session_id_dict)

        browsing_data_row = yield non_blocking_get_browsing_session_data_row_by_id(browsing_session_data_row_id)
        return_dictionary = make_return_dictionary()

        returnValue(CallResult(**return_dictionary))
