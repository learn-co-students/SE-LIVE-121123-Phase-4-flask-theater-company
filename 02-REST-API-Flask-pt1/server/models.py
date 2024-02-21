from flask_sqlalchemy import SQLAlchemy

# 6.✅ Import SerializerMixin from sqlalchemy_serializer


db = SQLAlchemy()


# 7.✅ Pass Productions the SerializerMixin
class Production(db.Model):
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

    cast_members = db.relationship("CastMember", back_populates="production")

    # 7.1 ✅ Create a serialize rule that will help prevent `cast_members` from recursion
    # 7.2 ✅ Create a serialize rule that will remove created_at and updated_at.
    # 7.3 Demo serialize_only by only allowing title to be included in the response
    #    once done remove or comment the serialize_only line.

    def __repr__(self):
        return f"<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>"


# 8.✅ Pass CastMember the SerializerMixin
class CastMember(db.Model):
    __tablename__ = "cast_members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"))
    production = db.relationship(Production, back_populates="cast_members")

    # 8.✅ Create a serialize rule that will prevent recursion with production

    def __repr__(self):
        return f"<Production Name:{self.name}, Role:{self.role}"


# 9.✅ Navigate back to `app.py` for further steps.
