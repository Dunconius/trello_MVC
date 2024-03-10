# this file for making routes for authorization and login.
# python libraries
from datetime import timedelta

# libraries we installed
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from psycopg2 import errorcodes

# imports from local files
from init import db, bcrypt
from models.user import User, user_schema

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # URL prefix means all following with be under this folder

@auth_bp.route("/register", methods=["POST"]) # /auth/register
def auth_register():
    try:
        # this data comes from the body of the request (in insomnia)
        body_data = request.get_json()
        # create the user instance (without password)
        user = User(
            name=body_data.get('name'),
            email=body_data.get('email')
        )
        # password from the request body
        password = body_data.get('password')
        # if password exists, hash the password and apply it directly to the user
        if password:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')

        # add and commit the user to the database
        db.session.add(user)
        db.session.commit()
        # respond back through the client
        # The '201 Created' status code means that the request was successfully fulfilled and resulted in one or possibly multiple new resources being created.
        return user_schema.dump(user), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The {err.orig.diag.column_name} is required"} 
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use"}, 409  # 409 = conflict
    
@auth_bp.route("/login", methods=["POST"]) #auth/login
def auth_login():
    # get the request body
    body_data = request.get_json()
    # from the User database, find the user with that email
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # if user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # create jwt (JSON Web Token)
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        # return the token along with the user information
        return {"emil": user.email, "token": token, "is_admin": user.is_admin}
    # else
    else:
        # return error
        return {"error": "Invalid email or password"}, 401 # The 401 Unauthorized.
    
