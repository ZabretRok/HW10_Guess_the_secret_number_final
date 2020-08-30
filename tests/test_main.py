import os
import pytest
from main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory;"
    client = app.test_client()

    cleanup()

    db.create_all()

    yield client

def cleanup():
    db.drop_all()

def test_index_not_logged_in(client):
    response = client.get('/')
    assert b'Enter your name' in response.data

def test_index_logged_in(client):
    client.post('/login', data={
        "user-name": "test_user",
        "user-email": "test@email.com",
        "user-password": "123"
    }, follow_redirects=True)
    response = client.get("/")
    assert b'Enter your guess' in response.data

def test_get_user_list(client):
    client.post('/login', data={
        "user-name": "test_user",
        "user-email": "test@email.com",
        "user-password": "123"
    })
    client.post('/login', data={
        "user-name": "test_user-2",
        "user-email": "test-2@email.com",
        "user-password": "123"
    })

    response = client.get("/users")

    assert b'test-user' in response.data
    assert b'test-user-2' in response.data

