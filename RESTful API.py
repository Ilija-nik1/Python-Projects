import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from marshmallow import ValidationError as maValidationError

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'  # SQLite database
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')  # Replace with a secret key for JWT

# Initialize database and extensions
db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Create a simple User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Create a schema for user serialization
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# API resources
class UserListResource(Resource):
    @jwt_required
    def get(self):
        try:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)
        except ValueError:
            return jsonify(error='Invalid page or per_page value'), 400

        users = User.query.paginate(page, per_page, error_out=False)

        # Check if there is a previous page
        prev_page = request.base_url + '?page=' + str(users.prev_num) if users.has_prev else None
        # Check if there is a next page
        next_page = request.base_url + '?page=' + str(users.next_num) if users.has_next else None

        result = {
            'users': users_schema.dump(users.items),
            'total_pages': users.pages,
            'current_page': users.page,
            'total_users': users.total,
            'prev_page': prev_page,
            'next_page': next_page,
        }
        return jsonify(result)

    def post(self):
        try:
            args = user_schema.load(request.get_json())
        except maValidationError as err:
            return jsonify(error=err.messages), 400

        existing_user = User.query.filter_by(email=args['email']).first()
        if existing_user:
            return jsonify(error='User with this email already exists'), 409

        user = User(args['name'], args['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully', id=user.id), 201

class UserResource(Resource):
    @jwt_required
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user_schema.dump(user))
        else:
            return jsonify(error='User not found'), 404

    @jwt_required
    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            try:
                args = user_schema.load(request.get_json())
            except maValidationError as err:
                return jsonify(error=err.messages), 400

            existing_user = User.query.filter(User.email == args['email'], User.id != user.id).first()
            if existing_user:
                return jsonify(error='User with this email already exists'), 409

            user.name = args['name']
            user.email = args['email']
            db.session.commit()
            return jsonify(message='User updated successfully', id=user.id)
        else:
            return jsonify(error='User not found'), 404

    @jwt_required
    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(message='User deleted successfully', id=user.id)
        else:
            return jsonify(error='User not found'), 404

class UserSearchResource(Resource):
    @jwt_required
    def get(self):
        search_query = request.args.get('q')
        if not search_query:
            return jsonify(error='Search query parameter "q" is missing'), 400

        users = User.query.filter(User.name.ilike(f'%{search_query}%')).all()
        result = users_schema.dump(users)
        return jsonify(result)

class UserCountResource(Resource):
    @jwt_required
    def get(self):
        count = User.query.count()
        return jsonify(count=count)

class UserValidationResource(Resource):
    def get(self):
        username = request.args.get('username')
        if not username:
            return jsonify(error='Username parameter "username" is missing'), 400

        existing_user = User.query.filter_by(name=username).first()
        if existing_user:
            return jsonify(valid=False)
        else:
            return jsonify(valid=True)

# Add API resources
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserSearchResource, '/users/search')
api.add_resource(UserCountResource, '/users/count')
api.add_resource(UserValidationResource, '/users/validate')

if __name__ == '__main__':
    # Create the database tables
    db.create_all()
    # Run the Flask app in debug mode
    app.run(debug=True)