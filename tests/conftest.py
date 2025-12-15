import os
import tempfile
import pytest
from app import app as flask_app

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True

    db_fd, db_path = tempfile.mkstemp()
    flask_app.config['DATABASE'] = db_path

    yield flask_app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()
