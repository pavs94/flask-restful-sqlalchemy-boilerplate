from flask import Flask,request, jsonify
from flask_restful import Api, Resource
from db import *

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self):
        return jsonify(message="Hello World")

class User(Resource):
    def get(self):
        email=request.args['email']
        user=dbGetUser(email)
        user=json.loads(user)
        return jsonify(user)

api.add_resource(Test, '/')
api.add_resource(User, '/user')


if __name__ == '__main__':
    app.run(debug=True)