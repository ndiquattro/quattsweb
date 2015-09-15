from flask import Blueprint

mcb = Blueprint('mcb', __name__, template_folder='templates',
                static_folder='static')

import views
