from flask import Flask
from .midnightstandings import midnightstandings
from .mcb import mcb

# Start Flask
qweb = Flask(__name__)

# Register Blueprints
qweb.register_blueprint(midnightstandings, url_prefix='/midnightstandings')
qweb.register_blueprint(mcb, url_prefix='/mcb')

import mcb, midnightstandings