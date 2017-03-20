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


class PublishPresenceCTASComponent(ApplicationSession):
    """
    An application component that polls Presence Health browsing data entries for ones that have been updated recently
    and publishes the appropriate cta to appropriate topic based on browsing data and cookie_id
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("PublishPresenceCTASComponent attached")

        # Infinite loop, is always publishing
        while True:
            # Query presence browsing data for recently updated entries

            # loop through browsing data entries, find appropriate ctas, and publish to dynamic topic based on entry's
            # cookie id
            self.publish(u'examples.pubsub.complex.heartbeat')