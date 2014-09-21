import json

from battles import db
from battles.models import User

from tests.base import BaseTestCase


class UserResourceTestCase(BaseTestCase):

    def test_401_without_basic_auth(self):
        res = self.client.post(
            "/users", data="", content_type="application/json")
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            res.headers['WWW-Authenticate'], 'Basic realm="Login Required"')

    def test_post_user_happy_case(self):
        data = {
            "first": "Skylar",
            "last": "Saveland",
            "nickname": "skyl",
        }
        res = self.client.post(
            "/users",
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers
        )
        users = User.query.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].nickname, "skyl")

        ret = json.loads(res.data.decode('utf-8'))
        self.assertEqual(ret['userid'], 1)
        self.assertEqual(ret['error'], False)
        self.assertIn('timestamp', ret)

    def test_modify_user(self):
        u = User()
        db.session.add(u)
        db.session.commit()
        put = {
            "field": "last_name",
            "value": "Henderson",
        }
        res = self.client.put(
            "/users/1",
            data=json.dumps(put),
            content_type='application/json',
            headers=self.headers,
        )
        self.assertEqual(res.status_code, 200)

        u = User.query.get(1)
        self.assertEqual(u.last_name, "Henderson")

    def test_detail_user(self):
        u = User({
            "first_name": "Merle",
            "last_name": "Haggard",
            "nickname": "Hag",
        })
        db.session.add(u)
        res = self.client.get(
            "/users/1",
            headers=self.headers,
        )
        self.assertEqual(res.status_code, 200)
        ret = json.loads(res.data.decode('utf-8'))
        self.assertEqual(ret["first"], "Merle")
        self.assertEqual(ret["last"], "Haggard")
        self.assertEqual(ret["nickname"], "Hag")

    def test_search_users(self):
        u = User({
            "first_name": "foo",
            "last_name": "bar",
            "nickname": "baz",
        })
        db.session.add(u)
        res = self.client.get(
            "/users/search?nickname=%s" % "baz",
            headers=self.headers
        )
        self.assertEqual(res.status_code, 302)
        self.assertIn("/users/1", res.headers['location'])
