from __future__ import print_function
import json
from datetime import datetime

from twistar.dbobject import DBObject
from twistar.registry import Registry
from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue

from sqlalchemy_blocking_orm_models.presence_db_models.base import BaseClassForTableWithIntentFields
from sqlalchemy_blocking_orm_models.presence_db_models.base import INTENT_KEYWORDS
from sqlalchemy_blocking_orm_models.presence_db_models.base import INTENT_KEYWORD_FIELD_NAMES_W_TYPES
from sqlalchemy_blocking_orm_models.base import CURRENT_INTENT_FORMULA_VERSION


# using BaseBrowsingDataClass mixin may cause problems because there is no current_intent db field, currently no probs
class PresenceBrowsingData(DBObject, BaseClassForTableWithIntentFields):
    TABLENAME = 'presencebrowsingdata'

    HASMANY = [
        {
            'name': 'non_blocking_intent_snapshots',
            'class_name': 'PresenceBrowsingIntentSnaphot',
            'foreign_key': 'presence_browsing_session_data_id'
        }
    ]

    def return_values_dict(self):
        values_dict = {
            "id": self.id
        }

        if self.date_created:
            values_dict["date_created"] = self.date_created.isoformat()

        if self.date_last_updated:
            values_dict["date_last_updated"] = self.date_last_updated.isoformat()

        for intent_keyword in INTENT_KEYWORDS:
            for field_name, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
                keyword_field_name = "{}_{}".format(intent_keyword, field_name)
                values_dict[keyword_field_name] = getattr(self, keyword_field_name)

        return values_dict


# using BaseBrowsingDataClass mixin may cause problems because there is no current_intent db field, currently no probs
class PresenceBrowsingIntentSnaphot(DBObject, BaseClassForTableWithIntentFields):
    TABLENAME = 'presence_browsing_intent_snapshot'

    def return_values_dict(self):
        values_dict = {
            "id": self.id,
            'presence_browsing_session_data_id': self.presence_browsing_session_data_id if hasattr(self, 'presence_browsing_session_data_id') else None,
            "calculated_intent": self.calculated_intent,
            "intent_formula_version": self.intent_formula_version
        }

        if self.date_created:
            values_dict["date_created"] = self.date_created.isoformat()

        for intent_keyword in INTENT_KEYWORDS:
            for field_name, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
                keyword_field_name = "{}_{}".format(intent_keyword, field_name)
                values_dict[keyword_field_name] = getattr(self, keyword_field_name)

        return values_dict


Registry.register(PresenceBrowsingData, PresenceBrowsingIntentSnaphot)


@inlineCallbacks
def non_blocking_create_presence_browsing_session_data_row():
    presence_browsing_session_data_row = PresenceBrowsingData()
    presence_browsing_session_data_row = yield presence_browsing_session_data_row.save()

    for browsing_keyword in INTENT_KEYWORDS:
        setattr(presence_browsing_session_data_row, "{}_{}".format(browsing_keyword, "clicks"), 0)
        setattr(presence_browsing_session_data_row, "{}_{}".format(browsing_keyword, "hover_time"), 0.0)

    current_date_time = datetime.utcnow()
    presence_browsing_session_data_row.date_created = current_date_time
    presence_browsing_session_data_row.date_last_updated = current_date_time

    presence_browsing_session_data_row = yield presence_browsing_session_data_row.save()

    returnValue(presence_browsing_session_data_row)


