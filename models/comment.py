from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = "comments"

    # fields native to this table
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)

    # foreign fields --------------------------- table/column they come from
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), nullable=False)

    # this helps format the returned value to be more readable, giving us both the card and the user details
    user = db.relationship("User", back_populates="comments")
    card = db.relationship("Card", back_populates="comments")

class CommentSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=['name', 'email'])

    card = fields.Nested('CardSchema', exclude=['comments'])

    class Meta:
        fields = ('id', 'message', 'user', 'card')

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

