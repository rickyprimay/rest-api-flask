import os
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
CORS(app)


# configure db
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

db = SQLAlchemy(app)

# create model db
class ModelDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    address = db.Column(db.TEXT)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

@app.route("/")
def index():
    return render_template("index.html")

class ExampleResource(Resource):
    def get(self):
        query = ModelDb.query.all()
        output = [
            {
                "id": data.id,
                "name": data.name, 
                "age": data.age, 
                "address": data.address
            } 
            for data in query
        ]

        response = {
            "code" : 200,
            "msg" : "Query Data Success",
            "data" : output
        }

        return response, 200
    
    def post(self):
        dataName = request.form["name"]
        dataAge = request.form["age"]
        dataAddress = request.form["address"]

        model = ModelDb(name=dataName, age=dataAge, address=dataAddress)
        model.save()

        response = {
            "Message": "Success insert data",
            "Status Code": 200
        }

        return response
    def delete(self):
        query = ModelDb.query.all()
        for data in query:
            db.session.delete(data)
            db.session.commit()
        response = {
            "msg": "Delete all data success",
            "code": "200"
        }
        return response
    

class UpdateResource(Resource):
    def put(self, id):
        query = ModelDb.query.get(id)

        if query is None:
            response = {
                "msg": "Data Not Found",
                "code": "404"
            }
            return response

        editName = request.form['name']
        editAge = request.form['age']
        editAddress = request.form['address']

        query.name = editName
        query.age = editAge
        query.address = editAddress
        db.session.commit()

        response = {
            "msg" : "edit data success",
            "code" : "200"
        }

        return response
    def delete(self, id):
        query = ModelDb.query.get(id)
        if query is None:
            response = {
                "msg": "Data Not Found",
                "code": "404"
            }
            return response

        db.session.delete(query)
        db.session.commit()

        response = {
            "msg" : "Delete data success",
            "code" : "200"
        }
        return response

api.add_resource(ExampleResource, "/api", methods=["GET", "POST", "DELETE"])
api.add_resource(UpdateResource, "/api/<id>", methods=["PUT", "DELETE"])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5005)
