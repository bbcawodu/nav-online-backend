from __future__ import print_function
import json
from twisted.internet.defer import inlineCallbacks
from twisted.enterprise import adbapi
from twistar.registry import Registry
from autobahn.wamp.types import CallResult
from twisted.internet.defer import returnValue
from autobahn.twisted.wamp import ApplicationSession
from patient_assist_browsing_data_components import PARSED_DB_URL
from twistar_db_models import PresenceBrowsingData
from utils import find_presence_health_db_entry_from_cookie_id
from patient_assist_db_models.presence_db_models.base import INTENT_KEYWORDS


class PresenceCollectComponent(ApplicationSession):
    """
    An application component that collects browsing data for users of the Presence Health Website.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("PresenceCollectComponent attached")

        # create a new database connection pool. connections are created lazy (as needed)
        def onPoolConnectionCreated(conn):
            # callback fired when Twisted adds a new database connection to the pool.
            # use this to do any app specific configuration / setup on the connection
            pid = conn.get_backend_pid()
            print("New DB connection created (backend PID {})".format(pid))

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

        try:
            yield self.register(self.create_browsing_data_instance, u'patient_assist_backend.presence_health.create_browsing_data_instance')
        except Exception as e:
            print("failed to register 'patient_assist_backend.presence_health.create_browsing_data_instance' procedure: {}".format(e))
        else:
            print("'patient_assist_backend.presence_health.create_browsing_data_instance' procedure registered")

        try:
            yield self.register(self.submit_browsing_data, u'patient_assist_backend.presence_health.submit_browsing_data')
        except Exception as e:
            print("failed to register 'patient_assist_backend.presence_health.submit_browsing_data' procedure: {}".format(e))
        else:
            print("'patient_assist_backend.presence_health.submit_browsing_data' procedure registered")

    @inlineCallbacks
    def create_browsing_data_instance(self):
        """
        This procedure creates a new presence health browsing data db entry and returns the db id and cookie_id of the
        newly created entry.

        Takes no params

        :return: Returns keywords results that are accessible through the results' kwargs property.
                id: (type: Integer) Database id of newly created presence health browsing data row.
                cookie_id: (type: String) Cookie id of newly created presence health browsing data row.
        """

        presence_data_instance = PresenceBrowsingData()
        presence_data_instance = yield presence_data_instance.save()

        presence_data_instance.cookie_id = str(presence_data_instance.id)
        presence_data_instance.send_cta_updates = False
        for browsing_keyword in INTENT_KEYWORDS:
            setattr(presence_data_instance, "{}_{}".format(browsing_keyword, "clicks"), 0)
            setattr(presence_data_instance, "{}_{}".format(browsing_keyword, "hover_time"), 0.0)

        presence_data_instance = yield presence_data_instance.save()

        returnValue(CallResult(id=presence_data_instance.id, cookie_id=presence_data_instance.cookie_id))

    @inlineCallbacks
    def submit_browsing_data(self, *args):
        """
        This procedure takes a given cookie_id corresponding to a presence health browsing data db row along with client
        browsing data information, updates the db record, and returns relevant updated info about the entry.

        :param args: Argument list. Accepts only one argument.
                 [browsing_data_json]
                 browsing_data_json: A JSON formatted object that has the following mandatory keys.
                                     cookie_id: (type: String) Cookie id of presence health browsing data row.
                                     keyword: (type: String) keyword corresponding the given browsing data.
                                     keyword_clicks: (type: Integer) number of clicks corresponding to given keyword.
                                     keyword_hover_time: (type: Float) length of hover time corresponding to given keyword.

        :return: Returns keywords results that are accessible through the results' kwargs property.
            id: (type: Integer) Database id of newly created presence health browsing data row.
            cookie_id: (type: String) Cookie id of newly created presence health browsing data row.
            oncology_clicks: (type: Integer) Total number of clicks corresponding to the 'oncology' keyword.
            oncology_hover_time: (type: Float) Total amount of time corresponding to the 'oncology' keyword.
        """

        browsing_data_json = check_args_for_browsing_data(args)

        browsing_data_raw = decode_json_arg(browsing_data_json)

        cookie_user_id, browsing_keyword, keyword_clicks, keyword_hover_time = check_browsing_data_for_args(browsing_data_raw)

        browsing_data_entry = yield find_presence_health_db_entry_from_cookie_id(cookie_user_id)

        browsing_data_entry = yield update_presence_health_db_entry(browsing_data_entry, browsing_keyword, keyword_clicks, keyword_hover_time)

        returnValue(CallResult(id=browsing_data_entry.id, cookie_id=browsing_data_entry.cookie_id, oncology_clicks=browsing_data_entry.oncology_clicks, oncology_hover_time=browsing_data_entry.oncology_hover_time))


def check_args_for_browsing_data(args):
    """
    This function takes an argument list containing one argument, browsing_data, parses it for errors, and returns the
    JSON object retrieved from the argument list.

    :param args: Argument list. Accepts only one argument.
                 [browsing_data]
                 browsing_data: (type: Unicode or String) JSON object that contains submitted browsing data.
    :return: (type: Unicode or String) JSON object that contains submitted browsing data.
    """

    if len(args) != 1:
        raise Exception(
            "'patient_assist_backend.submit_browsing_data_presence_health' accepts exactly 1 argument, browsing data.")
    browsing_data_json = args[0]
    # parse arguments for validity before processing
    if not isinstance(browsing_data_json, unicode) and not isinstance(browsing_data_json, str):
        raise Exception("browsing data must be a unicode or string object. It is {}".format(type(browsing_data_json)))

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
    :return: Argument List: [cookie_user_id, browsing_keyword, keyword_clicks, keyword_hover_time]
             cookie_user_id: (type: String or Unicode) Cookie id of presence health browsing data instance.
             browsing_keyword: (type: String or Unicode) Browsing data keyword to update.
             keyword_clicks: (type: Integer) Number of clicks for corresponding keyword.
             keyword_hover_time: (type: Float) Amount of time, in seconds, of hover time for corresponding keyword.
    """

    try:
        cookie_user_id = browsing_data['cookie_id']
        if not isinstance(cookie_user_id, unicode) and not isinstance(cookie_user_id, str):
            raise Exception("'cookie_id' must be a unicode or string object.")
    except KeyError:
        raise Exception("'cookie_id' key is not present in browsing data JSON object.")

    try:
        browsing_keyword = browsing_data['keyword']
        if not isinstance(browsing_keyword, unicode) and not isinstance(browsing_keyword, str):
            raise Exception("'keyword' must be a unicode or string object.")
        if browsing_keyword not in INTENT_KEYWORDS:
            raise Exception("'keyword' must be in the following list of accepted keywords: {}.".format(json.dumps(INTENT_KEYWORDS)))
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

    return cookie_user_id, browsing_keyword, keyword_clicks, keyword_hover_time


