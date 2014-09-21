from battles import db
from battles.models.utils import deserialize_dt, serialize_dt


class Battle(db.Model):
    __tablename__ = "Battle"

    id = db.Column(db.Integer, primary_key=True)

    attacker_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    attacker = db.relationship(
        'User', backref=db.backref('battles_attacking', lazy='dynamic'),
        foreign_keys=[attacker_id])

    defender_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    defender = db.relationship(
        'User', backref=db.backref('battles_defending', lazy='dynamic'),
        foreign_keys=[defender_id])

    winner_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    winner = db.relationship(
        'User', backref=db.backref('battles_won', lazy='dynamic'),
        foreign_keys=[winner_id])

    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

    def __init__(self, fields={}):
        for k, v in fields.items():
            if callable(v):
                v = v()
            setattr(self, k, v)

    def __repr__(self):
        return '<Battle %s>' % self.id

    @classmethod
    def from_request_json(cls, d):
        """
        {
            “attacker”: <attacker_userid>,
            “defender”: <defender_userid>,
            “winner”: <winner_userid>,
            “start”: <battle_start_time>,
            “end”: <battle_end_time>
        }
        We expect start/end to come in like:
            2014-09-19T05:44:44.753Z
            %Y-%m-%dT%H:%M:%S.%fZ
        """
        return cls({
            "attacker_id": d["attacker"],
            "defender_id": d["defender"],
            "winner_id": d["winner"],
            "start": deserialize_dt(d["start"]),
            "end:": deserialize_dt(d["end"]),
        })

    def to_dict(self):
        """
        Returns JSON-serializable dict.
        """
        return {
            "attacker_id": self.attacker_id,
            "defender_id": self.defender_id,
            "winner_id": self.winner_id,
            "start": serialize_dt(self.start),
            "end": serialize_dt(self.end),
        }
