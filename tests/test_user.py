from fastapi.testclient import TestClient
from main import app

# Create user test
def test_create_user_ok():
    client = TestClient(app)

    user = {
        'email': 'test_create_user_ok@cosasdedevs.com',
        'username': 'test_create_user_ok',
        'password': 'admin123'
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['email'] == user['email']
    assert data['username'] == user['username']

# Create duplicate email
def test_create_user_duplicate_email():
    client = TestClient(app)

    user = {
        'email': 'test_create_user_duplicate_email@cosasdedevs.com',
        'username': 'test_create_user_duplicate_email',
        'password': 'admin123'
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 201, response.text

    user['username'] = 'test_create_user_duplicate_email2'

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Email already exists'

# Create duplicate user
def test_create_user_duplicate_username():
    client = TestClient(app)

    user = {
        'email': 'test_create_user_duplicate_username@cosasdedevs.com',
        'username': 'test_create_user_duplicate_username',
        'password': 'admin123'
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 201, response.text


    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data['detail'] == 'Username already exists'

# test login
def test_login():
    client = TestClient(app)
    
    user = {
        'email': 'testlogin@cosasdedevs.com',
        'username': 'testlogin',
        'password': 'admin123'
    }

    response = client.post(
        '/api/v1/user/',
        json=user,
    )
    assert response.status_code == 201, response.text   
    
    login = {
        'username': 'testlogin',
        'password': 'admin123'
    }
    
    response = client.post(
        '/api/v1/login/',
        data=login,
        headers = {
            'headers': 'application/x-www-form-urlencoded'
        },
        allow_redirects=True
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data['access_token']) > 0
    assert data['token_type'] == 'bearer'