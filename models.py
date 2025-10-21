# models.py
from datetime import datetime
from db import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, index=True, nullable=False)
    author = db.Column(db.String(120), nullable=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "author": self.author,
            "text": self.text,
            "created_at": None if not self.created_at else self.created_at.isoformat(),
            "updated_at": None if not self.updated_at else self.updated_at.isoformat(),
        }
