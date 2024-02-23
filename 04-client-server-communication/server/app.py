#!/usr/bin/env python3
# 📚 Review With Students:
# CORS
# Set up:
# cd into server and run the following in Terminal
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5000
# flask db init
# flask db revision --autogenerate -m'Create tables'
# flask db upgrade
# python seed.py
# cd into client and run `npm`
# Running React Together
# Verify that gunicorn and honcho have been added to the pipenv
# Create Procfile.dev in root
# in Procfile.dev add:
# web: PORT=3000 npm start --prefix client
# api: gunicorn -b 127.0.0.1:5000 --chdir ./server app:app
# In Terminal, cd into root and run:
# `honcho start -f Procfile.dev`

from flask import Flask, abort, make_response, request

# 5.✅ Import CORS from flask_cors, invoke it and pass it app
#   5.1Start up the server / client and navigate to client/src/App.js
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Actor, CastMember, Production, db
from werkzeug.exceptions import NotFound

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

Api.error_router = lambda self, handler, e: handler(e)
api = Api(app)


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
        # 4.✅ Add a try except, try to create a new production. If a ValueError is raised call abort with a 422 and pass it the validation errors.
        try:
            # new_production = Production(
            #     title=form_json["title"],
            #     genre=form_json["genre"],
            #     budget=int(form_json["budget"]),
            #     image=form_json["image"],
            #     director=form_json["director"],
            #     description=form_json["description"],
            # )
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
        try:
            for attr in request.form:
                setattr(production, attr, request.form[attr])

            production.ongoing = bool(request.form["ongoing"])
            production.budget = int(request.form["budget"])
        except ValueError as e:
            abort(422, e.args[0])

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


class CastMembers(Resource):
    def get(self):
        cast_members_list = [
            cast_member.to_dict() for cast_member in CastMember.query.all()
        ]

        response = make_response(cast_members_list, 200)
        return response

    def post(self):
        request_json = request.get_json()
        new_cast = CastMember(
            actor_id=request_json["actor_id"],
            role=request_json["role"],
            production_id=request_json["production_id"],
        )
        db.session.add(new_cast)
        db.session.commit()

        response_dict = new_cast.to_dict()

        response = make_response(response_dict, 201)
        return response


api.add_resource(CastMembers, "/cast_members")


#'/cast_members/<int:id>'
class CastMembersByID(Resource):
    def get(self, id):
        cast_member = CastMember.query.filter_by(id=id).first()
        if not cast_member:
            abort(404, "The cast_member you were looking for was not found!")

        cast_member_dict = cast_member.to_dict()
        response = make_response(cast_member_dict, 200)

        return response

    # patch
    def patch(self, id):
        cast_member = CastMember.query.filter_by(id=id).first()
        if not cast_member:
            abort(404, "The cast member you were trying to update was not found!")

        request_json = request.get_json()
        for key in request_json:
            setattr(cast_member, key, request_json[key])

        db.session.add(cast_member)
        db.session.commit()

        response = make_response(cast_member.to_dict(), 200)

        return response

    def delete(self, id):
        cast_member = CastMember.query.filter_by(id=id).first()
        if not cast_member:
            abort(404, "The cast_member you were trying to delete was not found!")

        db.session.delete(cast_member)
        db.session.commit()

        response = make_response("", 204)

        return response


api.add_resource(CastMembersByID, "/cast_members/<int:id>")


@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        f"Not Found: Sorry the {request.path.strip('/1234567890').title()} resource you are looking for does not exist",
        404,
    )

    return response


# To run the file as a script
if __name__ == "__main__":
    app.run(port=5555, debug=True)
