import datetime
import os
import pytest
import copy

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from orm_models.blocking.presence import PresenceBrowsingData
from orm_models.blocking.presence import PresenceBrowsingIntentSnapshot
from orm_models.blocking.base import DeclarativeBase

TEST_BROWSING_DATA_VALUES = [
    {
        "date_created": datetime.datetime.utcnow(),
        "date_last_updated": datetime.datetime.utcnow(),
        "oncology_clicks": 12,
        "oncology_hover_time": 12.6
    },
    {
        "date_created": datetime.datetime.utcnow() - datetime.timedelta(days=1),
        "date_last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=1),
        "oncology_clicks": 2,
        "oncology_hover_time": 2.1
    },
    {
        "date_created": datetime.datetime.utcnow() - datetime.timedelta(days=2),
        "date_last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=2),
        "oncology_clicks": 4,
        "oncology_hover_time": 4.2
    },
    {
        "date_created": datetime.datetime.utcnow() - datetime.timedelta(days=3),
        "date_last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=3),
        "oncology_clicks": 6,
        "oncology_hover_time": 6.3
    },
    {
        "date_created": datetime.datetime.utcnow() - datetime.timedelta(days=4),
        "date_last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=4),
        "oncology_clicks": 8,
        "oncology_hover_time": 8.4
    },
    {
        "date_created": datetime.datetime.utcnow() - datetime.timedelta(days=5),
        "date_last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=5),
        "oncology_clicks": 10,
        "oncology_hover_time": 10.5
    },
]

TEST_INTENT_SNAPSHOT_VALUES = [
    {
        "date_created": datetime.datetime.utcnow(),
        "date_last_updated": datetime.datetime.utcnow(),
        "oncology_clicks": 12,
        "oncology_hover_time": 12.6,
        "calculated_intent": "oncology"
    },
    {
        "date_created": datetime.datetime.utcnow() - datetime.timedelta(days=1),
        "date_last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=1),
        "oncology_clicks": 2,
        "oncology_hover_time": 2.1,
        "calculated_intent": "oncology"
    },
    {
        "date_created": datetime.datetime.utcnow() - datetime.timedelta(days=2),
        "date_last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=2),
        "oncology_clicks": 4,
        "oncology_hover_time": 4.2,
        "calculated_intent": "oncology"
    },
    {
        "date_created": datetime.datetime.utcnow() - datetime.timedelta(days=3),
        "date_last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=3),
        "oncology_clicks": 6,
        "oncology_hover_time": 6.3,
        "calculated_intent": "oncology"
    },
    {
        "date_created": datetime.datetime.utcnow() - datetime.timedelta(days=4),
        "date_last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=4),
        "oncology_clicks": 8,
        "oncology_hover_time": 8.4,
        "calculated_intent": "oncology"
    },
    {
        "date_created": datetime.datetime.utcnow() - datetime.timedelta(days=5),
        "date_last_updated": datetime.datetime.utcnow() - datetime.timedelta(days=5),
        "oncology_clicks": 10,
        "oncology_hover_time": 10.5,
        "calculated_intent": "oncology"
    },
]


@pytest.fixture(scope="session", autouse=True)
def populate_test_db_for_http_server_tests(request):
    global transaction, connection, engine, test_app, test_db_obj, populate_session

    # Connect to the test database and create the schema using the declarative base metadata
    engine = create_engine(os.environ['TEST_DATABASE_URL'])
    DeclarativeBase.metadata.create_all(engine)

    # Create session and populate test db using the session
    populate_session_factory = sessionmaker(bind=engine)
    populate_session = populate_session_factory(expire_on_commit=False)

    test_browsing_session_objects = []
    test_intent_snapshot_objects = []

    for i, browsing_session_test_values_instance in enumerate(TEST_BROWSING_DATA_VALUES):
        browsing_data_model_obj = PresenceBrowsingData()
        for key, value in browsing_session_test_values_instance.items():
            setattr(browsing_data_model_obj, key, value)

        intent_snapshot_model_obj = PresenceBrowsingIntentSnapshot()
        for key, value in TEST_INTENT_SNAPSHOT_VALUES[i].items():
            setattr(intent_snapshot_model_obj, key, value)
        browsing_data_model_obj.browsing_intent_snapshots = [intent_snapshot_model_obj]

        populate_session.add(browsing_data_model_obj)

        test_browsing_session_objects.append(browsing_data_model_obj)
        test_intent_snapshot_objects.append(intent_snapshot_model_obj)

    populate_session.commit()

    request.addfinalizer(delete_test_data_and_destroy_test_db)


def delete_test_data_and_destroy_test_db():
    DeclarativeBase.metadata.drop_all(bind=engine)


def combinations(data):
    current_combo = []
    list_of_combos = []

    combinations_helper(current_combo, list_of_combos, data)

    return list_of_combos


def combinations_helper(current_combo, list_of_combinations, data):
    for i in range(len(data)):
        current_combo_copy = copy.copy(current_combo)

        current_combo_copy.append(data[i])
        data_copy = data[i+1:]

        list_of_combinations.append(current_combo_copy)

        combinations_helper(current_combo_copy, list_of_combinations, data_copy)
