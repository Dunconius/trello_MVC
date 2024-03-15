from datetime import date
import functools

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.card import Card, cards_schema, card_schema
from models.user import User
from controllers.comment_controller import comments_bp

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')
cards_bp.register_blueprint(comments_bp)

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        # if user is admin
        if user.is_admin:
            # continue and run decorated function
            return fn(*args, **kwargs)
        # else
        else:
            # return an error
            return {"error": "Not authorized to delete a card"}, 403
    return wrapper

# to get ALL the cards
@cards_bp.route('/')
def get_all_cards():
    stmt = db.select(Card).order_by(Card.date.desc())
    cards = db.session.scalars(stmt)
    return cards_schema.dump(cards)

# http://localhost:8080/cards/{card_id} - needs a dynamic route - GET
@cards_bp.route('/<int:card_id>')
def get_one_card(card_id):
    # will return empty list if id = non-existent
    stmt = db.select(Card).filter_by(id=card_id) # select * from cards where id={card_id}
    card = db.session.scalar(stmt)
    # if statement to return something logical in case of non-existent card
    if card:
        return card_schema.dump(card)
    else:
        return {"error": f"Card {card_id} not found"}, 404
    
# route to create cards:
@cards_bp.route("/", methods=["POST"])
@jwt_required()
def create_card():
    # this will now use the validation specified in the card model
    body_data = card_schema.load(request.get_json())
    # create new card model instance
    card = Card(
        title = body_data.get('title'),
        description = body_data.get('description'),
        date = date.today(),
        status = body_data.get('status'),
        priority = body_data.get('priority'),
        user_id = get_jwt_identity()
    )
    # add to session and commit
    db.session.add(card)
    db.session.commit()
    # return newly created card
    return card_schema.dump(card), 201

# route to delete cards - DELETE
@cards_bp.route("/<int:card_id>", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_card(card_id):
    # # check user admin status
    # is_admin = is_user_admin()
    # if not is_admin:
    #     return {"error": "Not authorized to delete a card"}, 403
    # # get card from database with card={card_id}
    stmt = db.select(Card).where(Card.id == card_id) # can also use filter by instead of where
    card = db.session.scalar(stmt)
    # if card exists
    if card:
        # delete from session and commit
        db.session.delete(card)
        db.session.commit()
        # return success message
        return {'message': f"Card {card.title} deleted successfully"}
    # else
    else:
        # return error message
        return {'error': f"Card {card_id} not found"}, 404

# dynamic route to update cards - PUT, PATCH
# PUT changes the whole resource. PATCH changes only the selected attributes
@cards_bp.route("/<int:card_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_card(card_id):
    # get the data to be updated from the request
    body_data = card_schema.load(request.get_json(), partial=True)
    # get the card from the db who needs to be update
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    # if card exists:
    if card:
        if str(card.user_id) != get_jwt_identity():
            return {"error": "Only card owner can edit card"}, 403
        # update the fields
        # updating with the request data or leaving as is - must do all editable fields
        card.title = body_data.get('title') or card.title 
        card.description = body_data.get('description') or card.description
        card.status = body_data.get('status') or card.status
        card.priority = body_data.get('priority') or card.priority
        # commit the changes
        db.session.commit()
        # return the updated card and success message
        return card_schema.dump(card)
    # else:
    else:
        # return error message
        return {'error': f"Card {card_id} not found"}, 404
    
def is_user_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin

