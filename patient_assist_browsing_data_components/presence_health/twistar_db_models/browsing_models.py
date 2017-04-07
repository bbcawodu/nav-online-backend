from twistar.dbobject import DBObject
from patient_assist_db_models import BaseBrowsingDataClass


# using BaseBrowsingDataClass mixin may cause problems because there is no current_intent db field, currently no probs
class PresenceBrowsingData(DBObject, BaseBrowsingDataClass):
    TABLENAME = 'presencebrowsingdata'
