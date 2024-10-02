

def test_transactions_get_all_endpoint(client, account_name):
    """
    WHEN a GET request is made to transactions endpoint
    THEN response of status 200 and return all transactions for the account.
    """
    get_trans_url = '/transactions?account_id=1'
    account_obj = {'name': account_name}
    account_obj = client.post('/accounts', json=account_obj)
    account_obj = account_obj.get_json()

    # when GET request for account-1 is made
    # then expect no objects returned
    response = client.get(get_trans_url)
    resp_json = response.get_json()
    assert len(resp_json) == 0

    # when a POST request to transactions is made
    transaction_1 = dict(
        account_id=account_obj['id'],
        amount=10,
        description='transaction_1',
    )
    response = client.post('/transactions', json=transaction_1)

    # then expect the transaction is created to that account
    resp_json = response.get_json()
    assert resp_json['description'] == transaction_1['description']
    assert resp_json['account_id'] == transaction_1['account_id']
    assert resp_json['type'] == 'credit'
    assert response.status_code == 201

    # when GET request for account-1 is made
    # then expect 1 object returned
    response = client.get(get_trans_url)
    resp_json = response.get_json()
    assert len(resp_json) == 1

    # when a POST request to transactions is made
    transaction_2 = dict(
        account_id=account_obj['id'],
        amount=-10,
        description='transaction_2',
    )
    response = client.post('/transactions', json=transaction_2)

    # then expect the transaction is created to that account
    resp_json = response.get_json()
    assert resp_json['description'] == transaction_2['description']
    assert resp_json['account_id'] == transaction_2['account_id']
    assert resp_json['type'] == 'debit'
    assert response.status_code == 201

    # when GET request for account-1 is made
    # then expect 2 object returned
    response = client.get(get_trans_url)
    resp_json = response.get_json()
    assert len(resp_json) == 2


def test_on_create_transaction_zero_amount_error(client, account_name):
    """
    GIVEN a zero amount to transactions
    WHEN a POST request is made to transactions endpoint
    THEN response of status 422 and error message zero not allowed.
    """
    get_trans_url = '/transactions?account_id=1'
    account_obj = {'name': account_name}
    account_obj = client.post('/accounts', json=account_obj)
    account_obj = account_obj.get_json()


    # when a POST request to transactions is made
    transaction = dict(
        account_id=account_obj['id'],
        amount=0,
        description='transaction',
    )
    response = client.post('/transactions', json=transaction)

    # then expect error message and 422 status
    resp_json = response.get_json()
    assert response.status_code == 422
    assert resp_json[0]['msg'] == 'Assertion failed, amount cannot be zero.'
