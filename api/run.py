from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
global_var = {"started": False, "mode": "user", "state": "free"}
import views
