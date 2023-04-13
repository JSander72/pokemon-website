from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from . import routes 
#from . import models (doesn't exist yet, just save it for later)