from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# allowing only specific values for the card status field
# all caps means these variables should be constant
VALID_STATUSES = ("To Do", "Ongoing", "Done", "Testing", "Deployed")
VALID_PRIORITIES = ("Low", "Medium", "High", "Urgent")

class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) # string is limited to 255 chars
    description = db.Column(db.Text) # text can be a lot longer than string
    date = db.Column(db.Date) # Date card was created
    status = db.Column(db.String)
    priority = db.Column(db.String)

    # -------------------------------------- name of the users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # when adding foreign keys, will always be int (as its the ID#)

    # -------------name of the User Class
    user = db.relationship('User', back_populates='cards') # a user can have multiple cards
    comments = db.relationship('Comment', back_populates='card', cascade='all, delete') # a comment can only have a single card

class CardSchema(ma.Schema):

    # validating using marshmallow -------------------- condition ---- error message
    # must be validated in card controller
    title = fields.String(required=True, validate=And(
         Length(min=2, error="Title must be 2 chars long"),
         Regexp('^[a-zA-Z0-9 ]+$', error="Title can only have alphanumeric characters")
    ))
    
    status = fields.String(validate=OneOf(VALID_STATUSES))
    priority = fields.String(validate=OneOf(VALID_PRIORITIES))

    # There can only be one card with status 'Ongoing'
    @validates('status')
    def validate_status(_, value):
        if value == VALID_STATUSES[1]:
            stmt = db.select(db.func.count()).select_from(Card).filter_by(status=VALID_STATUSES[1])
            count = db.session.scalar(stmt)
            if count > 0:
                raise ValidationError('You already have an ongoing card')

    # in order for marshmallow to serialise the user field we need to tell it that it's a relationship
    user = fields.Nested('UserSchema', only = ['name', 'email'])
    comments = fields.List(fields.Nested("CommentSchema", exclude=['card']))

    class Meta: # this is serializing the data
            fields = ('id', 'title', 'description', 'date', 'status', 'priority', 'user', 'comments')
            ordered=True

card_schema = CardSchema()
cards_schema = CardSchema(many=True)
