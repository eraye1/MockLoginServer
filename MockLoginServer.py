from flask import Flask, request, jsonify
from functools import wraps
import hashlib

app = Flask(__name__)

# Authentication
# Yes, this should be a separate file or module, but wouldn't you like to use this
# as one file as opposed to a bunch?
def check_auth(username, password):
    return username == 'admin' and password == 'secret'

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

# Routing
@app.route('/users/<userid>', methods = ['GET'])
def api_users(userid):
    users = {'1':'john', '2':'steve', '3':'bill'}

    if userid in users:
        return jsonify({userid:users[userid]})
    else:
        return not_found()

@app.route('/basicAuth')
@requires_auth
def api_hello():
    return "Shhh this is top secret spy stuff!"

@app.route('/login')
@requires_auth
def api_login():
    username = request.authorization.username
    password = request.authorization.password

    hashUsernameAndPassword = hashlib.sha224(username + password).hexdigest()

    message = {
        'status' : 200,
        'session' : hashUsernameAndPassword
    }

    resp = jsonify(message)
    resp.status_code = 200

    return resp

# Error Messages
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

#App running
if __name__ == '__main__':
    app.run()