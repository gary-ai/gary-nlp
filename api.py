from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "gary_db"
mongo = PyMongo(app, config_prefix='MONGO')
APP_URL = "http://mongo:5000"


class GaryNlp(Resource):
    @staticmethod
    def get(user=None, command=None, channel=None):
        if user and command and channel:
            user_config = mongo.db.student.find_one({"userid": user}, {"_id": 0})
            if user_config:
                return jsonify({"status": "ok", "data": user_config})
            else:
                return {"response": "no config found for {}".format(user)}


class Index(Resource):
    def get(self):
        return redirect(url_for("matching"))


api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(GaryNlp, "/api/<string:user>/<string:command>/<string:channel>", endpoint="matching")

if __name__ == "__main__":
    app.run(debug=True)
