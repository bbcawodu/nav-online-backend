from __future__ import print_function
from twisted.internet.defer import inlineCallbacks
from twistar_db_models import PresenceBrowsingData
from twisted.internet.defer import returnValue


@inlineCallbacks
def find_presence_health_db_entry_from_cookie_id(cookie_user_id):
    """
    This function takes a cookie id, parses it for any errors, and returns the corresponding Presence Browsing Data
    instance.

    :param cookie_user_id: (type: String) Cookie id of presence health browsing data row.
    :return: (type: twistar PresenceBrowsingData instance) Presence Browsing Data instance.
    """

    browsing_data_entry = yield PresenceBrowsingData.findBy(cookie_id=cookie_user_id)
    if not browsing_data_entry:
        raise Exception("No Presence Health Browsing data entry found for cookie_id: {}".format(cookie_user_id))
    elif len(browsing_data_entry) > 1:
        raise Exception(
            "More than one Presence Health Browsing data entry found for cookie_id: {}".format(cookie_user_id))
    else:
        returnValue(browsing_data_entry[0])
