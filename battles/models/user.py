import datetime

from battles import db
from battles.models.constants import DATE_FORMAT_STR

nowf = datetime.datetime.utcnow


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    nickname = db.Column(db.String(120), unique=True)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    current_win_streak = db.Column(db.Integer, default=0)
    created_dt = db.Column(db.DateTime, default=nowf)
    last_seen_dt = db.Column(db.DateTime, default=nowf, onupdate=nowf)

    def __init__(self, fields={}):
        for k, v in fields.items():
            if callable(v):
                v = v()
            setattr(self, k, v)

    def __repr__(self):
        return '<User %s>' % self.nickname

    @classmethod
    def from_request_json(cls, d):
        """
        converts JSON like
        {
            first: <first_name>,
            last: <last_name>,
            nickname: <nickname>
        }
        into a new User
        """
        return cls({
            "first_name": d['first'],
            "last_name": d['last'],
            "nickname": d['nickname'],
        })

    def to_dict(self):
        """
        JSON-serializable dict representation of the User instance.
        """
        return {
            "first": self.first_name,
            "last": self.last_name,
            "nickname": self.nickname,
            "wins": self.wins,
            "losses": self.losses,
            "current_win_streak": self.current_win_streak,
            "created": self.created_dt.strftime(DATE_FORMAT_STR),
            "last_seen_dt": self.last_seen_dt.strftime(DATE_FORMAT_STR),
        }
