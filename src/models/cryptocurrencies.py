from app import db


class CryptoWalletConfig(db.Model):
    __tablename__ = "CryptoWalletConfig"

    id = db.Column("Id", db.Integer, primary_key=True)
    name = db.Column("Name", db.String(50))
    value = db.Column("Value", db.String(255))
    description = db.Column("Description", db.String(50))


class CryptoWalletManualAssets(db.Model):
    __tablename__ = "CryptoWalletManualAssets"

    id = db.Column("Id", db.Integer, primary_key=True)
    asset = db.Column("Asset", db.String(50))
    amount = db.Column("Amount", db.Float)
    exchange = db.Column("Exchange", db.String(50))


class ETHBlockchainAddresses(db.Model):
    __tablename__ = "ETHBlockchainAddresses"

    id = db.Column("Id", db.Integer, primary_key=True)
    address = db.Column("address", db.String(255))
    exchange = db.Column("Exchange", db.String(50))