@inlineCallbacks
def update_presence_health_db_entry(browsing_data_entry, browsing_keyword, keyword_clicks, keyword_hover_time):
    """
    This function takes a presence browsing data twistar instance and submitted browsing data as arguments and uses
    the submitted data to update and save the twistar instance. The updated instance is returned.

    :param browsing_data_entry: (type: twistar PresenceBrowsingData instance) Presence Browsing Data instance.
    :param browsing_keyword: (type: String or Unicode) Browsing data keyword to update.
    :param keyword_clicks: (type: Integer) Number of clicks for corresponding keyword.
    :param keyword_hover_time: (type: Float) Amount of time, in seconds, of hover time for corresponding keyword.
    :return: (type: twistar PresenceBrowsingData instance) Updated Presence Browsing Data instance.
    """

    if browsing_keyword not in INTENT_KEYWORDS:
        raise Exception("'keyword' must be in the following list of accepted keywords: {}.".format(json.dumps(INTENT_KEYWORDS)))
    else:
        clicks_field_name = "{}_{}".format(browsing_keyword, "clicks")
        entry_clicks_value = getattr(browsing_data_entry, clicks_field_name)
        hover_time_field_name = "{}_{}".format(browsing_keyword, "hover_time")
        entry_hover_time_value = getattr(browsing_data_entry, hover_time_field_name)

        if entry_clicks_value is None:
            setattr(browsing_data_entry, clicks_field_name, keyword_clicks)
        else:
            setattr(browsing_data_entry, clicks_field_name, entry_clicks_value+keyword_clicks)

        if entry_hover_time_value is None:
            setattr(browsing_data_entry, hover_time_field_name, keyword_hover_time)
        else:
            setattr(browsing_data_entry, hover_time_field_name, entry_hover_time_value+keyword_hover_time)

    browsing_data_entry = yield browsing_data_entry.save()

    returnValue(browsing_data_entry)
