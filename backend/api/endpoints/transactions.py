from flask import make_response
from flask_openapi3 import APIBlueprint, Tag

from backend.api.models.transactions import TransactionTypeEnum
from backend.api.serializers import (
    AccountsGet,
    TransactionsCreate,
    TransactionsGet,
    TransactionsGetId,
    TransactionsUpdate,
)


transactions_tag = Tag(name='transactions', description='Transactions')

transactions_bp = APIBlueprint(
    '/transactions',
    __name__,
    abp_tags=[transactions_tag],
    abp_security=[{"jwt": []}],
)


def is_debit_or_credit(amount):
    return (
        TransactionTypeEnum.debit
        if amount < 0 else TransactionTypeEnum.credit
    )


@transactions_bp.get('/transactions/<int:id>')
def get_transaction(path: TransactionsGetId):
    return make_response(path.get_obj(**dict(rel=True)), 200)


@transactions_bp.get('/transactions')
def get_transactions(query: TransactionsGet):
    extra_kw = dict(rel=query.get_related)
    data = query.model_dump(exclude_unset=True, exclude={'get_related'})
    return make_response(
        TransactionsGet(**data).get_objs_by_order(
            order_by=dict(field="created_time", desc=True),**extra_kw),
        200
    )


@transactions_bp.put('/transactions/<int:id>')
def update_transactions(path: TransactionsGetId, body: TransactionsUpdate):
    data = body.model_dump(exclude_unset=True)
    if 'amount' in data:
        data['type'] = is_debit_or_credit(data['amount'])
    return make_response(
        TransactionsUpdate(**data).update(
            filter_fields=dict(id=path.id), **dict(rel=True)),
        200,
    )


@transactions_bp.post('/transactions')
def create_transaction(body: TransactionsCreate):
    # Check if account exist
    if not AccountsGet(**dict(id=body.account_id)).get_obj():
        return make_response(
            {
                'message': f'Please create '
                           f'Account ID `{body.account_id}` first.'
            },
            400
        )
    body.type = is_debit_or_credit(body.amount)
    return make_response(body.create(**dict(rel=True)), 201)


@transactions_bp.delete('/transactions/<int:id>')
def delete_transactions(path: TransactionsGetId):
    return make_response(
        path.hard_delete(),
        200,
    )
