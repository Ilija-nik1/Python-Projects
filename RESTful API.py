from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'  # SQLite database
db = SQLAlchemy(app)
api = Api(app)

# Create a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

# Create a schema for user serialization
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# API resources
class UserResource(Resource):
    def get(self):
        users = User.query.all()
        result = users_schema.dump(users)
        return result

    def post(self):
        try:
            args = user_schema.load(request.get_json())
        except ValidationError as err:
            return {'error': err.messages}, 400

        user = User(args['name'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully', 'id': user.id}

class UserItemResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            result = user_schema.dump(user)
            return result
        else:
            return {'error': 'User not found'}, 404

    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            try:
                args = user_schema.load(request.get_json())
            except ValidationError as err:
                return {'error': err.messages}, 400

            user.name = args['name']
            db.session.commit()
            return {'message': 'User updated successfully', 'id': user.id}
        else:
            return {'error': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully', 'id': user.id}
        else:
            return {'error': 'User not found'}, 404

api.add_resource(UserResource, '/users')
api.add_resource(UserItemResource, '/users/<int:user_id>')

if __name__ == '__main__':
    db.create_all()  # Create the database tables
    app.run(debug=True)