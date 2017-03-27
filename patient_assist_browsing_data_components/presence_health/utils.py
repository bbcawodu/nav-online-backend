from __future__ import print_function
from twisted.internet.defer import inlineCallbacks
from db_models import PresenceBrowsingData
from twisted.internet.defer import returnValue

BROWSING_KEYWORDS = ['oncology']


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
