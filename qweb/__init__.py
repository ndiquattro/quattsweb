from flask import Flask
from .midnightstandings import midnightstandings
from .mcb import mcb

# Start Flask
qweb = Flask(__name__)

# Read config
qweb.config.from_pyfile('config.py')

# Register Blueprints
qweb.register_blueprint(midnightstandings, subdomain='midnightstandings')
qweb.register_blueprint(mcb, url_prefix='/mcb')
