from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

db.drop_all()

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(254),nullable=False)
    password = db.Column(db.String(128), nullable=False)
    interests = db.relationship('UserInterestModel',backref='user')

    def __repr__(self):
        return f'User(username = {self.username}, email = {self.email}, password = {len(self.password) * "*"})'

class InterestModel(db.Model):
    __tablename__ = 'interest'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(4000), nullable = False)
    users = db.relationship('UserInterestModel', backref='interest')

    def __repr__(self):
        return f'Interest(title = {self.title}, description = {self.description})'

class UserInterestModel(db.Model):
    __tablename__ = 'userinterest'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    interest_id = db.Column(db.Integer, db.ForeignKey('interest.id'), primary_key=True)

    def __repr__(self):
        return f'Interest(title = {self.user_id}, description = {self.interest_id})'

db.create_all()

user_put_args = reqparse.RequestParser()
user_put_args.add_argument('username', type=str, help='Username of user is required', required=True)
user_put_args.add_argument('email', type=str, help='Email of user is required', required = True)
user_put_args.add_argument('password', type=str, help='Password of user is required', required = True)

user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument('username', type=str, help='Username of user')
user_patch_args.add_argument('email', type=str, help='Email of user')
user_patch_args.add_argument('password', type=str, help='Password of user')

interest_put_args = reqparse.RequestParser()
interest_put_args.add_argument('title', type=str, help='Title of interest', required = True)
interest_put_args.add_argument('description', type=str, help='Description of interest', required = True)

interest_patch_args = reqparse.RequestParser()
interest_patch_args.add_argument('title', type=str, help='Title of interest')
interest_patch_args.add_argument('description', type=str, help='Description of interest')

user_resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
}

interest_resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
}

user_interest_resource_fields = {
    'user_id': fields.Integer,
    'interest_id': fields.Integer
}

class User(Resource):
    @marshal_with(user_resource_fields)
    def get(self, id):
        result = UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404)
        return result, 200
    @marshal_with(user_resource_fields)
    def put(self, id):
        args = user_put_args.parse_args()
        result = UserModel.query.filter_by(id=id).first()
        if result:
            abort(409)
        user = UserModel(id=id, username=args['username'], email=args['email'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201
    @marshal_with(user_resource_fields)
    def delete(self, id):
        result=UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404)
        db.session.delete(result)
        db.session.commit()
        return '', 204
    @marshal_with(user_resource_fields)
    def patch(self,id):
        args = user_patch_args.parse_args()
        result = UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404)
    
        if(args['username']):
            result.username = args['username']
        if(args['email']):
            result.email = args['email']
        if(args['password']):
            result.password = args['password']

        db.session.commit()
        return result

api.add_resource(User,'/user/<int:id>')

class Interest(Resource):

    @marshal_with(interest_resource_fields)
    def get(self,id):
        interest = InterestModel.query.filter_by(id=id).first()
        if not interest:
            abort(404)
        return interest
    @marshal_with(interest_resource_fields)
    def put(self, id):
        args = interest_put_args.parse_args()
        interest = InterestModel.query.filter_by(id=id).first()
        if interest:
            return abort(409)

        interest = InterestModel(id=id, title=args['title'], description=args['description'])
        db.session.add(interest)
        db.session.commit()
        return interest, 201
    def delete(self, id):
        result=InterestModel.query.filter_by(id=id).first()
        if not result:
            abort(404)
        db.session.remove(result)
        db.session.commit()
        return '', 204
    @marshal_with(interest_resource_fields)
    def patch(self,id):
        args = interest_patch_args.parse_args()
        result = InterestModel.query.filter_by(id=id).first()
        if not result:
            abort(404)
        
        if(args['title']):
            result['title']=args['title']
        if(args['description']):
            result['description']=args['description']

        db.session.commit()
        return result

api.add_resource(Interest,'/interest/<int:id>')


class UserInterest(Resource):
    @marshal_with(user_interest_resource_fields)
    def get(self,user_id, interest_id):
        user_interest = UserInterestModel.query.filter_by(user_id=user_id,interest_id=interest_id).first()
        if not user_interest:
            abort(404)
        return user_interest
    @marshal_with(user_interest_resource_fields)
    def put(self, user_id, interest_id):
        interest = UserInterestModel.query.filter_by(user_id=user_id,interest_id=interest_id).first()
        if interest:
            return abort(409)

        user_interest = UserInterestModel(user_id=user_id, interest_id=interest_id)
        db.session.add(user_interest)
        db.session.commit()
        return user_interest, 201

api.add_resource(UserInterest,'/userinterest/<int:user_id>/<int:interest_id>')


if __name__ == '__main__':
    app.run(debug=True)