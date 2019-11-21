"""Insta485 package initializer."""
import flask


# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name


app.config.from_object('quant.config')
app.config.from_envvar("QUANT_SETTINGS", silent=True)

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import quant.api	 # noqa: E402 pylint: disable=wrong-import-position
import quant.api.model

# initialize extension
from flask_cognito import CognitoAuth
cogauth = CognitoAuth(app)

@cogauth.identity_handler
def lookup_cognito_user(payload):
    """Look up user in our database from Cognito JWT payload."""
    return User.query.filter(User.cognito_username == payload['username']).one_or_none()
