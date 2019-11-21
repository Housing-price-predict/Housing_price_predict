import json

from flask import Flask, abort
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse

from time import time
from functools import wraps
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature


class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, username):
        info = {
            'username': username,
            'creation_time': time()
        }

        token = self.serializer.dumps(info)
        return token.decode()

    def validate_token(self, token):
        info = self.serializer.loads(token.encode())

        if time() - info['creation_time'] > self.expires_in:
            raise SignatureExpired("The Token has been expired; get a new token")

        return info['username']


SECRET_KEY = "A SECRET KEY; USUALLY A VERY LONG RANDOM STRING"
expires_in = 600
auth = AuthenticationToken(SECRET_KEY, expires_in)

app = Flask(__name__)
api = Api(app,
          authorizations={
                'API-KEY': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'AUTH-TOKEN'
                }
            },
          security='API-KEY',
          default="Product prediction",
          title="Product prediction",
          description="This is an api to predict the house product price")

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authentication token is missing')

        try:
            user = auth.validate_token(token)
        except SignatureExpired as e:
            abort(401, e.message)
        except BadSignature as e:
            abort(401, e.message)

        return f(*args, **kwargs)

    return decorated

credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str)
credential_parser.add_argument('password', type=str)


@api.route('/token')
class Token(Resource):
    @api.response(200, 'Successful')
    @api.doc(description="Generates a authentication token")
    @api.expect(credential_parser, validate=True)
    def get(self):
        args = credential_parser.parse_args()

        username = args.get('username')
        password = args.get('password')

        if username == 'admin' and password == 'admin':
            return {"token": auth.generate_token(username)}

        return {"message": "authorization has been refused for those credentials."}, 401

@api.route('/product_predict')
@api.param('Rooms', 'number of rooms the house has', request=True)
@api.param('Type', 'house type', request=True)
@api.param('Method', 'what is the situation of the house', request=True)
@api.param('Field', 'house postcode', request=True)
@api.param('Regionname', 'where is the house', request=True)
@api.param('Distance', 'the distance from CBD in kilometres', request=True)
@api.param('Bedroom', 'number of bedrooms', request=True)
@api.param('Bathroom', 'number of bathroom', request=True)
@api.param('Car', 'number of carpots', request=True)
@api.param('Landsize', 'land size in metres', request=True)

class prediction(Resource):
    @api.response(200, 'Successful')
    @api.response(400, 'Validation Error')
    @api.doc(description="Predicting the house product pricing")
    @requires_auth
    def get(self):
        # AI 使用插入
        def predict_price(att_l):
            return att_l
        # AI 使用插入

        def get_int_parameter(name, min_n, max_n):
            try:
                result = int(request.args.get(name))
            except:
                return {"message": name + " is invalid"}, 400
            if result > max_n or result < min_n:
                return {"message": name + " = " + str(result) + " is invalid"}, 400
            return result

        def get_float_parameter(name, min_n, max_n):
            try:
                result = float(request.args.get(name))
            except:
                return {"message": name + " is invalid"}, 400
            if result > max_n or result < min_n:
                return {"message": name + " = " + str(result) + " is invalid"}, 400
            return result

        def get_other_parameter(name):
            try:
                result = int(request.args.get(name))
            except:
                return {"message": name + " is invalid"}, 400
            return result

        rooms = get_int_parameter('Rooms', 1, 16)
        distance = get_float_parameter('Distance', 0, 64.1)
        bedroom = get_int_parameter('Bedroom', 0, 10)
        bathroom = get_int_parameter('Bathroom', 0, 8)
        car = get_int_parameter('Car', 0, 10)
        landsize = get_int_parameter('Landsize', 0, 76000)
        type = get_other_parameter('Type')
        method = get_other_parameter('Method')
        field = get_other_parameter('Field')
        region = get_other_parameter('Regionname')

        att_list = [rooms, type, method, field, region, distance, bedroom, bathroom, car, landsize]
        result = predict_price(att_list)  # AI程序调用

        return {'predict price': "{}".format(result)}, 200


if __name__ == '__main__':
    app.run(debug=True)
