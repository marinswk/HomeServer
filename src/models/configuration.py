from app import db


class Configuration(db.Model):
    __tablename__ = "Configuration"

    id = db.Column("Id", db.Integer, primary_key=True)
    name = db.Column("Name", db.String(50))
    value = db.Column("Value", db.String(50))
    description = db.Column("Description", db.String(50))
