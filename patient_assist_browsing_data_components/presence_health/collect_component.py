from __future__ import print_function
import json
from twisted.internet.defer import inlineCallbacks
from twisted.enterprise import adbapi
from twistar.registry import Registry
from autobahn.wamp.types import CallResult
from twisted.internet.defer import returnValue
from autobahn.twisted.wamp import ApplicationSession
from patient_assist_browsing_data_components import PARSED_DB_URL
from db_models import PresenceBrowsingData


BROWSING_KEYWORDS = ['oncology']


class PresenceCollectComponent(ApplicationSession):
    """
    An application component that collects browsing data for users of the Presence Health Website
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

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
            print("failed to register 'create_browsing_data_instance_presence_health' procedure: {}".format(e))
        else:
            print("'create_browsing_data_instance_presence_health' procedure registered")

        try:
            yield self.register(self.submit_browsing_data, u'patient_assist_backend.presence_health.submit_browsing_data')
        except Exception as e:
            print("failed to register 'submit_browsing_data_presence_health' procedure: {}".format(e))
        else:
            print("'submit_browsing_data_presence_health' procedure registered")

    @inlineCallbacks
    def create_browsing_data_instance(self):
        """
        This procedure creates a new presence health browsing data db entry and returns the db id and cookie_id of the
        newly created entry.

        Takes no params

        :return: Returns keywords results that are accessible through the results' kwargs property.
                id: (type: Integer) Database id of newly created presence health browsing data row
                cookie_id: (type: String) Cookie id of newly created presence health browsing data row
        """

        presence_data_instance = PresenceBrowsingData()
        presence_data_instance = yield presence_data_instance.save()
        presence_data_instance.cookie_id = str(presence_data_instance.id)
        presence_data_instance.oncology_clicks = 0
        presence_data_instance.oncology_hover_time = 0.0
        presence_data_instance = yield presence_data_instance.save()

        returnValue(CallResult(id=presence_data_instance.id, cookie_id=presence_data_instance.cookie_id))

    @inlineCallbacks
    def submit_browsing_data(self, *args):
        """
        This procedure takes a given cookie_id corresponding to a presence health browsing data db row along with client
        browsing data information, updates the db record, and returns relevant updated info about the entry.

        :param args: Argument list. Accepts only one argument
                 [browsing_data_json]
                 browsing_data_json: A JSON formatted object that has the following mandatory keys
                                     cookie_id: (type: String) Cookie id of presence health browsing data row
                                     keyword: (type: String) name corresponding the given browsing data. Currently only accepts 'oncology'
                                     keyword_clicks: (type: Integer) number of clicks corresponding to given keyword
                                     keyword_hover_time: (type: Float) length of hover time corresponding to given keyword

        :return: Returns keywords results that are accessible through the results' kwargs property.
            id: (type: Integer) Database id of newly created presence health browsing data row
            cookie_id: (type: String) Cookie id of newly created presence health browsing data row
            oncology_clicks: (type: Integer) Total number of clicks corresponding to the 'oncology' keyword
            oncology_hover_time: (type: Float) Total amount of time corresponding to the 'oncology' keyword
        """

        browsing_data_json = check_args_for_browsing_data(args)

        browsing_data_raw = decode_json_arg(browsing_data_json)

        cookie_user_id, browsing_keyword, keyword_clicks, keyword_hover_time = check_browsing_data_for_args(browsing_data_raw)

        browsing_data_entry = yield find_presence_health_db_entry_from_cookie_id(cookie_user_id)

        browsing_data_entry = yield update_presence_health_db_entry(browsing_data_entry, browsing_keyword, keyword_clicks, keyword_hover_time)

        returnValue(CallResult(id=browsing_data_entry.id, cookie_id=browsing_data_entry.cookie_id, oncology_clicks=browsing_data_entry.oncology_clicks, oncology_hover_time=browsing_data_entry.oncology_hover_time))


def check_args_for_browsing_data(args):
    """

    :param args:
    :return:
    """

    if len(args) != 1:
        raise Exception(
            "'patient_assist_backend.submit_browsing_data_presence_health' accepts exactly 1 argument, browsing data.")
    browsing_data_json = args[0]
    # parse arguments for validity before processing
    if not isinstance(browsing_data_json, unicode):
        raise Exception("browsing data must be a unicode object. It is {}".format(type(browsing_data_json)))

    return browsing_data_json


def decode_json_arg(json_arg):
    """

    :param json_arg:
    :return:
    """

    try:
        return json.loads(json_arg)
    except ValueError:
        print("Decoding JSON argument has failed")
        raise Exception("Decoding JSON argument has failed")


def check_browsing_data_for_args(browsing_data):
    """

    :param browsing_data:
    :return:
    """

    try:
        cookie_user_id = browsing_data['cookie_id']
        if not isinstance(cookie_user_id, unicode):
            raise Exception("'cookie_id' must be unicode.")
    except KeyError:
        raise Exception("'cookie_id' key is not present in browsing data JSON object.")

    try:
        browsing_keyword = browsing_data['keyword']
        if not isinstance(browsing_keyword, unicode):
            raise Exception("'keyword' must be a string.")
        if browsing_keyword not in BROWSING_KEYWORDS:
            raise Exception("'keyword' must be in the following list of accepted keywords: {}.".format(json.dumps(BROWSING_KEYWORDS)))
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
def find_presence_health_db_entry_from_cookie_id(cookie_user_id):
    """

    :param cookie_user_id:
    :return:
    """

    browsing_data_entry = yield PresenceBrowsingData.findBy(cookie_id=cookie_user_id)
    if not browsing_data_entry:
        raise Exception("No Presence Health Browsing data entry found for cookie_id: {}".format(cookie_user_id))
    elif len(browsing_data_entry) > 1:
        raise Exception(
            "More than one Presence Health Browsing data entry found for cookie_id: {}".format(cookie_user_id))
    else:
        returnValue(browsing_data_entry[0])


@inlineCallbacks
def update_presence_health_db_entry(browsing_data_entry, browsing_keyword, keyword_clicks, keyword_hover_time):
    """

    :param browsing_data_entry:
    :param browsing_keyword:
    :param keyword_clicks:
    :param keyword_hover_time:
    :return:
    """

    if browsing_keyword == 'oncology':
        if browsing_data_entry.oncology_clicks is None:
            browsing_data_entry.oncology_clicks = keyword_clicks
        else:
            browsing_data_entry.oncology_clicks += keyword_clicks

        if browsing_data_entry.oncology_hover_time is None:
            browsing_data_entry.oncology_hover_time = keyword_hover_time
        else:
            browsing_data_entry.oncology_hover_time += keyword_hover_time
    else:
        raise Exception("No valid browsing data keywords present.")

    browsing_data_entry = yield browsing_data_entry.save()

    returnValue(browsing_data_entry)
