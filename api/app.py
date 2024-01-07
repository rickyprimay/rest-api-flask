# app.py
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)

@app.route("/api", methods=["GET", "POST"])
def example_resource():
    if request.method == "GET":
        return {"msg": "Hello, this is a serverless API"}
    elif request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        response = {"msg": "Success insert data", "name": name, "age": age}
        return response

CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run(debug=True)
