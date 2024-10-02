

def test_health_endpoint(client):
    """
    WHEN get request is made to health endpoint
    THEN response of status 200 and {status=GREEN} object returned
    """
    response = client.get('/health')
    resp_json = response.get_json()

    assert response.status_code == 200
    assert resp_json == {'status': 'GREEN'}
