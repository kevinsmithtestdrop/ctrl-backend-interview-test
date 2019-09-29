# Flask framework
from flask import Flask, url_for, request
from functools import wraps
import json
import platform
import locale
import datetime
import jwt

locale.setlocale(locale.LC_ALL, str('en_US.UTF-8'))

app = Flask(__name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """ Auth decorator function"""
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]  # Removes "Bearer" section from token (Postman)

        for at in auth_tokens:
            if decode_auth_token(token) == at[0]:
                if token.encode() != at[1]:
                    return {'detail': 'Incorrect authentication credentials.'}, 403

        return f(*args, **kwargs)

    return decorated


def list_routes():
    import urllib.parse
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)
    return sorted(output)


# Substituting a database system here for test
user = [(1, {'username': 'SolidSnake', 'email': 'a@a.com', 'balance': 1600.0}),
        (2, {'username': 'HanSolo', 'email': 'b@b.com', 'balance': 1500.0}),
        (3, {'username': 'Rick', 'email': 'c@c.com', 'balance': 0.0})
        ]

# example of auth token for SolidSnake
auth_tokens = [(0, 'xxxxxx')]

SECRET_KEY = 'wubba_lubba_dub_dub'

"""
Lets assume you are building the auth yourself or using a framework's auth. You can get creative and use whatever 
you need.

I am not testing a in depth-knowledge of flask ,merely thinking behind building an API.

To test the API I recommend using Insomnia or Postman:https://www.getpostman.com/apps or https://insomnia.rest/download/

If I have create a example endpoint on the root endpoint http://localhost:8000/ and health endpoint 
http://localhost:8000/health

Add a authentication endpoint                                    
 * POST request with email and password
 * Returns a auth token to user and stores it

Add a GET user endpoint (retrieve user)
 * Requires authenticated user (Header with Authorization:token

Add a POST user endpoint to create a new user
* This requires a POST request capturing the email, username and password
* returns auth token much like authentication

Add a GET with auth to get the user's balance - balance inquiry    

Bonus: one POST request for both credit and debit. Hint query/params 

"""


@app.route('/', methods=['GET'])
def root():
    return app.response_class(
        json.dumps({
            "message": "Welcome to the Ctrl API test",
            "endpoints": list_routes()
        })
    )


@app.route('/health', methods=['GET'])
def health():
    platform_string = "{} - {} - {}".format(
        # platform.machine(),
        # platform.version(),
        # platform.platform(),
        platform.uname(),
        platform.system(),
        platform.processor()
    )
    return app.response_class(
        json.dumps({
            "message": "I seem to be healthy",
            "whoami": platform_string
        })
    )


def encode_auth_token(user_id):
    """
    Generates a Auth token to add to the auth_tokens list of tuples
    :return: exception or a encoded token.
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(token):
    """
    Decodes auth token being used by a user.
    :param token:
    :return: error string or a user_id for identification
    """
    try:
        payload = jwt.decode(token, SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token Expired. Please log in again'
    except jwt.InvalidTokenError:
        return 'Token Invalid. Please log in again'


def create_token(user_id):
    token = ''.encode()
    for at in auth_tokens:
        if at[0] == user_id:
            token = at[1]  # existing token
        else:
            token = encode_auth_token(user_id)  # new token.
            auth_tokens.append((user_id, token))
    return token


@app.route('/auth/login', methods=['POST'])
def authentication():
    """
    Auth function to create an associate an auth token for a user wanting to perform operations with the API
    :return: json object with the token in queue.
    """
    email = request.form.get('email')
    password = request.form.get('password')  # password is irrelevant
    user_id = 0

    for details in user:
        if details[1]['email'] == email:
            user_id = details[0]  # what is needed for the auth token "db mimic"

    if user_id == 0:
        return app.response_class(json.dumps({'detail': 'You don’t have the right credentials for access'})), 401

    # this is where the should be a password check. for this test it doesnt matter - skip psw check

    token = create_token(user_id)

    return app.response_class(
        json.dumps({
            'status': 'success',
            'message': 'Successfully authorized.',
            'access_token': token.decode()
        })
    )


@app.route('/auth/register', methods=['POST'])
def register():
    """
    Auth and register function to create and associate an auth token for a new user wanting to perform operations
    with the API. There are checks in place to prohibit duplicates
    :return: json object with the token in queue.
    """
    email = request.form.get('email')
    password = request.form.get('password')  # password is irrelevant
    username = request.form.get('username')

    for details in user:
        if details[1]['email'] == email:
            return app.response_class(json.dumps({'detail': 'Email already exits'})), 403
        if details[1]['username'] == username:
            return app.response_class(json.dumps({'detail': 'Username already exits'})), 403

    user_count = len(user)
    new_user_id = user_count + 1

    user.append((new_user_id, {'username': username, 'email': email, 'balance': 0.0}))

    token = create_token(new_user_id)

    return app.response_class(
        json.dumps({
            'status': 'success',
            'message': 'Successfully created new user.',
            'access_token': token.decode()
        })
    )


@app.route('/user', methods=['GET'])
@token_required
def user_endpoint():
    """
    Retrieve user details if there is an Auth token present
    :return: json object containing user details as per the dummy database
    """
    username = ''
    email = ''
    balance = ''

    token = request.headers['Authorization'].split()[1]
    user_id = decode_auth_token(token)

    for u in user:
        if u[0] == user_id:
            username = u[1]['username']
            email = u[1]['email']
            balance = u[1]['balance']

    return app.response_class(
        json.dumps({
            "user_id": user_id,
            "username": username,
            "email": email,
            "balance": balance,
        })
    )


@app.route('/user/balance', methods=['GET'])
@token_required
def user_balance():
    """
    Retrieve user details if there is an Auth token present
    :return: json object containing user details as per the dummy database
    """
    balance = ''

    token = request.headers['Authorization'].split()[1]
    user_id = decode_auth_token(token)

    for u in user:
        if u[0] == user_id:
            balance = u[1]['balance']

    return app.response_class(
        json.dumps({
            "balance": balance,
        })
    )


@app.route('/user/transact', methods=['POST'])
@token_required
def transaction():
    """
    Perform a credit or debit based on query/parameters placed in the api call.
    Allow negative balances to exits.
    :return: json object as result with transaction outcome.
    """
    username = ''
    email = ''
    balance = 0.00
    new_balance = 0.00

    amount = request.args.get('amount')
    tran_type = request.args.get('tran_type')

    token = request.headers['Authorization'].split()[1]
    user_id = decode_auth_token(token)

    # tuples are immutable, delete and recreate the user.
    for u in user:
        if u[0] == user_id:
            balance = u[1]['balance']
            username = u[1]['username']
            email = u[1]['email']
            user.remove(u)

    if tran_type == 'debit':
        new_balance = balance - float(amount)

    if tran_type == 'credit':
        new_balance = balance + float(amount)

    user.append((user_id, {'username': username, 'email': email, 'balance': new_balance}))

    return app.response_class(
        json.dumps({
            'status': 'success',
            'transaction_type': tran_type,
            'amount': amount
        })
    )
