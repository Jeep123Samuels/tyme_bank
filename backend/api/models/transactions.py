import enum

from sqlalchemy import orm

from backend.app import db
from backend.api.mixins.json_mixin import OutputMixin
from backend.api.mixins.timestamps import CreatedTimeStamps


class TransactionTypeEnum(str, enum.Enum):
    blank = ''
    credit = 'credit'
    debit = 'debit'


class Transactions(OutputMixin, CreatedTimeStamps, db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    type = db.Column(db.Enum(TransactionTypeEnum), nullable=False)
    description = db.Column(db.String(length=100), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    account = orm.relationship('Accounts')
