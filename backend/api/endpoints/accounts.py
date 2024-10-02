from flask import make_response
from flask_openapi3 import APIBlueprint, Tag

from backend.api.serializers import (
    AccountsCreate,
    AccountsGet,
    AccountsGetId,
)


accounts_tag = Tag(name='accounts', description='Accounts')

accounts_bp = APIBlueprint(
    'accounts',
    __name__,
    abp_tags=[accounts_tag],
    abp_security=[{"jwt": []}],
)


@accounts_bp.get('/accounts/<int:id>')
def get_account(path: AccountsGetId):
    return make_response(path.get_obj(**dict(rel=True)), 200)


@accounts_bp.get('/accounts')
def get_accounts():
    return make_response(
        AccountsGet().get_objects(**dict(rel=True)),
        200
    )


@accounts_bp.post('/accounts')
def create_account(body: AccountsCreate):
    return make_response(body.get_or_create(**dict(rel=True)), 201)


@accounts_bp.delete('/accounts/<int:id>')
def delete_account(path: AccountsGetId):
    return make_response(
        path.hard_delete(),
        200,
    )
