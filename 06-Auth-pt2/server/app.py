#!/usr/bin/env python3
# 📚 Review With Students:
# Set up:
# cd into server and run the following in Terminal:
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5000
# flask db init
# flask db revision --autogenerate -m'Create tables'
# flask db upgrade
# python seed.py
# Running React Together
# In Terminal, run:
# `honcho start -f Procfile.dev`

from config import api, app
from flask import Flask, abort, jsonify, make_response, request, session
from flask_restful import Resource
from models import CastMember, Production, User, db
from werkzeug.exceptions import NotFound, Unauthorized

# 0.0 Move Flask app and SQLAlchemy initialization and configuration to config.py
# 0.1 Update imports as necessary


# 2.✅ Navigate to "models.py"
# Continue on Step 3


# the following adds route-specific authoriztion
@app.before_request
def check_if_logged_in():
    open_access_list = ["signup", "login", "logout", "authorized"]

    if request.endpoint not in open_access_list and not session.get("user_id"):
        raise Unauthorized


class Productions(Resource):
    def get(self):
        production_list = [p.to_dict() for p in Production.query.all()]
        response = make_response(
            production_list,
            200,
        )

        return response

    def post(self):
        form_json = request.get_json()
        try:
            new_production = Production(
                title=form_json["title"],
                genre=form_json["genre"],
                budget=int(form_json["budget"]),
                image=form_json["image"],
                director=form_json["director"],
                description=form_json["description"],
            )
        except ValueError as e:
            abort(422, e.args[0])

        db.session.add(new_production)
        db.session.commit()

        response_dict = new_production.to_dict()

        response = make_response(
            response_dict,
            201,
        )
        return response


api.add_resource(Productions, "/productions")


class ProductionByID(Resource):
    def get(self, id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            raise NotFound
        production_dict = production.to_dict()
        response = make_response(production_dict, 200)

        return response

    def patch(self, id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            raise NotFound

        for attr in request.form:
            setattr(production, attr, request.form[attr])

        production.ongoing = bool(request.form["ongoing"])
        production.budget = int(request.form["budget"])

        db.session.add(production)
        db.session.commit()

        production_dict = production.to_dict()

        response = make_response(production_dict, 200)
        return response

    def delete(self, id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            raise NotFound
        db.session.delete(production)
        db.session.commit()

        response = make_response("", 204)

        return response


api.add_resource(ProductionByID, "/productions/<int:id>")


# 10.✅ Create a Signup route
class Users(Resource):
    def post(self):
        req_json = request.get_json()
        try:
            new_user = User(
                name=req_json["name"],
                email=req_json["email"],
                password_hash=req_json["password"],
            )
        except:
            abort(422, "Some values failed validation")
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id  # give the new_user "logged in status"
        return make_response(new_user.to_dict(), 201)


api.add_resource(Users, "/users", "/signup")


# User.query.order_by(User.id.desc()).first()._password_hash

# 11.✅ Create a Login route


@app.route("/login", methods=["POST"])
def login():
    user = User.query.filter_by(name=request.get_json()["name"]).first()
    if user and user.authenticate(request.get_json()["password"]):
        session["user_id"] = user.id  # "logs in" the user
        return make_response(user.to_dict(), 200)
    else:
        raise Unauthorized


# 12 Head to client/components/authenticate


# 13.✅ Create a route that checks to see if the User is currently in sessions


@app.route("/authorized")
def authorized():
    user = User.query.filter_by(id=session.get("user_id")).first()
    if not user:
        raise Unauthorized
        # abort(401, "User is unauthorized")
    return make_response(user.to_dict(), 200)


# 14.✅ Create a Logout route
# 14.1 Use add_resource to add a logout endpoint
# 14.2 Create a delete method
# 14.2.1 Set the user_id in sessions to None
# 14.2.1 Create a response with no content and a 204
# 14.3 Test out your route with the client or Postman
@app.route("/logout", methods=["DELETE"])
def logout():
    # session["user_id"] = None
    session.clear()
    return make_response({}, 204)


# 14.✅ Navigate to client navigation


@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        {"message": "Not Found: Sorry the resource you are looking for does not exist"},
        404,
    )

    return response


@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    response = make_response(
        {"message": "Unauthorized: you must be logged in to make that request."},
        401,
    )

    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
