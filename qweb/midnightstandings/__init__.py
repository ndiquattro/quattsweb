from flask import Blueprint

midnightstandings = Blueprint('midnightstandings', __name__,
                              template_folder='templates',
                              static_folder='static')

import views
