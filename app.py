from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)

@app.route("/")
def index():
    return "This is Restful API"

api = Api(app)

CORS(app)

identity = {}

class ExampleResource(Resource):
    def get(self):
        # response = {"msg" : "Hello this is restful API"}
        return identity
    
    def post(self):
        name = request.form["name"]
        age = request.form["age"]
        identity["name"] = name
        identity["age"] = age
        response = {"msg" : "Success insert data"}
        return response

    
api.add_resource(ExampleResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)