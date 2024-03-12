from init import db, ma
from marshmallow import fields
# this file is where we define the 'models'. Each table in the ERD is represented here as a model.

# here we are defining the Users model and declaring the different elements (columns) that appear in that particular model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    cards = db.relationship('Card', back_populates='user', cascade='all, delete')

    comments = db.relationship("Comment", back_populates="user", cascade="all, delete")

# here we're making the User SCHEMA. Schemas define how data should be represented when it's transmitted over the network, usually in formats like JSON or XML.
class UserSchema(ma.Schema):

    cards = fields.List(fields.Nested('CardSchema', exclude=['user']))

    comments = fields.List(fields.Nested('CommentSchema', exclude=["user"]))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin', 'cards', 'comments')

# instances for user schemas. One for handling many users, and one for handling a single used
user_schema = UserSchema(exclude=['password']) # deserializes a single dictionary {}
users_schema = UserSchema(many=True, exclude=['password']) # deserializes a list of dictionaries [{}, {}, {}]
