from init import db, ma
# this file is where we define the 'models'. Each table in the ERD is represented here as a model.

# here we are defining the Users model and declaring the different elements (columns) that appear in that particular model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# here we're making the User SCHEMA. Schemas define how data should be represented when it's transmitted over the network, usually in formats like JSON or XML.
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')

# instances for user schemas. One for handling many users, and one for handling a single used
user_schema = UserSchema(exclude=['password']) # deserializes a single dictionary {}
users_schema = UserSchema(many=True, exclude=['password']) # deserializes a list of dictionaries [{}, {}, {}]
