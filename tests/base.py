import unittest
import base64

from battles import db, app


class BaseTestCase(unittest.TestCase):

    headers = {
        "Authorization": "Basic %s" %
                         base64.b64encode(b"admin:secret").decode("ascii")
    }

    def setUp(self):
        db.create_all()
        self.app = app
        self.db = db
        self.client = app.test_client()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