@inlineCallbacks
def non_blocking_update_presence_session_row_w_submitted_data(presence_browsing_session_data_row, browsing_keyword, keyword_clicks, keyword_hover_time):
    """
    This function takes a presence browsing data twistar instance and submitted browsing data as arguments and uses
    the submitted data to update and save the twistar instance. The updated instance is returned.

    :param presence_browsing_session_data_row: (type: twistar PresenceBrowsingData instance) Presence Browsing Data instance.
    :param browsing_keyword: (type: String or Unicode) Browsing data keyword to update.
    :param keyword_clicks: (type: Integer) Number of clicks for corresponding keyword.
    :param keyword_hover_time: (type: Float) Amount of time, in seconds, of hover time for corresponding keyword.
    :return: (type: twistar PresenceBrowsingData instance) Updated Presence Browsing Data instance.
    """

    if browsing_keyword not in INTENT_KEYWORDS:
        raise Exception("'keyword' must be in the following list of accepted keywords: {}.".format(json.dumps(INTENT_KEYWORDS)))
    else:
        clicks_field_name = "{}_{}".format(browsing_keyword, "clicks")
        entry_clicks_value = getattr(presence_browsing_session_data_row, clicks_field_name)
        hover_time_field_name = "{}_{}".format(browsing_keyword, "hover_time")
        entry_hover_time_value = getattr(presence_browsing_session_data_row, hover_time_field_name)

        if entry_clicks_value is None:
            setattr(presence_browsing_session_data_row, clicks_field_name, keyword_clicks)
        else:
            setattr(presence_browsing_session_data_row, clicks_field_name, entry_clicks_value + keyword_clicks)

        if entry_hover_time_value is None:
            setattr(presence_browsing_session_data_row, hover_time_field_name, keyword_hover_time)
        else:
            setattr(presence_browsing_session_data_row, hover_time_field_name, entry_hover_time_value + keyword_hover_time)

    current_date_time = datetime.utcnow()
    presence_browsing_session_data_row.date_last_updated = current_date_time

    presence_browsing_session_data_row = yield presence_browsing_session_data_row.save()

    returnValue(presence_browsing_session_data_row)


@inlineCallbacks
def non_blocking_get_browsing_session_data_row_by_id(browsing_session_data_id):
    browsing_data_entry = yield PresenceBrowsingData.findBy(id=browsing_session_data_id)
    if not browsing_data_entry:
        raise Exception("No Presence Health Browsing data entry found for id: {}".format(browsing_session_data_id))
    elif len(browsing_data_entry) > 1:
        raise Exception(
            "More than one Presence Health Browsing data entry found for id: {}".format(browsing_session_data_id))
    else:
        returnValue(browsing_data_entry[0])


@inlineCallbacks
def non_blocking_create_intent_snapshot_row(browsing_session_data_row_id):
    presence_browsing_session_data_row = yield non_blocking_get_browsing_session_data_row_by_id(browsing_session_data_row_id)
    intent_snapshot_row = PresenceBrowsingIntentSnaphot()
    intent_snapshot_row.presence_browsing_session_data_id = presence_browsing_session_data_row.id

    for browsing_keyword in INTENT_KEYWORDS:
        keyword_clicks_field_name = "{}_{}".format(browsing_keyword, "clicks")
        keyword_hover_time_field_name = "{}_{}".format(browsing_keyword, "hover_time")

        setattr(intent_snapshot_row, keyword_clicks_field_name, getattr(presence_browsing_session_data_row, keyword_clicks_field_name))
        setattr(intent_snapshot_row, keyword_hover_time_field_name, getattr(presence_browsing_session_data_row, keyword_hover_time_field_name))

    intent_snapshot_row.calculated_intent = presence_browsing_session_data_row.current_intent
    intent_snapshot_row.intent_formula_version = CURRENT_INTENT_FORMULA_VERSION

    current_date_time = datetime.utcnow()
    intent_snapshot_row.date_created = current_date_time

    intent_snapshot_row = yield intent_snapshot_row.save()

    returnValue(intent_snapshot_row)


@inlineCallbacks
def non_blocking_get_intent_snapshot_rows_from_session_id(browsing_session_data_row_id):
    presence_browsing_session_data_row = yield non_blocking_get_browsing_session_data_row_by_id(browsing_session_data_row_id)
    intent_snapshots_for_this_session = yield presence_browsing_session_data_row.non_blocking_intent_snapshots.get()

    returnValue(intent_snapshots_for_this_session)


@inlineCallbacks
def non_blocking_get_intent_snapshot_row_by_id(intent_snapshot_row_id):
    intent_snapshot_row = yield PresenceBrowsingIntentSnaphot.findBy(id=intent_snapshot_row_id)
    if not intent_snapshot_row:
        raise Exception("No presence_browsing_intent_snapshot row found for id: {}".format(intent_snapshot_row_id))
    elif len(intent_snapshot_row) > 1:
        raise Exception(
            "More than one presence_browsing_intent_snapshot row was found for id: {}".format(intent_snapshot_row_id))
    else:
        returnValue(intent_snapshot_row[0])
