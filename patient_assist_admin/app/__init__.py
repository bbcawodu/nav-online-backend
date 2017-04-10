from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from patient_assist_db_models import BROWSING_KEYWORDS
from patient_assist_db_models import BROWSING_DATA_FIELDS
from patient_assist_db_models import PresenceBrowsingData

# Create Flask WSGI object
app = Flask(__name__)

# Add app configs to WSGI object
app.config.from_object('patient_assist_admin.config')

# Create flask db object for WSGI app
db = SQLAlchemy(app)

# Create admin page for Flask app
admin = Admin(app, name='Patient Assist Admin', template_mode='bootstrap3')

# Create a field list for browsing data objects: for use in admin pages
browsing_data_column_list_base = ['cookie_id', 'send_cta_updates']
for browsing_keyword in BROWSING_KEYWORDS:
    for field, field_type in BROWSING_DATA_FIELDS.items():
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
from patient_assist_admin.app import views
