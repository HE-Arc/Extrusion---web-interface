from flask import Flask
from flask_restful import Api
from package.sequence.sequence_manager import SequenceManager

app = Flask(__name__)
api = Api(app)
global_var = {"started": False, "mode": "master", "state": "free"}
SequenceManager(global_var).start()
import views
