import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from applications.extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='User ID')
    username = db.Column(db.String(20), comment='User Name')
    password_hash = db.Column(db.String(128), comment='Password Hash')
    role = db.Column(db.String(20), comment='Role')

    status = db.Column(db.Integer, comment='Status')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='Create Time')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                            comment='Update Time')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
