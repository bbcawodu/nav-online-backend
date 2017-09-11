from __future__ import print_function

import json

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import CallResult
from twistar.registry import Registry
from twisted.enterprise import adbapi
from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue

from sqlalchemy_blocking_orm_models.presence_db_models.base import INTENT_KEYWORDS
from sqlalchemy_blocking_orm_models.presence_db_models.base import INTENT_KEYWORD_FIELD_NAMES_W_TYPES
from twistar_non_blocking_orm_models.presence_db_models import non_blocking_get_intent_snapshot_rows_from_session_id
from twistar_non_blocking_orm_models.presence_db_models import non_blocking_create_intent_snapshot_row
from twistar_non_blocking_orm_models.presence_db_models import non_blocking_get_intent_snapshot_row_by_id
from wamp_server_components.base import PARSED_DB_URL


class PresenceBrowsingIntentSnapshotComponent(ApplicationSession):
    """
    An application component that collects browsing data for users of the Presence Health Website.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("PresenceBrowsingIntentSnapshotComponent attached")

        # create a new database connection pool. connections are created lazy (as needed)
        def onPoolConnectionCreated(conn):
            # callback fired when Twisted adds a new database connection to the pool.
            # use this to do any app specific configuration / setup on the connection
            pid = conn.get_backend_pid()
            print("New DB connection created (backend PID {})".format(pid))

        @inlineCallbacks
        def register_rpcs_with_component():
            create_browsing_intent_snapshot_row_procedure_uri = u'create_browsing_intent_snapshot_row'
            read_browsing_intent_snapshot_row_procedure_uri = u'read_browsing_intent_snapshot_rows'
            delete_browsing_intent_snapshot_row_procedure_uri = u'delete_browsing_intent_snapshot_row'

            try:
                yield self.register(self.create_browsing_intent_snapshot_row, create_browsing_intent_snapshot_row_procedure_uri)
            except Exception as e:
                print("failed to register '{}' procedure: {}".format(create_browsing_intent_snapshot_row_procedure_uri, e))
            else:
                print("'{}' procedure registered".format(create_browsing_intent_snapshot_row_procedure_uri))

            try:
                yield self.register(self.read_browsing_intent_snapshot_rows, read_browsing_intent_snapshot_row_procedure_uri)
            except Exception as e:
                print("failed to register '{}' procedure: {}".format(read_browsing_intent_snapshot_row_procedure_uri, e))
            else:
                print("'{}' procedure registered".format(read_browsing_intent_snapshot_row_procedure_uri))

            try:
                yield self.register(self.delete_browsing_intent_snapshot_row, delete_browsing_intent_snapshot_row_procedure_uri)
            except Exception as e:
                print("failed to register '{}' procedure: {}".format(delete_browsing_intent_snapshot_row_procedure_uri, e))
            else:
                print("'{}' procedure registered".format(delete_browsing_intent_snapshot_row_procedure_uri))

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
    def create_browsing_intent_snapshot_row(self, *args):
        def get_and_decode_json_arg(argument_list):
            if len(argument_list) != 1:
                raise Exception(
                    "'create_browsing_intent_snapshot_row' accepts exactly 1 argument, browsing_session_id_obj.")
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
                if not isinstance(db_id, unicode) and not isinstance(
                        db_id, str):
                    raise Exception("'id' must be a unicode or string object.")
                db_id = int(db_id)
            except KeyError:
                raise Exception("id' key is not present in browsing data JSON object.")

            return db_id

        browsing_session_id_dict = get_and_decode_json_arg(args)

        browsing_session_data_row_id = check_input_dict_for_id(browsing_session_id_dict)

        intent_snapshot_row = yield non_blocking_create_intent_snapshot_row(browsing_session_data_row_id)

        returnValue(CallResult(**intent_snapshot_row.return_values_dict()))

    @inlineCallbacks
    def read_browsing_intent_snapshot_rows(self, *args):
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

        def make_return_dictionary():
            return_value = {
                'intent_snapshot_rows': json.dumps([intent_snapshot_row.return_values_dict() for intent_snapshot_row in intent_snapshot_rows]),
            }

            return return_value

        browsing_session_id_dict = get_and_decode_json_arg(args)

        browsing_session_data_row_id = check_input_dict_for_id( browsing_session_id_dict)

        intent_snapshot_rows = yield non_blocking_get_intent_snapshot_rows_from_session_id(browsing_session_data_row_id)
        return_dictionary = make_return_dictionary()

        returnValue(CallResult(**return_dictionary))

    @inlineCallbacks
    def delete_browsing_intent_snapshot_row(self, *args):
        def get_and_decode_json_arg(argument_list):
            if len(argument_list) != 1:
                raise Exception(
                    "'delete_browsing_intent_snapshot_row' accepts exactly 1 argument, intent_snapshot_id_obj.")
            id_json = argument_list[0]

            # parse arguments for validity before processing
            if not isinstance(id_json, unicode) and not isinstance(id_json, str):
                raise Exception(
                    "id_json must be a unicode or string object. It is {}".format(
                        type(id_json)))

            try:
                return json.loads(id_json)
            except ValueError:
                print("Decoding JSON argument has failed")
                raise Exception("Decoding JSON argument has failed")

        def check_input_dict_for_id(browsing_data):
            try:
                db_id = browsing_data['id']
                if not isinstance(db_id, unicode) and not isinstance(
                        db_id, str):
                    raise Exception("'id' must be a unicode or string object.")
                db_id = int(db_id)
            except KeyError:
                raise Exception("id' key is not present in browsing data JSON object.")

            return db_id

        def make_return_dictionary():
            return_value = {
                'id': 'deleted'
            }
            return return_value

        intent_snapshot_id_dict = get_and_decode_json_arg(args)

        intent_snapshot_id = check_input_dict_for_id(intent_snapshot_id_dict)

        intent_snapshot_row = yield non_blocking_get_intent_snapshot_row_by_id(intent_snapshot_id)

        yield intent_snapshot_row.delete()

        return_dictionary = make_return_dictionary()

        returnValue(CallResult(**return_dictionary))
