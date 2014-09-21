import json
import time

from functools import wraps

from flask import Response


def handles_errors(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # TODO - do something better to find these latere
            # logging, sentry, statsd, new relic ... ?
            # import traceback, sys
            # traceback.print_exception(*sys.exc_info(), file=sys.stdout)
            # TODO - don't return error, return hash as msg.
            ret = json.dumps({
                "error": True,
                "timestamp": int(time.time()),
                "msg": repr(e),
            })
            return Response(ret, 400)

    return decorated
