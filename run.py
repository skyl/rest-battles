import os
from battles import app, db
with app.app_context():
    db.create_all()
#import IPython; IPython.embed()
app.run(
    debug=True,
    host=os.environ.get("HOST", "127.0.0.1"),
    port=int(os.environ.get("PORT", 5000)),
)
