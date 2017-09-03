from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

from blocking_orm_models import PresenceBrowsingData
from blocking_orm_models.presence_db_models.base import INTENT_KEYWORDS
from blocking_orm_models.presence_db_models.base import \
    INTENT_KEYWORD_FIELD_NAMES_W_TYPES

# Create Flask WSGI object
app = Flask(__name__)

# Add app configs to WSGI object
app.config.from_object('http_server_pkg.config')

# Create flask db object for WSGI app
db = SQLAlchemy(app)

# Create admin page for Flask app
admin = Admin(app, name='Patient Assist Admin', template_mode='bootstrap3')

# Create a field list for browsing data objects: for use in admin pages
browsing_data_column_list_base = []
for browsing_keyword in INTENT_KEYWORDS:
    for field, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
        browsing_data_column_list_base.append('{}_{}'.format(browsing_keyword, field))
browsing_data_column_list_base.append("current_intent")


# Add admin pane for each db model
class BrowsingDataModelView(ModelView):
    can_create = False
    column_list = tuple(browsing_data_column_list_base)
admin.add_view(BrowsingDataModelView(PresenceBrowsingData, db.session))

"""
If you are wondering why the import statement is at the end and not at the beginning of the script as it is always done,
the reason is to avoid circular references, because you are going to see that the views module needs to import the app
variable defined in this script. Putting the import at the end avoids the circular import error.
"""
from http_server_pkg.app import views
