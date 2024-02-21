from flask_sqlalchemy import SQLAlchemy

# 6.✅ Import SerializerMixin from sqlalchemy_serializer
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


# 7.✅ Pass Productions the SerializerMixin
class Production(db.Model, SerializerMixin):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # SQLAlchemy will create a list of CastMembers which belong to a Production
    # sqlalchemy_serializer will treat cast_members as another attribute of a Production and serialize the list
    # this will create recursion when it also tries to serialize the production on a cast_member > the cast_members of that production > the production of each cast_member...etc. forever
    cast_members = db.relationship("CastMember", back_populates="production")

    # 7.1 ✅ Create a serialize rule that will help prevent `cast_members` from recursion
    # 7.2 ✅ Create a serialize rule that will remove created_at and updated_at.
    serialize_rules = ("-created_at", "-updated_at", "-cast_members.production")
    # 7.3 Demo serialize_only by only allowing title to be included in the response
    #    once done remove or comment the serialize_only line.
    # serialize_only = ("title", "director")

    def __repr__(self):
        return f"<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>"


# 8.✅ Pass CastMember the SerializerMixin
class CastMember(db.Model, SerializerMixin):
    __tablename__ = "cast_members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"))
    # This relationship must be here for 'back_populates' to work.  It is the mirror of 'cast_members' on Production
    # The first arg to relationship() can be either a ref to the model class OR a string naming the model class
    production = db.relationship(Production, back_populates="cast_members")

    # 8.✅ Create a serialize rule that will prevent recursion with production
    serialize_rules = ("-production.cast_members", "-created_at", "-updated_at")

    def __repr__(self):
        return f"<Production Name:{self.name}, Role:{self.role}"


# 9.✅ Navigate back to `app.py` for further steps.
