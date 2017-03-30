from __future__ import print_function
from twisted.internet.defer import inlineCallbacks
from twisted.enterprise import adbapi
from twistar.registry import Registry
from autobahn.wamp.types import CallResult
from twisted.internet.defer import returnValue
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from patient_assist_browsing_data_components import PARSED_DB_URL
from twistar_db_models import PresenceBrowsingData
from utils import find_presence_health_db_entry_from_cookie_id
from patient_assist_db_models import BROWSING_KEYWORDS
from sys import maxint


class PublishPresenceCTASComponent(ApplicationSession):
    """
    An application component that polls Presence Health browsing data entries for ones that have been updated recently
    and publishes the appropriate cta to appropriate topic based on browsing data and cookie_id
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("PublishPresenceCTASComponent attached")

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
            yield self.register(self.enable_cta_updates, u'patient_assist_backend.presence_health.enable_cta_updates')
        except Exception as e:
            print("failed to register 'patient_assist_backend.presence_health.enable_cta_updates' procedure: {}".format(e))
        else:
            print("'patient_assist_backend.presence_health.enable_cta_updates' procedure registered")

        try:
            yield self.register(self.disable_cta_updates, u'patient_assist_backend.presence_health.disable_cta_updates')
        except Exception as e:
            print("failed to register 'patient_assist_backend.presence_health.disable_cta_updates' procedure: {}".format(e))
        else:
            print("'patient_assist_backend.presence_health.disable_cta_updates' procedure registered")

        # Infinite loop, is always publishing
        while True:
            browsing_data_entries = yield PresenceBrowsingData.findBy(send_cta_updates=True)

            for browsing_data_entry in browsing_data_entries:
                # find appropriate cta based on browsing data and publish to topic
                cta_url = retrieve_cta_based_on_browsing_data(browsing_data_entry)

                self.publish(u'patient_assist_backend.presence_health.new_ctas.{}'.format(browsing_data_entry.cookie_id),
                             cta_url=cta_url)

            yield sleep(2)

    @inlineCallbacks
    def enable_cta_updates(self, *args):
        """
        This procedure takes a given cookie_id corresponding to a presence health browsing data db row and sets its
        send_cta_updates value to True. When a given browsing data's instance is set to True, it will publish the URL
        for the most updated CTA for a given browsing data instance at uri
        'patient_assist_backend.presence_health.new_ctas.<cookie_id>'.

        :param args: Argument list. Accepts only one argument
                     [cookie_id]
                     cookie_id: (type: String) Cookie id of presence health browsing data.
        :return: Returns keywords results that are accessible through the results' kwargs property.
                id: (type: Integer) Database id of newly created presence health browsing data row
                cookie_id: (type: String) Cookie id of newly created presence health browsing data row
                sending_browsing_data: (type: Boolean) Whether or not updated CTA's are being published for this entry.
        """

        browsing_data_entry = yield retrieve_presence_db_entry_from_args(args)

        browsing_data_entry.send_cta_updates = True

        browsing_data_entry = yield browsing_data_entry.save()

        returnValue(CallResult(id=browsing_data_entry.id, cookie_id=browsing_data_entry.cookie_id,
                               sending_browsing_data=browsing_data_entry.send_cta_updates))

    @inlineCallbacks
    def disable_cta_updates(self, *args):
        """
        This procedure takes a given cookie_id corresponding to a presence health browsing data db row and sets its
        send_cta_updates value to True. When a given browsing data's instance is set to False, it will NOT publish the URL
        for the most updated CTA until set back to True.

        :param args: Argument list. Accepts only one argument
                     [cookie_id]
                     cookie_id: (type: String) Cookie id of presence health browsing data.
        :return: Returns keywords results that are accessible through the results' kwargs property.
                id: (type: Integer) Database id of newly created presence health browsing data row
                cookie_id: (type: String) Cookie id of newly created presence health browsing data row
                sending_browsing_data: (type: Boolean) Whether or not updated CTA's are being published for this entry.
        """

        browsing_data_entry = yield retrieve_presence_db_entry_from_args(args)

        browsing_data_entry.send_cta_updates = False

        browsing_data_entry = yield browsing_data_entry.save()

        returnValue(CallResult(id=browsing_data_entry.id, cookie_id=browsing_data_entry.cookie_id,
                               sending_browsing_data=browsing_data_entry.send_cta_updates))

@inlineCallbacks
def retrieve_presence_db_entry_from_args(args):
    """
    This function takes an argument list containing one argument, cookie_id, parses it for errors, and returns a
    twistar instance of the presence health browsing data table

    :param args: Argument list. Accepts only one argument
                 [cookie_id]
                 cookie_id: (type: String) Cookie id of presence health browsing data instance.
    :return:
    """
    cookie_id = check_args_for_cookie_id(args)

    browsing_data_entry = yield find_presence_health_db_entry_from_cookie_id(cookie_id)

    returnValue(browsing_data_entry)


def check_args_for_cookie_id(args):
    """
    This function takes an argument list containing one argument, cookie_id, parses it for errors, and returns the
    cookie_id

    :param args: Argument list. Accepts only one argument
                 [cookie_id]
                 cookie_id: (type: String) Cookie id of presence health browsing data instance.
    :return:
    """

    if len(args) != 1:
        raise Exception("function accepts exactly 1 positional argument, cookie_id.")
    cookie_id = args[0]
    # parse arguments for validity before processing
    if not isinstance(cookie_id, unicode) and not isinstance(cookie_id, str):
        raise Exception("cookie_id must be a unicode or string object. It is {}".format(type(cookie_id)))

    return cookie_id


def retrieve_cta_based_on_browsing_data(browsing_data_entry):
    """
    This function takes a twistar instance of the presence health browsing data table, calculates the appropriate call
    to action from the browsing data, and returns an HTTP url that contains information about the corresponding CTA
    in the JSON formatted BODY.

    :param browsing_data_entry: (type: twistar PresenceBrowsingData instance) Browsing data instance to retrieve browsing
                                data from
    :return:
    """

    cta_url = "https://picbackend.herokuapp.com/v2/cta/?intent="

    keyword_data_list = []
    max_intent_index_entry = {"keyword": None,
                              "clicks": -maxint - 1,
                              "hover_time": -maxint - 1,
                              "intent_index": -maxint - 1}
    max_clicks_entry = {"keyword": None,
                        "clicks": -maxint-1,
                        "hover_time": -maxint-1}
    max_hover_time_entry = {"keyword": None,
                            "clicks": -maxint - 1,
                            "hover_time": -maxint - 1}

    for keyword in BROWSING_KEYWORDS:
        keyword_clicks = getattr(browsing_data_entry, "{}_{}".format(keyword, "clicks"))
        keyword_hover_time = getattr(browsing_data_entry, "{}_{}".format(keyword, "hover_time"))
        keyword_data_list_entry = {"keyword": keyword,
                                   "clicks": keyword_clicks,
                                   "hover_time": keyword_hover_time,
                                   "intent_index": 10*keyword_clicks+keyword_hover_time}

        max_clicks_entry = max(max_clicks_entry, keyword_data_list_entry, key=lambda entry: entry['clicks'])
        max_hover_time_entry = max(max_hover_time_entry, keyword_data_list_entry, key=lambda entry: entry['hover_time'])
        max_intent_index_entry = max(max_intent_index_entry, keyword_data_list_entry, key=lambda entry: entry['intent_index'])
        keyword_data_list.append(keyword_data_list_entry)

    if max_hover_time_entry["intent_index"] > 0:
        cta_url += max_clicks_entry["keyword"]
    else:
        cta_url += "default"

    # if max_clicks_entry["clicks"] > 0:
    #     cta_url += max_clicks_entry["keyword"]
    # elif max_hover_time_entry["hover_time"] > 0:
    #     cta_url += max_clicks_entry["keyword"]
    # else:
    #     cta_url += "default"

    return cta_url
