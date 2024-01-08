from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api

import jwt
import datetime
#decorator
from functools import wraps

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = "testing-key"    

def token_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return make_response(jsonify({
                "msg" : "token not found"
            }), 404)
        try:
            output = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except: 
            return make_response(jsonify({
                "msg" : "invalid token"
            }))
        return function(*args, **kwargs)
    return decorator

class LoginUser(Resource):
    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password == 'root':
            token = jwt.encode({
                    "username" : username,
                    "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            return jsonify({
                "token" : token,
                "msg" : "you success to login"
            })
        
        return jsonify({
            "msg" : "wrong password or username"
        })

class Dashboard(Resource):
    @token_required
    def get(self):
        return jsonify({
            "msg" : "this is dashboard page can only access with login first"
        })    
    
class HomePage(Resource):
    def get(self):
        return jsonify({
            "msg" : "this is public page"
        })

api.add_resource(LoginUser, "/api/login", methods=["POST"])
api.add_resource(Dashboard, "/api/dashboard", methods=["POST", "GET"])
api.add_resource(HomePage, "/api", methods=["POST", "GET"])

if __name__ == "__main__":
    app.run(debug=True, port=5006)