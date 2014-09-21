from battles.models import Battle, User

from tests.base import BaseTestCase


class UserTestCase(BaseTestCase):

    def test_battle_callable_fields(self):
        u = User({
            "nickname": "foobar"
        })
        self.db.session.add(u)
        self.db.session.commit()
        b = Battle({
            "winner_id": lambda: u.id,
            "attacker_id": lambda: u.id,
        })
        self.db.session.add(b)
        self.db.session.commit()
        self.assertEqual(b.id, 1)
