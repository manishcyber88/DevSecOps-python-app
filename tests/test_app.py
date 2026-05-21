import os
import tempfile
import pytest
from app import app, init_db, DB_PATH


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary DB for tests
    db_file = tmp_path / "test.db"
    monkeypatch.setattr('app.DB_PATH', str(db_file))
    init_db()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    rv = client.get('/')
    assert b'DevSecOps CI/CD Demo App' in rv.data
