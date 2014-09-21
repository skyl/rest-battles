from functools import wraps
from flask import request, Response


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        "Please login",
        401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    # print("REQUIRES OUTER!")

    @wraps(f)
    def decorated(*args, **kwargs):
        # print("DECORATED")
        # print(request.headers)
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
