from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(20), default='text')  # 'text' or 'image'
    
    def to_dict(self):
        return {
            'id': self.id,
            'section': self.section,
            'key': self.key,
            'value': self.value,
            'content_type': self.content_type
        }

class ClientLogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    order_index = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_path': self.image_path,
            'order_index': self.order_index
        }

