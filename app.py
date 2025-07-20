from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="flask_crud_app.log",
)

app = Flask(__name__)
# RODAR SOMENTE EM TESTE LOCAL
if environ.get('DB_URL') is None:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

# BUILD PARA DOCKER
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password, phone, address, is_admin):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.address = address
        self.is_admin = is_admin

    def json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "password": self.password, "phone": self.phone, "address": self.address
                , "is_admin": self.is_admin}

#create a main route / with message "up and running"
@app.route("/")
def index():
    try:
        db.create_all()
        logging.info('[/] Success.')
        return "up and running"
    except Exception as e:
        print(e)
        logging.exception('[/] Exception found: \n\n%s', e)
        return "Database already created"

#create a retrieve route
@app.route("/users", methods=["GET"])
def get_all():
    try:
        users = User.query.all()

        if len(users):
            response = make_response(jsonify({"code": 200,"data": {"users": [user.json() for user in users]}}), 200)                
        else:
            response = make_response(jsonify({"code": 404,"data": {"users": []}}), 404)
        logging.info('[GET /users] Success.')
        return response
    except Exception as e:
        logging.exception('[GET /users] Exception found: \n\n%s', e)
        return make_response(jsonify({"code": 500, "message": "An error occurred while getting users."}), 500)

# create a route to retrieve a user by id
@app.route("/users/<int:id>", methods=["GET"])
def get_user_by_id(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            response = make_response(jsonify({"code": 200, "data": {"user": user.json()}}), 200)
        else:
            response = make_response(jsonify({"code": 404, "data": {"user": None}}), 404)
        logging.info('[GET /users/id] Success.')
        return response        
    except Exception as e:
        logging.exception('[GET /users/id] Exception found: \n\n%s', e)
        return make_response(jsonify({"code": 500, "message": "An error occurred while getting user."}), 500)

# create a route to retrieve a user by is_admin is True
@app.route("/users/admin", methods=["GET"])
def get_admin_users():
    try:
        users = User.query.filter_by(is_admin=True).all()
        if users:
            response = make_response(jsonify({"code": 200, "data": {"users": [user.json() for user in users]}}), 200)
        else:
            response = make_response(jsonify({"code": 404, "data": {"users": []}}), 404)
        logging.info('[GET /users/admin] Success.')
        return response
    except Exception as e:
        logging.exception('[GET /users/admin] Exception found: \n\n%s', e)
        return make_response(jsonify({"code": 500, "message": "An error occurred while getting admin users."}), 500)

# create a route to retrieve a user by name
@app.route("/users/name/<name>", methods=["GET"])
def get_user_by_name(name):
    try:
        users = []
        users_res = User.query.filter(User.name.ilike(f"%{name}%")).all()

        for user in users_res:
            users.append(user.json())

        if users:
            response = make_response(jsonify({"code": 200, "data": {"user": users}}), 200)
        else:
            response = make_response(jsonify({"code": 404, "data": {"user": None}}), 404)
        logging.info('[GET /users/name/] Success.')
        return response
    except Exception as e:
        logging.exception('[GET /users/name] Exception found: \n\n%s', e)
        return make_response(jsonify({"code": 500, "message": "An error occurred while getting user."}), 500)

# create a route to create a user
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data_res = request.get_json()
        if isinstance(data_res, dict):
            data_res = [data_res]

        for data in data_res:
            user = User(data["name"], data["email"], data["password"], data["phone"], data["address"], data["is_admin"])
            db.session.add(user)
            db.session.commit()
        logging.info('[POST /users] Success.')
        return make_response(jsonify({"code": 201, "data": {"user": user.json()}}), 201)
    except Exception as e:
        logging.exception('[POST /users] Exception found: \n\n%s', e)
        return make_response(jsonify({"code": 500, "message": "An error occurred while creating user."}), 500)

# create a route to update a user
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    try:
        data = request.get_json()
        user = User.query.filter_by(id=id).first()
        if user:
            user.name = data["name"]
            user.email = data["email"]
            user.password = data["password"]
            user.phone = data["phone"]
            user.address = data["address"]
            user.is_admin = data["is_admin"]
            db.session.commit()
            response = make_response(jsonify({"code": 200, "data": {"user": user.json()}}), 200)
        else:
            response = make_response(jsonify({"code": 404, "data": {"user": None}}), 404)
        logging.info('[PUT /users/id] Success.')
        return response
    except Exception as e:
        logging.exception('[PUT /users/id] Exception found: \n\n%s', e)
        return make_response(jsonify({"code": 500, "message": "An error occurred while updating user."}), 500)

# create a route to update all users
@app.route("/users", methods=["PUT"])
def update_all_users():
    try:
        res = request.get_json()

        for data in res:
            user = User.query.filter_by(email=data['email']).first()
            if user:
                user.name = data["name"]
                user.email = data["email"]
                user.password = data["password"]
                user.phone = data["phone"]
                user.address = data["address"]
                user.is_admin = data["is_admin"]
                db.session.commit()
            else:
                user = User(data["name"], data["email"], data["password"], data["phone"], data["address"], data["is_admin"])
                db.session.add(user)
                db.session.commit()

        users = User.query.all()
        logging.info('[PUT /users] Success.')
        return make_response(jsonify({"code": 200, "data": {"users": [user.json() for user in users]}}), 200)
        
    except Exception as e:
        logging.exception('[PUT /users] Exception found: \n\n%s', e)
        return make_response(jsonify({"code": 500, "message": "An error occurred while updating users."}), 500) 


# create a route to delete a user
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            response = make_response(jsonify({"code": 200, "data": {"user": user.json()}}), 200)
        else:
            response = make_response(jsonify({"code": 404, "data": {"user": None}}), 404)
        logging.info('[DELETE /users/id] Success.')
        return response
    except Exception as e:
        logging.exception('[DELETE /users/id] Exception found: \n\n%s', e)
        return make_response(jsonify({"code": 500, "message": "An error occurred while deleting user."}), 500)

# create a route to delete all users
@app.route("/users", methods=["DELETE"])
def delete_all_users():
    try:
        users = User.query.all()
        if users:
            for user in users:
                db.session.delete(user)
            db.session.commit()
            response = make_response(jsonify({"code": 200, "data": {"users": [user.json() for user in users]}}), 200)
        else:
            response = make_response(jsonify({"code": 404, "data": {"users": []}}), 404)
        logging.info('[DELETE /users] Success.')
        return response
    except Exception as e:
        logging.exception('[DELETE /users] Exception found: \n\n%s', e)
        return make_response(jsonify({"code": 500, "message": "An error occurred while deleting users."}), 500)

# RODAR SOMENTE EM TESTE LOCAL
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True)