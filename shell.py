from battles import app, db

from battles.models import *
print(sorted(k for k in locals().keys() if not k.startswith("_")))
import IPython
IPython.embed()
