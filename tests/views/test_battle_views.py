import json
import datetime

from battles import db
from battles.models import User, Battle
from battles.models.utils import serialize_dt

from tests.base import BaseTestCase


class BattleResourceTestCase(BaseTestCase):

    def _create_users(self):
        u1 = User({
            "nickname": "skyl"
        })
        u2 = User({
            "nickname": "tony"
        })
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        # sqlalchemy.orm.exc.DetachedInstanceError
        # why do we need to manually rehydrate these user objects?
        self.u1 = User({
            "nickname": "skyl"
        })
        self.u2 = User({
            "nickname": "tony"
        })

    def test_post_battle_happy_case(self):

        self._create_users()

        data = {
            "attacker": self.u2.id,
            "defender": self.u1.id,
            "winner": self.u1.id,
            "start": "2014-09-19T05:44:44.753Z",
            "end": "2014-09-19T05:45:44.753Z",
        }
        res = self.client.post(
            "/battles",
            data=json.dumps(data),
            content_type='application/json',
            headers=self.headers
        )
        self.assertEqual(res.status_code, 200)
        battles = Battle.query.all()
        self.assertEqual(len(battles), 1)
        b = battles[0]
        self.assertEqual(b.winner_id, self.u1.id)
        self.assertEqual(b.attacker_id, self.u2.id)
        self.assertEqual(b.defender_id, self.u1.id)
        self.assertIn("1", repr(b))

    def test_error(self):
        data = {
            "hrm": "blap",
        }
        res = self.client.post(
            "/battles",
            data=json.dumps(data),
            content_type="application/json",
            headers=self.headers
        )
        self.assertEqual(res.status_code, 400)

    def _create_battles(self):
        self._create_users()
        before = datetime.datetime(1990, 10, 10)
        self.start = start = datetime.datetime(1990, 10, 10, 1)
        within1 = datetime.datetime(1990, 10, 10, 2)
        within2 = datetime.datetime(1990, 10, 10, 3)
        self.end = end = datetime.datetime(1990, 10, 10, 4)
        after = datetime.datetime(1990, 10, 10, 5)
        d = {
            "attacker_id": self.u1.id,
            "defender_id": self.u2.id,
            "winner_id": self.u1.id,
        }
        # creates 5 battles, 1 before, 1 after, 3 within
        dates = [before, start, within1, within2, end, after]
        for i in range(len(dates) - 1):
            bd = d.copy()
            bd["start"] = dates[i]
            bd["end"] = dates[i + 1]
            b = Battle(bd)
            db.session.add(b)
        db.session.commit()

    def test_battles_date_range(self):
        self._create_battles()
        res = self.client.get(
            "/battles",
            query_string={
                "start": serialize_dt(self.start),
                "end": serialize_dt(self.end),
            },
            headers=self.headers,
        )
        self.assertEqual(res.status_code, 200)
        ret = json.loads(res.data.decode('utf-8'))
        self.assertEqual(len(ret), 3)

    def test_battles_no_querystring(self):
        self._create_battles()
        res = self.client.get("/battles", headers=self.headers)
        self.assertEqual(res.status_code, 400)
        self.assertIn("QueryString parameters required", str(res.data))
