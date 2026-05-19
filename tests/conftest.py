import os
import tempfile

import pytest
from voxpopulli import create_app
from voxpopulli.db import get_db, init_db

test_sql_path = os.path.join(os.path.dirname(__file__), 'data.sql')
with open(test_sql_path, 'rb') as f:
    test_sql = f.read().decode('utf8')

@pytest.fixture(scope='module')
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app()
    app.config.update(
        {"TESTING": True,
         "DATABASE": db_path}
    )

    with app.app_context():
        init_db()
        db = get_db()
        db.executescript(test_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture()
def client(app):
    return app.test_client()
