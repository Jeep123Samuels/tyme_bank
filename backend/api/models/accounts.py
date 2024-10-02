import enum

from backend.app import db
from backend.api.mixins.json_mixin import OutputMixin
from backend.api.mixins.timestamps import CreatedTimeStamps


class TransactionTypeEnum(str, enum.Enum):
    blank = ''
    credit = 'credit'
    debit = 'debit'


class Accounts(OutputMixin, CreatedTimeStamps, db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=100), unique=True, nullable=False)
