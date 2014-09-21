import time
import json

from flask import Response, Blueprint, request, redirect

from battles import db
from battles.decorators.auth import requires_auth
from battles.decorators.errors import handles_errors
from battles.models import User

users = Blueprint('users', __name__)


@users.route('/users', methods=['POST'])
@requires_auth
@handles_errors
def create_user():
    u = User.from_request_json(request.get_json())
    db.session.add(u)
    db.session.commit()
    ret = {
        "error": False,
        "timestamp": int(time.time()),
        "userid": u.id
    }
    res = Response(json.dumps(ret), 200)
    res.headers['Content-Type'] = "application/json"
    return res


@users.route('/users/<userid>', methods=['PUT'])
@requires_auth
@handles_errors
def modify_user(userid):
    u = User.query.get(userid)
    j = request.get_json()
    setattr(u, j["field"], j["value"])
    db.session.add(u)
    db.session.commit()
    ret = {
        "error": False,
        "timestamp": int(time.time()),
    }
    return Response(json.dumps(ret), 200)


@users.route('/users/<userid>', methods=['GET'])
@requires_auth
@handles_errors
def detail_user(userid):
    u = User.query.get(userid)
    return Response(json.dumps(u.to_dict()), 200)


# TODO - should just make this a GET on /users instead of /users/search
@users.route('/users/search', methods=['GET'])
@requires_auth
@handles_errors
def search_users():
    nickname = request.args.get('nickname')
    u = User.query.filter_by(nickname=nickname).first()
    return redirect("/users/%s" % u.id, code=302)
