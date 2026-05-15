import pytest, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, init_db

@pytest.fixture
def client(tmp_path):
    test_db = str(tmp_path / 'test.db')
    app.config['TESTING'] = True
    import app as app_module
    app_module.DB = test_db
    with app.test_client() as c:
        with app.app_context():
            init_db()
            yield c

def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_todo(client):
    response = client.post('/add', data={'task': 'Buy milk'})
    assert response.status_code == 302

def test_add_empty_task(client):
    response = client.post('/add', data={'task': ''})
    assert response.status_code == 302

def test_mark_done(client):
    client.post('/add', data={'task': 'Test task'})
    response = client.get('/done/1')
    assert response.status_code == 302
