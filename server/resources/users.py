#resources/users.py
from flask_restful import Resource
from models.users import UserModel
import resources.parsers


class UserRegister(Resource):
    '''
    Testing resource, which registers a new user.
    '''

    def post(self):
        '''
        If a user not already exists, the user will be created.
        '''
        data = resources.parsers.ParseUser.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400 #bad request

        user = UserModel(**data) # UserModel(**data)
        #user = UserModel(data['username'],data['password']) # UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully."}, 201 #created
