from init import db, ma
from marshmallow import fields

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
    user = db.relationship('User', back_populates='cards')

class CardSchema(ma.Schema):
    # in order for marshmallow to serialise the user field we need to tell it that it's a relationship
    user = fields.Nested('UserSchema', only = ['name', 'email'])

    class Meta: # this is serializing the data
            fields = ('id', 'title', 'description', 'date', 'status', 'priority', 'user')

card_schema = CardSchema()
cards_schema = CardSchema(many=True)
