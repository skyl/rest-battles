from battles import db
from battles.models import User

from tests.base import BaseTestCase


class UserTestCase(BaseTestCase):

    def test_create_user_basic(self):
        u = User()
        db.session.add(u)
        db.session.commit()

    def test_create_user_update_last_seen(self):
        u = User({
            'first_name': 'Skylar',
            'last_name': 'Saveland',
            'nickname': 'skyl',
        })
        db.session.add(u)
        db.session.commit()
        u = User.query.filter_by(nickname='skyl').first()
        self.assertEqual(u.first_name, "Skylar")
        # they are actually not the same
        # self.assertEqual(u.last_seen_dt, u.created_dt)
        u.wins += 1
        db.session.add(u)
        db.session.commit()
        u = User.query.filter_by(nickname='skyl').first()
        self.assertGreater(u.last_seen_dt, u.created_dt)
        self.assertEqual(u.wins, 1)

    def test_callable_attr(self):
        nickf = lambda: "foobar"
        u = User({
            'first_name': 'Dale',
            'last_name': 'Earnhardt',
            'nickname': nickf,
        })
        db.session.add(u)
        db.session.commit()
        self.assertEqual(
            User.query.filter_by(nickname='foobar').first().first_name,
            'Dale')
        self.assertEqual(repr(u), '<User %s>' % nickf())

    def test_to_dict(self):
        u = User({
            'first_name': 'Waylon',
            'last_name': 'Jennings',
            'nickname': 'Hoss',
        })
        # have to save to get the created_dt not be None.
        db.session.add(u)
        db.session.commit()
        d = u.to_dict()
        self.assertEqual(d['last'], u.last_name)
        self.assertEqual(d['first'], u.first_name)
        self.assertEqual(d['nickname'], u.nickname)
