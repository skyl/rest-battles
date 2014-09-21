import time
import json

from flask import Response, Blueprint, request

from battles import db
from battles.decorators.auth import requires_auth
from battles.decorators.errors import handles_errors
from battles.models import Battle
from battles.models.utils import deserialize_dt

battles = Blueprint('battles', __name__)


@battles.route('/battles', methods=['POST'])
@requires_auth
@handles_errors
def create_battle():
    # TODO: validate start before end?
    b = Battle.from_request_json(request.get_json())
    db.session.add(b)
    db.session.commit()
    ret = {
        "error": False,
        "timestamp": int(time.time()),
    }
    res = Response(json.dumps(ret), 200)
    res.headers['Content-Type'] = "application/json"
    return res


START_END_REQUIRED_MSG = """
QueryString parameters required, start and end:
?start=%Y-%m-%dT%H:%M:%S.%fZ&end=%Y-%m-%dT%H:%M:%S.%fZ
"""


@battles.route('/battles', methods=['GET'])
@requires_auth
@handles_errors
def report_battles():
    """
    /battles?start=<starttime>&end=<endtime>
      display battle logs for specified time rage

    Interpret this as returning all battles whose start is >= <start> param
    and end is <= <end> param
    """
    # TODO: pagination
    # TODO: better define desired behavior - no querystring?
    # for now, just return 400 - require start and end
    if "start" not in request.args or "end" not in request.args:
        return Response(START_END_REQUIRED_MSG, 400)
    start = deserialize_dt(request.args.get("start"))
    end = deserialize_dt(request.args.get("end"))
    battles = Battle.query.filter(Battle.start >= start, Battle.end <= end)
    j = [b.to_dict() for b in battles]
    return Response(json.dumps(j), 200)
