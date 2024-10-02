import typing as t
from decimal import Decimal

from pydantic import BaseModel, Field, ValidationInfo, field_validator

from backend.app import db
from backend.api.mixins.pydantic_psql import BaseCrud
from backend.api.models.transactions import Transactions, TransactionTypeEnum


class TransactionsBase(BaseCrud, BaseModel):
    __model_kls__ = Transactions
    __db_session__ = db.session


class ValidatorZero:
    @field_validator('amount')
    @classmethod
    def not_zero(cls, v: Decimal, info: ValidationInfo) -> Decimal:
        assert v != Decimal(0), f'{info.field_name} cannot be zero.'
        return v


class TransactionsCreate(ValidatorZero, TransactionsBase):
    amount: Decimal = Field(max_digits=11, decimal_places=2)
    description: str
    type: t.Optional[str] = None
    account_id: int


class TransactionsUpdate(ValidatorZero, TransactionsBase):
    amount: t.Optional[Decimal] = Field(
        max_digits=11,
        decimal_places=2,
        default=None,
    )
    description: t.Optional[str] = None
    type: t.Optional[str] = None


class TransactionsGet(TransactionsBase):
    id: t.Optional[int] = None
    account_id: t.Optional[int] = None
    description: t.Optional[str] = None
    type: t.Optional[TransactionTypeEnum] = TransactionTypeEnum.blank
    get_related: t.Optional[bool] = False

class TransactionsGetId(TransactionsBase):
    id: int
