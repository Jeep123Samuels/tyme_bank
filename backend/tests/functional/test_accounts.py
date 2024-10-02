
def test_account_create_endpoint(client, account_name):
    """
    GIVEN an account object data
    WHEN a POST request is made to account endpoint
    THEN response of status 201 and return
    """
    account_obj = {'name': account_name}
    response = client.post('/accounts', json=account_obj)

    resp_json = response.get_json()

    assert response.status_code == 201
    assert resp_json['name'] == account_name


def test_accounts_get_all_endpoint(client, account_name_no_2):
    """
    WHEN a GET request is made to accounts endpoint
    THEN response of status 200 and return 2 objects
    """
    account_obj = {'name': account_name_no_2}
    client.post('/accounts', json=account_obj)

    response = client.get('/accounts')
    resp_json = response.get_json()

    assert response.status_code == 200
    assert len(resp_json) == 2


def test_accounts_get_endpoint(client, account_name):
    """
    WHEN a GET request is made to accounts/id endpoint
    THEN response of status 200 and return the specified account
    """
    response = client.get('/accounts/1')
    resp_json = response.get_json()

    assert response.status_code == 200
    assert resp_json['id'] == 1
    assert resp_json['name'] == account_name


def test_accounts_delete_endpoint(client):
    """
    WHEN a GET request is made to accounts endpoint
    THEN response of status 200 and return 2 objects
    WHEN a delete request is made to accounts/id endpoint
    THEN response of status 200 and
    WHEN a GET request is made to accounts endpoint
    THEN response of status 200 and return 1 objects
    """
    response = client.get('/accounts')
    resp_json = response.get_json()
    assert len(resp_json) == 2

    response = client.delete('/accounts/2')
    assert response.status_code == 200

    response = client.get('/accounts')
    resp_json = response.get_json()
    assert len(resp_json) == 1
