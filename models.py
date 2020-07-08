from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Pullrequest(db.Model):
    __tablename__ = "pullrequests"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    base = db.Column(db.String, nullable=False)
