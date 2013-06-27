# coding: utf-8

import os
import tempfile
import unittest
from flask import Flask
from .oauth1_server import create_server, db
from .oauth1_client import create_client


class BaseSuite(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.debug = True
        app.testing = True
        app.secret_key = 'development'

        self.db_fd, self.db_file = tempfile.mkstemp()
        config = {
            'OAUTH1_PROVIDER_ENFORCE_SSL': False,
            'OAUTH1_PROVIDER_KEY_LENGTH': (3, 30),
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///%s' % self.db_file
        }
        app.config.update(config)

        app = create_server(app)
        app = create_client(app)

        self.app = app
        self.client = app.test_client()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        os.close(self.db_fd)
        os.unlink(self.db_file)


class TestWebAuth(BaseSuite):
    def test_login(self):
        rv = self.client.get('/login')
        assert 'token' in rv.location