#!/usr/bin/env python3

# Running React Together
# In Terminal, run:
# `honcho start -f Procfile.dev`

from config import api, app, db
from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    render_template,
    request,
    session,
)
from flask_cors import CORS
from flask_restful import Resource
from models import CastMember, Production, User, db
from werkzeug.exceptions import NotFound, Unauthorized

CORS(app)


@app.before_request
def check_if_logged_in():
    open_access_list = [
        "signup",
        "login",
        "logout",
        "authorized",
        "productions",
        "index",
        "static",
    ]

    if request.endpoint not in open_access_list and not session.get("user_id"):
        raise Unauthorized


@app.route("/")
@app.route("/<int:id>")
def index(id=0):
    return render_template("index.html")


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
            new_production = Production(**form_json)
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


class Signup(Resource):
    def post(self):
        req_json = request.get_json()
        try:
            new_user = User(
                name=req_json["name"],
                email=req_json["email"],
                password_hash=req_json["password"],
            )
        except:
            abort(422, "Invalid user data")
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return make_response(new_user.to_dict(), 201)


api.add_resource(Signup, "/signup")


class Login(Resource):
    def post(self):
        user = User.query.filter(User.name == request.get_json()["name"]).first()
        if user and user.authenticate(request.get_json()["password"]):
            session["user_id"] = user.id
            return make_response(user.to_dict(), 200)
        else:
            raise Unauthorized


api.add_resource(Login, "/login")


class AuthorizedSession(Resource):
    def get(self):
        try:
            user = User.query.filter_by(id=session["user_id"]).first()
            response = make_response(user.to_dict(), 200)
            return response
        except:
            raise Unauthorized


api.add_resource(AuthorizedSession, "/authorized")


class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        response = make_response("", 204)
        return response


api.add_resource(Logout, "/logout")


@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        {"message": "Not Found: Sorry the resource you are looking for does not exist"},
        404,
    )

    return response


@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    return make_response(
        {"message": "Unauthorized: you must be logged in to make that request."}, 401
    )


if __name__ == "__main__":
    app.run(port=5555, debug=True)
