from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api

import jwt
import datetime
#decorator
from functools import wraps

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = "testing-key"

class LoginUser(Resource):
    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password == 'root':
            token = jwt.encode({
                    "username" : username,
                    "exp" : datetime.datetime.utcnow() + datetime.timedelta(),
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            return jsonify({
                "token" : token,
                "msg" : "you success to login"
            })
        
        return jsonify({
            "msg" : "please log in"
        })
    
api.add_resource(LoginUser, "/api/login", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5006)