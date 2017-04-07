from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import patient_assist_db_models as models


app = Flask(__name__)

app.config.from_object('patient_assist_admin.config')

db = SQLAlchemy(app)

admin = Admin(app, name='Patient Assist Admin', template_mode='bootstrap3')

browsing_data_column_list_base = ['cookie_id', 'send_cta_updates']
for browsing_keyword in models.BROWSING_KEYWORDS:
    for field, field_type in models.BROWSING_DATA_FIELDS.items():
        browsing_data_column_list_base.append('{}_{}'.format(browsing_keyword, field))
browsing_data_column_list_base.append("current_intent")


class BrowsingDataModelView(ModelView):
    can_create = False
    column_list = tuple(browsing_data_column_list_base)
admin.add_view(BrowsingDataModelView(models.PresenceBrowsingData, db.session))

"""
If you are wondering why the import statement is at the end and not at the beginning of the script as it is always done,
the reason is to avoid circular references, because you are going to see that the views module needs to import the app
variable defined in this script. Putting the import at the end avoids the circular import error.
"""
from patient_assist_admin.app import views
