import typing as t

from pydantic import BaseModel

from backend.app import db
from backend.api.mixins.pydantic_psql import BaseCrud
from backend.api.models.accounts import Accounts


class AccountsBase(BaseCrud, BaseModel):
    __model_kls__ = Accounts
    __db_session__ = db.session


class AccountsCreate(AccountsBase):
    name: str


class AccountsGet(AccountsBase):
    id: t.Optional[int] = None
    name: t.Optional[str] = None


class AccountsGetId(AccountsBase):
    id: int
